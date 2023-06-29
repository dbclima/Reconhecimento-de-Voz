import tkinter as tk
from PIL import Image, ImageTk

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
    def __init__(self):
        super().__init__()
        self.geometry('350x600')
        self.title('Processamento de Voz - 23.1')

        tk.Button(self, text='Iniciar Jogo', command=self.iniciar_jogo).pack(expand=True)


    def iniciar_jogo(self, dificuldade=None):
        self.dificuldade = dificuldade or 'Médio'
        self.top = TopLevelJogo(self, dificuldade=self.dificuldade)
    

if __name__ == '__main__':
    app = Menu()

    app.mainloop()
