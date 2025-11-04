"""
Script de diagnostico para verificar problemas no servidor.
"""

import os
import sys
import traceback

# Configurar variáveis de ambiente
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('JWT_SECRET_KEY', 'test-jwt-secret-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
os.environ.setdefault('GEMINI_API_KEY', 'test-key')

print("=== DIAGNOSTICO DO MERC AI BACKEND ===\n")

# Teste 1: Importar configuracoes
print("1. Testando importacao de configuracoes...")
try:
    from src.config.settings import Settings
    settings = Settings()
    print("   OK: Settings importado")
    print(f"   DATABASE_URL: {settings.DATABASE_URL[:30]}...")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 2: Importar database
print("\n2. Testando importacao do database...")
try:
    from src.config.database import Base, engine, init_db, get_db
    print("   OK: Database importado")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 3: Importar models
print("\n3. Testando importacao dos models...")
try:
    from src.models.user import User
    print("   OK: User model importado")
    from src.models import store, product, offer, shopping_list, list_item
    print("   OK: Todos os models importados")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Inicializar banco
print("\n4. Testando inicializacao do banco...")
try:
    init_db()
    print("   OK: Banco inicializado")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 5: Criar sessao
print("\n5. Testando criacao de sessao...")
try:
    db = next(get_db())
    print("   OK: Sessao criada")
    db.close()
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 6: Criar usuario
print("\n6. Testando criacao de usuario...")
try:
    db = next(get_db())
    try:
        # Verificar se usuario existe
        existing = db.query(User).filter(User.email == 'test@example.com').first()
        if existing:
            print("   OK: Usuario ja existe (teste anterior)")
        else:
            # Criar usuario
            user = User(email='test@example.com', name='Test User')
            user.set_password('testpass123')
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"   OK: Usuario criado (ID: {user.id})")
    finally:
        db.close()
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 7: Importar API
print("\n7. Testando importacao da API...")
try:
    from src.api.auth import auth_bp
    print("   OK: Auth blueprint importado")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

# Teste 8: Importar JWT
print("\n8. Testando importacao do JWT...")
try:
    from src.utils.jwt import generate_token, decode_token
    print("   OK: JWT utils importado")
    
    # Testar geracao de token
    token = generate_token('test-user-id', 'test@example.com')
    payload = decode_token(token)
    if payload:
        print(f"   OK: Token gerado e decodificado")
    else:
        print("   ERRO: Token nao foi decodificado")
except Exception as e:
    print(f"   ERRO: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n=== DIAGNOSTICO COMPLETO ===")
print("Todos os testes passaram! O sistema esta pronto.")

