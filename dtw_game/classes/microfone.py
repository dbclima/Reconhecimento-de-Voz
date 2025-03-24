from threading import Thread
from queue import Queue

import speech_recognition as sr

class Microfone:
    def __init__(self):
        self.fila_entrada = Queue()
        self.interprete = sr.Recognizer()
        self.fila_saida = Queue()

        self.ativo = True

        loop_thread_interprete = Thread(target=self._thread_interprete)
        loop_thread_interprete.setDaemon(True)
        loop_thread_interprete.start()

        loop_thread_escuta = Thread(target=self._thread_escuta)
        loop_thread_escuta.setDaemon(True)
        loop_thread_escuta.start()

    def _thread_interprete(self):
        while True:
            audio = self.fila_entrada.get()

            if audio == None:
                break

            try:
                comando = self.interprete.recognize_google(audio, language='pt-BR')

                if 'direita' in comando:
                    self.fila_saida.put('Right')
                elif 'esquerda' in comando:
                    self.fila_saida.put('Left')
                elif 'cima' in comando:
                    self.fila_saida.put('Up')
                elif 'baixo' in comando:
                    self.fila_saida.put('Down')
            
            except sr.UnknownValueError:
                print('Comando não reconhecido')

            except sr.RequestError as e:
                print('Não foi possível requisitar a API:', e)

            self.fila_entrada.task_done()

    def _thread_escuta(self):
        with sr.Microphone() as source:
            while True:
                if not self.ativo:
                    self.fila_entrada.put(None)

                self.fila_entrada.put(self.interprete.listen(source))

    def desligar(self):
        self.fila_entrada.join()
        self.ativo = False

    def get_comando(self):
        if self.fila_saida.empty():
            return None
        
        return self.fila_saida.get()

if __name__ == '__main__':
    mic = Microfone()

    while True:
        a = input('Insira o comando: ')
        if a == 'desligar':
            print('desligou')
            mic.desligar()
        