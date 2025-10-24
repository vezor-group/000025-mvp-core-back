from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


@dataclass
class User:
    """Entidade User para autenticação"""
    id: str
    email: str
    name: str
    password_hash: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.PENDING
    email_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def is_active(self) -> bool:
        """Verifica se o usuário está ativo"""
        return self.status == UserStatus.ACTIVE

    def can_login(self) -> bool:
        """Verifica se o usuário pode fazer login"""
        return self.is_active() and self.email_verified

    def update_last_login(self):
        """Atualiza o timestamp do último login"""
        self.last_login_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
