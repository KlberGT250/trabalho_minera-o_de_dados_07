# Backend

O backend é uma aplicação **FastAPI** que expõe 7 endpoints REST. Está organizado em 4 módulos dentro de `backend/app/`.

---

## Módulo: `app.py` (ponto de entrada)

**Arquivo:** `backend/app/app.py`

### Responsabilidades

- Criar e configurar a instância do **FastAPI**
- Gerenciar o **ciclo de vida** da aplicação (carregar/descarregar o modelo)
- Configurar **CORS** para permitir requisições do frontend
- Importar e registrar o **router** de endpoints

### Lifespan

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
```

O FastAPI 0.139 utiliza o padrão `lifespan` (substitui eventos `startup`/`shutdown`):

1. **Startup** (`yield` anterior):
   - Verifica se `modelos/modelo_regressao.pkl` existe
   - Se existir: carrega com `joblib.load()` e armazena em `app.state.modelo_regressao`
   - Se não existir: loga aviso e define estado como `None`
2. **Shutdown** (`yield` posterior):
   - Remove `modelo_regressao` do state da aplicação

### CORS

Origens permitidas:
- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `https://trabalho-minera-o-de-dados-07.vercel.app`

### Constantes

```python
CAMINHO_ATUAL = os.path.dirname(__file__)
ARQUIVO_MODELO = os.path.join(CAMINHO_ATUAL, "modelos", "modelo_regressao.pkl")
```

---

## Módulo: `router_modelos.py` (rotas e lógica de ML)

**Arquivo:** `backend/app/router_modelos.py`

### Constantes de caminho

```python
CAMINHO_ATUAL = os.path.dirname(__file__)
ARQUIVOS_DIR = os.path.join(CAMINHO_ATUAL, "arquivos")
MODELOS_DIR = os.path.join(CAMINHO_ATUAL, "modelos")

ARQUIVO_DADOS_COMPLETOS = os.path.join(ARQUIVOS_DIR, "funcionarios_inteiros.csv")
ARQUIVO_TREINO = os.path.join(ARQUIVOS_DIR, "df_train.csv")
ARQUIVO_TESTE = os.path.join(ARQUIVOS_DIR, "df_test.csv")
ARQUIVO_MODELO = os.path.join(MODELOS_DIR, "modelo_regressao.pkl")
```

### Função auxiliar `_carregar_csv`

```python
def _carregar_csv(caminho: str) -> pd.DataFrame:
```

- Verifica se o arquivo existe com `os.path.exists()`
- Se não existir, levanta `HTTPException(404)`
- Se existir, retorna `pd.read_csv(caminho)`

### Endpoints

#### `GET /json-bruto`

```python
@router.get("/json-bruto")
def retornar_dados_completo():
```

- Carrega `funcionarios_inteiros.csv`
- Retorna como `{"dados": [ {...}, {...}, ... ]}` (`orient="records"`)
- **Sem modelo necessário** — funciona mesmo sem treinar

#### `POST /predicao`

```python
@router.post("/predicao", response_model=Score)
def prever_regressao(dados: DataInput, request: Request):
```

- Recebe `{ idade, salario, anos_de_estudo, anos_de_trabalho }`
- Obtém o modelo de `request.app.state.modelo_regressao`
- Retorna `{"score": float}`
- Se o modelo não foi carregado: `HTTPException(503)`

#### `GET /metricas`

```python
@router.get("/metricas", response_model=Metricas)
def metricas(request: Request):
```

- Carrega `df_test.csv`
- Remove a coluna `credit_score` (target)
- Calcula: MAE, MSE, RMSE, R²
- Retorna `{"mae": float, "mse": float, "rmse": float, "r2": float}`
- Se o modelo não foi carregado: `HTTPException(503)`

#### `POST /criar-modelo-com-hiperparametros`

```python
@router.post("/criar-modelo-com-hiperparametros", response_model=RespostaGenerica)
def criar_modelo_com_hiperparametros(hiperparametros: Hiperparametros, request: Request):
```

- Carrega `df_train.csv`
- Instancia `LinearRegression` com:
  - `fit_intercept` (bool)
  - `positive` (bool)
  - `n_jobs` (int)
- Treina com `.fit(X, y)`
- Salva com `joblib.dump()` em `modelo_regressao.pkl`
- Recarrega no estado da aplicação

#### `POST /split-dataset`

```python
@router.post("/split-dataset", response_model=RespostaGenerica)
def split_csv_data(split: Split):
```

- Carrega `funcionarios_inteiros.csv`
- Divide com `train_test_split(test_size=split.test_size_percentage)`
- Salva `df_train.csv` e `df_test.csv`
- Tratamento de erros: `FileNotFoundError` → 404, `Exception` → 500

#### `GET /dbscan` e `GET /hdbscan`

Ambos delegam para a função interna `_executar_clusterizacao`:

```python
def _executar_clusterizacao(algoritmo: str):
```

1. Carrega `df_train.csv`
2. Separa features (`X`) e remove target (`credit_score`)
3. Padroniza com `StandardScaler`
4. Executa o algoritmo:
   - **DBSCAN**: `eps=0.7, min_samples=5`
   - **HDBSCAN**: `min_cluster_size=15, min_samples=5`
5. Adiciona rótulos dos clusters ao DataFrame
6. Reduz dimensionalidade com `PCA(n_components=2)`
7. Retorna `{ "scan": { coluna: [valores...], "cluster": [...] }, "pca": [[x,y], ...] }`

---

## Módulo: `schemas.py`

**Arquivo:** `backend/app/schemas.py`

Define 6 modelos Pydantic para validação de entrada/saída:

| Classe | Uso | Campos |
|--------|-----|--------|
| `DataInput` | `POST /predicao` | `idade` (0-120), `salario` (≥0), `anos_de_estudo` (0-30), `anos_de_trabalho` (0-50) |
| `Hiperparametros` | `POST /criar-modelo-com-hiperparametros` | `fit_intercept` (default: True), `positive` (default: True), `n_jobs` (default: -1) |
| `Split` | `POST /split-dataset` | `test_size_percentage` (0.0-1.0, default: 0.2) |
| `Metricas` | Resposta de `GET /metricas` | `mae`, `mse`, `rmse`, `r2` (todos float) |
| `Score` | Resposta de `POST /predicao` | `score` (float) |
| `RespostaGenerica` | Resposta de operações | `objetivo` (str), `mensagem` (str) |

---

## Módulo: `database.py`

**Arquivo:** `backend/app/database.py`

> ⚠️ **Módulo não utilizado pelas rotas atuais.**

Contém uma função `dados()` que tenta ler `funcionarios_para_dashboard.csv` — arquivo que **não existe** no projeto. Mantido apenas como referência histórica. As rotas em `router_modelos.py` gerenciam seus próprios caminhos de arquivo.
