"""
Sistema de cadastro de reserva de estudantes - Projeto Final
Disciplina de Estrutura de Dados

Interface com o usuario (menus, leitura de teclado). Este arquivo NAO se
comunica diretamente com as estruturas de dados (Lista Encadeada, Arvore,
Grafo): toda a comunicacao passa pelos modulos atribuicoes_secretario.py,
atribuicoes_diretor.py e atribuicoes_assistente.py.

Fluxo do sistema (simulando, em uma unica execucao, a troca de
funcionarios que em um sistema real usaria um banco de dados):
    1) Secretario(a) cadastra pessoas na lista de espera.
    2) Diretor(a) valida/edita/consulta a lista (agora como arvore
       binaria de busca).
    3) Assistente consulta distancias entre cidades (grafo ponderado).
"""

import atribuicoes_secretario as secretario
import atribuicoes_diretor as diretor
import atribuicoes_assistente as assistente


# ---------------------------------------------------------------------
# Funcoes auxiliares de leitura/validacao de entrada
# ---------------------------------------------------------------------

def ler_opcao(minimo, maximo, prompt="Digite sua opção: "):
    """Le uma opcao de menu, repetindo ate que um numero inteiro dentro
    do intervalo [minimo, maximo] seja informado."""
    while True:
        entrada = input(prompt).strip()
        if entrada.lstrip("-").isdigit():
            opcao = int(entrada)
            if minimo <= opcao <= maximo:
                return opcao
        print(f"Opção inválida. Digite um número entre {minimo} e {maximo}.")


def ler_idade():
    while True:
        entrada = input("Digite a idade: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("Idade inválida. Digite um número inteiro.")


def ler_confirmacao(prompt):
    while True:
        resposta = input(prompt).strip().upper()
        if resposta in ("S", "N"):
            return resposta == "S"
        print("Resposta inválida. Digite S ou N.")


# ---------------------------------------------------------------------
# Menu do(a) Secretario(a) - Secao 3.1
# ---------------------------------------------------------------------

def menu_secretario():
    lista_espera = secretario.criar_lista_espera()

    print("\n------------- Olá, Secretário(a)! -------------\n")

    while True:
        print("Você deseja:")
        print("(1) Cadastrar nova pessoa na lista de espera.")
        print("(2) Consultar pessoa cadastrada.")
        print("(3) Ver quantidade de pessoas cadastradas.")
        print("(4) Finalizar execução.")
        opcao = ler_opcao(1, 4)
        print()

        if opcao == 1:
            nome = input("Digite o nome da pessoa: ").strip()
            idade = ler_idade()
            telefone = input("Digite o telefone: ").strip()
            secretario.cadastrar_pessoa(lista_espera, nome, idade, telefone)
            # Mostra a lista de espera completa (e não só a pessoa recem-cadastrada),
            # como pedido no enunciado ("mostra a lista após a inclusão da pessoa").
            for p in secretario.obter_lista_pessoas(lista_espera):
                print(p)

        elif opcao == 2:
            nome = input("Digite o nome da pessoa: ").strip()
            pessoa = secretario.consultar_pessoa(lista_espera, nome)
            if pessoa is None:
                print("Pessoa não cadastrada. Tem certeza que o nome está certo?")
            else:
                print(pessoa)

        elif opcao == 3:
            print(f"São {secretario.contar_pessoas(lista_espera)} pessoas na lista de espera.")

        elif opcao == 4:
            print("Fim das atividades sob responsabilidade do(a) Secretário(a).")
            break

        print()

    return lista_espera


# ---------------------------------------------------------------------
# Menu do(a) Diretor(a) - Secao 3.2
# ---------------------------------------------------------------------

def menu_diretor(lista_espera):
    pessoas = secretario.obter_lista_pessoas(lista_espera)
    arvore = diretor.gerar_arvore_a_partir_da_lista(pessoas)

    print("\n------------- Olá, Diretor(a)! -------------\n")

    while True:
        print("Você deseja:")
        print("(1) Alterar nome, idade ou telefone de pessoa cadastrada.")
        print("(2) Descadastrar pessoa.")
        print("(3) Obter informações da primeira pessoa em ordem alfabética de nome.")
        print("(4) Obter informações da última pessoa em ordem alfabética de nome.")
        print("(5) Confirmar validade da lista de espera e finalizar execução.")
        opcao = ler_opcao(1, 5)
        print()

        if opcao == 1:
            nome = input("Digite o nome da pessoa que você quer editar: ").strip()
            pessoa = diretor.buscar_pessoa(arvore, nome)
            if pessoa is None:
                print("Pessoa não cadastrada. Tem certeza que o nome está certo?")
            else:
                print(pessoa)
                sub_opcao = ler_opcao(
                    1, 3,
                    "O que você quer editar? Digite 1 para nome, 2 para idade ou 3 para telefone: ",
                )
                if sub_opcao == 1:
                    novo_nome = input("Digite o novo nome: ").strip()
                    diretor.editar_nome(arvore, nome, novo_nome)
                elif sub_opcao == 2:
                    nova_idade = ler_idade()
                    diretor.editar_idade(arvore, nome, nova_idade)
                else:
                    novo_telefone = input("Digite o novo telefone: ").strip()
                    diretor.editar_telefone(arvore, nome, novo_telefone)
                print("Dados atualizados com sucesso.")

        elif opcao == 2:
            nome = input("Digite o nome da pessoa que você quer descadastrar: ").strip()
            pessoa = diretor.buscar_pessoa(arvore, nome)
            if pessoa is None:
                print("Pessoa não cadastrada ou lista de espera vazia. Tem certeza que o nome da pessoa está certo?")
            else:
                print(pessoa)
                confirmou = ler_confirmacao(
                    f"Tem certeza que deseja descadastrar {pessoa.nome}? Digite S ou N: "
                )
                if confirmou:
                    diretor.descadastrar_pessoa(arvore, nome)
                    print(f"{pessoa.nome} descadastrado(a) com sucesso.")
                else:
                    print("Operação cancelada.")

        elif opcao == 3:
            pessoa = diretor.primeira_pessoa_alfabetica(arvore)
            if pessoa is None:
                print("Não há pessoas cadastradas na lista de espera.")
            else:
                print(pessoa)

        elif opcao == 4:
            pessoa = diretor.ultima_pessoa_alfabetica(arvore)
            if pessoa is None:
                print("Não há pessoas cadastradas na lista de espera.")
            else:
                print(pessoa)

        elif opcao == 5:
            print("Fim das atividades sob responsabilidade do(a) Diretor(a).")
            break

        print()

    return arvore


# ---------------------------------------------------------------------
# Menu do(a) Assistente - Secao 3.3
# ---------------------------------------------------------------------

def menu_assistente(arvore):
    grafo = assistente.gerar_grafo()

    print("\n------------- Olá, Assistente! -------------\n")

    while True:
        print("Você deseja:")
        print("(1) Ver a menor distância entre a cidade da escola e a cidade de uma pessoa.")
        print("(2) Ver a menor distância da cidade da escola até a cidade da pessoa passando por uma cidade específica.")
        print("(3) Ver dados da(s) pessoa(s) que mora(m) na cidade mais perto da cidade da escola (incluindo distância).")
        print("(4) Finalizar execução.")
        opcao = ler_opcao(1, 4)
        print()

        if opcao == 1:
            nome = input("Digite o nome da pessoa cuja cidade te interessa: ").strip()
            pessoa = diretor.buscar_pessoa(arvore, nome)
            if pessoa is None:
                print("Pessoa não cadastrada ou lista de espera vazia. Tem certeza que o nome da pessoa está certo?")
            else:
                print(pessoa)
                caminho, custo = assistente.menor_distancia_ate_pessoa(grafo, pessoa)
                if caminho is None:
                    print(f"Não foi encontrado caminho entre {assistente.CIDADE_ESCOLA} e {pessoa.cidade}.")
                else:
                    print(f"Menor caminho = {caminho} com custo {custo:g}")

        elif opcao == 2:
            nome = input("Digite o nome da pessoa cuja cidade te interessa: ").strip()
            pessoa = diretor.buscar_pessoa(arvore, nome)
            if pessoa is None:
                print("Pessoa não cadastrada ou lista de espera vazia. Tem certeza que o nome da pessoa está certo?")
            else:
                print(pessoa)
                caminho, custo = assistente.menor_distancia_com_intermediaria(grafo, pessoa)
                if caminho is None:
                    print(
                        f"Não foi encontrado caminho entre {assistente.CIDADE_ESCOLA} e "
                        f"{pessoa.cidade} passando por {assistente.CIDADE_INTERMEDIARIA_FIXA}."
                    )
                else:
                    print(f"Menor caminho = {caminho} com custo {custo:g}")

        elif opcao == 3:
            pessoas = diretor.listar_pessoas(arvore)
            if not pessoas:
                print("Não há pessoas cadastradas na lista de espera.")
            else:
                cidade, distancia = assistente.cidade_mais_proxima_da_escola_com_moradores(grafo, pessoas)
                if cidade is None:
                    print("Não foi possível determinar a cidade mais próxima.")
                else:
                    print(
                        f"A cidade mais próxima à cidade da escola que tem moradores na "
                        f"lista de espera (ver abaixo) é {cidade}. Distância = {distancia:g}"
                    )
                    for pessoa in pessoas:
                        if pessoa.cidade == cidade:
                            print(pessoa)

        elif opcao == 4:
            print("Fim das atividades sob responsabilidade do(a) Assistente. Encerrando o sistema.")
            break

        print()


# ---------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------

def main():
    lista_espera = menu_secretario()
    arvore = menu_diretor(lista_espera)
    menu_assistente(arvore)


if __name__ == "__main__":
    main()
