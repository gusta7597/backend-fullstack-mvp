from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.morador import Base as BaseMorador
from model.gasto import Base as BaseGasto

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

def criar_base():
    BaseMorador.metadata.create_all(engine)
    BaseGasto.metadata.create_all(engine)
