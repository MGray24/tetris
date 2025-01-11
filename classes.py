import pygame


class Game:
    lightBlue = pygame.image.load("images/light-blue-tile.png")
    darkBlue = pygame.image.load("images/dark-blue-tile.png")
    green = pygame.image.load("images/green-tile.png")
    orange = pygame.image.load("images/orange-tile.png")
    yellow = pygame.image.load("images/yellow-tile.png")
    red = pygame.image.load("images/red-tile.png")
    purple = pygame.image.load("images/purple-tile.png")

    idToImage = {1:lightBlue, 2:darkBlue, 3:orange, 4:yellow, 5:green, 6:purple, 7:red}

    activePiece = None
    activeCords = [] #cords of active piece
    activeCenter = () #center of active piece

    def __init__(self, rows, cols):
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def print(self):
        for i in self.board:
            print(i)

    def spawn(self, piece):
        for x, y in piece.sCords:
            self.board[y][x] = piece.id

    def movePiece(self): #for falling
        oldCords = self.activeCords
        newCords = []
        for x, y in oldCords:
            newCords.append([int(x), int(y+1)])
            if y+1 > len(self.board) - 1 or (self.board[y+1][x] != 0 and [x, y+1] not in oldCords): #make sure piece can fall
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
            if x + shiftAmt < 0 or x + shiftAmt > len(self.board[0]) - 1 or (self.board[y][x+shiftAmt] != 0 and [x+shiftAmt, y] not in oldCords): #finds out if shift is invalid
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
                        (self.board[testy][testx] != 0 and [testx, testy] not in oldCords)): # checks if the rotation/wallkick is valid
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

        print(wallKickID)
        piece.rotationState = desiredRotationState
        self.activeCords = rotatedCords

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
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 2
        self.rotationState = 0
        self.wallKicks = wallKicks

class L:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [5, 1], [5, 0]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 3
        self.rotationState = 0
        self.wallKicks = wallKicks

class O:

    def __init__(self):
        spawnPos = [[4, 0], [5, 0], [5, 1], [4, 1]]
        spawnCenter = [4.5, 0.5]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 4
        self.rotationState = 0
        self.wallKicks = wallKicks

class S:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 0]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 5
        self.rotationState = 0
        self.wallKicks = wallKicks

class T:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 1]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 6
        self.rotationState = 0
        self.wallKicks = wallKicks

class Z:

    def __init__(self):
        spawnPos = [[3, 0], [4, 0], [4, 1], [5, 1]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 7
        self.rotationState = 0
        self.wallKicks = wallKicks
