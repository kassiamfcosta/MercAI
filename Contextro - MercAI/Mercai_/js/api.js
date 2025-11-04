/**
 * Classe API - Comunicação Centralizada com Backend
 * 
 * Gerencia todas as requisições HTTP ao backend com tratamento de erros,
 * loading states e autenticação automática.
 */

class API {
    constructor() {
        this.baseURL = window.API_CONFIG?.BASE_URL || 'http://localhost:5000/api';
        this.timeout = window.API_CONFIG?.TIMEOUT || 30000;
    }
    
    /**
     * Faz uma requisição HTTP genérica
     * 
     * @param {string} endpoint - Endpoint da API
     * @param {object} options - Opções da requisição (method, body, headers, etc)
     * @returns {Promise} Resposta da API
     */
    async request(endpoint, options = {}) {
        const {
            method = 'GET',
            body = null,
            headers = {},
            requiresAuth = true,
            timeout = this.timeout
        } = options;
        
        // Preparar headers
        const requestHeaders = {
            ...window.API_CONFIG?.DEFAULT_HEADERS,
            ...headers
        };
        
        // Adicionar token de autenticação se necessário
        if (requiresAuth && window.Auth) {
            window.Auth.addAuthHeader(requestHeaders);
        }
        
        // Preparar URL
        const url = endpoint.startsWith('http') 
            ? endpoint 
            : `${this.baseURL}${endpoint}`;
        
        // Preparar controller para timeout
        const controller = new AbortController();
        let timeoutId = null;
        
        // Preparar opções da requisição
        const fetchOptions = {
            method,
            headers: requestHeaders,
            signal: controller.signal
        };
        
        // Configurar timeout
        timeoutId = setTimeout(() => controller.abort(), timeout);
        
        // Adicionar body se existir
        if (body) {
            if (body instanceof FormData) {
                // Não definir Content-Type para FormData (browser define automaticamente)
                delete requestHeaders['Content-Type'];
                fetchOptions.body = body;
            } else {
                fetchOptions.body = JSON.stringify(body);
            }
        }
        
        try {
            const response = await fetch(url, fetchOptions);
            
            // Parsear resposta
            let data;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }
            
            // Verificar se a resposta foi bem-sucedida
            if (!response.ok) {
                // Se token expirado, fazer logout
                if (response.status === 401 && window.Auth) {
                    window.Auth.clearAuth();
                    window.location.href = 'login.html?expired=true';
                    throw new Error('Sessão expirada. Faça login novamente.');
                }
                
                // Criar objeto de erro com detalhes da resposta
                const error = new Error(data.message || `Erro ${response.status}: ${response.statusText}`);
                
                // Adicionar informações extras ao erro para preservar dados da API
                error.response = {
                    status: response.status,
                    statusText: response.statusText,
                    data: data
                };
                
                // Preservar campos success e errors se existirem
                if (data.success !== undefined) {
                    error.success = data.success;
                }
                if (data.errors) {
                    error.errors = data.errors;
                }
                
                throw error;
            }
            
            return data;
            
        } catch (error) {
            // Tratar erro de timeout
            if (error.name === 'AbortError' || error.message?.includes('aborted')) {
                const timeoutError = new Error('Requisição excedeu o tempo limite. Tente novamente.');
                timeoutError.isTimeout = true;
                throw timeoutError;
            }
            
            // Tratar erro de rede
            if (error instanceof TypeError && error.message.includes('fetch')) {
                const networkError = new Error('Erro de conexão. Verifique sua internet e tente novamente.');
                networkError.isNetworkError = true;
                throw networkError;
            }
            
            // Preservar erros já tratados (com response)
            if (error.response) {
                throw error;
            }
            
            // Para outros erros, criar um erro padronizado
            const unknownError = new Error(error.message || 'Erro desconhecido ao processar requisição');
            unknownError.originalError = error;
            throw unknownError;
        } finally {
            // Garantir que o timeout seja limpo
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
        }
    }
    
    // Métodos HTTP simplificados
    
    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }
    
    async post(endpoint, body, options = {}) {
        return this.request(endpoint, { ...options, method: 'POST', body });
    }
    
    async put(endpoint, body, options = {}) {
        return this.request(endpoint, { ...options, method: 'PUT', body });
    }
    
    async delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
    
    // Métodos específicos da API
    
    /**
     * Autenticação
     */
    async login(email, password) {
        const response = await this.post('/auth/login', { email, password }, { requiresAuth: false });
        if (response.success && response.data) {
            window.Auth?.saveToken(response.data.token, response.data.user);
        }
        return response;
    }
    
    async register(userData) {
        const response = await this.post('/auth/register', userData, { requiresAuth: false });
        if (response.success && response.data) {
            window.Auth?.saveToken(response.data.token, response.data.user);
        }
        return response;
    }
    
    async getMe() {
        return this.get('/auth/me');
    }
    
    /**
     * Produtos
     */
    async searchProducts(query, category = null) {
        const params = new URLSearchParams({ q: query });
        if (category) params.append('category', category);
        return this.get(`/products/search?${params.toString()}`);
    }
    
    async getCategories() {
        return this.get('/products/categories');
    }
    
    async getPopularProducts() {
        return this.get('/products/popular');
    }
    
    async getProduct(productId) {
        return this.get(`/products/${productId}`);
    }
    
    /**
     * Listas
     */
    async getLists() {
        return this.get('/lists');
    }
    
    async getList(listId) {
        return this.get(`/lists/${listId}`);
    }
    
    async createList(listData) {
        return this.post('/lists', listData);
    }
    
    async updateList(listId, listData) {
        return this.put(`/lists/${listId}`, listData);
    }
    
    async deleteList(listId) {
        return this.delete(`/lists/${listId}`);
    }
    
    async addListItem(listId, itemData) {
        return this.post(`/lists/${listId}/items`, itemData);
    }
    
    async updateListItem(listId, itemId, itemData) {
        return this.put(`/lists/${listId}/items/${itemId}`, itemData);
    }
    
    async deleteListItem(listId, itemId) {
        return this.delete(`/lists/${listId}/items/${itemId}`);
    }
    
    /**
     * Ranking
     */
    async getRanking(listId, latitude = null, longitude = null) {
        const params = new URLSearchParams({ list_id: listId });
        if (latitude) params.append('latitude', latitude);
        if (longitude) params.append('longitude', longitude);
        return this.get(`/ranking?${params.toString()}`);
    }
    
    async getDetailedRanking(listId, latitude = null, longitude = null) {
        const params = new URLSearchParams();
        if (latitude) params.append('latitude', latitude);
        if (longitude) params.append('longitude', longitude);
        return this.get(`/ranking/${listId}/detailed?${params.toString()}`);
    }
    
    /**
     * Lojas
     */
    async getStores() {
        return this.get('/stores');
    }
    
    async getStore(storeId) {
        return this.get(`/stores/${storeId}`);
    }
    
    async getNearbyStores(latitude, longitude, radius = 5) {
        const params = new URLSearchParams({
            lat: latitude,
            lon: longitude,
            radius: radius
        });
        return this.get(`/stores/nearby?${params.toString()}`);
    }
}

// Criar instância global
window.api = new API();
