# Nomenclatura Xadrez (en)

## Básico

O xadrez é um jogo de tabuleiro que possui uma matriz de movimento 8x8. As colunas vão de "a" a "h" e as linhas de 1 a 8.

---
## Representação das Peças

- Peão: sem letra **[ ]**
- Rei => **[K]**
- Rainha => **[Q]**
- Torre => **[R]**
- Bispo => **[B]**
- Cavalo => **[N]**
---
## Representação das Rodadas

Branco sempre começa e preto joga após. Para representar as rodadas teremos o seguinte padrão:

- **1. [movimento branco] [movimento preto]**
- **2. [movimento branco] [movimento preto]**
- **3. [movimento branco] [movimento preto]**

---

## Representação do Movimento

### Caso Não Haja Captura

Padrão: **[Letra da Peça][Destino]**

#### Exemplos

No caso do peão a letra da peça é vazia, por tanto temos:

**e4**: Pẽao se move para casa *e4*.

<!-- Colocar um gif aqui demostrando o movimento-->

**Kf3**: Cavalo se move para casa *f3*.

![Alt Text](/images/knight_to_f3.gif)

**Outro Exemplo aqui**

<!-- Colocar um gif aqui demostrando o movimento-->
    
### Caso Haja Captura

Um 'x' é colocado antes da célula de destino da peça.

**[Letra da Peça][x][Destino]**

#### Exemplos

**Bxe5**: Bispo captura a peça que está em *e5*

<!-- Coloca um gif aqui -->

No caso do peão a letra da peça é vazia, portanto temos:

**exd6**: Peão da coluna *e* captura peça que está em *d6* ¹

[1] O mesmo é válido para captura en passant.
Digamos que o peão preto que estava em *e2* se mova para *e4*, o movimento que representa a captura en passant de um peão branca que estaria na coluna *d* é: **dxe3**, com *e3* representando a posição de destino do peão.
<!-- Coloca gif aqui -->

### Movimentos Ambíguos

Se duas peça idênticas podem se mover para a mesma posição a nomenclatura segue as seguintes regras:

[1] Caso a coluna da partida seja diferente entre as duas ou mais peças, então ela é suficiente para clarificar o movimento, a representação fica da seguinte forma:

**[Letra da peça][Coluna da partida][Destino]**

#### Exemplo

<!-- Colocar exemplos -->

[2] Caso a coluna seja a mesma, as linhas das peças sejam diferentes representamos apenas a linha, como clarificador.

**[Letra da peça][Linhas da partida][Destino]**

#### Exemplo

<!-- Colocar exemplos -->

[3] Caso nem a coluna nem a linha sejam suficiente para esclarecer um movimento ambíguo (o que só acontece em casos raros), então representamos a linha e a coluna da peça para clarificar o movimento.

**[Letra da peça][Coluna da partida][Linhas da partida][Destino]**

#### Exemplo

<!-- Colocar exemplos -->

### Promoções de Peões

Quando um peão vai se promover a nomenclatura utilizada é:

**[Destino][Letra da Peça de Promoção]**

#### Exemplo

### Oferta de Empate

Indicado pelo símbolo **(=)**


### Roque

Para rocar pelo lado do rei: **(0-0)**
Para rocar pelo lado da rainha: **(0-0-0)**

### Check

Toda vez que houver um check basta adicionar um **+** ao final da representação do movimento.

#### Exemplo

<!-- Colocar exemplo -->

### Check Mate

Representado pelo sinal **#** ao final da representação.

---

## Referências

- https://en.wikipedia.org/wiki/Algebraic_notation
    


