import pygame
import random
import pickle

class Ball:
    def __init__(self):
        self.x = 300
        self.y = 200
        self.vx = random.choice([-4, 4])
        self.vy = random.choice([-4, 4])
        self.size = 10

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.y <= 0 or self.y >= 400:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size, self.size))

class Paddle:
    def __init__(self):
        self.x = 20
        self.y = 200
        self.v = 4
        self.width = 10
        self.height = 60

    def move(self, direction):
        self.y += direction * self.v
        self.y = max(min(self.y, 400 - self.height), 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

    def get_state(self, ball, paddle):
        return (
            ball.x // 20,
            ball.y // 20,
            (ball.vx > 0),
            (ball.vy > 0),
            paddle.y // 20
        )

    def choose_action(self, state):
        if random.random() < self.epsilon or state not in self.q_table:
            return random.choice([-1, 0, 1])
        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {-1: 0, 0: 0, 1: 0}
        if next_state not in self.q_table:
            self.q_table[next_state] = {-1: 0, 0: 0, 1: 0}

        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())

        self.q_table[state][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

class PongGame:
    def __init__(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.agent = QLearningAgent()
        self.score = 0

    def step(self):
        state = self.agent.get_state(self.ball, self.paddle)
        action = self.agent.choose_action(state)
        self.paddle.move(action)
        self.ball.move()

        reward = 0
        if self.ball.x <= self.paddle.x + self.paddle.width and self.paddle.y < self.ball.y < self.paddle.y + self.paddle.height:
            self.ball.vx *= -1
            reward = 1
            self.score += 1
        elif self.ball.x < 0:
            self.ball = Ball()
            reward = -1
            self.score = 0

        next_state = self.agent.get_state(self.ball, self.paddle)
        self.agent.update(state, action, reward, next_state)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.ball.draw(screen)
        self.paddle.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pong = PongGame()
    clock = pygame.time.Clock()

    for _ in range(10000):
        pong.step()

    with open("agent.pkl", "wb") as f:
        pickle.dump(pong.agent, f)

    print("Tréning kész.")
    pygame.quit()
