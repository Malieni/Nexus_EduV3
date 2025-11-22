# 🔧 Solução de Erros no Deploy do Vercel

Guia para resolver os erros mais comuns ao fazer deploy no Vercel.

## 🔍 Como Identificar o Erro

1. No painel do Vercel, vá em **Deployments**
2. Clique no deployment que falhou
3. Vá em **"Build Logs"** ou **"Function Logs"**
4. Procure por mensagens de erro em vermelho

---

## ❌ Erros Comuns e Soluções

### 1. Erro: "ModuleNotFoundError" ou "No module named 'X'"

**Causa:** Dependência faltando no `requirements.txt`

**Solução:**
1. Verifique se o `requirements.txt` está na pasta `Back-end/`
2. Verifique se todas as dependências estão listadas
3. O arquivo deve ter pelo menos:
   ```
   fastapi==0.104.1
   mangum==0.17.0
   supabase==2.0.3
   groq==0.4.0
   python-dotenv==1.0.0
   ```

**Como corrigir:**
- Edite o `Back-end/requirements.txt`
- Adicione as dependências faltantes
- Faça commit e push:
  ```bash
  git add Back-end/requirements.txt
  git commit -m "Fix: Adicionar dependências faltantes"
  git push
  ```
- O Vercel fará um novo deploy automaticamente

---

### 2. Erro: "Cannot find module" ou "ImportError"

**Causa:** Problema com paths de importação no Vercel

**Solução:**
1. Verifique se o arquivo `Back-end/api/index.py` existe
2. Verifique se o `vercel.json` está configurado corretamente

**Como corrigir:**
- O arquivo `api/index.py` deve estar em: `Back-end/api/index.py`
- O `vercel.json` deve estar em: `Back-end/vercel.json`

---

### 3. Erro: "Environment variable not found"

**Causa:** Variáveis de ambiente não configuradas no Vercel

**Solução:**
1. No painel do Vercel, vá no projeto
2. Clique em **Settings > Environment Variables**
3. Verifique se TODAS estas variáveis estão configuradas:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GROQ_API_KEY`
   - `JWT_SECRET_KEY`
   - `JWT_ALGORITHM` (opcional, padrão: HS256)
   - `CORS_ORIGINS` (opcional)
   - `PORT` (opcional)

**Como corrigir:**
1. Adicione as variáveis faltantes
2. Clique em **Save**
3. Vá em **Deployments**
4. Clique nos três pontos do último deployment
5. Clique em **Redeploy**

---

### 4. Erro: "Unable to resolve root directory" ou "Root Directory not found"

**Causa:** Root Directory configurado incorretamente no Vercel

**Solução:**
1. No painel do Vercel, vá no projeto
2. Clique em **Settings**
3. Clique em **General**
4. Verifique o **Root Directory**:
   - **Backend:** deve ser `Back-end` (com hífen!)
   - **Frontend:** deve ser `Front-end` (com hífen!)

**Como corrigir:**
1. Edite o Root Directory
2. Digite exatamente: `Back-end` ou `Front-end`
3. Clique em **Save**
4. Faça um novo deploy

---

### 5. Erro: "Build failed" ou "Build timeout"

**Causa:** Build muito lento ou com muitas dependências

**Solução:**
1. Verifique os logs do build
2. Veja qual etapa está travando
3. Pode ser problema com dependências pesadas

**Como corrigir:**
- Simplifique o `requirements.txt` (remova dependências não usadas)
- Verifique se não há dependências duplicadas
- Se necessário, aumente o timeout no Vercel (Plano Pro)

---

### 6. Erro: "Handler not found" ou "Function error"

**Causa:** Problema com o handler do Vercel

**Solução:**
Verifique se o arquivo `Back-end/api/index.py` termina com:

```python
handler = Mangum(app, lifespan="off")
```

**Como corrigir:**
1. Verifique se `mangum` está no `requirements.txt`
2. Verifique se o `api/index.py` está correto
3. Faça commit e push novamente

---

### 7. Erro: "404 Not Found" após deploy bem-sucedido

**Causa:** Rotas não configuradas corretamente

**Solução:**
Verifique o `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
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

**Como corrigir:**
- Certifique-se de que o `vercel.json` está na pasta `Back-end/`
- Verifique se o caminho está correto

---

### 8. Erro: "Configuration error" no frontend

**Causa:** `VITE_API_URL` não configurada ou incorreta

**Solução:**
1. No projeto frontend no Vercel
2. Vá em **Settings > Environment Variables**
3. Verifique se `VITE_API_URL` está configurada
4. Deve ser a URL completa do backend:
   ```
   https://nexus-education-api.vercel.app
   ```

**Como corrigir:**
- Adicione ou atualize `VITE_API_URL`
- Certifique-se de usar `https://` (não `http://`)
- Não adicione barra no final (`/`)
- Faça um redeploy do frontend

---

## 📋 Checklist de Verificação

Antes de fazer deploy, verifique:

### Backend:
- [ ] Arquivo `Back-end/requirements.txt` existe e tem todas as dependências
- [ ] Arquivo `Back-end/api/index.py` existe
- [ ] Arquivo `Back-end/vercel.json` existe
- [ ] Root Directory configurado como `Back-end`
- [ ] Todas as variáveis de ambiente configuradas no Vercel
- [ ] `mangum` está no `requirements.txt`

### Frontend:
- [ ] Arquivo `Front-end/package.json` existe
- [ ] Arquivo `Front-end/vercel.json` existe
- [ ] Root Directory configurado como `Front-end`
- [ ] `VITE_API_URL` configurada no Vercel

---

## 🔄 Processo de Correção Padrão

1. **Identifique o erro** nos logs do Vercel
2. **Encontre a solução** na lista acima
3. **Corrija o problema** no código ou configuração
4. **Faça commit e push:**
   ```bash
   git add .
   git commit -m "Fix: Descrição do problema corrigido"
   git push
   ```
5. **O Vercel fará um novo deploy automaticamente**
6. **Verifique os logs** novamente

---

## 🆘 Erro Não Listado?

Se o erro não está na lista:

1. **Copie a mensagem de erro completa** dos logs
2. **Verifique:**
   - Se todas as dependências estão no `requirements.txt`
   - Se as variáveis de ambiente estão configuradas
   - Se o Root Directory está correto
   - Se os arquivos estão nas pastas corretas

3. **Teste localmente:**
   - Execute o backend localmente para ver se funciona
   - Se funcionar localmente, o problema é de configuração do Vercel

---

## 📞 Ajuda Adicional

Se ainda tiver problemas:

1. Verifique a documentação do Vercel: [vercel.com/docs](https://vercel.com/docs)
2. Veja os logs completos no painel do Vercel
3. Teste o backend localmente primeiro

---

## ✅ Deploy Bem-Sucedido

Após resolver os erros, você deve ver:

- ✅ **Build successful**
- ✅ **Deployment ready**
- ✅ API respondendo em `/health`
- ✅ Documentação em `/docs`

🎉 **Parabéns! Seu sistema está funcionando!**

