"""
Vercel serverless handler para FastAPI
Este arquivo adapta a aplicação FastAPI para funcionar no Vercel

STRATÉGIA DE RESILIÊNCIA:
1. Todas as importações críticas têm try/except
2. O handler SEMPRE é criado, mesmo se houver erros parciais
3. Logs detalhados em cada etapa para diagnóstico
4. Fallbacks para tudo que pode falhar
"""
import sys
import os
import traceback
import json

print("=" * 80)
print("🚀 Iniciando carregamento do módulo api/index.py")
print("=" * 80)

# Adiciona o diretório pai ao path para importar módulos
# Isso é necessário porque o Vercel executa a partir de api/
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    print(f"✅ Adicionado ao sys.path: {backend_dir}")

# Variáveis globais - inicializadas como None
app = None
handler = None

# ============================================================================
# PASSO 1: Importar FastAPI e dependências básicas
# ============================================================================
try:
    print("📦 Tentando importar FastAPI...")
    from fastapi import FastAPI, HTTPException, status
    from fastapi.middleware.cors import CORSMiddleware
    from mangum import Mangum
    print("✅ FastAPI e dependências básicas importadas com sucesso")
except Exception as e:
    print(f"❌ ERRO CRÍTICO: Não foi possível importar FastAPI: {e}")
    traceback.print_exc()
    
    # Se nem o FastAPI funcionar, criamos um handler mínimo que retorna erro claro
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "FUNCTION_INVOCATION_FAILED",
                "message": "FastAPI não pôde ser importado. Verifique se as dependências estão instaladas.",
                "details": str(e)
            })
        }
else:
    # ============================================================================
    # PASSO 2: Criar aplicação FastAPI mínima
    # ============================================================================
    try:
        print("🔧 Criando aplicação FastAPI...")
        app = FastAPI(
            title="Nexus Education API",
            description="API para sistema de análise de ementas acadêmicas",
            version="0.1.0"
        )
        print("✅ Aplicação FastAPI criada")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação FastAPI: {e}")
        traceback.print_exc()
        app = FastAPI()  # Tenta criar app mínima
        
    # ============================================================================
    # PASSO 3: Configurar CORS (com fallback)
    # ============================================================================
    try:
        print("🌐 Configurando CORS...")
        cors_origins = ["*"]  # Padrão permissivo
        
        # Tenta carregar do config, mas não faz crash se falhar
        try:
            from config import settings
            if hasattr(settings, 'cors_origins_list'):
                cors_origins = settings.cors_origins_list.copy()
                print(f"✅ CORS carregado do config: {cors_origins}")
        except Exception as config_error:
            print(f"⚠️ Não foi possível carregar config para CORS: {config_error}")
            # Usa variáveis de ambiente diretamente
            cors_env = os.environ.get("CORS_ORIGINS", "")
            if cors_env:
                cors_origins = [origin.strip() for origin in cors_env.split(",")]
        
        # Permite URLs do Vercel automaticamente
        if os.environ.get("VERCEL_URL"):
            vercel_origin = f"https://{os.environ.get('VERCEL_URL')}"
            if vercel_origin not in cors_origins:
                cors_origins.append(vercel_origin)
        
        # Permite URL do frontend se configurada
        frontend_url = os.environ.get("FRONTEND_URL")
        if frontend_url and frontend_url not in cors_origins:
            cors_origins.append(frontend_url)
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("✅ CORS configurado")
    except Exception as e:
        print(f"⚠️ Erro ao configurar CORS: {e}")
        traceback.print_exc()
        # Continua sem CORS em vez de crashar
    
    # ============================================================================
    # PASSO 4: Registrar rotas (com fallback)
    # ============================================================================
    routes_loaded = False
    try:
        print("📦 Tentando importar e registrar rotas...")
        from routes import auth, analysis
        
        app.include_router(auth.router)
        app.include_router(analysis.router)
        
        routes_loaded = True
        print("✅ Rotas registradas com sucesso")
    except ImportError as e:
        print(f"⚠️ ERRO DE IMPORTAÇÃO ao carregar rotas: {e}")
        traceback.print_exc()
        
        # Tenta diagnosticar qual módulo está falhando
        modules_to_test = ["models", "services", "middleware", "database", "config"]
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"✅ Módulo {module_name} importável")
            except Exception as module_error:
                print(f"❌ Módulo {module_name} falhou: {module_error}")
        
        # Cria rotas de diagnóstico
        @app.get("/api/auth/status")
        async def auth_status():
            return {
                "status": "error",
                "message": "Rotas de autenticação não disponíveis",
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
        
        @app.get("/api/analysis/status")
        async def analysis_status():
            return {
                "status": "error",
                "message": "Rotas de análise não disponíveis",
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
    except Exception as e:
        print(f"⚠️ ERRO INESPERADO ao registrar rotas: {e}")
        traceback.print_exc()
    
    # ============================================================================
    # PASSO 5: Rotas básicas (sempre disponíveis)
    # ============================================================================
    @app.get("/")
    async def root():
        return {
            "message": "Nexus Education API",
            "version": "0.1.0",
            "status": "running",
            "routes_loaded": routes_loaded
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "routes_loaded": routes_loaded
        }
    
    # Handlers para favicon (evita 500 errors)
    @app.get("/favicon.ico")
    async def favicon_ico():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favicon not found")
    
    @app.get("/favicon.png")
    async def favicon_png():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favicon not found")
    
    # ============================================================================
    # PASSO 6: Criar handler Mangum
    # ============================================================================
    try:
        print("🔧 Criando handler Mangum...")
        handler = Mangum(app, lifespan="off")
        print("✅ Handler Mangum criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar handler Mangum: {e}")
        traceback.print_exc()
        # Cria handler mínimo como último recurso
        def handler(event, context):
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": "Handler não pôde ser criado",
                    "details": str(e)
                })
            }

# ============================================================================
# PASSO 7: Garantir que handler sempre existe
# ============================================================================
if handler is None:
    print("⚠️ Handler não foi criado! Criando handler de emergência...")
    try:
        # Tenta criar uma app mínima e handler
        app = FastAPI()
        @app.get("/")
        async def root():
            return {
                "error": "FUNCTION_INVOCATION_FAILED",
                "message": "Handler não foi inicializado corretamente",
                "instruction": "Verifique os logs do Vercel para mais detalhes"
            }
        handler = Mangum(app, lifespan="off")
        print("✅ Handler de emergência criado")
    except Exception as e:
        print(f"❌ Erro ao criar handler de emergência: {e}")
        traceback.print_exc()
        # Último recurso - handler puro
        def handler(event, context):
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "FUNCTION_INVOCATION_FAILED",
                    "message": "Erro crítico na inicialização do módulo",
                    "instruction": "Verifique os logs do Vercel"
                })
            }

print("=" * 80)
print("✅ Módulo api/index.py carregado com sucesso")
print(f"✅ Handler criado: {handler is not None}")
print(f"✅ App criada: {app is not None if 'app' in globals() else False}")
print("=" * 80)
