# Sistema de Autenticação - VZR-LBS API

## Visão Geral

O sistema de autenticação foi implementado seguindo a arquitetura DDD (Domain-Driven Design) e oferece suporte a:

- **Login Básico**: Email e senha
- **Login Social**: Google e Microsoft
- **Cadastro de Usuários**: Básico e social
- **Gerenciamento de Sessões**: JWT com refresh tokens
- **Middleware de Autenticação**: Para proteger endpoints

## Endpoints Disponíveis

### 1. Login (POST /api/v1/signin)

#### Login Básico
```json
{
    "providerAuth": "basic",
    "email": "usuario@exemplo.com",
    "senhaHash": "senha123"
}
```

#### Login Google
```json
{
    "providerAuth": "google",
    "email": "usuario@gmail.com"
}
```

#### Login Microsoft
```json
{
    "providerAuth": "microsoft",
    "email": "usuario@outlook.com"
}
```

**Resposta de Sucesso:**
```json
{
    "success": true,
    "message": "Login realizado com sucesso",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "expires_at": "2024-01-15T10:30:00",
        "user": {
            "id": "user_1234567890",
            "email": "usuario@exemplo.com",
            "name": "João Silva",
            "role": "user",
            "status": "active"
        }
    }
}
```

### 2. Cadastro (POST /api/v1/signup)

#### Cadastro Básico
```json
{
    "email": "novo@exemplo.com",
    "name": "Novo Usuário",
    "password": "senha123"
}
```

#### Cadastro Social
```json
{
    "email": "usuario@gmail.com",
    "name": "Usuário Google",
    "providerAuth": "google",
    "providerId": "google_user_id_123"
}
```

**Resposta de Sucesso:**
```json
{
    "success": true,
    "message": "Usuário criado com sucesso. Verifique seu email para ativar a conta.",
    "data": {
        "user": {
            "id": "user_1234567890",
            "email": "novo@exemplo.com",
            "name": "Novo Usuário",
            "role": "user",
            "status": "pending",
            "email_verified": false,
            "created_at": "2024-01-15T10:00:00"
        }
    }
}
```

### 3. Informações do Usuário (GET /api/v1/me)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta:**
```json
{
    "success": true,
    "message": "Usuário autenticado",
    "data": {
        "user": {
            "id": "user_1234567890",
            "email": "usuario@exemplo.com",
            "name": "João Silva",
            "role": "user",
            "status": "active"
        },
        "session": {
            "id": "session_user_1234567890_1705312800",
            "expires_at": "2024-01-15T10:30:00"
        }
    }
}
```

### 4. Renovar Token (POST /api/v1/refresh)

```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta:**
```json
{
    "success": true,
    "message": "Token renovado com sucesso",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "expires_at": "2024-01-15T10:30:00"
    }
}
```

## Estrutura da Arquitetura DDD

### Domain Layer (Domínio)
- **Entidades**: `User`, `AuthSession`, `AuthProvider`
- **Serviços**: `AuthService`, `PasswordService`, `TokenService`
- **Enums**: `UserStatus`, `UserRole`, `AuthProviderType`

### Application Layer (Aplicação)
- **Casos de Uso**: `SignInUseCase`, `SignUpUseCase`, `TokenValidationUseCase`
- **Orquestração**: Coordenação entre domínio e infraestrutura

### Infrastructure Layer (Infraestrutura)
- **Repositórios**: `UserRepository`, `AuthSessionRepository`, `AuthProviderRepository`
- **Implementações**: Versões em memória para desenvolvimento

### Interface Layer (Interface)
- **Controllers**: `AuthController`
- **DTOs**: `SignInRequest`, `SignUpRequest`, `AuthResponse`
- **Middleware**: `AuthMiddleware`

## Configuração

### Variáveis de Ambiente

```bash
# Configurações da API
PROJECT_NAME=VZR-LBS-v0-mvp-base-back
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Configurações de Autenticação
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# Configurações de Banco de Dados
DB_POSTGRES_HOST=localhost
DB_POSTGRES_PORT=5432
DB_POSTGRES_DATABASE=vzr_lbs
DB_POSTGRES_USER=postgres
DB_POSTGRES_PASSWORD=password

# Configurações de Provedores Sociais
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
```

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

## Exemplos de Uso

### 1. Cadastro e Login Básico

```python
import requests

# Cadastro
signup_data = {
    "email": "teste@exemplo.com",
    "name": "Usuário Teste",
    "password": "senha123"
}

response = requests.post("http://localhost:8000/api/v1/signup", json=signup_data)
print(response.json())

# Login
signin_data = {
    "providerAuth": "basic",
    "email": "teste@exemplo.com",
    "senhaHash": "senha123"
}

response = requests.post("http://localhost:8000/api/v1/signin", json=signin_data)
auth_data = response.json()

# Usar token para acessar endpoint protegido
headers = {"Authorization": f"Bearer {auth_data['data']['access_token']}"}
response = requests.get("http://localhost:8000/api/v1/me", headers=headers)
print(response.json())
```

### 2. Usando o Middleware de Autenticação

```python
from fastapi import FastAPI, Depends
from app.interface.auth.auth_middleware import auth_middleware

app = FastAPI()

@app.get("/protected")
async def protected_endpoint(current_user: dict = Depends(auth_middleware.get_current_user)):
    return {"message": f"Olá {current_user['user']['name']}!"}

@app.get("/admin-only")
async def admin_endpoint(current_user: dict = Depends(auth_middleware.require_role("admin"))):
    return {"message": "Acesso administrativo concedido"}
```

## Segurança

- **Senhas**: Hash com PBKDF2 e salt
- **Tokens**: JWT com assinatura HMAC
- **Sessões**: Controle de expiração e revogação
- **Validação**: Verificação de email e força da senha

## Próximos Passos

1. **Integração com Banco de Dados**: Substituir repositórios em memória
2. **Verificação de Email**: Implementar envio de emails
3. **Provedores Sociais**: Integração real com Google/Microsoft APIs
4. **Rate Limiting**: Proteção contra ataques de força bruta
5. **Auditoria**: Log de tentativas de login e ações do usuário
