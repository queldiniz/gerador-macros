from ma import ma
from back_end.models.nutrition import NutritionModel, RefeicaoModel

# 1. Primeiro criamos o Schema da Refeição
class RefeicaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefeicaoModel
        load_instance = True
        ordered = True
        include_fk = True # Isso garante que o ID do paciente apareça no JSON da comida

# 2. Depois atualizamos o Schema do Paciente
class NutritionSchema(ma.SQLAlchemyAutoSchema):
    # O Pulo do Gato: Isso faz com que as refeições venham junto com os dados do paciente!
    refeicoes = ma.Nested(RefeicaoSchema, many=True, dump_only=True)

    class Meta:
        model = NutritionModel
        load_instance = True
        ordered = True