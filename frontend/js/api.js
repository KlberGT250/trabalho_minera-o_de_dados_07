
/**
 * api.js — Funções para chamar os endpoints da API de análise de crédito.
 *



 * Todas as funções usam fetch() com um wrapper centralizado de tratamento de erros.
 * A constante API pode ser alterada para apontar para ambiente local ou remoto.
 */

/** URL base da API */
const API = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://trabalho-minera-o-de-dados-07.onrender.com";
/**

 * Wrapper centralizado para chamadas fetch.
 *
 * @param {string} url - URL completa do endpoint
 * @param {object} [options] - Opções do fetch (method, headers, body)

 * @returns {Promise<object>} - Resposta JSON decodificada
 * @throws {Error} - Se a requisição falhar ou o servidor retornar erro HTTP
 */
async function request(url, options = {}) {
    let response;
    try {

        response = await fetch(url, options);
    } catch (networkError) {
        throw new Error(
            "Não foi possível conectar ao servidor. Verifique se o backend está rodando."
        );
    }







    if (!response.ok) {
        let detail = `Erro HTTP ${response.status}`;
        try {
            const body = await response.json();
            if (body.detail) detail = body.detail;
        } catch {
            // corpo não é JSON — mantém a mensagem padrão
        }
        throw new Error(detail);
    }







    return response.json();
}




/**


 * Busca as métricas de desempenho do modelo atual.
 * GET /metricas → { mae, mse, rmse, r2 }
 */
export async function getMetricas() {
    return request(`${API}/metricas`);
}







/**


 * Busca dados do HDBSCAN (clusters + redução PCA).
 * GET /hdbscan → { scan: {...}, pca: [[x,y], ...] }
 */
export async function getHdbscan() {
    return request(`${API}/hdbscan`);
}







/**


 * Busca dados do DBSCAN (clusters + redução PCA).
 * GET /dbscan → { scan: {...}, pca: [[x,y], ...] }
 */
export async function getDbscan() {
    return request(`${API}/dbscan`);
}







/**
 * Busca o dataset completo em formato JSON.

 * GET /json-bruto → { dados: {...} }
 */
export async function getJsonBruto() {
    return request(`${API}/json-bruto`);
}















/**
 * Divide o dataset em treino e teste.
 * POST /split-dataset
 *

 * @param {number} testSize - Proporção para teste (0.0 a 1.0, ex: 0.2)
 */
export async function dividirDataset(testSize) {
    return request(`${API}/split-dataset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ test_size_percentage: testSize }),
    });



}













/**
 * Treina um novo modelo LinearRegression com hiperparâmetros.
 * POST /criar-modelo-com-hiperparametros
 *
 * @param {object} hiperparametros - { fit_intercept, positive, n_jobs }
 */
export async function criarModelo(hiperparametros) {
    return request(`${API}/criar-modelo-com-hiperparametros`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(hiperparametros),
    });



}













/**
 * Realiza uma predição de credit_score.
 * POST /predicao
 *
 * @param {object} dados - { idade, salario, anos_de_estudo, anos_de_trabalho }
 */
export async function prever(dados) {
    return request(`${API}/predicao`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });



}

