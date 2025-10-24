from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.domain.auth.services.token_service import TokenService
from app.infrastructure.repositories.auth.user_repository import UserRepository
from app.infrastructure.repositories.auth.auth_session_repository import AuthSessionRepository


class TokenValidationUseCase:
    """Caso de uso para validação de tokens"""
    
    def __init__(
        self,
        token_service: TokenService,
        user_repository: UserRepository,
        session_repository: AuthSessionRepository
    ):
        self.token_service = token_service
        self.user_repository = user_repository
        self.session_repository = session_repository
    
    async def execute(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Valida um token de acesso
        
        Args:
            access_token: Token de acesso JWT
            
        Returns:
            Optional[Dict[str, Any]]: Dados do usuário se token válido
        """
        # Verificar se o token é válido
        payload = self.token_service.verify_token(access_token)
        if not payload or payload.get("type") != "access":
            return None
        
        # Buscar sessão
        session = await self.session_repository.get_by_access_token(access_token)
        if not session or not session.is_valid():
            return None
        
        # Buscar usuário
        user = await self.user_repository.get_by_id(payload["user_id"])
        if not user or not user.can_login():
            return None
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
                "status": user.status.value
            },
            "session": {
                "id": session.id,
                "expires_at": session.expires_at.isoformat()
            }
        }
    
    async def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Renova um token de acesso usando refresh token
        
        Args:
            refresh_token: Token de refresh
            
        Returns:
            Optional[Dict[str, Any]]: Novos tokens se refresh válido
        """
        # Verificar refresh token
        payload = self.token_service.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None
        
        # Buscar usuário
        user = await self.user_repository.get_by_id(payload["user_id"])
        if not user or not user.can_login():
            return None
        
        # Gerar novos tokens
        new_access_token = self.token_service.generate_access_token(user)
        new_refresh_token = self.token_service.generate_refresh_token(user)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
