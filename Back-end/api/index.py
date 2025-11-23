"""
Vercel serverless handler para FastAPI
Este arquivo adapta a aplicação FastAPI para funcionar no Vercel
"""
import sys
import os

# Adiciona o diretório pai ao path para importar módulos
# Isso é necessário porque o Vercel executa a partir de api/
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Agora podemos importar os módulos
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from config import settings
    from routes import auth, analysis
    from mangum import Mangum
except Exception as e:
    # Se houver erro de import, vamos criar uma app básica para debug
    print(f"ERRO AO IMPORTAR MÓDULOS: {e}")
    from fastapi import FastAPI
    from mangum import Mangum
    
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"error": f"Erro ao carregar módulos: {str(e)}"}
    
    handler = Mangum(app, lifespan="off")
else:
    # Cria a aplicação FastAPI
    app = FastAPI(
        title="Nexus Education API",
        description="API para sistema de análise de ementas acadêmicas",
        version="0.1.0"
    )
    
    # CORS - Configuração dinâmica para produção
    try:
        cors_origins = settings.cors_origins_list.copy()
    except Exception as e:
        print(f"ERRO AO CARREGAR CORS: {e}")
        cors_origins = ["*"]  # Fallback para permitir todas as origens
    
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
    
    # Routes
    try:
        app.include_router(auth.router)
        app.include_router(analysis.router)
    except Exception as e:
        print(f"ERRO AO REGISTRAR ROTAS: {e}")
        import traceback
        traceback.print_exc()
    
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

