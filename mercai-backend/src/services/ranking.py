"""
Ranking Service - Algoritmo de Ranking

Módulo responsável por calcular scores e gerar rankings de ofertas.
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
import logging
import uuid

from src.config.database import get_db
from src.models.shopping_list import ShoppingList
from src.models.list_item import ListItem
from src.models.offer import Offer
from src.models.product import Product
from src.models.store import Store
from src.services.cache import cache
from src.services.geo import calculate_distance, calculate_proximity_score

logger = logging.getLogger(__name__)


def calculate_offer_score(
    offer: Dict[str, Any],
    user_location: Optional[Dict[str, float]] = None,
    max_price: Optional[float] = None
) -> float:
    """
    Calcula score de uma oferta (0-100).
    
    Pesos:
    - Preço: 40%
    - Desconto: 30%
    - Disponibilidade: 20%
    - Proximidade: 10% (se user_location fornecida)
    
    Args:
        offer: Dicionário com dados da oferta (price, original_price, discount_percentage, in_stock, store).
        user_location: Dicionário com 'lat' e 'lon' do usuário (opcional).
        max_price: Preço máximo para normalização (opcional, calculado automaticamente se não fornecido).
    
    Returns:
        float: Score de 0 a 100.
    """
    try:
        score = 0.0
        
        # Extrair dados da oferta
        price = float(offer.get('price', 0))
        original_price = offer.get('original_price')
        discount_percentage = offer.get('discount_percentage')
        in_stock = offer.get('in_stock', True)
        store = offer.get('store', {})
        
        # Validar preço
        if price <= 0:
            return 0.0
        
        # 1. Score de Preço (40 pontos)
        # Normalizar preço: menor preço = maior score
        if max_price and max_price > 0:
            price_score = (1 - (price / max_price)) * 40
        else:
            # Se não há max_price, usar uma normalização relativa
            # Assumir que preço muito alto (1000+) recebe 0, preço baixo recebe 40
            normalized_price = min(price / 100.0, 1.0)  # Normalizar até 100 reais
            price_score = (1 - normalized_price) * 40
        
        score += price_score
        
        # 2. Score de Desconto (30 pontos)
        if discount_percentage:
            discount = float(discount_percentage)
            # Limitar desconto a 50% (descontos maiores recebem 30 pontos)
            discount_score = min((discount / 50.0), 1.0) * 30
            score += discount_score
        elif original_price and original_price > price:
            # Calcular desconto se não fornecido
            discount = ((float(original_price) - price) / float(original_price)) * 100
            discount_score = min((discount / 50.0), 1.0) * 30
            score += discount_score
        
        # 3. Score de Disponibilidade (20 pontos)
        if in_stock:
            score += 20
        
        # 4. Score de Proximidade (10 pontos)
        if user_location:
            store_lat = store.get('latitude')
            store_lon = store.get('longitude')
            
            if store_lat and store_lon:
                try:
                    distance = calculate_distance(
                        user_location['lat'],
                        user_location['lon'],
                        float(store_lat),
                        float(store_lon)
                    )
                    proximity_score = calculate_proximity_score(distance)
                    score += proximity_score
                except Exception as e:
                    logger.warning(f"Erro ao calcular proximidade: {e}")
        
        return round(min(score, 100.0), 2)
    
    except Exception as e:
        logger.error(f"Erro ao calcular score da oferta: {e}", exc_info=True)
        return 0.0


def generate_ranking(
    shopping_list_id: str,
    user_location: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Gera ranking completo de ofertas para uma lista de compras.
    
    Args:
        shopping_list_id: UUID da lista de compras.
        user_location: Dicionário com 'lat' e 'lon' do usuário (opcional).
    
    Returns:
        Dict[str, Any]: Ranking completo com melhores ofertas por produto.
    """
    try:
        # Verificar cache
        cache_key = f"ranking:{shopping_list_id}"
        if user_location:
            cache_key += f":{user_location.get('lat', '')}:{user_location.get('lon', '')}"
        
        cached_ranking = cache.get(cache_key)
        if cached_ranking:
            logger.info(f"Ranking cacheado encontrado para lista: {shopping_list_id}")
            return cached_ranking
        
        logger.info(f"Gerando ranking para lista: {shopping_list_id}")
        
        db = next(get_db())
        
        try:
            # Buscar lista
            shopping_list = db.query(ShoppingList).filter(
                ShoppingList.id == uuid.UUID(shopping_list_id)
            ).first()
            
            if not shopping_list:
                logger.warning(f"Lista não encontrada: {shopping_list_id}")
                return {
                    "list_id": shopping_list_id,
                    "items": [],
                    "error": "Lista não encontrada"
                }
            
            # Buscar itens da lista
            items = db.query(ListItem).filter(
                ListItem.list_id == shopping_list.id
            ).all()
            
            if not items:
                logger.info(f"Lista vazia: {shopping_list_id}")
                return {
                    "list_id": shopping_list_id,
                    "items": [],
                    "message": "Lista vazia"
                }
            
            ranking_items = []
            
            # Para cada item da lista
            for item in items:
                if not item.product:
                    continue
                
                product_id = item.product_id
                quantity = item.quantity
                
                # Buscar ofertas do produto
                offers = db.query(Offer).filter(
                    Offer.product_id == product_id,
                    Offer.in_stock == True
                ).all()
                
                if not offers:
                    # Sem ofertas disponíveis
                    ranking_items.append({
                        "product": item.product.to_dict(),
                        "quantity": quantity,
                        "best_offer": None,
                        "all_offers": []
                    })
                    continue
                
                # Calcular max_price para normalização
                max_price = max(float(offer.price) for offer in offers)
                
                # Calcular score de cada oferta
                scored_offers = []
                for offer in offers:
                    offer_dict = offer.to_dict(include_store=True)
                    score = calculate_offer_score(
                        offer_dict,
                        user_location,
                        max_price
                    )
                    offer_dict['score'] = score
                    scored_offers.append(offer_dict)
                
                # Ordenar por score (maior primeiro)
                scored_offers.sort(key=lambda x: x['score'], reverse=True)
                
                # Melhor oferta
                best_offer = scored_offers[0] if scored_offers else None
                
                ranking_items.append({
                    "product": item.product.to_dict(),
                    "quantity": quantity,
                    "best_offer": best_offer,
                    "all_offers": scored_offers[:5]  # Top 5 ofertas
                })
            
            # Otimizar combinação de lojas
            best_combination = optimize_store_combination(ranking_items)
            
            ranking = {
                "list_id": str(shopping_list_id),
                "items": ranking_items,
                "best_combination": best_combination
            }
            
            # Cachear ranking (1 hora)
            cache.set(cache_key, ranking, ttl=3600)
            
            logger.info(f"Ranking gerado com sucesso: {len(ranking_items)} itens processados")
            
            return ranking
        
        except Exception as e:
            logger.error(f"Erro ao gerar ranking: {e}", exc_info=True)
            return {
                "list_id": shopping_list_id,
                "items": [],
                "error": str(e)
            }
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro ao gerar ranking: {e}", exc_info=True)
        return {
            "list_id": shopping_list_id,
            "items": [],
            "error": str(e)
        }


def optimize_store_combination(ranking_items: List[Dict]) -> Dict[str, Any]:
    """
    Encontra a melhor combinação de lojas para minimizar custo total.
    
    Args:
        ranking_items: Lista de itens do ranking com melhores ofertas.
    
    Returns:
        Dict[str, Any]: Recomendação de melhor combinação de lojas.
    """
    try:
        if not ranking_items:
            return {
                "recommended_store": None,
                "estimated_total": 0.0,
                "total_savings": 0.0,
                "alternatives": []
            }
        
        # Agrupar por loja
        store_totals = {}
        
        for item in ranking_items:
            best_offer = item.get('best_offer')
            if not best_offer:
                continue
            
            store = best_offer.get('store', {})
            store_id = store.get('id')
            store_name = store.get('name', 'Loja Desconhecida')
            
            if not store_id:
                continue
            
            price = float(best_offer.get('price', 0))
            quantity = item.get('quantity', 1)
            item_total = price * quantity
            
            if store_id not in store_totals:
                store_totals[store_id] = {
                    "store": store,
                    "total": 0.0,
                    "items_count": 0,
                    "savings": 0.0
                }
            
            store_totals[store_id]['total'] += item_total
            store_totals[store_id]['items_count'] += 1
            
            # Calcular economia (se houver preço original)
            original_price = best_offer.get('original_price')
            if original_price and original_price > price:
                savings = (float(original_price) - price) * quantity
                store_totals[store_id]['savings'] += savings
        
        # Ordenar por total (menor preço primeiro)
        sorted_stores = sorted(
            store_totals.values(),
            key=lambda x: x['total']
        )
        
        if not sorted_stores:
            return {
                "recommended_store": None,
                "estimated_total": 0.0,
                "total_savings": 0.0,
                "alternatives": []
            }
        
        # Melhor loja (primeira da lista)
        best_store = sorted_stores[0]
        
        # Alternativas (próximas 3)
        alternatives = []
        for store_data in sorted_stores[1:4]:
            alternatives.append({
                "store": store_data['store'],
                "estimated_total": round(store_data['total'], 2),
                "items_count": store_data['items_count'],
                "savings": round(store_data['savings'], 2)
            })
        
        return {
            "recommended_store": best_store['store'].get('name'),
            "store_id": best_store['store'].get('id'),
            "estimated_total": round(best_store['total'], 2),
            "total_savings": round(best_store['savings'], 2),
            "items_count": best_store['items_count'],
            "alternatives": alternatives
        }
    
    except Exception as e:
        logger.error(f"Erro ao otimizar combinação de lojas: {e}", exc_info=True)
        return {
            "recommended_store": None,
            "estimated_total": 0.0,
            "total_savings": 0.0,
            "alternatives": []
        }

