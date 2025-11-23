# ✅ CHECKLIST: Recriar Projeto no Vercel

## 📋 Passo 1: Verificar Arquivos Locais

### ✅ Verificar se requirements.txt está commitado

Execute:
```bash
git ls-files | grep requirements.txt
```

Deve mostrar:
- `Back-end/requirements.txt`
- `Back-end/api/requirements.txt`

### ✅ Verificar conteúdo do requirements.txt

O arquivo `Back-end/requirements.txt` deve conter:
```
fastapi==0.121.3
uvicorn[standard]==0.38.0
python-multipart==0.0.20
python-dotenv==1.2.1
supabase==2.0.3
groq==0.36.0
pypdf2==3.0.1
pydantic==2.12.4
pydantic-settings==2.12.0
python-jose[cryptography]==3.5.0
passlib[bcrypt]==1.7.4
mangum==0.19.0
```

### ✅ Verificar runtime.txt

O arquivo `Back-end/runtime.txt` deve conter:
```
3.12
```

---

## 📝 Passo 2: Anotar Configurações do Projeto Atual

**No Vercel (painel web):**

1. **Vá em Settings > General**
   - Anote o **Root Directory**: `Back-end`

2. **Vá em Settings > Environment Variables**
   - Anote TODAS as variáveis:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `GROQ_API_KEY`
     - `JWT_SECRET_KEY`
     - `CORS_ORIGINS`
     - `FRONTEND_URL` (se existir)

3. **Vá em Deployments**
   - Anote a URL do projeto: `https://seu-projeto.vercel.app`

**📝 Use este espaço para anotar:**

```
Root Directory: ___________

Environment Variables:
- SUPABASE_URL: ___________
- SUPABASE_KEY: ___________
- GROQ_API_KEY: ___________
- JWT_SECRET_KEY: ___________
- CORS_ORIGINS: ___________
- FRONTEND_URL: ___________

URL do Projeto: ___________
```

---

## 🗑️ Passo 3: Deletar Projeto no Vercel

**⚠️ ATENÇÃO: Isso vai deletar o projeto atual. Certifique-se de ter anotado todas as configurações!**

1. No Vercel, vá em **Settings > General**
2. Role até o final da página
3. Na seção **Danger Zone**, clique em **Delete Project**
4. Digite o nome do projeto para confirmar
5. Clique em **Delete**

✅ Projeto deletado com sucesso!

---

## 🆕 Passo 4: Criar Novo Projeto

1. No Vercel, clique em **Add New Project** (botão no topo)

2. **Import Git Repository:**
   - Selecione o repositório: `Malieni/Nexus_EduV3`
   - Clique em **Import**

3. **Configure o Projeto:**
   
   **Project Name:** `nexus-education-backend` (ou qualquer nome)
   
   **Framework Preset:** `Other` (selecione na lista)
   
   **Root Directory:** `Back-end` ← **MUITO IMPORTANTE!**
   
   **Build Command:** (deixe vazio)
   
   **Output Directory:** (deixe vazio)
   
   **Install Command:** (deixe vazio)

4. Clique em **Deploy**

5. **Aguarde o primeiro deploy** (pode falhar, é normal)

✅ Projeto criado!

---

## ⚙️ Passo 5: Configurar Environment Variables

1. Depois do primeiro deploy, vá em **Settings > Environment Variables**

2. **Adicione cada variável uma por uma:**

   **Variável 1:**
   - **Key:** `SUPABASE_URL`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

   **Variável 2:**
   - **Key:** `SUPABASE_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

   **Variável 3:**
   - **Key:** `GROQ_API_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

   **Variável 4:**
   - **Key:** `JWT_SECRET_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

   **Variável 5:**
   - **Key:** `CORS_ORIGINS`
   - **Value:** (cole o valor que você anotou ou `https://seu-frontend.vercel.app`)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

   **Variável 6 (opcional):**
   - **Key:** `FRONTEND_URL`
   - **Value:** (URL do seu frontend, se existir)
   - **Environments:** ✅ Production ✅ Preview ✅ Development
   - Clique em **Save**

✅ Todas as variáveis configuradas!

---

## 🔄 Passo 6: Fazer Redeploy

1. Vá em **Deployments**
2. Clique nos **três pontos (⋯)** do último deployment
3. Clique em **Redeploy**
4. **Aguarde o build completar** (pode levar 1-2 minutos)

✅ Redeploy concluído!

---

## 🔍 Passo 7: Verificar Build Logs

1. Clique no deployment que acabou de ser feito
2. Clique em **Build Logs** (não Function Logs!)
3. **Procure por estas mensagens:**

✅ **Se você VER isso, está funcionando:**
```
Installing required dependencies from requirements.txt...
Collecting fastapi==0.121.3
Collecting uvicorn[standard]==0.38.0
...
Successfully installed fastapi-0.121.3 uvicorn-0.38.0 ...
```

❌ **Se você NÃO VER "Successfully installed...":**
- As dependências não foram instaladas
- Pode ser necessário verificar o Root Directory novamente

---

## 🧪 Passo 8: Testar o Endpoint

1. **Copie a URL do projeto** (aparece em Deployments > [seu deployment])

2. **Tente acessar:**
   ```
   https://seu-projeto.vercel.app/health
   ```
   
   Ou no navegador:
   ```
   https://seu-projeto.vercel.app/
   ```

3. **Resultado esperado:**

   ✅ **Se funcionar:**
   ```json
   {"status": "ok"}
   ```
   Ou:
   ```json
   {"message": "Nexus Education API", "status": "running"}
   ```

   ❌ **Se não funcionar:**
   - Verifique os Function Logs
   - Me envie os logs completos

---

## ✅ Checklist Final

- [ ] Passo 1: Verificações locais concluídas
- [ ] Passo 2: Configurações anotadas
- [ ] Passo 3: Projeto antigo deletado
- [ ] Passo 4: Novo projeto criado com Root Directory = `Back-end`
- [ ] Passo 5: Todas as Environment Variables configuradas
- [ ] Passo 6: Redeploy feito
- [ ] Passo 7: Build Logs mostram "Successfully installed..."
- [ ] Passo 8: Endpoint `/health` retorna `{"status": "ok"}`

---

## 🎉 Pronto!

Se todos os passos foram concluídos e o endpoint está funcionando, **parabéns!** O problema foi resolvido!

Se ainda houver problemas, me envie:
1. Os Build Logs completos
2. Os Function Logs (se disponível)
3. O que você vê ao acessar o endpoint

