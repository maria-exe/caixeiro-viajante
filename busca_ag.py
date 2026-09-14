import random, itertools, math
from problema import Grafo
from collections import Counter

class AlgoritmoGenetico:
    def __init__(self, grafo, tam_populacao, taxa_crossover, taxa_mutacao, geracoes, k):
        self.matriz = grafo
        self.tam_populacao = tam_populacao
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao
        self.geracoes = geracoes
        self.k = k

        self.custos = []

    def calcula_custo(self, percurso): # equacao pronta!!!
        custo = 0 
        tam = len(percurso)

        for i in range(tam - 1):
            custo += self.matriz[percurso[i]][percurso[i+1]] 
        custo += self.matriz[percurso[-1]][percurso[0]]

        return custo

    def gera_populacao(self, tam_populacao):
        populacao = [] # lista de percursos diferentes para a matriz de cidades
        n = len(self.matriz)
        for i in range(tam_populacao):
            percurso = random.sample(range(n), n)
            populacao.append(percurso)
        return populacao

    def fitness(self, percurso, max_custo):
        return max_custo - self.calcula_custo(percurso)
    
    def selecao(self, populacao):
        selecionados = random.sample(populacao, self.k)
        return min(selecionados, key=self.calcula_custo)

    def mutacao(self, percurso):
        n = len(percurso)
        i, j = sorted(random.sample(range(n), 2))
        percurso_mutado = percurso.copy()
        percurso_mutado[i:j+1] = reversed(percurso_mutado[i:j+1])
        return percurso_mutado

    def executa_busca(self):
        pass

def main():
    matriz_teste = [
        [0,  10, 15, 20, 25],
        [10, 0,  35, 25, 30],
        [15, 35, 0,  30, 5],
        [20, 25, 30, 0,  15],
        [25, 30, 5,  15, 0],
    ]

    ag = AlgoritmoGenetico(
        grafo=matriz_teste,
        tam_populacao=3,
        taxa_crossover=0.8,
        taxa_mutacao=0.05,
        geracoes=10,
        k=2
    )

    populacao_teste = [[0,1,2,3,4], [4,3,2,1,0], [0,2,4,1,3]]

    print("Custos da população de teste:")
    for individuo in populacao_teste:
        print(individuo, "->", ag.calcula_custo(individuo))

    print("\nResultados da seleção por torneio (k=2), 5 rodadas:")
    for _ in range(5):
        selecionado = ag.selecao(populacao_teste)
        print(selecionado, "-> custo:", ag.calcula_custo(selecionado))

    resultados = [tuple(ag.selecao(populacao_teste)) for _ in range(1000)]
    print(Counter(resultados))

if __name__ == "__main__":
    main()