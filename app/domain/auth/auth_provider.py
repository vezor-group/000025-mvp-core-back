from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class AuthProviderType(Enum):
    BASIC = "basic"
    GOOGLE = "google"
    MICROSOFT = "microsoft"


@dataclass
class AuthProvider:
    """Entidade AuthProvider para gerenciar provedores de autenticação"""
    id: str
    user_id: str
    provider_type: AuthProviderType
    provider_id: str  # ID do usuário no provedor externo
    provider_data: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @classmethod
    def create_basic(cls, user_id: str):
        """Cria um provedor básico (email/senha)"""
        return cls(
            id=f"basic_{user_id}",
            user_id=user_id,
            provider_type=AuthProviderType.BASIC,
            provider_id=user_id
        )

    @classmethod
    def create_google(cls, user_id: str, google_id: str, provider_data: Optional[Dict[str, Any]] = None):
        """Cria um provedor Google"""
        return cls(
            id=f"google_{user_id}",
            user_id=user_id,
            provider_type=AuthProviderType.GOOGLE,
            provider_id=google_id,
            provider_data=provider_data
        )

    @classmethod
    def create_microsoft(cls, user_id: str, microsoft_id: str, provider_data: Optional[Dict[str, Any]] = None):
        """Cria um provedor Microsoft"""
        return cls(
            id=f"microsoft_{user_id}",
            user_id=user_id,
            provider_type=AuthProviderType.MICROSOFT,
            provider_id=microsoft_id,
            provider_data=provider_data
        )
