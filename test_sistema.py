"""
Testes automatizados do projeto final.

Rodar com:  python3 -m unittest discover -s tests -v
(a partir da pasta raiz do projeto, onde fica o cidades_vizinhas.csv)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pessoa import Pessoa
from lista_encadeada import ListaEncadeada
from arvore_binaria import ArvoreBinariaBusca
from grafo import carregar_grafo, caminho_com_intermediaria, cidade_mais_proxima_com_moradores
from cidades import carregar_cidades

CAMINHO_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cidades_vizinhas.csv")


class TestListaEncadeada(unittest.TestCase):
    def test_inserir_buscar_contar(self):
        lista = ListaEncadeada()
        self.assertEqual(lista.contar(), 0)
        lista.inserir(Pessoa("João", 23, "9878-9000", "Guatapará"))
        lista.inserir(Pessoa("Maria", 30, "1234-5678", "Santos"))
        self.assertEqual(lista.contar(), 2)

        encontrado = lista.buscar("joão")  # busca deve ignorar maiusculas/minusculas
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nome, "João")

        self.assertIsNone(lista.buscar("Paulo"))

    def test_para_lista_python_preserva_ordem(self):
        lista = ListaEncadeada()
        nomes = ["João", "Maria", "Paulo", "Miriam"]
        for nome in nomes:
            lista.inserir(Pessoa(nome, 20, "0000-0000", "Guarujá"))
        self.assertEqual([p.nome for p in lista.para_lista_python()], nomes)


class TestArvoreBinaria(unittest.TestCase):
    def _arvore_exemplo(self):
        arvore = ArvoreBinariaBusca()
        for nome, idade in [("João", 23), ("Mariana", 32), ("Paulo", 40), ("Miriam", 57)]:
            arvore.inserir(Pessoa(nome, idade, "0000-0000", "Guarujá"))
        return arvore

    def test_buscar(self):
        arvore = self._arvore_exemplo()
        self.assertIsNotNone(arvore.buscar("Paulo"))
        self.assertIsNone(arvore.buscar("Pedro"))

    def test_primeiro_e_ultimo_em_ordem_alfabetica(self):
        arvore = self._arvore_exemplo()
        # ordem alfabetica: João, Mariana, Miriam, Paulo
        self.assertEqual(arvore.primeiro_em_ordem().nome, "João")
        self.assertEqual(arvore.ultimo_em_ordem().nome, "Paulo")

    def test_renomear_atualiza_chave(self):
        arvore = self._arvore_exemplo()
        self.assertTrue(arvore.renomear("Paulo", "Paula"))
        self.assertIsNone(arvore.buscar("Paulo"))
        self.assertIsNotNone(arvore.buscar("Paula"))

    def test_remover_pessoa_com_dois_filhos(self):
        arvore = self._arvore_exemplo()
        self.assertTrue(arvore.remover("Mariana"))
        self.assertIsNone(arvore.buscar("Mariana"))
        # os demais continuam acessiveis e a ordenacao continua correta
        nomes_restantes = [p.nome for p in arvore.em_ordem()]
        self.assertEqual(nomes_restantes, ["João", "Miriam", "Paulo"])

    def test_remover_pessoa_inexistente(self):
        arvore = self._arvore_exemplo()
        self.assertFalse(arvore.remover("Pedro"))


class TestGrafo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grafo = carregar_grafo(CAMINHO_CSV)

    def test_menor_caminho_bate_com_exemplo_do_enunciado(self):
        # O enunciado mostra, para uma pessoa em Vargem Grande Paulista:
        # Menor caminho = ['Guarujá', 'Santos', 'São Bernardo do Campo',
        #                   'São Paulo', 'Vargem Grande Paulista'] com custo 127
        caminho, custo = self.grafo.dijkstra("Guarujá", "Vargem Grande Paulista")
        self.assertEqual(custo, 127)
        self.assertEqual(caminho[0], "Guarujá")
        self.assertEqual(caminho[-1], "Vargem Grande Paulista")

    def test_menor_caminho_com_intermediaria_bate_com_exemplo_do_enunciado(self):
        # O enunciado mostra, passando por Indaiatuba:
        # Menor caminho = ['Guarujá', 'Santos', 'Indaiatuba', 'Santos',
        #  'São Bernardo do Campo', 'São Paulo', 'Vargem Grande Paulista'] com custo 511
        caminho, custo = caminho_com_intermediaria(
            self.grafo, "Guarujá", "Vargem Grande Paulista", "Indaiatuba"
        )
        self.assertEqual(custo, 511)
        self.assertEqual(caminho[0], "Guarujá")
        self.assertEqual(caminho[-1], "Vargem Grande Paulista")
        self.assertIn("Indaiatuba", caminho)

    def test_cidade_mais_proxima_com_moradores(self):
        # Reproduz o exemplo do enunciado: unica pessoa cadastrada mora em
        # Vargem Grande Paulista -> cidade mais proxima = ela mesma, custo 127.
        cidade, distancia = cidade_mais_proxima_com_moradores(
            self.grafo, "Guarujá", ["Vargem Grande Paulista"]
        )
        self.assertEqual(cidade, "Vargem Grande Paulista")
        self.assertEqual(distancia, 127)

    def test_cidade_desconhecida_nao_quebra(self):
        caminho, custo = self.grafo.dijkstra("Guarujá", "Cidade Que Não Existe")
        self.assertIsNone(caminho)
        self.assertEqual(custo, float("inf"))


class TestCidades(unittest.TestCase):
    def test_carrega_cidades_das_duas_colunas(self):
        cidades = carregar_cidades(CAMINHO_CSV)
        self.assertIn("São Paulo", cidades)
        self.assertIn("Guarujá", cidades)
        self.assertIn("Vargem Grande Paulista", cidades)
        # nao deve haver repeticoes
        self.assertEqual(len(cidades), len(set(cidades)))


if __name__ == "__main__":
    unittest.main()
