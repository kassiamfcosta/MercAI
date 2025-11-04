"""
Configuração do Banco de Dados

Módulo responsável por configurar a conexão com PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import logging

from src.config.settings import Settings

logger = logging.getLogger(__name__)

# Carregar configurações
settings = Settings()

# Criar engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_recycle=3600,   # Recicla conexões a cada 1 hora
    echo=settings.FLASK_DEBUG  # Log de queries apenas em desenvolvimento
)

# Criar session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Scoped session para threads
ScopedSession = scoped_session(SessionLocal)

# Base para models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection para obter sessão do banco de dados.
    
    Yields:
        Session: Sessão do SQLAlchemy.
    
    Example:
        ```python
        def some_endpoint():
            db = next(get_db())
            try:
                # usar db
                user = db.query(User).first()
                return user
            finally:
                db.close()
        ```
    """
    db: Session = ScopedSession()
    try:
        yield db
    finally:
        db.close()
        ScopedSession.remove()


def init_db() -> None:
    """
    Inicializa o banco de dados criando todas as tabelas.
    
    Importa todos os models antes de criar as tabelas.
    """
    try:
        # Importar todos os models para que sejam registrados no Base
        from src.models import user  # noqa: F401
        from src.models import store  # noqa: F401
        from src.models import product  # noqa: F401
        from src.models import offer  # noqa: F401
        from src.models import shopping_list  # noqa: F401
        from src.models import list_item  # noqa: F401
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados criadas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise


def close_db() -> None:
    """
    Fecha todas as conexões do banco de dados.
    
    Útil para limpeza ao encerrar a aplicação.
    """
    try:
        ScopedSession.remove()
        engine.dispose()
        logger.info("Conexões do banco de dados fechadas")
    except Exception as e:
        logger.error(f"Erro ao fechar conexões do banco de dados: {e}")


# Event listener para logar queries lentas em desenvolvimento
if settings.FLASK_DEBUG:
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        """Loga queries antes da execução em modo debug."""
        logger.debug(f"Query: {statement[:200]}...")
        if parameters:
            logger.debug(f"Parameters: {parameters}")


# Context manager para usar em blocos with
class DatabaseSession:
    """
    Context manager para sessão do banco de dados.
    
    Example:
        ```python
        with DatabaseSession() as db:
            user = User(email='test@example.com')
            db.add(user)
            db.commit()
        ```
    """
    
    def __init__(self):
        """Inicializa o context manager."""
        self.db: Session = None
    
    def __enter__(self) -> Session:
        """
        Entra no context manager e retorna a sessão.
        
        Returns:
            Session: Sessão do banco de dados.
        """
        self.db = ScopedSession()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Sai do context manager e fecha a sessão.
        
        Args:
            exc_type: Tipo da exceção (se houver).
            exc_val: Valor da exceção (se houver).
            exc_tb: Traceback da exceção (se houver).
        """
        if exc_type is not None:
            self.db.rollback()
            logger.error(f"Erro no contexto do banco de dados: {exc_val}")
        
        self.db.close()
        ScopedSession.remove()
        return False  # Propaga exceções se houver
