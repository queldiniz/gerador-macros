from ma import ma
# Importando TODOS os modelos, inclusive o novo HistoricoModel!
from back_end.models.paciente import NutritionModel, RefeicaoModel, HistoricoModel

# 1. Schema das Refeições
class RefeicaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefeicaoModel
        load_instance = True
        include_fk = True

# 2. Schema do Histórico (Aqui está ele!)
class HistoricoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoricoModel
        load_instance = True
        include_fk = True

# 3. Schema do Paciente
class NutritionSchema(ma.SQLAlchemyAutoSchema):
    # O pulo do gato: traz as refeições E o histórico junto com o paciente!
    refeicoes = ma.Nested(RefeicaoSchema, many=True, dump_only=True)
    historico = ma.Nested(HistoricoSchema, many=True, dump_only=True)

    class Meta:
        model = NutritionModel
        load_instance = True
        include_fk = True