from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.auth.user import User


class UserRepository(ABC):
    """Interface do repositório de usuários"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Cria um novo usuário"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Atualiza um usuário"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Remove um usuário"""
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Lista todos os usuários"""
        pass


class InMemoryUserRepository(UserRepository):
    """Implementação em memória do repositório de usuários (para desenvolvimento)"""
    
    def __init__(self):
        self._users: dict[str, User] = {}
    
    async def create(self, user: User) -> User:
        """Cria um novo usuário"""
        self._users[user.id] = user
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        return self._users.get(user_id)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    async def update(self, user: User) -> User:
        """Atualiza um usuário"""
        if user.id in self._users:
            self._users[user.id] = user
        return user
    
    async def delete(self, user_id: str) -> bool:
        """Remove um usuário"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Lista todos os usuários"""
        users = list(self._users.values())
        return users[offset:offset + limit]
