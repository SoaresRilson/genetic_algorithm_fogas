# Fogás VRP - Algoritmo Genético

## Descrição do Problema

O desafio consiste em resolver um **Vehicle Routing Problem (VRP)** para a empresa Fogás, que distribui botijões de gás. O objetivo é otimizar as rotas de entrega para 30 clientes a partir de um depósito central, utilizando 5 veículos, cada um com capacidade de 100 botijões. Cada cliente possui uma demanda específica (total de 350 botijões), e as rotas devem minimizar a distância total percorrida, respeitando a capacidade dos veículos. O problema considera:
- **Depósito**: Localizado em (400, 100).
- **Clientes**: 30 pontos com coordenadas (x, y) e demandas entre 5 e 20 botijões.
- **Restrições**: Todos os clientes devem ser atendidos, e a soma das demandas por veículo não pode exceder 100 botijões.
- **Objetivo**: Encontrar rotas que minimizem a distância total percorrida, com visualização interativa das rotas e da convergência do algoritmo.

## Solução Implementada

A solução utiliza um **algoritmo genético** para otimizar as rotas, implementado em Python com as bibliotecas Pygame e NumPy. As principais características são:

- **Algoritmo Genético**:
  - **População**: Inicializada com 60 indivíduos (máximo entre 50 e 2 vezes o número de clientes), cada um representando uma configuração de rotas para 5 veículos.
  - **Aptidão**: Calculada como a distância total percorrida, usando uma **matriz de distâncias** pré-calculada para maior eficiência, em vez de cálculos repetidos da distância euclidiana.
  - **Seleção**: Seleção dos melhores indivíduos com base na aptidão.
  - **Cruzamento**: Combina rotas de dois pais, garantindo que a capacidade dos veículos não seja excedida.
  - **Mutação**: Aplica trocas ou realocações de clientes entre rotas com taxa de 5%.
  - **Gerações**: 2000 iterações para explorar soluções e alcançar convergência.

- **Otimização com Matriz de Distâncias**:
  - Uma matriz 31x31 (depósito + 30 clientes) armazena as distâncias euclidianas calculadas uma única vez no início.
  - Reduz o custo computacional da função de aptidão, essencial para 2000 gerações.

- **Visualização**:
  - **Gráfico de Convergência**: Um gráfico quadrado (300x300 pixels) à esquerda da tela exibe a evolução da melhor aptidão (distância total) ao longo das 2000 gerações, com linha verde, fundo branco, bordas pretas e rótulos em Arial para os eixos (gerações e aptidão).
  - **Rotas**: Desenhadas à direita, com o depósito (círculo vermelho), clientes (círculos azuis) e rotas em cores distintas para cada veículo.
  - Inspirado no estilo visual do exemplo `genetic_algorithm_camouflage`.

- **Saída**: O console exibe a melhor aptidão e solução a cada geração, com a solução final detalhada ao término.

## Requisitos para Execução

Para executar o programa, você precisa de:

- **Python**: Versão 3.6 ou superior.
- **Bibliotecas**:
  - `pygame`: Para visualização gráfica (gráfico e rotas).
  - `numpy`: Para cálculos eficientes com a matriz de distâncias.
- **Instalação**:
  ```bash
  pip install pygame numpy
  ```
- **Sistema Operacional**: Windows, macOS ou Linux (qualquer sistema compatível com Python e Pygame).

## Como Executar

1. **Clone o Repositório** (se aplicável) ou salve os arquivos:
   - `vrp_fogas.py`: Contém o programa principal, incluindo inicialização, visualização e chamada do algoritmo.
   - `genetic_algorithm.py`: Implementa as funções do algoritmo genético (inicialização, aptidão, seleção, cruzamento, mutação).
2. **Certifique-se de que os arquivos estejam no mesmo diretório**.
3. **Execute o programa**:
   ```bash
   python vrp_fogas.py
   ```
4. **Interação**:
   - A janela Pygame mostrará o gráfico de convergência à esquerda e as rotas à direita.
   - Pressione `q` ou feche a janela para encerrar.
5. **Saída**:
   - O console exibe a aptidão a cada geração e a melhor solução final.
   - Exemplo: `Geração 2000: Melhor aptidão = 1234.56`, seguido da configuração das rotas.

## Observações

- **Configuração**: 30 clientes (demanda total = 350 botijões), 5 veículos (capacidade = 100 cada), 2000 gerações.
- **Eficiência**: A matriz de distâncias reduz o tempo de execução, tornando o algoritmo escalável para problemas maiores.
- **Visualização**: O gráfico quadrado à esquerda ajuda a analisar a convergência, enquanto as rotas à direita mostram a solução visualmente.
- **Melhorias Futuras**: Adicionar pausa entre gerações, salvar a matriz de distâncias em um arquivo ou incluir rótulos adicionais no gráfico.