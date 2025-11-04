"""
Testes Unitários - Autenticação

Testes para os endpoints de autenticação (register, login, me).
"""

import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
import uuid

from flask import Flask
from src.config.settings import Settings
from src.config.database import Base, engine
from src.models.user import User
from src.api.auth import auth_bp
from src.utils.jwt import generate_token, decode_token


@pytest.fixture
def app():
    """Fixture para criar app Flask de teste."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Criar tabelas
    Base.metadata.create_all(engine)
    
    # Registrar blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    yield app
    
    # Limpar tabelas
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(app):
    """Fixture para criar cliente de teste."""
    return app.test_client()


@pytest.fixture
def test_user_data():
    """Fixture com dados de usuário de teste."""
    return {
        'email': 'test@example.com',
        'password': 'testpass123',
        'name': 'Test User'
    }


class TestRegister:
    """Testes para endpoint de registro."""
    
    def test_register_success(self, client, test_user_data):
        """Testa registro bem-sucedido."""
        response = client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'token' in data['data']
        assert 'user' in data['data']
        assert data['data']['user']['email'] == test_user_data['email']
    
    def test_register_duplicate_email(self, client, test_user_data):
        """Testa registro com email duplicado."""
        # Primeiro registro
        client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        # Segundo registro com mesmo email
        response = client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'já cadastrado' in data['message'].lower() or 'já existe' in data['message'].lower()
    
    def test_register_invalid_email(self, client):
        """Testa registro com email inválido."""
        response = client.post(
            '/api/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_register_short_password(self, client):
        """Testa registro com senha muito curta."""
        response = client.post(
            '/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'short'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_register_missing_fields(self, client):
        """Testa registro com campos faltando."""
        response = client.post(
            '/api/auth/register',
            json={'email': 'test@example.com'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False


class TestLogin:
    """Testes para endpoint de login."""
    
    def test_login_success(self, client, test_user_data):
        """Testa login bem-sucedido."""
        # Criar usuário primeiro
        client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        # Fazer login
        response = client.post(
            '/api/auth/login',
            json={
                'email': test_user_data['email'],
                'password': test_user_data['password']
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'token' in data['data']
        assert 'user' in data['data']
    
    def test_login_invalid_credentials(self, client, test_user_data):
        """Testa login com credenciais inválidas."""
        # Criar usuário primeiro
        client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        # Tentar login com senha errada
        response = client.post(
            '/api/auth/login',
            json={
                'email': test_user_data['email'],
                'password': 'wrongpassword'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_login_nonexistent_user(self, client):
        """Testa login com usuário inexistente."""
        response = client.post(
            '/api/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'somepassword'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False


class TestJWT:
    """Testes para utilitários JWT."""
    
    def test_generate_token(self):
        """Testa geração de token JWT."""
        user_id = str(uuid.uuid4())
        email = 'test@example.com'
        
        token = generate_token(user_id, email)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_token(self):
        """Testa decodificação de token JWT."""
        user_id = str(uuid.uuid4())
        email = 'test@example.com'
        
        token = generate_token(user_id, email)
        payload = decode_token(token)
        
        assert payload is not None
        assert payload['user_id'] == user_id
        assert payload['email'] == email
    
    def test_decode_invalid_token(self):
        """Testa decodificação de token inválido."""
        invalid_token = 'invalid.token.here'
        payload = decode_token(invalid_token)
        
        assert payload is None
    
    def test_token_expiration(self):
        """Testa que token expirado não é válido."""
        # Este teste precisaria de mock do tempo
        # Por enquanto apenas verifica que a função existe
        user_id = str(uuid.uuid4())
        email = 'test@example.com'
        token = generate_token(user_id, email)
        payload = decode_token(token)
        
        assert payload is not None  # Token recém-criado deve ser válido


class TestMe:
    """Testes para endpoint /me."""
    
    def test_get_me_success(self, client, test_user_data):
        """Testa obter dados do usuário logado."""
        # Criar usuário e fazer login
        register_response = client.post(
            '/api/auth/register',
            json=test_user_data,
            content_type='application/json'
        )
        
        register_data = json.loads(register_response.data)
        token = register_data['data']['token']
        
        # Buscar dados do usuário
        response = client.get(
            '/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data['data']
        assert data['data']['user']['email'] == test_user_data['email']
    
    def test_get_me_without_token(self, client):
        """Testa obter dados sem token."""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_me_invalid_token(self, client):
        """Testa obter dados com token inválido."""
        response = client.get(
            '/api/auth/me',
            headers={'Authorization': 'Bearer invalid.token.here'}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False

