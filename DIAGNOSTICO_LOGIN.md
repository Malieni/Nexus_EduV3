# 🔍 Diagnóstico Rápido - Problema de Login/Cadastro

## ✅ Problemas Mais Comuns

### 1️⃣ Verificar Erros no Console do Navegador

**PASSO IMPORTANTE:**
1. Abra a aplicação no navegador
2. Pressione **F12** (DevTools)
3. Vá na aba **Console**
4. Tente fazer login ou cadastro
5. **ME MOSTRE OS ERROS QUE APARECEM!**

---

## 🔧 Checklist de Verificação

### Frontend:
- [ ] **Console do navegador:** Abra F12 > Console e veja se há erros
- [ ] **VITE_API_URL:** Está configurada no Vercel?
  - No Vercel: Settings > Environment Variables
  - Deve ser: `https://seu-backend.vercel.app` (URL do seu backend)

### Backend:
- [ ] **Backend responde?** Teste: `https://seu-backend.vercel.app/health`
  - Deve retornar: `{"status": "ok"}`
- [ ] **CORS configurado?** Settings > Environment Variables > `CORS_ORIGINS`
  - Deve incluir: `https://seu-frontend.vercel.app`

### Banco de Dados:
- [ ] **Tabelas criadas?** Vá no Supabase > SQL Editor
  - Execute o SQL abaixo para criar as tabelas

---

## 🗄️ Criar Tabelas no Supabase (IMPORTANTE!)

**Se você ainda não criou as tabelas, faça isso AGORA:**

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Vá no seu projeto
3. Clique em **SQL Editor** (ícone de banco de dados)
4. Clique em **New Query**
5. **Cole e execute este SQL:**

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

-- Índices
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
```

6. Clique em **Run**
7. Deve aparecer: **Success. No rows returned**

---

## 🧪 Testar API Diretamente

### Teste 1: Health Check

Abra no navegador:
```
https://seu-backend.vercel.app/health
```

**Deve retornar:** `{"status": "ok"}`

Se não retornar, o backend não está funcionando!

### Teste 2: Documentação Swagger

Abra no navegador:
```
https://seu-backend.vercel.app/docs
```

**Deve abrir:** Interface Swagger para testar a API

### Teste 3: Cadastro via Swagger

1. Acesse `https://seu-backend.vercel.app/docs`
2. Expanda o endpoint `/api/auth/register`
3. Clique em **"Try it out"**
4. Preencha:
   ```json
   {
     "email": "teste@teste.com",
     "password": "senha123",
     "name": "Teste Usuario"
   }
   ```
5. Clique em **Execute**
6. **Veja se funciona ou qual erro aparece**

---

## 🎯 Correções Aplicadas

✅ **Corrigido bug no AuthContext** - Faltava `try` no `register`

**Faça commit e push:**
```bash
git add Front-end/src/contexts/AuthContext.jsx
git commit -m "Fix: Corrigir bug no registro de usuário"
git push
```

---

## 📋 Me Diga:

1. **O que aparece no console do navegador?** (F12 > Console)
   - Copie os erros que aparecem em vermelho

2. **O backend responde?**
   - Teste: `https://seu-backend.vercel.app/health`

3. **As tabelas foram criadas no Supabase?**
   - Vá em SQL Editor e execute o SQL acima

4. **A URL do backend está configurada no frontend?**
   - Verifique: Settings > Environment Variables > `VITE_API_URL`

5. **CORS está configurado?**
   - Verifique: Backend > Settings > Environment Variables > `CORS_ORIGINS`

Com essas informações, consigo resolver o problema específico! 🚀

