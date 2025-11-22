# 🚀 Guia de Publicação no Vercel

Este guia detalhado mostra como publicar o sistema Nexus Education no Vercel.

## 📋 Pré-requisitos

1. ✅ Conta no [Vercel](https://vercel.com) (gratuita)
2. ✅ Conta no [Supabase](https://supabase.com) (gratuita)
3. ✅ Conta no [Groq](https://console.groq.com) (gratuita)
4. ✅ Git instalado
5. ✅ GitHub, GitLab ou Bitbucket (para conectar com Vercel)

## 📦 Preparação

### 1. Configurar Repositório Git

Se ainda não tiver um repositório Git:

```bash
# Na pasta raiz do projeto
git init
git add .
git commit -m "Initial commit: Nexus Education"
```

### 2. Enviar para GitHub/GitLab

Crie um repositório no GitHub e envie o código:

```bash
git remote add origin https://github.com/seu-usuario/nexus-education.git
git push -u origin main
```

⚠️ **IMPORTANTE**: Certifique-se de que o `.env` está no `.gitignore` (não deve ser commitado!)

---

## 🌐 Parte 1: Publicar Backend (API)

### Passo 1: Criar Projeto no Vercel

1. Acesse [https://vercel.com](https://vercel.com)
2. Clique em **"Add New Project"** ou **"New Project"**
3. Conecte seu repositório (GitHub/GitLab/Bitbucket)
4. Selecione o repositório `nexus-education`

### Passo 2: Configurar Projeto Backend

**Configurações do Projeto:**

- **Framework Preset**: Outro (ou deixe em branco)
- **Root Directory**: `Back-end`
- **Build Command**: Deixe vazio (Vercel detecta automaticamente)
- **Output Directory**: Deixe vazio (API não precisa)
- **Install Command**: `pip install -r requirements.txt`

**Ou use estas configurações no `vercel.json` (já criado):**

O arquivo `Back-end/vercel.json` já está configurado com:
- Python 3.11
- Handler em `api/index.py`
- Rotas configuradas

### Passo 3: Configurar Variáveis de Ambiente

No Vercel, vá em **Settings > Environment Variables** e adicione:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_do_supabase
GROQ_API_KEY=gsk_sua_chave_do_groq
JWT_SECRET_KEY=sua_chave_secreta_jwt
JWT_ALGORITHM=HS256
CORS_ORIGINS=https://seu-frontend.vercel.app
PORT=8000
```

**Importante:**
- **CORS_ORIGINS**: Coloque a URL do seu frontend no Vercel (você obterá após publicar o frontend)
- Para desenvolvimento, você pode usar `*` temporariamente, mas não em produção

### Passo 4: Publicar Backend

1. Clique em **"Deploy"**
2. Aguarde o build (pode levar alguns minutos na primeira vez)
3. Após o deploy, você receberá uma URL como: `https://nexus-education-api.vercel.app`

### Passo 5: Verificar Backend

Teste a API:
- Acesse: `https://sua-api.vercel.app/health`
- Deve retornar: `{"status": "ok"}`
- Acesse: `https://sua-api.vercel.app/docs` (documentação Swagger)

✅ **Anote a URL da API**, você precisará dela para configurar o frontend!

---

## 🎨 Parte 2: Publicar Frontend

### Passo 1: Criar Novo Projeto no Vercel

1. No painel do Vercel, clique em **"Add New Project"** novamente
2. Conecte o mesmo repositório
3. Desta vez, vamos configurar para o frontend

### Passo 2: Configurar Projeto Frontend

**Configurações do Projeto:**

- **Framework Preset**: Vite
- **Root Directory**: `Front-end`
- **Build Command**: `npm run build` (Vercel detecta automaticamente)
- **Output Directory**: `dist` (Vercel detecta automaticamente)
- **Install Command**: `npm install`

**Ou use estas configurações no `vercel.json` (já criado):**

O arquivo `Front-end/vercel.json` já está configurado.

### Passo 3: Configurar Variáveis de Ambiente do Frontend

No Vercel, vá em **Settings > Environment Variables** e adicione:

```env
VITE_API_URL=https://sua-api-backend.vercel.app
```

**Onde `sua-api-backend.vercel.app` é a URL do backend que você publicou!**

### Passo 4: Atualizar CORS no Backend

Agora que você tem a URL do frontend, atualize o CORS no backend:

1. Vá no projeto do **Backend** no Vercel
2. Vá em **Settings > Environment Variables**
3. Atualize `CORS_ORIGINS`:
   ```
   https://seu-frontend.vercel.app
   ```
4. Faça um novo deploy (Vercel faz automaticamente ou clique em "Redeploy")

### Passo 5: Publicar Frontend

1. Clique em **"Deploy"**
2. Aguarde o build
3. Após o deploy, você receberá uma URL como: `https://nexus-education.vercel.app`

### Passo 6: Verificar Frontend

1. Acesse a URL do frontend
2. Teste o login/cadastro
3. Teste o upload de PDF

✅ **Sistema publicado!**

---

## 🔄 Atualizações Futuras

### Atualizar o Código

Quando você fizer alterações:

```bash
git add .
git commit -m "Descrição das alterações"
git push
```

O Vercel detecta automaticamente e faz um novo deploy! 🎉

### Deploy Manual

Se precisar fazer deploy manual:

1. No painel do Vercel
2. Vá em **Deployments**
3. Clique nos três pontos ao lado do deployment
4. Clique em **"Redeploy"**

---

## 🐛 Solução de Problemas

### Erro: "Module not found"

**Problema**: Dependências não instaladas.

**Solução**:
- Verifique se o `requirements.txt` está na pasta `Back-end/`
- Verifique se o `package.json` está na pasta `Front-end/`

### Erro: "Environment variable not found"

**Problema**: Variáveis de ambiente não configuradas.

**Solução**:
- Vá em **Settings > Environment Variables** no Vercel
- Verifique se todas as variáveis estão configuradas
- Certifique-se de fazer um novo deploy após adicionar variáveis

### Erro: "CORS policy blocked"

**Problema**: CORS não configurado corretamente.

**Solução**:
- Verifique se `CORS_ORIGINS` no backend inclui a URL do frontend
- Certifique-se de que não há barra no final das URLs
- Faça um novo deploy do backend após atualizar CORS

### API não responde

**Problema**: Handler não configurado corretamente.

**Solução**:
- Verifique se o arquivo `Back-end/api/index.py` existe
- Verifique se o `vercel.json` está na pasta `Back-end/`
- Veja os logs do deployment no Vercel

### Frontend não encontra API

**Problema**: `VITE_API_URL` não configurada ou incorreta.

**Solução**:
- Verifique se `VITE_API_URL` no frontend aponta para a URL correta do backend
- Certifique-se de que a URL começa com `https://`
- Faça um novo deploy do frontend após atualizar a variável

---

## 📊 Verificando Logs

Para ver os logs de erros:

1. No painel do Vercel
2. Vá em **Deployments**
3. Clique no deployment
4. Vá em **Functions** (para backend) ou **Build Logs** (para frontend)

---

## ✅ Checklist de Publicação

- [ ] Backend publicado no Vercel
- [ ] Variáveis de ambiente do backend configuradas
- [ ] API respondendo em `/health`
- [ ] Documentação da API acessível em `/docs`
- [ ] Frontend publicado no Vercel
- [ ] `VITE_API_URL` configurada no frontend
- [ ] `CORS_ORIGINS` atualizado no backend com URL do frontend
- [ ] Login/Cadastro funcionando
- [ ] Upload de PDF funcionando

---

## 🎯 URLs Finais

Após publicar, você terá:

- **Frontend**: `https://seu-frontend.vercel.app`
- **Backend**: `https://seu-backend.vercel.app`
- **API Docs**: `https://seu-backend.vercel.app/docs`

---

## 🔒 Segurança em Produção

⚠️ **IMPORTANTE**:

1. **NUNCA** commite o arquivo `.env` no Git
2. Use variáveis de ambiente no Vercel
3. Use `https://` em produção (não `http://`)
4. Configure CORS apenas com URLs confiáveis
5. Mantenha suas chaves de API em segredo

---

## 📞 Suporte

Se tiver problemas:

1. Verifique os logs no Vercel
2. Veja a documentação: [https://vercel.com/docs](https://vercel.com/docs)
3. Verifique se todas as variáveis estão configuradas
4. Certifique-se de que o banco de dados Supabase está configurado

---

## 🎉 Pronto!

Seu sistema Nexus Education está publicado e funcionando no Vercel! 🚀

