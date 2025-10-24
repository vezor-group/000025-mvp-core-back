"""
Inicialização e gerenciamento dos bancos de dados
"""
import asyncio
import logging
from typing import Dict, Any

from .config import get_database_config
from .postgres.setup import postgres_setup
from .mongo.setup import mongo_setup
from .redis.setup import redis_setup

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gerenciador central de todos os bancos de dados"""
    
    def __init__(self):
        self.config = get_database_config()
        self.postgres = postgres_setup
        self.mongo = mongo_setup
        self.redis = redis_setup
        self._initialized = False
    
    async def initialize_all(self) -> Dict[str, bool]:
        """Inicializa todos os bancos de dados"""
        results = {
            "postgres": False,
            "mongo": False,
            "redis": False
        }
        
        try:
            logger.info("Iniciando inicialização dos bancos de dados...")
            
            # Inicializa PostgreSQL
            try:
                await self.postgres.initialize()
                results["postgres"] = True
                logger.info("PostgreSQL inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar PostgreSQL: {e}")
            
            # Inicializa MongoDB
            try:
                await self.mongo.initialize()
                results["mongo"] = True
                logger.info("MongoDB inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar MongoDB: {e}")
            
            # Inicializa Redis
            try:
                await self.redis.initialize()
                results["redis"] = True
                logger.info("Redis inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar Redis: {e}")
            
            self._initialized = all(results.values())
            
            if self._initialized:
                logger.info("Todos os bancos de dados foram inicializados com sucesso")
            else:
                failed_dbs = [db for db, status in results.items() if not status]
                logger.warning(f"Alguns bancos falharam na inicialização: {failed_dbs}")
            
            return results
        
        except Exception as e:
            logger.error(f"Erro geral na inicialização dos bancos: {e}")
            return results
    
    async def test_all_connections(self) -> Dict[str, bool]:
        """Testa todas as conexões"""
        results = {
            "postgres": False,
            "mongo": False,
            "redis": False
        }
        
        try:
            # Testa PostgreSQL
            if self.postgres:
                results["postgres"] = await self.postgres.test_connection()
            
            # Testa MongoDB
            if self.mongo:
                results["mongo"] = await self.mongo.test_connection()
            
            # Testa Redis
            if self.redis:
                results["redis"] = await self.redis.test_connection()
            
            return results
        
        except Exception as e:
            logger.error(f"Erro ao testar conexões: {e}")
            return results
    
    def get_postgres_session(self):
        """Retorna sessão do PostgreSQL"""
        return self.postgres.get_session()
    
    async def get_postgres_async_session(self):
        """Retorna sessão assíncrona do PostgreSQL"""
        return self.postgres.get_async_session()
    
    def get_mongo_collection(self, collection_name: str):
        """Retorna coleção do MongoDB"""
        return self.mongo.get_collection(collection_name)
    
    def get_mongo_async_collection(self, collection_name: str):
        """Retorna coleção assíncrona do MongoDB"""
        return self.mongo.get_async_collection(collection_name)
    
    def get_redis_client(self):
        """Retorna cliente do Redis"""
        return self.redis.get_client()
    
    def get_redis_async_client(self):
        """Retorna cliente assíncrono do Redis"""
        return self.redis.get_async_client()
    
    async def close_all_connections(self) -> None:
        """Fecha todas as conexões"""
        try:
            logger.info("Fechando todas as conexões dos bancos de dados...")
            
            if self.postgres:
                self.postgres.close_connections()
            
            if self.mongo:
                self.mongo.close_connections()
            
            if self.redis:
                self.redis.close_connections()
            
            logger.info("Todas as conexões foram fechadas")
        
        except Exception as e:
            logger.error(f"Erro ao fechar conexões: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status dos bancos de dados"""
        return {
            "initialized": self._initialized,
            "config": {
                "postgres_host": self.config.postgres_host,
                "postgres_port": self.config.postgres_port,
                "mongo_host": self.config.mongo_host,
                "mongo_port": self.config.mongo_port,
                "redis_host": self.config.redis_host,
                "redis_port": self.config.redis_port
            }
        }


# Instância global do gerenciador
database_manager = DatabaseManager()


async def initialize_databases() -> Dict[str, bool]:
    """Função de conveniência para inicializar todos os bancos"""
    return await database_manager.initialize_all()


async def test_database_connections() -> Dict[str, bool]:
    """Função de conveniência para testar todas as conexões"""
    return await database_manager.test_all_connections()


async def close_database_connections() -> None:
    """Função de conveniência para fechar todas as conexões"""
    await database_manager.close_all_connections()


def get_database_manager() -> DatabaseManager:
    """Retorna a instância do gerenciador de bancos de dados"""
    return database_manager
