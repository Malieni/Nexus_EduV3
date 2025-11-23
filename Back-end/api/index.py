"""
Vercel serverless handler para FastAPI
ESTRATÉGIA: Handler mínimo que SEMPRE funciona, mesmo se tudo mais falhar

DIAGNÓSTICO: Build Logs mostram "Installing dependencies" mas não confirmam
instalação. Este handler verifica se dependências estão disponíveis e fornece
diagnóstico detalhado.
"""
import sys
import os
import traceback
import json

# ============================================================================
# HANDLER DE EMERGÊNCIA - Criado PRIMEIRO para garantir que sempre existe
# ============================================================================
def create_emergency_handler(error_message=None, diagnostic_info=None):
    """Cria um handler de emergência que sempre funciona"""
    def emergency_handler(event, context):
        response = {
            "error": "FUNCTION_INVOCATION_FAILED",
            "message": error_message or "Erro durante inicialização do módulo",
            "instruction": "Verifique os logs do Vercel para mais detalhes",
            "python_version": sys.version.split()[0] if hasattr(sys, 'version') else "unknown",
            "sys_path": sys.path[:5] if hasattr(sys, 'path') else []  # Primeiros 5 itens
        }
        if diagnostic_info:
            response["diagnostic"] = diagnostic_info
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response, indent=2)
        }
    return emergency_handler

# Handler padrão de emergência (criado ANTES de qualquer coisa)
handler = create_emergency_handler("Tentando inicializar módulo...")

# ============================================================================
# PASSO 1: Logs iniciais e diagnóstico do ambiente
# ============================================================================
diagnostic_info = {
    "step": "initialization",
    "errors": [],
    "available_modules": [],
    "missing_modules": []
}

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
    print(f"Sys.path (first 5): {sys.path[:5]}")
    
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
        print(f"✅ Added {backend_dir} to sys.path")
    
    # Verifica se diretórios de módulos existem
    diagnostic_info["sys_path"] = sys.path[:5]
    diagnostic_info["backend_dir"] = backend_dir
    
except Exception as e:
    error_msg = f"Erro ao configurar sys.path: {e}"
    print(f"❌ {error_msg}")
    traceback.print_exc()
    diagnostic_info["errors"].append(error_msg)

# ============================================================================
# PASSO 2: Verificar disponibilidade de módulos Python padrão
# ============================================================================
print("\n📦 PASSO 2: Verificando módulos Python padrão...")
standard_modules = ["json", "os", "sys", "traceback"]
for module_name in standard_modules:
    try:
        __import__(module_name)
        diagnostic_info["available_modules"].append(module_name)
        print(f"  ✅ {module_name} disponível")
    except Exception as e:
        diagnostic_info["missing_modules"].append(module_name)
        print(f"  ❌ {module_name} NÃO disponível: {e}")

# ============================================================================
# PASSO 3: Tentar importar FastAPI com diagnóstico detalhado
# ============================================================================
app = None
FastAPI_available = False
CORSMiddleware_available = False
Mangum_available = False

print("\n📦 PASSO 3: Tentando importar FastAPI...")
try:
    # Primeiro, verifica se o diretório fastapi existe em algum lugar do sys.path
    fastapi_found = False
    for path in sys.path:
        fastapi_path = os.path.join(path, 'fastapi')
        if os.path.exists(fastapi_path) or os.path.exists(fastapi_path + '.py'):
            print(f"  ✅ Encontrado fastapi em: {path}")
            fastapi_found = True
            break
    
    if not fastapi_found:
        print("  ⚠️ Diretório 'fastapi' não encontrado em nenhum sys.path")
        print("  Verificando sys.path completo:")
        for i, path in enumerate(sys.path[:10]):  # Primeiros 10
            print(f"    {i}: {path}")
            if os.path.exists(path):
                contents = os.listdir(path)[:5]  # Primeiros 5 itens
                print(f"      Conteúdo: {contents}")
    
    # Tenta importar
    from fastapi import FastAPI
    FastAPI_available = True
    diagnostic_info["available_modules"].append("fastapi")
    print("✅ FastAPI importado com sucesso")
except ImportError as e:
    error_msg = f"FastAPI ImportError: {e}"
    diagnostic_info["errors"].append(error_msg)
    diagnostic_info["missing_modules"].append("fastapi")
    print(f"❌ {error_msg}")
    traceback.print_exc()
    # Atualiza handler com diagnóstico
    handler = create_emergency_handler(
        "FastAPI não disponível. Dependências podem não ter sido instaladas.",
        diagnostic_info
    )
except Exception as e:
    error_msg = f"FastAPI Exception: {e}"
    diagnostic_info["errors"].append(error_msg)
    print(f"❌ {error_msg}")
    traceback.print_exc()

# Se FastAPI estiver disponível, tenta outras dependências
if FastAPI_available:
    try:
        print("📦 Tentando importar CORSMiddleware...")
        from fastapi.middleware.cors import CORSMiddleware
        CORSMiddleware_available = True
        diagnostic_info["available_modules"].append("fastapi.middleware.cors")
        print("✅ CORSMiddleware importado com sucesso")
    except Exception as e:
        print(f"⚠️ CORSMiddleware não disponível: {e}")
        traceback.print_exc()
    
    try:
        print("📦 Tentando importar Mangum...")
        from mangum import Mangum
        Mangum_available = True
        diagnostic_info["available_modules"].append("mangum")
        print("✅ Mangum importado com sucesso")
    except Exception as e:
        error_msg = f"Mangum não disponível: {e}"
        diagnostic_info["errors"].append(error_msg)
        diagnostic_info["missing_modules"].append("mangum")
        print(f"❌ {error_msg}")
        traceback.print_exc()
        Mangum_available = False

# ============================================================================
# PASSO 4: Criar aplicação FastAPI (se possível)
# ============================================================================
if FastAPI_available and not app:
    try:
        print("\n🔧 PASSO 4: Criando aplicação FastAPI...")
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
# PASSO 5: Configurar CORS (se possível)
# ============================================================================
if app and CORSMiddleware_available:
    try:
        print("\n🌐 PASSO 5: Configurando CORS...")
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

# ============================================================================
# PASSO 6: Registrar rotas (se possível)
# ============================================================================
routes_loaded = False
if app:
    try:
        print("\n📦 PASSO 6: Tentando registrar rotas...")
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
                diagnostic_info["available_modules"].append(module_name)
            except Exception as module_error:
                print(f"  ❌ {module_name} falhou: {module_error}")
                diagnostic_info["missing_modules"].append(module_name)
        # Cria rotas de diagnóstico
        try:
            @app.get("/api/auth/status")
            async def auth_status():
                return {
                    "status": "error",
                    "message": "Rotas não carregadas",
                    "error": str(e),
                    "diagnostic": diagnostic_info
                }
            
            @app.get("/api/analysis/status")
            async def analysis_status():
                return {
                    "status": "error",
                    "message": "Rotas não carregadas",
                    "error": str(e),
                    "diagnostic": diagnostic_info
                }
        except Exception:
            pass
    except Exception as e:
        print(f"⚠️ Erro inesperado ao registrar rotas: {e}")
        traceback.print_exc()

# ============================================================================
# PASSO 7: Rotas básicas (sempre disponíveis se app existe)
# ============================================================================
if app:
    try:
        print("\n🔧 PASSO 7: Criando rotas básicas...")
        
        @app.get("/")
        async def root():
            return {
                "message": "Nexus Education API",
                "version": "0.1.0",
                "status": "running",
                "routes_loaded": routes_loaded,
                "fastapi_available": FastAPI_available,
                "mangum_available": Mangum_available,
                "diagnostic": diagnostic_info
            }
        
        @app.get("/health")
        async def health():
            return {
                "status": "ok",
                "routes_loaded": routes_loaded,
                "fastapi_available": FastAPI_available,
                "diagnostic": diagnostic_info
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
# PASSO 8: Criar handler Mangum (se tudo estiver disponível)
# ============================================================================
if app and Mangum_available:
    try:
        print("\n🔧 PASSO 8: Criando handler Mangum...")
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
                    "app_created": app is not None,
                    "diagnostic": diagnostic_info
                }, indent=2)
            }

# ============================================================================
# VERIFICAÇÃO FINAL: Garantir que handler sempre existe
# ============================================================================
if handler is None or not callable(handler):
    print("⚠️ Handler não foi criado! Criando handler de emergência...")
    diagnostic_info["step"] = "final_check"
    diagnostic_info["errors"].append("Handler não foi criado corretamente")
    handler = create_emergency_handler("Handler não foi criado corretamente", diagnostic_info)

print("\n" + "=" * 80)
print("✅ MÓDULO api/index.py CARREGADO")
print(f"  Handler criado: {handler is not None}")
print(f"  App criada: {app is not None if 'app' in globals() else False}")
print(f"  FastAPI disponível: {FastAPI_available}")
print(f"  Mangum disponível: {Mangum_available}")
print(f"  Rotas carregadas: {routes_loaded}")
print(f"  Módulos disponíveis: {len(diagnostic_info.get('available_modules', []))}")
print(f"  Módulos faltando: {len(diagnostic_info.get('missing_modules', []))}")
print("=" * 80)
