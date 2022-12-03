from dql_model import Network
import random
import numpy as np
from events import deboog

XP_MAX_SIZE = 1000
SYNC_NETS = 100
EPSILON_MAX = 1.0
EPSILON_MIN = 0.01
EPSILON_FINAL_FRAME_DECAY = 300000

class Brain():
    def __init__(self) -> None:
        self.network = Network()
        self.xp_buffer = []
        self.frame_count = 0
        self.epsilon = EPSILON_MAX
    
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
            # self.save_exp(self.state, self.action, reward, env_state)
            pass
        self.state = env_state
        if random.random() < self.epsilon:
            self.action = random.randint(0, 8)
        else:
            self.action = self.act(self.state)
        if len(self.xp_buffer) >=  XP_MAX_SIZE:
            self.update_net()
        self.epsilon = max(EPSILON_MIN, EPSILON_MAX - self.frame_count/EPSILON_FINAL_FRAME_DECAY)
        deboog(f'Epsilon: {self.epsilon}')
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