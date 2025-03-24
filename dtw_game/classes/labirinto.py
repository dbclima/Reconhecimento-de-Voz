import random
import numpy as np

class Celula:
    SHAPE = (3, 3)
    IDX_CENTRO_ELEMENTO = (1, 1)
    def __init__(self, pos):
        self.pos = pos
        self.x, self.y = pos
        self.visitado = False
        self.iniciar_elemento()

    def __str__(self):
        string = str()
        for row in self.matriz:
            for elemento in row:
                string += str(elemento) + ' '
            string += '\n'
        return string

    def iniciar_elemento(self):
        self.matriz = np.ones(self.SHAPE)
        x, y = self.IDX_CENTRO_ELEMENTO
        self.matriz[x, y] = 0

    def remover_parede(self, lado):
        x, y = self.IDX_CENTRO_ELEMENTO
        if lado == 'd':
            self.matriz[x + 1, y] = 0
        if lado == 'e':
            self.matriz[x - 1, y] = 0
        if lado == 'c':
            self.matriz[x, y - 1] = 0
        if lado == 'b':
            self.matriz[x, y + 1] = 0

class Labirinto:
    DTF_SHAPE = (5, 3)
    def __init__(self, shape):
        self.shape = self.tratar_shape(shape) or self.DFT_SHAPE

        self.grid = list()
        self.criar_grid()

        self.pilha = list()
        self.extremidades = list()

        self.celula_atual: Celula = self.grid[0][0]

        self.gerar_caminhos()

    def __str__(self):
        string = str()
        for row in self.grid:
            for elemento in row:
                string += str(elemento)
            string += '\n'
        return string

    def criar_grid(self):
        for y in range(self.shape[1]):
            self.grid.append(list())
            for x in range(self.shape[0]):
                self.grid[y].append(Celula((x, y)))

    def verificar_celula(self, pos) -> Celula:
        x, y = pos
        if x < 0 or x > self.shape[0] - 1 or y < 0 or y > self.shape[1] - 1:
            return False
        return self.grid[y][x]
    
    def verificar_vizinhos(self, celula: Celula) -> Celula:
        x, y = celula.pos
        vizinhos = list()

        cima = self.verificar_celula((x, y - 1))
        baixo = self.verificar_celula((x, y + 1))
        direita = self.verificar_celula((x + 1, y))
        esquerda = self.verificar_celula((x - 1, y))

        if cima and not cima.visitado:
            vizinhos.append(cima)
        if baixo and not baixo.visitado:
            vizinhos.append(baixo)
        if direita and not direita.visitado:
            vizinhos.append(direita)
        if esquerda and not esquerda.visitado:
            vizinhos.append(esquerda)

        if (not vizinhos) and (not celula.visitado):
                self.extremidades.append(celula.pos)

        return random.choice(vizinhos) if vizinhos else False
    
    def remover_paredes(self, celula_atual: Celula, celula_prox: Celula) -> None:
        dx = celula_atual.x - celula_prox.x
        if dx == 1:
            celula_atual.remover_parede('e')
            celula_prox.remover_parede('d')
        elif dx == -1:
            celula_atual.remover_parede('d')
            celula_prox.remover_parede('e')

        dy = celula_atual.y - celula_prox.y
        if dy == 1:
            celula_atual.remover_parede('c')
            celula_prox.remover_parede('b')
        elif dy == -1:
            celula_atual.remover_parede('b')
            celula_prox.remover_parede('c')
        return None
    
    def gerar_caminhos(self):
        while True:
            celula_prox = self.verificar_vizinhos(self.celula_atual)
            self.celula_atual.visitado = True
            if celula_prox:
                # celula_prox.visitado = True
                self.pilha.append(self.celula_atual)
                self.remover_paredes(self.celula_atual, celula_prox)
                self.celula_atual = celula_prox
            elif self.pilha:
                self.celula_atual = self.pilha.pop()
            else:
                break

    def export_array(self):
        array = np.ones((self.shape[0] * 2 + 1, self.shape[1] * 2 + 1))
        for i, row in enumerate(self.grid):
            for j, elemento in enumerate(row):
                matriz_elemento = np.array(elemento.matriz)
                array[j*2: j*2 + 2, i*2: i*2 + 2] = matriz_elemento[:-1, :-1]

        return array
    
    def tratar_shape(self, shape):
        if shape:
            return (int((shape[0] - 1) / 2), int((shape[1] - 1) / 2))
        return False

if __name__ == '__main__':
    a = Labirinto((11, 7))
    print(a.export_array())
    

