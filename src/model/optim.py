from layers import Flatten, ReLU


# Esta clase recibe el batch size, suma los valores de los gradientes y hace la media 
class Optimizer:
    def __init__(self, net, lr):
        self.net = net
        self.lr = lr

    def step(self, batch_size):
        for layer in self.net.layers:
            self.update_params(layer, batch_size)
    
    def update_params(layer):
        pass

class SGD(Optimizer):
    def update_params(self, layer, batch_size):
        if not (isinstance(layer, Flatten) or (isinstance(layer, ReLU))):
            # dw = layer.weight_gradients / batch_size
            # db = layer.bias_gradients / batch_size
            layer.weights -= self.lr * layer.dw
            layer.bias -= self.lr * layer.db