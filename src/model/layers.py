import numpy as np
# from events import deboog

class Layer:
    def __init__(self):
        pass

    def forward(self, inputs):
        pass
    
    def extract(self):
        return {self.name+'.weights':self.weights, self.name+'.bias':self.bias}

    def feed(self, weights, bias):
        self.weights = weights
        self.bias = bias

class Conv2D(Layer):
    def __init__(self, inputs_channel, num_filters, kernel_size=4, padding=0, stride=1, name="", activation='relu'):
        # weight size: (numfilters, inchannels, kernel_size, kernel_size)
        # bias size: (num_filters) 
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.in_channels = inputs_channel
        self.__init_params()
        self.stride = stride
        self.name = name
        self.activation = activation
        super(Layer, self).__init__()

    def __init_params(self):
        self.weights = np.zeros((self.num_filters, self.in_channels, self.kernel_size, self.kernel_size), dtype=np.float32)
        self.bias = np.zeros((self.num_filters, 1), dtype=np.float32)
        for filter in range(0,self.num_filters):
            self.weights[filter,:,:,:] = np.random.normal(loc=0, 
                            scale=(2. / (self.in_channels * self.kernel_size * self.kernel_size)**0.5), 
                            size=(self.in_channels, self.kernel_size, self.kernel_size))

    def forward(self, inputs):
        """Accepts four dimensional input, with shape (Batch, Channels, Height, Width)"""
        input_windows = self.__stride_input(inputs)
        self.inputs = inputs, input_windows
        output = np.einsum('bchwkt,fckt->bfhw', input_windows, self.weights) + self.bias[np.newaxis, :, np.newaxis]
        return output 

    def __stride_input(self, inputs):
        batch_size, channels, h, w = inputs.shape
        b_stride, c_stride, h_stride, w_stride = inputs.strides
        out_w = int((w - self.kernel_size) / self.stride + 1)
        out_h = int((h - self.kernel_size) / self.stride + 1)
        new_shape = (batch_size, channels, out_h, out_w, self.kernel_size, self.kernel_size)
        new_strides = (b_stride, c_stride, self.stride * h_stride, self.stride * w_stride, h_stride, w_stride)
        return np.lib.stride_tricks.as_strided(inputs, new_shape, new_strides)
    
    def backward(self, dy):
        _, input_windows = self.inputs
        self.dw = np.einsum('bchwkt,bfhw->bfckt', input_windows, dy).mean(0)
        self.db = dy.mean(axis=(0,2,3))[:,np.newaxis]
        rot_kernels = np.rot90(self.weights, 2, axes=(2,3))
        dy_windows = self.__stride_dy(dy)
        dx = np.einsum('bchwkt,fckt->bchw', dy_windows, rot_kernels)
        return dx

    def __stride_dy(self, dy):
        inputs, _ = self.inputs
        b, c, out_h, out_w = inputs.shape
        b_stride, c_stride, h_stride, w_stride = dy.strides
        new_shape = (b, c, out_h, out_w, self.kernel_size, self.kernel_size)
        new_strides = (b_stride, c_stride, h_stride, w_stride, h_stride, w_stride)
        return np.lib.stride_tricks.as_strided(dy, new_shape, new_strides)

class FullyConnected(Layer):

    def __init__(self, num_inputs, num_outputs, name=''):
        self.init_params(num_inputs, num_outputs)
        self.name = name
        super(Layer, self).__init__()

    def init_params(self, num_inputs, num_outputs):
        self.weights = np.random.normal(0, 2/num_inputs**0.5, (num_inputs, num_outputs))
        self.bias = np.zeros((num_outputs, 1), dtype=np.float32)

    def forward(self, inputs):
        self.inputs = inputs
        return np.dot(self.inputs, self.weights) + self.bias.T

   
    def backward(self, dy):
        batch_size = dy.shape[0]
        if dy.shape[0] == self.inputs.shape[0]:
            dy = dy.T
        self.dw = (dy.dot(self.inputs)/batch_size).T
        self.db = np.mean(dy, axis=1, keepdims=True)
        dx = np.dot(dy.T, self.weights.T)
        return dx

class Flatten(Layer):
    def __init__(self):
        super(Layer, self).__init__()

    def forward(self, inputs):
        if len(inputs.shape) != 4:
            inputs = inputs[np.newaxis,: , :, :]
        B, self.C, self.W, self.H = inputs.shape
        return inputs.reshape(B, self.C*self.W*self.H)

    def backward(self, dy):
        if len(dy.shape) == 3:
            return dy.reshape(self.C, self.W, self.H)
        return dy.reshape(dy.shape[0], self.C, self.W, self.H)
  
class ReLU(Layer):
    def __init__(self):
        super(Layer, self).__init__()

    def forward(self, inputs):
        self.inputs = inputs
        return np.maximum(0, inputs)

    def backward(self, dl):
        return np.greater(self.inputs, 0.).astype(np.float32)
        
   