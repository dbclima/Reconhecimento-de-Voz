import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import time
from pathlib import Path
import pyaudio as pa
import sys

try:
    import ctypes
    ctypes.windll.schcore.SetProcessDpi.Awareness(1)
except:
    pass


class MicUi(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.input_index = tk.StringVar()

        self.index = -1

        self.title('I/O Selection')
        self.geometry('400x100')
        self.resizable(False, False)

        self.frame_input = ttk.Frame(self)
        self.label_input = ttk.Label(self.frame_input, text="Selecione o microfone:", font=('Segoe UI',))

        p = pa.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numero_entradas = info.get('deviceCount')
        self.mic_values: list = [p.get_device_info_by_host_api_device_index(0, i).get('name') for i in range(numero_entradas) if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0]
        
        self.drop_input = ttk.Combobox(self.frame_input, textvariable=self.input_index)
        self.drop_input['values'] = self.mic_values

        self.botao_confirmar = ttk.Button(self.frame_input, text='Confirmar', command=self.func_confirmar)
    
        self.config_grid()

    def config_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid_rowconfigure([0, 1], weight=1)
        self.frame_input.grid_columnconfigure([0, 1], weight=1)
        
        self.frame_input.grid(row=0, column=0, sticky='nswe')
        self.label_input.grid(row=0, column=0, sticky='we', padx=10)
        self.drop_input.grid(row=0, column=1, sticky='we', padx=10)
        self.botao_confirmar.grid(row=1, column=1, sticky='e', padx=10, pady=10)

    def func_confirmar(self) -> None:
        self.index = self.mic_values.index(self.input_index.get())
        self.destroy()
        return None


def main():
    app = MicUi()
    app.mainloop()

    print(app.index)

if __name__ == '__main__':
    main()
