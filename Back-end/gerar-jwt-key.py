"""
Script para gerar JWT Secret Key
Execute: python gerar-jwt-key.py
"""
import secrets

print("Gerando JWT Secret Key...\n")
key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY gerada:")
print(key)
print("\nCopie o valor acima e cole no arquivo .env como JWT_SECRET_KEY")

