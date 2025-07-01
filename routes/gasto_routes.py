from datetime import date
from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy import extract
from database import Session
from model.gasto import Gasto
from model.morador import Morador
from schemas.gasto import (
    EstadoFinanceiroSchema,
    GastoSchema,
    GastoViewSchema,
    IdGastoSchema,
    ListaEstadoFinanceiroSchema,
    ListaGastosSchema,
    MessageSchema
)
from schemas.morador import ErrorSchema, IdMoradorSchema

gasto_routes = APIBlueprint(
    'gasto',
    __name__,
    url_prefix='/gastos',
    abp_tags=[Tag(name="Gasto", description="Operações com gastos dos moradores")]
)

@gasto_routes.post(
    '',
    summary="Criar gasto",
    description="Cria um novo gasto associado a um morador.",
    responses={
        "200": GastoViewSchema,
        "400": ErrorSchema,
        "404": ErrorSchema
    }
)
def criar_gasto(form: GastoSchema):
    """Criação de um novo gasto para um morador"""
    session = Session()
    morador = session.query(Morador).filter(Morador.id == form.morador_id).first()
    if not morador:
        return {"message": "Morador não encontrado."}, 404

    gasto = Gasto(
        descricao=form.descricao,
        dataGasto=form.dataGasto,
        valor=form.valor,
        morador_id=form.morador_id
    )
    try:
        session.add(gasto)
        session.commit()
        return {
            "id": gasto.id,
            "descricao": gasto.descricao,
            "valor": gasto.valor,
            "morador_id": gasto.morador_id
        }
    except:
        session.rollback()
        return {"message": "Erro ao criar gasto."}, 400

@gasto_routes.get(
    '',
    summary="Listar todos os gastos",
    description="Retorna todos os gastos registrados no sistema.",
    responses={
        "200": ListaGastosSchema
    }
)
def listar_gastos():
    """Listagem de todos os gastos registrados"""
    session = Session()
    gastos = session.query(Gasto).all()
    return {
        "gastos": [
            {
                "id": g.id,
                "descricao": g.descricao,
                "valor": g.valor,
                "morador_id": g.morador_id,
                "data_gasto": g.dataGasto
            } for g in gastos
        ]
    }

@gasto_routes.get(
    '/morador/<int:id>',
    summary="Listar gastos de um morador",
    description="Retorna todos os gastos de um morador específico pelo ID.",
    responses={
        "200": ListaGastosSchema,
        "404": ErrorSchema
    }
)
def listar_gastos_por_morador(path: IdMoradorSchema):
    """Listagem dos gastos de um morador específico"""
    session = Session()
    morador = session.query(Morador).filter(Morador.id == path.id).first()
    if not morador:
        return {"message": "Morador não encontrado."}, 404

    return {
        "gastos": [
            {
                "id": g.id,
                "descricao": g.descricao,
                "valor": g.valor,
                "morador_id": g.morador_id,
                "data_gasto": g.dataGasto
            } for g in morador.gastos
        ]
    }

@gasto_routes.delete(
    '/<int:id>',
    summary="Deletar gasto",
    description="Exclui um gasto específico pelo ID.",
    responses={
        "200": MessageSchema,
        "404": ErrorSchema
    }
)
def deletar_gasto(path: IdGastoSchema):
    """Exclusão de um gasto pelo ID"""
    session = Session()
    gasto = session.query(Gasto).filter(Gasto.id == path.id).first()
    if not gasto:
        return {"message": "Gasto não encontrado."}, 404

    session.delete(gasto)
    session.commit()
    return {"message": "Gasto deletado com sucesso."}

@gasto_routes.get(
    '/estado-financeiro',
    summary="Estado financeiro geral",
    description="Retorna o saldo atual de todos os moradores no mês atual, com base no salário e gastos registrados.",
    responses={
        "200": ListaEstadoFinanceiroSchema,
        "404": ErrorSchema
    }
)
def estado_financeiro_geral():
    """Cálculo do estado financeiro de todos os moradores no mês atual"""
    session = Session()
    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    resultado = []

    moradores = session.query(Morador).all()
    if not moradores:
        return {"message": "Moradores não encontrados."}, 404

    for morador in moradores:
        gastos_mes = session.query(Gasto).filter(
            Gasto.morador_id == morador.id,
            extract('month', Gasto.dataGasto) == mes_atual,
            extract('year', Gasto.dataGasto) == ano_atual
        ).all()

        total_gastos = sum([g.valor for g in gastos_mes])
        saldo = morador.salario - total_gastos

        resultado.append({
            "id": morador.id,
            "nome": morador.nome,
            "salario": morador.salario,
            "total_gastos_mes": total_gastos,
            "saldo_atual": saldo
        })

    if len(resultado) == 0:
        return {"message": "Gastos não encontrados."}, 404

    return {"resultado": resultado}
