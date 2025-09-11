from flask_cors import CORS
from ma import ma
from db import db
from back_end.server.instance import server
from back_end.controllers import nutrition  # importa para registrar o namespace

# inicializando API e APP
api = server.api
app = server.app

if __name__ == '__main__':
    # primeiro registra o app no SQLAlchemy e no Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # depois cria as tabelas no contexto do app
    with app.app_context():
        db.create_all()

    # habilita CORS
    CORS(app)

    # inicia o servidor Flask
    app.run(debug=True, port=5000)
