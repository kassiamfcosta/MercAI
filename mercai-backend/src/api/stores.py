"""
API de Lojas - Endpoints

Módulo responsável pelos endpoints de listagem e detalhes de lojas.
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func, or_
from decimal import Decimal
from typing import Optional
import logging
import math

from src.config.database import get_db
from src.models.store import Store
from src.models.offer import Offer
from src.services.cache import cache

logger = logging.getLogger(__name__)

# Criar blueprint
stores_bp = Blueprint('stores', __name__)


def calculate_distance(lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal) -> float:
    """
    Calcula distância em km entre dois pontos usando fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas do primeiro ponto
        lat2, lon2: Coordenadas do segundo ponto
    
    Returns:
        float: Distância em quilômetros
    """
    # Raio da Terra em km
    R = 6371.0
    
    # Converter para float
    lat1, lon1 = float(lat1), float(lon1)
    lat2, lon2 = float(lat2), float(lon2)
    
    # Converter para radianos
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance


@stores_bp.route('', methods=['GET'])
def get_stores():
    """
    Lista todas as lojas.
    
    GET /api/stores
    
    Query Parameters:
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 20, máximo: 50)
    
    Returns:
        200: Lista de lojas com paginação
        500: Erro interno
    """
    try:
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(50, max(1, int(request.args.get('per_page', 20))))
        
        # Verificar cache
        cache_key = f'stores_list:{page}:{per_page}'
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para lista de lojas: {page}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Contar total
            total = db.query(Store).count()
            
            # Paginar
            offset = (page - 1) * per_page
            stores = db.query(Store).order_by(Store.name).offset(offset).limit(per_page).all()
            
            # Calcular total de páginas
            total_pages = (total + per_page - 1) // per_page if total > 0 else 1
            
            # Serializar lojas
            stores_data = [store.to_dict(include_offers=False) for store in stores]
            
            result = {
                "success": True,
                "message": "Lojas recuperadas com sucesso",
                "data": {
                    "stores": stores_data,
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": total,
                        "pages": total_pages
                    }
                }
            }
            
            # Cachear resultado (1 hora)
            cache.set(cache_key, result, ttl=3600)
            
            logger.info(f"Lojas recuperadas: {total}")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar lojas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar lojas"
            }), 500
        
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Parâmetro inválido: {e}"
        }), 400
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar lojas: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@stores_bp.route('/<int:store_id>', methods=['GET'])
def get_store(store_id: int):
    """
    Retorna detalhes de uma loja específica.
    
    GET /api/stores/:id
    
    Returns:
        200: Detalhes da loja com ofertas atuais
        404: Loja não encontrada
        500: Erro interno
    """
    try:
        # Verificar cache
        cache_key = f'store:{store_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para loja: {store_id}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar loja
            store = db.query(Store).filter(Store.id == store_id).first()
            
            if not store:
                return jsonify({
                    "success": False,
                    "message": "Loja não encontrada"
                }), 404
            
            # Buscar ofertas atuais (apenas em estoque)
            offers_count = db.query(Offer).filter(
                Offer.store_id == store_id,
                Offer.in_stock == True
            ).count()
            
            # Serializar loja
            store_data = store.to_dict(include_offers=False)
            store_data['offers_count'] = offers_count
            
            result = {
                "success": True,
                "message": "Loja encontrada",
                "data": {
                    "store": store_data
                }
            }
            
            # Cachear resultado (30 minutos)
            cache.set(cache_key, result, ttl=1800)
            
            logger.info(f"Loja recuperada: {store_id}")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar loja: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar loja"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar loja: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@stores_bp.route('/nearby', methods=['GET'])
def get_nearby_stores():
    """
    Retorna lojas próximas a uma localização.
    
    GET /api/stores/nearby?lat=-15.8229&lon=-48.0844&radius=5&limit=10
    
    Query Parameters:
        lat: Latitude (obrigatório)
        lon: Longitude (obrigatório)
        radius: Raio de busca em km (padrão: 5, máximo: 50)
        limit: Número máximo de resultados (padrão: 10, máximo: 50)
    
    Returns:
        200: Lista de lojas próximas ordenadas por distância
        400: Parâmetros inválidos
        500: Erro interno
    """
    try:
        # Obter parâmetros
        lat_str = request.args.get('lat', '').strip()
        lon_str = request.args.get('lon', '').strip()
        radius = min(50, max(1, float(request.args.get('radius', 5))))
        limit = min(50, max(1, int(request.args.get('limit', 10))))
        
        # Validar coordenadas
        if not lat_str or not lon_str:
            return jsonify({
                "success": False,
                "message": "Latitude e longitude são obrigatórios"
            }), 400
        
        try:
            lat = Decimal(lat_str)
            lon = Decimal(lon_str)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Coordenadas inválidas"
            }), 400
        
        # Validar range de coordenadas
        if not (-90 <= float(lat) <= 90) or not (-180 <= float(lon) <= 180):
            return jsonify({
                "success": False,
                "message": "Coordenadas fora do range válido"
            }), 400
        
        # Verificar cache
        cache_key = f'stores_nearby:{lat}:{lon}:{radius}:{limit}'
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para lojas próximas: {lat}, {lon}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar todas as lojas com coordenadas
            stores = db.query(Store).filter(
                Store.latitude.isnot(None),
                Store.longitude.isnot(None)
            ).all()
            
            # Calcular distâncias e filtrar
            nearby_stores = []
            for store in stores:
                distance = calculate_distance(lat, lon, store.latitude, store.longitude)
                
                if distance <= radius:
                    store_dict = store.to_dict(include_offers=False)
                    store_dict['distance'] = round(distance, 2)
                    nearby_stores.append((store, distance))
            
            # Ordenar por distância
            nearby_stores.sort(key=lambda x: x[1])
            
            # Limitar resultados
            nearby_stores = nearby_stores[:limit]
            
            # Serializar
            stores_data = []
            for store, distance in nearby_stores:
                store_dict = store.to_dict(include_offers=False)
                store_dict['distance'] = round(distance, 2)
                stores_data.append(store_dict)
            
            result = {
                "success": True,
                "message": "Lojas próximas recuperadas com sucesso",
                "data": {
                    "stores": stores_data,
                    "count": len(stores_data),
                    "location": {
                        "latitude": float(lat),
                        "longitude": float(lon)
                    },
                    "radius": radius
                }
            }
            
            # Cachear resultado (10 minutos - dados de localização mudam)
            cache.set(cache_key, result, ttl=600)
            
            logger.info(f"Lojas próximas encontradas: {len(stores_data)} para ({lat}, {lon})")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar lojas próximas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar lojas próximas"
            }), 500
        
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Parâmetro inválido: {e}"
        }), 400
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar lojas próximas: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500
