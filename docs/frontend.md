# Frontend

O frontend é uma **Single Page Application (SPA)** em JavaScript puro (sem frameworks), organizada em módulos ES6. Utiliza **Chart.js** via CDN para renderização de gráficos.

---

## HTML: `index.html`

**Arquivo:** `frontend/index.html`

### Estrutura

```
<body>
  <header>          ← Título e subtítulo
  <main>
    <section>       ← Clusterização (DBSCAN + HDBSCAN)
    <section>       ← Treinamento (métricas, split, hiperparâmetros)
    <section>       ← Evolução das métricas
    <section>       ← Predição (formulário + resultado)
  </main>
  <script module>   ← Carrega js/main.js
</body>
```

### Elementos DOM relevantes

| ID | Tipo | Finalidade |
|----|------|------------|
| `graficoDBSCAN` | `<canvas>` | Gráfico scatter DBSCAN |
| `graficoHDBSCAN` | `<canvas>` | Gráfico scatter HDBSCAN |
| `graficoHistorico` | `<canvas>` | Gráfico de evolução das métricas |
| `mae`, `mse`, `rmse`, `r2` | `<span>` | Cards de métricas |
| `testSize` | `<input number>` | % do conjunto de teste |
| `btnDividir` | `<button>` | Ação de dividir dataset |
| `fitIntercept` | `<input checkbox>` | Hiperparâmetro |
| `positive` | `<input checkbox>` | Hiperparâmetro |
| `nJobs` | `<input number>` | Hiperparâmetro |
| `btnTreinar` | `<button>` | Ação de treinar modelo |
| `btnPredicao` | `<button>` | Ação de predizer |
| `idade`, `salario`, `estudo`, `trabalho` | `<input number>` | Dados para predição |
| `resultado` | `<span>` | Resultado da predição |
| `painelPredicao` | `<section>` | Seção de predição (oculta inicialmente) |

---

## JavaScript: `main.js` (ponto de entrada)

**Arquivo:** `frontend/js/main.js`

```javascript
import { criarGraficoDBSCAN, criarGraficoHDBSCAN } from "./graficos.js";
import { inicializarRegressao } from "./regressao.js";

window.onload = async () => {
    await criarGraficoDBSCAN();
    await criarGraficoHDBSCAN();
    inicializarRegressao();
};
```

**Fluxo:**
1. Aguarda o carregamento da página (`window.onload`)
2. Busca dados da API e renderiza gráfico DBSCAN
3. Busca dados da API e renderiza gráfico HDBSCAN
4. Registra event listeners para os botões de split, treino e predição

---

## JavaScript: `api.js` (comunicação HTTP)

**Arquivo:** `frontend/js/api.js`

### Constante

```javascript
const API = "http://127.0.0.1:8000";
```

### Função interna `request`

```javascript
async function request(url, options = {})
```

Wrapper centralizado para `fetch()`:
- Captura erros de rede e lança mensagem amigável
- Verifica `response.ok` — se falso, extrai `body.detail` do JSON de erro
- Retorna o JSON decodificado

### Funções exportadas

| Função | Método | Endpoint |
|--------|--------|----------|
| `getMetricas()` | GET | `/metricas` |
| `getHdbscan()` | GET | `/hdbscan` |
| `getDbscan()` | GET | `/dbscan` |
| `getJsonBruto()` | GET | `/json-bruto` |
| `dividirDataset(testSize)` | POST | `/split-dataset` |
| `criarModelo(hiperparametros)` | POST | `/criar-modelo-com-hiperparametros` |
| `prever(dados)` | POST | `/predicao` |

---

## JavaScript: `graficos.js` (gráficos de clusterização)

**Arquivo:** `frontend/js/graficos.js`

### Fluxo

```
getDbscan() / getHdbscan()
    → dados = { scan: { cluster: [...], ... }, pca: [[x,y], ...] }
    → criarDatasets(dados)
    → configurarGrafico(titulo, datasets)
    → new Chart(ctx, config)
```

### `criarDatasets(dados)`

Agrupa pontos por cluster:
- Itera sobre `pca` e `scan.cluster` simultaneamente
- Para cada cluster, cria um dataset separado
- Ruído (cluster -1) recebe cor preta e label "Ruído"
- Clusters válidos recebem cores da paleta `cores` (cíclica)

### `configurarGrafico(titulo, datasets)`

Configuração padrão Chart.js:
- Tipo: `scatter`
- Eixos: PCA 1 (x), PCA 2 (y)
- Título configurável
- Legenda na parte inferior

### `criarGraficoDBSCAN()` e `criarGraficoHDBSCAN()`

- Chamam a API correspondente
- Renderizam no canvas apropriado
- Em caso de erro: exibem mensagem no console e no DOM

---

## JavaScript: `regressao.js` (treinamento e predição)

**Arquivo:** `frontend/js/regressao.js`

### `inicializarRegressao()`

Registra 3 event listeners:

| Botão | Handler |
|-------|---------|
| `btnDividir` | `dividir()` |
| `btnTreinar` | `treinarModelo()` |
| `btnPredicao` | `fazerPredicao()` |

### `dividir()`

- Lê `testSize` (valor ÷ 100)
- Chama `dividirDataset(porcentagem)`
- Exibe mensagem de retorno no `#statusSplit`

### `treinarModelo()`

1. Lê valores dos campos de hiperparâmetros
2. Chama `criarModelo(hiper)`
3. Chama `getMetricas()`
4. Atualiza os 4 cards de métrica via `atualizarMetricas()`
5. Registra no histórico via `registrarTreino(hiper, metricas)`
6. Exibe mensagem de sucesso
7. Torna visível o painel de predição (`#painelPredicao`)

### `fazerPredicao()`

1. Lê valores dos campos de entrada
2. Chama `prever(dados)`
3. Exibe `resposta.score` no `#resultado`

### `atualizarMetricas(metricas)`

Atualiza o `textContent` dos 4 spans com valores formatados:
- MAE, MSE, RMSE → 2 casas decimais
- R² → 4 casas decimais

---

## JavaScript: `historicoTreinos.js` (evolução das métricas)

**Arquivo:** `frontend/js/historicoTreinos.js`

### Estado

```javascript
const historico = [];       // Array de { label, descricao, mae, mse, rmse, r2 }
let graficoHistorico = null; // Instância do Chart
```

### `registrarTreino(hiperparametros, metricas)`

- Cria label sequencial: `#1`, `#2`, ...
- Cria descrição: `fit=true pos=false jobs=1`
- Adiciona ao array `historico`
- Chama `renderizarGrafico()`

### `renderizarGrafico()`

Renderiza um gráfico de linhas Chart.js com:

| Dataset | Eixo Y | Cor |
|---------|--------|-----|
| MAE | `y` (esquerda) | Azul `#1976d2` |
| MSE | `y1` (direita) | Roxo `#7b1fa2` |
| RMSE | `y1` (direita) | Verde `#00897b` |
| R² | `y2` (direita, 0-1) | Laranja `#f57c00` (tracejado) |

O tooltip mostra a descrição dos hiperparâmetros usados em cada ponto.

---

## CSS

### `style.css` (319 linhas)

- **Variáveis CSS**: cores primárias, sombras, raio de borda
- **Header**: gradiente azul com elemento decorativo circular
- **Cards**: fundo branco, borda arredondada, sombra suave
- **Grid de gráficos**: 2 colunas (responsive: 1 coluna em mobile)
- **Grid de métricas**: 4 colunas (responsive: 2 → 1 coluna)
- **Formulários**: flex-wrap com labels estilizados
- **Botões**: azul primário com hover elevado
- **Cards de métrica**: borda superior colorida, número grande em negrito
- **Resultado**: gradiente de fundo, score em destaque

### `dashboard.css` (50 linhas)

- Sobrescreve estilo dos containers de gráfico com borda colorida
- Oculta o `<h3>` manual (o título é renderizado pelo Chart.js)
- Define altura fixa de 320px para os canvases
