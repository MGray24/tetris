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
        self.board = [[0 for i in range(cols)] for j in range(rows)]

    def print(self):
        for i in self.board:
            print(i)

    def spawn(self, piece):
        for x, y in piece.sCords:
            self.board[y][x] = piece.id

    def movePiece(self):
        oldCords = self.activeCords
        newCords = []
        for x, y in oldCords:
            newCords.append([x, y+1])
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

'''PIECE OUTLINE
                  []              []      [][]
I = [][][][]  J = [][][]  L = [][][]  O = [][]

      [][]        []        [][]
S = [][]    T = [][][]  Z =   [][]

Spawn positions relative to top left corner of board, in terms of tiles. Top left tile is 0, 0
'''

class I:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [5, 1], [6, 1]]
        spawnCenter = [4.5, 1.5]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 1

class J:

    def __init__(self):
        spawnPos = [[3, 0], [3, 1], [4, 1], [5, 1]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 2

class L:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [5, 1], [5, 0]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 3

class O:

    def __init__(self):
        spawnPos = [[4, 0], [5, 0], [5, 1], [4, 1]]
        spawnCenter = [4.5, 0.5]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 4

class S:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 0]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 5

class T:

    def __init__(self):
        spawnPos = [[3, 1], [4, 1], [4, 0], [5, 1]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 6

class Z:

    def __init__(self):
        spawnPos = [[3, 0], [4, 0], [4, 1], [5, 1]]
        spawnCenter = [4, 1]
        self.sCords = spawnPos
        self.sCenter = spawnCenter
        self.id = 7
