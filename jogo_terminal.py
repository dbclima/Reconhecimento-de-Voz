import tkinter as tk
from tkinter import ttk

import numpy as np

import os
import time
import sys

class Jogador:
    def __init__(self, posicao=None):
        if posicao == None:
            self.posicao = (1, 1)
        else:
            self.posicao = posicao  

    def get_posicao(self):
        return int(self.posicao[0]), int(self.posicao[1])

    def set_posicao(self, nova_posicao: tuple):
        self.posicao = nova_posicao

class Mapa:
    DEFAULT = (20, 20)
    def __init__(self, shape=None):
        if shape == None:
            self.tiles = np.zeros(self.DEFAULT, dtype=np.uint8)
        else:
            self.tiles = np.zeros(shape, dtype=np.uint8)

        self.criar_paredes()

    def criar_paredes(self):
        largura, altura = self.tiles.shape
        for i, row in enumerate(self.tiles):
            for j in range(len(row)):
                if i == 0 or i == altura - 1:
                    self.tiles[j, i] = 1

                if j == 0 or j == largura - 1:
                    self.tiles[j, i] = 1

class Jogo:
    JOGADOR = 2
    DFT_SHAPE = (20, 20)
    DFT_PLAYER_POS = (1, 1)
    def __init__(self, shape=None, player_pos=None):
        self.jogador = Jogador(player_pos or self.DFT_PLAYER_POS)
        self.map = Mapa(shape or self.DFT_SHAPE)

        self.posicionar_jogador()
        self.main_loop()

    def posicionar_jogador(self):
        i, j = self.jogador.get_posicao()
        if self.map.tiles[j, i] != 0:
            print('Posição inválida')
        else:
            self.map.tiles[j, i] = 2

    def processar_comando(self, cmd: str):
        if cmd == 'q':
            sys.exit()

        movimentos = {
                'e': -1,
                'd': 1,
                'c': -1j,
                'b': +1j}

        x_inicial, y_inicial = self.jogador.get_posicao()
        x_final = x_inicial + np.real(movimentos[cmd.casefold()])
        y_final = y_inicial + np.imag(movimentos[cmd.casefold()])

        if x_final < 0:
            x_final == x_inicial
        if y_final < 0:
            y_final = y_inicial

        print(y_final, x_final)

        if self.map.tiles[int(y_final), int(x_final)] == 1:
            x_final = x_inicial
            y_final = y_inicial
        else:
            self.map.tiles[y_inicial, x_inicial] = 0
            self.jogador.set_posicao((x_final, y_final))
            self.posicionar_jogador()

    def main_loop(self):
        os.system('clear')
        print(self)

        cmd = input('\nInsira o movimento do jogador: ')
        
        if cmd.casefold() not in ['e', 'd', 'c', 'b', 'q']:
            print('Comando não reconecido')
            time.sleep(0.5)
            self.main_loop()

        self.processar_comando(cmd)
        self.main_loop()

    def __str__(self):
        retorno = str()
        for row in self.map.tiles:
            for element in row:
                if element == self.JOGADOR:
                    retorno += 'j' + ' '
                    continue
                retorno += str(element) + ' '

            retorno += '\n'
        return retorno

if __name__ == '__main__':
    mapa_teste = Jogo((20, 20), (1, 1))
    print(mapa_teste)
    # teste = np.zeros((5, 10))
    # teste[1, 2] = 1
    # print(teste)
