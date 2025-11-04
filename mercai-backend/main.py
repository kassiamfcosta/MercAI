"""
MercAI Backend - Entry Point

Aplicação Flask para comparação de preços de supermercados com IA.
"""

from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
import logging
import sys
import os
from datetime import datetime

from src.config.settings import Settings
from src.config.database import init_db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Carregar configurações
settings = Settings()

# Caminho para o frontend (ajustar conforme necessário)
FRONTEND_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'Contextro - MercAI',
    'Mercai_'
)

# Inicializar Flask com suporte para arquivos estáticos
app = Flask(
    __name__,
    static_folder=FRONTEND_PATH if os.path.exists(FRONTEND_PATH) else None,
    static_url_path=''
)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['DEBUG'] = settings.FLASK_DEBUG

# Configurar CORS para permitir requisições do frontend
CORS(app, resources={
    r"/api/*": {
        "origins": "*" if settings.FLASK_ENV == "development" else settings.CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Inicializar banco de dados
try:
    init_db()
    logger.info("Banco de dados inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar banco de dados: {e}")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check para monitoramento."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.FLASK_ENV
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Redireciona para /health"""
    return jsonify({
        "message": "MercAI Backend API",
        "version": "1.0.0",
        "health": "/health"
    }), 200

# Rotas para servir arquivos estáticos do frontend
@app.route('/<path:path>', methods=['GET'])
def serve_frontend(path):
    """
    Serve arquivos estáticos do frontend.
    
    Tenta servir o arquivo solicitado. Se não encontrar, retorna index.html
    para suportar SPA routing.
    
    IMPORTANTE: Não intercepta rotas que começam com /api/
    """
    # Não servir arquivos estáticos para rotas da API
    if path.startswith('api/'):
        # Deixar que o Flask retorne 404 se a rota não existir nos blueprints
        return jsonify({
            "success": False,
            "message": "Endpoint não encontrado"
        }), 404
    
    if os.path.exists(FRONTEND_PATH):
        # Se o arquivo existe, serve ele
        if os.path.isfile(os.path.join(FRONTEND_PATH, path)):
            return send_from_directory(FRONTEND_PATH, path)
        # Se for um diretório, tenta servir index.html desse diretório
        elif os.path.isdir(os.path.join(FRONTEND_PATH, path)):
            index_path = os.path.join(FRONTEND_PATH, path, 'index.html')
            if os.path.exists(index_path):
                return send_file(index_path)
        # Caso contrário, tenta servir index.html (para SPA routing)
        index_file = os.path.join(FRONTEND_PATH, 'index.html')
        if os.path.exists(index_file):
            return send_file(index_file)
    
    # Se não encontrar nada, retorna 404
    return jsonify({
        "success": False,
        "message": "Arquivo não encontrado"
    }), 404

# Registrar blueprints
from src.api.auth import auth_bp
from src.api.products import products_bp
from src.api.lists import lists_bp
from src.api.ranking import ranking_bp
from src.api.stores import stores_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(lists_bp, url_prefix='/api/lists')
app.register_blueprint(ranking_bp, url_prefix='/api/ranking')
app.register_blueprint(stores_bp, url_prefix='/api/stores')

# Tratamento global de erros
@app.errorhandler(404)
def not_found(error):
    """Handler para erros 404"""
    return jsonify({
        "success": False,
        "message": "Endpoint não encontrado"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros 500"""
    logger.error(f"Erro interno: {error}", exc_info=True)
    return jsonify({
        "success": False,
        "message": "Erro interno do servidor"
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handler genérico para exceções não tratadas"""
    logger.error(f"Exceção não tratada: {e}", exc_info=True)
    return jsonify({
        "success": False,
        "message": "Erro ao processar requisição"
    }), 500

if __name__ == '__main__':
    # Usar PORT do ambiente (Render.com) ou padrão 8000
    port = int(os.environ.get('PORT', settings.PORT or 8000))
    debug = settings.FLASK_DEBUG
    
    # Desabilitar debug em produção
    if settings.is_production():
        debug = False
    
    logger.info(f"Iniciando servidor Flask na porta {port} (debug={debug})")
    logger.info(f"Frontend path: {FRONTEND_PATH}")
    app.run(host='0.0.0.0', port=port, debug=debug)
