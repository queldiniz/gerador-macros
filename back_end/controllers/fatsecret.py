import requests
from flask import request
from flask_restx import Resource, Namespace

from dotenv import load_dotenv 
import os 
load_dotenv()

# Cria um novo agrupamento no seu Swagger chamado alimentos
ns = Namespace('alimentos', description='Consultas na API da FatSecret')

# Suas chaves de acesso geradas na plataforma
FATSECRET_CLIENT_ID = os.environ.get("FATSECRET_CLIENT_ID")
FATSECRET_CLIENT_SECRET = os.environ.get("FATSECRET_CLIENT_SECRET")

@ns.route('/buscar')
class FatSecretSearch(Resource):
    @ns.doc(params={'pesquisa': 'Nome do alimento (ex: Tapioca)'})
    def get(self):
        """Busca um alimento e seus macros na base de dados da FatSecret"""
        alimento = request.args.get('pesquisa')
        
        if not alimento:
            return {"erro": "Por favor, digite um alimento para pesquisar."}, 400

        # 1. Solicita a permissão (Token de Acesso)
        token_url = "https://oauth.fatsecret.com/connect/token"
        token_data = {"grant_type": "client_credentials"}
        
        try:
            token_response = requests.post(
                token_url, 
                data=token_data, 
                auth=(FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET)
            )
            token_response.raise_for_status()
            access_token = token_response.json().get("access_token")
            
            # 2. Faz a busca do alimento com a permissão concedida
            search_url = "https://platform.fatsecret.com/rest/server.api"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            search_params = {
                "method": "foods.search",
                "search_expression": alimento,
                "format": "json",
                "max_results": 5,
                "region": "BR",
                "language": "pt" # Traz os 5 resultados mais relevantes
            }
            
            food_response = requests.post(search_url, headers=headers, data=search_params)
            food_response.raise_for_status()
            
            # Devolve os dados prontos para o React
            return food_response.json(), 200

        except Exception as e:
            return {"erro": "Falha ao consultar a API externa", "detalhes": str(e)}, 500