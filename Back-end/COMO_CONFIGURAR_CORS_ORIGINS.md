# 🔧 Como Configurar CORS_ORIGINS no Vercel

## 🔍 O que é CORS_ORIGINS?

`CORS_ORIGINS` é a lista de **URLs que são permitidas acessar seu backend**. Basicamente, é o **endereço do seu frontend**.

## ✅ O que colocar em CORS_ORIGINS?

### 1. URL do Frontend no Vercel

Depois de publicar o frontend no Vercel, você terá uma URL como:
- `https://nexus-education-frontend.vercel.app`
- `https://nexus-education-frontend-git-main.vercel.app`

### 2. Formato da Variável

No Vercel, configure `CORS_ORIGINS` com a URL do seu frontend:

**Valor:**
```
https://seu-frontend.vercel.app
```

**OU se tiver múltiplas URLs (produção + preview):**
```
https://seu-frontend.vercel.app,https://seu-frontend-git-main.vercel.app
```

## 📋 Passo a Passo

### 1. Publicar o Frontend no Vercel

1. Conecte o repositório ao Vercel
2. Configure o **Root Directory** como `Front-end`
3. Configure as variáveis de ambiente (incluindo `VITE_API_URL`)
4. Faça o deploy
5. **Anote a URL** que aparece (ex: `https://nexus-education-frontend.vercel.app`)

### 2. Configurar CORS_ORIGINS no Backend

1. No painel do Vercel, vá no projeto **Backend**
2. Vá em **Settings > Environment Variables**
3. Clique em **Add New**
4. Preencha:
   - **Key:** `CORS_ORIGINS`
   - **Value:** `https://seu-frontend.vercel.app` (URL do seu frontend!)
   - **Environment:** Selecione **Production**, **Preview** e **Development**
5. Clique em **Save**

### 3. Redeploy do Backend

1. Vá em **Deployments**
2. Clique nos três pontos (⋯) do último deployment
3. Clique em **Redeploy**

## 🧪 Exemplo Completo

### Seu Frontend está em:
```
https://nexus-education-frontend.vercel.app
```

### Configure CORS_ORIGINS como:
```
https://nexus-education-frontend.vercel.app
```

### Ou se quiser permitir múltiplas URLs:
```
https://nexus-education-frontend.vercel.app,https://nexus-education-frontend-git-main.vercel.app,http://localhost:5173
```

## ⚠️ Importante

1. **Não coloque espaços** entre as URLs
2. **Use vírgulas** para separar múltiplas URLs
3. **Use https://** para produção (não http://)
4. **Não inclua a barra final** (não coloque `/` no final)

## ✅ Exemplo Correto

```
https://nexus-education-frontend.vercel.app
```

## ❌ Exemplo Incorreto

```
https://nexus-education-frontend.vercel.app/  ← Barra final
https://nexus-education-frontend.vercel.app, ← Vírgula final
 http://nexus-education-frontend.vercel.app   ← Espaços
```

## 🔄 Se não souber a URL do Frontend

1. Publique o frontend no Vercel primeiro
2. A URL aparecerá após o deploy
3. Depois configure o `CORS_ORIGINS` no backend com essa URL
4. Faça um Redeploy do backend

## 🎯 Resumo

- **CORS_ORIGINS** = URL do seu frontend no Vercel
- Exemplo: `https://nexus-education-frontend.vercel.app`
- Configure no Vercel: Settings > Environment Variables
- Faça um Redeploy do backend após configurar

