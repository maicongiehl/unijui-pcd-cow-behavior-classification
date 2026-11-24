# Projeto Aplicado de Ciência de Dados: Classificação de Comportamento Animal

Este repositório contém o pipeline completo de Ciência de Dados para o monitoramento e classificação automatizada do comportamento de vacas leiteiras a partir de dados de aceleração triaxial coletados por sensores vestíveis (acelerômetros em colares).

---

## 📌 Visão Geral do Projeto

O objetivo do projeto é prever o comportamento de bovinos em janelas de tempo de 10 segundos, convertendo sinais brutos de aceleração em insights acionáveis sobre o bem-estar e a rotina dos animais.

As 8 classes originais de comportamento foram mapeadas e agrupadas em **3 classes principais**:
1. **Deitada** (Classe 7): Representa cerca de 51,1% das janelas.
2. **Em pé/andando** (Classes 1 e 2 agrupadas): Representa cerca de 28,4% das janelas.
3. **Alimentação** (Classes 4, 5 e 6 agrupadas — comer, lamber e beber): Representa cerca de 20,5% das janelas.

---

## 📁 Estrutura do Repositório

```text
├── dados/
│   ├── raw/                        # Dados brutos de sensores e rótulos
│   │   ├── sensor_data/main_data/immu/T{vaca}/T{vaca}_{data}.csv
│   │   └── behavior_labels/individual/C{vaca}_{data}.csv
│   └── clean/                      # Datasets limpos e agregados por vaca (T01.csv a T10.csv)
├── figuras/                        # Gráficos e visualizações geradas pelos notebooks
├── extract.py                      # Script de extração e estruturação dos dados brutos
├── clean.ipynb                     # Notebook para limpeza, conversão e extração de atributos estatísticos
├── inspect.ipynb                   # Notebook para auditoria, inspeção e análise exploratória (EDA)
├── model.ipynb                     # Notebook para treinamento, engenharia de contexto e avaliação de modelos
└── requirements.txt                # Lista de dependências e bibliotecas Python do projeto
```

---

## ⚙️ Pipeline de Dados

### 1. Extração e Limpeza (`extract.py` & `clean.ipynb`)
- **Filtragem**: Leitura dos sensores das vacas selecionadas (T01 a T10) e cruzamento com os rótulos de comportamento anotados (`CXX_0725.csv`). Remoção de registros sem anotação válida (classe 0) e valores nulos.
- **Cálculo de Magnitude**: Derivação da magnitude vetorial da aceleração:
  $$\text{acc\_mag} = \sqrt{\text{accel\_x}^2 + \text{accel\_y}^2 + \text{accel\_z}^2}$$
- **Janelamento Temporal**: Agrupamento dos sinais em janelas de 10 segundos. O rótulo da janela é definido pela moda (comportamento mais frequente).
- **Extração de Atributos (16 features)**: Para cada janela, calcula-se média (`mean`), desvio padrão (`std`), mínimo (`min`) e máximo (`max`) dos eixos $X, Y, Z$ e da magnitude `acc_mag`.
- **Saída**: Criação de arquivos `.csv` limpos na pasta `dados/clean/` (contendo 71.244 janelas de 10s no total).

### 2. Inspeção e Análise Exploratória (`inspect.ipynb`)
- Auditagem da qualidade dos dados (0 nulos e 0 duplicatas).
- Análise da variação do comportamento por vaca e ao longo das horas do dia.
- Análise da separabilidade dos atributos (boxplots) e redundância entre atributos do acelerômetro (matriz de correlação em heatmap).
- Geração e salvamento automático das figuras demonstrativas no diretório `figuras/`.

### 3. Modelagem e Validação (`model.ipynb`)
- **Baseline (Splitting Aleatório 70/30)**: Random Forest atinge acurácia otimista de **86,05%**, porém sujeita a vazamento temporal/animal.
- **Engenharia de Recursos de Contexto**: Criação de atributos de janelas vizinhas temporais ($t-1, t-2$ e $t+1, t+2$), expandindo os atributos de 16 para 32 (apenas passado) ou 48 (dois lados).
- **Validação Cruzada por Animal (Group Split)**: Treinamento com 8 vacas e teste cego em 2 vacas não vistas durante o treino (T09 e T10), simulando a aplicação do modelo em animais novos.
- **Comparação de Algoritmos**:
  - *Chute Frequencial*: 53,6% de acurácia.
  - *Random Forest Original (16 features)*: 81,4% de acurácia.
  - *Random Forest + Contexto Passado (32 features)*: 85,3% de acurácia (viável para execução em tempo real).
  - *Random Forest + Contexto Ambos Lados (48 features)*: 87,0% de acurácia.
  - *HistGradientBoosting*: 87,1% de acurácia.
  - *GradientBoosting (GBM)*: 87,1% de acurácia.
- **Modelo Selecionado**: **Random Forest** com atributos de contexto, por alinhar alta acurácia (87%), robustez e velocidade de treinamento.

---

## 🚀 Como Executar o Projeto

### Pre-requisitos
Certifique-se de ter o Python 3.9+ instalado em seu ambiente.

### Passos para Execução

1. **Clonar o Repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar a Limpeza e Pré-processamento**:
   Execute o script de extração/limpeza para gerar as bases em `dados/clean/`:
   ```bash
   python extract.py
   ```
   *(ou rode as células do notebook `clean.ipynb`)*.

4. **Executar a Análise Exploratória e Treinamento**:
   Abra e execute os notebooks na sequência recomendada:
   - `inspect.ipynb`: Para validar o dataset e gerar as visualizações.
   - `model.ipynb`: Para treinar os algoritmos e avaliar a matriz de confusão e métricas F1-score.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Processamento de Dados**: `pandas`, `numpy`
- **Visualização**: `matplotlib`, `seaborn`
- **Machine Learning**: `scikit-learn` (`RandomForestClassifier`, `HistGradientBoostingClassifier`, `GradientBoostingClassifier`, `train_test_split`, `metrics`)
- **Utilitários**: `pathlib`, `glob`, `os`
