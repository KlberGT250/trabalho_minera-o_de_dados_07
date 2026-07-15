from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib

from app import router_modelos


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.modelo_regressao = joblib.load("app/modelos/modelo_regressao.pkl")

    yield

    del app.state.modelo_regressao


app = FastAPI(lifespan=lifespan)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_modelos.router)