from flask import request
from flask_restx import Resource, fields, Namespace

# Importações dos nossos Modelos e Schemas
from back_end.models.paciente import HistoricoModel, NutritionModel
from back_end.schemas.paciente import HistoricoSchema

historico_ns = Namespace('historico', description='Gerenciamento da Evolução dos Pacientes')

historico_schema = HistoricoSchema()

# Modelo do que o React vai enviar para o Python
historico_payload = historico_ns.model('HistoricoPayload', {
    'data_registro': fields.String(required=True, description='Mês da avaliação. Ex: Jan/2026'),
    'peso': fields.Float(required=True, description='Peso do paciente em kg'),
    'gordura': fields.Float(required=True, description='Percentual de gordura'),
    'paciente_id': fields.Integer(required=True, description='ID do paciente')
})

@historico_ns.route('/')
class HistoricoList(Resource):
    
    @historico_ns.doc('adicionar_historico')
    @historico_ns.expect(historico_payload, validate=True)
    def post(self):
        """Adiciona uma nova avaliação ao histórico do paciente"""
        json_data = request.get_json()
        
        try:
            # 1. Verificar se o paciente existe
            paciente = NutritionModel.find_by_id(json_data.get('paciente_id'))
            if not paciente:
                return {"erro": "Paciente não encontrado."}, 404
                
            # 2. Transformar o JSON do Objeto do Banco de Dados
            novo_historico = historico_schema.load(json_data)
            
            # 3. Salvar no banco de dados
            novo_historico.save_to_db()
            
            return historico_schema.dump(novo_historico), 201

        except Exception as e:
            print(f"🚨 Erro interno no Python (Histórico): {e}")
            return {"erro": "Falha ao salvar histórico", "detalhes": str(e)}, 500