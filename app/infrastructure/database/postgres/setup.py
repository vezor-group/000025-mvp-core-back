"""
Setup e configuração do PostgreSQL
"""
import asyncio
import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import asynccontextmanager

from ..config import get_database_config, get_postgres_url

logger = logging.getLogger(__name__)


class PostgreSQLSetup:
    """Classe para setup e gerenciamento do PostgreSQL"""
    
    def __init__(self):
        self.config = get_database_config()
        self.engine = None
        self.async_engine = None
        self.session_factory = None
        self.async_session_factory = None
    
    def create_engine_sync(self) -> None:
        """Cria engine síncrono do PostgreSQL"""
        try:
            self.engine = create_engine(
                get_postgres_url(),
                poolclass=QueuePool,
                pool_size=self.config.max_connections,
                max_overflow=self.config.max_connections - self.config.min_connections,
                pool_timeout=self.config.connection_timeout,
                pool_recycle=3600,
                echo=False
            )
            logger.info("Engine PostgreSQL síncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar engine PostgreSQL síncrono: {e}")
            raise
    
    def create_engine_async(self) -> None:
        """Cria engine assíncrono do PostgreSQL"""
        try:
            # Converte URL para asyncpg
            async_url = get_postgres_url().replace("postgresql://", "postgresql+asyncpg://")
            
            self.async_engine = create_async_engine(
                async_url,
                pool_size=self.config.max_connections,
                max_overflow=self.config.max_connections - self.config.min_connections,
                pool_timeout=self.config.connection_timeout,
                pool_recycle=3600,
                echo=False
            )
            logger.info("Engine PostgreSQL assíncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar engine PostgreSQL assíncrono: {e}")
            raise
    
    def create_session_factories(self) -> None:
        """Cria factories de sessão"""
        if self.engine:
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
        
        if self.async_engine:
            self.async_session_factory = sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False
            )
    
    async def test_connection(self) -> bool:
        """Testa a conexão com o PostgreSQL"""
        try:
            if not self.async_engine:
                self.create_engine_async()
            
            async with self.async_engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.fetchone()
            
            logger.info("Conexão PostgreSQL testada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão PostgreSQL: {e}")
            return False
    
    async def create_database_if_not_exists(self) -> None:
        """Cria o banco de dados se não existir"""
        try:
            # Conecta ao PostgreSQL sem especificar database
            admin_url = f"postgresql://{self.config.postgres_user}:{self.config.postgres_password}@{self.config.postgres_host}:{self.config.postgres_port}/postgres"
            admin_engine = create_engine(admin_url)
            
            with admin_engine.connect() as conn:
                # Verifica se o banco existe
                result = conn.execute(text(
                    f"SELECT 1 FROM pg_database WHERE datname = '{self.config.postgres_database}'"
                ))
                
                if not result.fetchone():
                    # Cria o banco
                    conn.execute(text(f"CREATE DATABASE {self.config.postgres_database}"))
                    logger.info(f"Banco de dados '{self.config.postgres_database}' criado com sucesso")
                else:
                    logger.info(f"Banco de dados '{self.config.postgres_database}' já existe")
        
        except Exception as e:
            logger.error(f"Erro ao criar banco de dados: {e}")
            raise
    
    def get_session(self):
        """Retorna uma sessão síncrona"""
        if not self.session_factory:
            self.create_engine_sync()
            self.create_session_factories()
        
        return self.session_factory()
    
    @asynccontextmanager
    async def get_async_session(self):
        """Retorna uma sessão assíncrona"""
        if not self.async_session_factory:
            self.create_engine_async()
            self.create_session_factories()
        
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def initialize(self) -> None:
        """Inicializa o PostgreSQL"""
        try:
            await self.create_database_if_not_exists()
            self.create_engine_sync()
            self.create_engine_async()
            self.create_session_factories()
            await self.test_connection()
            logger.info("PostgreSQL inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar PostgreSQL: {e}")
            raise
    
    def close_connections(self) -> None:
        """Fecha todas as conexões"""
        if self.engine:
            self.engine.dispose()
        if self.async_engine:
            asyncio.create_task(self.async_engine.dispose())


# Instância global
postgres_setup = PostgreSQLSetup()
