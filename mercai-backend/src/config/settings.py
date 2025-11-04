"""
Configurações do Sistema

Módulo responsável por carregar e validar variáveis de ambiente.
"""

import os
from typing import Optional, List
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class Settings:
    """
    Classe de configurações do sistema.
    
    Carrega todas as variáveis de ambiente e fornece validação.
    Usa padrão Singleton implícito através de instância única.
    """
    
    # Aplicação
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG: bool = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT: Optional[int] = int(os.getenv('PORT', '8000')) if os.getenv('PORT') else 8000
    
    # Banco de Dados (Supabase PostgreSQL)
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    
    # Redis (Upstash)
    REDIS_URL: str = os.getenv('REDIS_URL', '')
    
    # IA (Google Gemini)
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    # Scraping
    USER_AGENT: str = os.getenv('USER_AGENT', 'MercAI/1.0 (Educational Project)')
    SCRAPING_DELAY_MIN: int = int(os.getenv('SCRAPING_DELAY_MIN', '1'))
    SCRAPING_DELAY_MAX: int = int(os.getenv('SCRAPING_DELAY_MAX', '3'))
    
    # CORS
    CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', '*').split(',')
    
    def __init__(self):
        """Inicializa as configurações e valida variáveis obrigatórias."""
        self._validate_required_vars()
        logger.info(f"Configurações carregadas - Ambiente: {self.FLASK_ENV}")
    
    def _validate_required_vars(self) -> None:
        """
        Valida variáveis de ambiente obrigatórias.
        
        Raises:
            ValueError: Se alguma variável obrigatória não estiver definida.
        """
        required_vars = []
        
        if not self.DATABASE_URL:
            required_vars.append('DATABASE_URL')
        
        if not self.REDIS_URL:
            required_vars.append('REDIS_URL')
        
        if not self.GEMINI_API_KEY:
            required_vars.append('GEMINI_API_KEY')
        
        if self.FLASK_ENV == 'production':
            if self.SECRET_KEY == 'dev-secret-key-change-in-production':
                required_vars.append('SECRET_KEY')
            if self.JWT_SECRET_KEY == 'dev-secret-key-change-in-production':
                required_vars.append('JWT_SECRET_KEY')
        
        if required_vars:
            missing = ', '.join(required_vars)
            logger.warning(f"Variáveis obrigatórias não definidas: {missing}")
            logger.warning("O sistema pode não funcionar corretamente sem essas variáveis.")
    
    def is_production(self) -> bool:
        """
        Verifica se está em ambiente de produção.
        
        Returns:
            bool: True se estiver em produção, False caso contrário.
        """
        return self.FLASK_ENV == 'production'
    
    def is_development(self) -> bool:
        """
        Verifica se está em ambiente de desenvolvimento.
        
        Returns:
            bool: True se estiver em desenvolvimento, False caso contrário.
        """
        return self.FLASK_ENV == 'development'
