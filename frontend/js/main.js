import {criarGraficoDBSCAN, criarGraficoHDBSCAN } from "./graficos.js";

import {inicializarRegressao} from "./regressao.js";

window.onload = async ()=>{

    await criarGraficoDBSCAN();

    await criarGraficoHDBSCAN();

    inicializarRegressao();

}