"""
Teste mínimo para verificar se o handler funciona
Este arquivo testa se as dependências básicas estão disponíveis
"""
import sys

print("Python version:", sys.version)
print("Python path:", sys.path[:3])

try:
    import fastapi
    print("✅ FastAPI disponível:", fastapi.__version__)
except ImportError as e:
    print("❌ FastAPI NÃO disponível:", e)

try:
    import mangum
    print("✅ Mangum disponível:", mangum.__version__)
except ImportError as e:
    print("❌ Mangum NÃO disponível:", e)

try:
    from config import settings
    print("✅ Config disponível")
except ImportError as e:
    print("❌ Config NÃO disponível:", e)

print("✅ Teste concluído")

