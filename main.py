"""
VZR-LBS API - Sistema de Balcão de Milhas
API principal do sistema VZR-LBS v0 MVP Base
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação da aplicação FastAPI
app = FastAPI(
    title="VZR-LBS API",
    description="Sistema de Balcão de Milhas - VZR-LBS v0 MVP Base",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variáveis de ambiente
PROJECT_NAME = os.getenv("PROJECT_NAME", "VZR-LBS-v0-mvp-base-back")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "True").lower() == "true"

# Endpoint raiz
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à VZR-LBS API",
        "project": PROJECT_NAME,
        "version": "0.1.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {
        "status": "healthy",
        "service": PROJECT_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0"
    }

# Endpoint de informações do sistema
@app.get("/info")
async def system_info():
    """Informações do sistema"""
    return {
        "project_name": PROJECT_NAME,
        "api_host": API_HOST,
        "api_port": API_PORT,
        "debug_mode": API_DEBUG,
        "environment": {
            "db_postgres_host": os.getenv("DB_POSTGRES_HOST", "not_configured"),
            "db_mongo_host": os.getenv("DB_MONGO_HOST", "not_configured"),
            "db_redis_host": os.getenv("DB_REDIS_HOST", "not_configured")
        },
        "timestamp": datetime.now().isoformat()
    }

# Endpoint de teste dos bancos de dados
@app.get("/database/status")
async def database_status():
    """Status dos bancos de dados"""
    status = {
        "postgres": {
            "host": os.getenv("DB_POSTGRES_HOST", "not_configured"),
            "port": os.getenv("DB_POSTGRES_PORT", "not_configured"),
            "database": os.getenv("DB_POSTGRES_DATABASE", "not_configured"),
            "status": "configured" if os.getenv("DB_POSTGRES_HOST") else "not_configured"
        },
        "mongo": {
            "host": os.getenv("DB_MONGO_HOST", "not_configured"),
            "port": os.getenv("DB_MONGO_PORT", "not_configured"),
            "database": os.getenv("DB_MONGO_DATABASE", "not_configured"),
            "status": "configured" if os.getenv("DB_MONGO_HOST") else "not_configured"
        },
        "redis": {
            "host": os.getenv("DB_REDIS_HOST", "not_configured"),
            "port": os.getenv("DB_REDIS_PORT", "not_configured"),
            "database": os.getenv("DB_REDIS_DATABASE", "not_configured"),
            "status": "configured" if os.getenv("DB_REDIS_HOST") else "not_configured"
        }
    }
    
    return {
        "databases": status,
        "timestamp": datetime.now().isoformat()
    }

# Endpoint de exemplo para milhas
@app.get("/milhas")
async def get_milhas():
    """Endpoint de exemplo para milhas"""
    return {
        "message": "Endpoint de milhas - em desenvolvimento",
        "data": {
            "milhas_disponiveis": 0,
            "milhas_utilizadas": 0,
            "milhas_pendentes": 0
        },
        "timestamp": datetime.now().isoformat()
    }

# Endpoint de exemplo para ofertas
@app.get("/ofertas")
async def get_ofertas():
    """Endpoint de exemplo para ofertas"""
    return {
        "message": "Endpoint de ofertas - em desenvolvimento",
        "data": {
            "ofertas_ativas": 0,
            "ofertas_pendentes": 0,
            "ofertas_finalizadas": 0
        },
        "timestamp": datetime.now().isoformat()
    }

# Handler de erro global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    logger.info(f"🚀 Iniciando {PROJECT_NAME} na porta {API_PORT}")
    logger.info(f"📊 Modo debug: {API_DEBUG}")
    logger.info(f"🌐 Host: {API_HOST}")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de finalização"""
    logger.info(f"🛑 Finalizando {PROJECT_NAME}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_DEBUG,
        log_level="info"
    )
