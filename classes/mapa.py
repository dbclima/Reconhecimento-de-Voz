import numpy as np

class Mapa:
    DEFAULT = (20, 20)
    def __init__(self, shape=None):
            
        self.tiles = np.zeros((shape or self.DEFAULT), dtype=np.uint8)

        self.criar_paredes()

    def criar_paredes(self):
        altura, largura = self.tiles.shape
        for i, row in enumerate(self.tiles):
            for j in range(len(row)):
                if i == 0 or i == altura - 1:
                    self.tiles[i, j] = 1

                if j == 0 or j == largura - 1:
                    self.tiles[i, j] = 1

                # if (i + j) % 2 == 1:
                #     self.tiles[i, j] = 1

    def is_vazio(self, pos) -> bool:
        x, y = pos
        if x >= self.tiles.shape[0] - 1 or y >= self.tiles.shape[1]:
            return False
        if self.tiles[x, y] != 0:
            return False


        return True
