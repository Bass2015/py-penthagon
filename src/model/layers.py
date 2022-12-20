import numpy as np
# from events import deboog

class Conv2D:
    # Agregar la función de activación. 
    def __init__(self, inputs_channel, num_filters, kernel_size=4, padding=0, stride=1, learning_rate=0.01, name="", activation='relu'):
        # weight size: (numfilters, inchannels, kernel_size, kernel_size)
        # bias size: (num_filters) 
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.in_channels = inputs_channel
        self.init_params()
        self.stride = stride
        self.lr = learning_rate
        self.name = name
        self.activation = activation

    def init_params(self):
        self.weights = np.zeros((self.num_filters, self.in_channels, self.kernel_size, self.kernel_size))
        self.bias = np.zeros((self.num_filters, 1))
        for filter in range(0,self.num_filters):
            self.weights[filter,:,:,:] = np.random.normal(loc=0, 
                            scale=np.sqrt(1. / (self.in_channels * self.kernel_size * self.kernel_size)), 
                            size=(self.in_channels, self.kernel_size, self.kernel_size))

    def forward(self, inputs):
        # input size: (C, W, H)
        # output size: (N, F ,WW, HH)
        C = inputs.shape[0]
        W = inputs.shape[1]
        H = inputs.shape[2]
        self.inputs = inputs #np.zeros((C, W, H))
        WW = int((W - self.kernel_size) / self.stride + 1)
        HH = int((H - self.kernel_size) / self.stride + 1)
        outputs = np.zeros((self.num_filters, WW, HH))
        for f in range(self.num_filters):
            for w in range(0, WW, self.stride):
                for h in range(0, HH, self.stride):
                    outputs[f,w,h] = np.sum(self.inputs[:,w:w+self.kernel_size,h:h+self.kernel_size] * self.weights[f,:,:,:]) + self.bias[f]
        if self.activation == 'relu':
            return ReLU(outputs)
        else:
            return outputs

    def zero_grad(self, batch_size):
        grads_shape = list(self.weights.shape)
        grads_shape.insert(0, batch_size)
        self.weight_gradients = np.zeros(grads_shape)
        b_grads_shape = list(self.bias.shape)
        b_grads_shape.insert(0, batch_size)
        self.bias_gradients = np.zeros(b_grads_shape)

    def backward(self, dy, batch_index):
        print(f'{self.name}--->, W.shape: {self.weights.shape}, DY.shape: {dy.shape}, Inputs: {self.inputs.shape}')

        C, W, H = self.inputs.shape
        dx = np.zeros(self.inputs.shape)
        dw = np.zeros(self.weights.shape)
        db = np.zeros(self.bias.shape)
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
        self.weight_gradients[batch_index] = dw
        self.bias_gradients[batch_index] = db
        print(f'\tDW.shape: {dw.shape}, Grads.shape: {self.weight_gradients.shape}')
        self.weights -= self.lr * dw
        self.bias -= self.lr * db
        return dx

    def extract(self):
        return {self.name+'.weights':self.weights, self.name+'.bias':self.bias}

    def feed(self, weights, bias):
        self.weights = weights
        self.bias = bias

class FullyConnected:

    def __init__(self, num_inputs, num_outputs, learning_rate=0.01, name=''):
        self.init_params(num_inputs, num_outputs)
        self.lr = learning_rate
        self.name = name

    def init_params(self, num_inputs, num_outputs):
        self.weights = 0.01 * np.random.rand(num_inputs, num_outputs)
        self.bias = np.zeros((num_outputs, 1))

    def forward(self, inputs):
        self.inputs = inputs
        return np.dot(self.inputs, self.weights) + self.bias.T

    def zero_grad(self, batch_size):
        w_grads_shape = list(self.weights.shape)
        w_grads_shape.insert(0, batch_size)
        self.weight_gradients = np.zeros(w_grads_shape)
        b_grads_shape = list(self.bias.shape)
        b_grads_shape.insert(0, batch_size)
        self.bias_gradients = np.zeros(b_grads_shape)
        

    def backward(self, dy, batch_index):
        print(f'{self.name}--->, W.shape: {self.weights.shape}, DY.shape: {dy.shape}, Inputs: {self.inputs.shape}')
        if dy.shape[0] == self.inputs.shape[0]:
            dy = dy.T
        dw = dy.dot(self.inputs)
        db = np.sum(dy, axis=1, keepdims=True)
        dx = np.dot(dy.T, self.weights.T)
        
        # Saving the gradiens to calculate the mean later
        self.weight_gradients[batch_index] = dw.T
        self.bias_gradients[batch_index] = db

        print(f'\tDW.shape: {dw.shape}, Grads.shape: {self.weight_gradients.shape}')

        # self.weights -= self.lr * dw.T
        # self.bias -= self.lr * db

        return dx

    def extract(self):
        return {self.name+'.weights':self.weights, self.name+'.bias':self.bias}

    def feed(self, weights, bias):
        self.weights = weights
        self.bias = bias

class Flatten:
    def __init__(self):
        pass

    def forward(self, inputs):
        self.C, self.W, self.H = inputs.shape
        return inputs.reshape(1, self.C*self.W*self.H)

    def backward(self, dy, batch_index):
        return dy.reshape(self.C, self.W, self.H)
        
    def extract(self):
        return
    
    def zero_grad(self, batch_size):
        return

def ReLU(x):
    return np.maximum(0, x)

def ReLU_grad(x):
    return np.greater(x, 0.).astype(np.float32)