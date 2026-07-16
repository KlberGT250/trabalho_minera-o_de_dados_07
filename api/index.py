import sys
import os
from pathlib import Path

# Adiciona backend/ ao path e muda o CWD para ele
backend_dir = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Importa o app FastAPI
from app.app import app


# Endpoint de health check (não depende de CSVs ou modelo)
from fastapi import APIRouter
health = APIRouter()

@health.get("/health")
def health_check():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "arquivos_existem": os.path.isdir(os.path.join(os.getcwd(), "app", "arquivos")),
        "modelo_existe": os.path.isfile(os.path.join(os.getcwd(), "app", "modelos", "modelo_regressao.pkl")),
    }

app.include_router(health)
