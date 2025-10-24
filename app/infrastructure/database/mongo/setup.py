"""
Setup e configuração do MongoDB
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database
from contextlib import asynccontextmanager

from ..config import get_database_config, get_mongo_url

logger = logging.getLogger(__name__)


class MongoSetup:
    """Classe para setup e gerenciamento do MongoDB"""
    
    def __init__(self):
        self.config = get_database_config()
        self.client: Optional[AsyncIOMotorClient] = None
        self.sync_client: Optional[MongoClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.sync_database: Optional[Database] = None
    
    def create_client(self) -> None:
        """Cria cliente assíncrono do MongoDB"""
        try:
            self.client = AsyncIOMotorClient(
                get_mongo_url(),
                maxPoolSize=self.config.max_connections,
                minPoolSize=self.config.min_connections,
                serverSelectionTimeoutMS=self.config.connection_timeout * 1000,
                connectTimeoutMS=self.config.connection_timeout * 1000,
                socketTimeoutMS=self.config.connection_timeout * 1000
            )
            self.database = self.client[self.config.mongo_database]
            logger.info("Cliente MongoDB assíncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar cliente MongoDB assíncrono: {e}")
            raise
    
    def create_sync_client(self) -> None:
        """Cria cliente síncrono do MongoDB"""
        try:
            self.sync_client = MongoClient(
                get_mongo_url(),
                maxPoolSize=self.config.max_connections,
                minPoolSize=self.config.min_connections,
                serverSelectionTimeoutMS=self.config.connection_timeout * 1000,
                connectTimeoutMS=self.config.connection_timeout * 1000,
                socketTimeoutMS=self.config.connection_timeout * 1000
            )
            self.sync_database = self.sync_client[self.config.mongo_database]
            logger.info("Cliente MongoDB síncrono criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar cliente MongoDB síncrono: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Testa a conexão com o MongoDB"""
        try:
            if not self.client:
                self.create_client()
            
            # Testa a conexão
            await self.client.admin.command('ping')
            logger.info("Conexão MongoDB testada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão MongoDB: {e}")
            return False
    
    async def create_database_if_not_exists(self) -> None:
        """Cria o banco de dados se não existir"""
        try:
            if not self.client:
                self.create_client()
            
            # Lista os bancos existentes
            db_list = await self.client.list_database_names()
            
            if self.config.mongo_database not in db_list:
                # Cria o banco criando uma coleção temporária
                temp_collection = self.database.temp_collection
                await temp_collection.insert_one({"temp": True})
                await temp_collection.drop()
                logger.info(f"Banco de dados '{self.config.mongo_database}' criado com sucesso")
            else:
                logger.info(f"Banco de dados '{self.config.mongo_database}' já existe")
        
        except Exception as e:
            logger.error(f"Erro ao criar banco de dados: {e}")
            raise
    
    async def create_indexes(self) -> None:
        """Cria índices básicos para o banco"""
        try:
            if not self.database:
                self.create_client()
            
            # Índices para coleções comuns
            collections_indexes = {
                'users': [
                    ('email', 1),
                    ('created_at', 1),
                    ('status', 1)
                ],
                'sessions': [
                    ('user_id', 1),
                    ('expires_at', 1),
                    ('token', 1)
                ],
                'audit_logs': [
                    ('user_id', 1),
                    ('action', 1),
                    ('created_at', 1)
                ]
            }
            
            for collection_name, indexes in collections_indexes.items():
                collection = self.database[collection_name]
                for index_spec in indexes:
                    try:
                        await collection.create_index([index_spec])
                    except Exception as e:
                        logger.warning(f"Erro ao criar índice {index_spec} na coleção {collection_name}: {e}")
            
            logger.info("Índices MongoDB criados com sucesso")
        
        except Exception as e:
            logger.error(f"Erro ao criar índices: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        """Retorna uma coleção síncrona"""
        if not self.sync_database:
            self.create_sync_client()
        
        return self.sync_database[collection_name]
    
    def get_async_collection(self, collection_name: str):
        """Retorna uma coleção assíncrona"""
        if not self.database:
            self.create_client()
        
        return self.database[collection_name]
    
    @asynccontextmanager
    async def get_session(self):
        """Retorna uma sessão MongoDB para transações"""
        if not self.client:
            self.create_client()
        
        async with await self.client.start_session() as session:
            try:
                yield session
            except Exception:
                await session.abort_transaction()
                raise
    
    async def create_collection_if_not_exists(self, collection_name: str) -> None:
        """Cria uma coleção se não existir"""
        try:
            if not self.database:
                self.create_client()
            
            collections = await self.database.list_collection_names()
            if collection_name not in collections:
                await self.database.create_collection(collection_name)
                logger.info(f"Coleção '{collection_name}' criada com sucesso")
            else:
                logger.info(f"Coleção '{collection_name}' já existe")
        
        except Exception as e:
            logger.error(f"Erro ao criar coleção '{collection_name}': {e}")
            raise
    
    async def initialize(self) -> None:
        """Inicializa o MongoDB"""
        try:
            self.create_client()
            self.create_sync_client()
            await self.create_database_if_not_exists()
            await self.create_indexes()
            await self.test_connection()
            logger.info("MongoDB inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar MongoDB: {e}")
            raise
    
    def close_connections(self) -> None:
        """Fecha todas as conexões"""
        if self.client:
            self.client.close()
        if self.sync_client:
            self.sync_client.close()


# Instância global
mongo_setup = MongoSetup()
