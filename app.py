from flask import jsonify
from marshmallow import ValidationError
from flask_cors import CORS

from ma import ma
from db import db
from controllers.nutrition import Nutrition, NutritionList
from server.instance import server

api = server.api
app = server.app

if __name__ == '__main__':
    # primeiro registra o app no SQLAlchemy e no Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # depois cria as tabelas no contexto do app
    with app.app_context():
        db.create_all()

    # registra as rotas da API
    api.add_resource(Nutrition, '/nutrition/<int:id>')
    api.add_resource(NutritionList, '/nutrition')

    # habilita CORS
    CORS(app)

    # inicia o servidor Flask
    app.run(debug=True, port=5000)