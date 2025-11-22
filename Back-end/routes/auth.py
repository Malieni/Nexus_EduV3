from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, UserLogin, TokenResponse, UserResponse
from services.auth_service import register_user, authenticate_user, create_access_token
from middleware import get_current_user
from datetime import timedelta


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Endpoint para cadastro de novo usuário"""
    try:
        user = await register_user(user_data)
        
        # Gera token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(hours=24)
        )
        
        return TokenResponse(
            access_token=access_token,
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar usuário: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Endpoint para login"""
    try:
        user = await authenticate_user(credentials)
        
        # Gera token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(hours=24)
        )
        
        return TokenResponse(
            access_token=access_token,
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao fazer login: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Endpoint para obter informações do usuário autenticado"""
    return current_user

