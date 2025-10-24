import hashlib
import secrets
from typing import Tuple


class PasswordService:
    """Serviço para gerenciamento de senhas"""
    
    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """
        Gera hash da senha com salt
        
        Returns:
            Tuple[str, str]: (password_hash, salt)
        """
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return password_hash.hex(), salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """
        Verifica se a senha está correta
        
        Args:
            password: Senha em texto plano
            password_hash: Hash da senha armazenado
            salt: Salt usado no hash
            
        Returns:
            bool: True se a senha está correta
        """
        test_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return test_hash.hex() == password_hash
    
    @staticmethod
    def generate_reset_token() -> str:
        """Gera token para reset de senha"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """
        Verifica se a senha é forte o suficiente
        
        Args:
            password: Senha para verificar
            
        Returns:
            bool: True se a senha é forte
        """
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
