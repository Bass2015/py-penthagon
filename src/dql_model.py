import random
import events
import constants


class Brain():
    def __init__(self) -> None:
        self.network = Network()
    
    def act(self, state=None):
        return self.network(state)
    
class Network:
    def __init__(self):
        self.conv = []
        self.fully_connected = []
        # self.build_network()
        self.layer = Conv2D()
    def __call__(self, state):
        action = self.forward(state)
        return action

    def build_network(self):
        self.conv.append((Conv2D(4, 32, kernel_size=7, stride=4), 
                            Conv2D(32, 64, kernel_size=5, stride=2),
                            Conv2D(4, 32, kernel_size=7, stride=4)))

    def forward(self, state=None):
        # hacer forward por las convolutional layers
        # flatten el output
        # hacer forward con las fully connected
        return self.layer.forward(state)

class Conv2D:
    def __init__(self) -> None:
        pass

    def forward(self, state):
        return 0