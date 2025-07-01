from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError
from database import Session
from model.morador import Morador
from schemas.morador import (
    MoradorSchema,
    MoradorViewSchema,
    ListaMoradoresSchema,
    ErrorSchema,
    MessageSchema,
    IdMoradorSchema
)

morador_routes = APIBlueprint(
    'morador',
    __name__,
    url_prefix='/moradores',
    abp_tags=[Tag(name="Morador", description="Operações relacionadas aos moradores")]
)

@morador_routes.post(
    '',
    summary="Criar morador",
    description="Cria um novo morador com nome e salário.",
    responses={
        "200": MoradorViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema
    }
)
def criar_morador(form: MoradorSchema):
    """Criação de um novo morador"""
    session = Session()
    morador = Morador(nome=form.nome, salario=form.salario)
    try:
        session.add(morador)
        session.commit()
        return {
            "id": morador.id,
            "nome": morador.nome,
            "salario": morador.salario
        }
    except IntegrityError:
        session.rollback()
        return {"message": "Morador com esse nome já existe."}, 409
    except:
        session.rollback()
        return {"message": "Erro ao criar morador."}, 400

@morador_routes.get(
    '',
    summary="Listar moradores",
    description="Retorna uma lista com todos os moradores cadastrados.",
    responses={
        "200": ListaMoradoresSchema
    }
)
def listar_moradores():
    """Listagem de todos os moradores"""
    session = Session()
    moradores = session.query(Morador).all()
    return {
        "moradores": [
            {"id": m.id, "nome": m.nome, "salario": m.salario} for m in moradores
        ]
    }

@morador_routes.get(
    '/<int:id>',
    summary="Obter morador por ID",
    description="Retorna os dados de um morador específico pelo seu ID.",
    responses={
        "200": MoradorViewSchema,
        "404": ErrorSchema
    }
)
def obter_morador(path: IdMoradorSchema):
    """Busca um morador pelo ID"""
    session = Session()
    morador = session.query(Morador).filter(Morador.id == path.id).first()
    if not morador:
        return {"message": "Morador não encontrado."}, 404
    return {
        "id": morador.id,
        "nome": morador.nome,
        "salario": morador.salario
    }

@morador_routes.delete(
    '/<int:id>',
    summary="Deletar morador",
    description="Remove um morador do sistema com base no ID.",
    responses={
        "200": MessageSchema,
        "404": ErrorSchema
    }
)
def deletar_morador(path: IdMoradorSchema):
    """Exclusão de um morador pelo ID"""
    session = Session()
    morador = session.query(Morador).filter(Morador.id == path.id).first()
    if not morador:
        return {"message": "Morador não encontrado."}, 404
    session.delete(morador)
    session.commit()
    return {"message": "Morador deletado com sucesso."}
