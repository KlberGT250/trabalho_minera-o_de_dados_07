from fastapi import APIRouter, Request, HTTPException
from .schemas import DataInput, Hiperparametros, Split, Matricas, Score, RespostaGenerica
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
from sklearn.model_selection import train_test_split
from fastapi.responses import JSONResponse
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA


caminho_atual = os.path.dirname(__file__)


router = APIRouter()

@router.get('/json-bruto')
def retornar_dados_completo():
    df = pd.read_csv("app/arquivos/funcionarios_inteiros.csv")

    return {
        "dados": df.to_dict()
    }

@router.post("/predicao", response_model=Score)
def prever_regressao(dados: DataInput, request: Request):
    modelo = request.app.state.modelo_regressao
    resultado = modelo.predict([[dados.idade,
                                dados.salario,
                                dados.anos_de_estudo,
                                dados.anos_de_trabalho]])
    return {"score": int(resultado[0])}


@router.get("/metricas",
             response_model=Matricas)
def metricas(request: Request):
    modelo = request.app.state.modelo_regressao
    df_test = pd.read_csv('app/arquivos/df_test.csv')
    X = df_test.drop("credit_score", axis=1)
    y = df_test["credit_score"]

    y_pred = modelo.predict(X)

    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)

    return {'mae' : mae,
            'mse' : mse,
            'rmse': rmse,
            'r2'  : r2}

@router.post('/criar-modelo-com-hiperparametros', response_model=RespostaGenerica)
def criar_modelo_com_hiperparametros(hiperparametros: Hiperparametros, request: Request):
    df_train = pd.read_csv('app/arquivos/df_train.csv')
    X = df_train.drop("credit_score", axis=1)
    y = df_train["credit_score"]
    
    modelo_reg = LinearRegression(
        fit_intercept=hiperparametros.fit_intercept,  
        positive=hiperparametros.positive,  
        n_jobs=hiperparametros.n_jobs
        )
    modelo_reg.fit(X, y)
    joblib.dump(modelo_reg, os.path.join(caminho_atual, "modelos\\modelo_regressao.pkl") )
    request.app.state.modelo_regressao = joblib.load(os.path.join(caminho_atual, "modelos\\modelo_regressao.pkl"))
    
    return {
        'objetivo': 'Treinar modelo com hiperparametros',
        "mensagem": "Modelo retreinado com sucesso!"}

@router.post('/split-dataset', response_model=RespostaGenerica)
def split_csv_data(split: Split ):

    try:
        file_path = os.path.join(caminho_atual, "arquivos\\funcionarios_inteiros.csv")
        train_output_path=os.path.join(caminho_atual, "arquivos\\df_train.csv")
        test_output_path=os.path.join(caminho_atual, "arquivos\\df_test.csv")
        df = pd.read_csv(file_path)
        
        # Dividir o dataset
        df_train, df_test = train_test_split(df, test_size=split.test_size_percentage)
        
        # Salvar os conjuntos de treino e teste
        df_train.to_csv(train_output_path, index=False)
        df_test.to_csv(test_output_path, index=False)
        
        print(f"Dados divididos com sucesso")
        return {
        'objetivo': f'Separar dataset com {split.test_size_percentage*100}% para treino',
        "mensagem": "Dados divididos com sucesso!"}
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado no caminho especificado: {file_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

@router.get("/dbscan")
def dbscan():
    df_train = pd.read_csv("app/arquivos/df_train.csv")
    X = df_train.drop("credit_score", axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    dbscan = DBSCAN(eps=1.0, min_samples=5)
    labels = dbscan.fit_predict(X_scaled)

    df = pd.DataFrame(
        X,
        columns=["age", "income", "education_years", "experience"]
    )
    df["cluster"] = labels

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled) 

    return {
        "scan": df.to_dict(orient="list"),
        "pca": X_pca.tolist()
        }

@router.get("/hdbscan")
def Hdbscan():
    df_train = pd.read_csv("app/arquivos/df_train.csv")
    X = df_train.drop("credit_score", axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    hdb = HDBSCAN(min_cluster_size=5, min_samples=2)
    labels = hdb.fit_predict(X_scaled)

    df = pd.DataFrame(
        X,
        columns=["age", "income", "education_years", "experience"]
    )
    df["cluster"] = labels

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled) 

    return {
        "scan": df.to_dict(orient="list"),
        "pca": X_pca.tolist()
        }
    
    
    
