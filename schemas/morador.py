from pydantic import BaseModel
from typing import List

class MoradorSchema(BaseModel):
    nome: str
    salario: float

class MoradorViewSchema(BaseModel):
    id: int
    nome: str
    salario: float

class ListaMoradoresSchema(BaseModel):
    moradores: List[MoradorViewSchema]

class ErrorSchema(BaseModel):
    message: str
    
class MessageSchema(BaseModel):
    message: str

class IdMoradorSchema(BaseModel):
    id: int