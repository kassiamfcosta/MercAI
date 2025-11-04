"""
Script para testar o servidor Flask manualmente.

Execute: python test_server.py
"""

import os
import sys
from flask import Flask

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar variáveis de ambiente para teste
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-development')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')

# Importar app
from main import app

if __name__ == '__main__':
    print("=" * 60)
    print("MercAI Backend - Servidor de Testes")
    print("=" * 60)
    print("\nEndpoints disponíveis:")
    print("  GET  /health - Health check")
    print("  POST /api/auth/register - Registrar usuário")
    print("  POST /api/auth/login - Fazer login")
    print("  GET  /api/auth/me - Dados do usuário logado")
    # Porta configurável via variável de ambiente, padrão 8000
    port = int(os.environ.get('PORT', 8000))
    
    print(f"\nServidor iniciando em http://localhost:{port}")
    print("Pressione Ctrl+C para parar\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=True)

