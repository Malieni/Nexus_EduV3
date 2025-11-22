from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import auth, analysis


app = FastAPI(
    title="Nexus Education API",
    description="API para sistema de análise de ementas acadêmicas",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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

