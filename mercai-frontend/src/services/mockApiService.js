/**
 * Mock API Service - Simulação do Backend
 * 
 * Este serviço simula as respostas da API real para desenvolvimento,
 * seguindo a estratégia Mock-First do guia.
 */

import {
  mockUsers,
  mockProducts,
  mockStores,
  mockOffers,
  mockShoppingLists,
  mockListItems,
  delay,
  findProductById,
  findStoreById,
  findOffersByProductId,
  findItemsByListId,
} from '../data/mockData';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Helper para gerar UUID simples
 */
const generateUUID = () => {
  return 'mock-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
};

/**
 * Serviço de Autenticação Mock
 */
export const authService = {
  /**
   * Registra um novo usuário
   */
  async register(email, password, name) {
    await delay(800);

    // Verificar se email já existe
    const existingUser = mockUsers.find(u => u.email === email);
    if (existingUser) {
      throw { message: 'Email já cadastrado' };
    }

    // Criar novo usuário
    const newUser = {
      id: generateUUID(),
      email,
      name,
      created_at: new Date().toISOString(),
    };

    // Simular token
    const token = 'mock-token-' + Date.now();

    // Salvar no AsyncStorage
    await AsyncStorage.setItem('token', token);
    await AsyncStorage.setItem('user', JSON.stringify(newUser));

    return {
      success: true,
      message: 'Usuário registrado com sucesso',
      data: {
        user: newUser,
        token,
      },
    };
  },

  /**
   * Faz login
   */
  async login(email, password) {
    await delay(1000);

    // Credenciais mock válidas
    if (email === 'teste@example.com' && password === '123456') {
      const user = mockUsers[0];
      const token = 'mock-token-' + Date.now();

      await AsyncStorage.setItem('token', token);
      await AsyncStorage.setItem('user', JSON.stringify(user));

      return {
        success: true,
        message: 'Login bem-sucedido',
        data: {
          user: {
            id: user.id,
            email: user.email,
            name: user.name,
          },
          token,
        },
      };
    }

    // Outros usuários mock
    const user = mockUsers.find(u => u.email === email);
    if (user) {
      const token = 'mock-token-' + Date.now();
      await AsyncStorage.setItem('token', token);
      await AsyncStorage.setItem('user', JSON.stringify(user));

      return {
        success: true,
        message: 'Login bem-sucedido',
        data: {
          user: {
            id: user.id,
            email: user.email,
            name: user.name,
          },
          token,
        },
      };
    }

    throw { message: 'Credenciais inválidas' };
  },

  /**
   * Obtém dados do usuário logado
   */
  async getMe() {
    await delay(500);

    const userStr = await AsyncStorage.getItem('user');
    if (!userStr) {
      throw { message: 'Usuário não autenticado' };
    }

    const user = JSON.parse(userStr);
    return {
      success: true,
      message: 'Dados do usuário recuperados',
      data: {
        user,
      },
    };
  },

  /**
   * Faz logout
   */
  async logout() {
    await delay(300);
    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('user');
  },

  /**
   * Verifica se usuário está logado
   */
  async isAuthenticated() {
    const token = await AsyncStorage.getItem('token');
    return !!token;
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
 * Serviço de Produtos Mock
 */
export const productsService = {
  /**
   * Busca produtos
   */
  async search(query, category = null, page = 1, perPage = 20) {
    await delay(600);

    let results = mockProducts;

    // Filtrar por query
    if (query && query.length >= 3) {
      const queryLower = query.toLowerCase();
      results = results.filter(p =>
        p.name.toLowerCase().includes(queryLower) ||
        (p.brand && p.brand.toLowerCase().includes(queryLower))
      );
    }

    // Filtrar por categoria
    if (category) {
      results = results.filter(p =>
        p.category && p.category.toLowerCase().includes(category.toLowerCase())
      );
    }

    // Paginação
    const total = results.length;
    const totalPages = Math.ceil(total / perPage);
    const offset = (page - 1) * perPage;
    const paginatedResults = results.slice(offset, offset + perPage);

    return {
      success: true,
      message: 'Busca realizada com sucesso',
      data: {
        products: paginatedResults,
        pagination: {
          page,
          per_page: perPage,
          total,
          pages: totalPages,
        },
      },
    };
  },

  /**
   * Obtém detalhes de um produto
   */
  async getProduct(productId) {
    await delay(500);

    const product = findProductById(productId);
    if (!product) {
      throw { message: 'Produto não encontrado' };
    }

    const offers = findOffersByProductId(productId).filter(o => o.in_stock);

    // Adicionar dados das lojas às ofertas
    const offersWithStores = offers.map(offer => {
      const store = findStoreById(offer.store_id);
      return {
        ...offer,
        store,
      };
    });

    return {
      success: true,
      message: 'Produto encontrado',
      data: {
        product: {
          ...product,
          offers: offersWithStores,
          offers_count: offersWithStores.length,
        },
      },
    };
  },

  /**
   * Obtém ofertas de um produto
   */
  async getProductOffers(productId, sort = 'price_asc', inStockOnly = true) {
    await delay(500);

    const product = findProductById(productId);
    if (!product) {
      throw { message: 'Produto não encontrado' };
    }

    let offers = findOffersByProductId(productId);

    // Filtrar por estoque
    if (inStockOnly) {
      offers = offers.filter(o => o.in_stock);
    }

    // Adicionar dados das lojas
    offers = offers.map(offer => {
      const store = findStoreById(offer.store_id);
      return {
        ...offer,
        store,
      };
    });

    // Ordenar
    if (sort === 'price_asc') {
      offers.sort((a, b) => a.price - b.price);
    } else if (sort === 'price_desc') {
      offers.sort((a, b) => b.price - a.price);
    } else if (sort === 'score') {
      offers.sort((a, b) => {
        const scoreA = (a.discount_percentage || 0) + (a.in_stock ? 1 : 0);
        const scoreB = (b.discount_percentage || 0) + (b.in_stock ? 1 : 0);
        return scoreB - scoreA;
      });
    }

    return {
      success: true,
      message: 'Ofertas encontradas',
      data: {
        product,
        offers,
        count: offers.length,
      },
    };
  },
};

/**
 * Serviço de Listas de Compras Mock
 */
export const listsService = {
  /**
   * Cria uma nova lista
   */
  async createList(name, latitude = null, longitude = null) {
    await delay(600);

    const userStr = await AsyncStorage.getItem('user');
    if (!userStr) {
      throw { message: 'Usuário não autenticado' };
    }

    const user = JSON.parse(userStr);
    const newList = {
      id: generateUUID(),
      user_id: user.id,
      name,
      latitude,
      longitude,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    return {
      success: true,
      message: 'Lista criada com sucesso',
      data: {
        list: newList,
      },
    };
  },

  /**
   * Lista todas as listas do usuário
   */
  async getLists() {
    await delay(500);

    const userStr = await AsyncStorage.getItem('user');
    if (!userStr) {
      throw { message: 'Usuário não autenticado' };
    }

    const user = JSON.parse(userStr);
    const lists = mockShoppingLists.filter(l => l.user_id === user.id);

    return {
      success: true,
      message: 'Listas recuperadas com sucesso',
      data: {
        lists: lists.map(list => ({
          ...list,
          items: [],
        })),
        count: lists.length,
      },
    };
  },

  /**
   * Obtém detalhes de uma lista
   */
  async getList(listId) {
    await delay(500);

    const list = mockShoppingLists.find(l => l.id === listId);
    if (!list) {
      throw { message: 'Lista não encontrada' };
    }

    const items = findItemsByListId(listId).map(item => {
      const product = findProductById(item.product_id);
      return {
        ...item,
        product,
      };
    });

    return {
      success: true,
      message: 'Lista recuperada com sucesso',
      data: {
        list: {
          ...list,
          items,
        },
      },
    };
  },

  /**
   * Atualiza uma lista
   */
  async updateList(listId, name, latitude = null, longitude = null) {
    await delay(600);

    const list = mockShoppingLists.find(l => l.id === listId);
    if (!list) {
      throw { message: 'Lista não encontrada' };
    }

    const updatedList = {
      ...list,
      name: name || list.name,
      latitude: latitude !== null ? latitude : list.latitude,
      longitude: longitude !== null ? longitude : list.longitude,
      updated_at: new Date().toISOString(),
    };

    return {
      success: true,
      message: 'Lista atualizada com sucesso',
      data: {
        list: updatedList,
      },
    };
  },

  /**
   * Deleta uma lista
   */
  async deleteList(listId) {
    await delay(500);

    const list = mockShoppingLists.find(l => l.id === listId);
    if (!list) {
      throw { message: 'Lista não encontrada' };
    }

    return {
      success: true,
      message: 'Lista deletada com sucesso',
    };
  },

  /**
   * Adiciona um item à lista
   */
  async addItem(listId, productId, quantity = 1) {
    await delay(600);

    const product = findProductById(productId);
    if (!product) {
      throw { message: 'Produto não encontrado' };
    }

    const newItem = {
      id: mockListItems.length + 1,
      list_id: listId,
      product_id: productId,
      quantity,
      added_at: new Date().toISOString(),
    };

    return {
      success: true,
      message: 'Item adicionado com sucesso',
      data: {
        item: {
          ...newItem,
          product,
        },
      },
    };
  },

  /**
   * Remove um item da lista
   */
  async removeItem(listId, itemId) {
    await delay(500);

    return {
      success: true,
      message: 'Item removido com sucesso',
    };
  },

  /**
   * Atualiza a quantidade de um item
   */
  async updateItemQuantity(listId, itemId, quantity) {
    await delay(500);

    return {
      success: true,
      message: 'Item atualizado com sucesso',
      data: {
        item: {
          id: itemId,
          quantity,
        },
      },
    };
  },
};

/**
 * Serviço de Ranking Mock
 */
export const rankingService = {
  /**
   * Gera ranking básico para uma lista
   */
  async getRanking(listId, latitude = null, longitude = null) {
    await delay(1200);

    const list = mockShoppingLists.find(l => l.id === listId);
    if (!list) {
      throw { message: 'Lista não encontrada' };
    }

    const items = findItemsByListId(listId);
    const rankingItems = [];

    for (const item of items) {
      const product = findProductById(item.product_id);
      const offers = findOffersByProductId(item.product_id).filter(o => o.in_stock);

      if (offers.length > 0) {
        // Calcular scores simples
        const offersWithScores = offers.map(offer => {
          const store = findStoreById(offer.store_id);
          
          // Score simples: menor preço = maior score
          let score = 100 - (offer.price * 2);
          if (offer.discount_percentage) {
            score += offer.discount_percentage * 0.5;
          }
          if (offer.in_stock) {
            score += 10;
          }

          return {
            ...offer,
            store,
            score: Math.max(0, Math.min(100, score.toFixed(2))),
          };
        });

        offersWithScores.sort((a, b) => parseFloat(b.score) - parseFloat(a.score));
        const bestOffer = offersWithScores[0];

        rankingItems.push({
          product,
          quantity: item.quantity,
          best_offer: bestOffer,
          all_offers: offersWithScores.slice(0, 5),
        });
      } else {
        rankingItems.push({
          product,
          quantity: item.quantity,
          best_offer: null,
          all_offers: [],
        });
      }
    }

    // Calcular melhor combinação
    const storeTotals = {};
    for (const item of rankingItems) {
      if (item.best_offer) {
        const storeId = item.best_offer.store.id;
        if (!storeTotals[storeId]) {
          storeTotals[storeId] = {
            store: item.best_offer.store,
            total: 0,
            items_count: 0,
            savings: 0,
          };
        }
        storeTotals[storeId].total += item.best_offer.price * item.quantity;
        storeTotals[storeId].items_count += 1;
        if (item.best_offer.original_price) {
          storeTotals[storeId].savings +=
            (item.best_offer.original_price - item.best_offer.price) * item.quantity;
        }
      }
    }

    const sortedStores = Object.values(storeTotals).sort((a, b) => a.total - b.total);
    const bestCombination = sortedStores.length > 0 ? {
      recommended_store: sortedStores[0].store.name,
      store_id: sortedStores[0].store.id,
      estimated_total: parseFloat(sortedStores[0].total.toFixed(2)),
      total_savings: parseFloat(sortedStores[0].savings.toFixed(2)),
      items_count: sortedStores[0].items_count,
      alternatives: sortedStores.slice(1, 4).map(s => ({
        store: s.store,
        estimated_total: parseFloat(s.total.toFixed(2)),
        items_count: s.items_count,
        savings: parseFloat(s.savings.toFixed(2)),
      })),
    } : null;

    return {
      success: true,
      message: 'Ranking gerado com sucesso',
      data: {
        list_id: listId,
        items: rankingItems,
        best_combination: bestCombination,
      },
    };
  },

  /**
   * Gera ranking detalhado para uma lista
   */
  async getDetailedRanking(listId, latitude = null, longitude = null) {
    const basicRanking = await this.getRanking(listId, latitude, longitude);

    // Calcular resumo
    let estimatedTotal = 0;
    let totalSavings = 0;

    for (const item of basicRanking.data.items) {
      if (item.best_offer) {
        estimatedTotal += item.best_offer.price * item.quantity;
        if (item.best_offer.original_price) {
          totalSavings +=
            (item.best_offer.original_price - item.best_offer.price) * item.quantity;
        }
      }
    }

    basicRanking.data.summary = {
      estimated_total: parseFloat(estimatedTotal.toFixed(2)),
      total_savings: parseFloat(totalSavings.toFixed(2)),
      items_count: basicRanking.data.items.length,
    };

    return basicRanking;
  },
};

