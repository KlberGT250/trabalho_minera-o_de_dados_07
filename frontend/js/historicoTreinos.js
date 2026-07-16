/**
 * historicoTreinos.js
 *
 * Mantém um histórico das métricas a cada treino e exibe
 * um gráfico de linhas mostrando a evolução dos resultados
 * conforme os hiperparâmetros são alterados.
 */

const historico = [];
let graficoHistorico = null;

/**
 * Registra um novo treino no histórico e atualiza o gráfico.
 *
 * @param {Object} hiperparametros  - { fit_intercept, positive, n_jobs }
 * @param {Object} metricas         - { mae, mse, rmse, r2 }
 */
export function registrarTreino(hiperparametros, metricas) {
  const label = `#${historico.length + 1}`;
  const descricao = `fit=${hiperparametros.fit_intercept} pos=${hiperparametros.positive} jobs=${hiperparametros.n_jobs}`;

  historico.push({
    label,
    descricao,
    ...metricas,
  });

  renderizarGrafico();
}

/**
 * Renderiza (ou atualiza) o gráfico de linhas com Chart.js.
 */
function renderizarGrafico() {
  const ctx = document.getElementById("graficoHistorico");
  if (!ctx) return;

  const labels = historico.map((h) => h.label);
  const descricoes = historico.map((h) => h.descricao);

  if (graficoHistorico) {
    graficoHistorico.destroy();
  }

  graficoHistorico = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "MAE",
          data: historico.map((h) => h.mae),
          borderColor: "#1976d2",
          backgroundColor: "rgba(25, 118, 210, 0.1)",
          yAxisID: "y",
          tension: 0.3,
          fill: false,
        },
        {
          label: "MSE",
          data: historico.map((h) => h.mse),
          borderColor: "#7b1fa2",
          backgroundColor: "rgba(123, 31, 162, 0.1)",
          yAxisID: "y1",
          tension: 0.3,
          fill: false,
        },
        {
          label: "RMSE",
          data: historico.map((h) => h.rmse),
          borderColor: "#00897b",
          backgroundColor: "rgba(0, 137, 123, 0.1)",
          yAxisID: "y1",
          tension: 0.3,
          fill: false,
        },
        {
          label: "R²",
          data: historico.map((h) => h.r2),
          borderColor: "#f57c00",
          backgroundColor: "rgba(245, 124, 0, 0.1)",
          yAxisID: "y2",
          tension: 0.3,
          fill: false,
          borderDash: [5, 3],
        },
      ],
    },
    options: {
      responsive: true,
      interaction: {
        mode: "index",
        intersect: false,
      },
      plugins: {
        title: {
          display: true,
          text: "Evolução das Métricas por Treino",
          font: { size: 14, weight: "600" },
        },
        tooltip: {
          callbacks: {
            afterTitle(items) {
              const idx = items[0].dataIndex;
              return descricoes[idx] || "";
            },
          },
        },
        legend: {
          position: "bottom",
        },
      },
      scales: {
        x: {
          title: { display: true, text: "Treino" },
        },
        y: {
          type: "linear",
          display: true,
          position: "left",
          title: { display: true, text: "MAE" },
        },
        y1: {
          type: "linear",
          display: true,
          position: "right",
          title: { display: true, text: "MSE / RMSE" },
          grid: { drawOnChartArea: false },
        },
        y2: {
          type: "linear",
          display: true,
          position: "right",
          title: { display: true, text: "R²" },
          grid: { drawOnChartArea: false },
          // O R² normalmente fica entre 0 e 1; forçamos o range
          min: 0,
          max: 1,
        },
      },
    },
  });
}
