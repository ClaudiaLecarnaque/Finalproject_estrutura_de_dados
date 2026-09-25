"""
Lista encadeada simples, usada para armazenar a lista de espera enquanto
o(a) secretario(a) esta cadastrando as pessoas.

Estrutura escolhida conforme o enunciado: como o(a) secretario(a) pode
cadastrar quantas pessoas quiser, usamos uma lista encadeada simples (sem
tamanho fixo).
"""


class No:
    def __init__(self, pessoa):
        self.pessoa = pessoa
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def inserir(self, pessoa):
        """Insere uma nova pessoa no final da lista."""
        novo_no = No(pessoa)
        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self.tamanho += 1

    def buscar(self, nome):
        """Busca uma pessoa pelo nome (case-insensitive). Retorna o
        objeto Pessoa ou None se nao encontrado."""
        atual = self.inicio
        alvo = nome.strip().lower()
        while atual is not None:
            if atual.pessoa.nome.strip().lower() == alvo:
                return atual.pessoa
            atual = atual.proximo
        return None

    def contar(self):
        return self.tamanho

    def para_lista_python(self):
        """Retorna uma lista (list) do Python com todas as pessoas, na
        ordem em que foram cadastradas. Usado para gerar a arvore binaria
        de busca do(a) diretor(a)."""
        pessoas = []
        atual = self.inicio
        while atual is not None:
            pessoas.append(atual.pessoa)
            atual = atual.proximo
        return pessoas
