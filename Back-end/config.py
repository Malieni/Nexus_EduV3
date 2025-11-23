from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # Groq
    groq_api_key: str
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Server
    port: int = 8000
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # No Vercel, as variáveis vêm do ambiente, não do arquivo .env
        # Mas ainda tenta carregar do .env se existir localmente


# Tenta criar settings, mas trata erros de forma mais amigável
try:
    settings = Settings()
except Exception as e:
    # Se falhar, imprime informações de debug mas NÃO faz crash
    import sys
    print(f"ERRO ao carregar Settings: {e}")
    print("Variáveis de ambiente disponíveis:")
    for key in ["SUPABASE_URL", "SUPABASE_KEY", "GROQ_API_KEY", "JWT_SECRET_KEY"]:
        value = os.environ.get(key)
        if value:
            print(f"  {key}: {'*' * min(len(value), 10)} (presente)")
        else:
            print(f"  {key}: (AUSENTE)")
    
    # Em vez de fazer crash, cria um objeto Settings vazio com valores padrão
    # Isso permite que a aplicação inicie mesmo sem todas as variáveis
    class DummySettings:
        supabase_url: str = ""
        supabase_key: str = ""
        groq_api_key: str = ""
        jwt_secret_key: str = ""
        jwt_algorithm: str = "HS256"
        cors_origins: str = "*"
        port: int = 8000
        
        @property
        def cors_origins_list(self) -> List[str]:
            return ["*"] if self.cors_origins == "*" else [origin.strip() for origin in self.cors_origins.split(",")]
    
    settings = DummySettings()  # type: ignore
    print("AVISO: Usando configurações padrão. A aplicação pode não funcionar corretamente.")

