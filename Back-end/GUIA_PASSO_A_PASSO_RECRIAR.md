# 📋 GUIA PASSO A PASSO: Recriar Projeto no Vercel

## ✅ Passo 1: Verificação Local (COMPLETO)

### ✅ Verificação dos Arquivos

✅ **requirements.txt existe:** `Back-end/requirements.txt`  
✅ **requirements.txt contém todas as dependências:** 12 dependências  
✅ **runtime.txt existe:** `Back-end/runtime.txt`  
✅ **runtime.txt especifica Python 3.12**  
✅ **vercel.json está correto**

**Status:** ✅ Tudo está correto localmente!

---

## 📝 Passo 2: Anotar Configurações Atuais do Vercel

**⚠️ IMPORTANTE:** Antes de deletar o projeto, você PRECISA anotar todas as configurações!

### No Painel do Vercel:

1. **Abra o projeto atual** no Vercel
2. **Vá em Settings > General**
   - Anote o **Root Directory** (deve ser `Back-end`)
3. **Vá em Settings > Environment Variables**
   - **Anote TODAS as variáveis** e seus valores:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `GROQ_API_KEY`
     - `JWT_SECRET_KEY`
     - `CORS_ORIGINS`
     - `FRONTEND_URL` (se existir)

**📝 Use esta área para anotar:**

```
╔══════════════════════════════════════════════════════════╗
║  CONFIGURAÇÕES PARA ANOTAR                               ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Root Directory: Back-end                               ║
║                                                          ║
║  SUPABASE_URL: ________________________________         ║
║                                                          ║
║  SUPABASE_KEY: ________________________________         ║
║                                                          ║
║  GROQ_API_KEY: ________________________________         ║
║                                                          ║
║  JWT_SECRET_KEY: ________________________________       ║
║                                                          ║
║  CORS_ORIGINS: ________________________________         ║
║                                                          ║
║  FRONTEND_URL: ________________________________         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

**⏸️ PAUSE AQUI** até anotar todas as configurações!

---

## 🗑️ Passo 3: Deletar o Projeto no Vercel

**⚠️ ATENÇÃO:** Só faça isso DEPOIS de anotar todas as configurações!

1. No Vercel, vá em **Settings** (menu lateral esquerdo)
2. Clique em **General**
3. Role até o final da página
4. Na seção **Danger Zone**, clique em **Delete Project**
5. Digite o nome do projeto para confirmar
6. Clique em **Delete**

✅ **Projeto deletado com sucesso!**

---

## 🆕 Passo 4: Criar Novo Projeto

1. No Vercel, clique no botão **Add New...** (canto superior direito)
2. Selecione **Project**

3. **Import Git Repository:**
   - Na lista de repositórios, encontre **Malieni/Nexus_EduV3**
   - Clique em **Import** ao lado do repositório

4. **Configure o Projeto:**

   **Project Name:**
   ```
   nexus-education-backend
   ```
   
   **Framework Preset:**
   - Selecione **Other** na lista dropdown
   
   **Root Directory:**
   ```
   Back-end
   ```
   ⚠️ **MUITO IMPORTANTE:** Deve ser exatamente `Back-end` (com maiúscula B e hífen)
   
   **Build Command:**
   - Deixe **VAZIO**
   
   **Output Directory:**
   - Deixe **VAZIO**
   
   **Install Command:**
   - Deixe **VAZIO**

5. Clique em **Deploy**

6. **Aguarde o primeiro deploy** (pode levar 1-2 minutos)
   - ⚠️ O primeiro deploy pode falhar (é normal, faltam as variáveis de ambiente)

✅ **Projeto criado!**

---

## ⚙️ Passo 5: Configurar Environment Variables

**Agora vamos adicionar todas as variáveis que você anotou:**

1. No projeto recém-criado, vá em **Settings** (menu lateral)
2. Clique em **Environment Variables**

3. **Adicione cada variável UMA POR UMA:**

   **Variável 1: SUPABASE_URL**
   - Clique em **Add New**
   - **Key:** `SUPABASE_URL`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** Marque todas as 3 opções:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
   - Clique em **Save**

   **Variável 2: SUPABASE_KEY**
   - Clique em **Add New**
   - **Key:** `SUPABASE_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** Marque todas as 3 opções
   - Clique em **Save**

   **Variável 3: GROQ_API_KEY**
   - Clique em **Add New**
   - **Key:** `GROQ_API_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** Marque todas as 3 opções
   - Clique em **Save**

   **Variável 4: JWT_SECRET_KEY**
   - Clique em **Add New**
   - **Key:** `JWT_SECRET_KEY`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** Marque todas as 3 opções
   - Clique em **Save**

   **Variável 5: CORS_ORIGINS**
   - Clique em **Add New**
   - **Key:** `CORS_ORIGINS`
   - **Value:** (cole o valor que você anotou OU `https://seu-frontend.vercel.app`)
   - **Environments:** Marque todas as 3 opções
   - Clique em **Save**

   **Variável 6: FRONTEND_URL** (opcional, se você anotou)
   - Clique em **Add New**
   - **Key:** `FRONTEND_URL`
   - **Value:** (cole o valor que você anotou)
   - **Environments:** Marque todas as 3 opções
   - Clique em **Save**

✅ **Todas as variáveis configuradas!**

---

## 🔄 Passo 6: Fazer Redeploy

1. Vá em **Deployments** (menu lateral)
2. Encontre o último deployment (geralmente no topo)
3. Clique nos **três pontos (⋯)** à direita do deployment
4. Selecione **Redeploy**
5. **Aguarde o build completar** (1-2 minutos)

✅ **Redeploy concluído!**

---

## 🔍 Passo 7: Verificar Build Logs

1. No deployment que acabou de ser feito, clique nele
2. Clique na aba **Build Logs** (não Function Logs!)
3. **Procure por estas mensagens:**

### ✅ SE FUNCIONOU, você verá:

```
Installing required dependencies from requirements.txt...
Collecting fastapi==0.121.3
Collecting uvicorn[standard]==0.38.0
Collecting python-multipart==0.0.20
...
Successfully installed fastapi-0.121.3 uvicorn-0.38.0 ...
```

**🎉 Se você VER "Successfully installed...", as dependências foram instaladas!**

### ❌ SE NÃO FUNCIONOU:

- Você NÃO verá "Successfully installed..."
- Apenas verá "Installing..." mas sem confirmação
- Neste caso, verifique se o Root Directory está correto como `Back-end`

---

## 🧪 Passo 8: Testar o Endpoint

1. **Copie a URL do projeto** (aparece em Deployments > [seu deployment] > Domains)

2. **Tente acessar no navegador:**
   ```
   https://seu-projeto.vercel.app/health
   ```
   
   Ou:
   ```
   https://seu-projeto.vercel.app/
   ```

### ✅ SE FUNCIONOU, você verá:

**No endpoint `/health`:**
```json
{"status": "ok"}
```

**No endpoint `/`:**
```json
{
  "message": "Nexus Education API",
  "status": "running"
}
```

### ❌ SE NÃO FUNCIONOU:

- Você verá um erro 500
- Ou uma mensagem de erro JSON

**Neste caso:**
- Vá em **Functions** > **api/index** > **Logs**
- Copie os logs completos
- Me envie para análise

---

## ✅ Checklist Final

Marque cada item conforme completa:

- [ ] Passo 1: Verificação local completa
- [ ] Passo 2: Configurações anotadas
- [ ] Passo 3: Projeto antigo deletado
- [ ] Passo 4: Novo projeto criado com Root Directory = `Back-end`
- [ ] Passo 5: Todas as Environment Variables configuradas
- [ ] Passo 6: Redeploy feito
- [ ] Passo 7: Build Logs mostram "Successfully installed..."
- [ ] Passo 8: Endpoint `/health` retorna `{"status": "ok"}`

---

## 🎉 Pronto!

Se todos os passos foram concluídos e o endpoint está funcionando, **parabéns!** 🎉

O problema foi resolvido!

**Se ainda houver problemas, me envie:**
1. Os Build Logs completos
2. Os Function Logs (se disponível)
3. O que você vê ao acessar o endpoint

