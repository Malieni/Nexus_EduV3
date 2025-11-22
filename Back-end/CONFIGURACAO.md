# 🔧 Guia de Configuração - Nexus Education Backend

Este guia ajudará você a configurar as variáveis de ambiente necessárias para o backend.

## 📋 Passo a Passo

### 1. Configurar Supabase

#### Criar Projeto no Supabase
1. Acesse [https://app.supabase.com](https://app.supabase.com)
2. Faça login ou crie uma conta
3. Clique em "New Project"
4. Preencha os dados do projeto:
   - **Name**: Nome do seu projeto
   - **Database Password**: Crie uma senha forte (guarde ela!)
   - **Region**: Escolha a região mais próxima
5. Aguarde alguns minutos para o projeto ser criado

#### Obter Credenciais do Supabase
1. No painel do projeto, vá em **Settings** (ícone de engrenagem) > **API**
2. Você verá duas informações importantes:
   - **Project URL**: Esta é sua `SUPABASE_URL`
   - **anon public key**: Esta é sua `SUPABASE_KEY`
3. Copie essas informações e cole no arquivo `.env`

#### Criar Tabelas no Supabase
1. No painel do Supabase, vá em **SQL Editor** (ícone de banco de dados)
2. Clique em **New Query**
3. Execute o seguinte SQL:

```sql
-- Tabela de usuários
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de análises
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_name VARCHAR(255) NOT NULL,
  analysis_detail TEXT NOT NULL,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, student_name)
);

-- Índices para melhor performance
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
```

4. Clique em **Run** para executar

### 2. Configurar Groq API

#### Criar Conta e Obter Chave
1. Acesse [https://console.groq.com](https://console.groq.com)
2. Faça login ou crie uma conta (pode usar Google/GitHub)
3. Após fazer login, vá em **API Keys**
4. Clique em **Create API Key**
5. Dê um nome para a chave (ex: "Nexus Education")
6. Copie a chave gerada (ela começa com `gsk_`)
7. Cole no arquivo `.env` como `GROQ_API_KEY`

**Importante**: A chave só será mostrada uma vez! Guarde-a com segurança.

### 3. Gerar JWT Secret Key

A chave JWT é usada para assinar os tokens de autenticação. Você precisa gerar uma string aleatória segura.

#### Opção 1: Usando PowerShell (Windows)
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

#### Opção 2: Usando Python
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Opção 3: Online
Acesse [https://www.random.org/strings/](https://www.random.org/strings/) e gere uma string de 64 caracteres alfanuméricos.

Cole o resultado no arquivo `.env` como `JWT_SECRET_KEY`

### 4. Preencher o Arquivo .env

Agora que você tem todas as credenciais, edite o arquivo `Back-end/.env`:

```env
# Substitua pelos valores reais que você obteve:

SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JWT_SECRET_KEY=sua_string_aleatoria_gerada_aqui
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
PORT=8000
```

### 5. Verificar Configuração

Para testar se tudo está configurado corretamente:

```bash
cd Back-end
poetry install
poetry run python -c "from config import settings; print('✅ Configuração carregada com sucesso!')"
```

Se aparecer alguma mensagem de erro sobre variáveis faltando, verifique o arquivo `.env`.

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- **NUNCA** compartilhe o arquivo `.env`
- **NUNCA** faça commit do `.env` no Git (ele já está no `.gitignore`)
- Mantenha suas chaves em segredo
- Se uma chave vazar, gere uma nova imediatamente

## ✅ Próximos Passos

Após configurar o `.env`:

1. Instale as dependências: `poetry install`
2. Execute o servidor: `poetry run uvicorn main:app --reload --port 8000`
3. Acesse a documentação: `http://localhost:8000/docs`

## 🆘 Problemas Comuns

### Erro: "supabase_url is required"
- Verifique se o arquivo `.env` existe na pasta `Back-end/`
- Verifique se todas as variáveis estão preenchidas
- Certifique-se de que não há espaços extras antes ou depois dos valores

### Erro ao conectar no Supabase
- Verifique se a URL e a chave estão corretas
- Certifique-se de que o projeto Supabase está ativo
- Verifique sua conexão com a internet

### Erro ao usar Groq API
- Verifique se a chave está correta e começa com `gsk_`
- Verifique se sua conta Groq tem créditos disponíveis
- Confirme que a chave não foi revogada

## 📞 Suporte

Se tiver problemas, verifique:
- Os logs do servidor
- A documentação do Supabase: https://supabase.com/docs
- A documentação do Groq: https://console.groq.com/docs

