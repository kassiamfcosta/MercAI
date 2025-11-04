"""
Geo Service - Geolocalização

Módulo responsável por geocoding e cálculos de distância.
"""

import time
import requests
from typing import Optional, Dict, List, Tuple
from math import radians, cos, sin, asin, sqrt
import logging

from src.config.settings import Settings
from src.services.cache import cache

logger = logging.getLogger(__name__)
settings = Settings()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre dois pontos usando fórmula de Haversine.
    
    Args:
        lat1: Latitude do primeiro ponto.
        lon1: Longitude do primeiro ponto.
        lat2: Latitude do segundo ponto.
        lon2: Longitude do segundo ponto.
    
    Returns:
        float: Distância em quilômetros (precisão de 2 casas decimais).
    """
    try:
        # Converter graus para radianos
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Diferença de longitude e latitude
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        # Fórmula de Haversine
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Raio da Terra em km
        km = 6371 * c
        
        return round(km, 2)
    
    except Exception as e:
        logger.error(f"Erro ao calcular distância: {e}", exc_info=True)
        return 0.0


def geocode_address(address: str) -> Optional[Dict[str, float]]:
    """
    Converte um endereço em coordenadas (lat, lon) usando Nominatim (OpenStreetMap).
    
    Args:
        address: Endereço a ser geocodificado.
    
    Returns:
        Optional[Dict[str, float]]: Dicionário com 'lat' e 'lon' ou None se falhar.
    """
    if not address:
        return None
    
    # Verificar cache primeiro
    cache_key = f"geocode:{address}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.debug(f"Geocoding cache hit para: {address}")
        return cached_result
    
    try:
        # Nominatim API
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
            'countrycodes': 'br'  # Restringir ao Brasil
        }
        
        headers = {
            'User-Agent': settings.USER_AGENT
        }
        
        logger.info(f"Geocodificando endereço: {address}")
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            coordinates = {
                'lat': float(result['lat']),
                'lon': float(result['lon'])
            }
            
            # Cachear resultado (24 horas)
            cache.set(cache_key, coordinates, ttl=86400)
            
            logger.info(f"Endereço geocodificado: {address} -> lat={coordinates['lat']}, lon={coordinates['lon']}")
            
            return coordinates
        else:
            logger.warning(f"Endereço não encontrado: {address}")
            return None
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao geocodificar endereço '{address}': {e}")
        return None
    
    except Exception as e:
        logger.error(f"Erro ao processar geocoding: {e}", exc_info=True)
        return None
    
    finally:
        # Rate limiting: Nominatim permite 1 req/segundo
        time.sleep(1)


def find_nearest_stores(
    user_location: Dict[str, float],
    stores: List[Dict],
    max_distance: float = 20.0
) -> List[Dict]:
    """
    Encontra lojas dentro de um raio máximo e ordena por distância.
    
    Args:
        user_location: Dicionário com 'lat' e 'lon' do usuário.
        stores: Lista de lojas (cada loja deve ter 'latitude' e 'longitude').
        max_distance: Distância máxima em km (padrão: 20km).
    
    Returns:
        List[Dict]: Lista de lojas dentro do raio, ordenadas por distância.
    """
    try:
        if not user_location or 'lat' not in user_location or 'lon' not in user_location:
            logger.warning("Localização do usuário inválida")
            return []
        
        user_lat = user_location['lat']
        user_lon = user_location['lon']
        
        nearby_stores = []
        
        for store in stores:
            # Verificar se loja tem coordenadas
            store_lat = store.get('latitude')
            store_lon = store.get('longitude')
            
            if store_lat is None or store_lon is None:
                continue
            
            # Converter para float se necessário
            try:
                store_lat = float(store_lat)
                store_lon = float(store_lon)
            except (ValueError, TypeError):
                continue
            
            # Calcular distância
            distance = calculate_distance(user_lat, user_lon, store_lat, store_lon)
            
            # Filtrar por distância máxima
            if distance <= max_distance:
                store_with_distance = store.copy()
                store_with_distance['distance_km'] = distance
                nearby_stores.append(store_with_distance)
        
        # Ordenar por distância
        nearby_stores.sort(key=lambda x: x['distance_km'])
        
        logger.info(f"Encontradas {len(nearby_stores)} lojas dentro de {max_distance}km")
        
        return nearby_stores
    
    except Exception as e:
        logger.error(f"Erro ao buscar lojas próximas: {e}", exc_info=True)
        return []


def calculate_proximity_score(distance_km: float, max_distance: float = 20.0) -> float:
    """
    Calcula score de proximidade baseado na distância.
    
    Args:
        distance_km: Distância em km.
        max_distance: Distância máxima para score completo (padrão: 20km).
    
    Returns:
        float: Score de 0 a 10 (10 para distância 0, 0 para distância >= max_distance).
    """
    try:
        if distance_km < 0:
            return 0.0
        
        if distance_km >= max_distance:
            return 0.0
        
        # Score linear: 10 pontos para distância 0, 0 pontos para max_distance
        score = max(0, 10 - (distance_km / max_distance) * 10)
        
        return round(score, 2)
    
    except Exception as e:
        logger.error(f"Erro ao calcular score de proximidade: {e}", exc_info=True)
        return 0.0

