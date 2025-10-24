from pydantic import BaseModel, EmailStr
from typing import Optional
from app.domain.auth.auth_provider import AuthProviderType


class SignInRequest(BaseModel):
    """DTO para requisição de login"""
    providerAuth: str  # "basic", "google", "microsoft"
    email: EmailStr
    password: Optional[str] = None  # Senha em texto plano para providerAuth="basic"
    senhaHash: Optional[str] = None  # Campo legado - será mapeado para password


class SignUpRequest(BaseModel):
    """DTO para requisição de cadastro"""
    email: EmailStr
    name: str
    password: Optional[str] = None  # Para cadastro básico
    providerAuth: Optional[str] = None  # Para cadastro social
    providerId: Optional[str] = None  # ID do usuário no provedor social


class AuthResponse(BaseModel):
    """DTO para resposta de autenticação"""
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None


class UserInfo(BaseModel):
    """DTO para informações do usuário"""
    id: str
    email: str
    name: str
    role: str
    status: str
    email_verified: bool
    created_at: str


class SessionInfo(BaseModel):
    """DTO para informações da sessão"""
    access_token: str
    refresh_token: str
    expires_at: str
    user: UserInfo
