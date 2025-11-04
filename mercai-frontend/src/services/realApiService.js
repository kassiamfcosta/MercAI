/**
 * API Service - Integração com Backend
 * 
 * Serviço centralizado para comunicação com a API do backend MercAI.
 */

import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// URL base da API (ajustar conforme ambiente ou variável de ambiente)
let ENV_API_URL;
try {
  const env = require('@env');
  ENV_API_URL = env.API_BASE_URL;
} catch (error) {
  ENV_API_URL = undefined;
}

const API_BASE_URL = ENV_API_URL || (__DEV__ 
  ? 'http://localhost:5000/api'
  : 'https://seu-backend-render.com/api');

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token JWT
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Erro ao buscar token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar respostas
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  async (error) => {
    if (error.response?.status === 401) {
      // Token inválido ou expirado - fazer logout
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

/**
 * Serviço de Autenticação
 */
export const authService = {
  /**
   * Registra um novo usuário
   */
  async register(email, password, name) {
    try {
      const response = await api.post('/auth/register', {
        email,
        password,
        name,
      });
      
      if (response.success && response.data?.token) {
        await AsyncStorage.setItem('token', response.data.token);
        await AsyncStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao registrar usuário' };
    }
  },

  /**
   * Faz login
   */
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      
      if (response.success && response.data?.token) {
        await AsyncStorage.setItem('token', response.data.token);
        await AsyncStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao fazer login' };
    }
  },

  /**
   * Obtém dados do usuário logado
   */
  async getMe() {
    try {
      const response = await api.get('/auth/me');
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar usuário' };
    }
  },

  /**
   * Faz logout
   */
  async logout() {
    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('user');
  },

  /**
   * Verifica se usuário está logado
   */
  async isAuthenticated() {
    try {
      const token = await AsyncStorage.getItem('token');
      return !!token;
    } catch {
      return false;
    }
  },

  /**
   * Obtém token armazenado
   */
  async getToken() {
    return await AsyncStorage.getItem('token');
  },

  /**
   * Obtém usuário armazenado
   */
  async getUser() {
    const userStr = await AsyncStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
};

/**
 * Serviço de Produtos
 */
export const productsService = {
  /**
   * Busca produtos
   */
  async search(query, category = null, page = 1, perPage = 20) {
    try {
      const params = new URLSearchParams({
        q: query,
        page: page.toString(),
        per_page: perPage.toString(),
      });
      
      if (category) {
        params.append('category', category);
      }
      
      const response = await api.get(`/products/search?${params}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar produtos' };
    }
  },

  /**
   * Obtém detalhes de um produto
   */
  async getProduct(productId) {
    try {
      const response = await api.get(`/products/${productId}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar produto' };
    }
  },

  /**
   * Obtém ofertas de um produto
   */
  async getProductOffers(productId, sort = 'price_asc', inStockOnly = true) {
    try {
      const params = new URLSearchParams({
        sort,
        in_stock_only: inStockOnly.toString(),
      });
      
      const response = await api.get(`/products/${productId}/offers?${params}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar ofertas' };
    }
  },
};

/**
 * Serviço de Listas de Compras
 */
export const listsService = {
  /**
   * Cria uma nova lista
   */
  async createList(name, latitude = null, longitude = null) {
    try {
      const response = await api.post('/lists', {
        name,
        latitude,
        longitude,
      });
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao criar lista' };
    }
  },

  /**
   * Lista todas as listas do usuário
   */
  async getLists() {
    try {
      const response = await api.get('/lists');
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar listas' };
    }
  },

  /**
   * Obtém detalhes de uma lista
   */
  async getList(listId) {
    try {
      const response = await api.get(`/lists/${listId}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao buscar lista' };
    }
  },

  /**
   * Atualiza uma lista
   */
  async updateList(listId, name, latitude = null, longitude = null) {
    try {
      const response = await api.put(`/lists/${listId}`, {
        name,
        latitude,
        longitude,
      });
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao atualizar lista' };
    }
  },

  /**
   * Deleta uma lista
   */
  async deleteList(listId) {
    try {
      const response = await api.delete(`/lists/${listId}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao deletar lista' };
    }
  },

  /**
   * Adiciona um item à lista
   */
  async addItem(listId, productId, quantity = 1) {
    try {
      const response = await api.post(`/lists/${listId}/items`, {
        product_id: productId,
        quantity,
      });
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao adicionar item' };
    }
  },

  /**
   * Remove um item da lista
   */
  async removeItem(listId, itemId) {
    try {
      const response = await api.delete(`/lists/${listId}/items/${itemId}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao remover item' };
    }
  },

  /**
   * Atualiza a quantidade de um item
   */
  async updateItemQuantity(listId, itemId, quantity) {
    try {
      const response = await api.put(`/lists/${listId}/items/${itemId}`, {
        quantity,
      });
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao atualizar item' };
    }
  },
};

/**
 * Serviço de Ranking
 */
export const rankingService = {
  /**
   * Gera ranking básico para uma lista
   */
  async getRanking(listId, latitude = null, longitude = null) {
    try {
      const params = new URLSearchParams({
        list_id: listId,
      });
      
      if (latitude && longitude) {
        params.append('latitude', latitude.toString());
        params.append('longitude', longitude.toString());
      }
      
      const response = await api.get(`/ranking?${params}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao gerar ranking' };
    }
  },

  /**
   * Gera ranking detalhado para uma lista
   */
  async getDetailedRanking(listId, latitude = null, longitude = null) {
    try {
      const params = new URLSearchParams();
      
      if (latitude && longitude) {
        params.append('latitude', latitude.toString());
        params.append('longitude', longitude.toString());
      }
      
      const response = await api.get(`/ranking/${listId}/detailed?${params}`);
      return response;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao gerar ranking detalhado' };
    }
  },
};

export default api;

