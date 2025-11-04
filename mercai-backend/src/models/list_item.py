"""
Model ListItem - Entidade de Item de Lista

Model SQLAlchemy para representar itens de uma lista de compras.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.utils.uuid_type import GUID

from src.config.database import Base


class ListItem(Base):
    """
    Model de item de lista de compras.
    
    Attributes:
        id: ID único do item.
        list_id: ID da lista (FK).
        product_id: ID do produto (FK).
        quantity: Quantidade do produto.
        added_at: Data/hora de adição do item.
    """
    
    __tablename__ = 'list_items'
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    list_id = Column(
        GUID(),
        ForeignKey('shopping_lists.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    product_id = Column(
        Integer,
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    quantity = Column(
        Integer,
        default=1,
        nullable=False
    )
    added_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    list = relationship(
        'ShoppingList',
        back_populates='items'
    )
    product = relationship(
        'Product',
        back_populates='list_items'
    )
    
    def to_dict(self, include_product: bool = False, include_list: bool = False) -> Dict[str, Any]:
        """
        Serializa o item para dicionário.
        
        Args:
            include_product: Se deve incluir dados do produto.
            include_list: Se deve incluir dados da lista.
        
        Returns:
            Dict[str, Any]: Dicionário com dados do item.
        """
        data = {
            'id': self.id,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat() if self.added_at else None,
        }
        
        if include_product and self.product:
            data['product'] = self.product.to_dict(include_offers=False)
        
        if include_list and self.list:
            data['list'] = self.list.to_dict(include_items=False)
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação do item.
        """
        return f"<ListItem(id={self.id}, list_id={self.list_id}, product_id={self.product_id}, quantity={self.quantity})>"
