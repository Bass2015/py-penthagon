from layers import Flatten


# Esta clase recibe el batch size, suma los valores de los gradientes y hace la media 
class Optimizer:
    def __init__(self, net, lr):
        self.net = net
        self.lr = lr

    def step(self):
        for layer in self.net.layers:
            self.update_params(layer)
    
    def update_params(layer):
        pass

class SGD(Optimizer):
    def update_params(self, layer):
        if not isinstance(layer, Flatten):
            dw = layer.weight_gradients.mean(axis=0)
            db = layer.bias_gradients.mean(axis=0)
            layer.weights -= self.lr * dw
            layer.bias -= self.lr * db