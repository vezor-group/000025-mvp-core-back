from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class SessionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class AuthSession:
    """Entidade AuthSession para gerenciar sessões de autenticação"""
    id: str
    user_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def is_valid(self) -> bool:
        """Verifica se a sessão é válida"""
        return (
            self.status == SessionStatus.ACTIVE and 
            self.expires_at > datetime.utcnow()
        )

    def is_expired(self) -> bool:
        """Verifica se a sessão expirou"""
        return self.expires_at <= datetime.utcnow()

    def revoke(self):
        """Revoga a sessão"""
        self.status = SessionStatus.REVOKED
        self.updated_at = datetime.utcnow()

    def extend(self, hours: int = 24):
        """Estende a sessão por N horas"""
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        self.updated_at = datetime.utcnow()

    @classmethod
    def create(cls, user_id: str, access_token: str, refresh_token: str, expires_in_hours: int = 24):
        """Cria uma nova sessão"""
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        return cls(
            id=f"session_{user_id}_{int(datetime.utcnow().timestamp())}",
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
