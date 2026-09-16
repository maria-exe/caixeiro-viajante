import time
import random
import statistics
import csv

from problema import Grafo
from tempera_simulada import TemperaSimulada
from busca_ag import AlgoritmoGenetico

TAMANHOS_INSTANCIA = [10, 25, 50, 100]
N_EXECUCOES = 10
SEED = 42

PARAMS_TS = dict(
    temperatura_atual=1000,
    taxa_resfriamento=0.995,
    temp_iteracao=100,
)
LIMITE_TS = 1

PARAMS_AG = dict(
    tam_populacao=200,
    taxa_crossover=0.8,
    taxa_mutacao=0.15,
    geracoes=600,
    k=2,
)

INSTANCIAS_TSPLIB = {
    "berlin52": {"arquivo": "berlin52.tsp", "otimo": 7542},
}


def gera_instancia_propria(n_cidades, seed=None):
    if seed is not None:
        random.seed(seed)
    grafo = Grafo()
    grafo.gera_vertices(n_cidades)
    grafo.popula_matriz()
    return grafo.grafo.tolist()


def gera_instancia_tsplib(arquivo):
    grafo = Grafo()
    grafo.carrega_tsplib(arquivo)
    grafo.popula_matriz()
    return grafo.grafo.tolist()


def roda_ts(matriz, n_execucoes):
    custos, tempos = [], []
    for _ in range(n_execucoes):
        ts = TemperaSimulada(matriz, **PARAMS_TS)
        inicio = time.perf_counter()
        _, custo = ts.executa_busca(LIMITE_TS)
        tempos.append(time.perf_counter() - inicio)
        custos.append(custo)
    return custos, tempos


def roda_ag(matriz, n_execucoes):
    custos, tempos = [], []
    for _ in range(n_execucoes):
        ag = AlgoritmoGenetico(grafo=matriz, **PARAMS_AG)
        inicio = time.perf_counter()
        _, custo = ag.executa_busca()
        tempos.append(time.perf_counter() - inicio)
        custos.append(custo)
    return custos, tempos


def resume(valores):
    media = statistics.mean(valores)
    desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0
    return media, desvio, min(valores), max(valores)


def monta_linha(nome_instancia, tamanho, algoritmo, custos, tempos, otimo=None):
    media_c, desvio_c, min_c, max_c = resume(custos)
    media_t, desvio_t, min_t, max_t = resume(tempos)
    gap = ((media_c - otimo) / otimo * 100) if otimo else ""
    return [nome_instancia, tamanho, algoritmo,
            round(media_c, 2), round(desvio_c, 2), round(min_c, 2), round(max_c, 2),
            round(media_t, 4), round(desvio_t, 4),
            otimo if otimo else "", round(gap, 2) if otimo else ""]


def main():
    linhas = []

    for indice, tamanho in enumerate(TAMANHOS_INSTANCIA, start=1):
        nome_instancia = f"I{indice:02d}"
        print(f"\n{nome_instancia} — {tamanho}")
        matriz = gera_instancia_propria(tamanho, seed=SEED + tamanho)

        print("Rodando TS...")
        custos_ts, tempos_ts = roda_ts(matriz, N_EXECUCOES)
        linhas.append(monta_linha(nome_instancia, tamanho, "TS", custos_ts, tempos_ts))

        print("Rodando AG...")
        custos_ag, tempos_ag = roda_ag(matriz, N_EXECUCOES)
        linhas.append(monta_linha(nome_instancia, tamanho, "AG", custos_ag, tempos_ag))

    for nome, info in INSTANCIAS_TSPLIB.items():
        print(f"\n\Rodando{nome}")
        matriz = gera_instancia_tsplib(info["arquivo"])
        tamanho = len(matriz)

        print("Rodando TS...")
        custos_ts, tempos_ts = roda_ts(matriz, N_EXECUCOES)
        linhas.append(monta_linha(nome, tamanho, "TS", custos_ts, tempos_ts, info["otimo"]))

        print("Rodando AG...")
        custos_ag, tempos_ag = roda_ag(matriz, N_EXECUCOES)
        linhas.append(monta_linha(nome, tamanho, "AG", custos_ag, tempos_ag, info["otimo"]))

    cabecalho = ["Instância", "N cidades", "Algoritmo",
                 "Custo médio", "Desvio padrão custo", "Melhor custo", "Pior custo",
                 "Tempo médio (s)", "Desvio padrão tempo",
                 "Ótimo conhecido", "Gap (%)"]

    with open("recalibrado.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)


if __name__ == "__main__":
    main()