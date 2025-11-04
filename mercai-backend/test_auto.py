"""
Script para testar automaticamente os endpoints da API.

Execute: python test_auto.py
"""

import os
import sys
import time
import requests
import json

# Configurar variáveis de ambiente para teste
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-development-only')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
os.environ.setdefault('GEMINI_API_KEY', 'test-key')

# Porta configurável via variável de ambiente, padrão 8000
PORT = int(os.environ.get('TEST_PORT', 8000))
BASE_URL = f'http://localhost:{PORT}'

def print_header(title):
    """Imprime cabecalho formatado."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def wait_for_server(max_retries=10, delay=1):
    """Aguarda servidor ficar disponivel."""
    print("Aguardando servidor iniciar...")
    for i in range(max_retries):
        try:
            response = requests.get(f'{BASE_URL}/health', timeout=2)
            if response.status_code == 200:
                print("Servidor esta respondendo!")
                return True
        except:
            time.sleep(delay)
            print(f"Tentativa {i+1}/{max_retries}...")
    return False

def test_health():
    """Testa endpoint de health check."""
    print_header("Teste: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Status: {data.get('status')}")
        print(f"Environment: {data.get('environment')}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERRO: Servidor nao esta rodando!")
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def test_register():
    """Testa registro de usuario."""
    print_header("Teste: Registrar Usuario")
    try:
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User'
        }
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json=data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        if response.status_code == 201:
            token = result.get('data', {}).get('token', '')
            if token:
                print(f"Token recebido (primeiros 50 chars): {token[:50]}...")
                return token
        return None
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def test_login():
    """Testa login de usuario."""
    print_header("Teste: Login")
    try:
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json=data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        if response.status_code == 200:
            token = result.get('data', {}).get('token', '')
            if token:
                print(f"Token recebido (primeiros 50 chars): {token[:50]}...")
                return token
        return None
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def test_me(token):
    """Testa endpoint /me."""
    print_header("Teste: Obter Dados do Usuario (/me)")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{BASE_URL}/api/auth/me',
            headers=headers,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        if result.get('data', {}).get('user'):
            user = result['data']['user']
            print(f"User Email: {user.get('email')}")
            print(f"User Name: {user.get('name')}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def test_register_duplicate():
    """Testa registro com email duplicado."""
    print_header("Teste: Registro com Email Duplicado")
    try:
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User 2'
        }
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json=data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        # Deve retornar 409 (Conflict)
        if response.status_code == 409:
            print("OK: Email duplicado corretamente rejeitado")
            return True
        else:
            print(f"AVISO: Status inesperado (esperado 409, recebido {response.status_code})")
            return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def main():
    """Funcao principal de testes."""
    print_header("MERC AI BACKEND - TESTES AUTOMATICOS")
    
    # Aguardar servidor
    if not wait_for_server():
        print("\nERRO: Servidor nao esta disponivel!")
        print("Execute primeiro: python test_server.py")
        return
    
    results = []
    
    # Teste 1: Health Check
    results.append(("Health Check", test_health()))
    
    if not results[-1][1]:
        print("\nERRO: Servidor nao esta respondendo. Parando testes.")
        return
    
    # Teste 2: Registro
    token = test_register()
    results.append(("Registro", token is not None))
    
    # Teste 3: Registro Duplicado
    results.append(("Registro Duplicado", test_register_duplicate()))
    
    # Teste 4: Login
    token = test_login()
    results.append(("Login", token is not None))
    
    # Teste 5: /me
    if token:
        results.append(("Obter Dados (/me)", test_me(token)))
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"  {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\nSUCESSO: Todos os testes passaram!")
    else:
        print(f"\nATENCAO: {total - passed} teste(s) falharam")

if __name__ == '__main__':
    main()

