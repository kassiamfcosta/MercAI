"""
Model Store - Entidade de Loja

Model SQLAlchemy para representar lojas/supermercados do sistema.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base


class Store(Base):
    """
    Model de loja/supermercado.
    
    Attributes:
        id: ID único da loja.
        name: Nome da loja.
        url: URL do site da loja.
        logo_url: URL do logo da loja.
        latitude: Latitude da localização.
        longitude: Longitude da localização.
        address: Endereço completo.
        phone: Telefone de contato.
        created_at: Data de criação.
    """
    
    __tablename__ = 'stores'
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(
        String(100),
        nullable=False,
        index=True
    )
    url = Column(
        String(255),
        nullable=True
    )
    logo_url = Column(
        String(255),
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
    address = Column(
        Text,
        nullable=True
    )
    phone = Column(
        String(20),
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
        back_populates='store',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_offers: bool = False) -> Dict[str, Any]:
        """
        Serializa a loja para dicionário.
        
        Args:
            include_offers: Se deve incluir as ofertas relacionadas.
        
        Returns:
            Dict[str, Any]: Dicionário com dados da loja.
        """
        data = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if self.url:
            data['url'] = self.url
        
        if self.logo_url:
            data['logo_url'] = self.logo_url
        
        if self.latitude and self.longitude:
            data['latitude'] = float(self.latitude)
            data['longitude'] = float(self.longitude)
        
        if self.address:
            data['address'] = self.address
        
        if self.phone:
            data['phone'] = self.phone
        
        if include_offers and self.offers:
            data['offers'] = [offer.to_dict() for offer in self.offers]
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação da loja.
        """
        return f"<Store(id={self.id}, name={self.name})>"
