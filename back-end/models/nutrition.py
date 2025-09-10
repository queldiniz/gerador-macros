from db import db

class NutritionModel(db.Model):
  __tablename_ = 'nutrition'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  height = db.Column(db.Float(precision=2), nullable=False)
  weight = db.Column(db.Float(precision=2), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.String(10), nullable=False)
  activity_level = db.Column(db.String(20), nullable=False)

  #informações opcionais, podem ser nulas
  calories = db.Column(db.Float(precision=2))
  body_percentage = db.Column(db.Float(precision=2))

  def __init__(self, name, height, weight, age, gender, activity_level, calories=None, body_percentage=None):
    self.name = name
    self.height = height
    self.weight = weight
    self.age = age

  def _repr__(self):
    return f'<Nutrition {self.name}, {self.height}, {self.weight}, {self.age}, {self.gender}, {self.activity_level}, {self.calories}, {self.body_percentage}>'  
  
  def json(self):
    return {
      'id': self.id,
      'name': self.name,
      'height': self.height,
      'weight': self.weight,
      'age': self.age,
      'gender':self.gender,
      'activity_level': self.activity_level,
      'calories': self.calories, 
      'body_percentage': self.body_percentage
    } 
  
  #Métodos da Classe NutritionModel
  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()
  
  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()
  
  #Para pegar todos os registros do banco de dados
  @classmethod
  def find_all(cls):
    return cls.query.all()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
    #continuar aqui