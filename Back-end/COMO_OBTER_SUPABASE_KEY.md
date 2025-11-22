# 🔑 Como Obter a SUPABASE_KEY

Guia passo a passo para obter a chave do Supabase e configurar no arquivo `.env`.

## 📋 Passo a Passo

### 1️⃣ Acessar o Supabase

1. Acesse [https://app.supabase.com](https://app.supabase.com)
2. Faça login ou crie uma conta (é grátis)

### 2️⃣ Criar um Projeto (se ainda não tiver)

1. No painel do Supabase, clique em **"New Project"**
2. Preencha os dados:
   - **Name**: Nome do seu projeto (ex: "nexus-education")
   - **Database Password**: Crie uma senha forte (guarde ela!)
   - **Region**: Escolha a região mais próxima de você
3. Clique em **"Create new project"**
4. Aguarde alguns minutos para o projeto ser criado

### 3️⃣ Encontrar a SUPABASE_KEY

1. No painel do projeto, localize o menu lateral **esquerdo**
2. Clique no ícone de **engrenagem (⚙️)** na parte inferior esquerda
3. No menu que abrir, clique em **"API"**
4. Você verá uma página com várias configurações da API

### 4️⃣ Copiar as Credenciais

Na página de API, você verá duas informações importantes:

#### **Project URL** (SUPABASE_URL)
- Fica em uma caixa com o título **"Project URL"**
- É algo como: `https://xxxxxxxxxxxxx.supabase.co`
- **Esta é a URL que você coloca em `SUPABASE_URL`**

#### **anon public key** (SUPABASE_KEY)
- Fica logo abaixo, em uma caixa com o título **"Project API keys"**
- Procure por **"anon"** ou **"public"** key
- É uma string longa que começa com `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **Esta é a chave que você coloca em `SUPABASE_KEY`**

### 5️⃣ Copiar a Chave

1. Clique no botão de **cópia** (ícone de copiar) ao lado da chave `anon public`
2. Ou selecione todo o texto e copie (Ctrl+C)

---

## 📝 Exemplo Visual

Na página de API do Supabase, você verá algo assim:

```
┌─────────────────────────────────────────┐
│ Project URL                             │
│ https://abcdefghijkl.supabase.co        │
│                                         │
│ Project API keys                        │
│                                         │
│ anon public                             │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... │  ← Esta é a SUPABASE_KEY
│ [ícone de copiar]                       │
└─────────────────────────────────────────┘
```

---

## ✅ Adicionar no .env

Depois de copiar, adicione no arquivo `Back-end/.env`:

```env
SUPABASE_URL=https://abcdefghijkl.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbCIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjE2MjM5MDIyfQ...
```

---

## ⚠️ Importante

### Qual chave usar?
- Use a chave **"anon public"** (pública)
- **NÃO** use a chave **"service_role"** (privada, só para backend)
- A chave `anon` é segura para o frontend e backend

### Segurança
- A chave `anon public` é segura para usar no frontend
- Ela respeita as políticas de segurança (Row Level Security) do Supabase
- Mantenha-a em segredo mesmo assim

---

## 🆘 Não consegue encontrar?

Se não conseguir encontrar:

1. **Verifique se está no projeto correto**
   - No canto superior esquerdo do Supabase, verifique o nome do projeto

2. **Verifique o menu lateral**
   - Clique no ícone de engrenagem (⚙️) na parte inferior esquerda
   - Clique em **"API"** (não "General" ou "Database")

3. **Screenshot da localização:**
   ```
   Painel Supabase
   ├── Table Editor
   ├── SQL Editor
   ├── Authentication
   ├── ...
   └── ⚙️ Settings
       └── API  ← Clique aqui!
   ```

---

## 📚 Mais Informações

- Documentação Supabase: [https://supabase.com/docs](https://supabase.com/docs)
- Guia de API Keys: [https://supabase.com/docs/guides/api](https://supabase.com/docs/guides/api)

---

## ✅ Depois de Configurar

Após obter e configurar as chaves, não esqueça de:

1. ✅ Criar as tabelas no Supabase (veja `CONFIGURACAO.md`)
2. ✅ Configurar as outras variáveis do `.env`
3. ✅ Testar a conexão

---

## 🎯 Resumo

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Vá em **Settings > API**
3. Copie o **Project URL** → `SUPABASE_URL`
4. Copie a chave **anon public** → `SUPABASE_KEY`
5. Cole no arquivo `.env`

Pronto! 🎉

