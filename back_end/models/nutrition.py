from db import db

class NutritionModel(db.Model):
    """
    Esta classe representa a tabela 'nutrition' na base de dados.
    Contém a estrutura da tabela e os métodos para interagir com ela
    (criar, procurar, guardar, apagar).
    """
    # Nome da tabela na base de dados
    __tablename__ = 'nutrition'

    # Definição das colunas
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    weight = db.Column(db.Float(precision=2), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    activity_level = db.Column(db.String(20), nullable=False)

    # Informações opcionais, podem ser nulas
    calories = db.Column(db.Float(precision=2), nullable=True)
    body_percentage = db.Column(db.Float(precision=2), nullable=True)
    
    # Construtor da classe, para criar a instância a partir dos dados do controller
    def __init__(self, name, height, weight, age, gender, activity_level, **kwargs):
        self.name = name
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.activity_level = activity_level

    # Métodos de consulta à base de dados
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # Métodos para guardar e apagar na base de dados
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

