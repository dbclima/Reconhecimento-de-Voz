import tkinter as tk
from PIL import Image, ImageTk

from pathlib import Path
import random

from classes import Jogador, Mapa, Moeda

class Jogo(tk.Canvas):
    SCALE = 3
    TEMPO_ACOES = 800
    def __init__(self, shape=None, player_pos=None):
        self.largura, self.altura = shape or (21, 15)
        super().__init__(width=self.largura * 16 * self.SCALE, height=self.altura * 16 * self.SCALE, background='black', highlightthickness=0)

        self.fim = False

        self.map = Mapa(shape)
        self.moeda = Moeda()
        self.moeda_state = 0

        self.player = Jogador(player_pos)
        self.player_state = 0

        self.timer_pos = (self.largura - 2, 1)
        self.timer_state = 0

        self.carregar_imagens()
        self.criar_objetos_estaticos()
        self.criar_objetos_dinamicos()

        self.bind_all('<Key>', self.comando_wrapper)

    def carregar_imagens(self):
        path_pedras = [Path(pedra) for pedra in Path('./assets/rock').iterdir()]
        path_pedras.sort()
        imagens_pedras = [Image.open(pedra).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for pedra in path_pedras]
        self.pedra_imgs = [ImageTk.PhotoImage(pedra) for pedra in imagens_pedras]

        path_gramas = [Path(grama) for grama in Path('./assets/grass').iterdir()]
        path_gramas.sort()
        imagens_gramas = [Image.open(grama).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for grama in path_gramas]
        self.grama_imgs = [ImageTk.PhotoImage(grama) for grama in imagens_gramas]
        
        path_timer = [Path(timer) for timer in Path('./assets/timer').iterdir()]
        path_timer.sort()
        imagens_timer = [Image.open(timer).resize((16 * self.SCALE, 16 * self.SCALE), resample=Image.NEAREST) for timer in path_timer]
        self.timer_imgs = [ImageTk.PhotoImage(timer) for timer in imagens_timer]

        path_moedas = [Path(moeda) for moeda in Path('./assets/coin').iterdir()]
        path_moedas.sort()
        imagens_moedas = [Image.open(moeda).resize((16 * self.SCALE, 23 * self.SCALE), resample=Image.NEAREST) for moeda in path_moedas]
        self.moeda_imgs = [ImageTk.PhotoImage(moeda) for moeda in imagens_moedas]

        path_player = [Path(player) for player in Path('./assets/player').iterdir()]
        path_player.sort()
        imagens_player = [Image.open(player).resize((16 * self.SCALE, 23 * self.SCALE), resample=Image.NEAREST) for player in path_player]
        player_imgs_d = [ImageTk.PhotoImage(player) for player in imagens_player]
        player_imgs_e = [ImageTk.PhotoImage(player.transpose(Image.FLIP_LEFT_RIGHT)) for player in imagens_player]
        self.player_imgs = [player_imgs_e, player_imgs_d]

    def criar_objetos_estaticos(self):
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

    def criar_objetos_dinamicos(self):
        self.moeda.set_posicao((self.largura - 2, self.altura - 2))
        x, y = self.moeda.get_posicao()
        self.create_image(*self.display_point(x, y), image=self.moeda_imgs[self.moeda_state], tag='moeda', anchor='sw')
        self.atualizar_moeda()

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
            self.finalizar_comando()
            return None

        posicao = (x, y)
        posicao_intermediaria = (x_intermediario, y_intermediario)

        if self.map.is_vazio(posicao) and self.map.is_vazio(posicao_intermediaria):
            self.player.set_posicao(posicao)
            self.atualizar_player(comando)
            self.atualizar_timer()
        
        self.finalizar_comando()

    def finalizar_comando(self) -> None:
        if not self.condicao_vitoria():
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
    
    def atualizar_moeda(self):
        self.delete(self.find_withtag('moeda'))
        
        if self.fim:
            return None

        x, y = self.moeda.get_posicao()

        self.create_image(*self.display_point(x, y), image=self.moeda_imgs[self.moeda_state], tag='moeda', anchor='sw')
        self.moeda_state += 1

        if self.moeda_state == len(self.moeda_imgs):
            self.moeda_state = 0

        self.after(self.TEMPO_ACOES // len(self.moeda_imgs), self.atualizar_moeda)


    def display_point(self, x, y):
        return (x) * 16 * self.SCALE, (y + 1) * 16 * self.SCALE

    
    def condicao_vitoria(self) -> bool:
        if self.player.get_posicao() == self.moeda.get_posicao():
            self.fim = True
            return True
        return False


if __name__ == '__main__':
    app = tk.Tk()
    app.title('Processamento de Voz - 23.1')

    jogo = Jogo(shape=(21, 15))
    jogo.pack(expand=True)

    app.mainloop()
