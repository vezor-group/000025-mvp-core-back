import jwt
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from app.domain.auth.user import User


class TokenService:
    """Serviço para gerenciamento de tokens JWT"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_access_token(self, user: User, expires_in_hours: int = 24) -> str:
        """
        Gera token de acesso JWT
        
        Args:
            user: Usuário para o qual gerar o token
            expires_in_hours: Tempo de expiração em horas
            
        Returns:
            str: Token JWT
        """
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_refresh_token(self, user: User, expires_in_days: int = 30) -> str:
        """
        Gera token de refresh JWT
        
        Args:
            user: Usuário para o qual gerar o token
            expires_in_days: Tempo de expiração em dias
            
        Returns:
            str: Token JWT de refresh
        """
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=expires_in_days),
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica e decodifica um token JWT
        
        Args:
            token: Token JWT para verificar
            
        Returns:
            Optional[Dict[str, Any]]: Payload do token se válido, None caso contrário
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def extract_user_id(self, token: str) -> Optional[str]:
        """
        Extrai o ID do usuário do token
        
        Args:
            token: Token JWT
            
        Returns:
            Optional[str]: ID do usuário se válido, None caso contrário
        """
        payload = self.verify_token(token)
        if payload and payload.get("type") == "access":
            return payload.get("user_id")
        return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se o token está expirado
        
        Args:
            token: Token JWT para verificar
            
        Returns:
            bool: True se o token está expirado
        """
        payload = self.verify_token(token)
        if not payload:
            return True
        
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return True
        
        return datetime.utcnow().timestamp() > exp_timestamp
    
    @staticmethod
    def generate_session_id() -> str:
        """Gera ID único para sessão"""
        return secrets.token_urlsafe(32)
