import random
import events
import constants
import numpy as np
import time
from js import document, Blob, URL
import json

class Brain():
    def __init__(self) -> None:
        self.network = Network()
    
    def act(self, state=None):
        out = self.network(state)
        max_ind = np.argmax(out, axis=1)
        events.deboog(f'Output: {out}, Max_ind: {max_ind}')
        return max_ind
    
    def train(self, state=None):
        return self.act(state)
    
class Network:
    def __init__(self):
        self.layers = []
        self.build_network()
        self.load_params()
        
    def __call__(self, state):
        action = self.forward(state)
        return action

    def build_network(self):
        # build convolutional layers
        self.layers.append(Conv2D(4, 32, kernel_size=7, stride=4, name='conv1'))
        self.layers.append(Conv2D(32, 64, kernel_size=5, stride=2, name='conv2'))
        self.layers.append(Conv2D(64, 64, kernel_size=3, stride=1, name='conv3'))
        
        self.layers.append(Flatten())

        #build fully connected layers
        self.layers.append(FullyConnected(1600, 512, name='fc1'))
        self.layers.append(FullyConnected(512, 9, name='fc2'))

    def forward(self, state=None):
        # hacer forward por las convolutional layers
        x = state
        for layer in self.layers:
            output = layer.forward(x)
            x = output
        return output
    
    def save_params(self):
        params = {}
        for layer in range(len(self.layers)):
            params[layer] = {}
            if not isinstance(self.layers[layer], Flatten):
                params[layer]['w'] = self.layers[layer].weights.tolist()
                params[layer]['b'] = self.layers[layer].bias.tolist()
        json.dumps(params)
        tag = document.createElement('a')
        blob = Blob.new([json.dumps(params)])
        tag.href = URL.createObjectURL(blob)
        tag.download = 'filename'
        tag.click()
    
    def load_params(self):
        w = document.getElementById('weights').innerHTML
        params = json.loads(w)
        for layer in range(len(self.layers)):
            if not isinstance(self.layers[layer], Flatten):
                self.layers[layer].weights =  np.asarray(params[str(layer)]['w'])
                self.layers[layer].bias = np.asarray(params[str(layer)]['b'])
    
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

    def backward(self, dy):

        C, W, H = self.inputs.shape
        dx = np.zeros(self.inputs.shape)
        dw = np.zeros(self.weights.shape)
        db = np.zeros(self.bias.shape)

        F, W, H = dy.shape
        for f in range(F):
            for w in range(0, W, self.stride):
                for h in range(0, H, self.stride):
                    dw[f,:,:,:]+=dy[f,w,h]*self.inputs[:,w:w+self.K,h:h+self.K]
                    dx[:,w:w+self.K,h:h+self.K]+=dy[f,w,h]*self.weights[f,:,:,:]

        for f in range(F):
            db[f] = np.sum(dy[f, :, :])

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

    def backward(self, dy):

        if dy.shape[0] == self.inputs.shape[0]:
            dy = dy.T
        dw = dy.dot(self.inputs)
        db = np.sum(dy, axis=1, keepdims=True)
        dx = np.dot(dy.T, self.weights.T)

        self.weights -= self.lr * dw.T
        self.bias -= self.lr * db

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
    def backward(self, dy):
        return dy.reshape(self.C, self.W, self.H)
    def extract(self):
        return

def ReLU(x):
    return np.maximum(0, x)

def ReLU_grad(x):
    return np.greater(x, 0.).astype(np.float32)