"""
Models - Entidades de Dados

Módulo contendo os modelos SQLAlchemy que representam as entidades do sistema.
"""

from src.models.user import User
from src.models.store import Store
from src.models.product import Product
from src.models.offer import Offer
from src.models.shopping_list import ShoppingList
from src.models.list_item import ListItem

__all__ = [
    'User',
    'Store',
    'Product',
    'Offer',
    'ShoppingList',
    'ListItem',
]
