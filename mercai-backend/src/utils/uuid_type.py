"""
UUID Type para SQLite

TypeDecorator para suportar UUID em SQLite.
"""

import uuid
from sqlalchemy import TypeDecorator, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID


class GUID(TypeDecorator):
    """
    TypeDecorator para UUID que funciona com SQLite e PostgreSQL.
    
    Converte UUID para String no SQLite e usa UUID nativo no PostgreSQL.
    """
    
    impl = String
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        """Retorna o tipo apropriado para cada dialeto."""
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgresUUID())
        else:
            return dialect.type_descriptor(String(36))
    
    def process_bind_param(self, value, dialect):
        """Converte UUID para string ao salvar."""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(value)
            return str(value)
    
    def process_result_value(self, value, dialect):
        """Converte string para UUID ao ler."""
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

