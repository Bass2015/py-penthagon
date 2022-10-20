import random
from cnnB.model.layers import Conv2D, FullyConnected as FC

class Brain():
    def __init__(self) -> None:
        self.network = Network()
    
    def act(self, state):
        return self.network(state)
    
class Network:
    def __init__(self):
        self.conv = []
        self.fully_connected = []
        self.build_network()

    def build_network(self):
        self.conv.append((Conv2D(4, 32, kernel_size=7, stride=4), 
                            Conv2D(32, 64, kernel_size=5, stride=2),
                            Conv2D(4, 32, kernel_size=7, stride=4)))

    def forward(self):
        # hacer forward por las convolutional layers
        # flatten el output
        # hacer forward con las fully connected
        pass