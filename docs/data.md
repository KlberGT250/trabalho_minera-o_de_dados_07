# Dataset

## Fonte

O dataset `funcionarios_inteiros.csv` contém dados sintéticos de funcionários para análise de crédito. São **1000 registros** com 5 colunas.

## Estrutura

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `age` | int | Idade do funcionário |
| `income` | int | Salário |
| `education_years` | int | Anos de estudo formal |
| `experience` | int | Anos de trabalho |
| `credit_score` | int | **Target** — score de crédito |

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `arquivos/funcionarios_inteiros.csv` | Dataset completo (1000 registros) |
| `arquivos/df_train.csv` | Conjunto de treino (gerado via `/split-dataset`) |
| `arquivos/df_test.csv` | Conjunto de teste (gerado via `/split-dataset`) |

## Pipeline de dados

```
funcionarios_inteiros.csv
        │
        ▼
  POST /split-dataset
        │
        ├──→ df_train.csv  (ex: 80%)
        └──→ df_test.csv   (ex: 20%)
                │
                ├──→ POST /criar-modelo-com-hiperparametros (treino)
                └──→ GET /metricas (avaliação)
```

### Uso nos endpoints

- **`/json-bruto`** — retorna `funcionarios_inteiros.csv` completo
- **`/split-dataset`** — lê `funcionarios_inteiros.csv`, divide e salva `df_train.csv` / `df_test.csv`
- **`/metricas`** — avalia o modelo sobre `df_test.csv`
- **`/criar-modelo-com-hiperparametros`** — treina sobre `df_train.csv`
- **`/dbscan`** e **`/hdbscan`** — clusterizam sobre `df_train.csv`
- **`/predicao`** — usa o modelo carregado em memória (treinado sobre `df_train.csv`)

## Observação

A divisão treino/teste **não é persistida automaticamente**. Toda vez que o endpoint `/split-dataset` é chamado, novos arquivos são sobrescritos. É recomendável dividir o dataset uma vez antes de iniciar os treinos.
