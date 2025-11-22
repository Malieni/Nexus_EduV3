from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AnalysisCreate(BaseModel):
    student_name: str
    pdf_content: Optional[str] = None


class AnalysisResponse(BaseModel):
    id: str
    student_name: str
    analysis_detail: str
    created_at: datetime
    user_id: str


class AnalysisListResponse(BaseModel):
    id: str
    student_name: str
    analysis_detail: str
    created_at: datetime

