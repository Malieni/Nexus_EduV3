"""
Vercel serverless handler para FastAPI
Este arquivo adapta a aplicação FastAPI para funcionar no Vercel
"""
import sys
import os
import traceback

# Configura logging para debug
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("=" * 80)
print("🚀 Iniciando carregamento do módulo api/index.py")
print("=" * 80)
print(f"📁 Diretório atual: {os.getcwd()}")
print(f"📁 Arquivo atual: {__file__}")

# Adiciona o diretório pai ao path para importar módulos
# Isso é necessário porque o Vercel executa a partir de api/
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"📁 Backend dir: {backend_dir}")
print(f"📁 Sys.path antes: {sys.path}")

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    
print(f"📁 Sys.path depois: {sys.path}")

# Captura TODOS os erros possíveis durante a inicialização
app = None
handler = None

try:
    # Tenta importar FastAPI primeiro
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from mangum import Mangum
    print("✅ FastAPI importado com sucesso")
except Exception as e:
    print(f"❌ ERRO CRÍTICO ao importar FastAPI: {e}")
    traceback.print_exc()
    # Se falhar completamente, cria handler mínimo
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Erro crítico: {str(e)}"
        }
else:
    try:
        # Tenta importar config com tratamento de erros
        try:
            from config import settings
            print("✅ Config importado com sucesso")
        except Exception as e:
            print(f"⚠️ AVISO: Erro ao importar config: {e}")
            traceback.print_exc()
            # Cria settings padrão
            class Settings:
                cors_origins = "*"
                @property
                def cors_origins_list(self):
                    return ["*"]
            settings = Settings()
            print("✅ Usando configurações padrão")
        
        # Cria a aplicação FastAPI
        app = FastAPI(
            title="Nexus Education API",
            description="API para sistema de análise de ementas acadêmicas",
            version="0.1.0"
        )
        print("✅ Aplicação FastAPI criada")
        
        # CORS - Configuração dinâmica para produção
        try:
            cors_origins = settings.cors_origins_list.copy() if hasattr(settings, 'cors_origins_list') else ["*"]
        except Exception as e:
            print(f"⚠️ Erro ao carregar CORS: {e}")
            cors_origins = ["*"]
        
        # Permite a URL do Vercel automaticamente
        if os.environ.get("VERCEL_URL"):
            vercel_origin = f"https://{os.environ.get('VERCEL_URL')}"
            if vercel_origin not in cors_origins:
                cors_origins.append(vercel_origin)
        
        # Permite também a URL do frontend se estiver configurada
        frontend_url = os.environ.get("FRONTEND_URL")
        if frontend_url and frontend_url not in cors_origins:
            cors_origins.append(frontend_url)
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("✅ CORS configurado")
        
        # Routes - Tenta registrar as rotas, mas não faz crash se falhar
        # Importa cada módulo individualmente para identificar problemas
        routes_loaded = False
        try:
            print("📦 Tentando importar módulo routes.auth...")
            from routes import auth
            print("✅ routes.auth importado")
            
            print("📦 Tentando importar módulo routes.analysis...")
            from routes import analysis
            print("✅ routes.analysis importado")
            
            print("📦 Registrando router auth...")
            app.include_router(auth.router)
            print("✅ Router auth registrado")
            
            print("📦 Registrando router analysis...")
            app.include_router(analysis.router)
            print("✅ Router analysis registrado")
            
            routes_loaded = True
            print("✅ Todas as rotas registradas com sucesso")
        except ImportError as e:
            print(f"❌ ERRO DE IMPORTAÇÃO ao registrar rotas: {e}")
            traceback.print_exc()
            # Tenta importar dependências individuais para identificar o problema
            try:
                print("🔍 Tentando importar models...")
                import models
                print("✅ models importado")
            except Exception as models_error:
                print(f"❌ Erro ao importar models: {models_error}")
                traceback.print_exc()
            
            try:
                print("🔍 Tentando importar services...")
                import services
                print("✅ services importado")
            except Exception as services_error:
                print(f"❌ Erro ao importar services: {services_error}")
                traceback.print_exc()
            
            try:
                print("🔍 Tentando importar middleware...")
                import middleware
                print("✅ middleware importado")
            except Exception as middleware_error:
                print(f"❌ Erro ao importar middleware: {middleware_error}")
                traceback.print_exc()
            
            # Cria rotas básicas para indicar o problema
            @app.get("/api/auth/status")
            async def auth_status():
                return {"error": "Rotas de autenticação não disponíveis", "details": str(e), "type": type(e).__name__}
            
            @app.get("/api/analysis/status")
            async def analysis_status():
                return {"error": "Rotas de análise não disponíveis", "details": str(e), "type": type(e).__name__}
        except Exception as e:
            print(f"❌ ERRO INESPERADO ao registrar rotas: {e}")
            traceback.print_exc()
            # Cria rotas básicas para indicar o problema
            @app.get("/api/auth/status")
            async def auth_status():
                return {"error": "Rotas de autenticação não disponíveis", "details": str(e), "type": type(e).__name__}
            
            @app.get("/api/analysis/status")
            async def analysis_status():
                return {"error": "Rotas de análise não disponíveis", "details": str(e), "type": type(e).__name__}
        
        # Rotas básicas
        @app.get("/")
        async def root():
            return {"message": "Nexus Education API", "version": "0.1.0"}
        
        @app.get("/health")
        async def health():
            return {"status": "ok"}
        
        @app.get("/favicon.ico")
        async def favicon():
            """Endpoint para favicon - retorna 404 em vez de erro 500"""
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favicon not found")
        
        @app.get("/favicon.png")
        async def favicon_png():
            """Endpoint para favicon.png - retorna 404 em vez de erro 500"""
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favicon not found")
        
        # Handler para Vercel serverless usando Mangum
        handler = Mangum(app, lifespan="off")
        print("✅ Handler Mangum criado com sucesso")
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO durante inicialização: {e}")
        traceback.print_exc()
        # Se algo der errado, cria uma app mínima
        try:
            app = FastAPI()
            @app.get("/")
            async def root():
                return {"error": f"Erro na inicialização: {str(e)}"}
            handler = Mangum(app, lifespan="off")
        except Exception as critical_error:
            print(f"❌ ERRO CRÍTICO TOTAL: {critical_error}")
            traceback.print_exc()
            # Último recurso - handler básico
            def handler(event, context):
                return {
                    "statusCode": 500,
                    "body": f"Erro crítico: {str(critical_error)}"
                }

# Garante que handler existe
if handler is None:
    print("❌ Handler não foi criado! Criando handler de emergência...")
    try:
        # Tenta criar uma app mínima
        app = FastAPI()
        @app.get("/")
        async def root():
            return {"error": "Handler não foi inicializado corretamente", "message": "Verifique os logs"}
        handler = Mangum(app, lifespan="off")
        print("✅ Handler de emergência criado")
    except Exception as e:
        print(f"❌ Erro ao criar handler de emergência: {e}")
        traceback.print_exc()
        def handler(event, context):
            return {
                "statusCode": 500,
                "body": "Erro: Handler não foi inicializado corretamente"
            }

print("=" * 80)
print("✅ Módulo api/index.py carregado com sucesso")
print(f"✅ Handler criado: {handler is not None}")
print(f"✅ App criada: {app is not None if 'app' in globals() else False}")
print("=" * 80)
