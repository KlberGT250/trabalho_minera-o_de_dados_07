# Visão Geral

**Análise de Crédito** é uma aplicação web full-stack para análise de perfis financeiros. O projeto combina duas tarefas principais de machine learning:

1. **Regressão Linear** — predizer o `credit_score` de um funcionário com base em características como idade, salário, anos de estudo e anos de trabalho.
2. **Clusterização não supervisionada** — segmentar automaticamente os perfis usando DBSCAN e HDBSCAN, com projeção PCA 2D para visualização.

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│  HTML + CSS + JS (ES Modules) + Chart.js                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ main.js  │ │ api.js   │ │graficos.js│ │ regressao │ │
│  │ (entrada)│ │ (fetch)  │ │(DB/HDBSC)│ │ .js (ML)  │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (fetch)
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      Backend                            │
│  FastAPI + scikit-learn + pandas + joblib               │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐            │
│  │ app.py   │ │router_modelos│ │ schemas  │            │
│  │ (server) │ │ .py (rotas)  │ │ .py      │            │
│  └──────────┘ └──────────────┘ └──────────┘            │
└─────────────────────────────────────────────────────────┘
```

### Fluxo de dados

1. O frontend carrega e faz requisições `fetch()` para a API FastAPI
2. O backend lê CSVs da pasta `arquivos/`, processa com scikit-learn e retorna JSON
3. O modelo treinado é persistido em `modelos/modelo_regressao.pkl` via joblib
4. O frontend renderiza gráficos Chart.js com os dados recebidos

## Decisões técnicas

| Decisão | Justificativa |
|---------|---------------|
| **FastAPI** | Alto desempenho, validação automática com Pydantic, documentação OpenAPI interativa |
| **scikit-learn** | Biblioteca consolidada para ML com pipeline simples de treino/predição |
| **Chart.js** | Leve, sem dependências, excelente para gráficos de dispersão e linha |
| **Poetry** | Gerenciamento reprodutível de dependências Python |
| **joblib** | Serialização eficiente de modelos scikit-learn |
| **ES Modules** | Organização do frontend em módulos sem bundler |

## Fluxo do Dashboard

```
Abrir página
    │
    ├──→ GET /dbscan   → renderiza scatter plot DBSCAN
    ├──→ GET /hdbscan  → renderiza scatter plot HDBSCAN
    └──→ Registra eventos de clique
              │
              ├── "Dividir Dataset" → POST /split-dataset
              ├── "Criar Modelo"    → POST /criar-modelo-com-hiperparametros
              │                       → GET /metricas
              │                       → atualiza cards + gráfico de evolução
              └── "Realizar Predição" → POST /predicao
                                         → exibe score
```
