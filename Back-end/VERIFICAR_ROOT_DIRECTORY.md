# 🔍 Verificar Root Directory no Vercel

## ❌ Problema Atual

O Vercel não está instalando as dependências do `requirements.txt`, resultando em `ModuleNotFoundError: No module named 'fastapi'`.

## 🔍 Possível Causa

O **Root Directory** pode não estar configurado corretamente no Vercel, fazendo com que o Vercel procure os arquivos no local errado.

## ✅ Solução

### 1. Verificar Root Directory no Vercel

1. No painel do Vercel, vá no seu projeto **Backend**
2. Clique em **Settings**
3. Clique em **General**
4. Role até a seção **Root Directory**
5. Verifique se está configurado como: `Back-end` (com hífen e maiúscula!)

### 2. Se não estiver configurado ou estiver incorreto:

1. Clique em **Edit** ao lado de **Root Directory**
2. Digite exatamente: `Back-end` (com hífen!)
3. Clique em **Save**
4. Vá em **Deployments**
5. Clique nos três pontos (⋯) do último deployment
6. Clique em **Redeploy**

### 3. Verificar se o requirements.txt está correto

O arquivo `Back-end/requirements.txt` deve existir e conter:

```txt
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

### 4. Verificar os logs do build

Após configurar o Root Directory e fazer o Redeploy:

1. Vá em **Deployments**
2. Clique no deployment mais recente
3. Clique em **Build Logs**
4. Procure por mensagens como:
   - "Installing dependencies..."
   - "Collecting fastapi..."
   - "Successfully installed fastapi..."

Se você **NÃO** ver essas mensagens, significa que o Vercel não está encontrando o `requirements.txt`.

---

## 📋 Checklist

- [ ] Root Directory configurado como `Back-end` no Vercel
- [ ] `Back-end/requirements.txt` existe e contém todas as dependências
- [ ] `Back-end/requirements.txt` está commitado no Git
- [ ] Foi feito um **Redeploy** após configurar o Root Directory
- [ ] Os logs do build mostram "Installing dependencies..."

---

## 🧪 Teste

Após configurar o Root Directory e fazer o Redeploy:

```
https://seu-backend.vercel.app/health
```

Deve retornar: `{"status": "ok"}`

---

## 🔄 Se ainda não funcionar

1. **Tente remover e adicionar o Root Directory novamente:**
   - Remova o Root Directory
   - Faça um deploy
   - Adicione o Root Directory novamente
   - Faça outro deploy

2. **Verifique se há problemas com o cache do Vercel:**
   - Ao fazer Redeploy, selecione a opção para limpar o cache (se disponível)

3. **Consulte os logs detalhados:**
   - No Vercel, vá em **Functions > [nome da função] > Logs**
   - Procure por mensagens de erro específicas

