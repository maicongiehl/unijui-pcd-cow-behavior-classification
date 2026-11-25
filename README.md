# Classificação de comportamento de vacas leiteiras com acelerômetro

Trabalho de Ciência de Dados da UNIJUÍ (PCD). A ideia é descobrir o que uma vaca está fazendo olhando só para os dados de um acelerômetro preso no colar dela.

## Problema

Dado um trecho de 10 segundos de aceleração, o modelo diz se a vaca está deitada, em pé/andando ou se alimentando. Isso ajuda a acompanhar a saúde e o bem-estar do rebanho sem precisar de alguém observando o tempo todo.

As classes originais do conjunto de dados foram agrupadas em 3:
- Deitada: 51,1% das janelas
- Em pé/andando: 28,4% das janelas
- Alimentação (comer, lamber e beber): 20,5% das janelas

## Dados

Usamos o MmCows (https://huggingface.co/datasets/neis-lab/mmcows), um conjunto com sensores e comportamentos anotados de 10 vacas (T01 a T10). Aproveitamos só o sensor de movimento (immu) e as anotações de comportamento do dia 25/07/2023, o que dá 71.244 janelas de 10 segundos, ou cerca de 198 horas no total.

Os dados brutos são muito grandes (o sensor_data.zip tem uns 18 GB), então não estão no repositório. O que o projeto usa são os CSVs já limpos em dados/clean, um por vaca. As colunas estão descritas em dados/clean/README.md.

## Como foi feito

Na limpeza, juntamos os dados do acelerômetro com as anotações de comportamento, descartamos registros nulos e a classe 0 (sem anotação válida) e agrupamos tudo em janelas de 10 segundos. Para cada janela calculamos média, desvio, mínimo e máximo da aceleração em x, y, z e da magnitude, o que dá 16 atributos. O comportamento da janela é o mais frequente dentro dela. O dataset limpo não tem valores nulos nem janelas duplicadas.

Na análise exploratória vimos que:
- a classe deitada domina, então sempre chutar "deitada" já acerta cerca de 51%
- as proporções de comportamento mudam bastante de uma vaca para outra, o que pede teste em vacas não vistas
- há mais tempo deitada à noite e no começo da tarde
- todas as vacas têm lacunas de anotação nos mesmos horários, provavelmente a saída do curral
- alimentação tem desvio padrão da magnitude (mag_std) maior, por causa do movimento da cabeça
- em pé/andando se mistura com as outras classes, e é a mais difícil de acertar

Na modelagem usamos um Random Forest. Para a avaliação ser honesta, treinamos com 8 vacas (56.995 janelas) e testamos em 2 que o modelo nunca viu, T09 e T10 (14.249 janelas). Uma divisão aleatória das janelas daria um número otimista, porque janelas vizinhas da mesma vaca ficariam no treino e no teste.

Como os comportamentos duram minutos, também testamos usar atributos das janelas vizinhas. Com a janela atual são 16 atributos, e com 2 antes e 2 depois são 48. A versão com os dois lados usa janelas futuras, então só serve para dados já gravados.

Nesse teste mais honesto comparamos:
- chute, sempre prever deitada: 54% de acurácia, F1 macro 0,233
- Random Forest com os 16 atributos: 81%, F1 macro 0,790
- Random Forest com 2 janelas antes e 2 depois: 87%, F1 macro 0,857

Usar as janelas vizinhas foi o que mais ajudou.

## Resultados

O modelo final (Random Forest com 48 atributos) chegou a 87% de acurácia nas vacas T09 e T10. Por classe:
- Deitada: precisão 0,88 e recall 0,95
- Em pé/andando: precisão 0,82 e recall 0,69
- Alimentação: precisão 0,90 e recall 0,91

Em pé/andando é a mais difícil, e 24% dessas janelas são confundidas com deitada.

Limitações: o teste usa só 2 vacas, então o 87% pode mudar com outras. A versão que usa janelas futuras só serve para dados já gravados. Para monitorar em tempo real seria preciso uma versão sem janelas futuras, que não foi avaliada aqui.

## Estrutura

- extract.py: baixaria os dados brutos do Hugging Face, está desativado
- clean.ipynb: limpeza e criação das janelas, gera os CSVs em dados/clean
- inspect.ipynb: análise exploratória
- model.ipynb: modelos e comparação de resultados
- dados/clean: CSVs limpos, um por vaca
- figuras: gráficos usados na análise e nos resultados, numerados de 01 a 08, mais a tabela de comparação dos modelos
- requirements.txt: dependências do projeto

## Como rodar

Crie um ambiente e instale as dependências:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Depois abra inspect.ipynb e model.ipynb no Jupyter e rode as células em ordem. O model.ipynb leva alguns minutos. Só é preciso rodar o clean.ipynb se quiser refazer a limpeza a partir dos dados brutos, que precisam ser baixados à parte.

## Ferramentas

Python, pandas, numpy, matplotlib, seaborn e scikit-learn (RandomForestClassifier).

## Fonte dos dados

MmCows: A Multimodal Dataset for Dairy Cattle Monitoring (neis-lab/mmcows).
