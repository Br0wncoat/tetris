# 1. Import necessary libraries
import sys
import pygame
from pygame.locals import *
import random
import time

# 2. Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 25
FPS = 10

class Tetromino:
    shapes = [
        # I
        [['.....',
          '.....',
          'OOOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '..O..',
          '..O..'],
         ['.....',
          '.....',
          'OOOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '..O..',
          '..O..']],
        # O
        [['.....',
          '.....',
          '.OO..',
          '.OO..',
          '.....']],
        # T
        [['.....',
          '.....',
          '..O..',
          '.OOO.',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '..O..',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '..O..',
          '.....'],
         ['.....',
          '..O..',
          '.OO..',
          '..O..',
          '.....']],
        # S
        [['.....',
          '.....',
          '..OO.',
          '.OO..',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '...O.',
          '.....'],
         ['.....',
          '.....',
          '..OO.',
          '.OO..',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '...O.',
          '.....']],
        # Z
        [['.....',
          '.....',
          '.OO..',
          '..OO.',
          '.....'],
         ['.....',
          '...O.',
          '..OO.',
          '..O..',
          '.....'],
         ['.....',
          '.....',
          '.OO..',
          '..OO.',
          '.....'],
         ['.....',
          '...O.',
          '..OO.',
          '..O..',
          '.....']],
        # J
        [['.....',
          '.....',
          '.O...',
          '.OOO.',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '.OO..',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '...O.',
          '.....'],
         ['.....',
          '.OO..',
          '..O..',
          '..O..',
          '.....']],
        # L
        [['.....',
          '.....',
          '...O.',
          '.OOO.',
          '.....'],
         ['.....',
          '..OO.',
          '...O.',
          '...O.',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '.O...',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '..OO.',
          '.....']]
    ]

    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.shape = self.shapes[shape_idx]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        return self.shape[self.rotation]

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def place_tetromino(self, tetromino):
        shape = tetromino.shape[tetromino.rotation]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    self.grid[tetromino.y + y][tetromino.x + x] = 1

    def is_collision(self, tetromino, x, y, rotation):
        shape = tetromino.shape[rotation]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[y + i][x + j] != 0 or x + j < 0 or x + j >= self.width):
                        return True
                except IndexError:
                    if cell == 'O':
                        return True
        return False

    def remove_line(self, line):
        self.grid.pop(line)
        self.grid.insert(0, [0 for _ in range(self.width)])

    def clear_lines(self):
        lines_cleared = 0
        full_rows = []

        # Check for full rows
        for row in range(self.height):
            if all(self.grid[row][col] != 0 for col in range(self.width)):
                full_rows.append(row)

        if full_rows:
            # Blinking animation
            for _ in range(3):
                for row in full_rows:
                    self.grid[row] = [0] * self.width
                render()
                pygame.display.update()
                time.sleep(0.1)

                for row in full_rows:
                    self.grid[row] = [1] * self.width
                render()
                pygame.display.update()
                time.sleep(0.1)

            # Remove full rows
            for row in full_rows:
                del self.grid[row]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1

        return lines_cleared

    def is_game_over(self):
        return any(cell == 1 for cell in self.grid[0])

# Other imports and class definitions above

def new_tetromino():
    shape_idx = random.randint(0, len(Tetromino.shapes) - 1)
    x = board.width // 2
    y = 0
    return Tetromino(x, y, shape_idx)

# Render game objects (draw the game board, tetrominos, etc.) ->

def draw_grid():
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, (cell * 255, cell * 255, cell * 255),
                             (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1,
                              GRID_SIZE - 1))


def draw_tetromino(tetromino, x_offset=0, y_offset=0):
    shape = tetromino.shape[tetromino.rotation]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell == 'O':
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((tetromino.x + x + x_offset) * GRID_SIZE,
                                  (tetromino.y + y + y_offset) * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))


def draw_next_tetromino():
    draw_tetromino(next_tetromino, x_offset=12, y_offset=2)


def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (WINDOW_WIDTH - 200, 50))

def draw_ui():
    draw_next_tetromino()
    draw_score()

def display_game_over(score):
    font = pygame.font.Font(None, 48)
    text = font.render(f'Game Over', True, (255, 255, 255))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 + score_text.get_height()))
    pygame.display.flip()


def render():
    screen.fill((0, 0, 0))
    draw_grid()
    draw_tetromino(current_tetromino)
    draw_ui()
    pygame.display.flip()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

# Initialize game objects and variables
width = 15
height = 20
board = GameBoard(width, height)
current_tetromino = new_tetromino()
next_tetromino = new_tetromino()
score = 0
fall_time = 0
fall_speed = 500  # Adjust this value to change the falling speed, lower is faster

# Main game loop
while True:
    current_time = pygame.time.get_ticks()

    # Enable key repeat with a delay of 300ms
    pygame.key.set_repeat(200)

    # Handle events (user input, piece movement, etc.)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                if not board.is_collision(current_tetromino,
                                          current_tetromino.x,
                                          current_tetromino.y + 1,
                                          current_tetromino.rotation):
                    current_tetromino.y += 1
            elif event.key == K_LEFT:
                if not board.is_collision(current_tetromino,
                                          current_tetromino.x - 1,
                                          current_tetromino.y,
                                          current_tetromino.rotation):
                    current_tetromino.x -= 1
            elif event.key == K_RIGHT:
                if not board.is_collision(current_tetromino,
                                          current_tetromino.x + 1,
                                          current_tetromino.y,
                                          current_tetromino.rotation):
                    current_tetromino.x += 1
            elif event.key == K_SPACE:
                new_rotation = (current_tetromino.rotation + 1) % len(
                    current_tetromino.shape)
                if not board.is_collision(current_tetromino,
                                          current_tetromino.x,
                                          current_tetromino.y, new_rotation):
                    current_tetromino.rotation = new_rotation

    # Update game state (collision handling, line clearing, etc.)
    if current_time - fall_time > fall_speed:
        if not board.is_collision(current_tetromino, current_tetromino.x,
                                  current_tetromino.y + 1,
                                  current_tetromino.rotation):
            current_tetromino.y += 1
        else:
            board.place_tetromino(current_tetromino)
            lines_cleared = board.clear_lines()
            # Update score based on the lines cleared
            score += lines_cleared * 100

            current_tetromino = next_tetromino
            next_tetromino = new_tetromino()

            # Check if the new Tetromino can be placed at the starting position
            if board.is_collision(current_tetromino, current_tetromino.x,
                                  current_tetromino.y, current_tetromino.rotation):
                display_game_over(score)
                while True:
                    event = pygame.event.wait()
                    if event.type == QUIT or (
                            event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        # Reset game state and start a new game
                        board = GameBoard(width, height)
                        current_tetromino = new_tetromino()
                        next_tetromino = new_tetromino()
                        score = 0
                        fall_time = 0
                        break

            fall_time = current_time

    render()
    clock.tick(FPS)



