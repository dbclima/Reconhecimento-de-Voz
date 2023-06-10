import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import numpy as np
from pathlib import Path
import os
import time
import sys

class Jogador:
    def __init__(self, posicao=None):
        if posicao == None:
            self.posicao = [1, 1]
        else:
            self.posicao = posicao  

    def get_posicao(self):
        return int(self.posicao[0]), int(self.posicao[1])

    def set_posicao(self, nova_posicao: tuple):
        self.posicao = nova_posicao

    def direita(self):
        self.posicao[0] += 1

    def esquerda(self):
        self.posicao[0] -= 1

    def cima(self):
        self.posicao[1] -= 1
    
    def baixo(self):
        self.posicao[1] += 1

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

class Jogo(tk.Canvas):
    SCALE = 2
    def __init__(self, shape=None, player_pos=None):
        largura, altura = shape or (20, 20)
        super().__init__(width=largura * 16 * self.SCALE, height=altura * 16 * self.SCALE, background='black', highlightthickness=0)

        self.map = Mapa(shape)
        self.player = Jogador(player_pos)

        self.carregar_imagens()
        self.criar_objetos()

        self.bind_all('<Key>', self.comando)

    def carregar_imagens(self):
        path_pedra = Path('./assets/rock_1.png')
        imagem_pedra = Image.open(path_pedra).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST)
        self.pedra_img = ImageTk.PhotoImage(imagem_pedra)

        path_grama = Path('./assets/grass_1.png')
        imagem_grama = Image.open(path_grama).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST)
        self.grama_img = ImageTk.PhotoImage(imagem_grama)

        path_player = Path('./assets/player.png')
        imagem_player = Image.open(path_player).resize((15 * self.SCALE, 18 * self.SCALE), resample=Image.NEAREST)
        self.player_img = ImageTk.PhotoImage(imagem_player)

    def criar_objetos(self):
        # self.create_rectangle(7, 27, 593, 613, outline='#525d69')
        for i, row in enumerate(self.map.tiles):
            for j, element in enumerate(row):
                if element == 0:
                    self.create_image(i * 16 * self.SCALE, j * 16 * self.SCALE, image=self.grama_img, tag='grama', anchor='nw')
                if element == 1:
                    self.create_image(i * 16 * self.SCALE, j * 16 * self.SCALE, image=self.pedra_img, tag='pedra', anchor='nw')

        x, y = self.player.get_posicao()
        self.create_image(x * 16 * self.SCALE, y * 16 * self.SCALE, image=self.player_img, tag='player', anchor='nw')

    def verificar_colisoes(self):
        pass

    def comando(self, evento: tk.Event):
        comando = evento.keysym
        direcoes = ('Up', 'Down', 'Left', 'Right')

        if comando not in direcoes:
            return

        dict_comando = {'Up': self.player.cima,
                        'Down': self.player.baixo,
                        'Left': self.player.esquerda,
                        'Right': self.player.direita}
        
        dict_comando[comando]()

        self.atualizar_player()   

    def atualizar_player(self):
        x, y = self.player.get_posicao()
        self.coords(self.find_withtag('player'), x * 16 * self.SCALE, y * 16 * self.SCALE)

if __name__ == '__main__':
    app = tk.Tk()
    app.title('Processamento de Voz - 23.1')

    jogo = Jogo(shape=(30,15))
    jogo.pack()


    app.mainloop()
