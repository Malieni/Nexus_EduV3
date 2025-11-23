# 🔧 Solução: ModuleNotFoundError no Vercel

## ❌ Erro
```
ModuleNotFoundError: No module named 'fastapi'
```

## 🔍 Causa

O Vercel não está encontrando o `requirements.txt` para instalar as dependências. Isso acontece porque:

1. O `requirements.txt` precisa estar na **mesma pasta** que o handler (`api/index.py`)
2. OU o Vercel precisa encontrar o `requirements.txt` na raiz do projeto configurado

## ✅ Solução

### Opção 1: requirements.txt na pasta api/ (Recomendado)

O `requirements.txt` deve estar em `Back-end/api/requirements.txt`:

```
Back-end/
├── api/
│   ├── index.py
│   └── requirements.txt  ← Aqui!
├── vercel.json
└── requirements.txt (opcional, backup)
```

### Opção 2: Verificar Root Directory no Vercel

1. No painel do Vercel, vá no projeto **Backend**
2. Clique em **Settings > General**
3. Verifique se o **Root Directory** está configurado como: `Back-end`
4. Se não estiver, configure e faça um **Redeploy**

---

## 📋 Checklist

- [x] `requirements.txt` está em `Back-end/api/requirements.txt`
- [ ] `requirements.txt` contém todas as dependências necessárias
- [ ] Root Directory está configurado como `Back-end` no Vercel
- [ ] Deploy foi feito após as alterações

---

## 🧪 Teste

Após o deploy, teste:

```
https://seu-backend.vercel.app/health
```

Deve retornar: `{"status": "ok"}`

---

## 🔄 Se ainda não funcionar

1. **Verifique os logs do build:**
   - No Vercel, vá em **Deployments**
   - Clique no deployment mais recente
   - Vá em **Build Logs**
   - Procure por mensagens sobre `requirements.txt`

2. **Verifique se o requirements.txt está correto:**
   ```bash
   cat Back-end/api/requirements.txt
   ```

3. **Tente forçar um rebuild sem cache:**
   - No Vercel, vá em **Deployments**
   - Clique nos três pontos (⋯) do último deployment
   - Clique em **Redeploy** (se houver opção para limpar cache, selecione)

