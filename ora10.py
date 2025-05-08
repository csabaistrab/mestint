import numpy as np
import pygame
import numpy as np
from tqdm import tqdm

def main():
    # Initialize q-table values to 0
    Q = np.zeros((5, 10))
    print(Q)
    # Globális Paraméterek

    # Színek
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Jelek a játék dekódolásához

    # - üres (egy labdához vagy játékoshoz nem tartozó cella)
    SIGN_EMPTY = " "
    # - labda
    SIGN_BALL = "o"
    # - játékos (a téglalap)
    SIGN_PLAYER = "x"

    # Az "ablak" nagy ítás nélküli mérete
    SPACE_SIZE = (20, 20)

    # Ezt a felhasználói felület ablakának felnagyítására fogjuk használni
    # A felhasználói felület ablakának mérete SPACE_SIZE * ZOOM_SIZE
    ZOOM_SIZE = 10

    # 3 műveletünk van, amelyeket az ügynök bármikor megtehet:

    # - üresjárat (nem változik a helyzet)
    ACTION_IDLE = "IDLE"
    # - bal
    ACTION_LEFT = "LEFT"
    # - jobb
    ACTION_RIGHT = "RIGHT"

    ACTIONS = [
        ACTION_IDLE,
        ACTION_LEFT,
        ACTION_RIGHT
    ]

    # A lapát kezdő koordinátái
    rect_x = SPACE_SIZE[0] // 2
    rect_y = SPACE_SIZE[1] - 1

    # A lapát kezdeti sebessége
    rect_change_x = 0
    rect_change_y = 0

    rect_size_x = 5
    rect_size_to_sides_x = rect_size_x // 2
    rect_size_y = 1

    # A labda kezdeti helyzete
    ball_x = SPACE_SIZE[0] // 2
    ball_y = 1

    # A labda sebessége
    ball_change_x = 1
    ball_change_y = 1
    ball_size_to_sides = 1

    # A dictionary-t arra fogjuk használni,
    # hogy nyomon követhessük azokat az állapotokat,
    # amelyekkel eddig találkoztunk
    state_to_id = {}

    # A lehetséges állapotok száma összesen
    num_states = SPACE_SIZE[0] * SPACE_SIZE[1] * SPACE_SIZE[0] * SPACE_SIZE[1] * 2 * 2

    # Képernyő méret
    screen = 0

    # Agent
    agent = None
    print(RED)
    print(SIGN_PLAYER)
    print(SPACE_SIZE, ZOOM_SIZE)
    print(ACTIONS)

    return

if __name__ == '__main__':
    main()