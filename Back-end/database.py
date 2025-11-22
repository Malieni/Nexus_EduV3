from supabase import create_client, Client
from config import settings


class Database:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    def get_client(self) -> Client:
        return self.client


# Singleton instance
db = Database()

