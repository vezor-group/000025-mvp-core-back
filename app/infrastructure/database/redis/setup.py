"""
Setup e configuração do Redis
"""
import asyncio
import logging
from typing import Optional, Any, Dict, Union
import redis.asyncio as redis
import redis as sync_redis
from contextlib import asynccontextmanager

from ..config import get_database_config, get_redis_url

logger = logging.getLogger(__name__)


class RedisSetup:
    """Classe para setup e gerenciamento do Redis"""
    
    def __init__(self):
        self.config = get_database_config()
        self.client: Optional[redis.Redis] = None
        self.sync_client: Optional[sync_redis.Redis] = None
        self.connection_pool: Optional[redis.ConnectionPool] = None
        self.sync_connection_pool: Optional[sync_redis.ConnectionPool] = None
    
    def create_connection_pool(self) -> None:
        """Cria pool de conexões assíncrono do Redis"""
        try:
            self.connection_pool = redis.ConnectionPool.from_url(
                get_redis_url(),
                max_connections=self.config.max_connections,
                retry_on_timeout=True,
                socket_connect_timeout=self.config.connection_timeout,
                socket_timeout=self.config.connection_timeout
            )
            logger.info("Pool de conexões Redis assíncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar pool de conexões Redis assíncrono: {e}")
            raise
    
    def create_sync_connection_pool(self) -> None:
        """Cria pool de conexões síncrono do Redis"""
        try:
            self.sync_connection_pool = sync_redis.ConnectionPool.from_url(
                get_redis_url(),
                max_connections=self.config.max_connections,
                retry_on_timeout=True,
                socket_connect_timeout=self.config.connection_timeout,
                socket_timeout=self.config.connection_timeout
            )
            logger.info("Pool de conexões Redis síncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar pool de conexões Redis síncrono: {e}")
            raise
    
    def create_client(self) -> None:
        """Cria cliente assíncrono do Redis"""
        try:
            if not self.connection_pool:
                self.create_connection_pool()
            
            self.client = redis.Redis(
                connection_pool=self.connection_pool,
                decode_responses=True
            )
            logger.info("Cliente Redis assíncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar cliente Redis assíncrono: {e}")
            raise
    
    def create_sync_client(self) -> None:
        """Cria cliente síncrono do Redis"""
        try:
            if not self.sync_connection_pool:
                self.create_sync_connection_pool()
            
            self.sync_client = sync_redis.Redis(
                connection_pool=self.sync_connection_pool,
                decode_responses=True
            )
            logger.info("Cliente Redis síncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar cliente Redis síncrono: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Testa a conexão com o Redis"""
        try:
            if not self.client:
                self.create_client()
            
            # Testa a conexão
            await self.client.ping()
            logger.info("Conexão Redis testada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão Redis: {e}")
            return False
    
    async def setup_basic_keys(self) -> None:
        """Configura chaves básicas do sistema"""
        try:
            if not self.client:
                self.create_client()
            
            # Configurações básicas
            basic_config = {
                "system:status": "active",
                "system:version": "1.0.0",
                "system:startup_time": str(asyncio.get_event_loop().time())
            }
            
            for key, value in basic_config.items():
                await self.client.set(key, value)
            
            # Configura TTL para algumas chaves
            await self.client.expire("system:startup_time", 86400)  # 24 horas
            
            logger.info("Chaves básicas do Redis configuradas com sucesso")
        
        except Exception as e:
            logger.error(f"Erro ao configurar chaves básicas: {e}")
            raise
    
    async def create_namespaces(self) -> None:
        """Cria namespaces básicos para organização"""
        try:
            if not self.client:
                self.create_client()
            
            # Namespaces básicos
            namespaces = [
                "cache:",
                "session:",
                "lock:",
                "queue:",
                "metrics:",
                "config:"
            ]
            
            for namespace in namespaces:
                # Cria uma chave temporária para garantir que o namespace existe
                temp_key = f"{namespace}initialized"
                await self.client.set(temp_key, "true", ex=1)  # Expira em 1 segundo
            
            logger.info("Namespaces Redis criados com sucesso")
        
        except Exception as e:
            logger.error(f"Erro ao criar namespaces: {e}")
            raise
    
    def get_client(self) -> sync_redis.Redis:
        """Retorna cliente síncrono do Redis"""
        if not self.sync_client:
            self.create_sync_client()
        
        return self.sync_client
    
    def get_async_client(self) -> redis.Redis:
        """Retorna cliente assíncrono do Redis"""
        if not self.client:
            self.create_client()
        
        return self.client
    
    @asynccontextmanager
    async def get_pipeline(self):
        """Retorna um pipeline Redis para operações em lote"""
        if not self.client:
            self.create_client()
        
        async with self.client.pipeline() as pipeline:
            try:
                yield pipeline
                await pipeline.execute()
            except Exception:
                await pipeline.reset()
                raise
    
    async def set_with_namespace(self, namespace: str, key: str, value: Any, ex: Optional[int] = None) -> None:
        """Define uma chave com namespace"""
        if not self.client:
            self.create_client()
        
        full_key = f"{namespace}{key}"
        if ex:
            await self.client.setex(full_key, ex, value)
        else:
            await self.client.set(full_key, value)
    
    async def get_with_namespace(self, namespace: str, key: str) -> Any:
        """Obtém uma chave com namespace"""
        if not self.client:
            self.create_client()
        
        full_key = f"{namespace}{key}"
        return await self.client.get(full_key)
    
    async def delete_with_namespace(self, namespace: str, key: str) -> None:
        """Remove uma chave com namespace"""
        if not self.client:
            self.create_client()
        
        full_key = f"{namespace}{key}"
        await self.client.delete(full_key)
    
    async def get_keys_by_namespace(self, namespace: str) -> list:
        """Obtém todas as chaves de um namespace"""
        if not self.client:
            self.create_client()
        
        pattern = f"{namespace}*"
        return await self.client.keys(pattern)
    
    async def clear_namespace(self, namespace: str) -> None:
        """Limpa todas as chaves de um namespace"""
        if not self.client:
            self.create_client()
        
        keys = await self.get_keys_by_namespace(namespace)
        if keys:
            await self.client.delete(*keys)
    
    async def initialize(self) -> None:
        """Inicializa o Redis"""
        try:
            self.create_connection_pool()
            self.create_sync_connection_pool()
            self.create_client()
            self.create_sync_client()
            await self.test_connection()
            await self.setup_basic_keys()
            await self.create_namespaces()
            logger.info("Redis inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar Redis: {e}")
            raise
    
    def close_connections(self) -> None:
        """Fecha todas as conexões"""
        if self.client:
            asyncio.create_task(self.client.aclose())
        if self.sync_client:
            self.sync_client.close()
        if self.connection_pool:
            asyncio.create_task(self.connection_pool.aclose())
        if self.sync_connection_pool:
            self.sync_connection_pool.disconnect()


# Instância global
redis_setup = RedisSetup()
