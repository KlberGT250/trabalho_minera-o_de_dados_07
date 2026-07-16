# Instruções da Aplicação — Análise de Crédito

## Visão Geral

Este projeto é uma aplicação de **análise de crédito** com backend em **FastAPI** (Python) e frontend **HTML/CSS/JavaScript** (Chart.js).  
O backend expõe uma API REST com os seguintes recursos:

- Previsão de `credit_score` via regressão linear
- Cálculo de métricas de regressão (MAE, MSE, RMSE, R²)
- Treinamento de modelo linear com hiperparâmetros (`fit_intercept`, `positive`, `n_jobs`)
- Divisão do dataset em treino/teste
- Clusterização com **DBSCAN** e **HDBSCAN**
- Retorno dos dados brutos em JSON

O frontend consome esses endpoints e exibe gráficos de dispersão (PCA), painéis interativos de treinamento/predição **e um gráfico de evolução das métricas ao longo dos treinos**.

---

## Estrutura do Projeto

```
.
├── pyproject.toml              # Dependências e configuração do Poetry
├── README.md                   # README original do repositório
├── INSTRUCOES.md               # Este arquivo
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── app.py              # Inicialização do FastAPI, CORS e carregamento do modelo
│   │   ├── router_modelos.py   # Rotas da API e lógica de machine learning
│   │   ├── schemas.py          # Modelos Pydantic para validação de dados
│   │   ├── database.py         # Função de leitura de CSV (não utilizada pelo frontend)
│   │   ├── arquivos/
│   │   │   ├── funcionarios_inteiros.csv   # Dataset completo
│   │   │   ├── df_train.csv                # Dataset de treino
│   │   │   └── df_test.csv                 # Dataset de teste
│   │   └── modelos/
│   │       └── modelo_regressao.pkl        # Modelo treinado (joblib)
│   └── ...
├── frontend/
│   ├── index.html              # Interface do dashboard
│   ├── css/
│   │   ├── style.css           # Estilos principais
│   │   └── dashboard.css       # Estilos específicos dos gráficos
│   └── js/
│       ├── main.js             # Ponto de entrada — carrega gráficos e regressão
│       ├── api.js              # Funções para chamar os endpoints da API
│       ├── graficos.js         # Lógica de criação dos gráficos DBSCAN e HDBSCAN
│       ├── regressao.js        # Lógica de interação: split, treino, predição
│       └── historicoTreinos.js # Gráfico de evolução das métricas por treino
├── tests/
│   └── __init__.py             # Pasta de testes (vazia)
└── dist/                       # Artefatos de build (wheel)
```

---

## Dependências

- Python **>=3.12, <4.0**
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências

### Dependências principais

| Pacote              | Versão                      |
|---------------------|-----------------------------|
| `fastapi[standard]` | >=0.139.0, <0.140.0         |
| `scikit-learn`      | >=1.9.0, <2.0.0             |
| `pandas`            | >=3.0.3, <4.0.0             |

### Dependências de desenvolvimento

| Pacote       | Versão              |
|--------------|---------------------|
| `pytest`     | >=9.1.1, <10.0.0    |
| `pytest-cov` | >=7.1.0, <8.0.0     |
| `taskipy`    | >=1.14.1, <2.0.0    |
| `ruff`       | >=0.15.20, <0.16.0  |

---

## Instalação do ambiente

1. Abra um terminal na pasta raiz do repositório.
2. Instale as dependências do Poetry:

```bash
poetry install
```

3. Ative o ambiente virtual do Poetry:

```bash
poetry shell
```

> Se não estiver usando Poetry, instale manualmente as dependências com `pip install fastapi[standard] pandas scikit-learn`.

---

## Executando o backend

### Recomendado (local)

1. Entre na pasta `backend`:

```bash
cd backend
```

2. Execute o servidor com Uvicorn:

```bash
python -m uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

### Observação importante

- O arquivo `backend/app/app.py` carrega o modelo com um caminho relativo:
  - `joblib.load("app/modelos/modelo_regressao.pkl")`
- Portanto, o servidor deve ser iniciado a partir de `backend/`, não de `backend/app/`.

Se você iniciar a partir de `backend/app/`, a aplicação tentará carregar `app/modelos/modelo_regressao.pkl` a partir do diretório errado e falhará.

---

## Frontend

O frontend está em `frontend/` e é projetado para consumir a API.

### Como abrir localmente

- Basta abrir `frontend/index.html` no navegador.
- Ou use um servidor de arquivos estático simples, por exemplo:

```bash
cd frontend
python -m http.server 5500
```

### Observação sobre URL da API

Atualmente, `frontend/js/api.js` usa a constante:

```js
const API = "https://trabalho-minera-o-de-dados-07.onrender.com";
```

Isso faz o frontend chamar uma API remota. Para usar a API local, altere para:

```js
const API = "http://127.0.0.1:8000";
```

---

## Endpoints da API

### `GET /json-bruto`
Retorna o conteúdo do arquivo `funcionarios_inteiros.csv` como JSON.

**Exemplo de resposta:**
```json
{
  "dados": { "idade": [25, 32, ...], "salario": [3000, 5000, ...], ... }
}
```

---

### `POST /predicao`
Recebe dados de um funcionário e retorna o `credit_score` previsto.

**Body (JSON):**
```json
{
  "idade": 35,
  "salario": 5000,
  "anos_de_estudo": 12,
  "anos_de_trabalho": 10
}
```

**Resposta:**
```json
{
  "score": 712
}
```

---

### `GET /metricas`
Calcula e retorna as métricas de desempenho do modelo atual usando `df_test.csv`.

**Resposta:**
```json
{
  "mae": 45.23,
  "mse": 3120.45,
  "rmse": 55.86,
  "r2": 0.8745
}
```

---

### `POST /criar-modelo-com-hiperparametros`
Treina um novo modelo `LinearRegression` com os hiperparâmetros fornecidos.  
O modelo é salvo em `backend/app/modelos/modelo_regressao.pkl` e recarregado no estado da aplicação.

**Body (JSON):**
```json
{
  "fit_intercept": true,
  "positive": false,
  "n_jobs": -1
}
```

**Resposta:**
```json
{
  "objetivo": "Treinar modelo com hiperparametros",
  "mensagem": "Modelo retreinado com sucesso!"
}
```

---

### `POST /split-dataset`
Divide o dataset `funcionarios_inteiros.csv` em treino e teste.

**Body (JSON):**
```json
{
  "test_size_percentage": 0.2
}
```

**Resposta:**
```json
{
  "objetivo": "Separar dataset com 20% para treino",
  "mensagem": "Dados divididos com sucesso!"
}
```

> ⚠️ **Nota:** A mensagem do campo `objetivo` pode conter uma descrição imprecisa da porcentagem (ex: `20.0% para treino` quando deveria ser `para teste`). Isso é um detalhe cosmético que não afeta a funcionalidade.

---

### `GET /dbscan`
Executa o algoritmo **DBSCAN** sobre `df_train.csv` e retorna os clusters e a redução PCA 2D.

**Resposta:**
```json
{
  "scan": { "age": [...], "income": [...], "education_years": [...], "experience": [...], "cluster": [...] },
  "pca": [[x1, y1], [x2, y2], ...]
}
```

---

### `GET /hdbscan`
Executa o algoritmo **HDBSCAN** sobre `df_train.csv` e retorna os clusters e a redução PCA 2D (mesmo formato do DBSCAN).

---

## Fluxo de Uso do Dashboard

1. **Abra o frontend** no navegador.
2. **Gráficos de clusterização** — DBSCAN e HDBSCAN são carregados automaticamente.
3. **Divida o dataset** — informe a porcentagem para teste e clique em **"Dividir Dataset"**.
4. **Ajuste os hiperparâmetros** (Fit Intercept, Positive, N Jobs) e clique em **"Criar Modelo"**.
5. As **métricas** (MAE, MSE, RMSE, R²) são exibidas e o painel de predição é habilitado.
6. O **gráfico de evolução** acumula os resultados de cada treino, permitindo visualizar o impacto dos hiperparâmetros.
7. **Faça uma predição** — preencha idade, salário, anos de estudo e anos de trabalho, e clique em **"Realizar Predição"**.

---

## Gráfico de Evolução das Métricas

A funcionalidade implementada em `frontend/js/historicoTreinos.js` registra **cada execução de treino** em um array e renderiza um gráfico de linhas com **Chart.js** com:

- **Eixo X** — número sequencial do treino (`#1`, `#2`, ...)
- **Eixo Y (esquerda)** — MAE
- **Eixo Y (direita)** — MSE / RMSE
- **Eixo Y (direita, range fixo 0–1)** — R² (com linha tracejada)
- **Tooltip** — mostra os hiperparâmetros usados em cada ponto (`fit=true pos=false jobs=1`)

Isso permite comparar visualmente como diferentes combinações de `fit_intercept`, `positive` e `n_jobs` afetam o desempenho do modelo.

---

## Problemas Conhecidos

### 1. Barras invertidas nos caminhos (`\`)
Em `backend/app/router_modelos.py`, os caminhos de arquivo usam barras invertidas:

```python
os.path.join(caminho_atual, "modelos\\modelo_regressao.pkl")   # ⚠️ Errado
os.path.join(caminho_atual, "arquivos\\funcionarios_inteiros.csv")
```

Isso **funciona no Windows**, mas **quebra no Linux/macOS**. A forma correta é usar segmentos separados:

```python
os.path.join(caminho_atual, "modelos", "modelo_regressao.pkl")  # ✅ Correto
os.path.join(caminho_atual, "arquivos", "funcionarios_inteiros.csv")
```

### 2. Arquivo `funcionarios_para_dashboard.csv` inexistente
O arquivo `backend/app/database.py` tenta ler `funcionarios_para_dashboard.csv`, que **não existe** na pasta `arquivos/`.  
Este módulo não é chamado pelo frontend, mas o código contém um bug latente.

### 3. URL remota configurada como padrão no frontend
O frontend aponta para uma API no Render (`onrender.com`). Para desenvolvimento local, é necessário alterar manualmente a constante `API` em `frontend/js/api.js`.

### 4. Rota `/json-bruto` usa caminho absoluto relativo incorreto
A rota usa `pd.read_csv("app/arquivos/funcionarios_inteiros.csv")` sem usar `caminho_atual`.  
Isso funciona quando o servidor é iniciado a partir de `backend/`, mas falha se executado de outro diretório.

---

## Melhorias Sugeridas

- [ ] Substituir barras invertidas por `os.path.join()` com segmentos separados em todo o `router_modelos.py`
- [ ] Corrigir o `database.py` para apontar para o CSV correto (`funcionarios_inteiros.csv`) ou remover código não utilizado
- [ ] Centralizar a URL da API em uma variável de ambiente ou arquivo de configuração
- [ ] Padronizar o uso de `caminho_atual` em **todas** as rotas (incluindo `/json-bruto`, `/metricas`, `/dbscan`, `/hdbscan`)
- [ ] Adicionar testes automatizados em `tests/` para os endpoints e lógica de ML
- [ ] Corrigir a descrição no campo `objetivo` da rota `/split-dataset` (menciona "para treino" em vez de "para teste")
- [ ] Adicionar tratamento de erros mais robusto nas rotas (arquivos não encontrados, modelo não treinado, etc.)

---

## Comandos úteis

Executar backend local:

```bash
cd backend
python -m uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

Executar frontend local:

```bash
cd frontend
python -m http.server 5500
```

Alterar API local no frontend:

```js
const API = "http://127.0.0.1:8000";
```

---

## Resumo

Esta é uma aplicação de demonstração de análise de crédito que combina **regressão linear** (para previsão de score) e **clusterização não supervisionada** (DBSCAN/HDBSCAN para segmentação de perfis).  

O frontend oferece uma interface visual com:
- Gráficos de dispersão (PCA) para DBSCAN e HDBSCAN
- Cards de métricas MAE, MSE, RMSE e R²
- **Gráfico de evolução** que acumula resultados a cada treino, permitindo comparar o efeito dos hiperparâmetros
- Painel de predição de score

Para uso local, certifique-se de:
- Executar o backend a partir de `backend/`
- Alterar a URL da API no frontend para `http://127.0.0.1:8000`
- Verificar a existência dos CSVs em `backend/app/arquivos/`
