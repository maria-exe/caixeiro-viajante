import random, itertools, math
from problema import Grafo

class TemperaSimulada:
    def __init__(self, grafo, temperatura_atual, taxa_resfriamento):
        self.matriz = grafo
        self.temperatura = temperatura_atual
        self.taxa_resfriamento = taxa_resfriamento

        self.custos = []

    def vizinhanca(self,  percurso): # equacao pronta!
        n = len(percurso)

        index_i = random.randint(0, n-2)
        index_j = random.randint(index_i + 1, n-1)

        if (index_i == 0) and (index_j == n -1):
            index_j = n - 2

        cidade = percurso[index_i - 1]
        inicio_seg = percurso[index_i]
        fim_seg = percurso[index_j]
        
        cidade_corte = percurso[(index_j+1) % n]

        custo_removido = (self.matriz[cidade][inicio_seg] + self.matriz[fim_seg][cidade_corte])
        custo_adicionado = (self.matriz[cidade][fim_seg] + self.matriz[inicio_seg][cidade_corte])

        delta = custo_adicionado - custo_removido
        return index_i, index_j, delta

    def calcula_custo(self, percurso): # equacao pronta!!!
        custo = 0 
        tam = len(percurso)

        for i in range(tam - 1):
            custo += self.matriz[percurso[i]][percurso[i+1]] 
        custo += self.matriz[percurso[-1]][percurso[0]]

        return custo

    def executa_busca(self, limite):
        n = len(self.matriz)

        percurso_atual = random.sample(range(n), n)
        custo_atual = self.calcula_custo(percurso_atual)
        
        melhor_percurso = percurso_atual.copy()
        melhor_custo = custo_atual
        
        temperatura = self.temperatura
        iteracoes_por_temperatura = 100

        while (temperatura >= limite):
            for _ in range(iteracoes_por_temperatura):
                i, j, delta = self.vizinhanca(percurso_atual)

                if delta < 0 or random.random() < math.exp(-delta / temperatura):
                    percurso_atual[i:j+1] = reversed(percurso_atual[i:j+1])
                    custo_atual += delta

                    if custo_atual < melhor_custo:
                        melhor_percurso = percurso_atual.copy()
                        melhor_custo = custo_atual

            self.custos.append(melhor_custo)
            temperatura = temperatura * self.taxa_resfriamento

        return melhor_percurso, melhor_custo

def main():
    grafo = Grafo()
    grafo.gera_vertices(5)
    grafo.popula_matriz()
    print(grafo.grafo)

    tempera = TemperaSimulada(grafo.grafo, 100, 0.95)
    rota = [0, 1, 2, 3, 4]

    for i in range(len(rota)):
        rota_nova = tempera.vizinhanca(rota)
        print(rota_nova)

    
    melhor_percurso, melhor_custo = tempera.executa_busca(1)
    print(melhor_custo)
    print(melhor_percurso)
    print(len(tempera.custos))
if __name__ == "__main__":
    main()




