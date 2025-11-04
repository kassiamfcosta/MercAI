"""
API de Produtos - Endpoints

Módulo responsável pelos endpoints de busca e detalhes de produtos.
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func, desc
from typing import Optional
import logging

from src.config.database import get_db
from src.models.product import Product
from src.models.offer import Offer
from src.models.store import Store
from src.services.cache import cache

logger = logging.getLogger(__name__)

# Criar blueprint
products_bp = Blueprint('products', __name__)


@products_bp.route('/search', methods=['GET'])
def search_products():
    """
    Busca produtos por nome e categoria.
    
    GET /api/products/search?q=arroz&category=alimentos&page=1&per_page=20
    
    Query Parameters:
        q: Termo de busca (obrigatório, mínimo 3 caracteres).
        category: Categoria para filtrar (opcional).
        page: Número da página (padrão: 1).
        per_page: Itens por página (padrão: 20, máximo: 50).
    
    Returns:
        200: Lista de produtos com paginação
        400: Erro de validação
        500: Erro interno
    """
    try:
        # Obter parâmetros
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(50, max(1, int(request.args.get('per_page', 20))))
        
        # Validar query
        if not query or len(query) < 3:
            return jsonify({
                "success": False,
                "message": "Query deve ter no mínimo 3 caracteres"
            }), 400
        
        # Verificar cache
        cache_key = f"products_search:{query}:{category}:{page}:{per_page}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para busca: {query}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Construir query
            db_query = db.query(Product)
            
            # Filtrar por nome (busca parcial, case-insensitive)
            if query:
                db_query = db_query.filter(
                    Product.name.ilike(f'%{query}%')
                )
            
            # Filtrar por categoria
            if category:
                db_query = db_query.filter(
                    Product.category.ilike(f'%{category}%')
                )
            
            # Contar total
            total = db_query.count()
            
            # Paginar
            offset = (page - 1) * per_page
            products = db_query.order_by(Product.name).offset(offset).limit(per_page).all()
            
            # Calcular total de páginas
            total_pages = (total + per_page - 1) // per_page if total > 0 else 1
            
            # Serializar produtos
            products_data = [product.to_dict(include_offers=False) for product in products]
            
            result = {
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {
                    "products": products_data,
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
            
            logger.info(f"Busca realizada: '{query}' - {total} resultados")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar produtos: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar produtos"
            }), 500
        
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Parâmetro inválido: {e}"
        }), 400
    
    except Exception as e:
        logger.error(f"Erro inesperado na busca de produtos: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """
    Retorna detalhes de um produto específico.
    
    GET /api/products/:id
    
    Returns:
        200: Detalhes do produto com ofertas atuais
        404: Produto não encontrado
        500: Erro interno
    """
    try:
        # Verificar cache
        cache_key = f"product:{product_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para produto: {product_id}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar produto
            product = db.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return jsonify({
                    "success": False,
                    "message": "Produto não encontrado"
                }), 404
            
            # Buscar ofertas atuais (apenas em estoque)
            offers = db.query(Offer).filter(
                Offer.product_id == product_id,
                Offer.in_stock == True
            ).order_by(Offer.price).all()
            
            # Serializar produto com ofertas
            product_data = product.to_dict(include_offers=False)
            product_data['offers'] = [offer.to_dict(include_store=True) for offer in offers]
            product_data['offers_count'] = len(offers)
            
            result = {
                "success": True,
                "message": "Produto encontrado",
                "data": {
                    "product": product_data
                }
            }
            
            # Cachear resultado (30 minutos)
            cache.set(cache_key, result, ttl=1800)
            
            logger.info(f"Produto recuperado: {product_id}")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar produto: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar produto"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar produto: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@products_bp.route('/<int:product_id>/offers', methods=['GET'])
def get_product_offers(product_id: int):
    """
    Retorna todas as ofertas de um produto.
    
    GET /api/products/:id/offers
    
    Query Parameters:
        sort: Ordenação (price_asc, price_desc, score) - padrão: price_asc
        in_stock_only: Filtrar apenas em estoque (padrão: true)
    
    Returns:
        200: Lista de ofertas ordenadas
        404: Produto não encontrado
        500: Erro interno
    """
    try:
        # Obter parâmetros
        sort = request.args.get('sort', 'price_asc')
        in_stock_only = request.args.get('in_stock_only', 'true').lower() == 'true'
        
        # Verificar cache
        cache_key = f"product_offers:{product_id}:{sort}:{in_stock_only}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para ofertas do produto: {product_id}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Verificar se produto existe
            product = db.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return jsonify({
                    "success": False,
                    "message": "Produto não encontrado"
                }), 404
            
            # Construir query de ofertas
            offers_query = db.query(Offer).filter(Offer.product_id == product_id)
            
            # Filtrar por estoque
            if in_stock_only:
                offers_query = offers_query.filter(Offer.in_stock == True)
            
            # Ordenar
            if sort == 'price_asc':
                offers_query = offers_query.order_by(Offer.price.asc())
            elif sort == 'price_desc':
                offers_query = offers_query.order_by(Offer.price.desc())
            elif sort == 'score':
                # Ordenar por desconto (score simplificado)
                offers_query = offers_query.order_by(
                    Offer.discount_percentage.desc().nullslast(),
                    Offer.price.asc()
                )
            
            offers = offers_query.all()
            
            # Serializar ofertas com dados da loja
            offers_data = [offer.to_dict(include_store=True, include_product=False) for offer in offers]
            
            result = {
                "success": True,
                "message": "Ofertas encontradas",
                "data": {
                    "product": product.to_dict(include_offers=False),
                    "offers": offers_data,
                    "count": len(offers_data)
                }
            }
            
            # Cachear resultado (30 minutos)
            cache.set(cache_key, result, ttl=1800)
            
            logger.info(f"Ofertas recuperadas: {product_id} - {len(offers)} ofertas")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar ofertas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar ofertas"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar ofertas: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Retorna lista de todas as categorias disponíveis.
    
    GET /api/products/categories
    
    Returns:
        200: Lista de categorias com contagem de produtos
        500: Erro interno
    """
    try:
        # Verificar cache
        cache_key = 'products_categories'
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug("Cache hit para categorias")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar categorias com contagem de produtos
            categories_query = db.query(
                Product.category,
                func.count(Product.id).label('count')
            ).filter(
                Product.category.isnot(None),
                Product.category != ''
            ).group_by(Product.category).order_by(Product.category).all()
            
            categories = [
                {
                    'name': cat[0],
                    'count': cat[1]
                }
                for cat in categories_query
            ]
            
            result = {
                "success": True,
                "message": "Categorias recuperadas com sucesso",
                "data": {
                    "categories": categories,
                    "count": len(categories)
                }
            }
            
            # Cachear resultado (1 hora)
            cache.set(cache_key, result, ttl=3600)
            
            logger.info(f"Categorias recuperadas: {len(categories)}")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar categorias: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar categorias"
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar categorias: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500


@products_bp.route('/popular', methods=['GET'])
def get_popular_products():
    """
    Retorna produtos mais buscados/populares.
    
    GET /api/products/popular?limit=10
    
    Query Parameters:
        limit: Número de produtos a retornar (padrão: 10, máximo: 50)
    
    Returns:
        200: Lista de produtos populares
        500: Erro interno
    """
    try:
        # Obter parâmetros
        limit = min(50, max(1, int(request.args.get('limit', 10))))
        
        # Verificar cache
        cache_key = f'products_popular:{limit}'
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para produtos populares: {limit}")
            return jsonify(cached_result), 200
        
        # Obter sessão do banco
        db = next(get_db())
        
        try:
            # Buscar produtos com mais ofertas (produtos mais "populares")
            # A lógica pode ser melhorada adicionando um contador de buscas no futuro
            popular_query = db.query(
                Product,
                func.count(Offer.id).label('offers_count')
            ).join(
                Offer, Product.id == Offer.product_id
            ).filter(
                Offer.in_stock == True
            ).group_by(
                Product.id
            ).order_by(
                desc('offers_count'),
                Product.name
            ).limit(limit).all()
            
            products = [prod[0] for prod in popular_query]
            products_data = [product.to_dict(include_offers=False) for product in products]
            
            # Adicionar contagem de ofertas
            for i, prod in enumerate(popular_query):
                products_data[i]['offers_count'] = prod[1]
            
            result = {
                "success": True,
                "message": "Produtos populares recuperados com sucesso",
                "data": {
                    "products": products_data,
                    "count": len(products_data)
                }
            }
            
            # Cachear resultado (30 minutos)
            cache.set(cache_key, result, ttl=1800)
            
            logger.info(f"Produtos populares recuperados: {len(products_data)}")
            
            return jsonify(result), 200
        
        except Exception as e:
            logger.error(f"Erro ao buscar produtos populares: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno ao buscar produtos populares"
            }), 500
        
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Parâmetro inválido: {e}"
        }), 400
    
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar produtos populares: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Erro ao processar requisição"
        }), 500

