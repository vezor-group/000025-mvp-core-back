from typing import Optional, Dict, Any
from app.domain.auth.user import User, UserStatus
from app.domain.auth.auth_provider import AuthProvider, AuthProviderType
from app.domain.auth.services.auth_service import AuthService
from app.infrastructure.repositories.auth.user_repository import UserRepository
from app.infrastructure.repositories.auth.auth_provider_repository import AuthProviderRepository


class SignUpUseCase:
    """Caso de uso para cadastro de usuários"""
    
    def __init__(
        self,
        auth_service: AuthService,
        user_repository: UserRepository,
        provider_repository: AuthProviderRepository
    ):
        self.auth_service = auth_service
        self.user_repository = user_repository
        self.provider_repository = provider_repository
    
    async def execute_basic(self, email: str, name: str, password: str) -> Dict[str, Any]:
        """
        Executa cadastro básico com email e senha
        
        Args:
            email: Email do usuário
            name: Nome do usuário
            password: Senha do usuário
            
        Returns:
            Dict[str, Any]: Dados do usuário criado
        """
        # Verificar se usuário já existe
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Usuário já existe com este email")
        
        # Criar usuário
        user, auth_provider = self.auth_service.create_user(email, name, password)
        
        # Salvar usuário
        created_user = await self.user_repository.create(user)
        
        # Salvar provedor de autenticação
        if auth_provider:
            await self.provider_repository.create(auth_provider)
        
        return {
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "name": created_user.name,
                "role": created_user.role.value,
                "status": created_user.status.value,
                "email_verified": created_user.email_verified,
                "created_at": created_user.created_at.isoformat()
            },
            "message": "Usuário criado com sucesso. Verifique seu email para ativar a conta."
        }
    
    async def execute_social(self, provider_type: AuthProviderType, email: str, name: str, provider_id: str) -> Dict[str, Any]:
        """
        Executa cadastro social
        
        Args:
            provider_type: Tipo do provedor (Google, Microsoft)
            email: Email do usuário
            name: Nome do usuário
            provider_id: ID do usuário no provedor
            
        Returns:
            Dict[str, Any]: Dados do usuário criado
        """
        # Verificar se usuário já existe
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Usuário já existe com este email")
        
        # Criar usuário (sem senha para autenticação social)
        user, auth_provider = self.auth_service.create_user(email, name)
        
        # Salvar usuário
        created_user = await self.user_repository.create(user)
        
        # Criar e salvar provedor de autenticação social
        if provider_type == AuthProviderType.GOOGLE:
            auth_provider = AuthProvider.create_google(created_user.id, provider_id)
        elif provider_type == AuthProviderType.MICROSOFT:
            auth_provider = AuthProvider.create_microsoft(created_user.id, provider_id)
        
        if auth_provider:
            await self.provider_repository.create(auth_provider)
        
        return {
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "name": created_user.name,
                "role": created_user.role.value,
                "status": created_user.status.value,
                "email_verified": created_user.email_verified,
                "created_at": created_user.created_at.isoformat()
            },
            "message": "Usuário criado com sucesso via autenticação social."
        }
