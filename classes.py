import pygame


class Game:
    def __init__(self, rows, cols):
        self.board = [[0 for i in range(cols)] for j in range(rows)]

    def print(self):
        for i in self.board:
            print(i)

'''PIECE OUTLINE
                  []              []      [][]
I = [][][][]  J = [][][]  L = [][][]  O = [][]

      [][]        []        [][]
S = [][]    T = [][][]  Z =   [][]
'''

class I:
    def __init__(self):
        self.image = pygame.image.load("images/light-blue-tile.png")