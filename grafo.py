"""
Grafo ponderado e nao-direcionado das cidades vizinhas, montado a partir
de cidades_vizinhas.csv (cidade1;cidade2;distancia em cada linha).

Usado nas operacoes do(a) assistente:
  - menor caminho entre duas cidades (Dijkstra);
  - menor caminho passando por uma cidade intermediaria fixa;
  - cidade com morador cadastrado mais proxima da cidade da escola.
"""

import csv
import heapq


class Grafo:
    def __init__(self):
        self.adjacencia = {}  # cidade -> lista de (cidade_vizinha, peso)

    def adicionar_aresta(self, cidade1, cidade2, peso):
        self.adjacencia.setdefault(cidade1, []).append((cidade2, peso))
        self.adjacencia.setdefault(cidade2, []).append((cidade1, peso))

    def possui_cidade(self, cidade):
        return cidade in self.adjacencia

    def dijkstra(self, origem, destino):
        """Retorna (caminho, custo) com o menor caminho entre origem e
        destino. Se nao houver caminho (ou cidade desconhecida), retorna
        (None, float('inf'))."""
        if origem not in self.adjacencia or destino not in self.adjacencia:
            return None, float("inf")

        distancias = {cidade: float("inf") for cidade in self.adjacencia}
        anteriores = {cidade: None for cidade in self.adjacencia}
        distancias[origem] = 0

        fila = [(0, origem)]
        visitados = set()

        while fila:
            dist_atual, cidade_atual = heapq.heappop(fila)
            if cidade_atual in visitados:
                continue
            visitados.add(cidade_atual)

            if cidade_atual == destino:
                break

            for vizinho, peso in self.adjacencia[cidade_atual]:
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = cidade_atual
                    heapq.heappush(fila, (nova_dist, vizinho))

        if distancias[destino] == float("inf"):
            return None, float("inf")

        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        caminho.reverse()
        return caminho, distancias[destino]

    def distancias_a_partir_de(self, origem):
        """Retorna um dicionario {cidade: menor_distancia} a partir da
        origem, usando Dijkstra a partir de uma unica fonte."""
        distancias = {cidade: float("inf") for cidade in self.adjacencia}
        if origem not in self.adjacencia:
            return distancias

        distancias[origem] = 0
        fila = [(0, origem)]
        visitados = set()

        while fila:
            dist_atual, cidade_atual = heapq.heappop(fila)
            if cidade_atual in visitados:
                continue
            visitados.add(cidade_atual)

            for vizinho, peso in self.adjacencia[cidade_atual]:
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    heapq.heappush(fila, (nova_dist, vizinho))

        return distancias


def carregar_grafo(caminho_csv):
    """Le o cidades_vizinhas.csv e monta o grafo ponderado nao-direcionado."""
    grafo = Grafo()
    with open(caminho_csv, encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        for linha in leitor:
            if len(linha) < 3:
                continue
            cidade1 = linha[0].strip()
            cidade2 = linha[1].strip()
            peso_texto = linha[2].strip()
            if not cidade1 or not cidade2 or not peso_texto:
                continue
            peso = float(peso_texto)
            grafo.adicionar_aresta(cidade1, cidade2, peso)
    return grafo


def caminho_com_intermediaria(grafo, origem, destino, intermediaria):
    """Menor caminho entre origem e destino passando obrigatoriamente
    pela cidade intermediaria: concatena o menor caminho origem->
    intermediaria com o menor caminho intermediaria->destino.

    Como observado no enunciado, isso pode fazer com que uma mesma
    cidade (inclusive a propria intermediaria) apareca mais de uma vez
    no caminho final -- isso e esperado e nao deve ser "corrigido"."""
    caminho1, custo1 = grafo.dijkstra(origem, intermediaria)
    if caminho1 is None:
        return None, float("inf")

    caminho2, custo2 = grafo.dijkstra(intermediaria, destino)
    if caminho2 is None:
        return None, float("inf")

    caminho_completo = caminho1 + caminho2[1:]
    return caminho_completo, custo1 + custo2


def cidade_mais_proxima_com_moradores(grafo, origem, cidades_com_moradores):
    """Dentre as cidades informadas (cidades onde ha pessoas cadastradas),
    retorna a que possui a menor distancia ate a origem (cidade da
    escola). Retorna (cidade, distancia) ou (None, None) se nenhuma
    cidade candidata for alcancavel."""
    distancias = grafo.distancias_a_partir_de(origem)

    candidatos = [
        (distancias[cidade], cidade)
        for cidade in set(cidades_com_moradores)
        if cidade in distancias and distancias[cidade] < float("inf")
    ]
    if not candidatos:
        return None, None

    candidatos.sort(key=lambda item: item[0])
    menor_distancia, cidade_mais_proxima = candidatos[0]
    return cidade_mais_proxima, menor_distancia
