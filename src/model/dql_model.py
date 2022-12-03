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
    
    def save_params(self, loss=0):
        params = {}
        for layer in range(len(self.layers)):
            params[layer] = {}
            if not isinstance(self.layers[layer], Flatten):
                params[layer]['w'] = self.layers[layer].weights.tolist()
                params[layer]['b'] = self.layers[layer].bias.tolist()
        tag = self.create_tag(loss, params)
        # self.download_params(tag)

    def download_params(self, tag):
        tag.download = 'filename'
        tag.click()

    def create_tag(self, loss, params):
        tag = document.createElement('a')
        blob = Blob.new([json.dumps(params)])
        tag.innerHTML = f'Loss: {loss}'
        tag.href = URL.createObjectURL(blob)
        document.getElementById('params').appendChild(tag)

        return tag
    
    def load_params(self):
        w = document.getElementById('weights').innerHTML
        params = json.loads(w)
        for layer in range(len(self.layers)):
            if not isinstance(self.layers[layer], Flatten):
                self.layers[layer].weights =  np.asarray(params[str(layer)]['w'])
                self.layers[layer].bias = np.asarray(params[str(layer)]['b'])
    


