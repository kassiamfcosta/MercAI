"""
Utilitários JWT - Autenticação

Módulo responsável por gerenciar tokens JWT para autenticação.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import request, jsonify
import logging

from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def generate_token(user_id: str, email: str) -> str:
    """
    Gera um token JWT para o usuário.
    
    Args:
        user_id: ID do usuário (UUID como string).
        email: Email do usuário.
    
    Returns:
        str: Token JWT codificado.
    
    Raises:
        Exception: Se houver erro ao gerar o token.
    """
    try:
        payload = {
            'user_id': str(user_id),
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        logger.info(f"Token JWT gerado para usuário: {email}")
        return token
    except Exception as e:
        logger.error(f"Erro ao gerar token JWT: {e}")
        raise


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica e valida um token JWT.
    
    Args:
        token: Token JWT a ser decodificado.
    
    Returns:
        Optional[Dict[str, Any]]: Payload do token ou None se inválido.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token JWT expirado")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token JWT inválido: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao decodificar token JWT: {e}")
        return None


def token_required(f):
    """
    Decorator para proteger rotas que requerem autenticação.
    
    Extrai o token do header Authorization e valida.
    Adiciona o user_id ao request para uso na função decorada.
    
    Example:
        ```python
        @app.route('/api/protected')
        @token_required
        def protected_route(current_user_id):
            return {"user_id": current_user_id}
        ```
    
    Args:
        f: Função Flask a ser decorada.
    
    Returns:
        Função decorada que requer token JWT válido.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extrair token do header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Tentativa de acesso sem token JWT")
            return jsonify({
                "success": False,
                "message": "Token JWT não fornecido"
            }), 401
        
        # Formato esperado: "Bearer <token>"
        try:
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                raise ValueError("Tipo de autenticação inválido")
        except ValueError:
            logger.warning(f"Formato de header Authorization inválido: {auth_header}")
            return jsonify({
                "success": False,
                "message": "Formato de autenticação inválido. Use: Bearer <token>"
            }), 401
        
        # Decodificar e validar token
        payload = decode_token(token)
        
        if not payload:
            logger.warning("Tentativa de acesso com token JWT inválido ou expirado")
            return jsonify({
                "success": False,
                "message": "Token JWT inválido ou expirado"
            }), 401
        
        # Adicionar user_id aos kwargs da função
        user_id = payload.get('user_id')
        if not user_id:
            logger.error("Token JWT não contém user_id")
            return jsonify({
                "success": False,
                "message": "Token JWT malformado"
            }), 401
        
        # Passar user_id como primeiro argumento da função
        return f(user_id, *args, **kwargs)
    
    return decorated
