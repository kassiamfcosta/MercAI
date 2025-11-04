"""
Script de teste completo - limpa e testa tudo.
"""

import os
import sys
import time
import requests
import json

# Configurar variáveis de ambiente
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test_full.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
os.environ.setdefault('GEMINI_API_KEY', 'test-key')

# Porta configurável via variável de ambiente, padrão 8000
PORT = int(os.environ.get('TEST_PORT', 8000))
BASE_URL = f'http://localhost:{PORT}'

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def wait_for_server(max_retries=10, delay=1):
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
    print_header("Teste: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Status: {data.get('status')}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def test_register():
    print_header("Teste: Registrar Usuario")
    try:
        data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'name': 'New User'
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
                print(f"Token recebido!")
                return token
        return None
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def test_login(email, password):
    print_header("Teste: Login")
    try:
        data = {'email': email, 'password': password}
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json=data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        
        if response.status_code == 200:
            token = result.get('data', {}).get('token', '')
            if token:
                print(f"Token recebido!")
                return token
        return None
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def test_me(token):
    print_header("Teste: Obter Dados (/me)")
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

def main():
    print_header("MERC AI BACKEND - TESTES COMPLETOS")
    
    if not wait_for_server():
        print("\nERRO: Servidor nao esta disponivel!")
        print("Execute primeiro: python test_server.py")
        return
    
    results = []
    
    # Teste 1: Health Check
    results.append(("Health Check", test_health()))
    
    if not results[-1][1]:
        print("\nERRO: Servidor nao esta respondendo.")
        return
    
    # Teste 2: Registro
    token = test_register()
    results.append(("Registro", token is not None))
    
    # Teste 3: Login
    token = test_login('newuser@example.com', 'testpass123')
    results.append(("Login", token is not None))
    
    # Teste 4: /me
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
        return True
    else:
        print(f"\nATENCAO: {total - passed} teste(s) falharam")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

