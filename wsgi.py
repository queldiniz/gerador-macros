from flask_cors import CORS
from ma import ma
from db import db
from back_end.server.instance import server
from back_end.controllers import pacientes
from back_end.controllers.historico import historico_ns
from back_end.models.share_token import ShareTokenModel  # garante criacao da tabela
from flask import redirect  
api = server.api
app = server.app


# Garante que o Docker (Gunicorn) redirecione a raiz para o Swagger
@app.route('/')
def home_redirect():
    return redirect('/api/doc')

CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()