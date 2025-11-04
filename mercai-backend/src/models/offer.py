"""
Model Offer - Entidade de Oferta

Model SQLAlchemy para representar ofertas de produtos em lojas.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
from decimal import Decimal
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Boolean, Date, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from src.config.database import Base


class Offer(Base):
    """
    Model de oferta de produto em uma loja.
    
    Attributes:
        id: ID único da oferta.
        product_id: ID do produto (FK).
        store_id: ID da loja (FK).
        price: Preço atual.
        original_price: Preço original (antes do desconto).
        discount_percentage: Percentual de desconto.
        in_stock: Se o produto está em estoque.
        valid_until: Data de validade da oferta.
        scraped_at: Data/hora do scraping.
    """
    
    __tablename__ = 'offers'
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    product_id = Column(
        Integer,
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    store_id = Column(
        Integer,
        ForeignKey('stores.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    price = Column(
        DECIMAL(10, 2),
        nullable=False
    )
    original_price = Column(
        DECIMAL(10, 2),
        nullable=True
    )
    discount_percentage = Column(
        DECIMAL(5, 2),
        nullable=True
    )
    in_stock = Column(
        Boolean,
        default=True,
        nullable=False
    )
    valid_until = Column(
        Date,
        nullable=True
    )
    scraped_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('product_id', 'store_id', name='uq_offer_product_store'),
        Index('idx_offers_scraped', 'scraped_at'),
        Index('idx_offers_product', 'product_id'),
        Index('idx_offers_store', 'store_id'),
    )
    
    # Relacionamentos
    product = relationship(
        'Product',
        back_populates='offers'
    )
    store = relationship(
        'Store',
        back_populates='offers'
    )
    
    def calculate_discount_percentage(self) -> Optional[float]:
        """
        Calcula o percentual de desconto se houver preço original.
        
        Returns:
            Optional[float]: Percentual de desconto ou None.
        """
        if self.original_price and self.price < self.original_price:
            discount = float(
                ((self.original_price - self.price) / self.original_price) * 100
            )
            return round(discount, 2)
        return None
    
    def to_dict(self, include_product: bool = False, include_store: bool = False) -> Dict[str, Any]:
        """
        Serializa a oferta para dicionário.
        
        Args:
            include_product: Se deve incluir dados do produto.
            include_store: Se deve incluir dados da loja.
        
        Returns:
            Dict[str, Any]: Dicionário com dados da oferta.
        """
        data = {
            'id': self.id,
            'price': float(self.price),
            'in_stock': self.in_stock,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
        }
        
        if self.original_price:
            data['original_price'] = float(self.original_price)
        
        # Calcular desconto se necessário
        if self.discount_percentage:
            data['discount_percentage'] = float(self.discount_percentage)
        elif self.original_price and self.price < self.original_price:
            discount = self.calculate_discount_percentage()
            if discount:
                data['discount_percentage'] = discount
        
        if self.valid_until:
            data['valid_until'] = self.valid_until.isoformat()
        
        if include_product and self.product:
            data['product'] = self.product.to_dict()
        
        if include_store and self.store:
            data['store'] = self.store.to_dict()
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação da oferta.
        """
        return f"<Offer(id={self.id}, product_id={self.product_id}, store_id={self.store_id}, price={self.price})>"
