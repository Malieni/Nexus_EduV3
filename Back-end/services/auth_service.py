from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from typing import Optional
from config import settings
from database import db
from models import UserCreate, UserLogin, UserResponse
import secrets


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


async def register_user(user_data: UserCreate) -> UserResponse:
    """Registra novo usuário"""
    client = db.get_client()
    
    # Verifica se o usuário já existe
    existing = client.table("users").select("email").eq("email", user_data.email).execute()
    
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Hash da senha
    hashed_password = get_password_hash(user_data.password)
    
    # Insere usuário no Supabase
    user_record = {
        "email": user_data.email,
        "password": hashed_password,
        "name": user_data.name,
        "created_at": datetime.utcnow().isoformat()
    }
    
    result = client.table("users").insert(user_record).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )
    
    user = result.data[0]
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        created_at=datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")) if user.get("created_at") else None
    )


async def authenticate_user(credentials: UserLogin) -> UserResponse:
    """Autentica usuário"""
    client = db.get_client()
    
    # Busca usuário
    result = client.table("users").select("*").eq("email", credentials.email).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    user = result.data[0]
    
    # Verifica senha
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        created_at=datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")) if user.get("created_at") else None
    )


async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
    """Busca usuário por ID"""
    client = db.get_client()
    
    result = client.table("users").select("*").eq("id", user_id).execute()
    
    if not result.data:
        return None
    
    user = result.data[0]
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        created_at=datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")) if user.get("created_at") else None
    )

