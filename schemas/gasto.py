from datetime import date
from pydantic import BaseModel
from typing import List

class GastoSchema(BaseModel):
    descricao: str
    dataGasto: date
    valor: float
    morador_id: int

class GastoViewSchema(BaseModel):
    id: int
    descricao: str
    dataGasto: date
    valor: float
    morador_id: int

class ListaGastosSchema(BaseModel):
    gastos: List[GastoViewSchema]

class MessageSchema(BaseModel):
    message: str

class IdGastoSchema(BaseModel):
    id: int

class EstadoFinanceiroSchema(BaseModel):
    id: int
    nome: str
    salario: float
    total_gastos_mes: float
    saldo_atual: float

class ListaEstadoFinanceiroSchema(BaseModel):
    situacao: List[EstadoFinanceiroSchema]