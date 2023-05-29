import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import time
from pathlib import Path

try:
    import ctypes
    ctypes.windll.schcore.SetProcessDpi.Awareness(1)
except:
    pass

from utils import gravar, reproduzir

class Interface(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.audio_duracao = tk.StringVar(value='3')
        self.audio_nome = tk.StringVar(value='')

        self.title('Reconhecimento de Voz - UFRJ')
        self.geometry('500x200')

        self.frame_gravar = ttk.Frame(self)
        self.botao_gravar = ttk.Button(self.frame_gravar, text='Gravar', command=self.func_gravar)
        self.spin_tempo = ttk.Spinbox(self.frame_gravar, from_=1, to=10, textvariable=self.audio_duracao, increment=1, wrap=True, width=10, font=('Segoe UI',))
        self.input_nome = ttk.Entry(self.frame_gravar, textvariable=self.audio_nome, font=('Segoe UI',))

        self.frame_reproduzir = ttk.Frame(self)
        self.botao_reproduzir = ttk.Button(self.frame_reproduzir, text='Reproduzir', command=self.func_reproduzir)
    
        self.config_grid()

    def func_gravar(self):
        nome = self.audio_nome.get()
        tempo = self.audio_duracao.get()

        if nome == '':
            nome = time.time()

        gravar(int(tempo), nome)

    def func_reproduzir(self):
        arquivo = fd.askopenfilename(initialdir=Path('.'))
        if arquivo == '':
            return

        reproduzir(arquivo)

    def config_grid(self):
        self.grid_rowconfigure([0, 2], weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_gravar.grid_rowconfigure([0, 1], weight=1)
        self.frame_gravar.grid_columnconfigure([0, 1], weight=1)
        self.frame_reproduzir.grid_columnconfigure([1, 1], weight=1)
        
        self.frame_gravar.grid(row=0, column=0, sticky='nwe')
        ttk.Label(self.frame_gravar, text='Nome arquivo', font=('Segoe Ui',)).grid(row=0, column=0, sticky='swe', padx=10, pady=(10, 0))
        self.input_nome.grid(row=1, column=0, sticky='we', padx=10)
        ttk.Label(self.frame_gravar, text='Duração Gravação', font=('Segoe Ui',)).grid(row=0, column=1, sticky='swe', padx=10)
        self.spin_tempo.grid(row=1, column=1, sticky='we', padx=10)
        self.botao_gravar.grid(row=2, column=1, sticky='e', padx=10, pady=10)

        ttk.Separator(self, orient='horizontal').grid(row=1, sticky='we')

        self.frame_reproduzir.grid(row=2, column=0, sticky='nwe')
        ttk.Label(self.frame_reproduzir, text='Selecione o arquivo para reprodução:', font=('Segoe UI',)).grid(row=0, column=0, sticky='we', padx=10)
        self.botao_reproduzir.grid(row=0, column=1, sticky='e', padx=10, pady=10)


def main():
    app = Interface()
    app.mainloop()

if __name__ == '__main__':
    main()
