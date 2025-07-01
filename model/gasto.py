from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from model.morador import Morador
from datetime import date

from model import Base

class Gasto(Base):
    __tablename__ = 'gastos'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Float, nullable=False)
    dataGasto = Column(Date, nullable=False)
    morador_id = Column(Integer, ForeignKey('moradores.id'), nullable=False)

    morador = relationship("Morador", back_populates="gastos")
