import pyaudio as pa
import numpy as np
import struct
from queue import Queue
from threading import Thread
from time import perf_counter

class Buffer:
    MAX_SIZE = 100
    def __init__(self, size=None):
        self.inicio = perf_counter()
        self.size = size or self.MAX_SIZE
        self.elementos = list()

    def add(self, elemento):
        elemento_convertido = struct.unpack(f'<{len(elemento)//2}h', elemento)
        if len(self.elementos) == self.size:
            self.fim = perf_counter()
            print(self.fim - self.inicio)
            self.elementos[:-1] = self.elementos[1:]
            self.elementos[-1] = elemento_convertido

        else:
            self.elementos.append(elemento_convertido)

class Microfone:
    FORMATO = pa.paInt16
    CANAIS = 1
    RATE = 44100
    CHUNK = 1024

    def __init__(self):
        self.fila_in = Queue()
        self.buffer = Buffer()
        
        self.audio = pa.PyAudio()
        self.stream = self.audio.open(format=self.FORMATO,
                                      channels=self.CANAIS,
                                      rate=self.RATE,
                                      input=True,
                                      input_device_index=0,
                                      frames_per_buffer=self.CHUNK)

        loop_thread_escuta = Thread(target=self._thread_escuta, daemon=True)
        loop_thread_escuta.start()

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
            self.buffer.add(frame)

    def get_buffer(self):
        return self.buffer.elementos


if __name__ == '__main__':
    Mic = Microfone()

    while True:
        a = input('Insira o comando')
        if a == 'buffer':
            print(Mic.get_buffer())

