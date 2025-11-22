# Nexus Education - Backend

Backend API para o sistema Nexus Education, desenvolvido com FastAPI, Python e Poetry.

## Configuração

### 1. Instalar Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Ou usando pip
pip install poetry
```

### 2. Instalar dependências

```bash
cd Back-end
poetry install
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
- `SUPABASE_URL`: URL do seu projeto Supabase
- `SUPABASE_KEY`: Chave anon do Supabase
- `GROQ_API_KEY`: Chave API do Groq
- `JWT_SECRET_KEY`: Chave secreta para JWT (gere uma string aleatória segura)
- `CORS_ORIGINS`: Origens permitidas (separadas por vírgula)

### 4. Configurar banco de dados no Supabase

Crie as seguintes tabelas no Supabase:

#### Tabela `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Tabela `analyses`
```sql
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_name VARCHAR(255) NOT NULL,
  analysis_detail TEXT NOT NULL,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, student_name)
);
```

### 5. Executar servidor

```bash
poetry run uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`

## Endpoints

### Autenticação

- `POST /api/auth/register` - Cadastro de usuário
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Informações do usuário autenticado

### Análises

- `POST /api/analysis/upload` - Upload e análise de ementa (PDF)
- `GET /api/analysis/` - Listar todas as análises
- `GET /api/analysis/{id}` - Buscar análise específica

## Documentação

A documentação interativa está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

