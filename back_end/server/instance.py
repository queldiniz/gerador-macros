from flask import Flask, Blueprint
from flask_restx import Api

class Server():
    def __init__(self):
        # Cria a aplicação Flask
        self.app = Flask(__name__)

        # Cria um Blueprint para isolar a API
        # url_prefix='/api' significa que todas as rotas vão começar com /api
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')

        # Cria a instância da API RESTX
        # - doc='/doc' expõe a interface Swagger em /api/doc
        # - title define o nome que aparece no Swagger
        self.api = Api(
            self.blueprint,
            doc='/doc',
            title='Aplicação de Nutrição'
        )

        # Registra o blueprint na aplicação Flask
        self.app.register_blueprint(self.blueprint)

        # Configurações do banco de dados
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  # banco SQLite
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Cria e adiciona o namespace "nutrition" à API
        self.nutrition_ns = self._nutrition_ns()
        self.api.add_namespace(self.nutrition_ns)

    def _nutrition_ns(self):
        """
        Cria um namespace específico para as rotas de nutrição.
        Esse namespace agrupa todas as rotas relacionadas
        e aparecerá organizado no Swagger (/api/doc).
        """
        return self.api.namespace(
            name='nutrition',
            description='Operações de cálculo e registro de nutrição',
            path='/nutrition'
        )

    def run(self):
        """
        Inicia o servidor Flask, ouvindo em todas as interfaces (0.0.0.0),
        na porta 5000, com debug ativado.
        """
        self.app.run(
            port=5000,
            debug=True,
            host='0.0.0.0'
        )

# Cria uma instância única do servidor (singleton)
server = Server()
