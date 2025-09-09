from flask import Flask, Blueprint
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint, doc='/doc', title='Aplicação de Nutrição')
        self.app.register_blueprint(self.blueprint)

        # Configurações do banco de dados
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Chamamos o método para criar o namespace
        self.nutrition_ns = self._nutrition_ns()
        
        # Adicionar o namespace à API
        self.api.add_namespace(self.nutrition_ns)

    def _nutrition_ns(self):
        return self.api.namespace(
            name='nutrition',
            description='Operações de cálculo e registro de nutrição',
            path='/nutrition'
        )

    def run(self):
        self.app.run(
            port=5000,
            debug=True,
            host='0.0.0.0'
        )

server = Server()