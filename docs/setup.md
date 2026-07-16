# Instalação e Execução

## Pré-requisitos

- Python **>=3.12** (testado com 3.14)
- [Poetry](https://python-poetry.org/) (gerenciador de dependências)

## Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd trabalho_minera-o_de_dados_07

# Instalar dependências (incluindo dev)
poetry install

# Ativar o ambiente virtual
poetry shell
```

### Dependências

| Pacote | Versão | Finalidade |
|--------|--------|------------|
| `fastapi[standard]` | >=0.139.0, <0.140.0 | Framework web |
| `scikit-learn` | >=1.9.0, <2.0.0 | Machine learning |
| `pandas` | >=3.0.3, <4.0.0 | Manipulação de dados |
| `joblib` | (indireta) | Serialização de modelos |

### Dependências de desenvolvimento

| Pacote | Versão | Finalidade |
|--------|--------|------------|
| `pytest` | >=9.1.1 | Testes |
| `pytest-cov` | >=7.1.0 | Cobertura de testes |
| `ruff` | >=0.15.20 | Linter e formatador |
| `taskipy` | >=1.14.1 | Task runner |

## Execução

### Backend

O servidor **deve** ser iniciado a partir do diretório `backend/` para que os caminhos relativos dos arquivos CSV e do modelo funcionem corretamente.

```bash
cd backend
python -m uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

O parâmetro `--reload` reinicia automaticamente o servidor a cada alteração no código.

A API estará disponível em **http://127.0.0.1:8000**.

Documentação interativa (Swagger): **http://127.0.0.1:8000/docs**

### Frontend

```bash
cd frontend
python -m http.server 5500
```

O dashboard estará disponível em **http://127.0.0.1:5500**.

> O frontend carrega Chart.js via CDN — é necessária conexão com a internet na primeira execução.

## Configuração da URL da API

No arquivo `frontend/js/api.js`, a constante `API` define o endpoint base:

```javascript
const API = "http://127.0.0.1:8000";  // local
// const API = "https://<url-producao>";  // remoto
```

## Verificação

Para confirmar que tudo está funcionando:

```bash
# Testar se o servidor está no ar
curl http://127.0.0.1:8000/json-bruto | python3 -c "import sys,json; print(len(json.load(sys.stdin)['dados']), 'registros')"

# Testar predição
curl -X POST http://127.0.0.1:8000/predicao \
  -H "Content-Type: application/json" \
  -d '{"idade":35,"salario":5000,"anos_de_estudo":12,"anos_de_trabalho":10}'
```

## Comandos Taskipy

```bash
task lint        # Executa ruff check
task format      # Executa ruff format
task test        # Executa pytest com cobertura
task run         # Executa fastapi dev
```
