# Nexus Education

Sistema completo para análise de ementas acadêmicas utilizando inteligência artificial.

## 🚀 Tecnologias

### Backend
- **Python** com **Poetry** para gerenciamento de dependências
- **FastAPI** para API REST
- **Supabase** para banco de dados
- **Groq API** para análise de PDFs com IA
- **PyPDF2** para extração de texto de PDFs

### Frontend
- **React** com **Vite**
- **React Router** para navegação
- **Axios** para requisições HTTP

### Hospedagem
- **Vercel** para publicação

## 📋 Funcionalidades

- ✅ Autenticação completa (Login/Cadastro)
- ✅ Controle de acesso e sessão
- ✅ Upload de PDFs (ementas)
- ✅ Análise automática com IA (Groq)
- ✅ Histórico de análises
- ✅ Dashboard com estatísticas
- ✅ Menu lateral com configurações e políticas
- ✅ Sistema evita reanálise do mesmo aluno

## 🛠️ Instalação

### Backend

```bash
cd Back-end
poetry install
cp .env.example .env
# Edite o .env com suas credenciais
poetry run uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd Front-end
npm install
cp .env.example .env
# Edite o .env com a URL da API
npm run dev
```

## 📦 Configuração do Supabase

Crie as seguintes tabelas no Supabase:

### Tabela `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Tabela `analyses`
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

## 🔑 Variáveis de Ambiente

### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret_key
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 📝 Como Usar

1. **Cadastro/Login**: Acesse a aplicação e faça login ou cadastre-se
2. **Upload de Ementa**: Na área principal, envie um PDF com a ementa do aluno
3. **Análise Automática**: O sistema analisará o PDF usando IA
4. **Histórico**: Visualize todas as análises realizadas na tabela
5. **Detalhes**: Clique em "Ver Detalhes" para ver a análise completa

## 🌐 Publicação no Vercel

### Backend
Configure as variáveis de ambiente no Vercel e publique.

### Frontend
```bash
cd Front-end
npm run build
# Publique a pasta dist/ no Vercel
```

## 📚 Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API.

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Autenticação JWT
- Validação de rotas privadas
- CORS configurado

## 📄 Licença

Este projeto é privado e proprietário.

