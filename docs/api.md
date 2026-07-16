# Referência da API

A API REST é servida em **http://127.0.0.1:8000** e possui 7 endpoints. A documentação interativa OpenAPI está disponível em `/docs` (Swagger UI).

---

## `GET /json-bruto`

Retorna o dataset completo (`funcionarios_inteiros.csv`) como uma lista de objetos.

**Resposta (200):**
```json
{
  "dados": [
    { "age": 25, "income": 3000, "education_years": 12, "experience": 3, "credit_score": 450 },
    { "age": 32, "income": 5000, "education_years": 16, "experience": 8, "credit_score": 620 }
  ]
}
```

---

## `POST /predicao`

Prevê o `credit_score` com base nos dados do funcionário.

**Body:**
```json
{
  "idade": 35,
  "salario": 5000,
  "anos_de_estudo": 12,
  "anos_de_trabalho": 10
}
```

**Validação dos campos:**

| Campo | Tipo | Restrições |
|-------|------|------------|
| `idade` | int | 0 a 120 |
| `salario` | int | ≥ 0 |
| `anos_de_estudo` | int | 0 a 30 |
| `anos_de_trabalho` | int | 0 a 50 |

**Resposta (200):**
```json
{
  "score": 509.58
}
```

**Erros:**
- `503` — Modelo não carregado (treine um modelo primeiro)
- `422` — Dados inválidos (fora das restrições)

---

## `GET /metricas`

Calcula métricas de desempenho do modelo atual sobre `df_test.csv`.

**Resposta (200):**
```json
{
  "mae": 103.21,
  "mse": 16830.66,
  "rmse": 129.73,
  "r2": -0.688
}
```

| Métrica | Descrição |
|---------|-----------|
| **MAE** | Mean Absolute Error — erro médio absoluto |
| **MSE** | Mean Squared Error — erro quadrático médio |
| **RMSE** | Root Mean Squared Error — raiz do erro quadrático médio |
| **R²** | Coeficiente de determinação — qualidade do ajuste |

**Erros:**
- `503` — Modelo não carregado
- `404` — Arquivo `df_test.csv` não encontrado

---

## `POST /criar-modelo-com-hiperparametros`

Treina um novo modelo **LinearRegression** com os hiperparâmetros fornecidos. O modelo é salvo em disco e recarregado no estado da aplicação.

**Body:**
```json
{
  "fit_intercept": true,
  "positive": false,
  "n_jobs": -1
}
```

**Campos (todos opcionais — valores padrão):**

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `fit_intercept` | bool | `true` | Se deve calcular o intercepto |
| `positive` | bool | `true` | Força coeficientes não negativos |
| `n_jobs` | int | `-1` | Número de jobs (-1 = todos os CPUs) |

**Resposta (200):**
```json
{
  "objetivo": "Treinar modelo com hiperparametros",
  "mensagem": "Modelo retreinado com sucesso!"
}
```

**Erros:**
- `404` — Arquivo `df_train.csv` não encontrado

---

## `POST /split-dataset`

Divide o dataset completo em treino e teste, sobrescrevendo `df_train.csv` e `df_test.csv`.

**Body:**
```json
{
  "test_size_percentage": 0.2
}
```

| Campo | Tipo | Padrão | Restrições |
|-------|------|--------|------------|
| `test_size_percentage` | float | `0.2` | 0.0 a 1.0 |

**Resposta (200):**
```json
{
  "objetivo": "Separar dataset com 20% para teste",
  "mensagem": "Dados divididos com sucesso!"
}
```

**Erros:**
- `404` — Arquivo `funcionarios_inteiros.csv` não encontrado

---

## `GET /dbscan`

Executa **DBSCAN** sobre `df_train.csv` e retorna:
- `scan`: dicionário com as colunas originais + cluster atribuído
- `pca`: coordenadas 2D da redução PCA

**Parâmetros do algoritmo:** `eps=0.7`, `min_samples=5`

**Resposta (200):**
```json
{
  "scan": {
    "age": [25, 32, 28, ...],
    "income": [3000, 5000, 4200, ...],
    "education_years": [12, 16, 14, ...],
    "experience": [3, 8, 5, ...],
    "cluster": [-1, 0, 0, ...]
  },
  "pca": [[2.34, -1.02], [0.87, 0.45], ...]
}
```

**Notas:**
- Cluster `-1` = ruído (pontos não classificados)
- Cluster `0, 1, 2...` = grupos identificados

---

## `GET /hdbscan`

Executa **HDBSCAN** sobre `df_train.csv` com o mesmo formato de retorno do DBSCAN.

**Parâmetros do algoritmo:** `min_cluster_size=15`, `min_samples=5`

**Resposta (200):** Mesmo formato do `GET /dbscan`.
