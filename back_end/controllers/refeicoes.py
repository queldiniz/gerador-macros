from flask import request
from flask_restx import Resource, fields, Namespace

# Importações dos nossos Modelos e Schemas
from back_end.models.nutrition import RefeicaoModel, NutritionModel
from back_end.schemas.nutrition import RefeicaoSchema

refeicoes_ns = Namespace('refeicoes', description='Gerenciamento da Dieta dos Pacientes')

refeicao_schema = RefeicaoSchema()

# O "molde" do que o React vai enviar para o Python
refeicao_payload = refeicoes_ns.model('RefeicaoPayload', {
    'food_name': fields.String(required=True, description='Nome do Alimento'),
    'calories': fields.Float(required=True, description='Total de Calorias'),
    'carbs': fields.Float(default=0, description='Carboidratos em gramas'),
    'protein': fields.Float(default=0, description='Proteínas em gramas'),
    'fat': fields.Float(default=0, description='Gorduras em gramas'),
    'paciente_id': fields.Integer(required=True, description='ID do paciente que receberá a comida')
})

@refeicoes_ns.route('/')
class RefeicaoList(Resource):
    
    @refeicoes_ns.doc('adicionar_refeicao')
    @refeicoes_ns.expect(refeicao_payload, validate=True)
    def post(self):
        """Adiciona um novo alimento à dieta de um paciente"""
        json_data = request.get_json()
        
        # 1. Verifica se o paciente existe antes de adicionar a comida
        paciente = NutritionModel.find_by_id(json_data.get('paciente_id'))
        if not paciente:
            return {"erro": "Paciente não encontrado. Não é possível adicionar a refeição."}, 404
            
        # 2. Transforma o JSON no nosso Objeto do Banco de Dados
        nova_refeicao = refeicao_schema.load(json_data)
        
        # 3. Salva no banco de dados!
        nova_refeicao.save_to_db()
        
        return refeicao_schema.dump(nova_refeicao), 201


@refeicoes_ns.route('/<int:id>')
class Refeicao(Resource):
    
    @refeicoes_ns.doc('deletar_refeicao')
    def delete(self, id):
        """Remove um alimento da dieta"""
        refeicao = RefeicaoModel.query.get(id)
        if not refeicao:
            return {"erro": "Refeição não encontrada."}, 404
            
        refeicao.delete_from_db()
        return '', 204