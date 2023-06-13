import numpy as np
from classes.labirinto import Labirinto

class Mapa:
    DFT_SHAPE = (21, 15)
    def __init__(self, shape=None):
        self.shape = shape or self.DFT_SHAPE
        self.tiles = None

        self.criar_paredes()

    def criar_paredes(self):
        self.tiles = Labirinto(self.shape).export_array()

    def is_vazio(self, pos) -> bool:
        x, y = pos
        if x >= self.tiles.shape[0] - 1 or y >= self.tiles.shape[1]:
            return False
        if self.tiles[x, y] != 0:
            return False


        return True
