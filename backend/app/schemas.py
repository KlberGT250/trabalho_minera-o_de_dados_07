"""
schemas.py — Modelos Pydantic para validação de dados da API.

Define os esquemas de requisição e resposta para todos os endpoints.
"""

from pydantic import BaseModel, Field


class DataInput(BaseModel):
    """Dados de entrada para predição de credit_score."""
    idade: int = Field(..., ge=0, le=120, description="Idade do funcionário")
    salario: int = Field(..., ge=0, description="Salário do funcionário")
    anos_de_estudo: int = Field(..., ge=0, le=30, description="Anos de estudo")
    anos_de_trabalho: int = Field(..., ge=0, le=50, description="Anos de trabalho")


class Hiperparametros(BaseModel):
    """Hiperparâmetros para treinamento do modelo LinearRegression."""
    fit_intercept: bool = True
    positive: bool = True
    n_jobs: int = -1


class Split(BaseModel):
    """Parâmetros para divisão do dataset."""
    test_size_percentage: float = Field(
        default=0.2, ge=0.0, le=1.0, description="Proporção do conjunto de teste"
    )


class Metricas(BaseModel):
    """Métricas de desempenho do modelo."""
    mae: float
    mse: float
    rmse: float
    r2: float


class Score(BaseModel):
    """Resultado da predição de credit_score."""
    score: float


class RespostaGenerica(BaseModel):
    """Resposta genérica para operações com mensagem de retorno."""
    objetivo: str
    mensagem: str
