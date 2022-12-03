from dql_model import Network
import random
import numpy as np
from collections import deque
from events import deboog
import time

XP_BUFFER_SIZE = 10000
SYNC_NETS = 1000
EPSILON_MAX = 1.0
EPSILON_MIN = 0.01
EPSILON_FINAL_FRAME_DECAY = 300000

class Brain():
    def __init__(self) -> None:
        self.network = Network()
        self.xp_buffer = ExperienceBuffer(XP_BUFFER_SIZE)
        self.frame_count = 0
        self.epsilon = EPSILON_MAX
    
    def act(self, state=None):
        out = self.network(state)
        max_ind = np.argmax(out, axis=1)
        # events.deboog(f'Output: {out}, Max_ind: {max_ind}')
        return max_ind
    
    def train(self, reward, first_frame, env_state=None):
        self.frame_count += 1
        if not first_frame:
            self.xp_buffer.append(self.state, self.action, reward, env_state)
        self.state = env_state
        if random.random() < self.epsilon:
            self.action = random.randint(0, 8)
        else:
            self.action = self.act(self.state)
        if len(self.xp_buffer) >=  XP_BUFFER_SIZE:
            self.update_net()
        self.epsilon = max(EPSILON_MIN, EPSILON_MAX - self.frame_count/EPSILON_FINAL_FRAME_DECAY)
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

class ExperienceBuffer:
    def __init__(self, max_size):
        self.buffer = {
            'states': deque(maxlen=max_size),
            'actions': deque(maxlen=max_size),
            'rewards': deque(maxlen=max_size),
            'next_states': deque(maxlen=max_size)
        }
    
    def __len__(self):
        return len(self.buffer['states'])
    
    def append(self, state, action, reward, next_state):
        self.buffer['states'].append(state)
        self.buffer['actions'].append(action)
        self.buffer['rewards'].append(reward)
        self.buffer['next_states'].append(next_state)
    
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer['states']), 
                            size=batch_size, 
                            replace=False)
        states = [self.buffer['states'][i] for i in indices]
        actions = [self.buffer['actions'][i] for i in indices]
        rewards = [self.buffer['rewards'][i] for i in indices]
        next_states = [self.buffer['next_states'][i] for i in indices]
        return np.array(states), \
               np.array(actions), \
               np.array(rewards, dtype=np.float32), \
               np.array(next_states)
        
