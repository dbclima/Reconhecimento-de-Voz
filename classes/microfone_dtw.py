import pyaudio as pa
import numpy as np
import struct
from queue import Queue
from threading import Thread
from time import perf_counter
import matplotlib.pyplot as plt
import librosa
import librosa.display
import sys

class Buffer:
    MAX_SIZE = 100  # Aproximadamente 2.5s para preencher
    def __init__(self, size=None):
        self.inicio = perf_counter()
        self.size = size or self.MAX_SIZE
        self.elementos = list()
        self.elementos_vozeados = None
        self.full = False

    def add(self, elemento):
        elemento_convertido = struct.unpack(f'<{len(elemento)//4}f', elemento)
        if len(self.elementos) == self.size:
            self.full = True
            self.fim = perf_counter()
            self.elementos[:-1] = self.elementos[1:]
            self.elementos[-1] = elemento_convertido

        else:
            self.elementos.append(elemento_convertido)

    def clear(self):
        self.elementos = list()
        self.full = False

    def clear_parcial(self):
        self.elementos = self.elementos[len(self.elementos) // 2:]
        self.full = False

    def get_elementos(self):
        return np.array(self.elementos)
    
    def get_array_elementos(self):
        return self.get_elementos().flatten()
    
    def calibrar(self, buffer_ruido):
        array_ruido = buffer_ruido.get_array_elementos()
        maximo_ruido = np.divide(np.sum(np.square(array_ruido)), len(buffer_ruido.get_elementos())) * 1.1
        self.elementos_vozeados = [elemento for elemento in self.elementos if np.sum(np.square(elemento)) > maximo_ruido]
        print(len(self.elementos) ,len(self.elementos_vozeados))

    def get_elementos_vozeados(self):
        return np.array(self.elementos_vozeados)


class Microfone:
    FORMATO = pa.paFloat32
    CANAIS = 1
    RATE = 44100
    CHUNK = 1024
    TREINO_SIZE = 50
    RUIDO_SIZE = 50
    CAPTURA_SIZE = 75

    def __init__(self):
        self.fila_in = Queue()
        self.fila_saida = Queue()
        self.buffer_teste = Buffer(self.CAPTURA_SIZE)
        self.buffer_ruido = Buffer(self.RUIDO_SIZE)
        self.limiar = None
        self.lista_limiares = list()

        self.treino_keys = ['Direita', 'Esquerda', 'Cima', 'Baixo']
        self.dict_treino: dict[str, Buffer] = {key: Buffer(self.TREINO_SIZE) for key in self.treino_keys}
        self.dict_treino_mfcc: dict[str, np.ndarray] = dict()
        
        self.audio = pa.PyAudio()
        self.stream = self.audio.open(format=self.FORMATO,
                                      channels=self.CANAIS,
                                      rate=self.RATE,
                                      input=True,
                                      input_device_index=0,
                                      frames_per_buffer=self.CHUNK)
        
        loop_thread_escuta = Thread(target=self._thread_escuta, daemon=True)
        loop_thread_escuta.start()

        self.detectar_ruido()

        self.treino()
        
        loop_thread_buffer = Thread(target=self._thread_preencher_buffer, daemon=True)
        loop_thread_buffer.start()

    def _thread_escuta(self):
        while True:
            if not self.stream.is_active():
                break
            self.fila_in.put(self.stream.read(self.CHUNK))

    def _thread_preencher_buffer(self):
        while True:
            frame = self.fila_in.get()
            self.buffer_teste.add(frame)

            if self.buffer_teste.full:
                self.dtw_compare(self.buffer_teste)

    def preencher_buffer(self, buffer: Buffer):
        while not buffer.full:
            frame = self.fila_in.get()
            buffer.add(frame)

    def get_buffer(self):
        print(self.buffer_teste.get_elementos().shape)
        return self.buffer_teste.get_elementos()
    
    def treino(self):
        for key in self.dict_treino.keys():
            buffer = self.dict_treino[key]
            print(f'Diga {key}:')
            self.preencher_buffer(buffer)
            buffer.calibrar(self.buffer_ruido)
            # np.save(f'Treino/{key}_treino', buffer.get_elementos_vozeados())

        self.dict_treino_mfcc = {key: librosa.feature.mfcc(y=buffer.get_elementos_vozeados().flatten(), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False) for key, buffer in self.dict_treino.items()}
        
        mfccs_ruido = librosa.feature.mfcc(y=self.buffer_ruido.get_array_elementos(), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False)
        lista_limiares = list()
        for key, mfccs_treino in self.dict_treino_mfcc.items():
            D, wp = librosa.sequence.dtw(mfccs_treino, mfccs_ruido)
            print(np.sum(D[wp[:, 0], wp[:, 1]]))
            lista_limiares.append(np.sum(D[wp[:, 0], wp[:, 1]]))
        
        self.limiar = np.mean(lista_limiares)
        print(self.limiar)
        
    def adicionar_palavra(self, palavra: str) -> None:
        if not palavra:
            return None
        
        self.dict_treino[palavra] = Buffer(self.TREINO_SIZE)
        buffer = self.dict_treino[palavra]

        self.preencher_buffer(buffer)
        buffer.calibrar(self.buffer_ruido)

        self.dict_treino_mfcc[palavra] = librosa.feature.mfcc(y=buffer.get_elementos_vozeados().flatten(), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False)
        D, wp = librosa.sequence.dtw(self.dict_treino_mfcc[palavra], self.mfccs_ruido)
        self.lista_limiares.append(np.sum(D[wp[:, 0], wp[:, 1]]))


    def dtw_compare(self, buffer: Buffer):
        buffer_in = buffer.get_array_elementos()
        mfccs_teste = librosa.feature.mfcc(y=buffer_in, n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False)
        lista_custos = []
        for key, mfccs_treino in self.dict_treino_mfcc.items():
            D, wp = librosa.sequence.dtw(mfccs_treino, mfccs_teste)
            custo = np.sum(D[wp[:, 0], wp[:, 1]])
            if custo <= np.mean(self.lista_limiares) and buffer.full:
                lista_custos.append((custo, key))
                # np.save(f'Teste/teste_{key}', buffer.get_array_elementos())
        if lista_custos:
            self.fila_saida.put(lista_custos)
            buffer.clear()

    def detectar_ruido(self):
        print('-x-x-x-x-x-x-x-Detectando Ruido-x-x-x-x-x-x-x-')
        self.preencher_buffer(self.buffer_ruido)
        print('-x-x-x-x-x-x-Fim Detecção de Ruido-x-x-x-x-x-x-')
        self.mfccs_ruido = librosa.feature.mfcc(y=self.buffer_ruido.get_array_elementos(), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False)

    def get_comando(self):
        comandos = self.fila_saida.get()
        custo, comando = min(comandos)
        return comando


if __name__ == '__main__':
    Mic = Microfone()
    while True:
        print(Mic.fila_saida.get())
