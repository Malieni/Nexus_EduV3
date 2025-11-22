# 🔐 Problema: Não Consigo Logar Nem Cadastrar

Guia para diagnosticar e resolver problemas de autenticação após deploy.

## 🔍 Diagnóstico Passo a Passo

### 1️⃣ Verificar Erros no Navegador

1. Abra a aplicação no navegador
2. Pressione **F12** para abrir o DevTools
3. Vá na aba **Console**
4. Tente fazer login ou cadastro
5. **Veja se aparecem erros em vermelho**

**Me diga quais erros aparecem no console!**

---

### 2️⃣ Verificar CORS

**Sintomas:**
- Erro no console: `CORS policy blocked`
- `Access-Control-Allow-Origin` header is missing

**Solução:**
1. No Vercel, vá no projeto do **Backend**
2. Vá em **Settings > Environment Variables**
3. Verifique `CORS_ORIGINS`:
   - Deve incluir a URL do frontend: `https://seu-frontend.vercel.app`
   - Ou use temporariamente: `https://*.vercel.app`
4. Salve e faça um **Redeploy**

---

### 3️⃣ Verificar URL da API no Frontend

**Sintomas:**
- Erro: `Network Error` ou `Failed to fetch`
- Erro: `ERR_CONNECTION_REFUSED`

**Solução:**
1. No Vercel, vá no projeto do **Frontend**
2. Vá em **Settings > Environment Variables**
3. Verifique `VITE_API_URL`:
   - Deve ser a URL completa do backend: `https://seu-backend.vercel.app`
   - **COM** `https://`
   - **SEM** barra no final (`/`)
4. Salve e faça um **Redeploy**

---

### 4️⃣ Verificar Tabelas no Supabase

**Sintomas:**
- Erro: `relation "users" does not exist`
- Erro: `Table not found`

**Solução:**
1. Acesse [app.supabase.com](https://app.supabase.com)
2. Vá no seu projeto
3. Vá em **SQL Editor**
4. Execute este SQL para criar as tabelas:

```sql
-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de análises
CREATE TABLE IF NOT EXISTS analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_name VARCHAR(255) NOT NULL,
  analysis_detail TEXT NOT NULL,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, student_name)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
```

5. Clique em **Run** para executar

---

### 5️⃣ Verificar Credenciais do Supabase

**Sintomas:**
- Erro: `Invalid API key`
- Erro: `Authentication failed`

**Solução:**
1. No Vercel, vá no projeto do **Backend**
2. Vá em **Settings > Environment Variables**
3. Verifique:
   - `SUPABASE_URL`: deve começar com `https://` e terminar com `.supabase.co`
   - `SUPABASE_KEY`: deve ser a chave **anon public** (não service_role)
4. Para obter as credenciais:
   - Acesse [app.supabase.com](https://app.supabase.com)
   - Vá em **Settings > API**
   - Copie **Project URL** → `SUPABASE_URL`
   - Copie **anon public key** → `SUPABASE_KEY`

---

### 6️⃣ Verificar Logs do Backend

**No Vercel:**

1. Vá no projeto do **Backend**
2. Vá em **Deployments**
3. Clique no último deployment
4. Vá em **Functions** ou **Runtime Logs**
5. Tente fazer login/cadastro novamente
6. **Veja se aparecem erros nos logs**

---

## ✅ Checklist de Verificação

Marque o que você já verificou:

### Frontend:
- [ ] Console do navegador não mostra erros (ou anotou os erros)
- [ ] `VITE_API_URL` está configurada no Vercel
- [ ] URL do backend está correta (com `https://`)

### Backend:
- [ ] `CORS_ORIGINS` inclui a URL do frontend
- [ ] Todas as variáveis de ambiente configuradas
- [ ] Backend responde em `/health` (teste: `https://seu-backend.vercel.app/health`)

### Banco de Dados:
- [ ] Tabelas `users` e `analyses` criadas no Supabase
- [ ] Credenciais do Supabase estão corretas
- [ ] Projeto Supabase está ativo

---

## 🧪 Testar a API Diretamente

### Teste 1: Health Check

Abra no navegador:
```
https://seu-backend.vercel.app/health
```

**Deve retornar:** `{"status": "ok"}`

### Teste 2: Documentação

Abra no navegador:
```
https://seu-backend.vercel.app/docs
```

**Deve abrir:** Documentação Swagger da API

### Teste 3: Endpoint de Cadastro (via Swagger)

1. Acesse `https://seu-backend.vercel.app/docs`
2. Encontre o endpoint `/api/auth/register`
3. Clique em **"Try it out"**
4. Preencha os dados:
   ```json
   {
     "email": "teste@teste.com",
     "password": "senha123",
     "name": "Usuário Teste"
   }
   ```
5. Clique em **Execute**
6. **Veja se funciona ou qual erro aparece**

---

## 🔧 Soluções Rápidas

### Solução 1: Erro no Console do Navegador

**Se aparecer erro no console:**
1. Copie a mensagem de erro completa
2. Me mostre o erro
3. Vamos resolver baseado no erro específico

### Solução 2: Network Error

**Se aparecer "Network Error":**
1. Verifique se `VITE_API_URL` está configurada
2. Teste acessar a URL do backend diretamente no navegador
3. Verifique se o CORS está configurado

### Solução 3: Erro 404 ou 500

**Se aparecer erro 404 ou 500:**
1. Verifique os logs do backend no Vercel
2. Veja qual é a mensagem de erro específica
3. Me mostre o erro dos logs

### Solução 4: Tabelas Não Existem

**Se o erro é sobre tabelas:**
1. Execute o SQL acima no Supabase
2. Verifique se as tabelas foram criadas
3. Faça um novo teste de cadastro

---

## 🎯 Próximos Passos

**Me diga:**

1. **O que aparece no console do navegador quando você tenta logar?**
   - Copie os erros que aparecem

2. **A URL do backend está correta no frontend?**
   - Verifique em Settings > Environment Variables > `VITE_API_URL`

3. **As tabelas foram criadas no Supabase?**
   - Vá em SQL Editor e verifique se as tabelas existem

4. **O backend responde?**
   - Teste acessar `https://seu-backend.vercel.app/health`

5. **Qual é a mensagem de erro exata?**
   - No console do navegador ou nos logs do Vercel

Com essas informações, consigo resolver o problema específico! 🚀

