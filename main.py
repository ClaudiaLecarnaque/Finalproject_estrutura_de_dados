"""
Sistema de cadastro de reserva de estudantes - Projeto Final
Disciplina de Estrutura de Dados

ENTREGA 4.1 - Operacoes do(a) Secretario(a) (Secao 3.1)

Interface com o usuario (menus, leitura de teclado). Este arquivo NAO se
comunica diretamente com as estruturas de dados: toda a comunicacao passa
pelo modulo atribuicoes_secretario.py.
"""

import atribuicoes_secretario as secretario


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
# Ponto de entrada
# ---------------------------------------------------------------------

def main():
    menu_secretario()


if __name__ == "__main__":
    main()
