from datetime import datetime
from typing import Optional, Tuple
from app.domain.auth.user import User, UserStatus
from app.domain.auth.auth_session import AuthSession
from app.domain.auth.auth_provider import AuthProvider, AuthProviderType
from .password_service import PasswordService
from .token_service import TokenService


class AuthService:
    """Serviço principal de autenticação"""
    
    def __init__(self, token_service: TokenService):
        self.token_service = token_service
        self.password_service = PasswordService()
    
    def authenticate_basic(self, email: str, password: str, user: User) -> Optional[AuthSession]:
        """
        Autentica usuário com email e senha
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            user: Usuário encontrado no banco
            
        Returns:
            Optional[AuthSession]: Sessão criada se autenticação bem-sucedida
        """
        if not user.can_login():
            return None
        
        # Verificar senha (assumindo que o hash e salt estão armazenados no user)
        # Por enquanto, vamos simular a verificação
        if not self._verify_user_password(user, password):
            return None
        
        # Atualizar último login
        user.update_last_login()
        
        # Gerar tokens
        access_token = self.token_service.generate_access_token(user)
        refresh_token = self.token_service.generate_refresh_token(user)
        
        # Criar sessão
        session = AuthSession.create(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return session
    
    def authenticate_social(self, provider_type: AuthProviderType, email: str, provider_id: str, user: Optional[User] = None) -> Optional[AuthSession]:
        """
        Autentica usuário com provedor social
        
        Args:
            provider_type: Tipo do provedor (Google, Microsoft)
            email: Email do usuário
            provider_id: ID do usuário no provedor
            user: Usuário existente (opcional)
            
        Returns:
            Optional[AuthSession]: Sessão criada se autenticação bem-sucedida
        """
        if not user:
            return None
        
        if not user.can_login():
            return None
        
        # Atualizar último login
        user.update_last_login()
        
        # Gerar tokens
        access_token = self.token_service.generate_access_token(user)
        refresh_token = self.token_service.generate_refresh_token(user)
        
        # Criar sessão
        session = AuthSession.create(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return session
    
    def create_user(self, email: str, name: str, password: str = None) -> Tuple[User, Optional[AuthProvider]]:
        """
        Cria um novo usuário
        
        Args:
            email: Email do usuário
            name: Nome do usuário
            password: Senha (opcional para autenticação social)
            
        Returns:
            Tuple[User, Optional[AuthProvider]]: Usuário criado e provedor de auth
        """
        user_id = f"user_{int(datetime.utcnow().timestamp())}"
        
        # Criar usuário
        user = User(
            id=user_id,
            email=email,
            name=name,
            status=UserStatus.PENDING,
            email_verified=False
        )
        
        # Se tem senha, criar provedor básico
        auth_provider = None
        if password:
            password_hash, salt = self.password_service.hash_password(password)
            user.password_hash = f"{password_hash}:{salt}"  # Armazenar hash e salt juntos
            auth_provider = AuthProvider.create_basic(user_id)
        else:
            # Para autenticação social, marcar como verificado
            user.email_verified = True
            user.status = UserStatus.ACTIVE
        
        return user, auth_provider
    
    def validate_session(self, access_token: str) -> Optional[User]:
        """
        Valida uma sessão e retorna o usuário
        
        Args:
            access_token: Token de acesso
            
        Returns:
            Optional[User]: Usuário se a sessão for válida
        """
        payload = self.token_service.verify_token(access_token)
        if not payload or payload.get("type") != "access":
            return None
        
        # Aqui você buscaria o usuário no banco usando payload["user_id"]
        # Por enquanto, retornamos None para indicar que precisa ser implementado
        return None
    
    def _verify_user_password(self, user: User, password: str) -> bool:
        """
        Verifica a senha do usuário
        
        Args:
            user: Usuário
            password: Senha em texto plano
            
        Returns:
            bool: True se a senha está correta
        """
        if not user.password_hash:
            return False
        
        try:
            # Assumindo que password_hash está no formato "hash:salt"
            password_hash, salt = user.password_hash.split(":", 1)
            return self.password_service.verify_password(password, password_hash, salt)
        except ValueError:
            return False
