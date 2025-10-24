from typing import Optional, Dict, Any
from app.domain.auth.user import User
from app.domain.auth.auth_session import AuthSession
from app.domain.auth.auth_provider import AuthProviderType
from app.domain.auth.services.auth_service import AuthService
from app.infrastructure.repositories.auth.user_repository import UserRepository
from app.infrastructure.repositories.auth.auth_session_repository import AuthSessionRepository


class SignInUseCase:
    """Caso de uso para autenticação de usuários"""
    
    def __init__(
        self,
        auth_service: AuthService,
        user_repository: UserRepository,
        session_repository: AuthSessionRepository
    ):
        self.auth_service = auth_service
        self.user_repository = user_repository
        self.session_repository = session_repository
    
    async def execute_basic(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Executa login básico com email e senha
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Optional[Dict[str, Any]]: Dados da sessão se autenticação bem-sucedida
        """
        # Buscar usuário por email
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        
        # Autenticar com email e senha
        session = self.auth_service.authenticate_basic(email, password, user)
        if not session:
            return None
        
        # Salvar sessão
        await self.session_repository.create(session)
        
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at.isoformat(),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
                "status": user.status.value
            }
        }
    
    async def execute_social(self, provider_type: AuthProviderType, email: str, provider_id: str) -> Optional[Dict[str, Any]]:
        """
        Executa login social
        
        Args:
            provider_type: Tipo do provedor (Google, Microsoft)
            email: Email do usuário
            provider_id: ID do usuário no provedor
            
        Returns:
            Optional[Dict[str, Any]]: Dados da sessão se autenticação bem-sucedida
        """
        # Buscar usuário por email
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        
        # Autenticar com provedor social
        session = self.auth_service.authenticate_social(provider_type, email, provider_id, user)
        if not session:
            return None
        
        # Salvar sessão
        await self.session_repository.create(session)
        
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at.isoformat(),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
                "status": user.status.value
            }
        }
