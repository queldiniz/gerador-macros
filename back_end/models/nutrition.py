from db import db

class NutritionModel(db.Model):
    """
    Esta classe representa a tabela 'nutrition' (Pacientes) na base de dados.
    """
    __tablename__ = 'nutrition'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    weight = db.Column(db.Float(precision=2), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    activity_level = db.Column(db.String(20), nullable=False)
    calories = db.Column(db.Float(precision=2), nullable=True, default=0)
    body_percentage = db.Column(db.Float(precision=2), nullable=True, default=0)
    
    # NOVA LINHA: O relacionamento! 
    objective = db.Column(db.String(50), nullable=True, default="Manutenção")
    # Isso diz ao SQLAlchemy que um paciente tem várias refeições. 
    # O cascade="all, delete-orphan" apaga as refeições automaticamente se o paciente for excluído.
    refeicoes = db.relationship('RefeicaoModel', backref='paciente', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, height, weight, age, gender, activity_level, calories=0, body_percentage=0, objective="Manutenção"):
        self.name = name
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.activity_level = activity_level
        self.calories = calories
        self.body_percentage = body_percentage
        self.objective = objective


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


# ==========================================
# NOVA TABELA: REFEIÇÕES (DIETA DO PACIENTE)
# ==========================================
class RefeicaoModel(db.Model):
    """
    Esta classe representa os alimentos salvos para um paciente específico.
    """
    __tablename__ = 'refeicoes'

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(150), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=True, default=0)
    protein = db.Column(db.Float, nullable=True, default=0)
    fat = db.Column(db.Float, nullable=True, default=0)
    
    # A Chave Estrangeira: Liga este alimento ao 'id' da tabela 'nutrition'
    paciente_id = db.Column(db.Integer, db.ForeignKey('nutrition.id'), nullable=False)

    def __init__(self, food_name, calories, carbs, protein, fat, paciente_id):
        self.food_name = food_name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fat = fat
        self.paciente_id = paciente_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_paciente(cls, paciente_id):
        # Busca todas as refeições que pertencem a um paciente específico
        return cls.query.filter_by(paciente_id=paciente_id).all()