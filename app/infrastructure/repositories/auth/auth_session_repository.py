from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.auth.auth_session import AuthSession


class AuthSessionRepository(ABC):
    """Interface do repositório de sessões de autenticação"""
    
    @abstractmethod
    async def create(self, session: AuthSession) -> AuthSession:
        """Cria uma nova sessão"""
        pass
    
    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[AuthSession]:
        """Busca sessão por ID"""
        pass
    
    @abstractmethod
    async def get_by_access_token(self, access_token: str) -> Optional[AuthSession]:
        """Busca sessão por token de acesso"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[AuthSession]:
        """Busca todas as sessões de um usuário"""
        pass
    
    @abstractmethod
    async def update(self, session: AuthSession) -> AuthSession:
        """Atualiza uma sessão"""
        pass
    
    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        """Remove uma sessão"""
        pass
    
    @abstractmethod
    async def revoke_user_sessions(self, user_id: str) -> int:
        """Revoga todas as sessões de um usuário"""
        pass


class InMemoryAuthSessionRepository(AuthSessionRepository):
    """Implementação em memória do repositório de sessões (para desenvolvimento)"""
    
    def __init__(self):
        self._sessions: dict[str, AuthSession] = {}
    
    async def create(self, session: AuthSession) -> AuthSession:
        """Cria uma nova sessão"""
        self._sessions[session.id] = session
        return session
    
    async def get_by_id(self, session_id: str) -> Optional[AuthSession]:
        """Busca sessão por ID"""
        return self._sessions.get(session_id)
    
    async def get_by_access_token(self, access_token: str) -> Optional[AuthSession]:
        """Busca sessão por token de acesso"""
        for session in self._sessions.values():
            if session.access_token == access_token:
                return session
        return None
    
    async def get_by_user_id(self, user_id: str) -> List[AuthSession]:
        """Busca todas as sessões de um usuário"""
        return [session for session in self._sessions.values() if session.user_id == user_id]
    
    async def update(self, session: AuthSession) -> AuthSession:
        """Atualiza uma sessão"""
        if session.id in self._sessions:
            self._sessions[session.id] = session
        return session
    
    async def delete(self, session_id: str) -> bool:
        """Remove uma sessão"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    async def revoke_user_sessions(self, user_id: str) -> int:
        """Revoga todas as sessões de um usuário"""
        count = 0
        for session in self._sessions.values():
            if session.user_id == user_id:
                session.revoke()
                count += 1
        return count
