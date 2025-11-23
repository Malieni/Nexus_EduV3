# 🔧 Solução: Vercel não instala dependências do requirements.txt

## ❌ Problema

O Vercel não está instalando as dependências do `requirements.txt`, resultando em `ModuleNotFoundError: No module named 'fastapi'`.

## 🔍 Causa

O Vercel procura o `requirements.txt` em locais específicos:

1. **Na raiz do projeto configurado** (onde o Root Directory aponta)
2. **Na mesma pasta do handler** (`api/`)

Com o Root Directory configurado como `Back-end`, o Vercel procura em:
- `Back-end/requirements.txt` ✅ (deve existir)
- `Back-end/api/requirements.txt` ✅ (pode existir também)

## ✅ Solução

### 1. Verificar se o `requirements.txt` está na raiz do projeto

O arquivo `Back-end/requirements.txt` deve existir e conter todas as dependências:

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

### 2. Verificar Root Directory no Vercel

1. No painel do Vercel, vá no projeto **Backend**
2. Clique em **Settings > General**
3. Verifique se o **Root Directory** está configurado como: `Back-end`
4. Se não estiver, configure e faça um **Redeploy**

### 3. Verificar os logs do build

No Vercel, vá em **Deployments > [último deployment] > Build Logs** e procure por:

```
Installing dependencies...
Collecting fastapi...
Successfully installed fastapi...
```

Se você **NÃO** ver essas mensagens, significa que o Vercel não está encontrando o `requirements.txt`.

### 4. Garantir que o `requirements.txt` está commitado

Verifique se o arquivo está no Git:

```bash
git ls-files | grep requirements.txt
```

Deve mostrar:
```
Back-end/requirements.txt
Back-end/api/requirements.txt
```

### 5. Se ainda não funcionar, tente forçar o build

1. No Vercel, vá em **Deployments**
2. Clique nos três pontos (⋯) do último deployment
3. Clique em **Redeploy** (se houver opção para limpar cache, selecione)

---

## 📋 Checklist Final

- [ ] `Back-end/requirements.txt` existe e contém todas as dependências
- [ ] `Back-end/requirements.txt` está commitado no Git
- [ ] Root Directory está configurado como `Back-end` no Vercel
- [ ] Os logs do build mostram "Installing dependencies..."
- [ ] Foi feito um Redeploy após as alterações

---

## 🧪 Teste

Após o deploy, teste:

```
https://seu-backend.vercel.app/health
```

Deve retornar: `{"status": "ok"}`

---

## 🔄 Se ainda não funcionar

1. **Verifique se o Vercel detectou o Python:**
   - Nos logs do build, procure por "Detected Python"
   - Se não aparecer, o Vercel pode não estar reconhecendo o projeto como Python

2. **Tente usar a estrutura recomendada do Vercel:**
   - O `requirements.txt` deve estar na **raiz do Root Directory** configurado
   - Se o Root Directory é `Back-end`, então `Back-end/requirements.txt` deve existir

3. **Verifique se há problemas com as versões das dependências:**
   - Algumas versões podem ser incompatíveis com o Python 3.12 do Vercel
   - Tente usar versões mais recentes ou mais antigas

4. **Consulte os logs de erro detalhados:**
   - No Vercel, vá em **Functions > [nome da função] > Logs**
   - Procure por mensagens de erro específicas

