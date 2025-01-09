import pygame
from classes import Game

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 24
ROWS = 20
COLS = 10
BOARD_W, BOARD_H = CELL_SIZE*COLS, CELL_SIZE*ROWS
TPADDING = (HEIGHT - CELL_SIZE*ROWS) // 2  # the empty space at the top of the game

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(ROWS, COLS)

game.print()

def drawBoard(screen):
    startX = (WIDTH - CELL_SIZE*COLS) // 2
    #draw the grid
    for row in range(ROWS + 1):  # horizontal
        pygame.draw.line(screen, "blue", (startX, TPADDING + row*CELL_SIZE), (startX + BOARD_W, TPADDING + row*CELL_SIZE))

    for col in range(COLS + 1):  # vertical
        pygame.draw.line(screen, "blue", (startX + col*CELL_SIZE, TPADDING), (startX + col*CELL_SIZE, TPADDING + BOARD_H))

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawBoard(screen)

    pygame.display.flip()