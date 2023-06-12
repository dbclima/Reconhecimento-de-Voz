import random

# ref: Python Maze Generator. Depth-First Search

class Node:
    def __init__(self, pos):
        self.x, self.y = pos
        self.walls = {'up': True,
                      'down': True,
                      'left': True,
                      'right': True}

        self.visitado = False

    def verificar_celula(self, pos):
        index = lambda x, y: x + y * self.shape[1]
        x, y = pos

        if x < 0 or x > self.shape[0] - 1 or y > self.shape[1] - 1 or y < 0:
            return False
        return self.grid[index(x, y)]
    
    def verificar_vizinhos(self):
        vizinhos = []
        up = self.verificar_celula((self.x, self.y - 1))
        down = self.verificar_celula((self.x, self.y + 1))
        right = self.verificar_celula((self.x + 1, self.y))
        left = self.verificar_celula((self.x - 1, self.y))

        if up and not up.visitado:
            vizinhos.append(up)
        if down and not down.visitado:
            vizinhos.append(down)
        if right and not right.visitado:
            vizinhos.append(right)
        if left and not left.visitado:
            vizinhos.append(left)

        return random.choice(vizinhos) if vizinhos else False


class Maze:
    DFT_SHAPE = (10, 6)
    def __init__(self, shape=None):
        self.shape = shape or (10, 6)

        self.grid = [Node((x, y)) for x in range(self.shape[0]) for y in range(self.shape[1])]
        self.celula_atual = self.grid[0]

        self.stack = list()

    def construir(self):
        while True:
            self.celula_atual.visitado = True

            proxima_celula = self.celula_atual.verificar_vizinhos()
            if proxima_celula:
                proxima_celula.visitado = True
                self.celula_atual = proxima_celula


    



if __name__ == '__main__':
    Maze((4, 6))