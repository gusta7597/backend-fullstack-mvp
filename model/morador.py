from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, declarative_base

from model import Base

class Morador(Base):
    __tablename__ = 'moradores'

    id = Column("id",Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    salario = Column(Float, nullable=False)

    gastos = relationship("Gasto", back_populates="morador", cascade="all, delete-orphan")
