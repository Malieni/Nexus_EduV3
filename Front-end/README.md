# Nexus Education - Frontend

Frontend React para o sistema Nexus Education, desenvolvido com Vite.

## Configuração

### 1. Instalar dependências

```bash
cd Front-end
npm install
```

### 2. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com a URL da API:
```
VITE_API_URL=http://localhost:8000
```

### 3. Executar em desenvolvimento

```bash
npm run dev
```

O aplicativo estará disponível em `http://localhost:5173`

### 4. Build para produção

```bash
npm run build
```

Os arquivos de produção estarão na pasta `dist/`

## Estrutura

- `src/pages/` - Páginas principais (Login, Register, AreaPrincipal)
- `src/components/` - Componentes reutilizáveis
- `src/contexts/` - Contextos React (AuthContext)
- `src/services/` - Serviços de API

## Funcionalidades

- Autenticação (Login/Cadastro)
- Área restrita com controle de acesso
- Dashboard com estatísticas
- Upload e análise de PDFs
- Tabela de histórico de análises
- Menu lateral com configurações e políticas
- Logout

