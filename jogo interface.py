import tkinter as tk
from PIL import Image, ImageTk

from pathlib import Path
import random

from classes import Jogador, Mapa, Moeda

class Jogo(tk.Canvas):
    SCALE = 4
    TEMPO_ACOES = 800
    def __init__(self, shape=None, player_pos=None):
        largura, altura = shape or (20, 20)
        super().__init__(width=largura * 16 * self.SCALE, height=altura * 16 * self.SCALE, background='black', highlightthickness=0)

        self.map = Mapa(shape)
        self.player = Jogador(player_pos)
        self.player_state = 0

        self.timer_pos = (largura - 2, 1)
        self.timer_state = 0
        self.ref_timer = None

        self.carregar_imagens()
        self.criar_objetos()

        self.bind_all('<Key>', self.comando_wrapper)

    def carregar_imagens(self):
        path_pedras = [Path(pedra) for pedra in Path('./assets/rock').iterdir()]
        imagens_pedras = [Image.open(pedra).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for pedra in path_pedras]
        self.pedra_imgs = [ImageTk.PhotoImage(pedra) for pedra in imagens_pedras]

        path_gramas = [Path(grama) for grama in Path('./assets/grass').iterdir()]
        imagens_gramas = [Image.open(grama).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for grama in path_gramas]
        self.grama_imgs = [ImageTk.PhotoImage(grama) for grama in imagens_gramas]
        
        path_timer = [Path(timer) for timer in Path('./assets/timer').iterdir()]
        imagens_timer = [Image.open(timer).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for timer in path_timer]
        self.timer_imgs = [ImageTk.PhotoImage(timer) for timer in imagens_timer]

        path_player = [Path(player) for player in Path('./assets/player').iterdir()]
        imagens_player = [Image.open(player).resize((16 * self.SCALE, 23 * self.SCALE), resample=Image.NEAREST) for player in path_player]
        player_imgs_d = [ImageTk.PhotoImage(player) for player in imagens_player]
        player_imgs_e = [ImageTk.PhotoImage(player.transpose(Image.FLIP_LEFT_RIGHT)) for player in imagens_player]
        self.player_imgs = [player_imgs_e, player_imgs_d]

    def criar_objetos(self):
        for i, row in enumerate(self.map.tiles):
            for j, element in enumerate(row):
                if element == 0:
                    grama = random.choice(self.grama_imgs)
                    self.create_image(*self.display_point(i, j), image=grama, tag='grama', anchor='sw')
                if element == 1:
                    pedra = random.choice(self.pedra_imgs)
                    self.create_image(*self.display_point(i, j), image=pedra, tag='pedra', anchor='sw')

        x, y = self.player.get_posicao()
        self.create_image(*self.display_point(x, y), image=self.player_imgs[self.player.direcao][-1], tag='player', anchor='sw')

    def comando_wrapper(self, event: tk.Event):
        self.unbind_all('<Key>')
        self.comando(event.keysym)

    def comando(self, comando) -> None:
        x, y = self.player.get_posicao()
        x_intermediario, y_intermediario = x, y
        if comando == 'Up':
            y -= 2
            y_intermediario -= 1
        elif comando == 'Down':
            y += 2
            y_intermediario += 1
        elif comando == 'Right':
            x += 2
            x_intermediario += 1
            self.player.direcao = True
        elif comando == 'Left':
            x -= 2
            x_intermediario -= 1
            self.player.direcao = False
        else:
            return None

        posicao = (x, y)
        posicao_intermediaria = (x_intermediario, y_intermediario)

        if self.map.is_vazio(posicao) and self.map.is_vazio(posicao_intermediaria):
            self.player.set_posicao(posicao)
            self.atualizar_player(comando)
            self.atualizar_timer()
        
        self.finalizar_comando()

    def finalizar_comando(self) -> None:
        self.after(self.TEMPO_ACOES, lambda: self.bind_all('<Key>', self.comando_wrapper))

    def atualizar_timer(self) -> None:
        x, y = self.timer_pos
        self.create_image(*self.display_point(x, y), image=self.timer_imgs[self.timer_state], tag='timer', anchor='sw')
        self.timer_state += 1

        if self.timer_state == len(self.timer_imgs):
            self.timer_state = 0
            for img in self.find_withtag('timer'):
                self.delete(img)
            return None
        else:
            self.after(self.TEMPO_ACOES // len(self.timer_imgs), self.atualizar_timer)
            
    def atualizar_player(self, origem):
        self.delete(self.find_withtag('player'))

        x, y = self.player.get_posicao()

        if origem == 'Left':
            x_past, y_past = x + 2, y
        elif origem == 'Right':
            x_past, y_past = x - 2, y
        elif origem == 'Up':
            x_past, y_past = x, y + 2
        else:
            x_past, y_past = x, y - 2

        x_atual = x_past + (x - x_past)/(len(self.player_imgs[self.player.direcao]) * 2) * (self.player_state + 1)
        y_atual = y_past + (y - y_past)/(len(self.player_imgs[self.player.direcao]) * 2) * (self.player_state + 1)

        self.create_image(*self.display_point(x_atual, y_atual), image=self.player_imgs[self.player.direcao][self.player_state % 4], tag='player', anchor='sw')
        self.player_state += 1

        if self.player_state == len(self.player_imgs[self.player.direcao]) * 2:
            self.player_state = 0
        else:
            self.after(self.TEMPO_ACOES // (len(self.player_imgs[self.player.direcao]) * 2), lambda: self.atualizar_player(origem))

        return None

    def display_point(self, x, y):
        return (x) * 16 * self.SCALE, (y + 1) * 16 * self.SCALE


if __name__ == '__main__':
    app = tk.Tk()
    app.title('Processamento de Voz - 23.1')

    jogo = Jogo(shape=(31,15))
    jogo.pack(expand=True)

    app.mainloop()
