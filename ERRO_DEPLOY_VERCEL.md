# ❌ Erro ao Fazer Deploy no Vercel - Guia de Solução

## 🚨 Como Resolver AGORA

### Passo 1: Identifique o Erro

No painel do Vercel:
1. Vá em **Deployments**
2. Clique no deployment que falhou (marcado com ❌)
3. Veja os **"Build Logs"** ou **"Function Logs"**
4. **Copie a mensagem de erro completa**

---

## 🔧 Soluções Mais Comuns

### ✅ Solução 1: Erro de Dependências

**Se o erro é algo como:**
```
ModuleNotFoundError: No module named 'X'
```

**SOLUÇÃO:**
1. O arquivo `requirements.txt` já foi corrigido
2. Faça commit e push:
   ```bash
   git add Back-end/requirements.txt
   git commit -m "Fix: Corrigir requirements.txt"
   git push
   ```
3. O Vercel fará um novo deploy automaticamente

---

### ✅ Solução 2: Variáveis de Ambiente Faltando

**Se o erro é algo como:**
```
Field required: supabase_url
Environment variable not found
```

**SOLUÇÃO:**
1. No Vercel, vá em **Settings > Environment Variables**
2. Adicione TODAS estas variáveis:
   ```
   SUPABASE_URL = https://seu-projeto.supabase.co
   SUPABASE_KEY = sua_chave_anon
   GROQ_API_KEY = gsk_sua_chave
   JWT_SECRET_KEY = b1831c126ab7ec7065a597dfce756fe4d0ea8d45c623c5784a7db77fac92332e
   JWT_ALGORITHM = HS256
   CORS_ORIGINS = https://*.vercel.app
   PORT = 8000
   ```
3. Clique em **Save**
4. Vá em **Deployments** > Três pontos > **Redeploy**

---

### ✅ Solução 3: Root Directory Incorreto

**Se o erro é algo como:**
```
Unable to resolve root directory
Root Directory not found
```

**SOLUÇÃO:**
1. No Vercel, vá em **Settings > General**
2. Verifique o **Root Directory**:
   - **Backend:** deve ser `Back-end` (com hífen!)
   - **Frontend:** deve ser `Front-end` (com hífen!)
3. Se estiver errado, edite e salve
4. Faça um novo deploy

---

### ✅ Solução 4: Build Timeout

**Se o erro é:**
```
Build exceeded maximum duration
Build timeout
```

**SOLUÇÃO:**
1. O `requirements.txt` já foi otimizado
2. Verifique se não há dependências duplicadas
3. Faça commit e push novamente
4. Se persistir, considere usar Plano Pro do Vercel

---

## 📋 Checklist Rápido

Antes de tentar novamente, verifique:

### Backend:
- [ ] `Back-end/requirements.txt` existe e está limpo ✅ (já corrigido)
- [ ] `Back-end/api/index.py` existe ✅
- [ ] `Back-end/vercel.json` existe ✅
- [ ] **Root Directory** = `Back-end` (verificar no Vercel)
- [ ] **Todas as variáveis de ambiente** configuradas no Vercel

### Variáveis de Ambiente (OBRIGATÓRIAS):
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_KEY`
- [ ] `GROQ_API_KEY`
- [ ] `JWT_SECRET_KEY`
- [ ] `JWT_ALGORITHM` (opcional, mas recomendado)

---

## 🚀 Próximos Passos

### 1. Commit das Correções

Fiz as seguintes correções:
- ✅ `requirements.txt` limpo e otimizado
- ✅ Removidas dependências duplicadas
- ✅ Removidas dependências desnecessárias

**Agora faça commit:**
```bash
git add Back-end/requirements.txt
git commit -m "Fix: Corrigir requirements.txt para deploy no Vercel"
git push
```

### 2. Verificar Configuração no Vercel

**No painel do Vercel:**

1. **Root Directory:**
   - Vá em **Settings > General**
   - Certifique-se de que está como `Back-end`

2. **Variáveis de Ambiente:**
   - Vá em **Settings > Environment Variables**
   - Certifique-se de que todas estão configuradas

3. **Redeploy:**
   - Vá em **Deployments**
   - Clique nos três pontos do último deployment
   - Clique em **Redeploy**

---

## 🔍 Identificar Erro Específico

**Me diga:**
1. Qual é a mensagem de erro exata? (copie dos logs)
2. O erro acontece em qual etapa?
   - Build?
   - Deploy?
   - Runtime?
3. Backend ou Frontend?

Com essas informações, posso ajudar a resolver o problema específico!

---

## 📚 Guias de Referência

- **Solução de Erros Detalhada:** `Back-end/SOLUCAO_ERROS_VERCEL.md`
- **Troubleshooting:** `Back-end/TROUBLESHOOTING_VERCEL.md`
- **Diagnóstico:** `Back-end/DIAGNOSTICO_ERRO.md`

---

## ✅ O Que Foi Corrigido

1. ✅ `requirements.txt` limpo e otimizado
2. ✅ Dependências duplicadas removidas
3. ✅ Dependências desnecessárias removidas
4. ✅ Guias de troubleshooting criados

**Agora tente fazer deploy novamente!**

Se ainda tiver erro, copie a mensagem de erro completa dos logs do Vercel e me mostre que eu ajudo a resolver! 🚀

