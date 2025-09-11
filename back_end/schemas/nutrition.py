from ma import ma
from back_end.models.nutrition import NutritionModel

class NutritionSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = NutritionModel
    load_instance = True