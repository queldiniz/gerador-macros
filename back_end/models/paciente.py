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
    
    objective = db.Column(db.String(50), nullable=True, default="Manutenção")
    
    # --- RELACIONAMENTOS ---
    # Liga o paciente com a dieta
    refeicoes = db.relationship('RefeicaoModel', backref='paciente', lazy=True, cascade="all, delete-orphan")
    
    #Liga o paciente com o histórico (gráficos)
    historico = db.relationship('HistoricoModel', lazy='dynamic', cascade="all, delete-orphan")

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


# TABELA: REFEIÇÕES (DIETA DO PACIENTE)
# 
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
    tipo_refeicao = db.Column(db.String(50), nullable=False)
    
    paciente_id = db.Column(db.Integer, db.ForeignKey('nutrition.id'), nullable=False)

    def __init__(self, food_name, calories, carbs, protein, fat, tipo_refeicao, paciente_id):
        self.food_name = food_name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fat = fat
        self.tipo_refeicao = tipo_refeicao
        self.paciente_id = paciente_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_paciente(cls, paciente_id):
        return cls.query.filter_by(paciente_id=paciente_id).all()



# TABELA: HISTÓRICO (EVOLUÇÃO DO PACIENTE)
# 
class HistoricoModel(db.Model):
    """
    Esta classe representa o histórico de peso e gordura do paciente para os gráficos.
    """
    __tablename__ = 'historico'

    id = db.Column(db.Integer, primary_key=True)
    data_registro = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float(precision=2), nullable=False)
    gordura = db.Column(db.Float(precision=2), nullable=False)
    
    # A Chave Estrangeira: Liga este registro ao 'id' da tabela 'nutrition'
    paciente_id = db.Column(db.Integer, db.ForeignKey('nutrition.id'), nullable=False)

    def __init__(self, data_registro, peso, gordura, paciente_id):
        self.data_registro = data_registro
        self.peso = peso
        self.gordura = gordura
        self.paciente_id = paciente_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()