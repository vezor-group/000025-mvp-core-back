from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.aplication.auth.token_validation_use_case import TokenValidationUseCase
from app.domain.auth.services.token_service import TokenService
from app.infrastructure.repositories.auth.user_repository import InMemoryUserRepository
from app.infrastructure.repositories.auth.auth_session_repository import InMemoryAuthSessionRepository

# Inicialização dos serviços (em produção, usar injeção de dependência)
user_repository = InMemoryUserRepository()
session_repository = InMemoryAuthSessionRepository()
token_service = TokenService(secret_key="your-secret-key-here")
token_validation_use_case = TokenValidationUseCase(token_service, user_repository, session_repository)

# Esquema de autenticação HTTP Bearer
security = HTTPBearer()


class AuthMiddleware:
    """Middleware de autenticação JWT"""
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        Dependência para obter o usuário atual autenticado
        
        Args:
            credentials: Credenciais de autorização HTTP Bearer
            
        Returns:
            dict: Dados do usuário autenticado
            
        Raises:
            HTTPException: Se o token for inválido ou expirado
        """
        try:
            access_token = credentials.credentials
            result = await token_validation_use_case.execute(access_token)
            
            if not result:
                raise HTTPException(
                    status_code=401,
                    detail="Token inválido ou expirado",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno na autenticação: {str(e)}"
            )
    
    @staticmethod
    async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        """
        Dependência opcional para obter o usuário atual (não falha se não autenticado)
        
        Args:
            credentials: Credenciais de autorização HTTP Bearer (opcional)
            
        Returns:
            Optional[dict]: Dados do usuário autenticado ou None
        """
        if not credentials:
            return None
        
        try:
            access_token = credentials.credentials
            result = await token_validation_use_case.execute(access_token)
            return result
        except:
            return None
    
    @staticmethod
    def require_role(required_role: str):
        """
        Decorator para verificar se o usuário tem a role necessária
        
        Args:
            required_role: Role necessária para acessar o recurso
            
        Returns:
            function: Decorator que verifica a role
        """
        async def role_checker(current_user: dict = Depends(AuthMiddleware.get_current_user)):
            user_role = current_user.get("user", {}).get("role")
            
            if user_role != required_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"Acesso negado. Role necessária: {required_role}"
                )
            
            return current_user
        
        return role_checker
    
    @staticmethod
    def require_roles(required_roles: list):
        """
        Decorator para verificar se o usuário tem uma das roles necessárias
        
        Args:
            required_roles: Lista de roles necessárias para acessar o recurso
            
        Returns:
            function: Decorator que verifica as roles
        """
        async def roles_checker(current_user: dict = Depends(AuthMiddleware.get_current_user)):
            user_role = current_user.get("user", {}).get("role")
            
            if user_role not in required_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Acesso negado. Roles necessárias: {', '.join(required_roles)}"
                )
            
            return current_user
        
        return roles_checker


# Instância global do middleware
auth_middleware = AuthMiddleware()
