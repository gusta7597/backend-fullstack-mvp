from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from database import criar_base
from routes.morador_routes import morador_routes
from routes.gasto_routes import gasto_routes
from flask_cors import CORS

info = Info(title="API de Moradores e Gastos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins="*", allow_headers="*")

# Redireciona para documentação
@app.get('/', tags=[Tag(name="Documentação", description="Redireciona para Swagger")])
def home():
    return redirect('/openapi')

# Cria o banco de dados
criar_base()

# Registra as rotas
app.register_api(morador_routes)
app.register_api(gasto_routes)
