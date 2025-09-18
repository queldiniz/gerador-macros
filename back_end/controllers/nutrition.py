# controller vai receber as requisicoes e chamar os metodos do model (fazer os tratamentos necessarios)
from flask import request
from flask_restx import Resource, fields, Namespace
from back_end.models.nutrition import NutritionModel
from back_end.schemas.nutrition import NutritionSchema

# Criando namespace para organizar as rotas relacionadas com nutrition
nutrition_ns = Namespace(
    'nutrition',
    description='Registo e consulta de informações nutricionais'
)

# Schemas do Marshmallow para validar e serializar os dados
nutrition_schema = NutritionSchema()
nutritions_list_schema = NutritionSchema(many=True)

# Modelo de dados para a documentação Swagger (usado com @expect)
item_payload = nutrition_ns.model('NutritionPayload', {
    'name': fields.String(required=True, description='Nome do paciente', example='Joana Doe'),
    'height': fields.Float(required=True, description='A sua altura em metros', example=1.70),
    'weight': fields.Float(required=True, description='O seu peso em kg', example=68.5),
    'age': fields.Integer(required=True, description='A sua idade em anos', example=32),
    'gender': fields.String(required=True, description='O seu género', example=['Masculino', 'Feminino']),
    'activity_level': fields.String(required=True, description='Nível de atividade física', example=['Sedentário', 'Levemente Ativo', 'Moderadamente Ativo', 'Ativo', 'Muito Ativo']),
    'calories': fields.Float(default=0, description='Quantidade de calorias diárias consumidas'),
    'body_percentage': fields.Float(default=0, description='Percentual de gordura corporal')
})

# Modelo de dados de saída para a documentação Swagger (usado com @marshal_with)
# Herda do payload e adiciona campos que o servidor gera (id, calories, etc.)
nutrition_response_model = nutrition_ns.inherit('NutritionResponse', item_payload, {
    'id': fields.Integer(readonly=True, description='O ID único do registo')
})


# Rota para a lista de registos
@nutrition_ns.route('/')
class NutritionList(Resource):
    @nutrition_ns.doc('list_nutritions', params={'name': 'Filtra pacientes por nome (busca parcial)'})
    @nutrition_ns.marshal_list_with(nutrition_response_model)
    def get(self):
        """ Lista todos os pacientes, com opção de filtrar por nome"""
        name_query = request.args.get('name')
        if name_query:
            nutritions = NutritionModel.query.filter(NutritionModel.name.ilike(f'%{name_query}%')).all()
        else:
            nutritions = NutritionModel.find_all()
        return nutritions_list_schema.dump(nutritions), 200
        
    @nutrition_ns.doc('create_nutrition')
    @nutrition_ns.expect(item_payload, validate=True)
    @nutrition_ns.marshal_with(nutrition_response_model, code=201)
    @nutrition_ns.response(400, 'Dados de entrada inválidos')
    def post(self):
        """ Cria um novo registo de paciente"""
        nutrition_json = request.get_json()
        # Marshmallow valida os dados e retorna uma instância de NutritionModel
        nutrition_data = nutrition_schema.load(nutrition_json)
        nutrition_data.save_to_db()
        return nutrition_schema.dump(nutrition_data), 201

# Rota para um registo específico
@nutrition_ns.route('/<int:id>')
@nutrition_ns.param('id', 'O identificador do paciente')
@nutrition_ns.response(404, 'Paciente não encontrado')
class Nutrition(Resource):
    @nutrition_ns.doc('get_nutrition')
    @nutrition_ns.marshal_with(nutrition_response_model)
    def get(self, id):
        """Devolve os dados de um paciente pelo ID"""
        nutrition = NutritionModel.find_by_id(id)
        if nutrition:
            return nutrition_schema.dump(nutrition), 200
        return {'message': 'Paciente não encontrado'}, 404

    @nutrition_ns.doc('update_nutrition')
    @nutrition_ns.expect(item_payload, validate=True)
    @nutrition_ns.marshal_with(nutrition_response_model)
    @nutrition_ns.response(400, 'Dados de entrada inválidos')
    def put(self, id):
        """ Atualiza os dados de um paciente"""
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Paciente não encontrado"}, 404

        nutrition_json = request.get_json()
        updated_data = nutrition_schema.load(nutrition_json, instance=nutrition, partial=True)
        updated_data.save_to_db()
        return nutrition_schema.dump(updated_data), 200

    @nutrition_ns.doc('delete_nutrition')
    @nutrition_ns.response(204, 'Paciente apagado com sucesso')
    def delete(self, id):
        """ Apaga um paciente pelo ID"""
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Paciente não encontrado"}, 404

        nutrition.delete_from_db()
        return '', 204

