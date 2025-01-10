import pygame
import random
from classes import Game, I, J, L, O, S, T, Z

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 24
ROWS = 20
COLS = 10
BOARD_W, BOARD_H = CELL_SIZE*COLS, CELL_SIZE*ROWS
TPADDING = (HEIGHT - CELL_SIZE*ROWS) // 2  # the empty space at the top of the game

pieces = [I, J, L, O, S, T, Z]
turnTime = 60 # how long for each tick, in frames
deltaTime = 1 # subtracted from timer

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(ROWS, COLS)

def drawBoard(screen):
    screen.fill("black")
    startX = (WIDTH - CELL_SIZE*COLS) // 2
    #draw the grid
    for row in range(ROWS + 1):  # horizontal
        pygame.draw.line(screen, "blue", (startX, TPADDING + row*CELL_SIZE), (startX + BOARD_W, TPADDING + row*CELL_SIZE))

    for col in range(COLS + 1):  # vertical
        pygame.draw.line(screen, "blue", (startX + col*CELL_SIZE, TPADDING), (startX + col*CELL_SIZE, TPADDING + BOARD_H))

    for i in range(ROWS):
        for j in range(COLS):
            if game.board[i][j] != 0:
                screen.blit(game.idToImage[game.board[i][j]], (startX + j*CELL_SIZE, TPADDING + i*CELL_SIZE)) #takes a number from the board and draws the correct tile at the correct position


getNewActive = True #do we need a new active piece

run = True
while run:
    clock.tick(FPS)
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game.shift(1)
            if event.key == pygame.K_LEFT:
                game.shift(-1)

    #starts a new active piece
    if getNewActive:
        game.activePiece = random.choice(pieces)()
        game.spawn(game.activePiece)
        game.activeCords = game.activePiece.sCords
        game.activeCenter = game.activePiece.sCenter
        getNewActive = False

    # Timer for falling piece, triggers new piece when piece reaches bottom
    turnTime -= deltaTime
    if turnTime <= 0:
        if not game.movePiece():
            getNewActive = True
        turnTime = 60

    drawBoard(screen)

    pygame.display.flip()