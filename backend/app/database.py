import pandas as pd
import os

def dados():
    caminho_atual = os.path.dirname(__file__)
    caminho_csv = os.path.join(caminho_atual, 'funcionarios_para_dashboard.csv')
    
    df = pd.read_csv(caminho_csv)
    return df.to_json()
