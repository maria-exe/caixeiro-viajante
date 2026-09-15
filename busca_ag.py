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

    def calcula_custo(self, percurso):
        custo = 0 
        tam = len(percurso)

        for i in range(tam - 1):
            custo += self.matriz[percurso[i]][percurso[i+1]] 
        custo += self.matriz[percurso[-1]][percurso[0]]
        return custo

    def gera_populacao(self):
        populacao = [] # lista de percursos diferentes para a matriz de cidades
        n = len(self.matriz)
        
        for i in range(self.tam_populacao):
            percurso = random.sample(range(n), n)
            populacao.append(percurso)
    
        return populacao
    
    def selecao(self, populacao):
        selecionados = random.sample(populacao, self.k)
        return min(selecionados, key=self.calcula_custo)

    def mutacao(self, percurso):
        n = len(percurso)
        i, j = sorted(random.sample(range(n), 2))
        percurso_mutado = percurso.copy()
        
        # inversao 2opt
        percurso_mutado[i:j+1] = reversed(percurso_mutado[i:j+1])
        return percurso_mutado

    def crossover_ox(self, p1, p2):
        n = len(p1)
        i, j = sorted(random.sample(range(n), 2))

        filho = [None] * n
        filho[i:j+1] = p1[i:j+1]

        cidades_filho = set(filho[i:j+1])

        posicao = (j + 1) % n
        index_p2 = (j + 1) % n

        for _ in range(n):
            cidade = p2[index_p2]
            if cidade not in cidades_filho:
                filho[posicao] = cidade
                cidades_filho.add(cidade)
                posicao = (posicao + 1) % n
            index_p2 = (index_p2 + 1) % n
    
        return filho

    def executa_busca(self):
        populacao = self.gera_populacao()

        melhor_percurso = min(populacao, key=self.calcula_custo)
        melhor_custo = self.calcula_custo(melhor_percurso)
        self.custos = []

        for _ in range(self.geracoes):
            nova_populacao = [melhor_percurso.copy()]  # elitismo

            while len(nova_populacao) < self.tam_populacao:
                pai1 = self.selecao(populacao)
                pai2 = self.selecao(populacao)

                if random.random() < self.taxa_crossover:
                    filho = self.crossover_ox(pai1, pai2)
                else:
                    filho = pai1.copy()

                if random.random() < self.taxa_mutacao:
                    filho = self.mutacao(filho)

                nova_populacao.append(filho)

            populacao = nova_populacao

            # encontra o melhor da geracao atual
            melhor_geracao = min(populacao, key=self.calcula_custo)
            custo = self.calcula_custo(melhor_geracao)
            
            self.custos.append(custo)

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_percurso = melhor_geracao.copy()

        return melhor_percurso, melhor_custo
      
def main():
    grafo = Grafo()
    grafo.gera_vertices(50)
    grafo.popula_matriz()

    ag = AlgoritmoGenetico(
        grafo=grafo.grafo,        # <- troca aqui: matriz gerada, não mais matriz_teste fixa
        tam_populacao=100,
        taxa_crossover=0.8,
        taxa_mutacao=0.1,
        geracoes=200,
        k=5
    )

    melhor_percurso, melhor_custo = ag.executa_busca()
    print("Melhor percurso:", melhor_percurso)
    print("Melhor custo:", melhor_custo)
    print("Histórico de custos (por geração):", ag.custos)


if __name__ == "__main__":
    main()