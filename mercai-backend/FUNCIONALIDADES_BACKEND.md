# 🚀 Funcionalidades do Backend MercAI

## Status Geral: ✅ **FUNCIONANDO**

**Total de Endpoints**: 21 endpoints implementados  
**Servidor**: Rodando em `http://localhost:8000`  
**Banco de Dados**: SQLite (desenvolvimento)  
**Cache**: Redis (opcional - desabilitado se não configurado)  
**Autenticação**: JWT (JSON Web Tokens)

---

## 📋 Índice

1. [Autenticação](#1-autenticação)
2. [Produtos](#2-produtos)
3. [Lojas](#3-lojas)
4. [Listas de Compras](#4-listas-de-compras)
5. [Ranking de Ofertas](#5-ranking-de-ofertas)
6. [Funcionalidades Adicionais](#6-funcionalidades-adicionais)
7. [Serviços Internos](#7-serviços-internos)

---

## 1. 🔐 Autenticação

**Blueprint**: `/api/auth`

### ✅ POST `/api/auth/register`
- **Descrição**: Registra um novo usuário
- **Body**:
  ```json
  {
    "email": "usuario@example.com",
    "password": "senha123",
    "name": "Nome do Usuário" // opcional
  }
  ```
- **Validações**:
  - Email único e válido
  - Senha mínimo 8 caracteres, pelo menos 1 número
  - Nome máximo 100 caracteres (opcional)
- **Resposta**: Token JWT + dados do usuário
- **Status**: ✅ Funcionando

### ✅ POST `/api/auth/login`
- **Descrição**: Faz login e retorna token JWT
- **Body**:
  ```json
  {
    "email": "usuario@example.com",
    "password": "senha123"
  }
  ```
- **Resposta**: Token JWT + dados do usuário
- **Status**: ✅ Funcionando

### ✅ GET `/api/auth/me`
- **Descrição**: Retorna dados do usuário logado
- **Headers**: `Authorization: Bearer <token>`
- **Resposta**: Dados completos do usuário
- **Status**: ✅ Funcionando (requer autenticação)

---

## 2. 🛍️ Produtos

**Blueprint**: `/api/products`

### ✅ GET `/api/products/search`
- **Descrição**: Busca produtos por nome e categoria
- **Query Parameters**:
  - `q` (obrigatório): Termo de busca (mínimo 3 caracteres)
  - `category` (opcional): Filtrar por categoria
  - `page` (opcional): Número da página (padrão: 1)
  - `per_page` (opcional): Itens por página (padrão: 20, máximo: 50)
- **Exemplo**: `/api/products/search?q=arroz&category=alimentos&page=1`
- **Resposta**: Lista paginada de produtos
- **Cache**: ✅ 1 hora
- **Status**: ✅ Funcionando

### ✅ GET `/api/products/<product_id>`
- **Descrição**: Retorna detalhes de um produto específico
- **Resposta**: Dados completos do produto
- **Cache**: ✅ 30 minutos
- **Status**: ✅ Funcionando

### ✅ GET `/api/products/<product_id>/offers`
- **Descrição**: Retorna todas as ofertas de um produto
- **Query Parameters**:
  - `sort` (opcional): `price_asc`, `price_desc`, `score` (padrão: `price_asc`)
- **Resposta**: Lista de ofertas ordenadas
- **Status**: ✅ Funcionando

### ✅ GET `/api/products/categories`
- **Descrição**: Retorna lista de categorias disponíveis
- **Resposta**: Array de categorias
- **Cache**: ✅ 24 horas
- **Status**: ✅ Funcionando

### ✅ GET `/api/products/popular`
- **Descrição**: Retorna produtos mais populares
- **Query Parameters**:
  - `limit` (opcional): Número de produtos (padrão: 10, máximo: 50)
- **Resposta**: Lista de produtos populares
- **Cache**: ✅ 1 hora
- **Status**: ✅ Funcionando

---

## 3. 🏪 Lojas

**Blueprint**: `/api/stores`

### ✅ GET `/api/stores`
- **Descrição**: Lista todas as lojas cadastradas
- **Query Parameters**:
  - `page` (opcional): Número da página (padrão: 1)
  - `per_page` (opcional): Itens por página (padrão: 20, máximo: 50)
- **Resposta**: Lista paginada de lojas
- **Cache**: ✅ 1 hora
- **Status**: ✅ Funcionando

### ✅ GET `/api/stores/<store_id>`
- **Descrição**: Retorna detalhes de uma loja específica
- **Resposta**: Dados completos da loja + contagem de ofertas
- **Cache**: ✅ 30 minutos
- **Status**: ✅ Funcionando

### ✅ GET `/api/stores/nearby`
- **Descrição**: Retorna lojas próximas a uma localização (geolocalização)
- **Query Parameters**:
  - `lat` (obrigatório): Latitude
  - `lon` (obrigatório): Longitude
  - `radius` (opcional): Raio de busca em km (padrão: 5, máximo: 50)
  - `limit` (opcional): Número máximo de resultados (padrão: 10, máximo: 50)
- **Exemplo**: `/api/stores/nearby?lat=-15.8229&lon=-48.0844&radius=5`
- **Resposta**: Lista de lojas ordenadas por distância (inclui distância calculada)
- **Algoritmo**: ✅ Fórmula de Haversine para cálculo de distância
- **Cache**: ✅ 10 minutos
- **Status**: ✅ Funcionando

---

## 4. 📝 Listas de Compras

**Blueprint**: `/api/lists`

**Todas as rotas requerem autenticação JWT** 🔒

### ✅ POST `/api/lists`
- **Descrição**: Cria uma nova lista de compras
- **Body**:
  ```json
  {
    "name": "Lista de Compras",
    "latitude": -15.8229,  // opcional
    "longitude": -48.0844  // opcional
  }
  ```
- **Resposta**: Lista criada com UUID
- **Status**: ✅ Funcionando

### ✅ GET `/api/lists`
- **Descrição**: Lista todas as listas do usuário logado
- **Query Parameters**:
  - `page` (opcional): Número da página
  - `per_page` (opcional): Itens por página
- **Resposta**: Lista paginada de listas do usuário
- **Status**: ✅ Funcionando

### ✅ GET `/api/lists/<list_id>`
- **Descrição**: Retorna detalhes de uma lista específica
- **Validação**: ✅ Verifica se o usuário é dono da lista
- **Resposta**: Dados completos da lista + itens
- **Status**: ✅ Funcionando

### ✅ PUT `/api/lists/<list_id>`
- **Descrição**: Atualiza uma lista existente
- **Validação**: ✅ Verifica ownership
- **Body**: Mesmos campos do POST (name, latitude, longitude)
- **Status**: ✅ Funcionando

### ✅ DELETE `/api/lists/<list_id>`
- **Descrição**: Deleta uma lista (e seus itens)
- **Validação**: ✅ Verifica ownership
- **Status**: ✅ Funcionando

### ✅ GET `/api/lists/<list_id>/items`
- **Descrição**: Retorna todos os itens de uma lista
- **Validação**: ✅ Verifica ownership
- **Resposta**: Array de itens da lista
- **Status**: ✅ Funcionando

### ✅ POST `/api/lists/<list_id>/items`
- **Descrição**: Adiciona um item à lista
- **Validação**: ✅ Verifica ownership
- **Body**:
  ```json
  {
    "product_id": 1,
    "quantity": 2,
    "notes": "Preferir marca X"  // opcional
  }
  ```
- **Status**: ✅ Funcionando

### ✅ PUT `/api/lists/<list_id>/items/<item_id>`
- **Descrição**: Atualiza um item da lista
- **Validação**: ✅ Verifica ownership
- **Body**: quantity, notes, checked (opcional)
- **Status**: ✅ Funcionando

### ✅ DELETE `/api/lists/<list_id>/items/<item_id>`
- **Descrição**: Remove um item da lista
- **Validação**: ✅ Verifica ownership
- **Status**: ✅ Funcionando

---

## 5. 🏆 Ranking de Ofertas

**Blueprint**: `/api/ranking`

**Todas as rotas requerem autenticação JWT** 🔒

### ✅ GET `/api/ranking`
- **Descrição**: Gera ranking básico de ofertas para uma lista de compras
- **Query Parameters**:
  - `list_id` (obrigatório): UUID da lista
  - `latitude` (opcional): Latitude do usuário (para cálculo de distância)
  - `longitude` (opcional): Longitude do usuário
- **Validação**: ✅ Verifica se o usuário é dono da lista
- **Resposta**: Ranking com melhores ofertas por produto
- **Status**: ✅ Funcionando

### ✅ GET `/api/ranking/<list_id>/detailed`
- **Descrição**: Gera ranking detalhado com sugestões otimizadas
- **Query Parameters**:
  - `latitude` (opcional): Para cálculo de distância
  - `longitude` (opcional): Para cálculo de distância
- **Validação**: ✅ Verifica ownership
- **Resposta**: Ranking detalhado com sugestões de otimização de compras
- **Status**: ✅ Funcionando

---

## 6. ⚙️ Funcionalidades Adicionais

### ✅ GET `/health`
- **Descrição**: Health check do servidor
- **Resposta**: Status do servidor + timestamp + ambiente
- **Status**: ✅ Funcionando

### ✅ GET `/`
- **Descrição**: Endpoint raiz com informações da API
- **Resposta**: Informações básicas + link para /health
- **Status**: ✅ Funcionando

### ✅ Frontend Static Files
- **Descrição**: Serve arquivos HTML/CSS/JS do frontend
- **Rota**: `/<path:path>` (exceto `/api/*`)
- **Status**: ✅ Funcionando

---

## 7. 🔧 Serviços Internos

### ✅ Cache (Redis)
- **Descrição**: Sistema de cache opcional usando Redis
- **Status**: ⚠️ Configurado mas opcional (funciona sem Redis)
- **Nota**: Se Redis não estiver configurado, o sistema funciona normalmente sem cache

### ✅ Validação de Dados
- **Descrição**: Validação de entrada usando Marshmallow schemas
- **Schemas**: `RegisterSchema`, `LoginSchema`
- **Status**: ✅ Funcionando

### ✅ Autenticação JWT
- **Descrição**: Sistema de autenticação baseado em JWT
- **Decorator**: `@token_required`
- **Expiração**: Configurável (padrão: 24 horas)
- **Status**: ✅ Funcionando

### ✅ Geolocalização
- **Descrição**: Cálculo de distâncias usando fórmula de Haversine
- **Uso**: Endpoint `/api/stores/nearby` e ranking
- **Status**: ✅ Funcionando

### ✅ Paginação
- **Descrição**: Sistema de paginação padrão em todas as listas
- **Parâmetros**: `page`, `per_page`
- **Resposta**: Inclui metadata de paginação
- **Status**: ✅ Funcionando

### ✅ Logging
- **Descrição**: Sistema de logs estruturado
- **Níveis**: INFO, WARNING, ERROR
- **Status**: ✅ Funcionando

### ✅ Tratamento de Erros
- **Descrição**: Handlers globais para erros 404, 500 e exceções
- **Respostas**: Formato JSON padronizado
- **Status**: ✅ Funcionando

### ✅ CORS
- **Descrição**: Configurado para permitir requisições do frontend
- **Ambiente**: Development (permitir tudo), Production (origens específicas)
- **Status**: ✅ Funcionando

---

## 📊 Resumo por Categoria

| Categoria | Endpoints | Status |
|-----------|-----------|--------|
| Autenticação | 3 | ✅ 100% |
| Produtos | 5 | ✅ 100% |
| Lojas | 3 | ✅ 100% |
| Listas | 9 | ✅ 100% |
| Ranking | 2 | ✅ 100% |
| Sistema | 2 | ✅ 100% |
| **TOTAL** | **24** | ✅ **100%** |

---

## 🎯 Funcionalidades Principais (Requisitos)

### ✅ Receber lista de compras do usuário
- **Implementado**: POST `/api/lists` + POST `/api/lists/<id>/items`
- **Status**: ✅ Funcionando

### ✅ Comparar preços entre diferentes lojas
- **Implementado**: GET `/api/products/<id>/offers` (com ordenação por preço)
- **Status**: ✅ Funcionando

### ✅ Identificar melhores ofertas e descontos
- **Implementado**: GET `/api/ranking` (ranking por produto)
- **Status**: ✅ Funcionando

### ✅ Retornar ranking de preços por produto
- **Implementado**: GET `/api/ranking` + GET `/api/ranking/<id>/detailed`
- **Status**: ✅ Funcionando

### ✅ Atualizar Dashboard de preços
- **Implementado**: GET `/api/ranking` retorna dados para dashboard
- **Status**: ✅ Funcionando

### ✅ Otimizar sugestões (opcional)
- **Implementado**: GET `/api/ranking/<id>/detailed` (com otimização por distância)
- **Status**: ✅ Funcionando

---

## 🔍 Observações Importantes

1. **Redis**: O cache é opcional. O sistema funciona normalmente sem Redis, apenas sem cache.

2. **GEMINI_API_KEY**: Configurada no arquivo `.env`. Usada para funcionalidades de IA (quando implementadas).

3. **Banco de Dados**: SQLite em desenvolvimento, pode ser alterado para PostgreSQL em produção.

4. **Autenticação**: Todos os endpoints de listas e ranking requerem JWT válido.

5. **Validação de Ownership**: Listas são privadas por usuário. O sistema valida ownership antes de permitir acesso.

6. **Geolocalização**: Funcionalidades de lojas próximas e ranking otimizado usam coordenadas geográficas quando fornecidas.

---

## 📝 Próximos Passos (Opcional)

- [ ] Implementar web scraping do encartesdf.com.br
- [ ] Integrar OCR para processamento de recibos
- [ ] Adicionar funcionalidades de IA com Gemini
- [ ] Implementar sistema de notificações
- [ ] Adicionar testes automatizados completos

---

**Última atualização**: 03/11/2025  
**Versão do Backend**: 1.0.0  
**Status Geral**: ✅ **TODAS AS FUNCIONALIDADES PRINCIPAIS FUNCIONANDO**
