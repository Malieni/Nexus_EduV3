# 🚀 Como Publicar no Vercel - Guia Rápido

Este guia mostra como publicar o Nexus Education no Vercel passo a passo.

## 📋 Passo a Passo Completo

### 1️⃣ Preparar o Projeto no GitHub

1. **Criar repositório no GitHub:**
   - Acesse [github.com](https://github.com)
   - Crie um novo repositório (ex: `nexus-education`)
   - **NÃO** adicione `.env` ao commit (já está no `.gitignore`)

2. **Enviar código para GitHub:**
```bash
git init
git add .
git commit -m "Nexus Education - Initial commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/nexus-education.git
git push -u origin main
```

---

## 🌐 Parte 1: Publicar BACKEND (API)

### Passo 1: Criar Projeto Backend no Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login
2. Clique em **"Add New Project"** ou **"New Project"**
3. **Import Git Repository**: Conecte seu GitHub e selecione o repositório `nexus-education`

### Passo 2: Configurar Build do Backend

**Configure assim:**

- **Project Name**: `nexus-education-api` (ou outro nome)
- **Framework Preset**: **Other**
- **Root Directory**: `Back-end` ⚠️ **IMPORTANTE**
- **Build Command**: Deixe **VAZIO** ou `pip install -r requirements.txt`
- **Output Directory**: Deixe **VAZIO**
- **Install Command**: `pip install -r requirements.txt`

### Passo 3: Configurar Variáveis de Ambiente

Antes de fazer deploy, clique em **"Environment Variables"** e adicione:

```
SUPABASE_URL = https://seu-projeto.supabase.co
SUPABASE_KEY = sua_chave_anon_do_supabase
GROQ_API_KEY = gsk_sua_chave_do_groq
JWT_SECRET_KEY = sua_chave_secreta_jwt
JWT_ALGORITHM = HS256
CORS_ORIGINS = https://nexus-education.vercel.app
```

⚠️ **Importante sobre CORS_ORIGINS:**
- Agora coloque um valor temporário como: `*` ou `https://*.vercel.app`
- Depois de publicar o frontend, atualize com a URL real do frontend

### Passo 4: Fazer Deploy do Backend

1. Clique em **"Deploy"**
2. Aguarde alguns minutos (primeira vez é mais lento)
3. Após o deploy, você verá uma URL como: `https://nexus-education-api.vercel.app`

✅ **Anote esta URL!** Você precisará dela para o frontend.

### Passo 5: Testar o Backend

Teste a API:
- Acesse: `https://sua-api.vercel.app/health` → Deve retornar `{"status": "ok"}`
- Acesse: `https://sua-api.vercel.app/docs` → Deve abrir a documentação Swagger

---

## 🎨 Parte 2: Publicar FRONTEND

### Passo 1: Criar Projeto Frontend no Vercel

1. No painel do Vercel, clique em **"Add New Project"** novamente
2. Conecte o **mesmo repositório** `nexus-education`

### Passo 2: Configurar Build do Frontend

**Configure assim:**

- **Project Name**: `nexus-education` (ou outro nome)
- **Framework Preset**: **Vite** (Vercel detecta automaticamente)
- **Root Directory**: `Front-end` ⚠️ **IMPORTANTE**
- **Build Command**: `npm run build` (Vercel detecta automaticamente)
- **Output Directory**: `dist` (Vercel detecta automaticamente)
- **Install Command**: `npm install` (Vercel detecta automaticamente)

### Passo 3: Configurar Variável de Ambiente do Frontend

Antes de fazer deploy, clique em **"Environment Variables"** e adicione:

```
VITE_API_URL = https://nexus-education-api.vercel.app
```

⚠️ **Substitua** `nexus-education-api.vercel.app` pela URL real do seu backend!

### Passo 4: Fazer Deploy do Frontend

1. Clique em **"Deploy"**
2. Aguarde o build
3. Após o deploy, você verá uma URL como: `https://nexus-education.vercel.app`

### Passo 5: Atualizar CORS no Backend

Agora que você tem a URL do frontend:

1. Vá no projeto do **Backend** no Vercel
2. Vá em **Settings > Environment Variables**
3. Atualize `CORS_ORIGINS`:
   ```
   https://nexus-education.vercel.app
   ```
4. Vá em **Deployments** e faça um **"Redeploy"** do backend

### Passo 6: Testar o Sistema Completo

1. Acesse a URL do frontend: `https://nexus-education.vercel.app`
2. Teste:
   - ✅ Cadastro de usuário
   - ✅ Login
   - ✅ Upload de PDF
   - ✅ Visualização de análises

---

## ✅ Checklist Final

- [ ] Backend publicado no Vercel
- [ ] API respondendo em `/health` e `/docs`
- [ ] Variáveis de ambiente do backend configuradas
- [ ] Frontend publicado no Vercel
- [ ] `VITE_API_URL` configurada no frontend
- [ ] `CORS_ORIGINS` atualizado no backend
- [ ] Sistema funcionando end-to-end

---

## 🔄 Atualizar o Sistema

Quando você fizer alterações no código:

```bash
git add .
git commit -m "Descrição das alterações"
git push
```

O Vercel detecta automaticamente e faz um novo deploy! 🎉

---

## 🐛 Problemas Comuns

### ❌ Erro: "Module not found"

**Solução:**
- Verifique se `requirements.txt` está na pasta `Back-end/`
- Certifique-se de que o **Root Directory** está configurado como `Back-end`

### ❌ Erro: "Environment variable not found"

**Solução:**
- Vá em **Settings > Environment Variables** no Vercel
- Verifique se todas as variáveis estão configuradas
- Faça um **Redeploy** após adicionar variáveis

### ❌ Erro: "CORS policy blocked"

**Solução:**
- Atualize `CORS_ORIGINS` no backend com a URL exata do frontend
- Certifique-se de usar `https://` (não `http://`)
- Faça um **Redeploy** do backend após atualizar

### ❌ Frontend não encontra API

**Solução:**
- Verifique se `VITE_API_URL` está configurada corretamente
- Certifique-se de que a URL começa com `https://`
- Faça um **Redeploy** do frontend após atualizar

---

## 📱 URLs Finais

Após publicar, você terá:

- **Frontend**: `https://nexus-education.vercel.app`
- **Backend API**: `https://nexus-education-api.vercel.app`
- **API Docs**: `https://nexus-education-api.vercel.app/docs`

---

## 🎉 Pronto!

Seu sistema Nexus Education está publicado e funcionando no Vercel! 🚀

Agora você pode compartilhar o link do frontend com quem quiser testar o sistema.

