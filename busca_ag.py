import random
from problema import Grafo


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
            custo += self.matriz[percurso[i]][percurso[i + 1]]
        custo += self.matriz[percurso[-1]][percurso[0]]
        return custo

    def gera_populacao(self):
        n = len(self.matriz)
        return [random.sample(range(n), n) for _ in range(self.tam_populacao)]

    def selecao(self, populacao, custos):
        indices = random.sample(range(len(populacao)), self.k)
        melhor_indice = min(indices, key=lambda i: custos[i])
        return populacao[melhor_indice]

    def mutacao(self, percurso):
        n = len(percurso)
        i, j = sorted(random.sample(range(n), 2))
        percurso_mutado = percurso.copy()
        percurso_mutado[i:j + 1] = reversed(percurso_mutado[i:j + 1])
        return percurso_mutado

    def crossover_ox(self, p1, p2):
        n = len(p1)
        i, j = sorted(random.sample(range(n), 2))

        filho = [None] * n
        filho[i:j + 1] = p1[i:j + 1]
        cidades_filho = set(filho[i:j + 1])

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
        custos = [self.calcula_custo(ind) for ind in populacao]

        indice_melhor = custos.index(min(custos))
        melhor_percurso = populacao[indice_melhor].copy()
        melhor_custo = custos[indice_melhor]
        self.custos = []

        for _ in range(self.geracoes):
            nova_populacao = [melhor_percurso.copy()]

            while len(nova_populacao) < self.tam_populacao:
                pai1 = self.selecao(populacao, custos)
                pai2 = self.selecao(populacao, custos)

                if random.random() < self.taxa_crossover:
                    filho = self.crossover_ox(pai1, pai2)
                else:
                    filho = pai1.copy()

                if random.random() < self.taxa_mutacao:
                    filho = self.mutacao(filho)

                nova_populacao.append(filho)

            populacao = nova_populacao
            custos = [self.calcula_custo(ind) for ind in populacao]

            indice_melhor = custos.index(min(custos))
            custo = custos[indice_melhor]
            self.custos.append(custo)

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_percurso = populacao[indice_melhor].copy()

        return melhor_percurso, melhor_custo


if __name__ == "__main__":
    pass