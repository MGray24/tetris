import pygame


class Game:
    lightBlue = pygame.image.load("images/light-blue-tile.png")
    darkBlue = pygame.image.load("images/dark-blue-tile.png")
    green = pygame.image.load("images/green-tile.png")
    orange = pygame.image.load("images/orange-tile.png")
    yellow = pygame.image.load("images/yellow-tile.png")
    red = pygame.image.load("images/red-tile.png")
    purple = pygame.image.load("images/purple-tile.png")

    idToImage = {1:lightBlue, 2:darkBlue)}

    def __init__(self, rows, cols):
        self.board = [[0 for i in range(cols)] for j in range(rows)]

    def print(self):
        for i in self.board:
            print(i)

    def spawn(self, piece):
        for x, y in piece.cords:
            self.board[y][x] = piece.id

'''PIECE OUTLINE
                  []              []      [][]
I = [][][][]  J = [][][]  L = [][][]  O = [][]

      [][]        []        [][]
S = [][]    T = [][][]  Z =   [][]

Spawn positions relative to top left corner of board, in terms of tiles. Top left tile is 0, 0
'''

class I:

    def __init__(self):
        spawnPos = [(3, 1), (4, 1), (5, 1), (6, 1)]
        spawnCenter = (4.5, 1.5)
        self.cords = spawnPos
        self.center = spawnCenter
        self.id = 1
