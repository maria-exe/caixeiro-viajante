import math, random
import numpy as np
from faker import Faker

LIMITE_COORDENADA = 100

class Cidade: # para gerar a instância - problema inicial
    def __init__(self):
        fake = Faker('pt_BR')
        
        self.nome = fake.city()

        # gera aleatoriamente as coordenadas x e y do vértice (cidade)
        self.coordenada_x = random.randint(0, LIMITE_COORDENADA)
        self.coordenada_y = random.randint(0, LIMITE_COORDENADA)

class Grafo:
    def __init__(self):
       self.cidades = []
       self.grafo = [] # matriz de distância

    def gera_vertices(self, quantidade_vertices):
        for i in range(quantidade_vertices):
            cidade = Cidade()
            self.cidades.append(cidade)

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