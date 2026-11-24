# Projeto Aplicado de Ciência de Dados: Classificação Multimodal do Comportamento de Vacas Leiteiras

Este repositório contém o pipeline completo de Ciência de Dados para o monitoramento contínuo e a classificação automatizada do comportamento de vacas leiteiras. A solução utiliza dados de aceleração triaxial coletados por sensores vestíveis (acelerômetros instalados em colares inteligentes) e aplica algoritmos de Machine Learning com engenharia de contexto temporal para reconhecer padrões de atividades dos animais.

O pipeline abrange desde o pré-processamento de sinais brutos e agregação em janelas de 10 segundos até a análise exploratória de dados (EDA), engenharia de atributos temporais e validação cruzada rigorosa por animal (*Group Split* em vacas não vistas durante o treinamento).

---

## 📌 Visão Geral do Projeto

O objetivo central do projeto é prever o comportamento de bovinos leiteiros em janelas de tempo não sobrepostas de 10 segundos, convertendo telemetria bruta de aceleração em informações acionáveis sobre a saúde, bem-estar e rotina dos animais.

### Consolidação das Classes Comportamentais
As 8 classes originais de comportamento anotadas em campo foram mapeadas e agregadas em **3 categorias funcionais principais**:

1. **Deitada** (Classe 7): Representa o estado de repouso e ruminação deitada. Constitui a classe majoritária, englobando **51,1%** do volume total de janelas no dataset consolidado (e 62,59% na vaca T01).
2. **Em pé/andando** (Classes 1 e 2 agrupadas): Representa a postura vertical e deslocamentos ativos. Corresponde a **28,4%** das janelas.
3. **Alimentação** (Classes 4, 5 e 6 agrupadas — comer, lamber e beber): Representa as atividades de ingestão de alimento e água. Responde por **20,5%** das janelas.

---

## 📁 Estrutura do Repositório

```text
├── dados/
│   ├── raw/                        # Dados brutos de sensores e rótulos comportamentais
│   │   ├── sensor_data/main_data/immu/T{vaca}/T{vaca}_{data}.csv
│   │   └── behavior_labels/individual/C{vaca}_0725.csv
│   └── clean/                      # Datasets limpos e agrupados por vaca (T01.csv a T10.csv)
├── figuras/                        # Gráficos, mapas de calor e matrizes de confusão exportados
│   ├── 01_distribuicao_classes.png
│   ├── 02_comportamento_por_vaca.png
│   ├── 03_comportamento_por_hora.png
│   ├── 04_atributos_por_classe.png
│   ├── 05_correlacao_atributos.png
│   ├── 06_linha_do_tempo_vacas.png
│   ├── 07_comparacao_experimentos.png
│   ├── 08_acuracia_por_vaca.png
│   ├── 09_matriz_confusao.png
│   ├── 10_importancia_atributos.png
│   └── tabela_comparacao_modelos.csv
├── extract.py                      # Script de extração e estruturação dos dados brutos
├── clean.ipynb                     # Notebook para limpeza, conversão e extração de atributos estatísticos
├── inspect.ipynb                   # Notebook para auditoria, inspeção e análise exploratória (EDA)
├── model.ipynb                     # Notebook para treinamento, engenharia de contexto e avaliação de modelos
└── requirements.txt                # Lista de dependências e bibliotecas Python do projeto
```

---

## 📊 Dataset e Amostragem

O projeto utiliza o conjunto de dados open-source **MmCows** (`neis-lab/mmcows`). Foram selecionadas 10 vacas leiteiras identificadas pelos códigos **T01 a T10**, monitoradas com acelerômetros triaxiais ao longo do dia 25/07/2023.

| Vaca ID | Janelas Rotuladas (10s) | Tempo Total Processado |
| :--- | :---: | :---: |
| **T01** | 7.139 | ~19,8 horas |
| **T02** | 7.119 | ~19,8 horas |
| **T03** | 7.133 | ~19,8 horas |
| **T04** | 7.136 | ~19,8 horas |
| **T05** | 7.110 | ~19,75 horas |
| **T06** | 7.110 | ~19,75 horas |
| **T07** | 7.130 | ~19,8 horas |
| **T08** | 7.118 | ~19,77 horas |
| **T09** | 7.139 | ~19,8 horas |
| **T10** | 7.110 | ~19,75 horas |
| **Total** | **71.244** | **~197,9 horas** |

---

## ⚙️ Pipeline de Dados e Pré-Processamento (`clean.ipynb` / `extract.py`)

O pipeline de pré-processamento automatizado converte os registros brutos de telemetria nos conjuntos de dados estatísticos estruturados:

1. **Filtragem de Qualidade**: Cruzamento temporal dos arquivos de acelerômetro (`TXX_*.csv`) com os rótulos de comportamento (`CXX_0725.csv`). Descarte de registros nulos e da Classe 0 (*Unknown* / sem anotação válida).
2. **Cálculo da Magnitude Triaxial**: Derivação da magnitude vetorial da aceleração ($\text{acc\_mag}$):
   $$\text{acc\_mag} = \sqrt{\text{accel\_x}^2 + \text{accel\_y}^2 + \text{accel\_z}^2}$$
3. **Janelamento Temporal de 10 Segundos**: Segmentação da série temporal em janelas fixas sem sobreposição baseadas no timestamp (`timestamp // 10`).
4. **Extração de Atributos Estatísticos (16 Features Base)**: Para cada janela, calcula-se média (`mean`), desvio padrão (`std`), mínimo (`min`) e máximo (`max`) para os eixos $X, Y, Z$ e para a magnitude $\text{acc\_mag}$:
   - `x_mean`, `x_std`, `x_min`, `x_max`
   - `y_mean`, `y_std`, `y_min`, `y_max`
   - `z_mean`, `z_std`, `z_min`, `z_max`
   - `mag_mean`, `mag_std`, `mag_min`, `mag_max`
5. **Rotulação por Moda**: O comportamento atribuído à janela corresponde à classe mais frequente no intervalo.

---

## 🔍 Inspeção e Análise Exploratória (`inspect.ipynb`)

A auditoria confirmou que o dataset limpo de 71.244 janelas não possui valores nulos (0 nulos) nem janelas duplicadas (0 duplicatas).

### Principais Diagnósticos Exploratórios
- **Distribuição das Classes**: A classe *Deitada* (51,1%) domina a amostra. Um modeloIngênuo que previr apenas "Deitada" atinge 51,1% de acurácia baseline no dataset completo e 53,6% no conjunto de teste (T09/T10).
- **Variabilidade Inter-Animal**: As proporções comportamentais variam entre indivíduos (a vaca T06 passa menos tempo deitada do que a T07, por exemplo), justificando a necessidade de validação em animais não vistos.
- **Padrão Circadiano (CDT = UTC-5)**: Observou-se maior tempo de repouso no período noturno e início da tarde. Foram identificadas duas lacunas simultâneas de anotação em todas as vacas (04h30-05h00 e 15h30-16h15), correspondentes ao período provável de ordenha.
- **Separabilidade dos Atributos**:
  - *Alimentação* apresenta maior desvio padrão da magnitude (`mag_std`), refletindo a movimentação da cabeça.
  - *Deitada* exibe a média do eixo $Z$ (`z_mean`) menos negativa e mais dispersa.
  - *Em pé/andando* apresenta sobreposição com as demais classes, sendo a categoria com maior taxa de erro nos modelos.
  - Existe forte correlação interna entre atributos do mesmo eixo ($0,5$ a $0,9$), como entre `y_mean` e `y_max` ($0,9$).

---

## 🧪 Modelagem Preditiva e Experimentos (`model.ipynb`)

### Problema da Divisão Aleatória (*Data Leakage*)
A divisão aleatória tradicional (70/30) resulta em uma acurácia de **86,05%** com Random Forest. No entanto, este valor é otimista devido ao vazamento temporal de janelas consecutivas do mesmo animal presentes simultaneamente em treino e teste.

### Validação Cruzada por Animal (*Group Split*)
Para avaliar a generalização em animais não vistos, aplicou-se a separação por grupos:
- **Treinamento**: 56.995 janelas de **8 vacas** (T01 a T08).
- **Teste Cego**: 14.249 janelas de **2 vacas** (T09 e T10).

### Engenharia de Contexto Temporal (Janelas Vizinhas)
Aproveitando a continuidade biológica dos comportamentos, foram construídas variáveis de contexto temporal:
- **16 Atributos (Original)**: Apenas a janela atual ($t$).
- **32 Atributos (Contexto Passado)**: Janela atual ($t$) + janelas $t-1$ e $t-2$ (10s e 20s anteriores). *Adequado para monitoramento em tempo real*.
- **48 Atributos (Contexto Bidirecional)**: Janela atual ($t$) + janelas $t-1, t-2$ (passado) + janelas $t+1, t+2$ (futuro). *Adequado para processamento em lote pré-gravado*.

---

## 📈 Resultados e Comparativo de Desempenho

| Experimento / Algoritmo | Atributos | Acurácia (Teste T09/T10) | F1-Score Macro | Cenário de Aplicação |
| :--- | :---: | :---: | :---: | :--- |
| **Chute Frequencial (Sempre Deitada)** | 0 | 53,6% | 0,233 | Referência trivial |
| **Random Forest Original** | 16 | 81,4% | 0,790 | Modelo base sem contexto |
| **Random Forest + Contexto Passado** | 32 | **85,3%** | **0,838** | **Tempo Real (Streaming)** |
| **Random Forest + Contexto Bidirecional** | 48 | **87,0%** | **0,857** | **Processamento em Lote (Batch)** |
| **HistGradientBoosting + Contexto** | 48 | 87,1% | 0,858 | Elevado custo computacional |
| **GradientBoosting (GBM) + Contexto** | 48 | 87,1% | 0,857 | Treinamento muito lento (~4 min) |

### Desempenho do Modelo Final (Random Forest com 48 Atributos)

No conjunto de teste cego das vacas T09 e T10, o modelo final obteve acurácia individual de **84% na T09** e **90% na T10**.

#### Relatório de Classificação Detalhado:
```text
               precision    recall  f1-score   support

      Deitada      0.880     0.948     0.913      7636
Em pé/andando      0.820     0.694     0.752      4043
  Alimentação      0.902     0.913     0.907      2570

     accuracy                          0.870     14249
    macro avg      0.867     0.852     0.857     14249
 weighted avg      0.867     0.870     0.866     14249
```

> **Nota de Validação Cruzada Completa**: Na avaliação com 5 folds cruzados (testando todos os 5 pares de vacas possíveis), a acurácia média do Random Forest com contexto bidirecional foi de **84,0%** (variando entre 78,5% no par T05/T06 e 88,5% no par T03/T04). O resultado do par T09/T10 (87,0%) encontra-se acima da média global.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- **Python**: Versão 3.9 ou superior.

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o Pipeline de Dados
Para realizar o pré-processamento dos dados brutos e gerar os arquivos limpos em `dados/clean/`:
```bash
python extract.py
```

### 4. Executar a Análise e Modelagem
Abra e execute os notebooks Jupyter na ordem indicada:
1. `clean.ipynb`: Limpeza e extração das 16 estatísticas base.
2. `inspect.ipynb`: Auditoria de dados, análise exploratória (EDA) e exportação de figuras.
3. `model.ipynb`: Engenharia de atributos temporais, experimentos com modelos e relatórios de avaliação.

---

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.9+
- **Processamento de Dados**: `pandas`, `numpy`
- **Visualização**: `matplotlib`, `seaborn`
- **Machine Learning**: `scikit-learn` (`RandomForestClassifier`, `HistGradientBoostingClassifier`, `GradientBoostingClassifier`, `train_test_split`, `metrics`)
- **Manipulação do Sistema de Arquivos**: `pathlib`, `glob`, `os`

---

## 📜 Licença e Fonte dos Dados

O dataset empregado é proveniente do projeto **MmCows: A Multimodal Dataset for Dairy Cattle Monitoring** (`neis-lab/mmcows`).
