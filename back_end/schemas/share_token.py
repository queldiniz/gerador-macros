from ma import ma
from marshmallow import fields as mm_fields
from back_end.models.share_token import ShareTokenModel


class ShareTokenSchema(ma.SQLAlchemyAutoSchema):
    # Campos computados do modelo (propriedades @property)
    is_expired = mm_fields.Boolean(dump_only=True)
    is_valid = mm_fields.Boolean(dump_only=True)

    class Meta:
        model = ShareTokenModel
        load_instance = True
        include_fk = True
        dump_only = ('id', 'token', 'created_at', 'access_count')
