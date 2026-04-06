from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource, fields, Namespace

from back_end.models.paciente import NutritionModel
from back_end.models.share_token import ShareTokenModel
from back_end.schemas.paciente import NutritionSchema
from back_end.schemas.share_token import ShareTokenSchema

# ==========================================
# NAMESPACE 1: Gerenciamento de links (admin)
# Montado em /nutrition (mesmo prefixo, rotas distintas)
# ==========================================
share_ns = Namespace(
    'share',
    description='Gerenciamento de links de compartilhamento publico'
)

share_token_schema = ShareTokenSchema()
share_tokens_list_schema = ShareTokenSchema(many=True)

# Modelos Swagger
share_create_payload = share_ns.model('ShareCreatePayload', {
    'expires_in_days': fields.Integer(
        required=False,
        description='Dias ate o link expirar (null = nunca)',
        example=30
    ),
    'label': fields.String(
        required=False,
        description='Rotulo para identificar o link',
        example='Link para o paciente'
    )
})

share_token_response = share_ns.model('ShareTokenResponse', {
    'id': fields.Integer(description='ID do token'),
    'token': fields.String(description='UUID do link'),
    'paciente_id': fields.Integer(description='ID do paciente'),
    'created_at': fields.DateTime(description='Data de criacao'),
    'expires_at': fields.DateTime(description='Data de expiracao'),
    'is_active': fields.Boolean(description='Link ativo'),
    'access_count': fields.Integer(description='Quantidade de acessos'),
    'label': fields.String(description='Rotulo do link'),
    'is_expired': fields.Boolean(description='Se o link expirou'),
    'is_valid': fields.Boolean(description='Se o link e valido')
})


@share_ns.route('/<int:id>/share')
@share_ns.param('id', 'O identificador do paciente')
class ShareCreate(Resource):
    @share_ns.doc('create_share_link')
    @share_ns.expect(share_create_payload, validate=False)
    @share_ns.response(201, 'Link criado com sucesso', share_token_response)
    @share_ns.response(404, 'Paciente nao encontrado')
    def post(self, id):
        """Gera um novo link de compartilhamento para o paciente"""
        try:
            paciente = NutritionModel.find_by_id(id)
            if not paciente:
                return {'erro': 'Paciente nao encontrado'}, 404

            data = request.get_json(silent=True) or {}
            expires_in_days = data.get('expires_in_days')
            label = data.get('label')

            expires_at = None
            if expires_in_days and int(expires_in_days) > 0:
                expires_at = datetime.utcnow() + timedelta(days=int(expires_in_days))

            token = ShareTokenModel(
                paciente_id=id,
                expires_at=expires_at,
                label=label
            )
            token.save_to_db()

            return share_token_schema.dump(token), 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'erro': str(e)}, 500


@share_ns.route('/<int:id>/shares')
@share_ns.param('id', 'O identificador do paciente')
class ShareList(Resource):
    @share_ns.doc('list_share_links', params={
        'active_only': 'Filtrar apenas links ativos (true/false)'
    })
    @share_ns.response(200, 'Lista de links', [share_token_response])
    @share_ns.response(404, 'Paciente nao encontrado')
    def get(self, id):
        """Lista todos os links de compartilhamento do paciente"""
        paciente = NutritionModel.find_by_id(id)
        if not paciente:
            return {'erro': 'Paciente nao encontrado'}, 404

        active_only = request.args.get('active_only', 'false').lower() == 'true'

        if active_only:
            tokens = ShareTokenModel.find_active_by_paciente(id)
        else:
            tokens = ShareTokenModel.find_all_by_paciente(id)

        return share_tokens_list_schema.dump(tokens), 200


@share_ns.route('/<int:id>/share/<int:token_id>')
@share_ns.param('id', 'O identificador do paciente')
@share_ns.param('token_id', 'O ID do token a ser revogado')
class ShareRevoke(Resource):
    @share_ns.doc('revoke_share_link')
    @share_ns.response(200, 'Link revogado com sucesso')
    @share_ns.response(404, 'Token nao encontrado ou nao pertence a este paciente')
    def delete(self, id, token_id):
        """Revoga um link de compartilhamento"""
        token = ShareTokenModel.query.filter_by(id=token_id, paciente_id=id).first()
        if not token:
            return {'erro': 'Token nao encontrado ou nao pertence a este paciente'}, 404

        token.revoke()
        return {'mensagem': 'Link revogado com sucesso'}, 200


# ==========================================
# NAMESPACE 2: Acesso publico (read-only)
# Montado em /public
# ==========================================
public_ns = Namespace(
    'public',
    description='Acesso publico (read-only) aos dados do paciente via link compartilhado'
)

nutrition_schema = NutritionSchema()


@public_ns.route('/paciente/<string:token>')
@public_ns.param('token', 'O token UUID do link compartilhado')
class PublicPaciente(Resource):
    @public_ns.doc('get_public_paciente')
    @public_ns.response(200, 'Dados do paciente')
    @public_ns.response(404, 'Link invalido ou paciente nao encontrado')
    @public_ns.response(410, 'Link expirado ou revogado')
    def get(self, token):
        """Acessa os dados do paciente via link publico (somente leitura)"""
        share = ShareTokenModel.find_by_token(token)

        if not share:
            return {'erro': 'Link invalido ou nao encontrado.'}, 404

        if not share.is_active:
            return {'erro': 'Este link foi revogado.'}, 410

        if share.is_expired:
            return {'erro': 'Este link expirou.'}, 410

        # Busca o paciente
        paciente = NutritionModel.find_by_id(share.paciente_id)
        if not paciente:
            return {'erro': 'Dados do paciente nao disponiveis.'}, 404

        # Incrementa contador de acessos
        share.increment_access()

        return nutrition_schema.dump(paciente), 200
