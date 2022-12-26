import numpy as np
# from events import deboog

class Layer:
    def __init__(self):
        pass

    def forward(self, inputs, vectorized=True):
        pass
    
    def single_backward(self, dy, vectorized=True):
        pass

    def zero_grad(self):
        pass
    
    def extract(self):
        return {self.name+'.weights':self.weights, self.name+'.bias':self.bias}

    def feed(self, weights, bias):
        self.weights = weights
        self.bias = bias

class Conv2D(Layer):
    # Agregar la función de activación. 
    def __init__(self, inputs_channel, num_filters, kernel_size=4, padding=0, stride=1, name="", activation='relu'):
        # weight size: (numfilters, inchannels, kernel_size, kernel_size)
        # bias size: (num_filters) 
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.in_channels = inputs_channel
        self.init_params()
        self.stride = stride
        self.name = name
        self.activation = activation
        super(Layer, self).__init__()

    def init_params(self):
        self.weights = np.zeros((self.num_filters, self.in_channels, self.kernel_size, self.kernel_size), dtype=np.float32)
        self.bias = np.zeros((self.num_filters, 1), dtype=np.float32)
        for filter in range(0,self.num_filters):
            self.weights[filter,:,:,:] = np.random.normal(loc=0, 
                            scale=(2. / (self.in_channels * self.kernel_size * self.kernel_size)**0.5), 
                            size=(self.in_channels, self.kernel_size, self.kernel_size))

    
    def forward(self, inputs, vectorized=True):
        if not vectorized:
            return self.single_forward(inputs)
        return self.vect_forward(inputs)

    def single_forward(self, inputs):
        C = inputs.shape[0]
        W = inputs.shape[1]
        H = inputs.shape[2]
        self.inputs = inputs #np.zeros((C, W, H))
        WW = int((W - self.kernel_size) / self.stride + 1)
        HH = int((H - self.kernel_size) / self.stride + 1)
        outputs = np.zeros((self.num_filters, WW, HH), dtype=np.float32)
        for f in range(self.num_filters):
            for w in range(0, WW, self.stride):
                for h in range(0, HH, self.stride):
                    outputs[f,w,h] = np.sum(self.inputs[:,w:w+self.kernel_size,h:h+self.kernel_size] * self.weights[f,:,:,:]) + self.bias[f]
        return outputs

    def vect_forward(self, inputs):
        """Accepts four dimensional input, with shape (Batch, Channels, Height, Width)"""
        input_windows = self.stride_input(inputs)
        self.inputs = inputs, input_windows
        output = np.einsum('bchwkt,fckt->bfhw', input_windows, self.weights) + self.bias[np.newaxis, :, np.newaxis]
        return output 

    def stride_input(self, inputs):
        batch_size, channels, h, w = inputs.shape
        b_stride, c_stride, h_stride, w_stride = inputs.strides
        out_w = int((w - self.kernel_size) / self.stride + 1)
        out_h = int((h - self.kernel_size) / self.stride + 1)
        new_shape = (batch_size, channels, out_h, out_w, self.kernel_size, self.kernel_size)
        new_strides = (b_stride, c_stride, self.stride * h_stride, self.stride * w_stride, h_stride, w_stride)
        return np.lib.stride_tricks.as_strided(inputs, new_shape, new_strides)
    
    def stride_dy(self, dy):
        inputs, _ = self.inputs
        b, c, out_h, out_w = inputs.shape
        b_stride, c_stride, h_stride, w_stride = dy.strides
        new_shape = (b, c, out_h, out_w, self.kernel_size, self.kernel_size)
        new_strides = (b_stride, c_stride, h_stride, w_stride, h_stride, w_stride)
        return np.lib.stride_tricks.as_strided(dy, new_shape, new_strides)

    def zero_grad(self):
        self.weight_gradients = np.zeros(self.weights.shape, dtype=np.float32)
        self.bias_gradients = np.zeros(self.bias.shape, dtype=np.float32)

    def backward(self, dy, vectorized=True):
        if not vectorized:
            return self.single_backward(dy)
        return self.vect_backward(dy)

    def single_backward(self, dy):
        C, W, H = self.inputs.shape
        dx = np.zeros(self.inputs.shape, dtype=np.float32)
        dw = np.zeros(self.weights.shape, dtype=np.float32)
        db = np.zeros(self.bias.shape, dtype=np.float32)
        # Calcular derivada de relu
        F, W, H = dy.shape
        for f in range(F):
            for w in range(0, W, self.stride):
                for h in range(0, H, self.stride):
                    dw[f, :, :, :] += dy[f, w, h] * self.inputs[:, w:w+self.kernel_size, h:h+self.kernel_size]
                    dx[:,w:w+self.kernel_size,h:h+self.kernel_size]+=dy[f,w,h]*self.weights[f,:,:,:]

        for f in range(F):
            db[f] = np.sum(dy[f, :, :])

        # Saving the gradiens to calculate the mean later
        self.weight_gradients += dw
        self.bias_gradients += db
        return dx
    
    def vect_backward(self, dy):
        _, input_windows = self.inputs
        self.dw = np.einsum('bchwkt,bfhw->bfckt', input_windows, dy).mean(0)
        self.db = dy.mean(axis=(0,2,3))[:,np.newaxis]
        rot_kernels = np.rot90(self.weights, 2, axes=(2,3))
        dy_windows = self.stride_dy(dy)
        dx = np.einsum('bchwkt,fckt->bchw', dy_windows, rot_kernels)
        return dx

class FullyConnected(Layer):

    def __init__(self, num_inputs, num_outputs, name=''):
        self.init_params(num_inputs, num_outputs)
        self.name = name
        super(Layer, self).__init__()


    def init_params(self, num_inputs, num_outputs):
        self.weights = np.random.normal(0, 2/num_inputs**0.5, (num_inputs, num_outputs))
        self.bias = np.zeros((num_outputs, 1), dtype=np.float32)

    def forward(self, inputs, vectorized=True):
        self.inputs = inputs
        return np.dot(self.inputs, self.weights) + self.bias.T

    def zero_grad(self):
        self.weight_gradients = np.zeros(self.weights.shape, dtype=np.float32)
        self.bias_gradients = np.zeros(self.bias.shape, dtype=np.float32)
        
    def backward(self, dy, vectorized=True):
        if dy.shape[0] == self.inputs.shape[0]:
            dy = dy.T
        dw = dy.dot(self.inputs)
        db = np.sum(dy, axis=1, keepdims=True)
        dx = np.dot(dy.T, self.weights.T)
        
        # Saving the gradiens to calculate the mean later
        self.weight_gradients += dw.T
        self.bias_gradients += db
        return dx

class Flatten(Layer):
    def __init__(self):
        super(Layer, self).__init__()

    def forward(self, inputs, vectorized=True):
        if len(inputs.shape) != 4:
            inputs = inputs[np.newaxis,: , :, :]
        B, self.C, self.W, self.H = inputs.shape
        return inputs.reshape(B, self.C*self.W*self.H)

    def backward(self, dy, vectorized=True):
        if len(dy.shape) == 3:
            return dy.reshape(self.C, self.W, self.H)
        return dy.reshape(dy.shape[0], self.C, self.W, self.H)
  
class ReLU(Layer):
    def __init__(self):
        super(Layer, self).__init__()


    def forward(self, inputs, vectorized=True):
        self.inputs = inputs
        return np.maximum(0, inputs)

    def backward(self, dl, vectorized=True):
        return np.greater(self.inputs, 0.).astype(np.float32)
        
   