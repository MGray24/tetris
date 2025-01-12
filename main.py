import pygame
import random
from classes import Game, I, J, L, O, S, T, Z

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 24
ROWS = 20
COLS = 10
BOARD_W, BOARD_H = CELL_SIZE*COLS, CELL_SIZE*ROWS
TPADDING = (HEIGHT - CELL_SIZE*ROWS) // 2  # the empty space at the top of the game
font = pygame.font.Font("fonts/simpleblock.ttf", 24)
nextText = font.render('Next', False, "black")

pieces = [I, J, L, O, S, T, Z]
turnTime = 30 # how long for each tick, in frames
currentTime = turnTime
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
            if game.board[i][j] == 0 and game.boardCopy[i][j] != 0:
                screen.blit(game.idToImage[game.boardCopy[i][j]], (startX + j*CELL_SIZE, TPADDING + i*CELL_SIZE)) #takes a number from the board and draws the correct tile at the correct position
            elif game.board[i][j] != 0:
                screen.blit(game.idToImage[game.board[i][j]], (startX + j*CELL_SIZE, TPADDING + i*CELL_SIZE)) #takes a number from the board and draws the correct tile at the correct position

def drawNextBox(screen, pieceNext):
    pygame.draw.line(screen, "white", (450, TPADDING + 10), (570, TPADDING + 10), 21) #top
    pygame.draw.line(screen, "white", (450, TPADDING), (450, TPADDING + 140)) #left
    pygame.draw.line(screen, "white", (570, TPADDING), (570, TPADDING + 140)) #right
    pygame.draw.line(screen, "white", (450, TPADDING + 140), (570, TPADDING + 140)) #bottom
    screen.blit(nextText, (452, TPADDING))
    for x, y in pieceNext.sCords:
        screen.blit(game.idToImage[pieceNext.id], (x*CELL_SIZE+180+pieceNext.nextShift[0], y*CELL_SIZE+TPADDING+pieceNext.nextShift[1]))

def newActive():
    global pieceNext, getNewActive
    game.clear()
    game.activePiece = pieceNext
    pieceNext = random.choice(pieces)()
    game.spawn(game.activePiece)
    game.activeCords = game.activePiece.sCords
    game.activeCenter = game.activePiece.sCenter
    getNewActive = False

getNewActive = True #do we need a new active piece
pieceNext = random.choice(pieces)()

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
            elif event.key == pygame.K_LEFT:
                game.shift(-1)
            elif event.key == pygame.K_UP:
                game.rotate(game.activePiece, 1)
            elif event.key == pygame.K_z:
                game.rotate(game.activePiece, -1)
            elif event.key == pygame.K_SPACE:
                while game.movePiece():
                    pass
                newActive()
            game.updateGhost()

    #starts a new active piece
    if getNewActive:
        newActive()


    # Timer for falling piece, triggers new piece when piece reaches bottom
    currentTime -= deltaTime
    if currentTime <= 0:
        if not game.movePiece():
            getNewActive = True

        game.updateGhost()
        currentTime = turnTime


    drawBoard(screen)
    drawNextBox(screen, pieceNext)


    pygame.display.flip()