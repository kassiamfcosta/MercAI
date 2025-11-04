"""
Model ShoppingList - Entidade de Lista de Compras

Model SQLAlchemy para representar listas de compras dos usuários.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from decimal import Decimal
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey
from src.utils.uuid_type import GUID
from sqlalchemy.orm import relationship

from src.config.database import Base


class ShoppingList(Base):
    """
    Model de lista de compras.
    
    Attributes:
        id: UUID único da lista.
        user_id: ID do usuário (FK).
        name: Nome da lista.
        latitude: Latitude da localização.
        longitude: Longitude da localização.
        created_at: Data de criação.
        updated_at: Data de última atualização.
    """
    
    __tablename__ = 'shopping_lists'
    
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = Column(
        GUID(),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    name = Column(
        String(100),
        nullable=True
    )
    latitude = Column(
        DECIMAL(10, 8),
        nullable=True
    )
    longitude = Column(
        DECIMAL(11, 8),
        nullable=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    user = relationship(
        'User',
        back_populates='shopping_lists'
    )
    items = relationship(
        'ListItem',
        back_populates='list',
        cascade='all, delete-orphan',
        order_by='ListItem.added_at'
    )
    
    def calculate_total(self) -> Optional[float]:
        """
        Calcula o total estimado da lista baseado nas ofertas mais baratas.
        
        Returns:
            Optional[float]: Total estimado ou None se não houver itens/offers.
        """
        if not self.items:
            return None
        
        total = Decimal('0.0')
        has_prices = False
        
        for item in self.items:
            if item.product and item.product.offers:
                # Pegar a oferta mais barata
                cheapest_offer = min(
                    item.product.offers,
                    key=lambda o: o.price if o.in_stock else float('inf')
                )
                if cheapest_offer.in_stock:
                    item_total = cheapest_offer.price * item.quantity
                    total += item_total
                    has_prices = True
        
        return float(total) if has_prices else None
    
    def get_best_stores(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retorna as melhores lojas para comprar todos os itens da lista.
        
        Args:
            limit: Número máximo de lojas a retornar.
        
        Returns:
            List[Dict[str, Any]]: Lista de dicionários com dados das lojas e total.
        """
        if not self.items:
            return []
        
        # Agrupar ofertas por loja
        store_totals = {}
        
        for item in self.items:
            if item.product and item.product.offers:
                for offer in item.product.offers:
                    if offer.in_stock and offer.store:
                        store_id = offer.store_id
                        store_name = offer.store.name
                        
                        if store_id not in store_totals:
                            store_totals[store_id] = {
                                'store': offer.store.to_dict(),
                                'total': Decimal('0.0'),
                                'items_count': 0
                            }
                        
                        item_total = offer.price * item.quantity
                        store_totals[store_id]['total'] += item_total
                        store_totals[store_id]['items_count'] += 1
        
        # Ordenar por total (menor preço primeiro)
        sorted_stores = sorted(
            store_totals.values(),
            key=lambda x: x['total']
        )[:limit]
        
        # Converter para dicionários finais
        result = []
        for store_data in sorted_stores:
            result.append({
                'store': store_data['store'],
                'estimated_total': float(store_data['total']),
                'items_count': store_data['items_count']
            })
        
        return result
    
    def to_dict(self, include_items: bool = False, include_user: bool = False) -> Dict[str, Any]:
        """
        Serializa a lista para dicionário.
        
        Args:
            include_items: Se deve incluir os itens da lista.
            include_user: Se deve incluir dados do usuário.
        
        Returns:
            Dict[str, Any]: Dicionário com dados da lista.
        """
        data = {
            'id': str(self.id),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if self.name:
            data['name'] = self.name
        
        if self.latitude and self.longitude:
            data['latitude'] = float(self.latitude)
            data['longitude'] = float(self.longitude)
        
        # Calcular total estimado
        total = self.calculate_total()
        if total is not None:
            data['estimated_total'] = total
        
        if include_items and self.items:
            data['items'] = [item.to_dict(include_product=True) for item in self.items]
            data['items_count'] = len(self.items)
        
        if include_user and self.user:
            data['user'] = self.user.to_dict(include_email=False)
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação da lista.
        """
        return f"<ShoppingList(id={self.id}, user_id={self.user_id}, name={self.name})>"
