"""
Script para testar manualmente os endpoints da API.

Execute: python test_manual.py
"""

import os
import sys
import requests
import json

# Configurar encoding para evitar problemas com emojis no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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

def print_section(title):
    """Imprime seção formatada."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health():
    """Testa endpoint de health check."""
    print_section("Teste: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("[ERRO] Servidor nao esta rodando!")
        print("Execute primeiro: python test_server.py")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

def test_register():
    """Testa registro de usuário."""
    print_section("Teste: Registrar Usuário")
    try:
        # Usar email único baseado em timestamp para evitar conflitos
        import time
        unique_email = f'test_{int(time.time())}@example.com'
        
        data = {
            'email': unique_email,
            'password': 'testpass123',
            'name': 'Test User Novo'
        }
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json=data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            token = response.json()['data']['token']
            print(f"\n[OK] Token recebido: {token[:50]}...")
            print(f"[INFO] Usuario criado com email: {unique_email}")
            return token
        else:
            print(f"[AVISO] Status {response.status_code} - pode ser que o email ja existe")
        return None
    except Exception as e:
        print(f"[ERRO] {e}")
        return None

def test_login():
    """Testa login de usuário."""
    print_section("Teste: Login")
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
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            token = response.json()['data']['token']
            print(f"\n[OK] Token recebido: {token[:50]}...")
            return token
        return None
    except Exception as e:
        print(f"[ERRO] {e}")
        return None

def test_me(token):
    """Testa endpoint /me."""
    print_section("Teste: Obter Dados do Usuário (/me)")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{BASE_URL}/api/auth/me',
            headers=headers,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

def test_register_duplicate():
    """Testa registro com email duplicado."""
    print_section("Teste: Registro com Email Duplicado")
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
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Deve retornar 409 (Conflict)
        if response.status_code == 409:
            print("\n[OK] Teste passou: Email duplicado corretamente rejeitado")
            return True
        else:
            print("\n[AVISO] Status inesperado (esperado 409)")
            return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

def main():
    """Função principal de testes."""
    print("\n" + "=" * 60)
    print("  MERC AI BACKEND - TESTES MANUAIS")
    print("=" * 60)
    print("\n[AVISO] Certifique-se de que o servidor esta rodando!")
    print("   Execute em outro terminal: python test_server.py\n")
    
    # Aguardar um pouco para garantir que o servidor está pronto
    import time
    print("[INFO] Aguardando servidor iniciar...")
    time.sleep(2)
    
    results = []
    
    # Teste 1: Health Check
    results.append(("Health Check", test_health()))
    
    if not results[-1][1]:
        print("\n[ERRO] Servidor nao esta respondendo. Pare os testes aqui.")
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
    print_section("RESUMO DOS TESTES")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK] PASSOU" if result else "[ERRO] FALHOU"
        print(f"  {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n[SUCESSO] Todos os testes passaram!")
    else:
        print(f"\n[AVISO] {total - passed} teste(s) falharam")

if __name__ == '__main__':
    main()

