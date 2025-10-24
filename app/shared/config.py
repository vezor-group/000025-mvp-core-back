import os
from typing import Optional


class Settings:
    """Configurações da aplicação"""
    
    # Configurações da API
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "VZR-LBS-v0-mvp-base-back")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "True").lower() == "true"
    
    # Configurações de Autenticação
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", "24"))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # Configurações de Banco de Dados
    DB_POSTGRES_HOST: Optional[str] = os.getenv("DB_POSTGRES_HOST")
    DB_POSTGRES_PORT: Optional[str] = os.getenv("DB_POSTGRES_PORT")
    DB_POSTGRES_DATABASE: Optional[str] = os.getenv("DB_POSTGRES_DATABASE")
    DB_POSTGRES_USER: Optional[str] = os.getenv("DB_POSTGRES_USER")
    DB_POSTGRES_PASSWORD: Optional[str] = os.getenv("DB_POSTGRES_PASSWORD")
    
    DB_MONGO_HOST: Optional[str] = os.getenv("DB_MONGO_HOST")
    DB_MONGO_PORT: Optional[str] = os.getenv("DB_MONGO_PORT")
    DB_MONGO_DATABASE: Optional[str] = os.getenv("DB_MONGO_DATABASE")
    DB_MONGO_USER: Optional[str] = os.getenv("DB_MONGO_USER")
    DB_MONGO_PASSWORD: Optional[str] = os.getenv("DB_MONGO_PASSWORD")
    
    DB_REDIS_HOST: Optional[str] = os.getenv("DB_REDIS_HOST")
    DB_REDIS_PORT: Optional[str] = os.getenv("DB_REDIS_PORT")
    DB_REDIS_DATABASE: Optional[str] = os.getenv("DB_REDIS_DATABASE")
    DB_REDIS_PASSWORD: Optional[str] = os.getenv("DB_REDIS_PASSWORD")
    
    # Configurações de Email (para verificação)
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "True").lower() == "true"
    
    # Configurações de Provedores Sociais
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    
    MICROSOFT_CLIENT_ID: Optional[str] = os.getenv("MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET: Optional[str] = os.getenv("MICROSOFT_CLIENT_SECRET")
    
    # Configurações de Segurança
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
    PASSWORD_REQUIRE_UPPERCASE: bool = os.getenv("PASSWORD_REQUIRE_UPPERCASE", "True").lower() == "true"
    PASSWORD_REQUIRE_LOWERCASE: bool = os.getenv("PASSWORD_REQUIRE_LOWERCASE", "True").lower() == "true"
    PASSWORD_REQUIRE_DIGITS: bool = os.getenv("PASSWORD_REQUIRE_DIGITS", "True").lower() == "true"
    PASSWORD_REQUIRE_SPECIAL: bool = os.getenv("PASSWORD_REQUIRE_SPECIAL", "True").lower() == "true"


# Instância global das configurações
settings = Settings()
