import tkinter as tk
from PIL import Image, ImageTk

class Jogo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('350x600')
        self.title('Processamento de Voz - 23.1')

class Menu(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    app = Jogo()
    menu = Menu()
    menu.pack()
    app.mainloop()
