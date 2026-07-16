const API = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://trabalho-minera-o-de-dados-07.onrender.com";

export async function getMetricas(){

    const response = await fetch(`${API}/metricas`);

    return await response.json();

}

export async function getHdbscan(){

    const response = await fetch(`${API}/hdbscan`);

    return await response.json();

}

export async function getDbscan(){

    const response = await fetch(`${API}/dbscan`);

    return await response.json();

}

export async function getJsonBruto(){

    const response = await fetch(`${API}/json-bruto`);

    return await response.json();

}

export async function dividirDataset(testSize){

    const response = await fetch(`${API}/split-dataset`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            test_size_percentage:testSize
        })

    });

    return await response.json();

}

export async function criarModelo(hiperparametros){

    const response = await fetch(`${API}/criar-modelo-com-hiperparametros`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(hiperparametros)

    });

    return await response.json();

}

export async function prever(dados){

    const response = await fetch(`${API}/predicao`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(dados)

    });

    return await response.json();

}

