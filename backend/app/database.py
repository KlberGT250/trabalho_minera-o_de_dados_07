"""
database.py — Função de leitura de dados CSV.

ATENÇÃO: Este módulo não é utilizado pelo frontend nem pelas rotas atuais.
O arquivo 'funcionarios_para_dashboard.csv' referenciado abaixo NÃO EXISTE.
Para leitura de dados, as rotas em router_modelos.py usam caminhos próprios.
"""

import os

import pandas as pd


def dados():
    """
    Retorna o conteúdo do dataset como JSON.

    Nota: esta função referencia um arquivo que não existe
    (funcionarios_para_dashboard.csv). Mantida apenas para
    referência histórica.
    """
    caminho_atual = os.path.dirname(__file__)
    # ⚠️ Arquivo abaixo não existe na pasta arquivos/
    caminho_csv = os.path.join(caminho_atual, "funcionarios_para_dashboard.csv")

    try:
        df = pd.read_csv(caminho_csv)
        return df.to_json()
    except FileNotFoundError:
        return '{"erro": "Arquivo funcionarios_para_dashboard.csv não encontrado"}'
