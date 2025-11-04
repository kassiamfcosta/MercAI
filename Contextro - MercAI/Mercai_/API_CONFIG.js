/**
 * Configuração da API MercAI
 * 
 * Arquivo centralizado para configurações da API backend.
 */

const API_CONFIG = {
    // URL base da API - ajustar conforme ambiente
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/api'
        : `${window.location.protocol}//${window.location.host}/api`,
    
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
