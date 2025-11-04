/**
 * Mock Data - Dados simulados para desenvolvimento
 * 
 * Este arquivo contém dados mock para simular respostas da API
 * durante o desenvolvimento, seguindo a estratégia Mock-First.
 */

// Usuários mock
export const mockUsers = [
  {
    id: '1',
    email: 'teste@example.com',
    name: 'Usuário Teste',
    password: '123456', // Apenas para mock, nunca usar em produção real
  },
  {
    id: '2',
    email: 'maria@example.com',
    name: 'Maria Silva',
  },
  {
    id: '3',
    email: 'joao@example.com',
    name: 'João Santos',
  },
];

// Lojas mock
export const mockStores = [
  {
    id: 1,
    name: 'Supermercado Central',
    url: 'https://supercentral.com.br',
    logo_url: null,
    latitude: -15.7942,
    longitude: -47.8822,
    address: 'Av. Central, 123 - Brasília, DF',
    phone: '(61) 3333-4444',
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Mercado Popular',
    url: 'https://mercadopopular.com.br',
    logo_url: null,
    latitude: -15.8000,
    longitude: -47.8900,
    address: 'Rua Comercial, 456 - Brasília, DF',
    phone: '(61) 3333-5555',
    created_at: '2024-01-02T00:00:00Z',
  },
  {
    id: 3,
    name: 'Atacadão',
    url: 'https://atacadao.com.br',
    logo_url: null,
    latitude: -15.7900,
    longitude: -47.8800,
    address: 'Rodovia BR-040, Km 10 - Brasília, DF',
    phone: '(61) 3333-6666',
    created_at: '2024-01-03T00:00:00Z',
  },
  {
    id: 4,
    name: 'Supermercado Bom Preço',
    url: 'https://bompreco.com.br',
    logo_url: null,
    latitude: -15.8100,
    longitude: -47.9000,
    address: 'Av. Norte, 789 - Brasília, DF',
    phone: '(61) 3333-7777',
    created_at: '2024-01-04T00:00:00Z',
  },
];

// Produtos mock
export const mockProducts = [
  {
    id: 1,
    name: 'Arroz Tio João Tipo 1 - 5kg',
    category: 'Alimentos',
    brand: 'Tio João',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Feijão Carioca Camil - 1kg',
    category: 'Alimentos',
    brand: 'Camil',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 3,
    name: 'Óleo de Soja Liza - 900ml',
    category: 'Alimentos',
    brand: 'Liza',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 4,
    name: 'Açúcar Cristal União - 1kg',
    category: 'Alimentos',
    brand: 'União',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 5,
    name: 'Macarrão Espaguete Galo - 500g',
    category: 'Alimentos',
    brand: 'Galo',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 6,
    name: 'Coca-Cola Lata - 350ml',
    category: 'Bebidas',
    brand: 'Coca-Cola',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 7,
    name: 'Leite Longa Vida Parmalat - 1L',
    category: 'Frios e Laticínios',
    brand: 'Parmalat',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 8,
    name: 'Pão de Açúcar Francês - 500g',
    category: 'Padaria',
    brand: 'Pão de Açúcar',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 9,
    name: 'Sabão em Pó Omo - 1kg',
    category: 'Limpeza',
    brand: 'Omo',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 10,
    name: 'Detergente Ypê - 500ml',
    category: 'Limpeza',
    brand: 'Ypê',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 11,
    name: 'Papel Higiênico Personal Vip - 12 unidades',
    category: 'Higiene',
    brand: 'Personal Vip',
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 12,
    name: 'Tomate - 1kg',
    category: 'Hortifruti',
    brand: null,
    image_url: null,
    created_at: '2024-01-01T00:00:00Z',
  },
];

// Ofertas mock
export const mockOffers = [
  // Arroz - diferentes lojas
  {
    id: 1,
    product_id: 1,
    store_id: 1,
    price: 28.90,
    original_price: 32.90,
    discount_percentage: 12.16,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 2,
    product_id: 1,
    store_id: 2,
    price: 27.50,
    original_price: 30.00,
    discount_percentage: 8.33,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T11:00:00Z',
  },
  {
    id: 3,
    product_id: 1,
    store_id: 3,
    price: 26.99,
    original_price: null,
    discount_percentage: null,
    in_stock: true,
    valid_until: null,
    scraped_at: '2024-01-15T12:00:00Z',
  },
  // Feijão
  {
    id: 4,
    product_id: 2,
    store_id: 1,
    price: 8.90,
    original_price: 10.90,
    discount_percentage: 18.35,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 5,
    product_id: 2,
    store_id: 4,
    price: 9.50,
    original_price: null,
    discount_percentage: null,
    in_stock: true,
    valid_until: null,
    scraped_at: '2024-01-15T13:00:00Z',
  },
  // Óleo
  {
    id: 6,
    product_id: 3,
    store_id: 2,
    price: 6.99,
    original_price: 8.99,
    discount_percentage: 22.25,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T11:00:00Z',
  },
  {
    id: 7,
    product_id: 3,
    store_id: 3,
    price: 7.50,
    original_price: null,
    discount_percentage: null,
    in_stock: true,
    valid_until: null,
    scraped_at: '2024-01-15T12:00:00Z',
  },
  // Coca-Cola
  {
    id: 8,
    product_id: 6,
    store_id: 1,
    price: 4.50,
    original_price: 5.50,
    discount_percentage: 18.18,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 9,
    product_id: 6,
    store_id: 2,
    price: 4.99,
    original_price: null,
    discount_percentage: null,
    in_stock: true,
    valid_until: null,
    scraped_at: '2024-01-15T11:00:00Z',
  },
  // Leite
  {
    id: 10,
    product_id: 7,
    store_id: 4,
    price: 5.99,
    original_price: 6.99,
    discount_percentage: 14.31,
    in_stock: true,
    valid_until: '2024-12-31',
    scraped_at: '2024-01-15T13:00:00Z',
  },
  {
    id: 11,
    product_id: 7,
    store_id: 3,
    price: 6.50,
    original_price: null,
    discount_percentage: null,
    in_stock: true,
    valid_until: null,
    scraped_at: '2024-01-15T12:00:00Z',
  },
];

// Listas de compras mock
export const mockShoppingLists = [
  {
    id: 'list-1',
    user_id: '1',
    name: 'Compras do Mês',
    latitude: -15.7942,
    longitude: -47.8822,
    created_at: '2024-01-10T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'list-2',
    user_id: '1',
    name: 'Lista Semanal',
    latitude: -15.7942,
    longitude: -47.8822,
    created_at: '2024-01-20T00:00:00Z',
    updated_at: '2024-01-20T00:00:00Z',
  },
];

// Itens de lista mock
export const mockListItems = [
  {
    id: 1,
    list_id: 'list-1',
    product_id: 1,
    quantity: 2,
    added_at: '2024-01-10T10:00:00Z',
  },
  {
    id: 2,
    list_id: 'list-1',
    product_id: 2,
    quantity: 3,
    added_at: '2024-01-10T10:05:00Z',
  },
  {
    id: 3,
    list_id: 'list-1',
    product_id: 3,
    quantity: 2,
    added_at: '2024-01-10T10:10:00Z',
  },
  {
    id: 4,
    list_id: 'list-1',
    product_id: 6,
    quantity: 6,
    added_at: '2024-01-10T10:15:00Z',
  },
  {
    id: 5,
    list_id: 'list-1',
    product_id: 7,
    quantity: 4,
    added_at: '2024-01-10T10:20:00Z',
  },
  {
    id: 6,
    list_id: 'list-2',
    product_id: 11,
    quantity: 2,
    added_at: '2024-01-20T09:00:00Z',
  },
  {
    id: 7,
    list_id: 'list-2',
    product_id: 10,
    quantity: 3,
    added_at: '2024-01-20T09:05:00Z',
  },
];

/**
 * Helper function para simular delay de API
 */
export const delay = (ms = 500) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Helper function para encontrar produto por ID
 */
export const findProductById = (id) => {
  return mockProducts.find(p => p.id === id);
};

/**
 * Helper function para encontrar loja por ID
 */
export const findStoreById = (id) => {
  return mockStores.find(s => s.id === id);
};

/**
 * Helper function para encontrar ofertas de um produto
 */
export const findOffersByProductId = (productId) => {
  return mockOffers.filter(o => o.product_id === productId);
};

/**
 * Helper function para encontrar itens de uma lista
 */
export const findItemsByListId = (listId) => {
  return mockListItems.filter(item => item.list_id === listId);
};

