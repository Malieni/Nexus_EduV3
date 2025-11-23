"""
Vercel serverless handler para FastAPI
VERSÃO ULTRA-MÍNIMA: Handler que SEMPRE funciona, mesmo se nada mais funcionar

ESTRATÉGIA:
- Handler criado imediatamente, antes de qualquer importação
- Nenhuma importação no nível superior (exceto stdlib)
- Tudo é importado dentro do handler quando necessário
- Captura TODOS os erros possíveis
"""
import sys
import os
import json

# ============================================================================
# HANDLER MÍNIMO ABSOLUTO - Criado ANTES de qualquer coisa
# ============================================================================
def handler(event, context):
    """
    Handler que SEMPRE funciona, mesmo se todas as dependências falharem.
    Tenta carregar FastAPI e criar app apenas quando necessário.
    """
    try:
        # Tenta importar FastAPI dentro do handler (lazy loading)
        try:
            from fastapi import FastAPI
            from mangum import Mangum
            from fastapi.middleware.cors import CORSMiddleware
            
            # Verifica se app já existe (singleton)
            if not hasattr(handler, '_app'):
                # Cria app apenas uma vez
                handler._app = FastAPI(
                    title="Nexus Education API",
                    version="0.1.0"
                )
                
                # Configura CORS
                try:
                    cors_origins = ["*"]
                    
                    # Tenta carregar do config
                    try:
                        from config import settings
                        if hasattr(settings, 'cors_origins_list'):
                            cors_origins = settings.cors_origins_list.copy()
                    except Exception:
                        # Usa variáveis de ambiente
                        cors_env = os.environ.get("CORS_ORIGINS", "")
                        if cors_env:
                            cors_origins = [origin.strip() for origin in cors_env.split(",")]
                    
                    # Adiciona URLs do Vercel
                    if os.environ.get("VERCEL_URL"):
                        vercel_origin = f"https://{os.environ.get('VERCEL_URL')}"
                        if vercel_origin not in cors_origins:
                            cors_origins.append(vercel_origin)
                    
                    if os.environ.get("FRONTEND_URL"):
                        frontend_url = os.environ.get("FRONTEND_URL")
                        if frontend_url not in cors_origins:
                            cors_origins.append(frontend_url)
                    
                    handler._app.add_middleware(
                        CORSMiddleware,
                        allow_origins=cors_origins,
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"],
                    )
                except Exception:
                    pass  # Continua sem CORS
                
                # Rotas básicas
                @handler._app.get("/")
                async def root():
                    return {
                        "message": "Nexus Education API",
                        "version": "0.1.0",
                        "status": "running"
                    }
                
                @handler._app.get("/health")
                async def health():
                    return {"status": "ok"}
                
                # Tenta registrar rotas
                try:
                    from routes import auth, analysis
                    handler._app.include_router(auth.router)
                    handler._app.include_router(analysis.router)
                except Exception:
                    # Rotas não disponíveis, mas continua funcionando
                    pass
                
                # Handler Mangum
                handler._mangum = Mangum(handler._app, lifespan="off")
            
            # Usa o handler Mangum para processar a requisição
            return handler._mangum(event, context)
            
        except ImportError as e:
            # FastAPI não disponível - retorna erro detalhado
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": "FastAPI não está disponível. Dependências podem não ter sido instaladas.",
                    "import_error": str(e),
                    "python_version": sys.version.split()[0],
                    "sys_path": sys.path[:5],
                    "instruction": "Verifique se as dependências foram instaladas durante o build."
                }, indent=2)
            }
        except Exception as e:
            # Qualquer outro erro
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": f"Erro ao inicializar handler: {str(e)}",
                    "error_type": type(e).__name__,
                    "python_version": sys.version.split()[0],
                    "instruction": "Verifique os logs do Vercel para mais detalhes."
                }, indent=2)
            }
    except Exception as e:
        # Último recurso - erro crítico
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "FUNCTION_INVOCATION_FAILED",
                "message": f"Erro crítico no handler: {str(e)}",
                "error_type": type(e).__name__,
                "instruction": "Verifique os logs do Vercel para mais detalhes."
            }, indent=2)
        }
