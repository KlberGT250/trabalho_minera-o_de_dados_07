import sys
import os
from pathlib import Path

# Adiciona o diretório backend/ ao path para importar o módulo app
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.app import app

# Vercel espera a variável 'app' como handler ASGI
