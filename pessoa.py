"""
Modulo com o modelo de dados Pessoa.

Cada pessoa cadastrada na lista de espera possui nome, idade, telefone e
uma cidade (atribuida aleatoriamente no momento do cadastro).
"""


class Pessoa:
    def __init__(self, nome, idade, telefone, cidade):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.cidade = cidade

    def __str__(self):
        return (
            f"Nome: {self.nome} | Idade: {self.idade} | "
            f"Telefone: {self.telefone} | Cidade: {self.cidade}"
        )

    def __repr__(self):
        return self.__str__()
