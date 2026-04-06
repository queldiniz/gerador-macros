from flask import request
from flask_restx import Resource, fields, Namespace

# Importações dos nossos Modelos e Schemas
from back_end.models.paciente import RefeicaoModel, NutritionModel
from back_end.schemas.paciente import RefeicaoSchema

refeicoes_ns = Namespace('refeicoes', description='Gerenciamento da Dieta dos Pacientes')

refeicao_schema = RefeicaoSchema()

# Modelo do que o React vai enviar para o Python
refeicao_payload = refeicoes_ns.model('RefeicaoPayload', {
    'food_name': fields.String(required=True, description='Nome do Alimento'),
    'calories': fields.Float(required=True, description='Total de Calorias'),
    'carbs': fields.Float(default=0, description='Carboidratos em gramas'),
    'protein': fields.Float(default=0, description='Proteínas em gramas'),
    'fat': fields.Float(default=0, description='Gorduras em gramas'), 
    'tipo_refeicao': fields.String(required=True, description='Ex: Café da Manhã, Almoço'),
    'paciente_id': fields.Integer(required=True, description='ID do paciente que receberá a comida')
})

@refeicoes_ns.route('')
class RefeicaoList(Resource):
    
    @refeicoes_ns.doc('adicionar_refeicao')
    @refeicoes_ns.expect(refeicao_payload, validate=True)
    def post(self):
        """Adiciona um novo alimento à dieta de um paciente"""
        json_data = request.get_json()
        
        try:
            # 1. Verifica se o paciente existe antes de adicionar a comida
            paciente = NutritionModel.find_by_id(json_data.get('paciente_id'))
            if not paciente:
                return {"erro": "Paciente não encontrado. Não é possível adicionar a refeição."}, 404
                
            # 2. Transforma o JSON no nosso Objeto do Banco de Dados
            # O Marshmallow vai ler o "tipo_refeicao" automaticamente aqui!
            nova_refeicao = refeicao_schema.load(json_data)
            
            # 3. Salva no banco de dados!
            nova_refeicao.save_to_db()
            
            # Devolve o status 201 (Created) de sucesso!
            return refeicao_schema.dump(nova_refeicao), 201

        except Exception as e:
            # Se algo der errado, imprime no terminal preto do VS Code para a gente ver!
            print(f"🚨 Erro interno no Python: {e}")
            return {"erro": "Falha ao salvar a refeição no banco de dados", "detalhes": str(e)}, 500


@refeicoes_ns.route('/<int:id>')
class Refeicao(Resource):
    
    @refeicoes_ns.doc('deletar_refeicao')
    def delete(self, id):
        """Remove um alimento da dieta"""
        refeicao = RefeicaoModel.query.get(id)
        if not refeicao:
            return {"erro": "Refeição não encontrada."}, 404
            
        refeicao.delete_from_db()
        return '', 204 # Retorna status 204 de sucesso na exclusão