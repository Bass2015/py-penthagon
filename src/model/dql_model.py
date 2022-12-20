import random
import events
import constants
import numpy as np
import time
import json
from layers import *
from js import document, Blob, URL

class Network:
    def __init__(self):
        self.layers = []
        self.build_network()
        # self.load_params()
        
    def __call__(self, state):
        action = self.forward(state)
        return action

    def build_network(self):
        self.layers.append(Conv2D(4, 32, kernel_size=7, stride=4, name='conv1'))
        self.layers.append(ReLU())
        self.layers.append(Conv2D(32, 64, kernel_size=5, stride=2, name='conv2'))
        self.layers.append(ReLU())
        self.layers.append(Conv2D(64, 64, kernel_size=3, stride=1, name='conv3'))
        self.layers.append(ReLU())
        
        self.layers.append(Flatten())

        self.layers.append(FullyConnected(1600, 512, name='fc1'))
        self.layers.append(ReLU())
        self.layers.append(FullyConnected(512, 9, name='fc2'))

    def forward(self, state=None):
        # hacer forward por las convolutional layers
        x = state
        for layer in self.layers:
            output = layer.forward(x)
            x = output
        return output
    
    def backward(self, dl, batch_index):
        for layer in reversed(self.layers):
            dl = layer.backward(dl, batch_index)
             
    def zero_grad(self, batch_size):
        for layer in self.layers:
            layer.zero_grad(batch_size)

    def get_params(self):
        params = {}
        for layer in range(len(self.layers)):
            params[str(layer)] = {}
            #Arreglar esto v. Ponerlo como método en Layer
            if not (isinstance(self.layers[layer], Flatten) or isinstance(self.layers[layer], ReLU)):
                params[str(layer)]['w'] = self.layers[layer].weights.tolist()
                params[str(layer)]['b'] = self.layers[layer].bias.tolist()
        return params
    
    def set_params(self, params):
        for layer in range(len(self.layers)):
            if not (isinstance(self.layers[layer], Flatten) or isinstance(self.layers[layer], ReLU)):
                self.layers[layer].weights =  np.asarray(params[str(layer)]['w'])
                self.layers[layer].bias = np.asarray(params[str(layer)]['b'])

    def save_params(self, mean_score=0):
        params = self.get_params()
        tag = self.create_tag(mean_score, params)
        # self.download_params(tag)

    def create_tag(self, mean_score, params):
        tag = document.createElement('a')
        blob = Blob.new([json.dumps(params)])
        tag.innerHTML = f'Mean_score: {mean_score}'
        tag.href = URL.createObjectURL(blob)
        document.getElementById('params').appendChild(tag)
        return tag

    def download_params(self, tag):
        tag.download = 'filename'
        tag.click()
    
    def load_params(self):
        w = document.getElementById('weights').innerHTML
        params = json.loads(w)
        self.set_params(params)