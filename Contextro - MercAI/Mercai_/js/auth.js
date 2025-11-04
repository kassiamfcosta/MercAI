/**
 * Middleware de Autenticação MercAI
 * 
 * Gerencia autenticação JWT, tokens e redirecionamentos.
 */

const Auth = {
    /**
     * Chave para armazenar o token no localStorage
     */
    TOKEN_KEY: 'mercai_token',
    
    /**
     * Chave para armazenar dados do usuário
     */
    USER_KEY: 'mercai_user',
    
    /**
     * Verifica se o usuário está autenticado
     * 
     * @returns {boolean} True se autenticado, False caso contrário
     */
    isAuthenticated() {
        const token = localStorage.getItem(this.TOKEN_KEY);
        if (!token) {
            return false;
        }
        
        // Verificar se o token não expirou (decodificação básica)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const expirationTime = payload.exp * 1000; // Converter para milissegundos
            return Date.now() < expirationTime;
        } catch (e) {
            console.error('Erro ao verificar token:', e);
            return false;
        }
    },
    
    /**
     * Obtém o token JWT do localStorage
     * 
     * @returns {string|null} Token JWT ou null se não existir
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },
    
    /**
     * Salva o token JWT no localStorage
     * 
     * @param {string} token - Token JWT
     * @param {object} user - Dados do usuário (opcional)
     */
    saveToken(token, user = null) {
        localStorage.setItem(this.TOKEN_KEY, token);
        if (user) {
            localStorage.setItem(this.USER_KEY, JSON.stringify(user));
        }
    },
    
    /**
     * Remove o token e dados do usuário
     */
    clearAuth() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    },
    
    /**
     * Obtém dados do usuário do localStorage
     * 
     * @returns {object|null} Dados do usuário ou null
     */
    getUser() {
        const userStr = localStorage.getItem(this.USER_KEY);
        return userStr ? JSON.parse(userStr) : null;
    },
    
    /**
     * Adiciona o token JWT no header Authorization
     * 
     * @param {object} headers - Headers da requisição
     * @returns {object} Headers com Authorization adicionado
     */
    addAuthHeader(headers = {}) {
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },
    
    /**
     * Redireciona para a página de login se não autenticado
     * 
     * @param {string} redirectPath - Caminho para redirecionar após login
     */
    requireAuth(redirectPath = null) {
        if (!this.isAuthenticated()) {
            const currentPath = window.location.pathname;
            const redirectUrl = redirectPath || currentPath;
            window.location.href = `login.html?redirect=${encodeURIComponent(redirectUrl)}`;
            return false;
        }
        return true;
    },
    
    /**
     * Redireciona para a página inicial se já autenticado
     * (útil para páginas de login/cadastro)
     */
    redirectIfAuthenticated() {
        if (this.isAuthenticated()) {
            const urlParams = new URLSearchParams(window.location.search);
            const redirect = urlParams.get('redirect');
            window.location.href = redirect || 'inicio.html';
            return true;
        }
        return false;
    },
    
    /**
     * Faz logout e redireciona para login
     */
    logout() {
        this.clearAuth();
        window.location.href = 'login.html';
    }
};

// Exportar para uso global
window.Auth = Auth;
