# Compartilhamento Publico de Pacientes - Backend

## Explicacao Tecnica

### Arquitetura

O sistema de compartilhamento permite gerar links publicos (read-only) para que pacientes visualizem seus proprios dados. A solucao utiliza uma tabela auxiliar `share_tokens` no banco de dados para armazenar tokens UUID opacos.

### Modelo: ShareTokenModel

**Arquivo:** `back_end/models/share_token.py`

Tabela `share_tokens` com os seguintes campos:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `id` | Integer (PK) | Identificador unico do token |
| `token` | String(36) | UUID v4 gerado automaticamente — usado na URL publica |
| `paciente_id` | Integer (FK) | Referencia ao paciente na tabela `nutrition` |
| `created_at` | DateTime | Data/hora de criacao (UTC) |
| `expires_at` | DateTime (nullable) | Data/hora de expiracao. `NULL` = nunca expira |
| `is_active` | Boolean | `True` = ativo, `False` = revogado |
| `access_count` | Integer | Contador de acessos ao link |
| `label` | String(100) (nullable) | Rotulo opcional para identificar o link |

**Decisoes:**
- UUID v4 garante 122 bits de aleatoriedade — impossivel adivinhar tokens
- O ID inteiro do paciente nunca aparece na URL publica
- `backref` no relacionamento injeta `share_tokens` no NutritionModel sem modifica-lo
- Propriedades computadas `is_expired` e `is_valid` facilitam a validacao

### Endpoints

**Namespace admin (`share_ns`)** — montado em `/api/nutrition`:

| Metodo | Rota | Descricao |
|--------|------|-----------|
| `POST` | `/api/nutrition/{id}/share` | Gera novo token. Body: `{ "expires_in_days": 30, "label": "..." }` (ambos opcionais) |
| `GET` | `/api/nutrition/{id}/shares` | Lista tokens do paciente. Query: `?active_only=true` |
| `DELETE` | `/api/nutrition/{id}/share/{token_id}` | Revoga um token especifico |

**Namespace publico (`public_ns`)** — montado em `/api/public`:

| Metodo | Rota | Descricao |
|--------|------|-----------|
| `GET` | `/api/public/paciente/{token}` | Retorna dados completos do paciente (read-only) |

### Respostas do endpoint publico

| Cenario | HTTP Status | Corpo |
|---------|------------|-------|
| Token valido | 200 | Dados completos do paciente (mesmo formato do `GET /api/nutrition/{id}`) |
| Token nao encontrado | 404 | `{ "erro": "Link invalido ou nao encontrado." }` |
| Token revogado | 410 | `{ "erro": "Este link foi revogado." }` |
| Token expirado | 410 | `{ "erro": "Este link expirou." }` |
| Paciente deletado | 404 | `{ "erro": "Dados do paciente nao disponiveis." }` |

### Seguranca

- **Read-only enforced**: o namespace publico possui SOMENTE 1 endpoint GET. Nenhuma operacao de escrita e possivel.
- **Isolamento**: cada token aponta para exatamente 1 paciente. Nao e possivel enumerar ou acessar dados de outros pacientes.
- **Revogacao imediata**: setar `is_active = False` invalida o token instantaneamente.
- **Sem dependencias novas**: usa apenas `uuid` da stdlib do Python e SQLAlchemy.
- **CORS**: a configuracao existente (`/api/*` → `*`) ja cobre `/api/public/*`.

---

## Arquivos Criados/Modificados

| Arquivo | Acao | Descricao |
|---------|------|-----------|
| `back_end/models/share_token.py` | Novo | Modelo da tabela `share_tokens` |
| `back_end/schemas/share_token.py` | Novo | Schema Marshmallow para serializacao |
| `back_end/controllers/share.py` | Novo | Controller com 2 namespaces (admin + publico) |
| `back_end/server/instance.py` | Modificado | Registro dos novos namespaces |
| `app.py` | Modificado | Import do ShareTokenModel (garante criacao da tabela) |
| `wsgi.py` | Modificado | Import do ShareTokenModel (garante criacao da tabela) |

---

## Passo a Passo

### 1. A tabela e criada automaticamente

O `db.create_all()` ja existente em `app.py` e `wsgi.py` cria a tabela `share_tokens` automaticamente na primeira execucao.

### 2. Verificar novos endpoints no Swagger

Acesse `http://localhost:5000/api/doc` — os novos endpoints aparecem nos namespaces `share` e `public`.

### 3. Testar geracao de link

```bash
curl -X POST http://localhost:5000/api/nutrition/1/share \
  -H "Content-Type: application/json" \
  -d '{"expires_in_days": 30, "label": "Link para Maria"}'
```

### 4. Testar acesso publico

```bash
curl http://localhost:5000/api/public/paciente/{token-uuid-retornado}
```

### 5. Testar revogacao

```bash
# Listar tokens
curl http://localhost:5000/api/nutrition/1/shares

# Revogar
curl -X DELETE http://localhost:5000/api/nutrition/1/share/{token_id}

# Verificar que acesso publico retorna 410
curl http://localhost:5000/api/public/paciente/{token-uuid}
```

---

## Troubleshooting

| Problema | Causa provavel | Solucao |
|----------|---------------|---------|
| Tabela `share_tokens` nao existe | `db.create_all()` nao foi executado apos o import do modelo | Verifique que `from back_end.models.share_token import ShareTokenModel` esta em `app.py`/`wsgi.py` |
| Endpoint retorna 404 para token valido | Paciente foi deletado | O cascade delete do SQLAlchemy remove os tokens junto com o paciente. Esperado. |
| Namespace nao aparece no Swagger | `instance.py` nao registrou os namespaces | Verifique que `share_ns` e `public_ns` foram adicionados com `add_namespace` |
| Token igual para pacientes diferentes | Improvavel (UUID4 tem probabilidade de colisao ~1 em 2^122) | Se ocorrer, gere outro token |
