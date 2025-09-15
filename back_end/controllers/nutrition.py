# controller vai receber as requisicoes e chamar os metodos do model (fazer os tratamentos necessarios)
from flask import request
from flask_restx import Resource, fields
from back_end.models.nutrition import NutritionModel
from back_end.schemas.nutrition import NutritionSchema
from back_end.server.instance import server

# Criando namespace para organizar as rotas relacionadas a nutrition
nutrition_ns = server.nutrition_ns

# Schemas para validar e serializar os dados
nutrition_schema = NutritionSchema()
nutritions_list_schema = NutritionSchema(many=True)

# Definindo o modelo para Nutrition (apenas para a documentação Swagger)
item = nutrition_ns.model('Nutrition', {
    'name': fields.String(required=True, description='Nome do paciente'),
    'height': fields.Float(default=0, description='Sua altura em metros'),
    'weight': fields.Float(default=0, description='Seu peso em kg'),
    'age': fields.Integer(default=0, description='Sua idade em anos'),
    'gender': fields.String(required=True, description='Seu genero, masculino ou feminino'),
    'activity_level': fields.String(required=True, description='Nivel de atividade fisica, baixo, moderado ou alto'),
    'calories': fields.Float(default=0, description='Quantidade de calorias diarias recomendadas'),
    'body_percentage': fields.Float(default=0, description='Percentual de gordura corporal')      
})

# Rota para operações com um único registro (GET, PUT, DELETE)
@nutrition_ns.route('/<int:id>')
class Nutrition(Resource):
    def get(self, id):
        nutrition = NutritionModel.find_by_id(id)
        if nutrition:
            return nutrition_schema.dump(nutrition), 200
        return {'message': 'Paciente não encontrado'}, 404

    @nutrition_ns.expect(item)
    @nutrition_ns.doc('Update a nutrition item')
    def put(self, id):
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Nutrition not found"}, 404

        nutrition_json = request.get_json()
        if not nutrition_json:
            return {"message": "No input data provided"}, 400

        # Atualiza apenas os campos enviados
        for key, value in nutrition_json.items():
            setattr(nutrition, key, value)

        nutrition.save_to_db()
        return nutrition_schema.dump(nutrition), 200

    def delete(self, id):
        nutrition = NutritionModel.find_by_id(id)
        if not nutrition:
            return {"message": "Ops!.Paciente não encontrada"}, 404

        nutrition.delete_from_db()
        return {"message": "Paciente excluído"}, 200

# Rota para operações com múltiplos registros (GET, POST)
@nutrition_ns.route('/')
class NutritionList(Resource):
    #para pegar todos os registros
    def get(self):
        # 1. Pega o parâmetro 'name' da URL. Se não existir, será None.
        name_query = request.args.get('name')

        # 2. Se um nome foi fornecido na URL, faz uma busca filtrada
        if name_query:
            # .ilike() faz uma busca case-insensitive (não diferencia 'Beca' de 'beca')
            # Os '%' permitem buscas parciais (buscar por 'en' encontrará 'enzo')
            nutritions = NutritionModel.query.filter(NutritionModel.name.ilike(f'%{name_query}%')).all()
        else:
            # 3. Se nenhum nome foi fornecido, retorna todos os pacientes
            nutritions = NutritionModel.find_all()
        
        # 4. Retorna a lista (completa ou filtrada) para o front-end
        return nutritions_list_schema.dump(nutritions), 200
        
    @nutrition_ns.expect(item)
    @nutrition_ns.doc('Create a nutrition item')
    #para cadastrar um novo registro
    def post(self):
        nutrition_json = request.get_json()
        if not nutrition_json:
            return {"message": "No input data provided"}, 400

        # Valida e cria objeto NutritionModel
        nutrition_data = nutrition_schema.load(nutrition_json)
        nutrition_data.save_to_db()

        return nutrition_schema.dump(nutrition_data), 201