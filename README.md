<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.139-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/scikit--learn-1.9-F7931E?logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chart.js&logoColor=white" alt="Chart.js">
  <img src="https://img.shields.io/badge/Poetry-3.12-60A5FA?logo=poetry&logoColor=white" alt="Poetry">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
</p>

<h1 align="center">📊 Análise de Crédito</h1>

<p align="center">
  Dashboard interativo para análise de crédito com <strong>regressão linear</strong> e
  <strong>clusterização não supervisionada</strong> (DBSCAN / HDBSCAN).
</p>

<p align="center">
  <a href="#-sobre">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-stack">Stack</a> •
  <a href="#-começando">Começando</a> •
  <a href="#-comandos">Comandos</a> •
  <a href="#-estrutura">Estrutura</a> •
  <a href="#-documentação">Documentação</a>
</p>

---

## 📌 Sobre

Aplicação de **Análise de Crédito** que combina **regressão linear** para previsão de score de crédito com **clusterização não supervisionada** (DBSCAN e HDBSCAN) para segmentação de perfis financeiros. O backend expõe uma API REST em FastAPI e o frontend consome os endpoints exibindo gráficos interativos com Chart.js.

---

## ✨ Funcionalidades

- **Previsão de score** — regressão linear com `scikit-learn`
- **Clusterização** — DBSCAN e HDBSCAN com redução PCA para visualização 2D
- **Dashboard interativo** — gráficos de dispersão, cards de métricas e painel de predição
- **Treinamento dinâmico** — ajuste de hiperparâmetros (`fit_intercept`, `positive`, `n_jobs`)
- **Evolução de métricas** — gráfico de linhas acumulando resultados de cada treino
- **Divisão treino/teste** — controle da proporção via interface

---

## 🛠 Stack

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.12+, FastAPI, scikit-learn 1.9, pandas 3.0, joblib |
| **Frontend** | HTML5, CSS3, JavaScript ES Modules, Chart.js 4 |
| **Gerenciamento** | Poetry |
| **Linter** | Ruff |
| **Testes** | pytest + pytest-cov |

---

## 🚀 Começando

### Pré-requisitos

- Python **>=3.12**
- [Poetry](https://python-poetry.org/)

### Instalação

```bash
git clone <repo-url>
cd trabalho_minera-o_de_dados_07
poetry install
```

### Execução

**Backend** (terminal 1):
```bash
cd backend
python -m uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

**Frontend** (terminal 2):
```bash
cd frontend
python -m http.server 5500
```

Acesse **http://127.0.0.1:5500** no navegador.

---

## 📋 Comandos

```bash
task lint        # Ruff check
task format      # Ruff format
task test        # pytest com cobertura
task run         # fastapi dev
```

---

## 📁 Estrutura

```
.
├── pyproject.toml          # Dependências e configuração
├── backend/
│   └── app/
│       ├── app.py          # FastAPI: lifespan, CORS, setup
│       ├── router_modelos.py  # 7 endpoints + lógica de ML
│       ├── schemas.py      # 6 modelos Pydantic
│       ├── database.py     # Leitura CSV (não utilizado)
│       ├── arquivos/       # funcionarios_inteiros.csv, df_train.csv, df_test.csv
│       └── modelos/        # modelo_regressao.pkl
├── frontend/
│   ├── index.html          # Dashboard SPA
│   ├── css/
│   │   ├── style.css       # 319 linhas de estilo
│   │   └── dashboard.css   # 50 linhas (gráficos)
│   └── js/
│       ├── main.js         # Entry point
│       ├── api.js          # 5 funções de API
│       ├── graficos.js     # Gráficos DBSCAN / HDBSCAN
│       ├── regressao.js    # Split, treino, predição
│       └── historicoTreinos.js  # Evolução das métricas
├── docs/                   # Documentação detalhada
└── tests/
```

---

## 📚 Documentação

A documentação completa e detalhada de cada módulo está disponível na pasta [`docs/`](docs/):

| Documento | Conteúdo |
|-----------|----------|
| [index.md](docs/index.md) | Visão geral e arquitetura |
| [setup.md](docs/setup.md) | Instalação, execução e configuração |
| [backend.md](docs/backend.md) | Módulos do backend (app, router, schemas, database) |
| [frontend.md](docs/frontend.md) | Módulos do frontend (HTML, CSS, JS) |
| [api.md](docs/api.md) | Referência completa da API REST |
| [data.md](docs/data.md) | Estrutura e descrição do dataset |

---

## 👤 Autor

**Eduardo Silva Farias** — [@EduSF00](https://github.com/EduSF00)
