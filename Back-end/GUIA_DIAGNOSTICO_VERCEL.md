# 🔍 Guia de Diagnóstico: FUNCTION_INVOCATION_FAILED

## 🎯 Problema

Você está recebendo `FUNCTION_INVOCATION_FAILED` com `Python process exited with exit status: 1`, mesmo após múltiplas tentativas de correção.

## 🔍 Diagnóstico Passo a Passo

### PASSO 1: Verificar Build Logs no Vercel

**IMPORTANTE:** O erro provavelmente está acontecendo porque as dependências NÃO estão sendo instaladas durante o build.

#### Como Verificar:

1. No Vercel, vá em **Deployments**
2. Clique no **deployment mais recente** (que falhou)
3. Clique em **Build Logs** (NÃO Function Logs!)
4. Procure por estas mensagens:

#### ✅ Se está CORRETO, você verá:

```
Installing dependencies...
Collecting fastapi==0.121.3
Collecting uvicorn[standard]==0.38.0
...
Successfully installed fastapi-0.121.3 uvicorn-0.38.0 ...
```

#### ❌ Se está ERRADO, você verá:

- **NENHUMA mensagem** sobre "Installing dependencies..."
- **OU** mensagens como "requirements.txt not found"
- **OU** apenas "Build Completed" sem instalação de dependências

### PASSO 2: Verificar Root Directory

1. No Vercel, vá em **Settings > General**
2. Verifique o campo **Root Directory**:
   - Deve ser exatamente: `Back-end` (com maiúscula B e hífen)
   - **NÃO** deve ser: `Back-end/` (sem barra no final)
   - **NÃO** deve estar vazio

3. Se estiver incorreto:
   - Corrija para `Back-end`
   - Salve
   - Faça um **Redeploy** completo

### PASSO 3: Verificar Estrutura do Projeto

Execute este comando localmente:

```bash
git ls-files | grep requirements.txt
```

Deve mostrar:
```
Back-end/requirements.txt
Back-end/api/requirements.txt
```

Se **NÃO** mostrar esses arquivos:
- Os arquivos não estão commitados
- Faça: `git add Back-end/requirements.txt Back-end/api/requirements.txt`
- Faça commit e push

### PASSO 4: Verificar Conteúdo do requirements.txt

Verifique se o arquivo `Back-end/requirements.txt` contém:

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

### PASSO 5: Verificar vercel.json

O arquivo `Back-end/vercel.json` deve estar assim:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

## 🔧 Soluções Possíveis

### Solução 1: Recriar o Projeto no Vercel

Se os Build Logs **NÃO** mostram instalação de dependências:

1. No Vercel, vá em **Settings > General**
2. Anote todas as **Environment Variables**
3. **Delete o projeto** (ou desconecte do GitHub)
4. **Crie um novo projeto** conectando ao mesmo repositório
5. Configure o **Root Directory** como `Back-end`
6. Adicione todas as **Environment Variables** novamente
7. Faça o deploy

### Solução 2: Forçar Instalação de Dependências

Crie um arquivo `Back-end/.vercelignore` que **NÃO** ignore o `requirements.txt`:

```bash
# Não ignore requirements.txt
# node_modules/
# .git/
```

### Solução 3: Usar Build Command Explícito

Adicione um build command explícito no `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

**E também configure no Vercel:**
- Settings > General > Build & Development Settings
- Build Command: `pip install -r requirements.txt`
- Install Command: (deixe vazio)
- Output Directory: (deixe vazio)

## 📊 O Que Me Enviar

Para eu poder ajudar melhor, preciso que você envie:

1. **Build Logs completos** (não apenas Function Logs)
   - Deployments > [último deployment] > Build Logs
   - Copie TUDO desde o início do build até o final

2. **Screenshot ou texto** das configurações do projeto:
   - Settings > General > Root Directory
   - Settings > General > Build & Development Settings

3. **Resultado do comando:**
   ```bash
   git ls-files | grep requirements.txt
   ```

4. **Function Logs** (se disponível):
   - Functions > [nome da função] > Logs
   - Isso mostra o que acontece quando o código é executado

## 🎯 Próximos Passos

1. **Verifique os Build Logs** primeiro
2. **Me envie** os logs completos
3. Com base nos logs, aplicaremos a solução específica

**O problema mais provável é:** O Vercel não está instalando as dependências durante o build. Os Build Logs confirmarão isso.

