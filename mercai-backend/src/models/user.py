"""
Model User - Entidade de Usuário

Model SQLAlchemy para representar usuários do sistema com autenticação segura.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import bcrypt
import jwt
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base
from src.config.settings import Settings
from src.utils.uuid_type import GUID

settings = Settings()


class User(Base):
    """
    Model de usuário com autenticação segura.
    
    Attributes:
        id: UUID único do usuário.
        email: Email do usuário (único).
        password_hash: Hash da senha (bcrypt).
        name: Nome do usuário.
        created_at: Data de criação.
        updated_at: Data de última atualização.
    """
    
    __tablename__ = 'users'
    
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = Column(
        String(255),
        nullable=False
    )
    name = Column(
        String(100),
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
    shopping_lists = relationship(
        'ShoppingList',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password: str) -> None:
        """
        Define a senha do usuário usando bcrypt.
        
        Args:
            password: Senha em texto plano.
        
        Raises:
            ValueError: Se a senha tiver menos de 8 caracteres.
        """
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        
        # Gerar salt e hash da senha
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            salt
        ).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        
        Args:
            password: Senha em texto plano a ser verificada.
        
        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except Exception:
            return False
    
    def generate_token(self) -> str:
        """
        Gera um token JWT para o usuário.
        
        Returns:
            str: Token JWT.
        """
        payload = {
            'user_id': str(self.id),
            'email': self.email,
            'exp': datetime.utcnow().timestamp() + (settings.JWT_EXPIRATION_HOURS * 3600)
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        return token
    
    def to_dict(self, include_email: bool = True) -> Dict[str, Any]:
        """
        Serializa o usuário para dicionário.
        
        IMPORTANTE: Nunca inclui password_hash por segurança.
        
        Args:
            include_email: Se deve incluir o email no dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com dados do usuário.
        """
        data = {
            'id': str(self.id),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_email:
            data['email'] = self.email
        
        if self.name:
            data['name'] = self.name
        
        return data
    
    def __repr__(self) -> str:
        """
        Representação string do objeto.
        
        Returns:
            str: Representação do usuário.
        """
        return f"<User(id={self.id}, email={self.email})>"
