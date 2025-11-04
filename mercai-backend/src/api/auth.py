"""
API de Autenticação - Endpoints

Módulo responsável pelos endpoints de autenticação (registro, login, perfil).
"""

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
import logging

from src.config.database import get_db
from src.models.user import User
from src.utils.jwt import generate_token, token_required
from src.schemas.auth_schema import RegisterSchema, LoginSchema

logger = logging.getLogger(__name__)

# Criar blueprint
auth_bp = Blueprint('auth', __name__)

# Instanciar schemas
register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registro de novo usuário.
    
    POST /api/auth/register
    Body: {email, password, name (opcional)}
    
    Returns:
        200: Usuário criado com sucesso + token JWT
        400: Erro de validação
        409: Email já existe
        500: Erro interno
    """
    try:
        # Validar dados de entrada
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        # Validar schema
        errors = register_schema.validate(data)
        if errors:
            return jsonify({
                "success": False,
                "message": "Erro de validação",
                "errors": errors
            }), 400
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Verificar se email já existe
            existing_user = db.query(User).filter(User.email == data['email']).first()
            if existing_user:
                logger.warning(f"Tentativa de registro com email já existente: {data['email']}")
                return jsonify({
                    "success": False,
                    "message": "Email já cadastrado"
                }), 409
            
            # Criar novo usuário
            user = User(
                email=data['email'],
                name=data.get('name')
            )
            user.set_password(data['password'])
            
            # Salvar no banco
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Gerar token JWT
            token = generate_token(str(user.id), user.email)
            
            logger.info(f"Usuário registrado com sucesso: {user.email}")
            
            return jsonify({
                "success": True,
                "message": "Usuário registrado com sucesso",
                "data": {
                    "user": user.to_dict(),
                    "token": token
                }
            }), 201
        
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Erro de integridade ao registrar usuário: {e}")
            return jsonify({
                "success": False,
                "message": "Erro ao registrar usuário"
            }), 409
        
        except ValueError as e:
            db.rollback()
            logger.error(f"Erro de validação ao registrar usuário: {e}")
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro interno ao registrar usuário: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao registrar usuário"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado no registro: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuário.
    
    POST /api/auth/login
    Body: {email, password}
    
    Returns:
        200: Login bem-sucedido + token JWT
        400: Erro de validação
        401: Credenciais inválidas
        500: Erro interno
    """
    try:
        # Validar dados de entrada
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        # Validar schema
        errors = login_schema.validate(data)
        if errors:
            return jsonify({
                "success": False,
                "message": "Erro de validação",
                "errors": errors
            }), 400
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar usuário por email
            user = db.query(User).filter(User.email == data['email']).first()
            
            # Verificar credenciais
            if not user or not user.check_password(data['password']):
                logger.warning(f"Tentativa de login com credenciais inválidas: {data['email']}")
                return jsonify({
                    "success": False,
                    "message": "Email ou senha inválidos"
                }), 401
            
            # Gerar token JWT
            token = generate_token(str(user.id), user.email)
            
            logger.info(f"Login bem-sucedido: {user.email}")
            
            return jsonify({
                "success": True,
                "message": "Login bem-sucedido",
                "data": {
                    "user": user.to_dict(),
                    "token": token
                }
            }), 200
        
        except Exception as e:
            logger.error(f"Erro interno ao fazer login: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao fazer login"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado no login: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user_id: str):
    """
    Endpoint para obter dados do usuário logado.
    
    GET /api/auth/me
    Header: Authorization: Bearer <token>
    
    Args:
        current_user_id: ID do usuário extraído do token JWT.
    
    Returns:
        200: Dados do usuário
        404: Usuário não encontrado
        500: Erro interno
    """
    try:
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar usuário
            user = db.query(User).filter(User.id == current_user_id).first()
            
            if not user:
                logger.warning(f"Usuário não encontrado: {current_user_id}")
                return jsonify({
                    "success": False,
                    "message": "Usuário não encontrado"
                }), 404
            
            logger.info(f"Dados do usuário recuperados: {user.email}")
            
            return jsonify({
                "success": True,
                "message": "Dados do usuário recuperados",
                "data": {
                    "user": user.to_dict()
                }
            }), 200
        
        except Exception as e:
            logger.error(f"Erro interno ao buscar usuário: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar usuário"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar dados do usuário: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500
