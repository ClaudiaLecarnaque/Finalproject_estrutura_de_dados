"""
Funcao utilitaria para ler as cidades existentes no arquivo
cidades_vizinhas.csv (colunas 1 e 2). Usada para sortear a cidade de uma
pessoa recem-cadastrada.

Este modulo NAO altera o conteudo/formato do cidades_vizinhas.csv, apenas
o le.
"""

import csv


def carregar_cidades(caminho_csv):
    """Retorna a lista (ordenada, sem repeticao) de todas as cidades que
    aparecem nas duas primeiras colunas do csv."""
    cidades = set()
    with open(caminho_csv, encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        for linha in leitor:
            if len(linha) < 2:
                continue
            cidades.add(linha[0].strip())
            cidades.add(linha[1].strip())
    return sorted(cidades)
