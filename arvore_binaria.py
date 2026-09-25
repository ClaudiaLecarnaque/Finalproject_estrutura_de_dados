"""
Arvore binaria de busca (ABB), usada nas operacoes do(a) diretor(a).

A chave de cada no e o nome da pessoa (comparacao case-insensitive).
A arvore e gerada a partir da lista encadeada do(a) secretario(a)
(ver atribuicoes_diretor.gerar_arvore_a_partir_da_lista).

Justificativa (conforme o enunciado): as operacoes do(a) diretor(a)
dependem fortemente de busca por nome, e a lista encadeada simples nao e
eficiente para isso. Por isso, a partir do perfil diretor, a lista de
espera passa a ser representada por uma ABB.
"""


class NoArvore:
    def __init__(self, pessoa):
        self.pessoa = pessoa
        self.esquerda = None
        self.direita = None


class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    # ---------------------------------------------------------------
    # Insercao
    # ---------------------------------------------------------------
    def inserir(self, pessoa):
        self.raiz = self._inserir_recursivo(self.raiz, pessoa)

    def _inserir_recursivo(self, no, pessoa):
        if no is None:
            return NoArvore(pessoa)
        if pessoa.nome.strip().lower() < no.pessoa.nome.strip().lower():
            no.esquerda = self._inserir_recursivo(no.esquerda, pessoa)
        else:
            no.direita = self._inserir_recursivo(no.direita, pessoa)
        return no

    # ---------------------------------------------------------------
    # Busca
    # ---------------------------------------------------------------
    def buscar(self, nome):
        return self._buscar_recursivo(self.raiz, nome.strip().lower())

    def _buscar_recursivo(self, no, nome_busca):
        if no is None:
            return None
        nome_no = no.pessoa.nome.strip().lower()
        if nome_busca == nome_no:
            return no.pessoa
        if nome_busca < nome_no:
            return self._buscar_recursivo(no.esquerda, nome_busca)
        return self._buscar_recursivo(no.direita, nome_busca)

    # ---------------------------------------------------------------
    # Remocao
    # ---------------------------------------------------------------
    def remover(self, nome):
        self.raiz, removido = self._remover_recursivo(self.raiz, nome.strip().lower())
        return removido

    def _remover_recursivo(self, no, nome_busca):
        if no is None:
            return no, False

        nome_no = no.pessoa.nome.strip().lower()
        if nome_busca < nome_no:
            no.esquerda, removido = self._remover_recursivo(no.esquerda, nome_busca)
            return no, removido
        if nome_busca > nome_no:
            no.direita, removido = self._remover_recursivo(no.direita, nome_busca)
            return no, removido

        # Encontramos o no a remover.
        if no.esquerda is None:
            return no.direita, True
        if no.direita is None:
            return no.esquerda, True

        # Dois filhos: substitui pelo sucessor (menor da subarvore direita).
        sucessor = self._no_minimo(no.direita)
        no.pessoa = sucessor.pessoa
        no.direita, _ = self._remover_recursivo(no.direita, sucessor.pessoa.nome.strip().lower())
        return no, True

    def _no_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    # ---------------------------------------------------------------
    # Renomear (precisa remover e reinserir, pois o nome e a chave)
    # ---------------------------------------------------------------
    def renomear(self, nome_atual, novo_nome):
        pessoa = self.buscar(nome_atual)
        if pessoa is None:
            return False
        self.remover(nome_atual)
        pessoa.nome = novo_nome
        self.inserir(pessoa)
        return True

    # ---------------------------------------------------------------
    # Primeiro / ultimo em ordem alfabetica
    # ---------------------------------------------------------------
    def primeiro_em_ordem(self):
        if self.raiz is None:
            return None
        return self._no_minimo(self.raiz).pessoa

    def ultimo_em_ordem(self):
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.pessoa

    # ---------------------------------------------------------------
    # Percurso em ordem (retorna todas as pessoas, ordenadas por nome)
    # ---------------------------------------------------------------
    def em_ordem(self):
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _em_ordem_recursivo(self, no, resultado):
        if no is not None:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append(no.pessoa)
            self._em_ordem_recursivo(no.direita, resultado)
