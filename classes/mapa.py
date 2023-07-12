import numpy as np
from classes.labirinto import Labirinto

class Mapa:
    DFT_SHAPE = (21, 15)
    def __init__(self, shape=None):
        self.shape = shape or self.DFT_SHAPE
        self.tiles = None
        self.moeda_pos = None

        self.criar_paredes()

    def criar_paredes(self):
        labirinto = Labirinto(self.shape)
        self.tiles = labirinto.export_array()
        print(labirinto.extremidades)
        self.moeda_pos = labirinto.extremidades[-1]

    def is_vazio(self, pos) -> bool:
        x, y = pos
        if x >= self.tiles.shape[0] - 1 or y >= self.tiles.shape[1]:
            return False
        if self.tiles[x, y] != 0:
            return False
        return True
        
    def get_moeda_pos(self):
        return self.moeda_pos[0] * 2 + 1, self.moeda_pos[1] * 2 + 1
        return True
