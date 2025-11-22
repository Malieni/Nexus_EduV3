# ⚡ Quick Start - Deploy no Vercel (5 minutos)

Guia rápido para quem quer fazer deploy agora mesmo.

## 🚀 Passo a Passo Rápido

### 1️⃣ Criar Conta no Vercel
- Acesse: [vercel.com](https://vercel.com)
- Clique em "Sign Up" e conecte com GitHub

### 2️⃣ Deploy do BACKEND

1. **Criar projeto:**
   - Clique em "Add New Project"
   - Selecione repositório "Nexus_EduV3"

2. **Configurar:**
   - **Project Name:** `nexus-education-api`
   - **Root Directory:** `Back-end`
   - **Framework:** Other

3. **Adicionar variáveis de ambiente:**
   ```
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua_chave_anon
   GROQ_API_KEY=gsk_sua_chave
   JWT_SECRET_KEY=b1831c126ab7ec7065a597dfce756fe4d0ea8d45c623c5784a7db77fac92332e
   JWT_ALGORITHM=HS256
   CORS_ORIGINS=https://*.vercel.app
   PORT=8000
   ```

4. **Deploy** e anotar URL do backend

### 3️⃣ Deploy do FRONTEND

1. **Criar projeto novamente:**
   - Clique em "Add New Project"
   - Selecione repositório "Nexus_EduV3"

2. **Configurar:**
   - **Project Name:** `nexus-education`
   - **Root Directory:** `Front-end`
   - **Framework:** Vite (detecta automaticamente)

3. **Adicionar variável:**
   ```
   VITE_API_URL=https://nexus-education-api.vercel.app
   ```
   *(Use a URL REAL do seu backend)*

4. **Deploy** e anotar URL do frontend

### 4️⃣ Atualizar CORS

1. Vá no projeto do **backend** no Vercel
2. **Settings > Environment Variables**
3. Atualize `CORS_ORIGINS` com a URL do frontend:
   ```
   https://nexus-education.vercel.app
   ```
4. **Redeploy** do backend

### 5️⃣ Testar

- Frontend: `https://nexus-education.vercel.app`
- Backend: `https://nexus-education-api.vercel.app/docs`

✅ **Pronto!**

---

## 📚 Guia Detalhado

Para instruções mais detalhadas, veja: `DEPLOY_VERCEL_PASSO_A_PASSO.md`

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs no Vercel
2. Confira se todas as variáveis estão configuradas
3. Veja o guia detalhado para troubleshooting

