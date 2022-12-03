from dql_model import Network
import random
import numpy as np

XP_MAX_SIZE = 1000
SYNC_NETS = 100

class Brain():
    def __init__(self) -> None:
        self.network = Network()
        self.xp_buffer = []
        self.frame_count = 0
        self.epsilon = 1
    
    def act(self, state=None):
        out = self.network(state)
        max_ind = np.argmax(out, axis=1)
        # events.deboog(f'Output: {out}, Max_ind: {max_ind}')
        return max_ind
    
    def train(self, reward, first_frame, env_state=None):
        # El reward se tiene que calcular en la clase Agent, a partir del 
        # score, antes de llamar a brain.train
        self.frame_count += 1
        if not first_frame:
            self.save_exp(self.state, self.action, reward, env_state)
        self.state = env_state
        if self.epsilon < random.random():
            self.action = random.randint(0, 8)
        else:
            self.action = self.act(self.state)
        if len(self.xp_buffer) >=  XP_MAX_SIZE:
            self.update_net()
        return self.action

    def update_net(self):
        if self.frame_count % SYNC_NETS == 0:
            #sync_nets()
            pass
        # zero_grad
        # sample from xp_buffer
        # calculate loss
        # backwards propagation
        # optimize parameters
        pass