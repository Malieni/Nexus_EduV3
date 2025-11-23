try:
    from supabase import create_client, Client
    from config import settings
except Exception as e:
    # Se falhar ao importar, cria classes stub para evitar crash
    print(f"AVISO: Erro ao importar em database.py: {e}")
    import traceback
    traceback.print_exc()
    
    class Client:
        pass
    
    class DummySettings:
        supabase_url = ""
        supabase_key = ""
    
    settings = DummySettings()


class Database:
    def __init__(self):
        # Não cria o cliente imediatamente para evitar erro se as variáveis não estiverem configuradas
        self._client = None
    
    def get_client(self) -> Client:
        # Cria o cliente apenas quando necessário (lazy initialization)
        if self._client is None:
            if not hasattr(settings, 'supabase_url') or not settings.supabase_url or not hasattr(settings, 'supabase_key') or not settings.supabase_key:
                raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configuradas nas variáveis de ambiente")
            from supabase import create_client
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return self._client


# Singleton instance - cria apenas se não houver erro
try:
    db = Database()
except Exception as e:
    print(f"AVISO: Erro ao criar instância de Database: {e}")
    import traceback
    traceback.print_exc()
    # Cria uma instância vazia para evitar crash
    db = Database()

