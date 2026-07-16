import sys
import os
from pathlib import Path

# Adiciona backend/ ao path
backend_dir = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from app.app import app
