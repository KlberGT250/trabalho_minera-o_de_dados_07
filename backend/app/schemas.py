from pydantic import BaseModel, Field


class DataInput(BaseModel):
    idade: int
    salario: int
    anos_de_estudo: int
    anos_de_trabalho: int

class Hiperparametros(BaseModel):
    fit_intercept : bool = True  
    positive : bool  = True              
    n_jobs : int  = -1  

class Split(BaseModel):
    test_size_percentage: float = 0.2

class Matricas(BaseModel):
    mae : float
    mse : float
    rmse: float
    r2: float

class Score(BaseModel):
    score: float

class RespostaGenerica(BaseModel):
    objetivo: str
    mensagem: str
