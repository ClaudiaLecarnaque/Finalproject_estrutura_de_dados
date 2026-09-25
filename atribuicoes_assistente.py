"""
Interface entre main.py e a estrutura de dados usada pelo(a) assistente
(grafo ponderado nao-direcionado). main.py NUNCA importa grafo.py
diretamente -- ele so conversa com este modulo.
"""

from grafo import (
    carregar_grafo,
    caminho_com_intermediaria,
    cidade_mais_proxima_com_moradores,
)

CAMINHO_CSV_CIDADES = "cidades_vizinhas.csv"

CIDADE_ESCOLA = "Guarujá"
CIDADE_INTERMEDIARIA_FIXA = "Indaiatuba"


def gerar_grafo():
    """Monta o grafo de cidades vizinhas a partir do cidades_vizinhas.csv."""
    return carregar_grafo(CAMINHO_CSV_CIDADES)


def menor_distancia_ate_pessoa(grafo, pessoa):
    """Menor caminho entre a cidade da escola e a cidade da pessoa."""
    return grafo.dijkstra(CIDADE_ESCOLA, pessoa.cidade)


def menor_distancia_com_intermediaria(grafo, pessoa):
    """Menor caminho entre a cidade da escola e a cidade da pessoa,
    passando pela cidade intermediaria fixa (Indaiatuba)."""
    return caminho_com_intermediaria(
        grafo, CIDADE_ESCOLA, pessoa.cidade, CIDADE_INTERMEDIARIA_FIXA
    )


def cidade_mais_proxima_da_escola_com_moradores(grafo, pessoas):
    """Dentre as cidades das pessoas cadastradas, retorna a mais proxima
    da cidade da escola: (cidade, distancia)."""
    cidades = [pessoa.cidade for pessoa in pessoas]
    return cidade_mais_proxima_com_moradores(grafo, CIDADE_ESCOLA, cidades)
