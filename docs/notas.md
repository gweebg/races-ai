## Enunciado
Deselvolvimento de diversos algoritmos de procura para a resolução de
um jogo de simulação de carros simplificado.

## Regras da simulação

### Carro

- Tem capacidade de acelerar 1 unidade em qualquer direção
    - Aceleração representada por [*ax*,*ay*], em que *ax* e *ay* pertencem a {-1,0,1}

- Calculo da próxima velocidade [nvx,nvy]:
    - nvx = vx + ax
    - nvy = vy + ay

- Calculo da próxima posição [nx,ny]:
    - nx = x + vx + ax
    - ny = y + vy + ay

- Carro tem a possibilidade de sair da pista, sendo que, se ocorrer, terá de voltar à posição
anterior com velocidade zero.

- Movimento do carro entre posições tem o custo de 1 unidade, subindo para 25 uni. caso saia da pista

### Circuitos

- Ler circuito de um ficheiro de texto
    - 'X' -> fora da pista
    - 'P' -> posição inicial
    - 'F' -> posições finais
    - '-' -> pista

- Custo de viagem entre nodos:
  - Any -> '-'/'P'/'F' = 1
  - Any -> 'X' = 25

## Primeira Fase

- No mínimo 1 circuito com 1 participante a encontrar o caminho mais curto com um dos algoritmos
de pesquisa informada ou não informada.

- Formulação do problema como um problema de pesquisa, indicando a representação do estado inicial,
estado/teste objetivo, os operadores (nome, pré-condições, efeitos) e custo da solução.

- Representar a pista em forma de grafo

### Implementação

- Ler circuito de um ficheiro e guardar os seus dados de alguma forma.
- Gerar todos os nodos possiveis através da posição inicial e inseri-los no grafo
- Iniciar pesquisa
- ???
- Apresentação do circuito, do caminho escolhido e talvez informação da velocidade

## Segunda Fase

- Implementação de vários algoritmos de pesquisa informada e não informada.
- Pesquisa competitiva
- Pelo menos 2 participantes

## Relatório
### Descrição do problema

### Formulação do problema?

### Descrição de tarefas e Decisões tomadas

### Sumário e discussão dos resultados obtidos
