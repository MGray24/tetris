import copy
import pygame
import random
from classes import Game, I, J, L, O, S, T, Z

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/backgroundTechno.mp3")
pygame.mixer.music.play(-1)
thudSound = pygame.mixer.Sound("sounds/thump.wav")
clearSound = pygame.mixer.Sound("sounds/lineclear.wav")
clearSound.set_volume(1)
thudSound.set_volume(1)

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
holdText = font.render('Hold', False, "black")

pieces = [I, J, L, O, S, T, Z]
turnTime = 30 # how long for each tick, in frames
currentTime = turnTime
deltaTime = 1 # subtracted from timer

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(ROWS, COLS)


def drawBoard(screen):
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

def drawHoldBox(screen, pieceHold):
    pygame.draw.line(screen, "white", (30, TPADDING + 10), (150, TPADDING + 10), 21)  # top
    pygame.draw.line(screen, "white", (30, TPADDING), (30, TPADDING + 140))  # left
    pygame.draw.line(screen, "white", (150, TPADDING), (150, TPADDING + 140))  # right
    pygame.draw.line(screen, "white", (30, TPADDING + 140), (150, TPADDING + 140))  # bottom
    screen.blit(holdText, (32, TPADDING))
    if pieceHold != None:
        for x, y in pieceHold.sCords:
            screen.blit(game.idToImage[pieceHold.id], (
            x * CELL_SIZE + 180 + pieceHold.holdShift[0], y * CELL_SIZE + TPADDING + pieceHold.holdShift[1]))


def newActive():
    global pieceNext, getNewActive, canHold, GAME_OVER
    game.clear(clearSound)
    game.activePiece = pieceNext
    pieceNext = random.choice(pieces)()
    GAME_OVER = not game.spawn(game.activePiece)
    game.activeCords = game.activePiece.sCords
    game.activeCenter = copy.copy(game.activePiece.sCenter)
    getNewActive = False
    canHold = True

getNewActive = True #do we need a new active piece
pieceNext = random.choice(pieces)()
pieceHold = None
canHold = True
GAME_OVER = False

run = True
while run:
    clock.tick(FPS)
    screen.fill("black")

    if GAME_OVER:
        pygame.mixer.music.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.draw.rect(screen, "red",(180, TPADDING, 240, 480))
        drawBoard(screen)
        drawNextBox(screen, pieceNext)
        drawHoldBox(screen, pieceHold)
        pygame.display.flip()
        continue


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
            elif event.key == pygame.K_c:
                if canHold:
                    for x, y in game.activeCords:
                        game.board[y][x] = 0
                    if pieceHold != None:
                        pieceHold, game.activePiece = game.activePiece, pieceHold
                        pieceHold.rotationState = 0
                        GAME_OVER = not game.spawn(game.activePiece)
                        game.activeCords = game.activePiece.sCords
                        game.activeCenter = copy.copy(game.activePiece.sCenter)
                        canHold = False
                    else:
                        pieceHold = game.activePiece
                        pieceHold.rotationState = 0
                        newActive()

            elif event.key == pygame.K_SPACE:
                playSound = False
                while game.movePiece():
                    playSound = True # if the while loop is entered play the thud sound
                    pass
                pygame.mixer.Channel(0).play(thudSound)
                newActive()

            game.updateGhost()

    #starts a new active piece
    if getNewActive:
        newActive()


    # Timer for falling piece, triggers new piece when piece reaches bottom

    if currentTime <= 0:
        if not game.movePiece():
            getNewActive = True
        game.updateGhost()
        currentTime = turnTime


    drawBoard(screen)
    drawNextBox(screen, pieceNext)
    drawHoldBox(screen, pieceHold)


    pygame.display.flip()