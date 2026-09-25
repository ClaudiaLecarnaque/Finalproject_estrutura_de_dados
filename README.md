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


## Como rodar os testes automatizados

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem a lista encadeada, a árvore binária (inserção, busca,
renomear, remoção com dois filhos) e o grafo — inclusive dois testes que
reproduzem exatamente o exemplo do enunciado (pessoa em Vargem Grande
Paulista): o menor caminho direto dá custo **127** e, passando por
Indaiatuba, custo **511**, batendo com as figuras do documento do
projeto.

## Roteiro sugerido para testar manualmente cada perfil

**Secretário(a):**
1. Cadastre 3–4 pessoas (opção 1) — repare que a cidade é sempre
   sorteada, nunca digitada.
2. Consulte uma pessoa existente e uma inexistente (opção 2).
3. Veja a quantidade cadastrada (opção 3).
4. Finalize (opção 4) — o sistema passa para o(a) diretor(a).

**Diretor(a):**
1. Altere o nome de alguém (opção 1 → 1) e depois busque pelo nome
   antigo (deve dizer "não cadastrada") e pelo novo (deve encontrar).
2. Altere idade e telefone de outra pessoa.
3. Descadastre alguém, primeiro digitando **N** (cancela) e depois **S**
   (confirma) — confira que a pessoa some da lista.
4. Veja a primeira e a última pessoa em ordem alfabética (opções 3 e 4).
5. Finalize (opção 5) — o sistema passa para o(a) assistente.

**Assistente:**
1. Veja a menor distância até a cidade de uma pessoa cadastrada (opção 1).
2. Veja a menor distância passando por Indaiatuba (opção 2) — repare que
   o caminho pode repetir cidades, o que é esperado.
3. Veja a cidade com morador cadastrado mais próxima da escola (opção 3).
4. Finalize (opção 4) — encerra o programa.

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

## Sugestão de entrega (GitHub)

Como sugerido no enunciado, você pode criar um repositório no GitHub com
todos os arquivos acima e compartilhá-lo com o tutor. Como o projeto já
está com os três perfis integrados, o mesmo repositório serve para as
entregas 4.1, 4.2 e 4.3 — cada entrega pode corresponder a um commit.
