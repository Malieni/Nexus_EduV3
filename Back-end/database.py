from supabase import create_client, Client
from config import settings


class Database:
    def __init__(self):
        # Não cria o cliente imediatamente para evitar erro se as variáveis não estiverem configuradas
        self._client: Client | None = None
    
    def get_client(self) -> Client:
        # Cria o cliente apenas quando necessário (lazy initialization)
        if self._client is None:
            if not settings.supabase_url or not settings.supabase_key:
                raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configuradas nas variáveis de ambiente")
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return self._client


# Singleton instance
db = Database()

