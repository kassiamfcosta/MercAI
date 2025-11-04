"""
API de Listas - Endpoints

Módulo responsável pelos endpoints de CRUD de listas de compras.
"""

from flask import Blueprint, request, jsonify
from typing import Optional
import uuid
import logging

from src.config.database import get_db
from src.models.shopping_list import ShoppingList
from src.models.list_item import ListItem
from src.models.product import Product
from src.utils.jwt import token_required

logger = logging.getLogger(__name__)

# Criar blueprint
lists_bp = Blueprint('lists', __name__)


def _validate_list_ownership(db, list_id: str, user_id: str) -> bool:
    """
    Valida se o usuário é dono da lista.
    
    Args:
        db: Sessão do banco de dados.
        list_id: UUID da lista.
        user_id: UUID do usuário.
    
    Returns:
        bool: True se o usuário é dono, False caso contrário.
    """
    try:
        list_uuid = uuid.UUID(list_id)
        user_uuid = uuid.UUID(user_id)
        
        shopping_list = db.query(ShoppingList).filter(
            ShoppingList.id == list_uuid,
            ShoppingList.user_id == user_uuid
        ).first()
        
        return shopping_list is not None
    
    except (ValueError, TypeError):
        return False


@lists_bp.route('', methods=['POST'])
@token_required
def create_list(current_user_id: str):
    """
    Cria uma nova lista de compras.
    
    POST /api/lists
    Body: {name, latitude (opcional), longitude (opcional)}
    
    Returns:
        201: Lista criada com sucesso
        400: Erro de validação
        500: Erro interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        db = next(get_db())
        
        try:
            # Criar lista
            shopping_list = ShoppingList(
                user_id=uuid.UUID(current_user_id),
                name=data.get('name'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            
            db.add(shopping_list)
            db.commit()
            db.refresh(shopping_list)
            
            logger.info(f"Lista criada: {shopping_list.id} pelo usuário {current_user_id}")
            
            return jsonify({
                "success": True,
                "message": "Lista criada com sucesso",
                "data": {
                    "list": shopping_list.to_dict()
                }
            }), 201
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar lista: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao criar lista"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao criar lista: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('', methods=['GET'])
@token_required
def get_lists(current_user_id: str):
    """
    Lista todas as listas do usuário.
    
    GET /api/lists
    
    Returns:
        200: Lista de listas do usuário
        500: Erro interno
    """
    try:
        db = next(get_db())
        
        try:
            # Buscar listas do usuário
            shopping_lists = db.query(ShoppingList).filter(
                ShoppingList.user_id == uuid.UUID(current_user_id)
            ).order_by(ShoppingList.created_at.desc()).all()
            
            lists_data = [lst.to_dict(include_items=False) for lst in shopping_lists]
            
            logger.info(f"Listas recuperadas: {len(lists_data)} para usuário {current_user_id}")
            
            return jsonify({
                "success": True,
                "message": "Listas recuperadas com sucesso",
                "data": {
                    "lists": lists_data,
                    "count": len(lists_data)
                }
            }), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar listas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar listas"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar listas: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>', methods=['GET'])
@token_required
def get_list(current_user_id: str, list_id: str):
    """
    Retorna detalhes de uma lista específica.
    
    GET /api/lists/:id
    
    Returns:
        200: Detalhes da lista com itens
        404: Lista não encontrada
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Buscar lista
            shopping_list = db.query(ShoppingList).filter(
                ShoppingList.id == uuid.UUID(list_id)
            ).first()
            
            if not shopping_list:
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada"
                }), 404
            
            logger.info(f"Lista recuperada: {list_id}")
            
            return jsonify({
                "success": True,
                "message": "Lista recuperada com sucesso",
                "data": {
                    "list": shopping_list.to_dict(include_items=True)
                }
            }), 200
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID da lista inválido"
            }), 400
        
        except Exception as e:
            logger.error(f"Erro ao buscar lista: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar lista"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar lista: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>', methods=['PUT'])
@token_required
def update_list(current_user_id: str, list_id: str):
    """
    Atualiza uma lista de compras.
    
    PUT /api/lists/:id
    Body: {name (opcional), latitude (opcional), longitude (opcional)}
    
    Returns:
        200: Lista atualizada
        404: Lista não encontrada
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Buscar lista
            shopping_list = db.query(ShoppingList).filter(
                ShoppingList.id == uuid.UUID(list_id)
            ).first()
            
            if not shopping_list:
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada"
                }), 404
            
            # Atualizar campos
            if 'name' in data:
                shopping_list.name = data['name']
            
            if 'latitude' in data:
                shopping_list.latitude = data['latitude']
            
            if 'longitude' in data:
                shopping_list.longitude = data['longitude']
            
            db.commit()
            db.refresh(shopping_list)
            
            logger.info(f"Lista atualizada: {list_id}")
            
            return jsonify({
                "success": True,
                "message": "Lista atualizada com sucesso",
                "data": {
                    "list": shopping_list.to_dict()
                }
            }), 200
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID da lista inválido"
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar lista: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao atualizar lista"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar lista: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>', methods=['DELETE'])
@token_required
def delete_list(current_user_id: str, list_id: str):
    """
    Deleta uma lista de compras (cascade: deleta itens também).
    
    DELETE /api/lists/:id
    
    Returns:
        200: Lista deletada
        404: Lista não encontrada
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Buscar lista
            shopping_list = db.query(ShoppingList).filter(
                ShoppingList.id == uuid.UUID(list_id)
            ).first()
            
            if not shopping_list:
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada"
                }), 404
            
            # Deletar lista (cascade deleta itens automaticamente)
            db.delete(shopping_list)
            db.commit()
            
            logger.info(f"Lista deletada: {list_id}")
            
            return jsonify({
                "success": True,
                "message": "Lista deletada com sucesso"
            }), 200
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID da lista inválido"
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao deletar lista: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao deletar lista"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao deletar lista: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>/items', methods=['POST'])
@token_required
def add_item(current_user_id: str, list_id: str):
    """
    Adiciona um item à lista.
    
    POST /api/lists/:id/items
    Body: {product_id, quantity}
    
    Returns:
        201: Item adicionado
        400: Erro de validação
        404: Lista ou produto não encontrado
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # Validar
        if not product_id:
            return jsonify({
                "success": False,
                "message": "product_id é obrigatório"
            }), 400
        
        if quantity <= 0:
            return jsonify({
                "success": False,
                "message": "quantity deve ser maior que zero"
            }), 400
        
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Verificar se produto existe
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return jsonify({
                    "success": False,
                    "message": "Produto não encontrado"
                }), 404
            
            # Verificar se lista existe
            shopping_list = db.query(ShoppingList).filter(
                ShoppingList.id == uuid.UUID(list_id)
            ).first()
            
            if not shopping_list:
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada"
                }), 404
            
            # Criar item
            list_item = ListItem(
                list_id=uuid.UUID(list_id),
                product_id=product_id,
                quantity=quantity
            )
            
            db.add(list_item)
            db.commit()
            db.refresh(list_item)
            
            logger.info(f"Item adicionado à lista: {list_id} - produto {product_id}")
            
            return jsonify({
                "success": True,
                "message": "Item adicionado com sucesso",
                "data": {
                    "item": list_item.to_dict(include_product=True)
                }
            }), 201
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID inválido"
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao adicionar item: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao adicionar item"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao adicionar item: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user_id: str, list_id: str, item_id: int):
    """
    Remove um item da lista.
    
    DELETE /api/lists/:id/items/:item_id
    
    Returns:
        200: Item removido
        404: Item ou lista não encontrado
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Buscar item
            list_item = db.query(ListItem).filter(
                ListItem.id == item_id,
                ListItem.list_id == uuid.UUID(list_id)
            ).first()
            
            if not list_item:
                return jsonify({
                    "success": False,
                    "message": "Item não encontrado"
                }), 404
            
            # Deletar item
            db.delete(list_item)
            db.commit()
            
            logger.info(f"Item removido: {item_id} da lista {list_id}")
            
            return jsonify({
                "success": True,
                "message": "Item removido com sucesso"
            }), 200
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID inválido"
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao remover item: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao remover item"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao remover item: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@lists_bp.route('/<string:list_id>/items/<int:item_id>', methods=['PUT'])
@token_required
def update_item(current_user_id: str, list_id: str, item_id: int):
    """
    Atualiza a quantidade de um item.
    
    PUT /api/lists/:id/items/:item_id
    Body: {quantity}
    
    Returns:
        200: Item atualizado
        400: Erro de validação
        404: Item ou lista não encontrado
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não fornecidos"
            }), 400
        
        quantity = data.get('quantity')
        
        if not quantity or quantity <= 0:
            return jsonify({
                "success": False,
                "message": "quantity deve ser maior que zero"
            }), 400
        
        db = next(get_db())
        
        try:
            # Validar ownership
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
            
            # Buscar item
            list_item = db.query(ListItem).filter(
                ListItem.id == item_id,
                ListItem.list_id == uuid.UUID(list_id)
            ).first()
            
            if not list_item:
                return jsonify({
                    "success": False,
                    "message": "Item não encontrado"
                }), 404
            
            # Atualizar quantidade
            list_item.quantity = quantity
            
            db.commit()
            db.refresh(list_item)
            
            logger.info(f"Item atualizado: {item_id} - quantidade {quantity}")
            
            return jsonify({
                "success": True,
                "message": "Item atualizado com sucesso",
                "data": {
                    "item": list_item.to_dict(include_product=True)
                }
            }), 200
        
        except ValueError:
            return jsonify({
                "success": False,
                "message": "ID inválido"
            }), 400
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar item: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao atualizar item"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar item: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500

