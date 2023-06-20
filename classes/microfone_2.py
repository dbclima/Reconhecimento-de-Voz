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
        self.full = False

    def add(self, elemento):
        elemento_convertido = struct.unpack(f'<{len(elemento)//2}h', elemento)
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


class Microfone:
    FORMATO = pa.paInt16
    CANAIS = 1
    RATE = 44100
    CHUNK = 1024
    TREINO_SIZE = 50
    RUIDO_SIZE = 100
    CAPTURA_SIZE = 75

    def __init__(self):
        self.fila_in = Queue()
        self.buffer_teste = Buffer(self.CAPTURA_SIZE)
        self.buffer_ruido = Buffer(self.RUIDO_SIZE)

        self.treino_keys = [
            #'Ruido',
                             'Direita', 'Esquerda', 'Cima', 'Baixo']
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

        self.treino()
        self.dict_treino_mfcc = {key: librosa.feature.mfcc(y=buffer.get_array_elementos().astype(np.float32), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False) for key, buffer in self.dict_treino.items()}
        
        self.detectar_ruido()

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
            np.save(f'Treino/{key}_treino', buffer.get_array_elementos())

    def dtw_compare(self, buffer: Buffer):
        buffer_in = buffer.get_array_elementos()
        mfccs_teste = librosa.feature.mfcc(y=buffer_in.astype(np.float32), n_mfcc=13, n_fft=512, fmin=0, fmax=None, htk=False)
        lista_custos = []
        for key, mfccs_treino in self.dict_treino_mfcc.items():
            D, wp = librosa.sequence.dtw(mfccs_treino, mfccs_teste, metric='euclidean')
            custo = D[wp[-1, 0], wp[-1, 1]]
            if custo <= 20 and buffer.full:
                lista_custos.append((key, custo))
                np.save(f'Teste/teste_{key}', buffer.get_array_elementos())
                # sys.exit()
        if lista_custos:
            print(lista_custos)
            # buffer.clear_parcial()

    def detectar_ruido(self):
        print('Detectando Ruido')
        self.preencher_buffer(self.buffer_ruido)
        print('Fim detecção de ruido')
        array = self.buffer_ruido.get_array_elementos()
        print('Dados Ruído:')
        print(np.amax(array), np.amin(array), np.mean(array))


if __name__ == '__main__':
    Mic = Microfone()

    while True:
        cmd = input('Insira o comando: ')
        if cmd == 'buffer':
            print(Mic.get_buffer())

        if cmd == 'quit':
            sys.exit()
