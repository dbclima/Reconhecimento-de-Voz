import random
import numpy as np

# ref: Python Maze Generator. Depth-First Search

class Node:
    def __init__(self, pos: tuple, maze):
        self.x, self.y = pos
        self.maze = maze
        self.walls = {'up': True,
                      'down': True,
                      'left': True,
                      'right': True}

        self.visitado = False

    def verificar_celula(self, pos):
        index = lambda x, y: x + y * self.maze.shape[0]
        x, y = pos
        if x < 0 or x > self.maze.shape[0] - 1 or y > self.maze.shape[1] - 1 or y < 0:
            return False
        return self.maze.grid[index(x, y)]
    
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

        self.grid = [Node((x, y), self) for x in range(self.shape[0]) for y in range(self.shape[1])]
        self.celula_atual = self.grid[0]

        self.stack = list()
        self.maze_matrix = None

        self.construir()

    def construir(self):
        while True:
            self.celula_atual.visitado = True

            proxima_celula = self.celula_atual.verificar_vizinhos()
            if proxima_celula:
                # print((self.celula_atual.x, self.celula_atual.y), (proxima_celula.x, proxima_celula.y))
                proxima_celula.visitado = True
                self.stack.append(self.celula_atual)
                self.remover_parede(self.celula_atual, proxima_celula)
                self.celula_atual = proxima_celula
            elif self.stack:
                self.celula_atual = self.stack.pop()
            else:
                break

    def remover_parede(self, node_atual: Node, proximo_node: Node):
        dx = node_atual.x - proximo_node.x
        dy = node_atual.y - proximo_node.y
        if dx == 1:
            node_atual.walls['left'] = False
            proximo_node.walls['right'] = False
        elif dx == -1:
            node_atual.walls['right'] = False
            proximo_node.walls['left'] = False

        if dy == 1:
            node_atual.walls['up'] = False
            proximo_node.walls['down'] = False
        elif dy == -1:
            node_atual.walls['down'] = False
            proximo_node.walls['up'] = False

    def maze_to_matrix(self):
        # print(len(self.grid))
        self.maze_matrix = np.zeros((self.shape[0]*2 + 1, self.shape[1]*2 + 1))
        # print(self.maze_matrix)
            

if __name__ == '__main__':
    a = Maze((15, 2))
    print(a.maze_to_matrix())
    