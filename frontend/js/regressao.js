import {

    dividirDataset,

    criarModelo,

    prever,

    getMetricas

} from "./api.js";

export function inicializarRegressao(){

    document
        .getElementById("btnDividir")
        .addEventListener("click", dividir);

    document
        .getElementById("btnTreinar")
        .addEventListener("click", treinarModelo);

    document
        .getElementById("btnPredicao")
        .addEventListener("click", fazerPredicao);

}

async function dividir(){

    const porcentagem =
        Number(document.getElementById("testSize").value) / 100;

    const resposta = await dividirDataset(porcentagem);

    const status = document.getElementById("statusSplit");

    status.style.display = "block";

    status.textContent = resposta.mensagem;

}

async function treinarModelo(){

    const hiper = {

        fit_intercept:
            document.getElementById("fitIntercept").checked,

        positive:
            document.getElementById("positive").checked,

        n_jobs:
            Number(document.getElementById("nJobs").value)

    };

    const resposta = await criarModelo(hiper);
    await atualizarMetricas();

    document.getElementById("statusModelo").textContent = resposta.mensagem;

    document.getElementById("painelPredicao").style.display = "block";

}

async function fazerPredicao(){

    const dados = {

        idade: Number(document.getElementById("idade").value),

        salario: Number(document.getElementById("salario").value),

        anos_de_estudo: Number(document.getElementById("estudo").value),

        anos_de_trabalho: Number(document.getElementById("trabalho").value)

    };

    const resposta = await prever(dados);

    document.getElementById("resultado").textContent =
        resposta.score;

}

async function atualizarMetricas(){

    const metricas = await getMetricas();

    document.getElementById("mae").textContent =
        metricas.mae.toFixed(2);

    document.getElementById("mse").textContent =
        metricas.mse.toFixed(2);

    document.getElementById("rmse").textContent =
        metricas.rmse.toFixed(2);

    document.getElementById("r2").textContent =
        metricas.r2.toFixed(4);

}