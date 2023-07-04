import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from jogo_interface import Jogo

class TopLevelJogo(tk.Toplevel):
    def __init__(self, container, dificuldade=None):
        super().__init__(container)

        self.dificuldade = dificuldade or 'Médio'

        dict_dificuldade = {
            'Fácil': (7, 5),
            'Médio': (15, 9),
            'Difícil': (21, 13)
        }

        self.jogo = Jogo(self, dict_dificuldade[self.dificuldade])
        self.jogo.pack()
    

class Menu(tk.Tk):
    SCALE = 4
    LARGURA = 320
    ALTURA = 512

    def __init__(self):
        super().__init__()
        self.geometry('320x512')
        self.title('Processamento de Voz - 23.1')

        self.canvas = tk.Canvas(self, width=self.LARGURA, height=self.ALTURA, highlightthickness=0)
        self.carregar_imagens()
        self.criar_objetos()
        self.atribuir_funcionalidades()
        
        self.canvas.pack()

    def carregar_imagens(self) -> None:
        path_bkg = Path('./assets/menu/background.png')
        imagem_bkg = Image.open(path_bkg).resize((80 * self.SCALE, 128 * self.SCALE), resample=Image.NEAREST)
        self.bkg_img = ImageTk.PhotoImage(imagem_bkg)

        path_botao_treino = Path('./assets/menu/botao_treino.png')
        imagem_botao_treino = Image.open(path_botao_treino).resize((24 * self.SCALE, 26 * self.SCALE), resample=Image.NEAREST)
        self.botao_treino = ImageTk.PhotoImage(imagem_botao_treino)

        path_botao_facil = Path('./assets/menu/botao_facil.png')
        imagem_botao_facil = Image.open(path_botao_facil).resize((16 * self.SCALE, 20 * self.SCALE), resample=Image.NEAREST)
        self.botao_facil = ImageTk.PhotoImage(imagem_botao_facil)

        path_botao_medio = Path('./assets/menu/botao_medio.png')
        imagem_botao_medio = Image.open(path_botao_medio).resize((23 * self.SCALE, 20 * self.SCALE), resample=Image.NEAREST)
        self.botao_medio = ImageTk.PhotoImage(imagem_botao_medio)

        path_botao_dificil = Path('./assets/menu/botao_dificil.png')
        imagem_botao_dificil = Image.open(path_botao_dificil).resize((21 * self.SCALE, 28 * self.SCALE), resample=Image.NEAREST)
        self.botao_dificil = ImageTk.PhotoImage(imagem_botao_dificil)

    def criar_objetos(self) -> None:
        self.canvas.create_image((0, 0), image=self.bkg_img, tag='bkg', anchor='nw')
        self.canvas.create_image((self.LARGURA // 2, self.ALTURA // 3.2), image=self.botao_treino, tag='treino')
        self.canvas.create_image((self.LARGURA // 3, self.ALTURA // 1.9), image=self.botao_facil, tag='facil')
        self.canvas.create_image((self.LARGURA * 0.62, self.ALTURA // 1.35), image=self.botao_medio, tag='medio', anchor='sw')
        self.canvas.create_image((self.LARGURA * 0.16, self.ALTURA // 1.1), image=self.botao_dificil, tag='dificil', anchor='sw')

    def atribuir_funcionalidades(self) -> None:
        self.canvas.tag_bind('treino', '<ButtonPress-1>', lambda _: self.iniciar_jogo(dificuldade='Fácil'))
        self.canvas.tag_bind('facil', '<ButtonPress-1>', lambda _: self.iniciar_jogo(dificuldade='Fácil'))
        self.canvas.tag_bind('medio', '<ButtonPress-1>', lambda _: self.iniciar_jogo(dificuldade='Médio'))
        self.canvas.tag_bind('dificil', '<ButtonPress-1>', lambda _: self.iniciar_jogo(dificuldade='Difícil'))

        self.canvas.tag_bind('treino', '<Enter>', lambda _: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('treino', '<Leave>', lambda _: self.canvas.config(cursor='arrow'))

        self.canvas.tag_bind('facil', '<Enter>', lambda _: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('facil', '<Leave>', lambda _: self.canvas.config(cursor='arrow'))

        self.canvas.tag_bind('medio', '<Enter>', lambda _: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('medio', '<Leave>', lambda _: self.canvas.config(cursor='arrow'))

        self.canvas.tag_bind('dificil', '<Enter>', lambda _: self.canvas.config(cursor='hand2'))
        self.canvas.tag_bind('dificil', '<Leave>', lambda _: self.canvas.config(cursor='arrow'))



    def iniciar_jogo(self, dificuldade=None):
        self.dificuldade = dificuldade or 'Médio'
        self.top = TopLevelJogo(self, dificuldade=self.dificuldade)
    

if __name__ == '__main__':
    app = Menu()

    app.mainloop()
