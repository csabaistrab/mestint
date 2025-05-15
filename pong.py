### pong.py

import pygame
import numpy as np
from tqdm import tqdm

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

SIGN_EMPTY = " "
SIGN_BALL = "o"
SIGN_PLAYER = "x"

SPACE_SIZE = (20, 20)
ZOOM_SIZE = 10

ACTION_IDLE = "IDLE"
ACTION_LEFT = "LEFT"
ACTION_RIGHT = "RIGHT"
ACTIONS = [ACTION_IDLE, ACTION_LEFT, ACTION_RIGHT]

rect_x = SPACE_SIZE[0] // 2
rect_y = SPACE_SIZE[1] - 1
rect_change_x = 0
rect_change_y = 0
rect_size_x = 5
rect_size_to_sides_x = rect_size_x // 2
rect_size_y = 1

ball_x = SPACE_SIZE[0] // 2
ball_y = 1
ball_change_x = 1
ball_change_y = 1
ball_size_to_sides = 1

state_to_id = {}
num_states = SPACE_SIZE[0] * SPACE_SIZE[1] * SPACE_SIZE[0] * SPACE_SIZE[1] * 2 * 2
screen = 0
agent = None


def drawrect(screen, x, y):
    pygame.draw.rect(screen, RED, [(x - rect_size_to_sides_x) * ZOOM_SIZE, y * ZOOM_SIZE, ZOOM_SIZE * rect_size_x, ZOOM_SIZE])

def encode_state(ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y):
    return (ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y)

def reset():
    global ball_change_x, ball_change_y, ball_size_to_sides, ball_x, ball_y
    global rect_x, rect_y, rect_change_x, rect_change_y

    ball_change_x, ball_change_y = 1, 1
    ball_size_to_sides = 1
    ball_x, ball_y = SPACE_SIZE[0] // 2, 1
    rect_x, rect_y = SPACE_SIZE[0] // 2, SPACE_SIZE[1] - 1
    rect_change_x = rect_change_y = 0

def init_pong():
    global screen, clock
    pygame.init()
    size = (SPACE_SIZE[0] * ZOOM_SIZE, SPACE_SIZE[1] * ZOOM_SIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("pong")
    clock = pygame.time.Clock()

def play_episodes(n_episodes=10000, max_epsilon=1.0, min_epsilon=0.05, decay_rate=0.0001, gamma=0.99, learn=True, viz=False, human=False, log=False):
    global ball_change_x, ball_change_y, ball_size_to_sides
    global ball_x, ball_y, rect_x, rect_y, rect_change_x, rect_change_y
    global state_to_id, clock

    rewards = []
    epsilon_history = []

    for episode in tqdm(range(n_episodes)):
        done = False
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        total_reward = 0
        reset()

        state = encode_state(ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y)
        if state not in state_to_id:
            state_to_id[state] = len(state_to_id)

        while not done:
            reward = 0
            screen.fill(BLACK)

            if not human:
                action = agent.act(state=state_to_id[state], epsilon=epsilon)
                action_name = ACTIONS[action]
                rect_change_x = -1 if action_name == ACTION_LEFT else 1 if action_name == ACTION_RIGHT else 0
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            rect_change_x = -1
                        elif event.key == pygame.K_RIGHT:
                            rect_change_x = 1
                    elif event.type == pygame.KEYUP:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            rect_change_x = 0

            rect_x += rect_change_x

            if ball_x < 0 or ball_x > SPACE_SIZE[0]:
                ball_change_x *= -1
                ball_x = max(0, min(SPACE_SIZE[0], ball_x))
            if ball_y < 0:
                ball_change_y *= -1
                ball_y = 0
            elif ball_y == SPACE_SIZE[1] - 1 and rect_x - rect_size_to_sides_x <= ball_x <= rect_x + rect_size_to_sides_x:
                ball_change_y *= -1
                reward = 1
            elif ball_y > SPACE_SIZE[1] - 1:
                reward = -1
                done = True

            new_state = encode_state(ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y)
            if new_state not in state_to_id:
                state_to_id[new_state] = len(state_to_id)

            ball_x += ball_change_x
            ball_y += ball_change_y

            if rect_x - rect_size_to_sides_x < 0 or rect_x > SPACE_SIZE[0] - rect_size_to_sides_x - 1:
                reward = -1
                done = True

            if viz:
                pygame.draw.rect(screen, WHITE, [(ball_x - ball_size_to_sides) * ZOOM_SIZE, (ball_y - ball_size_to_sides) * ZOOM_SIZE, ZOOM_SIZE, ZOOM_SIZE])
                drawrect(screen, rect_x, rect_y)
                pygame.display.flip()
                clock.tick(60)

            if learn:
                agent.learn(state_to_id[state], action, reward, state_to_id[new_state], gamma)

            state = new_state
            total_reward += reward

        if log:
            print("Total reward:", total_reward)
        rewards.append(total_reward)
        epsilon_history.append(epsilon)

    return rewards, epsilon_history


### main.py
from qla import QLearningAgent
import pong
import matplotlib.pyplot as plt

pong.init_pong()
pong.agent = QLearningAgent(n_states=pong.num_states, n_actions=3, learning_rate=1.0)

rewards, epsilon_history = pong.play_episodes(
    n_episodes=50000,
    max_epsilon=1.0,
    min_epsilon=0.05,
    decay_rate=0.0001,
    gamma=0.95,
    learn=True,
    viz=False,
    human=False,
    log=False
)

plt.plot(epsilon_history)
plt.title("Epsilon decay")
plt.xlabel("Episodes")
plt.ylabel("Epsilon")
plt.grid(True)
plt.show()
