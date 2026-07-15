import { getDbscan, getHdbscan } from "./api.js";

const cores = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf"
];

function criarDatasets(dados){

    const pca = dados.pca;
    const clusters = dados.scan.cluster;

    const datasets = {};

    for(let i = 0; i < pca.length; i++){

        const cluster = clusters[i];

        if(!datasets[cluster]){

            datasets[cluster] = {

                label: cluster == -1
                    ? "Ruído"
                    : `Cluster ${cluster}`,

                data:[],

                backgroundColor:
                    cluster == -1
                        ? "#000000"
                        : cores[Math.abs(cluster) % cores.length],

                pointRadius:5,

                pointHoverRadius:8

            };

        }

        datasets[cluster].data.push({

            x:pca[i][0],

            y:pca[i][1]

        });

    }

    return Object.values(datasets);

}

export async function criarGraficoHDBSCAN(){

    const dados = await getHdbscan();

    const ctx = document.getElementById("graficoHDBSCAN");

    new Chart(ctx,{

        type:"scatter",

        data:{

            datasets:criarDatasets(dados)

        },

        options:{

            responsive:true,

            plugins:{

                title:{

                    display:true,

                    text:"HDBSCAN"

                },

                legend:{

                    position:"bottom"

                }

            },

            scales:{

                x:{

                    type:"linear",

                    position:"bottom",

                    title:{

                        display:true,

                        text:"PCA 1"

                    }

                },

                y:{

                    title:{

                        display:true,

                        text:"PCA 2"

                    }

                }

            }

        }

    });

}

export async function criarGraficoDBSCAN(){

    const dados = await getDbscan();

    const ctx = document.getElementById("graficoDBSCAN");

    new Chart(ctx,{

        type:"scatter",

        data:{

            datasets:criarDatasets(dados)

        },

        options:{

            responsive:true,

            plugins:{

                title:{

                    display:true,

                    text:"DBSCAN"

                },

                legend:{

                    position:"bottom"

                }

            },

            scales:{

                x:{

                    type:"linear",

                    position:"bottom",

                    title:{

                        display:true,

                        text:"PCA 1"

                    }

                },

                y:{

                    title:{

                        display:true,

                        text:"PCA 2"

                    }

                }

            }

        }

    });

}