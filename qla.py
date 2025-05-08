### qla.py
import random
import numpy as np

class QLearningAgent:
    def __init__(self, n_states, n_actions, learning_rate):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        self.q_table = np.zeros((n_states, n_actions))

    def act(self, state, epsilon):
        if random.uniform(0, 1) > epsilon:
            return np.argmax(self.q_table[state])
        else:
            return random.randint(0, self.n_actions - 1)

    def learn(self, state, action, reward, new_state, gamma):
        old_value = self.q_table[state][action]
        new_estimate = reward + gamma * max(self.q_table[new_state])
        self.q_table[state][action] = old_value + self.learning_rate * (new_estimate - old_value)