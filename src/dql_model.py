import keras
import random

class Brain():
    def __init__(self) -> None:
        self.network = None
    
    def act(self, state):
        # q_values = self.network(state)
        # _, action = torch.max(q_values, dim=1)
        return random.randint(0,17)
    