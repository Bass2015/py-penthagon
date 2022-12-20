import random
import numpy as np
import json
import time
from dql_model import Network
from collections import deque
from optim import SGD
from events import deboog
from js import document, Blob, URL


XP_BUFFER_SIZE = 10000
BATCH_SIZE = 32
LEARNING_RATE = 0.01
SYNC_NETS_FRAMES = 100
EPSILON_MAX = 1.0
EPSILON_MIN = 0.01
EPSILON_FINAL_FRAME_DECAY = 300000
GAMMA = 0.99

END_TRAINING_SCORE = 400

class Brain():
    def __init__(self) -> None:
        self.network = Network()
        self.target_net = Network()
        self.optim = SGD(self.network, LEARNING_RATE)
        # self.sync_nets()
        self.xp_buffer = ExperienceBuffer(XP_BUFFER_SIZE)
        self.frame_count = 0
        self.epsilon = 0
        self.scores = []
        self.best_mean_score = None
        self.costs = []
        self.training_info = {
            'game_number': [],
            'frames': [],
            'epsilon': [],
            'score': [],
            'mean_score': [], 
            'best_mean_score':[],
            'cost': []
        }

    def sync_nets(self):
        self.target_net.set_params(self.network.get_params())
        self.network.save_params('net')
        self.target_net.save_params('tgt_net')
    
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
            self.train_loop()
        self.epsilon = max(EPSILON_MIN, EPSILON_MAX - self.frame_count/EPSILON_FINAL_FRAME_DECAY)
        return self.action

    def train_loop(self):
        if self.frame_count % SYNC_NETS_FRAMES == 0:
            self.sync_nets()
        # Zero_grad -> vaciar las dw y db de las layers.
        self.network.zero_grad(BATCH_SIZE)
        states, actions, rewards, next_states = self.xp_buffer.sample(BATCH_SIZE)
        losses = np.zeros(BATCH_SIZE)
        for batch_index in range(len(states)):
            loss, d_loss = self.calculate_d_loss(states[batch_index], actions[batch_index], rewards[batch_index], next_states[batch_index])
            self.network.backward(d_loss, batch_index)
            losses[batch_index] = loss
        self.optim.step()
        self.costs.append(losses.mean())
               
    def calculate_d_loss(self, state, action, reward, next_state):
        """Calculates the predicted Q value (the state-action pairs that we chose) and 
        the expected Q value (with the target net and Bellman equation. 
        Then, calculate the derivative of the loss"""
        Q = self.network(state)
        Q_pred = Q[0,action]
        Q_exp = self.bellman_equation(reward, next_state)
        loss = 0.5 * (Q_pred - Q_exp)**2
        # Derivative with respect of the action taken
        d_loss = np.zeros_like(Q)
        d_loss[0, action] = Q_exp - Q_pred
        return loss,  d_loss
        
    def bellman_equation(self, reward, next_state):
        Q = self.target_net(next_state)
        maxQ = np.max(Q)
        # Bellman equation
        return reward + GAMMA * maxQ

    def on_match_ended(self, reward, final_score, env_state):
        self.xp_buffer.append(self.state, self.action, reward, env_state)
        self.scores.append(final_score)
        mean_score = np.mean(self.scores[-100:])
        if self.best_mean_score is None or mean_score > self.best_mean_score:
            self.network.save_params(mean_score)
            self.best_mean_score = mean_score
        self.save_info(final_score, mean_score)
        self.show_info(final_score, mean_score)
        self.costs.clear()
        if mean_score >= END_TRAINING_SCORE:
            # Trigger Training Ended event
            self.save_info_document()
            
    
    def save_info_document(self):
        tag = document.createElement('a')
        blob = Blob.new([json.dumps(self.training_info)])
        tag.innerHTML = f'Training information'
        tag.href = URL.createObjectURL(blob)
        document.getElementById('training_info').appendChild(tag)
        return tag
    
    def save_info(self, final_score, mean_score):
        self.training_info['game_number'].append(len(self.scores))
        self.training_info['frames'].append(self.frame_count)
        self.training_info['epsilon'].append(self.epsilon)
        self.training_info['score'].append(final_score)
        self.training_info['mean_score'].append(mean_score)
        self.training_info['best_mean_score'].append(self.best_mean_score)
        self.training_info['cost'].append(np.asarray(self.costs).mean())
    
    def show_info(self, final_score, mean_score):
        deboog(f"""Game No: {len(self.scores)}, 
                   Score: {final_score},
                   Frames: {self.frame_count}, 
                   Epsilon: {self.epsilon},
                   Mean Score: {mean_score}, 
                   Mean Cost: {np.asarray(self.costs).mean()}""")

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
        # ERRORRR
        # ragged nested sequence on actions while creating np.array
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
        
