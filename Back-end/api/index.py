"""
Vercel serverless handler para FastAPI
ESTRATÉGIA: Handler mínimo que SEMPRE funciona, mesmo se tudo mais falhar
"""
import sys
import os
import traceback
import json

# ============================================================================
# HANDLER DE EMERGÊNCIA - Criado PRIMEIRO para garantir que sempre existe
# ============================================================================
def create_emergency_handler(error_message=None):
    """Cria um handler de emergência que sempre funciona"""
    def emergency_handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "FUNCTION_INVOCATION_FAILED",
                "message": error_message or "Erro durante inicialização do módulo",
                "instruction": "Verifique os logs do Vercel para mais detalhes",
                "python_version": sys.version,
                "sys_path": sys.path[:3]  # Primeiros 3 itens para debug
            })
        }
    return emergency_handler

# Handler padrão de emergência
handler = create_emergency_handler("Tentando inicializar módulo...")

# ============================================================================
# PASSO 1: Configurar sys.path ANTES de qualquer importação
# ============================================================================
try:
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
except Exception as e:
    # Se falhar ao configurar path, ainda podemos continuar
    pass

# ============================================================================
# PASSO 2: Tentar importar FastAPI com tratamento EXTREMAMENTE robusto
# ============================================================================
app = None
FastAPI_available = False
CORSMiddleware_available = False
Mangum_available = False

try:
    from fastapi import FastAPI
    FastAPI_available = True
except Exception as e:
    # FastAPI não disponível - usar handler de emergência
    handler = create_emergency_handler(f"FastAPI não disponível: {str(e)}")
    
if FastAPI_available:
    try:
        from fastapi.middleware.cors import CORSMiddleware
        CORSMiddleware_available = True
    except Exception:
        pass  # Continua sem CORS
    
    try:
        from mangum import Mangum
        Mangum_available = True
    except Exception as e:
        # Mangum não disponível - criar handler básico
        handler = create_emergency_handler(f"Mangum não disponível: {str(e)}")
        Mangum_available = False

# ============================================================================
# PASSO 3: Criar aplicação FastAPI (se possível)
# ============================================================================
if FastAPI_available and not app:
    try:
        app = FastAPI(
            title="Nexus Education API",
            description="API para sistema de análise de ementas acadêmicas",
            version="0.1.0"
        )
    except Exception as e:
        # Se falhar, tenta criar app mínima
        try:
            app = FastAPI()
        except Exception:
            app = None

# ============================================================================
# PASSO 4: Configurar CORS (se possível)
# ============================================================================
if app and CORSMiddleware_available:
    try:
        cors_origins = ["*"]
        
        # Tenta carregar do config
        try:
            from config import settings
            if hasattr(settings, 'cors_origins_list'):
                cors_origins = settings.cors_origins_list.copy()
        except Exception:
            # Se falhar, tenta variáveis de ambiente
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
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    except Exception:
        # Se CORS falhar, continua sem CORS
        pass

# ============================================================================
# PASSO 5: Registrar rotas (se possível)
# ============================================================================
routes_loaded = False
if app:
    try:
        from routes import auth, analysis
        app.include_router(auth.router)
        app.include_router(analysis.router)
        routes_loaded = True
    except Exception:
        # Se rotas falharem, cria rotas de diagnóstico
        try:
            @app.get("/api/auth/status")
            async def auth_status():
                return {"status": "error", "message": "Rotas não carregadas"}
            
            @app.get("/api/analysis/status")
            async def analysis_status():
                return {"status": "error", "message": "Rotas não carregadas"}
        except Exception:
            pass

# ============================================================================
# PASSO 6: Rotas básicas (sempre disponíveis se app existe)
# ============================================================================
if app:
    try:
        @app.get("/")
        async def root():
            return {
                "message": "Nexus Education API",
                "version": "0.1.0",
                "status": "running",
                "routes_loaded": routes_loaded,
                "fastapi_available": FastAPI_available,
                "mangum_available": Mangum_available
            }
    except Exception:
        pass
    
    try:
        @app.get("/health")
        async def health():
            return {
                "status": "ok",
                "routes_loaded": routes_loaded,
                "fastapi_available": FastAPI_available
            }
    except Exception:
        pass
    
    # Handlers para favicon
    try:
        from fastapi import HTTPException, status
        
        @app.get("/favicon.ico")
        async def favicon_ico():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        @app.get("/favicon.png")
        async def favicon_png():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        pass

# ============================================================================
# PASSO 7: Criar handler Mangum (se tudo estiver disponível)
# ============================================================================
if app and Mangum_available:
    try:
        handler = Mangum(app, lifespan="off")
    except Exception as e:
        # Se Mangum falhar, cria handler básico que usa FastAPI diretamente
        def handler(event, context):
            # Tenta usar uvicorn em modo básico ou retorna erro
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "Mangum handler não disponível",
                    "details": str(e),
                    "app_created": app is not None
                })
            }

# ============================================================================
# VERIFICAÇÃO FINAL: Garantir que handler sempre existe
# ============================================================================
if handler is None or not callable(handler):
    # Último recurso - handler puro que sempre funciona
    handler = create_emergency_handler("Handler não foi criado corretamente")
