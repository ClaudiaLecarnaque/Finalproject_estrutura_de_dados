"""
Interface entre main.py e a estrutura de dados usada pelo(a) diretor(a)
(arvore binaria de busca). main.py NUNCA importa arvore_binaria.py
diretamente -- ele so conversa com este modulo.
"""

from arvore_binaria import ArvoreBinariaBusca


def gerar_arvore_a_partir_da_lista(pessoas):
    """Recebe a lista de pessoas (obtida via
    atribuicoes_secretario.obter_lista_pessoas) e monta a arvore binaria
    de busca correspondente, com o nome da pessoa como chave."""
    arvore = ArvoreBinariaBusca()
    for pessoa in pessoas:
        arvore.inserir(pessoa)
    return arvore


def buscar_pessoa(arvore, nome):
    return arvore.buscar(nome)


def editar_nome(arvore, nome_atual, novo_nome):
    """Altera o nome de uma pessoa. Como o nome e a chave da arvore, isso
    exige remover e reinserir o no."""
    return arvore.renomear(nome_atual, novo_nome)


def editar_idade(arvore, nome, nova_idade):
    pessoa = arvore.buscar(nome)
    if pessoa is None:
        return False
    pessoa.idade = nova_idade
    return True


def editar_telefone(arvore, nome, novo_telefone):
    pessoa = arvore.buscar(nome)
    if pessoa is None:
        return False
    pessoa.telefone = novo_telefone
    return True


def descadastrar_pessoa(arvore, nome):
    return arvore.remover(nome)


def primeira_pessoa_alfabetica(arvore):
    return arvore.primeiro_em_ordem()


def ultima_pessoa_alfabetica(arvore):
    return arvore.ultimo_em_ordem()


def listar_pessoas(arvore):
    """Retorna todas as pessoas atualmente na lista de espera (ja
    refletindo edicoes/exclusoes feitas pelo(a) diretor(a)), ordenadas
    por nome. Usado pelo(a) assistente."""
    return arvore.em_ordem()
