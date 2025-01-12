import time

import pygame
pygame.init()
import copy

class Game:
    lightBlue = pygame.image.load("images/light-blue-tile.png")
    darkBlue = pygame.image.load("images/dark-blue-tile.png")
    green = pygame.image.load("images/green-tile.png")
    orange = pygame.image.load("images/orange-tile.png")
    yellow = pygame.image.load("images/yellow-tile.png")
    red = pygame.image.load("images/red-tile.png")
    purple = pygame.image.load("images/purple-tile.png")

    transparency = 80

    def __init__(self, rows, cols):
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.boardCopy = copy.deepcopy(self.board)
        self.activePiece = None
        self.activeCords = []  # cords of active piece
        self.activeCenter = ()  # center of active piece
        self.ghostCords = []
        self.idToImage = {1: self.lightBlue, 2: self.darkBlue, 3: self.orange, 4: self.yellow, 5: self.green, 6: self.purple, 7: self.red,
                        11: self.lightBlue.convert_alpha(),
                        22: self.darkBlue.convert_alpha(),
                        33: self.orange.convert_alpha(),
                        44: self.yellow.convert_alpha(),
                        55: self.green.convert_alpha(),
                        66: self.purple.convert_alpha(),
                        77: self.red.convert_alpha()}
        for i in range(1, 8):
            key = int(str(i)*2)
            self.idToImage[key].set_alpha(self.transparency)
            if key == 66:
                self.idToImage[key].set_alpha(self.transparency + 50) #makes the purple a bit brighter

    def print(self):
        for i in self.board:
            print(i)

    def spawn(self, piece):
        spawnCords = []
        canSpawn = True
        for x, y in piece.sCords:
            if self.board[y][x] != 0:
                canSpawn = False
        if canSpawn:
            for x, y in piece.sCords:
                self.board[y][x] = piece.id
            return True
        else:
            return False

    def movePiece(self): #for falling
        oldCords = self.activeCords
        newCords = []
        for x, y in oldCords:
            newCords.append([int(x), int(y+1)])

            if y+1 > len(self.board) - 1 or (self.board[y+1][x] != 0 and self.board[y+1][x] <= 10 and [x, y+1] not in oldCords): #make sure piece can fall
                return False

        for x, y in oldCords:
            self.board[y][x] = 0

        for x, y in newCords:
            self.board[y][x] = self.activePiece.id

        self.activeCords = newCords
        self.activeCenter[1] += 1

        return True

    def shift(self, shiftAmt): #-1 goes left, 1 goes right
        oldCords = self.activeCords
        newCords = []
        for x, y in oldCords:
            newCords.append([x+shiftAmt, y])
            if x + shiftAmt < 0 or x + shiftAmt > len(self.board[0]) - 1 or (self.board[y][x+shiftAmt] != 0  and self.board[y][x+shiftAmt] <= 10 and [x+shiftAmt, y] not in oldCords): #finds out if shift is invalid
                return

        for x, y in oldCords:
            self.board[y][x] = 0

        for x, y in newCords:
            self.board[y][x] = self.activePiece.id

        self.activeCords = newCords
        self.activeCenter[0] += shiftAmt

    def rotate(self, piece, direction): #direction = 1 clockwise, -1 counterclockwise
        if type(piece) == O:
            return # O piece cant rotate and just causes weird errors

        desiredRotationState = (piece.rotationState + direction)%4 # this is a number 0-3
        wallKickID = piece.rotationState*10 + desiredRotationState # will produce a 2-digit number with digits 0-3
        wallKickPath = piece.wallKicks[wallKickID] #gets the specific wallkick path for this piece and rotation


        oldCords = self.activeCords
        centerx, centery = self.activeCenter
        zeroedCords = [[x-centerx,y-centery] for x, y in oldCords] # places the center at 0,0 for rotation formula to work
        rotatedCords = [[int(-(y*direction)+centerx),int((x*direction)+centery)] for x, y in zeroedCords] #had to add int() due to floating point errors

        for xshift, y in wallKickPath:
            yshift = -y #because pygame y coordinates are reversed from the data
            valid = True
            for x, y in rotatedCords:
                testx = int(x+xshift)
                testy = int(y+yshift)
                if (testx < 0 or testx > len(self.board[0]) - 1 or testy < 0 or testy > len(self.board) - 1 or
                        (self.board[testy][testx] != 0  and self.board[testy][testx] <= 10 and [testx, testy] not in oldCords)): # checks if the rotation/wallkick is valid
                    valid = False
                    break
            if valid:
                rotatedCords = [[x+xshift, y+yshift] for x, y in rotatedCords]
                self.activeCenter[0] += xshift
                self.activeCenter[1] += yshift
                break
            valid = False
        if not valid:
            return

        for x, y in oldCords:
            self.board[y][x] = 0

        for x, y in rotatedCords:
            self.board[y][x] = self.activePiece.id #had to add int() due to weird floating point errors

        piece.rotationState = desiredRotationState
        self.activeCords = rotatedCords

    def updateGhost(self):
        for x, y in self.ghostCords:
            self.boardCopy[y][x] = 0

        downwardShift = 1 #how far down to draw ghost piece
        valid = True
        while valid:
            for x, y in self.activeCords:
                if y + downwardShift > len(self.board) - 1 or (self.board[y+downwardShift][x] != 0 and [x, y+downwardShift] not in self.activeCords):
                    valid = False
                    break
            self.ghostCords = [[x,y+downwardShift-1] for x,y in self.activeCords]
            downwardShift += 1

        for x, y in self.ghostCords:
            self.boardCopy[y][x] = int(str(self.activePiece.id)*2)

    def clear(self, sound):
        clear = False
        for i, row in enumerate(self.board):
            if 0 not in row:
                self.board[i] = [0 for _ in range(10)]
                clear = True
        if clear:
            pygame.mixer.Channel(1).play(sound)
            changeMade = True
            while changeMade: #keeps moving rows down until none get moved
                changeMade = False
                for i in range(18, -1, -1): # go through each row backwards (dont need to check bottom row)
                    if self.board[i+1] == [0 for _ in range(10)] and self.board[i] != [0 for _ in range(10)]:
                        self.board[i+1] = [j for j in self.board[i]]
                        self.board[i] = [0 for _ in range(10)]
                        changeMade = True



'''PIECE OUTLINE
                  []              []      [][]
I = [][][][]  J = [][][]  L = [][][]  O = [][]

      [][]        []        [][]
S = [][]    T = [][][]  Z =   [][]

Spawn positions relative to top left corner of board, in terms of tiles. Top left tile is 0, 0
'''


'''
0 = spawn state
1 = state resulting from a clockwise rotation("right") from spawn
2 = state resulting from 2 successive rotations in either direction from spawn.
3 = state resulting from a counter -clockwise("left") rotation from spawn

so, 23 in the dictionary represents the wall kick patter for a rotation from 2 to 3
'''
 #THESE WALL KICKS DO NOT APPLY TO THE "I" TETRONIMO
wallKicks = {1:[(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)],
            10:[(0,0),(1,0),(1,-1),(0,2),(1,2)],
            12:[(0,0),(1,0),(1,-1),(0,2),(1,2)],
            21:[(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)],
            23:[(0,0),(1,0),(1,1),(0,-2),(1,-2)],
            32:[(0,0),(-1,0),(-1,-1),(0,2),(-1,2)],
            30:[(0,0),(-1,0),(-1,-1),(0,2),(-1,2)],
            3:[(0,0),(1,0),(1,1),(0,-2),(1,-2)]}

#"I" tetromino has its own wallkicks for some reason
Iwallkicks = {1:[(0,0),(-2,0),(1,0),(-2,-1),(1,2)],
            10:[(0,0),(2,0),(-1,0),(2,1),(-1,-2)],
            12:[(0,0),(-1,0),(2,0),(-1,2),(2,-1)],
            21:[(0,0),(1,0),(-2,0),(1,-2),(-2,1)],
            23:[(0,0),(2,0),(-1,0),(2,1),(-1,-2)],
            32:[(0,0),(-2,0),(1,0),(-2,-1),(1,2)],
            30:[(0,0),(1,0),(-2,0),(1,-2),(-2,1)],
            3:[(0,0),(-1,0),(2,0),(-1,2),(2,-1)]}

class I:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [5, 1], [6, 1]]
        spawnCenter = [4.5, 1.5]
        self.nextShift = (24*7+30+12, 44) #represents a shift in pixels to go from spawnPos to the next area
        self.holdShift = (-24 * 3 - 30 - 108, 44)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 1
        self.rotationState = 0
        self.wallKicks = Iwallkicks

class J:
    rotationTestOrder = [[-1,0],[-1,1],[0,-2]]
    def __init__(self):
        spawnPos = [[3, 0], [3, 1], [4, 1], [5, 1]]
        spawnCenter = [4, 1]
        self.nextShift = (24 * 7 + 30 + 24, 56)
        self.holdShift = (-24 * 3 - 30 - 96, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 2
        self.rotationState = 0
        self.wallKicks = wallKicks

class L:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [5, 1], [5, 0]]
        spawnCenter = [4, 1]
        self.nextShift = (24 * 7 + 30 + 24, 56)
        self.holdShift = (-24 * 3 - 30 - 96, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 3
        self.rotationState = 0
        self.wallKicks = wallKicks

class O:

    def __init__(self):
        spawnPos = [[4, 0], [5, 0], [5, 1], [4, 1]]
        spawnCenter = [4.5, 0.5]
        self.nextShift = (24 * 6 + 30 + 36, 56)
        self.holdShift = (-24 * 4 - 30 - 84, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 4
        self.rotationState = 0
        self.wallKicks = wallKicks

class S:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 0]]
        spawnCenter = [4, 1]
        self.nextShift = (24 * 7 + 30 + 24, 56)
        self.holdShift = (-24 * 3 - 30 - 96, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 5
        self.rotationState = 0
        self.wallKicks = wallKicks

class T:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 1]]
        spawnCenter = [4, 1]
        self.nextShift = (24 * 7 + 30 + 24, 56)
        self.holdShift = (-24 * 3 - 30 - 96, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 6
        self.rotationState = 0
        self.wallKicks = wallKicks

class Z:

    def __init__(self):
        spawnPos = [[3, 0], [4, 0], [4, 1], [5, 1]]
        spawnCenter = [4, 1]
        self.nextShift = (24 * 7 + 30 + 24, 56)
        self.holdShift = (-24 * 3 - 30 - 96, 56)
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 7
        self.rotationState = 0
        self.wallKicks = wallKicks
