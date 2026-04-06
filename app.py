from flask_cors import CORS
from ma import ma
from db import db
from back_end.server.instance import server
from back_end.controllers import pacientes  # importa para registrar o namespace
from back_end.controllers.historico import historico_ns

# inicializando API e APP
api = server.api
app = server.app

# Habilita CORS de forma global, com a sua configuração perfeita!
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

if __name__ == '__main__':
    # primeiro registra o app no SQLAlchemy e no Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # depois cria as tabelas no contexto do app
    with app.app_context():
        db.create_all()

    # inicia o servidor Flask
    app.run(debug=True, port=5000)