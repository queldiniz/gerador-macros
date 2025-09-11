from db import db

class NutritionModel(db.Model):
    # Nome da tabela no banco de dados
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

    # Construtor da classe
    def __init__(self, name, height, weight, age, gender, activity_level, calories=None, body_percentage=None):
        self.name = name
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.activity_level = activity_level
        self.calories = calories
        self.body_percentage = body_percentage

    # Representação da classe em formato string (para debug)
    def __repr__(self):
        return (
            f'<Nutrition {self.name}, {self.height}, {self.weight}, {self.age}, '
            f'{self.gender}, {self.activity_level}, {self.calories}, {self.body_percentage}>'
        )

    # Retorna os dados em formato JSON (dicionário)
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
            'age': self.age,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'calories': self.calories,
            'body_percentage': self.body_percentage
        }

    # Métodos de consulta ao banco de dados
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # Métodos para salvar e excluir no banco de dados
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
