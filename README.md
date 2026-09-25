# Projeto Final — Sistema de Cadastro de Reserva de Estudantes

Sistema de lista de espera de uma escola em Guarujá/SP, com três perfis de
uso em sequência na mesma execução: **Secretário(a) → Diretor(a) →
Assistente**, conforme a Seção 3 do enunciado.

## Estrutura de arquivos

```
main.py                     Interface com o usuário (menus, input/print).
                             Não acessa lista/árvore/grafo diretamente.

atribuicoes_secretario.py   Ponte entre main.py e a lista encadeada.
atribuicoes_diretor.py      Ponte entre main.py e a árvore binária de busca.
atribuicoes_assistente.py   Ponte entre main.py e o grafo de cidades.

pessoa.py                   Classe Pessoa (nome, idade, telefone, cidade).
lista_encadeada.py          Lista encadeada simples (perfil secretário).
arvore_binaria.py           Árvore binária de busca, chave = nome (perfil diretor).
grafo.py                    Grafo ponderado não-direcionado + Dijkstra (perfil assistente).
cidades.py                  Leitura das cidades do csv (para sorteio de cidade).

cidades_vizinhas.csv        Arquivo de distâncias entre cidades (não alterado).

tests/test_sistema.py       Testes automatizados (unittest).
```

Nenhuma estrutura de dados (`ListaEncadeada`, `ArvoreBinariaBusca`,
`Grafo`) é importada por `main.py`: ele só conhece as funções dos três
módulos `atribuicoes_*.py`, como pedido no enunciado.

## Observações de implementação

- **Lista encadeada (secretário):** inserção no fim, busca linear por
  nome (case-insensitive), contagem em O(1).
- **Árvore binária de busca (diretor):** é gerada uma única vez, a
  partir da lista encadeada, quando o(a) diretor(a) assume o sistema
  (`atribuicoes_diretor.gerar_arvore_a_partir_da_lista`). Como o nome é
  a chave da árvore, renomear alguém remove e reinsere o nó; alterar
  idade/telefone apenas atualiza o objeto `Pessoa` em memória, sem
  mexer na estrutura da árvore.
- **Grafo (assistente):** montado diretamente do `cidades_vizinhas.csv`
  (arestas não-direcionadas cidade1↔cidade2 com peso = distância). O
  caminho "passando por uma cidade intermediária" é obtido concatenando
  o menor caminho até a intermediária com o menor caminho da
  intermediária até o destino — por isso cidades podem se repetir no
  caminho final, como o próprio enunciado observa.
- A lista de pessoas usada pelo(a) assistente vem da árvore do(a)
  diretor(a) já **depois** das edições/exclusões feitas por ele(a), ou
  seja, reflete o estado mais atual da lista de espera.
- `cidades_vizinhas.csv` não foi alterado (conteúdo e formato originais).

