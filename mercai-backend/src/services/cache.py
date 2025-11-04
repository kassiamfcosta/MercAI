"""
Cache Service - Redis Wrapper

Módulo responsável por gerenciar cache usando Redis com padrão Singleton.
"""

import json
import hashlib
from typing import Optional, Any, Callable, Dict
from functools import wraps
import redis
import logging

from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


class CacheService:
    """
    Serviço de cache usando Redis com padrão Singleton.
    
    Singleton Pattern: Garante apenas uma instância de conexão Redis.
    """
    
    _instance: Optional['CacheService'] = None
    _client: Optional[redis.Redis] = None
    
    def __new__(cls):
        """
        Implementa padrão Singleton.
        
        Returns:
            CacheService: Instância única do serviço.
        """
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """
        Inicializa a conexão com Redis.
        """
        if self._initialized:
            return
        
        try:
            # Conectar ao Redis
            if settings.REDIS_URL:
                self._client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
                # Testar conexão
                self._client.ping()
                logger.info("Conexão com Redis estabelecida com sucesso")
            else:
                logger.warning("REDIS_URL não configurado. Cache desabilitado.")
                self._client = None
        except Exception as e:
            logger.error(f"Erro ao conectar ao Redis: {e}")
            self._client = None
        
        self._initialized = True
    
    def get(self, key: str) -> Optional[Any]:
        """
        Busca um valor no cache.
        
        Args:
            key: Chave do cache.
        
        Returns:
            Optional[Any]: Valor deserializado ou None se não existir.
        """
        if not self._client:
            return None
        
        try:
            value = self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao deserializar valor do cache (key={key}): {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar do cache (key={key}): {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Salva um valor no cache.
        
        Args:
            key: Chave do cache.
            value: Valor a ser serializado.
            ttl: Tempo de vida em segundos (padrão: 1 hora).
        
        Returns:
            bool: True se salvo com sucesso, False caso contrário.
        """
        if not self._client:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            result = self._client.setex(key, ttl, serialized)
            return result is True
        except (TypeError, ValueError) as e:
            logger.error(f"Erro ao serializar valor para cache (key={key}): {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao salvar no cache (key={key}): {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Remove uma chave do cache.
        
        Args:
            key: Chave a ser removida.
        
        Returns:
            bool: True se removido com sucesso, False caso contrário.
        """
        if not self._client:
            return False
        
        try:
            result = self._client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Erro ao deletar do cache (key={key}): {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Verifica se uma chave existe no cache.
        
        Args:
            key: Chave a ser verificada.
        
        Returns:
            bool: True se existe, False caso contrário.
        """
        if not self._client:
            return False
        
        try:
            return self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar existência no cache (key={key}): {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalida múltiplas chaves usando padrão.
        
        Args:
            pattern: Padrão de chaves (ex: "ranking:*", "product:*").
        
        Returns:
            int: Número de chaves removidas.
        """
        if not self._client:
            return 0
        
        try:
            keys = self._client.keys(pattern)
            if keys:
                return self._client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Erro ao invalidar padrão do cache (pattern={pattern}): {e}")
            return 0
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Gera chave de cache única baseada em argumentos.
        
        Args:
            prefix: Prefixo da chave.
            *args: Argumentos posicionais.
            **kwargs: Argumentos nomeados.
        
        Returns:
            str: Chave de cache gerada.
        """
        # Combinar argumentos em string
        key_parts = [prefix]
        
        if args:
            key_parts.extend(str(arg) for arg in args)
        
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            key_parts.extend(f"{k}:{v}" for k, v in sorted_kwargs)
        
        key_string = ":".join(key_parts)
        
        # Gerar hash para chaves muito longas
        if len(key_string) > 200:
            key_hash = hashlib.md5(key_string.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash}"
        
        return key_string


# Instância global do cache
cache = CacheService()


def cached(ttl: int = 3600, key_prefix: str = "") -> Callable:
    """
    Decorator para cachear resultados de funções.
    
    Args:
        ttl: Tempo de vida do cache em segundos.
        key_prefix: Prefixo para as chaves do cache.
    
    Returns:
        Callable: Decorator function.
    
    Example:
        ```python
        @cached(ttl=3600, key_prefix="product")
        def get_product(product_id: int):
            # Função será cacheada
            return product
        ```
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gerar chave de cache
            prefix = key_prefix or func.__name__
            cache_key = cache._generate_key(prefix, *args, **kwargs)
            
            # Tentar buscar do cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_value
            
            # Executar função e cachear resultado
            logger.debug(f"Cache miss: {cache_key}")
            result = func(*args, **kwargs)
            
            # Cachear resultado se não for None
            if result is not None:
                cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator

