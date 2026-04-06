# Docker - gerador-macros (Backend)

## Explicacao Tecnica

### Dockerfile

- **Imagem base**: `python:3.12-slim` (~150MB). A versao `slim` remove ferramentas de compilacao e documentacao desnecessarias, reduzindo o tamanho da imagem significativamente comparado a `python:3.12` (~1GB).
- **Camadas otimizadas**: O `requirements.txt` e copiado e instalado antes do codigo da aplicacao. Isso garante que a camada de dependencias fique em cache do Docker — se apenas o codigo mudar, o `pip install` nao e re-executado.
- **Gunicorn**: Servidor WSGI de producao que substitui o servidor embutido do Flask (`app.run()`). Roda com 2 workers paralelos, permitindo processar multiplas requisicoes simultaneamente. Se um worker crashar, o gunicorn reinicia outro automaticamente.
- **wsgi.py**: Ponto de entrada para o gunicorn. Replica a logica de inicializacao do `app.py` (CORS, SQLAlchemy, Marshmallow, criacao de tabelas) e expoe o objeto `app` no nivel de modulo, que e o que o gunicorn importa.

### Como o container executa

1. O gunicorn importa `wsgi:app`
2. O `wsgi.py` inicializa CORS, SQLAlchemy e Marshmallow
3. As tabelas do banco sao criadas automaticamente (se nao existirem)
4. O servidor escuta na porta 5000 com 2 workers

---

## docker-compose.yml

| Configuracao      | Descricao                                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **build context** | `.` (raiz do repositorio)                                                                                              |
| **porta**         | `5000:5000` — mapeia a porta do container para o host                                                                  |
| **env_file**      | `.env` — carrega `FATSECRET_CLIENT_ID` e `FATSECRET_CLIENT_SECRET`                                                     |
| **volume**        | `sqlite-data:/app/instance` — volume nomeado que persiste o arquivo `data.sqlite3` entre restarts e rebuilds           |
| **healthcheck**   | Verifica se a API responde em `/api/doc` a cada 30s. O container so e considerado "healthy" apos responder com sucesso |
| **restart**       | `unless-stopped` — reinicia automaticamente se o container parar inesperadamente                                       |

---

## Passo a Passo

### 1. Configurar o .env

Certifique-se de que o arquivo `.env` existe na raiz do repositorio com as credenciais da API FatSecret:

```
FATSECRET_CLIENT_ID=seu_client_id
FATSECRET_CLIENT_SECRET=seu_client_secret
```

### 2. Subir o container

```bash
docker compose up --build
```

O flag `--build` garante que a imagem seja reconstruida. Nas proximas vezes, se nao houver mudancas, pode usar apenas `docker compose up`.

### 3. Verificar que esta funcionando

- Acesse o Swagger: http://localhost:5000/api/doc
- Teste um endpoint: `curl http://localhost:5000/api/nutrition/`

### 4. Parar o container

```bash
docker compose down
```

Os dados do SQLite **persistem** no volume `sqlite-data` mesmo apos `docker compose down`.

### 5. Limpar tudo (incluindo dados)

```bash
docker compose down -v
```

O flag `-v` remove os volumes, apagando o banco de dados.

---

## Troubleshooting

| Problema                                     | Causa provavel                      | Solucao                                                                                                                                                     |
| -------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Error: port 5000 already in use`            | Outra aplicacao usando a porta 5000 | Pare o processo que usa a porta ou altere o mapeamento no `docker-compose.yml` para `"5001:5000"`                                                           |
| `FileNotFoundError: .env`                    | Arquivo `.env` nao existe           | Crie o arquivo `.env` com as credenciais do FatSecret                                                                                                       |
| `pip install` falha com caracteres estranhos | `requirements.txt` em UTF-16        | O arquivo ja foi corrigido para UTF-8. Se voltar a acontecer, salve o arquivo como UTF-8 no seu editor                                                      |
| Banco de dados vazio apos primeiro build     | Volume Docker criado vazio          | Normal no primeiro uso. Os dados existentes no `instance/data.sqlite3` local nao migram automaticamente. Para migrar, copie o arquivo para dentro do volume |
| Busca de alimentos nao funciona              | Credenciais FatSecret invalidas     | Verifique as variaveis `FATSECRET_CLIENT_ID` e `FATSECRET_CLIENT_SECRET` no `.env`                                                                          |
