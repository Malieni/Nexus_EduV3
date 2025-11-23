"""
Vercel serverless handler para FastAPI
VERSÃO ABSOLUTAMENTE MÍNIMA: Apenas o handler, sem nenhuma lógica extra
"""
import json

def handler(event, context):
    """
    Handler que SEMPRE funciona, mesmo se todas as dependências falharem.
    """
    try:
        # Tenta importar FastAPI
        try:
            from fastapi import FastAPI
            from mangum import Mangum
            from fastapi.middleware.cors import CORSMiddleware
            
            # Cria app se não existir
            if not hasattr(handler, '_app'):
                handler._app = FastAPI(title="Nexus Education API")
                
                # CORS
                try:
                    import os
                    cors_origins = ["*"]
                    if os.environ.get("VERCEL_URL"):
                        cors_origins.append(f"https://{os.environ.get('VERCEL_URL')}")
                    if os.environ.get("FRONTEND_URL"):
                        cors_origins.append(os.environ.get("FRONTEND_URL"))
                    
                    handler._app.add_middleware(
                        CORSMiddleware,
                        allow_origins=cors_origins,
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"],
                    )
                except Exception:
                    pass
                
                # Rotas básicas
                @handler._app.get("/")
                async def root():
                    return {"message": "Nexus Education API", "status": "running"}
                
                @handler._app.get("/health")
                async def health():
                    return {"status": "ok"}
                
                # Tenta rotas
                try:
                    import sys
                    import os
                    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    if backend_dir not in sys.path:
                        sys.path.insert(0, backend_dir)
                    from routes import auth, analysis
                    handler._app.include_router(auth.router)
                    handler._app.include_router(analysis.router)
                except Exception:
                    pass
                
                handler._mangum = Mangum(handler._app, lifespan="off")
            
            return handler._mangum(event, context)
        except ImportError as e:
            # Dependências não disponíveis
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": "Dependências não estão disponíveis",
                    "import_error": str(e),
                    "instruction": "Verifique se o requirements.txt foi instalado durante o build."
                })
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": f"Erro: {str(e)}",
                    "error_type": type(e).__name__
                })
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "FUNCTION_INVOCATION_FAILED",
                "message": f"Erro crítico: {str(e)}"
            })
        }
