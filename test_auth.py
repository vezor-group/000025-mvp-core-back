#!/usr/bin/env python3
"""
Script de teste para o sistema de autenticação
Execute: python test_auth.py
"""

import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_auth_system():
    """Testa o sistema de autenticação completo"""
    
    print("🧪 Testando Sistema de Autenticação VZR-LBS")
    print("=" * 50)
    
    # 1. Teste de cadastro básico
    print("\n1️⃣ Testando cadastro básico...")
    signup_data = {
        "email": "teste@exemplo.com",
        "name": "Usuário Teste",
        "password": "senha123"
    }
    
    try:
        response = requests.post(f"{API_URL}/signup", json=signup_data)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Cadastro realizado com sucesso!")
        else:
            print("❌ Erro no cadastro")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # 2. Teste de login básico
    print("\n2️⃣ Testando login básico...")
    signin_data = {
        "providerAuth": "basic",
        "email": "teste@exemplo.com",
        "senhaHash": "senha123"
    }
    
    try:
        response = requests.post(f"{API_URL}/signin", json=signin_data)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get("data", {}).get("access_token")
            print("✅ Login realizado com sucesso!")
            
            # 3. Teste de endpoint protegido
            print("\n3️⃣ Testando endpoint protegido...")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{API_URL}/me", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ Endpoint protegido acessado com sucesso!")
            else:
                print("❌ Erro ao acessar endpoint protegido")
                
        else:
            print("❌ Erro no login")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # 4. Teste de cadastro social
    print("\n4️⃣ Testando cadastro social (Google)...")
    signup_social_data = {
        "email": "usuario@gmail.com",
        "name": "Usuário Google",
        "providerAuth": "google",
        "providerId": "google_user_123"
    }
    
    try:
        response = requests.post(f"{API_URL}/signup", json=signup_social_data)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Cadastro social realizado com sucesso!")
        else:
            print("❌ Erro no cadastro social")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # 5. Teste de login social
    print("\n5️⃣ Testando login social (Google)...")
    signin_social_data = {
        "providerAuth": "google",
        "email": "usuario@gmail.com"
    }
    
    try:
        response = requests.post(f"{API_URL}/signin", json=signin_social_data)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Login social realizado com sucesso!")
        else:
            print("❌ Erro no login social")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")
    print(f"📅 Timestamp: {datetime.now().isoformat()}")

def test_server_status():
    """Testa se o servidor está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Servidor está rodando!")
            return True
        else:
            print("❌ Servidor não está respondendo corretamente")
            return False
    except Exception as e:
        print(f"❌ Servidor não está rodando: {e}")
        print("💡 Execute: python main.py")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do sistema de autenticação...")
    
    if test_server_status():
        test_auth_system()
    else:
        print("\n❌ Não foi possível executar os testes.")
        print("💡 Certifique-se de que o servidor está rodando com: python main.py")
