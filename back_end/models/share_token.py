import uuid
from datetime import datetime
from db import db


class ShareTokenModel(db.Model):
    """
    Tabela auxiliar para links de compartilhamento publico de pacientes.
    Cada registro representa um link unico que permite visualizar (read-only)
    os dados de um paciente sem autenticacao.
    """
    __tablename__ = 'share_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False, index=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('nutrition.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # None = nunca expira
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    access_count = db.Column(db.Integer, default=0, nullable=False)
    label = db.Column(db.String(100), nullable=True)

    # Relacionamento reverso — NutritionModel NAO e modificado (backref injeta automaticamente)
    paciente = db.relationship('NutritionModel', backref=db.backref('share_tokens', lazy=True, cascade="all, delete-orphan"))

    def __init__(self, paciente_id, expires_at=None, label=None):
        self.token = str(uuid.uuid4())
        self.paciente_id = paciente_id
        self.expires_at = expires_at
        self.label = label

    @property
    def is_expired(self):
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self):
        return self.is_active and not self.is_expired

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def find_active_by_paciente(cls, paciente_id):
        return cls.query.filter_by(paciente_id=paciente_id, is_active=True).all()

    @classmethod
    def find_all_by_paciente(cls, paciente_id):
        return cls.query.filter_by(paciente_id=paciente_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def revoke(self):
        self.is_active = False
        db.session.commit()

    def increment_access(self):
        self.access_count += 1
        db.session.commit()