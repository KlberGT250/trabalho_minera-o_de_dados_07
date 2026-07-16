"""
router_modelos.py — Rotas da API de análise de crédito.

Endpoints:
  - GET  /json-bruto              → Retorna dataset completo em JSON
  - POST /predicao                → Prediz credit_score com regressão linear
  - GET  /metricas                → Métricas de desempenho do modelo
  - POST /criar-modelo-com-hiperparametros → Treina novo modelo LinearRegression
  - POST /split-dataset           → Divide dataset em treino/teste
  - GET  /dbscan                  → Clusterização com DBSCAN + PCA
  - GET  /hdbscan                 → Clusterização com HDBSCAN + PCA
"""

import os

import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from sklearn.cluster import DBSCAN, HDBSCAN
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .schemas import (
    DataInput,
    Hiperparametros,
    Metricas,
    RespostaGenerica,
    Score,
    Split,
)

# Diretório onde este arquivo está localizado
CAMINHO_ATUAL = os.path.dirname(__file__)

# Caminhos para os arquivos de dados e modelo
ARQUIVOS_DIR = os.path.join(CAMINHO_ATUAL, "arquivos")
MODELOS_DIR = os.path.join(CAMINHO_ATUAL, "modelos")

ARQUIVO_DADOS_COMPLETOS = os.path.join(ARQUIVOS_DIR, "funcionarios_inteiros.csv")
ARQUIVO_TREINO = os.path.join(ARQUIVOS_DIR, "df_train.csv")
ARQUIVO_TESTE = os.path.join(ARQUIVOS_DIR, "df_test.csv")
ARQUIVO_MODELO = os.path.join(MODELOS_DIR, "modelo_regressao.pkl")


router = APIRouter()


def _carregar_csv(caminho: str) -> pd.DataFrame:
    """
    Carrega um arquivo CSV e lança HTTPException 404 se não existir.
    """
    if not os.path.exists(caminho):
        raise HTTPException(
            status_code=404,
            detail=f"Arquivo não encontrado: {caminho}",
        )
    return pd.read_csv(caminho)


@router.get("/json-bruto")
def retornar_dados_completo():

    """
    Retorna o dataset completo (funcionarios_inteiros.csv) como JSON.
    """
    df = _carregar_csv(ARQUIVO_DADOS_COMPLETOS)
    return {"dados": df.to_dict(orient="records")}


@router.post("/predicao", response_model=Score)
def prever_regressao(dados: DataInput, request: Request):
    """
    Recebe dados de um funcionário e retorna o credit_score previsto.

    Campos esperados: idade, salario, anos_de_estudo, anos_de_trabalho.
    """
    modelo = request.app.state.modelo_regressao

    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    entrada = [[dados.idade, dados.salario, dados.anos_de_estudo, dados.anos_de_trabalho]]
    resultado = modelo.predict(entrada)
    return {"score": float(resultado[0])}


@router.get("/metricas", response_model=Metricas)
def metricas(request: Request):
    """
    Calcula e retorna as métricas de desempenho do modelo atual
    usando o conjunto de teste (df_test.csv).
    """
    modelo = request.app.state.modelo_regressao

    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    df_test = _carregar_csv(ARQUIVO_TESTE)
    X = df_test.drop("credit_score", axis=1)
    y = df_test["credit_score"]

    y_pred = modelo.predict(X)

    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)

    rmse = float(np.sqrt(mse))
    r2 = r2_score(y, y_pred)

    return {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}


@router.post("/criar-modelo-com-hiperparametros", response_model=RespostaGenerica)
def criar_modelo_com_hiperparametros(hiperparametros: Hiperparametros, request: Request):

    """
    Treina um novo modelo LinearRegression com os hiperparâmetros fornecidos.

    O modelo é salvo em disco e recarregado no estado da aplicação.
    """
    df_train = _carregar_csv(ARQUIVO_TREINO)
    X = df_train.drop("credit_score", axis=1)
    y = df_train["credit_score"]

    modelo_reg = LinearRegression(




        fit_intercept=hiperparametros.fit_intercept,
        positive=hiperparametros.positive,
        n_jobs=hiperparametros.n_jobs,
    )
    modelo_reg.fit(X, y)

    # Salvar e recarregar no estado da aplicação
    joblib.dump(modelo_reg, ARQUIVO_MODELO)
    request.app.state.modelo_regressao = joblib.load(ARQUIVO_MODELO)

    return {


        "objetivo": "Treinar modelo com hiperparametros",
        "mensagem": "Modelo retreinado com sucesso!",
    }


@router.post("/split-dataset", response_model=RespostaGenerica)
def split_csv_data(split: Split):
    """
    Divide o dataset completo (funcionarios_inteiros.csv) em
    treino (df_train.csv) e teste (df_test.csv).

    O parâmetro test_size_percentage define a proporção para teste (0.0 a 1.0).
    """
    try:

        df = _carregar_csv(ARQUIVO_DADOS_COMPLETOS)

        df_train, df_test = train_test_split(df, test_size=split.test_size_percentage)

        df_train.to_csv(ARQUIVO_TREINO, index=False)
        df_test.to_csv(ARQUIVO_TESTE, index=False)

        return {


            "objetivo": f"Separar dataset com {split.test_size_percentage * 100:.0f}% para teste",
            "mensagem": "Dados divididos com sucesso!",
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"Arquivo não encontrado: {ARQUIVO_DADOS_COMPLETOS}",
        )
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Erro ao dividir dataset: {e}")


def _executar_clusterizacao(algoritmo: str):
    """
    Executa DBSCAN ou HDBSCAN sobre df_train.csv e retorna
    os clusters + redução PCA 2D.

    Args:
        algoritmo: "dbscan" ou "hdbscan"

    Returns:
        dict com "scan" (dados + cluster) e "pca" (coordenadas 2D)
    """
    df_train = _carregar_csv(ARQUIVO_TREINO)
    X = df_train.drop("credit_score", axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    if algoritmo == "dbscan":
        modelo = DBSCAN(eps=0.7, min_samples=5)
    elif algoritmo == "hdbscan":
        modelo = HDBSCAN(min_cluster_size=15, min_samples=5)
    else:
        raise HTTPException(status_code=400, detail=f"Algoritmo desconhecido: {algoritmo}")

    labels = modelo.fit_predict(X_scaled)

    # Preservar os nomes originais das colunas do CSV
    df_resultado = df_train.drop("credit_score", axis=1).copy()
    df_resultado["cluster"] = labels

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    return {



        "scan": df_resultado.to_dict(orient="list"),
        "pca": X_pca.tolist(),
    }


@router.get("/dbscan")
def dbscan():
    """Executa DBSCAN sobre df_train.csv e retorna clusters + PCA."""
    return _executar_clusterizacao("dbscan")


@router.get("/hdbscan")
def hdbscan():
    """Executa HDBSCAN sobre df_train.csv e retorna clusters + PCA."""
    return _executar_clusterizacao("hdbscan")
