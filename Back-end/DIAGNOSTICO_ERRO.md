# 🔍 Diagnóstico de Erro no Deploy

Use este guia para identificar e resolver o erro específico que você está enfrentando.

## 📋 Passo 1: Identificar o Tipo de Erro

### No painel do Vercel:

1. Vá em **Deployments**
2. Clique no deployment que falhou (marcado com ❌)
3. Vá em **"Build Logs"** ou **"Function Logs"**
4. **Copie a mensagem de erro completa**

---

## 🔎 Tipos de Erro Mais Comuns

### 1️⃣ Erro: "ModuleNotFoundError: No module named 'X'"

**Causa:** Dependência faltando

**Solução:**
```bash
# Edite Back-end/requirements.txt
# Adicione a dependência faltante
git add Back-end/requirements.txt
git commit -m "Fix: Adicionar dependência faltante"
git push
```

### 2️⃣ Erro: "ImportError: cannot import name 'X' from 'Y'"

**Causa:** Problema com paths de importação

**Solução:**
- Verifique se o arquivo existe
- Verifique se está na pasta correta
- Certifique-se de que o `api/index.py` está importando corretamente

### 3️⃣ Erro: "pydantic_settings.BaseSettings: Field required"

**Causa:** Variável de ambiente faltando

**Solução:**
1. No Vercel, vá em **Settings > Environment Variables**
2. Adicione a variável faltante:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GROQ_API_KEY`
   - `JWT_SECRET_KEY`
3. Faça um **Redeploy**

### 4️⃣ Erro: "FileNotFoundError" ou "No such file or directory"

**Causa:** Arquivo faltando ou caminho incorreto

**Solução:**
- Verifique se o arquivo existe
- Verifique se está na pasta correta
- Certifique-se de que o Root Directory está configurado corretamente

### 5️⃣ Erro: "Build timeout" ou "Build exceeded maximum duration"

**Causa:** Build muito lento

**Solução:**
- Simplifique o `requirements.txt`
- Remova dependências desnecessárias
- Verifique se não há dependências duplicadas

### 6️⃣ Erro: "Unable to resolve root directory"

**Causa:** Root Directory configurado incorretamente

**Solução:**
1. No Vercel, vá em **Settings > General**
2. Configure **Root Directory** como:
   - Backend: `Back-end`
   - Frontend: `Front-end`
3. Faça um novo deploy

---

## ✅ Verificação Rápida

Execute este checklist:

### Backend:
- [ ] `Back-end/requirements.txt` existe e tem todas as dependências?
- [ ] `Back-end/api/index.py` existe?
- [ ] `Back-end/vercel.json` existe?
- [ ] Root Directory = `Back-end`?
- [ ] Todas as variáveis de ambiente configuradas?

### Variáveis de Ambiente Necessárias:
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_KEY`
- [ ] `GROQ_API_KEY`
- [ ] `JWT_SECRET_KEY`
- [ ] `JWT_ALGORITHM` (opcional)
- [ ] `CORS_ORIGINS` (opcional)
- [ ] `PORT` (opcional)

---

## 🚀 Correção Rápida

Se você não sabe qual é o erro específico:

### 1. Limpeza Geral:

```bash
# 1. Certifique-se de que requirements.txt está limpo
# 2. Verifique se todas as variáveis estão configuradas
# 3. Faça commit e push
git add .
git commit -m "Fix: Limpeza e correção de configurações"
git push
```

### 2. Verifique os Logs:

No Vercel:
1. Deployments > Deployment que falhou
2. Build Logs
3. Procure pela primeira mensagem de erro (geralmente está no final)

### 3. Redeploy:

Após corrigir:
1. Vercel > Deployments
2. Três pontos ao lado do deployment
3. **Redeploy**

---

## 📞 Preciso de Mais Ajuda?

1. **Copie a mensagem de erro completa** dos logs
2. **Me diga:**
   - Qual é a mensagem de erro exata?
   - Em qual etapa o erro acontece? (Build? Deploy? Runtime?)
   - Backend ou Frontend?

Com essas informações, posso ajudar a resolver o problema específico!

---

## 🎯 Correções Aplicadas

✅ `requirements.txt` limpo e otimizado
✅ Guias de troubleshooting criados
✅ Checklist de verificação pronto

Agora tente fazer deploy novamente!

