from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.auth.auth_provider import AuthProvider, AuthProviderType


class AuthProviderRepository(ABC):
    """Interface do repositório de provedores de autenticação"""
    
    @abstractmethod
    async def create(self, provider: AuthProvider) -> AuthProvider:
        """Cria um novo provedor"""
        pass
    
    @abstractmethod
    async def get_by_id(self, provider_id: str) -> Optional[AuthProvider]:
        """Busca provedor por ID"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[AuthProvider]:
        """Busca todos os provedores de um usuário"""
        pass
    
    @abstractmethod
    async def get_by_provider_info(self, provider_type: AuthProviderType, provider_user_id: str) -> Optional[AuthProvider]:
        """Busca provedor por tipo e ID do usuário no provedor"""
        pass
    
    @abstractmethod
    async def update(self, provider: AuthProvider) -> AuthProvider:
        """Atualiza um provedor"""
        pass
    
    @abstractmethod
    async def delete(self, provider_id: str) -> bool:
        """Remove um provedor"""
        pass


class InMemoryAuthProviderRepository(AuthProviderRepository):
    """Implementação em memória do repositório de provedores (para desenvolvimento)"""
    
    def __init__(self):
        self._providers: dict[str, AuthProvider] = {}
    
    async def create(self, provider: AuthProvider) -> AuthProvider:
        """Cria um novo provedor"""
        self._providers[provider.id] = provider
        return provider
    
    async def get_by_id(self, provider_id: str) -> Optional[AuthProvider]:
        """Busca provedor por ID"""
        return self._providers.get(provider_id)
    
    async def get_by_user_id(self, user_id: str) -> List[AuthProvider]:
        """Busca todos os provedores de um usuário"""
        return [provider for provider in self._providers.values() if provider.user_id == user_id]
    
    async def get_by_provider_info(self, provider_type: AuthProviderType, provider_user_id: str) -> Optional[AuthProvider]:
        """Busca provedor por tipo e ID do usuário no provedor"""
        for provider in self._providers.values():
            if (provider.provider_type == provider_type and 
                provider.provider_id == provider_user_id):
                return provider
        return None
    
    async def update(self, provider: AuthProvider) -> AuthProvider:
        """Atualiza um provedor"""
        if provider.id in self._providers:
            self._providers[provider.id] = provider
        return provider
    
    async def delete(self, provider_id: str) -> bool:
        """Remove um provedor"""
        if provider_id in self._providers:
            del self._providers[provider_id]
            return True
        return False
