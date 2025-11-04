/**
 * API Service - Barrel File para Alternância entre Mock e Real API
 * 
 * Este arquivo atua como um ponto central que exporta o serviço apropriado
 * baseado em variáveis de ambiente e configuração, seguindo a estratégia
 * Mock-First do guia.
 * 
 * Configuração:
 * - EXPO_PUBLIC_USE_MOCK=true: Usa mockApiService (desenvolvimento/teste)
 * - EXPO_PUBLIC_USE_MOCK=false ou não definido: Usa realApiService (produção/padrão)
 * - __DEV__: Usa realApiService por padrão em desenvolvimento, a menos que USE_MOCK=true
 */

// Tentar importar variável de ambiente (pode ser undefined)
let USE_MOCK;
try {
  const env = require('@env');
  // Expo usa EXPO_PUBLIC_ prefix, mas o plugin converte para sem prefix
  USE_MOCK = env.USE_MOCK || env.EXPO_PUBLIC_USE_MOCK || process.env.EXPO_PUBLIC_USE_MOCK;
} catch (error) {
  // Se @env não estiver disponível, tenta process.env
  USE_MOCK = process.env.EXPO_PUBLIC_USE_MOCK || undefined;
}

// Determinar qual serviço usar
const shouldUseMock = () => {
  // Se variável de ambiente USE_MOCK estiver definida, respeitar
  if (USE_MOCK !== undefined && USE_MOCK !== null) {
    return USE_MOCK === 'true' || USE_MOCK === true || USE_MOCK === '1';
  }
  
  // Em desenvolvimento, padrão é usar API real
  // Mas pode ser sobrescrito pela variável de ambiente
  // Em produção, sempre usar API real
  return false;
};

const useMock = shouldUseMock();

// Importar serviços apropriados
let authService, productsService, listsService, rankingService;

if (useMock) {
  console.log('[API Service] Usando Mock API Service');
  const mockServices = require('./mockApiService');
  authService = mockServices.authService;
  productsService = mockServices.productsService;
  listsService = mockServices.listsService;
  rankingService = mockServices.rankingService;
} else {
  console.log('[API Service] Usando Real API Service');
  const realServices = require('./realApiService');
  authService = realServices.authService;
  productsService = realServices.productsService;
  listsService = realServices.listsService;
  rankingService = realServices.rankingService;
}

// Exportar serviços
export {
  authService,
  productsService,
  listsService,
  rankingService,
};

// Exportar função utilitária para verificar qual serviço está sendo usado
export const getApiServiceType = () => {
  return useMock ? 'mock' : 'real';
};

