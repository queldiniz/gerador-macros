# controller vai receber as requisicoes e chamar os metodos do model (fazer os tratamentos necessarios)
from flask import request
from flask_restx import Resource, fields, Namespace

# Importações dos seus modelos e schemas
from back_end.models.nutrition import NutritionModel
from back_end.schemas.nutrition import NutritionSchema

# Criando namespace para organizar as rotas relacionadas com nutrition
nutrition_ns = Namespace(
    'nutrition',
    description='Registro e consulta de informações nutricionais'
)

# Schemas do Marshmallow para validar e serializar os dados
nutrition_schema = NutritionSchema()
nutritions_list_schema = NutritionSchema(many=True)


# Modelo de dados para o payload de entrada (usado com @expect)
item_payload = nutrition_ns.model('NutritionPayload', {
    'name': fields.String(
        required=True,
        description='Nome do paciente',
        example='Joana Doe',
        pattern='^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    ),
    'height': fields.Float(
        required=True,
        description='A sua altura em metros',
        example=1.70,
        min=0.5,
        max=3.0
    ),
    'weight': fields.Float(
        required=True,
        description='O seu peso em kg',
        example=68.5,
        min=1.0,
        max=300.0
    ),
    'age': fields.Integer(
        required=True,
        description='A sua idade em anos',
        example=32,
        min=1,
        max=120
    ),
    'gender': fields.String(
        required=True,
        description='O seu género',
        example='Feminino',
        enum=['Masculino', 'Feminino']
    ),
    'activity_level': fields.String(
        required=True,
        description='Nível de atividade física',
        example='Moderadamente Ativo',
        enum=['Sedentário', 'Levemente Ativo', 'Moderadamente Ativo', 'Ativo', 'Muito Ativo']
    ),
    'calories': fields.Float(
        default=0,
        description='Quantidade de calorias diárias consumidas',
        min=0
    ),
    'body_percentage': fields.Float(
        default=0,
        description='Percentual de gordura corporal',
        min=0,
        max=100
    )
})

# Modelo de dados para a resposta de sucesso (usado com @marshal_with)
nutrition_response_model = nutrition_ns.inherit('NutritionResponse', item_payload, {
    'id': fields.Integer(readonly=True, description='O ID único do registro')
})


# Modelo de dados para respostas de erro
not_found_error_model = nutrition_ns.model('NotFoundError', {
    'message': fields.String(description='Mensagem de erro indicando que o recurso não foi encontrado')
})

validation_error_model = nutrition_ns.model('ValidationError', {
    'message': fields.String(description='Mensagem de erro geral da validação'),
    'errors': fields.Nested(
        nutrition_ns.model('ValidationErrorsDetails', {
            'campo_com_erro': fields.List(fields.String)
        }),
        description='Detalhes dos erros de validação por campo'
    )
})



# Exemplo de payload para o Swagger UI
nutrition_example_payload = {
    'name': 'Joana Doe',
    'height': 1.70,
    'weight': 68.5,
    'age': 32,
    'gender': 'Feminino',
    'activity_level': 'Moderadamente Ativo',
}

# Definição dos recursos (endpoints) da API
@nutrition_ns.route('/')
class NutritionList(Resource):
    @nutrition_ns.doc('list_nutritions', params={'name': 'Filtra pacientes por nome (busca parcial)'})
    @nutrition_ns.response(
        200,
        'Lista de pacientes',
        nutrition_response_model,
        example=[{**nutrition_example_payload, 'id': 1}, {**nutrition_example_payload, 'id': 2}]
    )
    @nutrition_ns.marshal_list_with(nutrition_response_model)
    def get(self):
        """Lista todos os pacientes"""
        name_query = request.args.get('name')
        if name_query:
            nutritions = NutritionModel.query.filter(NutritionModel.name.ilike(f'%{name_query}%')).all()
        else:
            nutritions = NutritionModel.find_all()
        return nutritions_list_schema.dump(nutritions), 200

    @nutrition_ns.doc('create_nutrition')
    @nutrition_ns.expect(item_payload, validate=True, example=nutrition_example_payload)
    @nutrition_ns.response(
        201,
        'Paciente criado com sucesso',
        nutrition_response_model,
        example={**nutrition_example_payload, 'id': 1}
    )
    @nutrition_ns.response(
        400,
        'Requisição inválida (campos faltando ou com erros)',
        validation_error_model,
        example={'message': 'Input payload validation failed', 'errors': {'age': ['Must be between 1 and 120.']}}
    )
    @nutrition_ns.marshal_with(nutrition_response_model, code=201)
    def post(self):
        """Cria um novo registro de paciente"""
        nutrition_json = request.get_json()
        nutrition_data = nutrition_schema.load(nutrition_json)
        nutrition_data.save_to_db()
        return nutrition_schema.dump(nutrition_data), 201


@nutrition_ns.route('/<int:id>')
@nutrition_ns.param('id', 'O identificador do paciente')
class Nutrition(Resource):
    @nutrition_ns.doc('get_nutrition')
    @nutrition_ns.response(
        200,
        'Paciente encontrado',
        nutrition_response_model,
        example={**nutrition_example_payload, 'id': 1}
    )
    @nutrition_ns.response(
        404,
        'Paciente não encontrado',
        not_found_error_model,
        example={'message': 'Paciente não encontrado'}
    )
    def get(self, id):
        """Obtém um paciente por ID"""
        nutrition = NutritionModel.find_by_id(id)
        if nutrition:
            return nutrition_schema.dump(nutrition), 200
        return {'message': 'Paciente não encontrado'}, 404

    @nutrition_ns.doc('update_nutrition')
    @nutrition_ns.expect(item_payload, validate=True, example=nutrition_example_payload)
    @nutrition_ns.response(
        200,
        'Paciente atualizado com sucesso',
        nutrition_response_model,
        example={**nutrition_example_payload, 'id': 1}
    )
    @nutrition_ns.response(
        400,
        'Requisição inválida',
        validation_error_model,
        example={'message': 'Input payload validation failed', 'errors': {'height': ['Must be a valid number.']}}
    )
    @nutrition_ns.response(
        404,
        'Paciente não encontrado',
        not_found_error_model,
        example={'message': 'Paciente não encontrado'}
    )
    def put(self, id):
        """Atualiza um registro de paciente existente"""
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Paciente não encontrado"}, 404

        nutrition_json = request.get_json()
        updated_data = nutrition_schema.load(nutrition_json, instance=nutrition, partial=True)
        updated_data.save_to_db()
        return nutrition_schema.dump(updated_data), 200

    @nutrition_ns.doc('delete_nutrition')
    @nutrition_ns.response(
        204,
        'Paciente apagado com sucesso'
    )
    @nutrition_ns.response(
        404,
        'Paciente não encontrado',
        not_found_error_model,
        example={'message': 'Paciente não encontrado'}
    )
    def delete(self, id):
        """Apaga um registro de paciente"""
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Paciente não encontrado"}, 404

        nutrition.delete_from_db()
        return '', 204
