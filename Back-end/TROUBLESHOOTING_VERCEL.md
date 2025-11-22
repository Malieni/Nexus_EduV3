# 🐛 Troubleshooting - Erros no Deploy do Vercel

Guia rápido para resolver erros comuns.

## ⚡ Solução Rápida

### Se o erro é "Module not found":

1. Verifique se o `requirements.txt` está completo
2. Limpe dependências duplicadas
3. Certifique-se de que está na pasta `Back-end/`

### Se o erro é "Environment variable":

1. Vá em Settings > Environment Variables
2. Adicione todas as variáveis necessárias
3. Faça um Redeploy

### Se o erro é "Root Directory":

1. Vá em Settings > General
2. Configure Root Directory como `Back-end` ou `Front-end`
3. Faça um novo deploy

---

## 🔍 Como Ver os Logs de Erro

1. No painel do Vercel
2. Clique no deployment que falhou
3. Veja a seção **"Build Logs"** ou **"Function Logs"**
4. Procure por linhas em vermelho

---

## 📝 Erros Mais Comuns

| Erro | Solução |
|------|---------|
| ModuleNotFoundError | Adicione a dependência no `requirements.txt` |
| ImportError | Verifique se os arquivos estão nas pastas corretas |
| Environment variable not found | Configure as variáveis no Vercel |
| Root Directory not found | Configure o Root Directory como `Back-end` ou `Front-end` |
| Build timeout | Simplifique as dependências ou use Plano Pro |
| 404 Not Found | Verifique o `vercel.json` |

---

## ✅ Checklist Rápido

Antes de reportar um erro, verifique:

- [ ] `requirements.txt` está completo?
- [ ] Variáveis de ambiente configuradas?
- [ ] Root Directory configurado corretamente?
- [ ] Arquivos nas pastas corretas?

---

Para mais detalhes, veja: `SOLUCAO_ERROS_VERCEL.md`

