# Análise de Crédito

Dashboard interativo para análise de crédito com regressão linear (predição de score) e clusterização não supervisionada (DBSCAN / HDBSCAN) com redução PCA.

## Funcionalidades

- **Previsão de score de crédito** via regressão linear
- **Clusterização** com DBSCAN e HDBSCAN + visualização PCA 2D
- **Treinamento interativo** com ajuste de hiperparâmetros (`fit_intercept`, `positive`, `n_jobs`)
- **Divisão do dataset** em treino/teste
- **Gráfico de evolução** das métricas ao longo dos treinos
- **Métricas de regressão**: MAE, MSE, RMSE, R²

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12+, FastAPI, scikit-learn, pandas, joblib |
| Frontend | HTML5, CSS3, JavaScript (ES Modules), Chart.js |
| Gerenciamento | Poetry |
| Linter | Ruff |
| Teste | pytest + pytest-cov |

## Estrutura

```
.
├── pyproject.toml          # Dependências e configuração
├── backend/
│   └── app/
│       ├── app.py          # FastAPI: lifespan, CORS, setup
│       ├── router_modelos.py  # Rotas e lógica de ML
│       ├── schemas.py      # Modelos Pydantic
│       ├── database.py     # Leitura CSV (não utilizado)
│       ├── arquivos/       # CSVs: funcionarios_inteiros, df_train, df_test
│       └── modelos/        # modelo_regressao.pkl
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   └── js/
│       ├── main.js         # Entry point
│       ├── api.js          # Wrapper fetch da API
│       ├── graficos.js     # Gráficos DBSCAN / HDBSCAN
│       ├── regressao.js    # Split, treino, predição
│       └── historicoTreinos.js  # Evolução das métricas
└── tests/
```

## Instalação

```bash
# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

## Execução

### Backend (porta 8000)

```bash
cd backend
python -m uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

### Frontend (porta 5500)

```bash
cd frontend
python -m http.server 5500
```

Acesse `http://127.0.0.1:5500` no navegador.

## API

### `GET /json-bruto`
Retorna o dataset completo como lista de registros.

### `POST /predicao`
Prevê o `credit_score` de um funcionário.
```json
{
  "idade": 35,
  "salario": 5000,
  "anos_de_estudo": 12,
  "anos_de_trabalho": 10
}
// → {"score": 509.58}
```

### `GET /metricas`
Retorna MAE, MSE, RMSE, R² do modelo atual sobre o conjunto de teste.

### `POST /criar-modelo-com-hiperparametros`
Treina novo `LinearRegression` com hiperparâmetros.
```json
{ "fit_intercept": true, "positive": false, "n_jobs": -1 }
```

### `POST /split-dataset`
Divide o dataset em treino e teste.
```json
{ "test_size_percentage": 0.2 }
```

### `GET /dbscan`
Cluster DBSCAN + projeção PCA 2D.

### `GET /hdbscan`
Cluster HDBSCAN + projeção PCA 2D.

## Comandos de Desenvolvimento

```bash
task lint        # Ruff check
task format      # Ruff format
task test        # pytest com cobertura
task run         # fastapi dev
```

## Fluxo do Dashboard

1. Gráficos DBSCAN e HDBSCAN carregam automaticamente
2. Ajuste a porcentagem de teste e clique em "Dividir Dataset"
3. Configure hiperparâmetros e clique em "Criar Modelo"
4. As métricas são exibidas e o painel de predição é habilitado
5. O gráfico de evolução acumula resultados de cada treino
6. Preencha os dados e clique em "Realizar Predição"

## Observações

- O servidor deve ser iniciado de `backend/` (não de `backend/app/`) para resolução correta dos caminhos
- O frontend em `api.js` aponta para `http://127.0.0.1:8000` por padrão — altere para URL remota se necessário

## Autores

- Eduardo Silva Farias (<96924789+EduSF00@users.noreply.github.com>)
