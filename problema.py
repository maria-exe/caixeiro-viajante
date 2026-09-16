import math, random
import numpy as np

LIMITE_COORDENADA = 1000

class Cidade:
    def __init__(self, x=None, y=None):
        self.coordenada_x = x if x is not None else random.randint(0, LIMITE_COORDENADA)
        self.coordenada_y = y if y is not None else random.randint(0, LIMITE_COORDENADA)

class Grafo:
    def __init__(self):
        self.cidades = []
        self.grafo = []

    def gera_vertices(self, quantidade_vertices):
        for i in range(quantidade_vertices):
            cidade = Cidade()
            self.cidades.append(cidade)

    def carrega_tsplib(self, caminho):
        self.cidades = []
        with open(caminho) as f:
            linhas = f.readlines()

        inicio = None
        for i, linha in enumerate(linhas):
            if linha.strip() == "NODE_COORD_SECTION":
                inicio = i + 1
                break

        for linha in linhas[inicio:]:
            linha = linha.strip()
            if linha == "EOF" or linha == "":
                break
            _, x, y = linha.split()
            self.cidades.append(Cidade(float(x), float(y)))

    def popula_matriz(self):
        n = len(self.cidades)
        self.grafo = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                distancia = self.calcula_distancia(self.cidades[i], self.cidades[j])
                self.grafo[i, j] = distancia
                self.grafo[j, i] = distancia

    def calcula_distancia(self, cidade_a, cidade_b):
        distancia_x = (cidade_a.coordenada_x - cidade_b.coordenada_x) ** 2
        distancia_y = (cidade_a.coordenada_y - cidade_b.coordenada_y) ** 2

        distancia_euclidiana = math.sqrt(distancia_x + distancia_y)

        return distancia_euclidiana