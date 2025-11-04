"""
Model Product - Entidade de Produto

Model SQLAlchemy para representar produtos do sistema.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base


class Product(Base):
    """
    Model de produto.
    
    Attributes:
        id: ID único do produto.
        name: Nome do produto.
        category: Categoria do produto.
        brand: Marca do produto.
        image_url: URL da imagem do produto.
        created_at: Data de criação.
    """
    
    __tablename__ = 'products'
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(
        String(255),
        nullable=False,
        index=True
    )
    category = Column(
        String(50),
        nullable=True,
        index=True
    )
    brand = Column(
        String(100),
        nullable=True,
        index=True
    )
    image_url = Column(
        String(255),
        nullable=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    offers = relationship(
        'Offer',
        back_populates='product',
        cascade='all, delete-orphan'
    )
    list_items = relationship(
        'ListItem',
        back_populates='product',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_offers: bool = False) -> Dict[str, Any]:
        """
        Serializa o produto para dicionário.
        
        Args:
            include_offers: Se deve incluir as ofertas relacionadas.
        
        Returns:
            Dict[str, Any]: Dicionário com dados do produto.
        """
        data = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if self.category:
            data['category'] = self.category
        
        if self.brand:
            data['brand'] = self.brand
        
        if self.image_url:
            data['image_url'] = self.image_url
        
        if include_offers and self.offers:
            data['offers'] = [offer.to_dict() for offer in self.offers]
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação do produto.
        """
        return f"<Product(id={self.id}, name={self.name})>"
