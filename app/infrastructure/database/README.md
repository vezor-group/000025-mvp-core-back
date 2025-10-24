# Configuração dos Bancos de Dados

Este diretório contém a configuração e setup para os bancos de dados PostgreSQL, MongoDB e Redis.

## Estrutura

```
database/
├── config.py              # Configurações centralizadas
├── __init__.py            # Gerenciador principal
├── postgres/
│   └── setup.py          # Setup do PostgreSQL
├── mongo/
│   └── setup.py          # Setup do MongoDB
├── redis/
│   └── setup.py          # Setup do Redis
├── example_usage.py      # Exemplos de uso
├── env.example           # Exemplo de variáveis de ambiente
└── README.md             # Este arquivo
```

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements-database.txt
```

2. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso Básico

### Inicialização
```python
from app.infrastructure.database import initialize_databases, database_manager

# Inicializa todos os bancos
results = await initialize_databases()
```

### PostgreSQL
```python
# Sessão síncrona
session = database_manager.get_postgres_session()

# Sessão assíncrona
async with database_manager.get_postgres_async_session() as session:
    # Use a sessão aqui
    pass
```

### MongoDB
```python
# Coleção síncrona
collection = database_manager.get_mongo_collection("users")

# Coleção assíncrona
async_collection = database_manager.get_mongo_async_collection("users")
```

### Redis
```python
# Cliente síncrono
redis_client = database_manager.get_redis_client()
redis_client.set("key", "value")

# Cliente assíncrono
async_redis = database_manager.get_redis_async_client()
await async_redis.set("key", "value")
```

## Configurações

As configurações são carregadas automaticamente do arquivo `.env` ou variáveis de ambiente:

- `DB_POSTGRES_*`: Configurações do PostgreSQL
- `DB_MONGO_*`: Configurações do MongoDB  
- `DB_REDIS_*`: Configurações do Redis

## Exemplo Completo

Execute o arquivo de exemplo:
```bash
python app/infrastructure/database/example_usage.py
```

## Recursos

- ✅ Pool de conexões configurável
- ✅ Suporte a operações síncronas e assíncronas
- ✅ Testes de conexão automáticos
- ✅ Criação automática de bancos/coleções
- ✅ Gerenciamento de sessões
- ✅ Namespaces no Redis
- ✅ Índices automáticos no MongoDB
- ✅ Logging detalhado
