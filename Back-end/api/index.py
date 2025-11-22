"""
Vercel serverless handler para FastAPI
Este arquivo adapta a aplicação FastAPI para funcionar no Vercel
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import auth, analysis
from mangum import Mangum
import sys
import os

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cria a aplicação FastAPI
app = FastAPI(
    title="Nexus Education API",
    description="API para sistema de análise de ementas acadêmicas",
    version="0.1.0"
)

# CORS - Configuração dinâmica para produção
cors_origins = settings.cors_origins_list.copy()
# Permite a URL do Vercel automaticamente
if os.environ.get("VERCEL_URL"):
    vercel_origin = f"https://{os.environ.get('VERCEL_URL')}"
    if vercel_origin not in cors_origins:
        cors_origins.append(vercel_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(analysis.router)


@app.get("/")
async def root():
    return {"message": "Nexus Education API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# Handler para Vercel serverless usando Mangum
handler = Mangum(app, lifespan="off")

