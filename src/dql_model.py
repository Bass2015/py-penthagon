import random
from cnn.src.model import Network

class Brain():
    def __init__(self) -> None:
        self.network = Network()
    
    def act(self, state):
        return self.network(state)
    