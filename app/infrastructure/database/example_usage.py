"""
Exemplo de uso dos bancos de dados
"""
import asyncio
import logging
from typing import Dict, Any

from . import database_manager, initialize_databases, test_database_connections

logger = logging.getLogger(__name__)


async def example_postgres_usage():
    """Exemplo de uso do PostgreSQL"""
    try:
        # Sessão síncrona
        session = database_manager.get_postgres_session()
        # Use a sessão aqui...
        session.close()
        
        # Sessão assíncrona
        async with database_manager.get_postgres_async_session() as async_session:
            # Use a sessão assíncrona aqui...
            pass
        
        logger.info("Exemplo PostgreSQL executado com sucesso")
    
    except Exception as e:
        logger.error(f"Erro no exemplo PostgreSQL: {e}")


async def example_mongo_usage():
    """Exemplo de uso do MongoDB"""
    try:
        # Coleção síncrona
        collection = database_manager.get_mongo_collection("users")
        # Use a coleção aqui...
        
        # Coleção assíncrona
        async_collection = database_manager.get_mongo_async_collection("users")
        # Use a coleção assíncrona aqui...
        
        logger.info("Exemplo MongoDB executado com sucesso")
    
    except Exception as e:
        logger.error(f"Erro no exemplo MongoDB: {e}")


async def example_redis_usage():
    """Exemplo de uso do Redis"""
    try:
        # Cliente síncrono
        redis_client = database_manager.get_redis_client()
        redis_client.set("exemplo", "valor")
        valor = redis_client.get("exemplo")
        
        # Cliente assíncrono
        async_redis = database_manager.get_redis_async_client()
        await async_redis.set("exemplo_async", "valor_async")
        valor_async = await async_redis.get("exemplo_async")
        
        logger.info("Exemplo Redis executado com sucesso")
    
    except Exception as e:
        logger.error(f"Erro no exemplo Redis: {e}")


async def main():
    """Função principal de exemplo"""
    try:
        # Inicializa todos os bancos
        logger.info("Inicializando bancos de dados...")
        results = await initialize_databases()
        logger.info(f"Resultados da inicialização: {results}")
        
        # Testa as conexões
        logger.info("Testando conexões...")
        connection_results = await test_database_connections()
        logger.info(f"Resultados dos testes: {connection_results}")
        
        # Exemplos de uso
        await example_postgres_usage()
        await example_mongo_usage()
        await example_redis_usage()
        
        # Status final
        status = database_manager.get_status()
        logger.info(f"Status final: {status}")
        
    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
    
    finally:
        # Fecha todas as conexões
        await database_manager.close_all_connections()


if __name__ == "__main__":
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Executa o exemplo
    asyncio.run(main())
