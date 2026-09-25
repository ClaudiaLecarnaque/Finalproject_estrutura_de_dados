"""
Interface entre main.py e a estrutura de dados usada pelo(a) secretario(a)
(lista encadeada simples). main.py NUNCA importa lista_encadeada.py ou
cidades.py diretamente -- ele so conversa com este modulo.
"""

import random

from lista_encadeada import ListaEncadeada
from pessoa import Pessoa
from cidades import carregar_cidades

CAMINHO_CSV_CIDADES = "cidades_vizinhas.csv"

_cidades_disponiveis = None


def _obter_cidades_disponiveis():
    """Carrega (uma unica vez) as cidades existentes no csv, usadas para
    sortear a cidade de uma nova pessoa cadastrada."""
    global _cidades_disponiveis
    if _cidades_disponiveis is None:
        _cidades_disponiveis = carregar_cidades(CAMINHO_CSV_CIDADES)
    return _cidades_disponiveis


def criar_lista_espera():
    """Cria e retorna uma lista de espera vazia (lista encadeada)."""
    return ListaEncadeada()


def cadastrar_pessoa(lista_espera, nome, idade, telefone):
    """Cadastra uma nova pessoa na lista de espera, com uma cidade
    sorteada aleatoriamente dentre as cidades do cidades_vizinhas.csv."""
    cidade = random.choice(_obter_cidades_disponiveis())
    pessoa = Pessoa(nome, idade, telefone, cidade)
    lista_espera.inserir(pessoa)
    return pessoa


def consultar_pessoa(lista_espera, nome):
    """Retorna a Pessoa com o nome informado, ou None se nao encontrada."""
    return lista_espera.buscar(nome)


def contar_pessoas(lista_espera):
    """Retorna a quantidade de pessoas cadastradas na lista de espera."""
    return lista_espera.contar()


def obter_lista_pessoas(lista_espera):
    """Retorna todas as pessoas cadastradas, como uma lista Python
    (usado para gerar a arvore binaria de busca do(a) diretor(a))."""
    return lista_espera.para_lista_python()
