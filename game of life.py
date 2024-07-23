"""



   ______                               _          ______                              ____   __    _ ____
  / ____/___  ____ _      ______ ___  _( )_____   / ____/___ _____ ___  ___     ____  / __/  / /   (_) __/__
 / /   / __ \/ __ \ | /| / / __ `/ / / /// ___/  / / __/ __ `/ __ `__ \/ _ \   / __ \/ /_   / /   / / /_/ _ \
/ /___/ /_/ / / / / |/ |/ / /_/ / /_/ / (__  )  / /_/ / /_/ / / / / / /  __/  / /_/ / __/  / /___/ / __/  __/
\____/\____/_/ /_/|__/|__/\__,_/\__, / /____/   \____/\__,_/_/ /_/ /_/\___/   \____/_/    /_____/_/_/  \___/
                               /____/

                                         BY: equationslayer12


        *=====================================================================================*
        *-------------------------------------------------------------------------------------*
        *=====================================================================================*
        *=*                                                                                 *=*
        *=*    The Game of Life is played on an two-dimensional rectangular grid of cells.  *=*
        *=*    Each cell can be either alive or dead.                                       *=*
        *=*    The status of each cell changes "generation" (each turn of the game),        *=*
        *=*    depending on the statuses of that cell's 8 neighbors.                        *=*
        *=*    Neighbors of a cell are cells that touch that cell,                          *=*
        *=*    either horizontal, vertical, or diagonal from that cell.                     *=*
        *=*                                                                                 *=*
        *=====================================================================================*
        *-------------------------------------------------------------------------------------*
        *=====================================================================================*


                     OPTIONS:
        left-click      :       Place an alive cell
        right-click     :       Place a dead cell

        Right           :       Next generation
        Left            :       Last generation (Careful! might delete data from next generation)
        Space           :       (Toggle) Automatically go through generations
        r               :       Reset board (delete all the data)
"""


import pygame
import numpy as np
from asyncio import sleep
import random

pygame.init()
pygame.display.set_caption('Game of life')

# CONSTANTS
BLOCK_SIZE = 10     # SIZE OF EACH CELL ON THE SCREEN (BLOCK_SIZE * BLOCK_SIZE)
SHAPE = 100, 100    # SIZE OF GRID OF CELLS (you might want to change that depending on the size of your screen)
TIME_GAP = 0.09     # when played, how much time between each generations (in seconds)

TIME_GAP = int(TIME_GAP * 1000)
WIDTH, HEIGHT = SHAPE[0] * BLOCK_SIZE, SHAPE[1] * BLOCK_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (212, 212, 212)
RANDOM = ((255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238))

BACKGROUND_COLOR = WHITE
GRID_COLOR = GRAY
CIRCLE_COLOR = BLACK

# WHITE, BLACK = BLACK, WHITE

async def loop(game):
    global run_loop

    while run_loop:
        game.create_page()
        await sleep(1)


class Game:
    def __init__(self, array):
        self.arrays = {0: Board(array)}
        self.num_of_pages = 1
        self.current_display = 0
        self.current_board = self.arrays[self.current_display]

    def create_page(self):
        self.arrays[self.num_of_pages] = Board(self.arrays[self.num_of_pages - 1].forward())
        self.num_of_pages += 1
        self.current_display += 1
        self.current_board = self.arrays[self.current_display]
        # print(f"{self.current_display + 1} / {self.num_of_pages}")

    def back(self):
        if self.current_display <= 0:
            return
        del self.arrays[self.current_display]
        self.num_of_pages -= 1
        self.current_display -= 1
        self.current_board = self.arrays[self.current_display]

    def update(self):
        self.current_board.update()


class Board:
    def __init__(self, array):
        self.array = array
        self.screen = screen

    def draw_grid(self):
        for x in range(WIDTH // BLOCK_SIZE):
            for y in range(HEIGHT // BLOCK_SIZE):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                                   BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1,)

    def draw_creatures(self):
        for y in range(len(self.array)):
            for x in range(len(self.array[y])):
                if self.array[y, x] == 1:
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (
                        x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2),
                                       BLOCK_SIZE // 2)

    def forward(self):
        new_board = np.copy(self.array)
        for y in range(len(new_board)):
            for x in range(len(new_board[y])):
                neighbors = get_neighbors((y, x), self.array)
                n_sum = sum(neighbors)
                if not (n_sum == 2 or n_sum == 3):
                    new_board[y, x] = 0
                    continue
                if n_sum == 3:
                    new_board[y, x] = 1
                    continue
        return new_board

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_creatures()
        pygame.display.update()

    def add_dot(self, position, item):
        x, y = position
        x, y = x // BLOCK_SIZE, y // BLOCK_SIZE
        self.array[y, x] = item


def get_neighbors(pos, array):
    y, x = pos
    neighbors = []
    for change_y in range(-1, 2):
        new_y = y + change_y
        if new_y < 0:
            continue
        if new_y >= SHAPE[1]:
            break

        for change_x in range(-1, 2):
            if change_y == 0 and change_x == 0:
                continue
            new_x = x + change_x
            if new_x <= -1:
                continue
            if new_x >= SHAPE[0]:
                break

            neighbors.append(array[new_y, new_x])
    return neighbors


run = True

game = Game(np.zeros((SHAPE[1], SHAPE[0])))

next_board = pygame.USEREVENT

hold_left = False
hold_right = False

run_loop = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                hold_left = True
            elif event.button == 3:
                hold_right = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                hold_left = False
            elif event.button == 3:
                hold_right = False
        if event.type == next_board:
            game.create_page()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game.create_page()
            elif event.key == pygame.K_LEFT:
                game.back()
            elif event.key == pygame.K_p:
                print(game.current_board.array)
            elif event.key == pygame.K_r:
                del game
                game = Game(np.zeros((SHAPE[1], SHAPE[0])))
                pygame.time.set_timer(next_board, 0)
                run_loop = False

            elif event.key == pygame.K_SPACE:
                if not run_loop:
                    pygame.time.set_timer(next_board, TIME_GAP)
                    run_loop = True
                else:
                    pygame.time.set_timer(next_board, 0)
                    run_loop = False

    if hold_left:
        game.current_board.add_dot(pygame.mouse.get_pos(), 1)
    elif hold_right:
        game.current_board.add_dot(pygame.mouse.get_pos(), 0)

    game.update()
    clock.tick(60)
pygame.quit()
