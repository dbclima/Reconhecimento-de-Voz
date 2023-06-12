class Jogador:
    def __init__(self, posicao=None):
        if posicao == None:
            self.posicao = (1, 1)
        else:
            self.posicao = posicao

        # Direcao: True = Direita, False = Esquerda
        self.direcao = True

    def get_posicao(self):
        return int(self.posicao[0]), int(self.posicao[1])

    def set_posicao(self, nova_posicao: tuple):
        self.posicao = nova_posicao