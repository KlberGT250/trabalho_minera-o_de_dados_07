"""
app.py — Ponto de entrada da aplicação FastAPI.

Inicializa o servidor, configura CORS e carrega o modelo de regressão
no estado da aplicação durante o lifespan.
"""

import logging
import os
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import router_modelos

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para o modelo (relativo a este arquivo)
CAMINHO_ATUAL = os.path.dirname(__file__)
ARQUIVO_MODELO = os.path.join(CAMINHO_ATUAL, "modelos", "modelo_regressao.pkl")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação:
    - startup: carrega o modelo do disco
    - shutdown: libera o modelo da memória
    """
    modelo_path = ARQUIVO_MODELO
    if not os.path.exists(modelo_path):
        logger.warning(
            f"Arquivo de modelo não encontrado: {modelo_path}. "
            "Treine um modelo usando o endpoint /criar-modelo-com-hiperparametros."
        )
        app.state.modelo_regressao = None
    else:
        try:
            app.state.modelo_regressao = joblib.load(modelo_path)
            logger.info(f"Modelo carregado com sucesso de: {modelo_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            app.state.modelo_regressao = None

    yield

    # Shutdown
    if hasattr(app.state, "modelo_regressao"):
        del app.state.modelo_regressao


app = FastAPI(
    title="API de Análise de Crédito",
    description=(
        "API para análise de crédito com regressão linear e "
        "clusterização (DBSCAN / HDBSCAN)."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

# Configuração do CORS — permite requisições do frontend local e remoto
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://trabalho-minera-o-de-dados-07.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_modelos.router)

# Monta o frontend como arquivos estáticos (para Vercel)
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
