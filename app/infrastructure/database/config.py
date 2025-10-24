"""
Configurações dos bancos de dados
"""
import os
from typing import Optional
from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    """Configurações centralizadas para todos os bancos de dados"""
    
    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_database: str = "vzr_lbs"
    postgres_url: Optional[str] = None
    
    # MongoDB
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = "mongo"
    mongo_password: str = "mongo"
    mongo_database: str = "vzr_lbs"
    mongo_url: Optional[str] = None
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_database: int = 0
    redis_url: Optional[str] = None
    
    # Configurações de pool de conexões
    max_connections: int = 20
    min_connections: int = 5
    connection_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_prefix = "DB_"
        case_sensitive = False


def get_database_config() -> DatabaseConfig:
    """Retorna a configuração dos bancos de dados"""
    return DatabaseConfig()


def get_postgres_url() -> str:
    """Retorna a URL de conexão do PostgreSQL"""
    config = get_database_config()
    if config.postgres_url:
        return config.postgres_url
    
    return f"postgresql://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_database}"


def get_mongo_url() -> str:
    """Retorna a URL de conexão do MongoDB"""
    config = get_database_config()
    if config.mongo_url:
        return config.mongo_url
    
    if config.mongo_user and config.mongo_password:
        return f"mongodb://{config.mongo_user}:{config.mongo_password}@{config.mongo_host}:{config.mongo_port}/{config.mongo_database}"
    else:
        return f"mongodb://{config.mongo_host}:{config.mongo_port}/{config.mongo_database}"


def get_redis_url() -> str:
    """Retorna a URL de conexão do Redis"""
    config = get_database_config()
    if config.redis_url:
        return config.redis_url
    
    if config.redis_password:
        return f"redis://:{config.redis_password}@{config.redis_host}:{config.redis_port}/{config.redis_database}"
    else:
        return f"redis://{config.redis_host}:{config.redis_port}/{config.redis_database}"
