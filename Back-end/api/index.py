"""
Vercel serverless handler para FastAPI
ESTRATÉGIA: Handler mínimo que SEMPRE funciona, mesmo se tudo mais falhar

DIAGNÓSTICO: Build Logs mostram que dependências estão sendo "instaladas" 
mas não há confirmação de instalação bem-sucedida. Este handler tem logs
detalhados para identificar exatamente onde está falhando.
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
                "python_version": sys.version.split()[0] if hasattr(sys, 'version') else "unknown",
                "sys_path": sys.path[:3] if hasattr(sys, 'path') else []  # Primeiros 3 itens para debug
            })
        }
    return emergency_handler

# Handler padrão de emergência (criado ANTES de qualquer coisa)
handler = create_emergency_handler("Tentando inicializar módulo...")

# ============================================================================
# PASSO 1: Logs iniciais e configuração de sys.path
# ============================================================================
try:
    print("=" * 80)
    print("🚀 INICIANDO CARREGAMENTO DO MÓDULO api/index.py")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script path: {__file__}")
    
    # Configurar sys.path ANTES de qualquer importação
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Backend directory: {backend_dir}")
    print(f"Sys.path before: {sys.path[:3]}")
    
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
        print(f"✅ Added {backend_dir} to sys.path")
    
    print(f"Sys.path after: {sys.path[:3]}")
except Exception as e:
    print(f"❌ ERRO ao configurar sys.path: {e}")
    traceback.print_exc()
    # Continua mesmo se falhar

# ============================================================================
# PASSO 2: Tentar importar FastAPI com diagnóstico detalhado
# ============================================================================
app = None
FastAPI_available = False
CORSMiddleware_available = False
Mangum_available = False
import_errors = []

try:
    print("\n📦 PASSO 2: Tentando importar FastAPI...")
    from fastapi import FastAPI
    FastAPI_available = True
    print("✅ FastAPI importado com sucesso")
except ImportError as e:
    import_errors.append(f"FastAPI ImportError: {e}")
    print(f"❌ FastAPI ImportError: {e}")
    traceback.print_exc()
    # Verifica se o módulo existe no sys.path
    print(f"Verificando módulos disponíveis em sys.path...")
    for path in sys.path[:3]:
        fastapi_path = os.path.join(path, 'fastapi')
        print(f"  Checking {fastapi_path}: {os.path.exists(fastapi_path)}")
except Exception as e:
    import_errors.append(f"FastAPI Exception: {e}")
    print(f"❌ FastAPI Exception: {e}")
    traceback.print_exc()

# Se FastAPI não estiver disponível, atualiza handler de emergência
if not FastAPI_available:
    error_msg = "FastAPI não disponível. " + "; ".join(import_errors)
    handler = create_emergency_handler(error_msg)
    print(f"⚠️ Usando handler de emergência: {error_msg}")
else:
    # Tenta importar outras dependências
    try:
        print("📦 Tentando importar CORSMiddleware...")
        from fastapi.middleware.cors import CORSMiddleware
        CORSMiddleware_available = True
        print("✅ CORSMiddleware importado com sucesso")
    except Exception as e:
        print(f"⚠️ CORSMiddleware não disponível: {e}")
        traceback.print_exc()
    
    try:
        print("📦 Tentando importar Mangum...")
        from mangum import Mangum
        Mangum_available = True
        print("✅ Mangum importado com sucesso")
    except Exception as e:
        print(f"❌ Mangum não disponível: {e}")
        traceback.print_exc()
        Mangum_available = False

# ============================================================================
# PASSO 3: Criar aplicação FastAPI (se possível)
# ============================================================================
if FastAPI_available and not app:
    try:
        print("\n🔧 PASSO 3: Criando aplicação FastAPI...")
        app = FastAPI(
            title="Nexus Education API",
            description="API para sistema de análise de ementas acadêmicas",
            version="0.1.0"
        )
        print("✅ Aplicação FastAPI criada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação FastAPI: {e}")
        traceback.print_exc()
        try:
            app = FastAPI()
            print("✅ Aplicação FastAPI mínima criada")
        except Exception as e2:
            print(f"❌ Erro ao criar app mínima: {e2}")
            app = None

# ============================================================================
# PASSO 4: Configurar CORS (se possível)
# ============================================================================
if app and CORSMiddleware_available:
    try:
        print("\n🌐 PASSO 4: Configurando CORS...")
        cors_origins = ["*"]
        
        # Tenta carregar do config
        try:
            from config import settings
            if hasattr(settings, 'cors_origins_list'):
                cors_origins = settings.cors_origins_list.copy()
                print(f"✅ CORS carregado do config: {cors_origins}")
        except Exception as config_error:
            print(f"⚠️ Não foi possível carregar config: {config_error}")
            # Usa variáveis de ambiente diretamente
            cors_env = os.environ.get("CORS_ORIGINS", "")
            if cors_env:
                cors_origins = [origin.strip() for origin in cors_env.split(",")]
                print(f"✅ CORS carregado de variáveis de ambiente: {cors_origins}")
        
        # Adiciona URLs do Vercel
        if os.environ.get("VERCEL_URL"):
            vercel_origin = f"https://{os.environ.get('VERCEL_URL')}"
            if vercel_origin not in cors_origins:
                cors_origins.append(vercel_origin)
                print(f"✅ Adicionada URL do Vercel: {vercel_origin}")
        
        if os.environ.get("FRONTEND_URL"):
            frontend_url = os.environ.get("FRONTEND_URL")
            if frontend_url not in cors_origins:
                cors_origins.append(frontend_url)
                print(f"✅ Adicionada URL do frontend: {frontend_url}")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("✅ CORS configurado com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao configurar CORS: {e}")
        traceback.print_exc()
        # Continua sem CORS

# ============================================================================
# PASSO 5: Registrar rotas (se possível)
# ============================================================================
routes_loaded = False
if app:
    try:
        print("\n📦 PASSO 5: Tentando registrar rotas...")
        from routes import auth, analysis
        app.include_router(auth.router)
        app.include_router(analysis.router)
        routes_loaded = True
        print("✅ Rotas registradas com sucesso")
    except ImportError as e:
        print(f"⚠️ Erro de importação ao carregar rotas: {e}")
        traceback.print_exc()
        # Tenta diagnosticar qual módulo está falhando
        modules_to_test = ["models", "services", "middleware", "database", "config"]
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"  ✅ {module_name} importável")
            except Exception as module_error:
                print(f"  ❌ {module_name} falhou: {module_error}")
        # Cria rotas de diagnóstico
        try:
            @app.get("/api/auth/status")
            async def auth_status():
                return {"status": "error", "message": "Rotas não carregadas", "error": str(e)}
            
            @app.get("/api/analysis/status")
            async def analysis_status():
                return {"status": "error", "message": "Rotas não carregadas", "error": str(e)}
        except Exception:
            pass
    except Exception as e:
        print(f"⚠️ Erro inesperado ao registrar rotas: {e}")
        traceback.print_exc()

# ============================================================================
# PASSO 6: Rotas básicas (sempre disponíveis se app existe)
# ============================================================================
if app:
    try:
        print("\n🔧 PASSO 6: Criando rotas básicas...")
        
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
        
        @app.get("/health")
        async def health():
            return {
                "status": "ok",
                "routes_loaded": routes_loaded,
                "fastapi_available": FastAPI_available
            }
        
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
        
        print("✅ Rotas básicas criadas")
    except Exception as e:
        print(f"⚠️ Erro ao criar rotas básicas: {e}")
        traceback.print_exc()

# ============================================================================
# PASSO 7: Criar handler Mangum (se tudo estiver disponível)
# ============================================================================
if app and Mangum_available:
    try:
        print("\n🔧 PASSO 7: Criando handler Mangum...")
        handler = Mangum(app, lifespan="off")
        print("✅ Handler Mangum criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar handler Mangum: {e}")
        traceback.print_exc()
        # Handler de fallback
        def handler(event, context):
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
    print("⚠️ Handler não foi criado! Criando handler de emergência...")
    handler = create_emergency_handler("Handler não foi criado corretamente")

print("\n" + "=" * 80)
print("✅ MÓDULO api/index.py CARREGADO")
print(f"  Handler criado: {handler is not None}")
print(f"  App criada: {app is not None if 'app' in globals() else False}")
print(f"  FastAPI disponível: {FastAPI_available}")
print(f"  Mangum disponível: {Mangum_available}")
print(f"  Rotas carregadas: {routes_loaded}")
print("=" * 80)
