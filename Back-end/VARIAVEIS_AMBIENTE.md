# 📚 Explicação das Variáveis de Ambiente

Este documento explica para que serve cada variável de ambiente do projeto Nexus Education.

## 🔐 JWT_SECRET_KEY

### O que é?
A chave secreta usada para assinar e verificar os **tokens JWT** (JSON Web Tokens) de autenticação.

### Para que serve?
- **Assinar tokens**: Quando o usuário faz login, o sistema cria um token JWT usando esta chave
- **Verificar tokens**: Quando o usuário acessa rotas protegidas, o sistema verifica se o token é válido usando esta mesma chave
- **Segurança**: Garante que ninguém pode criar tokens falsos sem conhecer esta chave

### Onde é usado no código?

```33:36:Back-end/services/auth_service.py
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
```

```42:44:Back-end/services/auth_service.py
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
```

### Exemplo:
```env
JWT_SECRET_KEY=minha_chave_super_secreta_que_ninguem_deve_saber_1234567890abcdef
```

### ⚠️ Importante:
- **NUNCA** compartilhe esta chave publicamente
- Use uma string aleatória longa (mínimo 32 caracteres)
- Se ela vazar, todos os tokens existentes ficam comprometidos
- Gere uma nova se suspeitar de comprometimento

---

## 🔑 JWT_ALGORITHM

### O que é?
O algoritmo criptográfico usado para assinar e verificar os tokens JWT.

### Para que serve?
Define **como** o token será assinado criptograficamente. O algoritmo mais comum e seguro é `HS256` (HMAC com SHA-256).

### Opções disponíveis:
- `HS256`: Algoritmo simétrico (mais comum, recomendado)
- `HS384`: Versão mais forte do HS256
- `HS512`: Versão mais forte ainda
- `RS256`: Algoritmo assimétrico (mais complexo, para casos avançados)

### Onde é usado no código?

```33:35:Back-end/services/auth_service.py
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
```

```42:44:Back-end/services/auth_service.py
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
```

### Exemplo:
```env
JWT_ALGORITHM=HS256
```

### 💡 Recomendação:
Deixe como `HS256` (padrão). É seguro e eficiente para a maioria dos casos.

---

## 🌐 CORS_ORIGINS

### O que é?
**CORS** significa "Cross-Origin Resource Sharing" (Compartilhamento de Recursos entre Origens).

### Para que serve?
Define **quais URLs do frontend** podem fazer requisições para a API backend.

### Por que é necessário?
Por padrão, navegadores bloqueiam requisições de JavaScript entre domínios diferentes (por segurança). Por exemplo:
- **Frontend** está em: `http://localhost:5173` (Vite)
- **Backend** está em: `http://localhost:8000` (FastAPI)

Sem CORS configurado, o navegador bloqueia as requisições do frontend para o backend!

### Onde é usado no código?

```14:20:Back-end/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Exemplo:
```env
# Desenvolvimento local (múltiplas URLs separadas por vírgula)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Produção (URL do Vercel)
CORS_ORIGINS=https://nexus-education.vercel.app
```

### 📝 Formato:
- Separe múltiplas URLs por vírgula
- **Sem** barra no final (ex: `http://localhost:5173` ✓, não `http://localhost:5173/` ✗)
- Para desenvolvimento, inclua `http://localhost:5173` (Vite)
- Para produção, inclua a URL do seu site no Vercel

### ⚠️ Segurança:
- **NÃO** use `*` (asterisco) em produção (permite qualquer origem)
- Liste apenas as URLs que você realmente usa
- Se sua API for pública, você pode precisar de várias URLs

---

## 🔌 PORT

### O que é?
A porta TCP/IP onde o servidor da API vai escutar requisições.

### Para que serve?
Define em qual porta o backend FastAPI vai rodar. Quando você acessa `http://localhost:8000`, o `8000` é a porta.

### Exemplos de portas comuns:
- `3000`: React padrão
- `5173`: Vite padrão
- `8000`: FastAPI comum (padrão do projeto)
- `5000`: Flask comum
- `8080`: Alternativa comum

### Onde é usado?

A porta é usada quando você inicia o servidor:

```bash
poetry run uvicorn main:app --reload --port 8000
```

### Exemplo:
```env
PORT=8000
```

### 💡 Observações:
- Para desenvolvimento local, pode usar qualquer porta disponível (8000, 8001, etc.)
- Certifique-se de que a porta não está sendo usada por outro programa
- No Vercel, a porta é definida automaticamente (você pode ignorar essa variável em produção)

### 🔍 Verificar se porta está em uso (Windows):
```powershell
netstat -ano | findstr :8000
```

---

## 📊 Resumo

| Variável | Obrigatória? | Para que serve | Valor Exemplo |
|----------|--------------|----------------|---------------|
| `JWT_SECRET_KEY` | ✅ Sim | Assinar/verificar tokens de autenticação | String aleatória longa |
| `JWT_ALGORITHM` | ❌ Não | Algoritmo de criptografia (padrão: HS256) | `HS256` |
| `CORS_ORIGINS` | ❌ Não | URLs permitidas para acessar API | `http://localhost:5173` |
| `PORT` | ❌ Não | Porta do servidor (padrão: 8000) | `8000` |

## ✅ Configuração Mínima

Para o sistema funcionar, você precisa configurar pelo menos:

```env
# Obrigatórias
SUPABASE_URL=sua_url
SUPABASE_KEY=sua_chave
GROQ_API_KEY=sua_chave_groq
JWT_SECRET_KEY=sua_chave_secreta

# Opcionais (têm valores padrão)
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
PORT=8000
```

## 🆘 Problemas Comuns

### Erro: "Token inválido"
- Verifique se `JWT_SECRET_KEY` está configurada
- Certifique-se de usar a mesma chave em desenvolvimento e produção

### Erro: "CORS policy: No 'Access-Control-Allow-Origin' header"
- Verifique se `CORS_ORIGINS` inclui a URL do seu frontend
- Certifique-se de não ter barra no final da URL

### Erro: "Address already in use" (porta em uso)
- Mude o `PORT` para outra porta (ex: 8001)
- Ou feche o programa que está usando a porta

