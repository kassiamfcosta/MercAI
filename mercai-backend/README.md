# MercAI Backend

Backend Flask para o aplicativo MercAI - Comparação de preços de supermercados com IA.

## 📋 Pré-requisitos

- Python 3.11
- PostgreSQL (Supabase) ou SQLite para desenvolvimento
- Redis (Upstash) ou local para desenvolvimento
- Google Gemini API Key
- Tesseract OCR instalado no sistema (para OCR)
- Git

## 🚀 Setup

### 1. Clonar o repositório

```bash
git clone <repo-url>
cd mercai-backend
```

### 2. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
- `DATABASE_URL`: URL de conexão do Supabase PostgreSQL (ou `sqlite:///test.db` para desenvolvimento)
- `REDIS_URL`: URL de conexão do Redis (Upstash) - opcional para desenvolvimento
- `GEMINI_API_KEY`: Chave da API do Google Gemini
- `JWT_SECRET_KEY`: Chave secreta para JWT (gere uma chave forte)
- `SECRET_KEY`: Chave secreta do Flask (gere uma chave forte)

### 5. Inicializar banco de dados

```bash
python -c "from src.config.database import init_db; init_db()"
```

### 6. Executar aplicação

```bash
# Desenvolvimento
python main.py

# Produção (com gunicorn)
gunicorn main:app --workers 2 --bind 0.0.0.0:5000
```

## 📚 Estrutura do Projeto

```
mercai-backend/
├── src/
│   ├── api/              # Endpoints Flask (Blueprints)
│   │   ├── auth.py        # Autenticação
│   │   ├── products.py    # Busca de produtos
│   │   ├── lists.py       # CRUD de listas
│   │   └── ranking.py     # Geração de ranking
│   ├── services/          # Lógica de negócio com Design Patterns
│   │   ├── scraper.py     # Web scraping
│   │   ├── ocr_processor.py # OCR
│   │   ├── ai.py          # Integração com Gemini
│   │   ├── ranking.py     # Algoritmo de scoring
│   │   ├── geo.py         # Geolocalização
│   │   └── cache.py       # Redis wrapper
│   ├── models/            # Entidades SQLAlchemy
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── store.py
│   │   ├── offer.py
│   │   ├── shopping_list.py
│   │   └── list_item.py
│   ├── factories/         # Factory Pattern
│   ├── strategies/         # Strategy Pattern
│   ├── facades/           # Facade Pattern
│   ├── config/            # Configurações
│   │   ├── settings.py
│   │   └── database.py
│   ├── utils/             # Helpers
│   │   ├── jwt.py
│   │   └── uuid_type.py
│   └── schemas/           # Marshmallow schemas
│       └── auth_schema.py
├── tests/                 # Testes
│   ├── unit/
│   └── integration/
├── main.py                # Entry point
└── requirements.txt       # Dependências
```

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação. Inclua o token no header:

```
Authorization: Bearer <token>
```

## 📖 API Endpoints

### Autenticação

#### POST /api/auth/register
Registra um novo usuário.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "senha123",
  "name": "Nome do Usuário"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Usuário registrado com sucesso",
  "data": {
    "user": {...},
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'
```

#### POST /api/auth/login
Faz login e retorna token JWT.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Login bem-sucedido",
  "data": {
    "user": {...},
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### GET /api/auth/me
Retorna dados do usuário logado.

**Headers:**
```
Authorization: Bearer <token>
```

**Exemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

### Produtos

#### GET /api/products/search
Busca produtos por nome e categoria.

**Query Parameters:**
- `q`: Termo de busca (obrigatório, mínimo 3 caracteres)
- `category`: Categoria para filtrar (opcional)
- `page`: Número da página (padrão: 1)
- `per_page`: Itens por página (padrão: 20, máximo: 50)

**Exemplo cURL:**
```bash
curl "http://localhost:5000/api/products/search?q=arroz&category=alimentos&page=1&per_page=20"
```

**Resposta:**
```json
{
  "success": true,
  "message": "Busca realizada com sucesso",
  "data": {
    "products": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 50,
      "pages": 3
    }
  }
}
```

#### GET /api/products/:id
Retorna detalhes de um produto específico com ofertas atuais.

**Exemplo cURL:**
```bash
curl http://localhost:5000/api/products/1
```

#### GET /api/products/:id/offers
Retorna todas as ofertas de um produto.

**Query Parameters:**
- `sort`: Ordenação (`price_asc`, `price_desc`, `score`) - padrão: `price_asc`
- `in_stock_only`: Filtrar apenas em estoque (padrão: `true`)

**Exemplo cURL:**
```bash
curl "http://localhost:5000/api/products/1/offers?sort=price_asc&in_stock_only=true"
```

---

### Listas de Compras

#### POST /api/lists
Cria uma nova lista de compras.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "name": "Compras do Mês",
  "latitude": -15.7942,
  "longitude": -47.8822
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/lists \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Compras do Mês",
    "latitude": -15.7942,
    "longitude": -47.8822
  }'
```

#### GET /api/lists
Lista todas as listas do usuário logado.

**Exemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/lists \
  -H "Authorization: Bearer SEU_TOKEN"
```

#### GET /api/lists/:id
Retorna detalhes de uma lista específica com itens.

**Exemplo cURL:**
```bash
curl -X GET http://localhost:5000/api/lists/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer SEU_TOKEN"
```

#### PUT /api/lists/:id
Atualiza uma lista de compras.

**Body:**
```json
{
  "name": "Novo Nome",
  "latitude": -15.7942,
  "longitude": -47.8822
}
```

#### DELETE /api/lists/:id
Deleta uma lista (cascade: deleta itens também).

#### POST /api/lists/:id/items
Adiciona um item à lista.

**Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/lists/123e4567-e89b-12d3-a456-426614174000/items \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

#### DELETE /api/lists/:id/items/:item_id
Remove um item da lista.

#### PUT /api/lists/:id/items/:item_id
Atualiza a quantidade de um item.

**Body:**
```json
{
  "quantity": 3
}
```

---

### Ranking

#### GET /api/ranking?list_id=xxx
Gera ranking básico para uma lista de compras.

**Query Parameters:**
- `list_id`: UUID da lista (obrigatório)
- `latitude`: Latitude do usuário (opcional)
- `longitude`: Longitude do usuário (opcional)

**Exemplo cURL:**
```bash
curl "http://localhost:5000/api/ranking?list_id=123e4567-e89b-12d3-a456-426614174000&latitude=-15.7942&longitude=-47.8822" \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta:**
```json
{
  "success": true,
  "message": "Ranking gerado com sucesso",
  "data": {
    "list_id": "123e4567-e89b-12d3-a456-426614174000",
    "items": [
      {
        "product": {...},
        "quantity": 2,
        "best_offer": {
          "store": {...},
          "price": 12.99,
          "score": 95.5
        },
        "all_offers": [...]
      }
    ],
    "best_combination": {
      "recommended_store": "Loja X",
      "estimated_total": 145.80,
      "total_savings": 32.50
    }
  }
}
```

#### GET /api/ranking/:list_id/detailed
Gera ranking detalhado com economia total.

**Query Parameters:**
- `latitude`: Latitude do usuário (opcional)
- `longitude`: Longitude do usuário (opcional)

**Exemplo cURL:**
```bash
curl "http://localhost:5000/api/ranking/123e4567-e89b-12d3-a456-426614174000/detailed?latitude=-15.7942&longitude=-47.8822" \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## 🧮 Modelos de Dados

### User
- `id`: UUID (primary key)
- `email`: String (único)
- `password_hash`: String (bcrypt)
- `name`: String (opcional)
- `created_at`: DateTime
- `updated_at`: DateTime

### Product
- `id`: Integer (primary key)
- `name`: String
- `category`: String (opcional)
- `brand`: String (opcional)
- `image_url`: String (opcional)
- `created_at`: DateTime

### Store
- `id`: Integer (primary key)
- `name`: String
- `url`: String (opcional)
- `logo_url`: String (opcional)
- `latitude`: Decimal (opcional)
- `longitude`: Decimal (opcional)
- `address`: Text (opcional)
- `phone`: String (opcional)
- `created_at`: DateTime

### Offer
- `id`: Integer (primary key)
- `product_id`: FK -> Product
- `store_id`: FK -> Store
- `price`: Decimal (não nulo)
- `original_price`: Decimal (opcional)
- `discount_percentage`: Decimal (opcional)
- `in_stock`: Boolean (padrão: True)
- `valid_until`: Date (opcional)
- `scraped_at`: DateTime

### ShoppingList
- `id`: UUID (primary key)
- `user_id`: FK -> User
- `name`: String (opcional)
- `latitude`: Decimal (opcional)
- `longitude`: Decimal (opcional)
- `created_at`: DateTime
- `updated_at`: DateTime

### ListItem
- `id`: Integer (primary key)
- `list_id`: FK -> ShoppingList (cascade delete)
- `product_id`: FK -> Product
- `quantity`: Integer (padrão: 1)
- `added_at`: DateTime

---

## 🎯 Algoritmo de Ranking

O algoritmo de ranking calcula um score de 0 a 100 para cada oferta usando os seguintes pesos:

### Pesos do Score

1. **Preço (40%)**
   - Quanto menor o preço, maior o score
   - Normalizado baseado no preço máximo encontrado

2. **Desconto (30%)**
   - Percentual de desconto em relação ao preço original
   - Máximo de 50% de desconto = 30 pontos

3. **Disponibilidade (20%)**
   - 20 pontos se estiver em estoque
   - 0 pontos se fora de estoque

4. **Proximidade (10%)**
   - Quanto mais próximo da localização do usuário, maior o score
   - Score linear de 10 pontos (distância 0) a 0 pontos (distância >= 20km)

### Cálculo do Score

```python
score = 0

# 1. Preço (40 pontos)
price_score = (1 - (price / max_price)) * 40
score += price_score

# 2. Desconto (30 pontos)
discount_score = min((discount_percentage / 50.0), 1.0) * 30
score += discount_score

# 3. Disponibilidade (20 pontos)
if in_stock:
    score += 20

# 4. Proximidade (10 pontos)
if user_location:
    distance_km = calculate_distance(...)
    proximity_score = max(0, 10 - (distance_km / 20.0) * 10)
    score += proximity_score

return round(score, 2)
```

### Otimização de Combinação de Lojas

O algoritmo também calcula a melhor combinação de lojas para minimizar o custo total da lista, considerando:
- Custo total estimado por loja
- Economia total (descontos)
- Número de itens disponíveis em cada loja

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/unit/test_auth.py -v

# Com cobertura
pytest tests/unit/test_auth.py --cov=src --cov-report=html
```

---

## 🚢 Deploy

### Render.com

O projeto está preparado para deploy no Render.com. Ver instruções em `render.yaml` e `Procfile`.

**Arquivos de deploy:**
- `render.yaml`: Configuração do serviço
- `Procfile`: Comando gunicorn
- `runtime.txt`: Versão Python

**Variáveis de ambiente no Render:**
- `DATABASE_URL`
- `REDIS_URL`
- `GEMINI_API_KEY`
- `JWT_SECRET_KEY`
- `SECRET_KEY`
- `FLASK_ENV=production`

---

## 📝 Licença

Educational Project
