# Exportando o jogo
# pyinstaller app.py --onefile --add-data "assets;assets" --windowed

import sys
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk
import random

INCREMENTO_MOVIMENTO = 20
jogadas_por_segundo = 15
VELOCIDADE_DO_JOGO = 1000 // jogadas_por_segundo

class SnakeApp(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background='black', highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.sortear_posicao_comida()
        self.score = 0
        self.direcao = 'Right'

        self.bind_all('<Key>', self.key_pressed)

        self.carregar_imagens()
        self.criar_objetos()

        self.after(VELOCIDADE_DO_JOGO, self.realizar_acoes)


    def carregar_imagens(self):

        diretorio = getattr(sys, '_MEIPASS', Path.cwd())
        path_snake = Path(diretorio) / 'assets' / 'snake.png'
        path_food = Path(diretorio) / 'assets' / 'food.png'

        imagem_snake = Image.open(path_snake)
        self.snake_body = ImageTk.PhotoImage(imagem_snake)
        imagem_food = Image.open(path_food)
        self.food = ImageTk.PhotoImage(imagem_food)

    def criar_objetos(self):
        self.create_text(100, 12, text=f'Score {self.score}, Speed {jogadas_por_segundo}', tag='score', fill='#fff', font=('TkDefaultFont', 14))
        for x, y in self.snake_positions:
            self.create_image(x, y, image=self.snake_body, tag='snake')

        self.create_image(*self.food_position, image=self.food, tag='food')
        self.create_rectangle(7, 27, 593, 613, outline='#525d69')

    def move_snake(self):
        x_cabeca, y_cabeca = self.snake_positions[0]

        if self.direcao == 'Left':
            nova_posicao = (x_cabeca - INCREMENTO_MOVIMENTO, y_cabeca)
        if self.direcao == 'Right':
            nova_posicao = (x_cabeca + INCREMENTO_MOVIMENTO, y_cabeca)
        if self.direcao == 'Up':
            nova_posicao = (x_cabeca, y_cabeca - INCREMENTO_MOVIMENTO)
        if self.direcao == 'Down':
            nova_posicao = (x_cabeca, y_cabeca + INCREMENTO_MOVIMENTO)

        self.snake_positions = [nova_posicao] + self.snake_positions[:-1]

        for segmento, posicao in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segmento, posicao)

    def realizar_acoes(self):
        if self.verificar_colisoes():
            self.endgame()
            return
        self.verificar_colisao_food()
        self.move_snake()
        self.after(VELOCIDADE_DO_JOGO, self.realizar_acoes)

    def verificar_colisoes(self):
        x_cabeca, y_cabeca = self.snake_positions[0]

        return (x_cabeca in (0, 600) or y_cabeca in (20, 620) or (x_cabeca, y_cabeca) in self.snake_positions[1:])
    
    def key_pressed(self, event: tk.Event):
        nova_direcao = event.keysym
        direcoes = ('Up', 'Down', 'Left', 'Right')
        opostos = ({'Up', 'Down'}, {'Left', 'Right'})

        if nova_direcao in direcoes and {nova_direcao, self.direcao} not in opostos:
            self.direcao = nova_direcao

    def verificar_colisao_food(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global jogadas_por_segundo
                jogadas_por_segundo += 1
                global VELOCIDADE_DO_JOGO
                VELOCIDADE_DO_JOGO = 1000 // jogadas_por_segundo

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')

            self.food_position = self.sortear_posicao_comida()
            self.coords(self.find_withtag('food'), self.food_position)

            score = self.find_withtag('score')
            self.itemconfigure(score, text=f'Score {self.score}, Speed {jogadas_por_segundo}', tag='score')

    def sortear_posicao_comida(self):
        while True:
            x = random.randint(1, 29) * INCREMENTO_MOVIMENTO
            y = random.randint(3, 30) * INCREMENTO_MOVIMENTO
            food_position = (x, y)

            if food_position not in self.snake_positions:
                return food_position
            
    def endgame(self):
        self.delete(tk.ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text=f'GAME OVER! {self.score}', fill='#fff', font=('TkDefaultFont', 24))



root = tk.Tk()
root.title('Snake Game')
root.resizable(False, False)

board = SnakeApp()
board.pack()

root.mainloop()