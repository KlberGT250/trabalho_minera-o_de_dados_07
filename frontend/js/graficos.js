/**
 * graficos.js — Criação dos gráficos de dispersão DBSCAN e HDBSCAN.
 *
 * Cada gráfico consome a API para obter clusters + redução PCA
 * e renderiza um scatter plot com Chart.js, colorindo cada cluster.
 */

import { getDbscan, getHdbscan } from "./api.js";

/** Paleta fixa de cores para os clusters (até 10 grupos). */
const cores = [










    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
];



/**
 * Converte os dados da API (scan + pca) em datasets do Chart.js.
 *
 * @param {object} dados - Resposta da API: { scan: { cluster: [...], ... }, pca: [[x,y], ...] }
 * @returns {object[]} - Array de datasets prontos para o Chart.js
 */
function criarDatasets(dados) {
    const pca = dados.pca;
    const clusters = dados.scan.cluster;

    const datasets = {};



    for (let i = 0; i < pca.length; i++) {
        const cluster = clusters[i];



        if (!datasets[cluster]) {
            datasets[cluster] = {







                label: cluster === -1 ? "Ruído" : `Cluster ${cluster}`,
                data: [],
                backgroundColor:

                    cluster === -1
                        ? "#000000"
                        : cores[Math.abs(cluster) % cores.length],





                pointRadius: 5,
                pointHoverRadius: 8,
            };

        }

        datasets[cluster].data.push({





            x: pca[i][0],
            y: pca[i][1],
        });

    }

    return Object.values(datasets);

}





























/**
 * Configuração padrão de um gráfico scatter do Chart.js.
 *
 * @param {string} titulo - Título exibido no topo do gráfico
 * @param {object[]} datasets - Datasets gerados por criarDatasets()
 * @returns {object} - Configuração do Chart.js
 */
function configurarGrafico(titulo, datasets) {
    return {
        type: "scatter",
        data: { datasets },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: titulo,
                    font: { size: 14, weight: "600" },
                },







                legend: {
                    position: "bottom",
                },
            },

















            scales: {
                x: {
                    type: "linear",
                    position: "bottom",
                    title: { display: true, text: "PCA 1" },
                },

















































                y: {
                    title: { display: true, text: "PCA 2" },
                },







            },
        },
    };
}

































/**
 * Cria o gráfico de HDBSCAN no canvas #graficoHDBSCAN.
 * Os dados são buscados da API automaticamente.
 */
export async function criarGraficoHDBSCAN() {
    try {
        const dados = await getHdbscan();
        const ctx = document.getElementById("graficoHDBSCAN");
        new Chart(ctx, configurarGrafico("HDBSCAN", criarDatasets(dados)));
    } catch (error) {
        console.error("Erro ao carregar gráfico HDBSCAN:", error.message);
        const ctx = document.getElementById("graficoHDBSCAN");
        if (ctx) {
            ctx.parentElement.innerHTML +=
                `<p style="color: #e53935; text-align:center;">Erro: ${error.message}</p>`;
        }
    }
}



/**
 * Cria o gráfico de DBSCAN no canvas #graficoDBSCAN.
 * Os dados são buscados da API automaticamente.
 */
export async function criarGraficoDBSCAN() {
    try {
        const dados = await getDbscan();
        const ctx = document.getElementById("graficoDBSCAN");
        new Chart(ctx, configurarGrafico("DBSCAN", criarDatasets(dados)));
    } catch (error) {
        console.error("Erro ao carregar gráfico DBSCAN:", error.message);
        const ctx = document.getElementById("graficoDBSCAN");
        if (ctx) {
            ctx.parentElement.innerHTML +=
                `<p style="color: #e53935; text-align:center;">Erro: ${error.message}</p>`;
        }
    }
}
