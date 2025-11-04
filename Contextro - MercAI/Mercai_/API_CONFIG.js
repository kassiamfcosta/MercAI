/**
 * Configuração da API MercAI
 * 
 * Arquivo centralizado para configurações da API backend.
 */

const API_CONFIG = {
    // URL base da API - ajustar conforme ambiente
    // Para GitHub Pages, usar URL do backend em produção
    BASE_URL: (() => {
        const hostname = window.location.hostname;
        
        // Desenvolvimento local
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000/api';
        }
        
        // GitHub Pages - usar URL do backend em produção
        // Altere esta URL para o seu backend em produção (ex: Render, Heroku, etc.)
        if (hostname.includes('github.io') || hostname.includes('github-pages')) {
            return 'https://seu-backend.herokuapp.com/api'; // Altere para sua URL de produção
        }
        
        // Outros ambientes - usar mesmo host
        return `${window.location.protocol}//${window.location.host}/api`;
    })(),
    
    // Timeout para requisições (ms)
    TIMEOUT: 30000,
    
    // Headers padrão
    DEFAULT_HEADERS: {
        'Content-Type': 'application/json',
    },
    
    // Endpoints
    ENDPOINTS: {
        // Autenticação
        AUTH: {
            LOGIN: '/auth/login',
            REGISTER: '/auth/register',
            ME: '/auth/me',
            LOGOUT: '/auth/logout'
        },
        // Produtos
        PRODUCTS: {
            SEARCH: '/products/search',
            CATEGORIES: '/products/categories',
            POPULAR: '/products/popular',
            DETAIL: (id) => `/products/${id}`
        },
        // Listas
        LISTS: {
            LIST: '/lists',
            DETAIL: (id) => `/lists/${id}`,
            ITEMS: (id) => `/lists/${id}/items`,
            ITEM: (listId, itemId) => `/lists/${listId}/items/${itemId}`
        },
        // Ranking
        RANKING: {
            GET: '/ranking',
            DETAILED: (listId) => `/ranking/${listId}/detailed`
        },
        // Lojas
        STORES: {
            LIST: '/stores',
            DETAIL: (id) => `/stores/${id}`,
            NEARBY: '/stores/nearby'
        }
    }
};

// Exportar para uso global
window.API_CONFIG = API_CONFIG;
