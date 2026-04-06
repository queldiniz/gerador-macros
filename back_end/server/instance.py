from flask import Flask, Blueprint
from flask_restx import Api
from back_end.controllers.pacientes import nutrition_ns
from back_end.controllers.fatsecret import ns as alimentos_ns
from back_end.controllers.refeicoes import refeicoes_ns
from back_end.controllers.historico import historico_ns
from back_end.controllers.share import share_ns, public_ns

class Server():
    def __init__(self):
        # Cria a aplicação Flask
        self.app = Flask(__name__)

        # Blueprint (todas as rotas começam com /api)
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(
            self.blueprint,
            version='1.0',
            title='API de Nutrição',
            description='Uma API para registar dados de pacientes ',
            doc='/doc'
        )

        # Regista o blueprint na aplicação Flask
        self.app.register_blueprint(self.blueprint)

        # Configurações da base de dados
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Regista o namespace importado do controller
        # O path '/nutrition' define que todas as rotas dentro do namespace começarão com /api/nutrition
        self.api.add_namespace(nutrition_ns, path='/nutrition')
        self.api.add_namespace(alimentos_ns, path='/alimentos')
        self.api.add_namespace(refeicoes_ns, path='/refeicoes')
        self.api.add_namespace(historico_ns, path='/historico')
        self.api.add_namespace(share_ns, path='/nutrition')
        self.api.add_namespace(public_ns, path='/public')

    def run(self):
        self.app.run(
            port=5000,
            debug=True,
            host='0.0.0.0'
        )

# Cria a instância única do servidor
server = Server()

