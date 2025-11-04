"""
API de Ranking - Endpoints

Módulo responsável pelos endpoints de geração de ranking de ofertas.
"""

from flask import Blueprint, request, jsonify
from typing import Optional, Dict
import logging

from src.services.ranking import generate_ranking
from src.utils.jwt import token_required
from src.config.database import get_db
from src.models.shopping_list import ShoppingList

logger = logging.getLogger(__name__)

# Criar blueprint
ranking_bp = Blueprint('ranking', __name__)


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
        import uuid
        list_uuid = uuid.UUID(list_id)
        user_uuid = uuid.UUID(user_id)
        
        shopping_list = db.query(ShoppingList).filter(
            ShoppingList.id == list_uuid,
            ShoppingList.user_id == user_uuid
        ).first()
        
        return shopping_list is not None
    
    except (ValueError, TypeError):
        return False


@ranking_bp.route('', methods=['GET'])
@token_required
def get_ranking(current_user_id: str):
    """
    Gera ranking básico para uma lista de compras.
    
    GET /api/ranking?list_id=xxx&latitude=xxx&longitude=xxx
    
    Query Parameters:
        list_id: UUID da lista (obrigatório).
        latitude: Latitude do usuário (opcional).
        longitude: Longitude do usuário (opcional).
    
    Returns:
        200: Ranking básico com melhores ofertas por produto
        400: Erro de validação
        404: Lista não encontrada
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        list_id = request.args.get('list_id')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        
        # Validar list_id
        if not list_id:
            return jsonify({
                "success": False,
                "message": "list_id é obrigatório"
            }), 400
        
        # Validar ownership
        db = next(get_db())
        
        try:
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
        
        finally:
            db.close()
        
        # Preparar localização do usuário (se fornecida)
        user_location = None
        if latitude and longitude:
            try:
                user_location = {
                    'lat': float(latitude),
                    'lon': float(longitude)
                }
            except ValueError:
                logger.warning(f"Coordenadas inválidas: lat={latitude}, lon={longitude}")
                user_location = None
        
        # Gerar ranking
        ranking = generate_ranking(list_id, user_location)
        
        if 'error' in ranking:
            logger.error(f"Erro ao gerar ranking: {ranking.get('error')}")
            return jsonify({
                "success": False,
                "message": ranking.get('error', "Erro ao gerar ranking")
            }), 500
        
        logger.info(f"Ranking gerado para lista: {list_id}")
        
        return jsonify({
            "success": True,
            "message": "Ranking gerado com sucesso",
            "data": ranking
        }), 200
    
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar ranking: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@ranking_bp.route('/<string:list_id>/detailed', methods=['GET'])
@token_required
def get_detailed_ranking(current_user_id: str, list_id: str):
    """
    Gera ranking detalhado para uma lista de compras.
    
    GET /api/ranking/:list_id/detailed?latitude=xxx&longitude=xxx
    
    Query Parameters:
        latitude: Latitude do usuário (opcional).
        longitude: Longitude do usuário (opcional).
    
    Returns:
        200: Ranking detalhado com todas as ofertas (top 5) por produto e economia total
        404: Lista não encontrada
        403: Usuário não tem permissão
        500: Erro interno
    """
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        
        # Validar ownership
        db = next(get_db())
        
        try:
            if not _validate_list_ownership(db, list_id, current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Lista não encontrada ou sem permissão"
                }), 404
        
        finally:
            db.close()
        
        # Preparar localização do usuário (se fornecida)
        user_location = None
        if latitude and longitude:
            try:
                user_location = {
                    'lat': float(latitude),
                    'lon': float(longitude)
                }
            except ValueError:
                logger.warning(f"Coordenadas inválidas: lat={latitude}, lon={longitude}")
                user_location = None
        
        # Gerar ranking
        ranking = generate_ranking(list_id, user_location)
        
        if 'error' in ranking:
            logger.error(f"Erro ao gerar ranking detalhado: {ranking.get('error')}")
            return jsonify({
                "success": False,
                "message": ranking.get('error', "Erro ao gerar ranking")
            }), 500
        
        # Calcular economia total
        total_savings = 0.0
        estimated_total = 0.0
        
        for item in ranking.get('items', []):
            best_offer = item.get('best_offer')
            if best_offer:
                price = float(best_offer.get('price', 0))
                quantity = item.get('quantity', 1)
                estimated_total += price * quantity
                
                # Calcular economia (se houver preço original)
                original_price = best_offer.get('original_price')
                if original_price and original_price > price:
                    savings = (float(original_price) - price) * quantity
                    total_savings += savings
        
        # Adicionar informações de economia ao ranking
        ranking['summary'] = {
            'estimated_total': round(estimated_total, 2),
            'total_savings': round(total_savings, 2),
            'items_count': len(ranking.get('items', []))
        }
        
        logger.info(f"Ranking detalhado gerado para lista: {list_id}")
        
        return jsonify({
            "success": True,
            "message": "Ranking detalhado gerado com sucesso",
            "data": ranking
        }), 200
    
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar ranking detalhado: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500

