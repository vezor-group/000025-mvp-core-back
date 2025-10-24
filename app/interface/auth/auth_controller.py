from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from app.interface.auth.auth_dto import SignInRequest, SignUpRequest, AuthResponse, SessionInfo
from app.aplication.auth.signin_use_case import SignInUseCase
from app.aplication.auth.signup_use_case import SignUpUseCase
from app.aplication.auth.token_validation_use_case import TokenValidationUseCase
from app.domain.auth.auth_provider import AuthProviderType
from app.domain.auth.services.token_service import TokenService
from app.domain.auth.services.auth_service import AuthService
from app.infrastructure.repositories.auth.user_repository import InMemoryUserRepository
from app.infrastructure.repositories.auth.auth_session_repository import InMemoryAuthSessionRepository
from app.infrastructure.repositories.auth.auth_provider_repository import InMemoryAuthProviderRepository


# Inicialização dos repositórios (em produção, usar injeção de dependência)
user_repository = InMemoryUserRepository()
session_repository = InMemoryAuthSessionRepository()
provider_repository = InMemoryAuthProviderRepository()

# Inicialização dos serviços
token_service = TokenService(secret_key="your-secret-key-here")  # Em produção, usar variável de ambiente
auth_service = AuthService(token_service)

# Inicialização dos casos de uso
signin_use_case = SignInUseCase(auth_service, user_repository, session_repository)
signup_use_case = SignUpUseCase(auth_service, user_repository, provider_repository)
token_validation_use_case = TokenValidationUseCase(token_service, user_repository, session_repository)

# Router para autenticação
auth_router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@auth_router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest):
    """
    Endpoint de login
    
    Suporta:
    - Login básico: providerAuth="basic", email, senhaHash
    - Login Google: providerAuth="google", email
    - Login Microsoft: providerAuth="microsoft", email
    """
    try:
        provider_type = AuthProviderType(request.providerAuth)
        
        if provider_type == AuthProviderType.BASIC:
            if not request.senhaHash:
                raise HTTPException(status_code=400, detail="Senha é obrigatória para login básico")
            
            result = await signin_use_case.execute_basic(request.email, request.senhaHash)
            
        elif provider_type in [AuthProviderType.GOOGLE, AuthProviderType.MICROSOFT]:
            # Para login social, assumimos que o providerId é o email por enquanto
            # Em produção, você validaria o token do provedor social
            result = await signin_use_case.execute_social(
                provider_type, 
                request.email, 
                request.email  # Em produção, seria o ID real do provedor
            )
        else:
            raise HTTPException(status_code=400, detail="Tipo de provedor não suportado")
        
        if not result:
            return AuthResponse(
                success=False,
                message="Credenciais inválidas",
                error="INVALID_CREDENTIALS"
            )
        
        return AuthResponse(
            success=True,
            message="Login realizado com sucesso",
            data=result
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@auth_router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """
    Endpoint de cadastro
    
    Suporta:
    - Cadastro básico: email, name, password
    - Cadastro social: email, name, providerAuth, providerId
    """
    try:
        if request.password:
            # Cadastro básico
            result = await signup_use_case.execute_basic(
                request.email, 
                request.name, 
                request.password
            )
        elif request.providerAuth and request.providerId:
            # Cadastro social
            provider_type = AuthProviderType(request.providerAuth)
            result = await signup_use_case.execute_social(
                provider_type,
                request.email,
                request.name,
                request.providerId
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail="Para cadastro básico forneça 'password' ou para social forneça 'providerAuth' e 'providerId'"
            )
        
        return AuthResponse(
            success=True,
            message=result["message"],
            data=result
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@auth_router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Endpoint para obter informações do usuário atual
    """
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token de autorização não fornecido")
        
        access_token = authorization.replace("Bearer ", "")
        result = await token_validation_use_case.execute(access_token)
        
        if not result:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        return AuthResponse(
            success=True,
            message="Usuário autenticado",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Endpoint para renovar token de acesso
    """
    try:
        result = await token_validation_use_case.refresh_token(refresh_token)
        
        if not result:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")
        
        return AuthResponse(
            success=True,
            message="Token renovado com sucesso",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


