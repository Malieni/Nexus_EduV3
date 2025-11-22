# 🚀 Deploy no Vercel - Passo a Passo Visual

Guia completo para fazer deploy do Nexus Education no Vercel, desde criar conta até publicar.

## 📋 Pré-requisitos

- ✅ Código no GitHub (já feito!)
- ✅ Conta no Supabase
- ✅ Conta no Groq
- ✅ Email para criar conta no Vercel

---

## 1️⃣ Criar Conta no Vercel

### Passo 1: Acessar o Vercel

1. Acesse [https://vercel.com](https://vercel.com)
2. Clique em **"Sign Up"** (Cadastrar)

### Passo 2: Escolher Método de Login

Escolha uma das opções:
- **GitHub** (recomendado - mais fácil de conectar seu repositório)
- **GitLab**
- **Bitbucket**
- **Email**

### Passo 3: Autorizar Acesso ao GitHub

Se escolher GitHub:
1. Clique em **"Authorize Vercel"**
2. Autorize o acesso aos seus repositórios
3. Aguarde o redirecionamento para o painel do Vercel

✅ **Conta criada!** Agora você verá o painel do Vercel.

---

## 2️⃣ Deploy do BACKEND (API)

### Passo 1: Criar Novo Projeto

1. No painel do Vercel, clique em **"Add New..."** ou **"New Project"**
2. Você verá seus repositórios do GitHub
3. Procure e clique em **"Nexus_EduV3"** (seu repositório)

### Passo 2: Configurar Projeto Backend

**Importante:** Configure exatamente assim:

```
┌─────────────────────────────────────────┐
│ Configure Project                       │
├─────────────────────────────────────────┤
│ Project Name:                           │
│ nexus-education-api  ← Digite isso      │
│                                         │
│ Framework Preset:                       │
│ [Other] ← Selecione "Other"             │
│                                         │
│ Root Directory:                         │
│ [Back-end]  ← Clique em "Edit" e digite │
│                                         │
│ Build Command:                          │
│ [vazio] ← Deixe vazio                   │
│                                         │
│ Output Directory:                       │
│ [vazio] ← Deixe vazio                   │
│                                         │
│ Install Command:                        │
│ pip install -r requirements.txt         │
└─────────────────────────────────────────┘
```

**Como configurar Root Directory:**
1. Clique no botão **"Edit"** ao lado de "Root Directory"
2. Digite: `Back-end`
3. Ou clique em "Browse" e selecione a pasta `Back-end`

### Passo 3: Configurar Variáveis de Ambiente

**Antes de fazer deploy**, clique em **"Environment Variables"** ou **"Add Environment Variables"**.

Você verá um formulário. Adicione cada variável:

#### Variável 1: SUPABASE_URL
```
Name:  SUPABASE_URL
Value: https://seu-projeto.supabase.co
```
*(Substitua pela URL real do seu Supabase)*

#### Variável 2: SUPABASE_KEY
```
Name:  SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
*(Substitua pela chave anon do seu Supabase)*

#### Variável 3: GROQ_API_KEY
```
Name:  GROQ_API_KEY
Value: gsk_sua_chave_do_groq
```
*(Substitua pela chave do Groq)*

#### Variável 4: JWT_SECRET_KEY
```
Name:  JWT_SECRET_KEY
Value: b1831c126ab7ec7065a597dfce756fe4d0ea8d45c623c5784a7db77fac92332e
```
*(Use a chave que geramos antes ou gere uma nova)*

#### Variável 5: JWT_ALGORITHM
```
Name:  JWT_ALGORITHM
Value: HS256
```

#### Variável 6: CORS_ORIGINS
```
Name:  CORS_ORIGINS
Value: https://*.vercel.app
```
*(Temporário - atualizaremos depois com a URL do frontend)*

#### Variável 7: PORT
```
Name:  PORT
Value: 8000
```

**Após adicionar todas:**
- Verifique se todas as 7 variáveis aparecem na lista
- Clique em **"Deploy"** ou **"Save & Deploy"**

### Passo 4: Aguardar Deploy

1. Você verá o log do build
2. Aguarde alguns minutos (primeira vez é mais lento)
3. Quando terminar, você verá: **"Deployment successful"** ✅

### Passo 5: Anotar URL do Backend

Após o deploy bem-sucedido, você verá algo como:

```
✅ Production: https://nexus-education-api.vercel.app
```

📝 **ANOTE ESTA URL!** Você precisará dela para o frontend.

### Passo 6: Testar o Backend

Abra uma nova aba e teste:
- **Health**: `https://nexus-education-api.vercel.app/health`
  - Deve retornar: `{"status": "ok"}`

- **Documentação**: `https://nexus-education-api.vercel.app/docs`
  - Deve abrir a documentação Swagger da API

✅ **Backend publicado!**

---

## 3️⃣ Deploy do FRONTEND

### Passo 1: Criar Novo Projeto (Novamente)

1. No painel do Vercel, clique em **"Add New..."** novamente
2. Clique novamente no repositório **"Nexus_EduV3"**

### Passo 2: Configurar Projeto Frontend

**Importante:** Configure exatamente assim:

```
┌─────────────────────────────────────────┐
│ Configure Project                       │
├─────────────────────────────────────────┤
│ Project Name:                           │
│ nexus-education  ← Digite isso          │
│                                         │
│ Framework Preset:                       │
│ [Vite] ← Vercel detecta automaticamente │
│                                         │
│ Root Directory:                         │
│ [Front-end]  ← Clique em "Edit" e digite│
│                                         │
│ Build Command:                          │
│ npm run build  ← Vercel detecta         │
│                                         │
│ Output Directory:                       │
│ dist  ← Vercel detecta                  │
│                                         │
│ Install Command:                        │
│ npm install  ← Vercel detecta           │
└─────────────────────────────────────────┘
```

**Como configurar Root Directory:**
1. Clique no botão **"Edit"** ao lado de "Root Directory"
2. Digite: `Front-end`
3. Ou clique em "Browse" e selecione a pasta `Front-end`

### Passo 3: Configurar Variável de Ambiente

**Antes de fazer deploy**, clique em **"Environment Variables"**.

Adicione apenas UMA variável:

#### Variável: VITE_API_URL
```
Name:  VITE_API_URL
Value: https://nexus-education-api.vercel.app
```
*(Substitua pela URL REAL do seu backend que você anotou antes!)*

**Importante:**
- Use a URL completa do backend
- Começa com `https://`
- Termina com `.vercel.app`
- **NÃO** adicione barra no final

### Passo 4: Fazer Deploy do Frontend

1. Clique em **"Deploy"**
2. Aguarde o build
3. Quando terminar: **"Deployment successful"** ✅

### Passo 5: Anotar URL do Frontend

Após o deploy, você verá:

```
✅ Production: https://nexus-education.vercel.app
```

📝 **ANOTE ESTA URL!**

### Passo 6: Testar o Frontend

1. Acesse a URL do frontend
2. Você deve ver a tela de login
3. Teste criar uma conta ou fazer login

✅ **Frontend publicado!**

---

## 4️⃣ Atualizar CORS no Backend

Agora que você tem a URL do frontend, precisa atualizar o CORS no backend:

### Passo 1: Ir no Projeto Backend

1. No painel do Vercel, encontre o projeto **"nexus-education-api"**
2. Clique nele

### Passo 2: Atualizar CORS_ORIGINS

1. Vá em **"Settings"** (ícone de engrenagem no topo)
2. Clique em **"Environment Variables"** no menu lateral
3. Encontre a variável **"CORS_ORIGINS"**
4. Clique nos **três pontinhos** ao lado
5. Clique em **"Edit"**
6. Atualize o valor para:
   ```
   https://nexus-education.vercel.app
   ```
   *(Substitua pela URL REAL do seu frontend!)*
7. Clique em **"Save"**

### Passo 3: Fazer Redeploy

1. Vá em **"Deployments"** no menu lateral
2. Clique nos **três pontinhos** ao lado do último deployment
3. Clique em **"Redeploy"**
4. Confirme clicando em **"Redeploy"** novamente
5. Aguarde o redeploy terminar

✅ **CORS atualizado!**

---

## 5️⃣ Testar o Sistema Completo

Agora teste tudo:

### Teste 1: Login/Cadastro
1. Acesse a URL do frontend
2. Tente criar uma conta
3. Tente fazer login

### Teste 2: Upload de PDF
1. Após fazer login
2. Tente fazer upload de um PDF
3. Verifique se a análise funciona

### Teste 3: Verificar Análises
1. Veja o histórico de análises
2. Clique em "Ver Detalhes" de uma análise

✅ **Sistema funcionando!**

---

## 🎯 Checklist Final

- [ ] Backend publicado no Vercel
- [ ] Variáveis de ambiente do backend configuradas
- [ ] Backend respondendo em `/health` e `/docs`
- [ ] Frontend publicado no Vercel
- [ ] `VITE_API_URL` configurada no frontend
- [ ] `CORS_ORIGINS` atualizado no backend
- [ ] Sistema testado end-to-end
- [ ] Login funcionando
- [ ] Upload de PDF funcionando

---

## 🔄 Futuras Atualizações

Quando você fizer alterações no código:

1. **Faça commit no GitHub:**
   ```bash
   git add .
   git commit -m "Descrição das alterações"
   git push
   ```

2. **O Vercel detecta automaticamente** e faz um novo deploy! 🎉

---

## 🐛 Problemas Comuns

### ❌ Erro: "Module not found"

**Solução:**
- Verifique se o **Root Directory** está correto
- Backend: `Back-end`
- Frontend: `Front-end`

### ❌ Erro: "Environment variable not found"

**Solução:**
- Vá em **Settings > Environment Variables**
- Verifique se todas as variáveis estão configuradas
- Faça um **Redeploy** após adicionar variáveis

### ❌ Erro: "CORS policy blocked"

**Solução:**
- Verifique se `CORS_ORIGINS` no backend inclui a URL exata do frontend
- Certifique-se de que não há barra no final (`/`)
- Faça um **Redeploy** do backend

### ❌ Frontend não encontra API

**Solução:**
- Verifique se `VITE_API_URL` está configurada corretamente
- Use a URL completa começando com `https://`
- Faça um **Redeploy** do frontend

---

## 📱 URLs Finais

Após concluir, você terá:

- **Frontend**: `https://nexus-education.vercel.app`
- **Backend**: `https://nexus-education-api.vercel.app`
- **API Docs**: `https://nexus-education-api.vercel.app/docs`

---

## 🎉 Pronto!

Seu sistema Nexus Education está publicado e funcionando no Vercel! 🚀

Agora você pode compartilhar o link do frontend com quem quiser testar o sistema.

