# Guia de Prompts para Desenvolvimento do MercAI no Cursor

**Data:** 01/11/2025  
**Projeto:** MercAI - MVP Backend  
**Ordem de Execução:** Seguir numeração sequencial

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:
- [ ] Python 3.11 instalado
- [ ] Node.js 18+ instalado (para o frontend depois)
- [ ] Git instalado
- [ ] Conta no GitHub
- [ ] Conta no Supabase (gratuita)
- [ ] Conta no Render.com (gratuita)
- [ ] VS Code ou Cursor instalado

---

## 🎯 FASE 1: Setup Inicial do Projeto Backend

### Prompt 1: Criar Estrutura do Projeto

```
Você é um arquiteto de software Python sênior, especialista em Flask e arquitetura modular.

TAREFA: Criar a estrutura completa de um projeto Flask para o backend do MercAI.

CONTEXTO:
O MercAI é um app de comparação de preços de supermercados. O backend precisa:
- API REST para o app mobile
- Web scraping de encartes de supermercados
- Processamento com IA (Gemini Flash)
- Banco PostgreSQL (Supabase)
- Cache com Redis (Upstash)

ESTRUTURA DESEJADA:
/mercai-backend
├── /src
│   ├── /api              # Endpoints Flask
│   │   ├── __init__.py
│   │   ├── auth.py       # Login, cadastro
│   │   ├── products.py   # Busca de produtos
│   │   ├── lists.py      # CRUD de listas
│   │   └── ranking.py    # Geração de ranking
│   ├── /services         # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── scraper.py    # Web scraping
│   │   ├── ranking.py    # Algoritmo de scoring
│   │   ├── ai.py         # Integração com Gemini
│   │   └── cache.py      # Redis wrapper
│   ├── /models           # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── store.py
│   │   ├── shopping_list.py
│   │   └── offer.py
│   ├── /utils            # Helpers
│   │   ├── __init__.py
│   │   ├── jwt.py        # Token helpers
│   │   └── validators.py # Validações
│   ├── /config           # Configurações
│   │   ├── __init__.py
│   │   ├── settings.py   # Variáveis de ambiente
│   │   └── database.py   # Conexão DB
│   └── /schemas          # Marshmallow schemas
│       └── __init__.py
├── /tests
│   ├── /unit
│   └── /integration
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py               # Entry point

AÇÃO:
1. Crie toda a estrutura de pastas e arquivos
2. Cada __init__.py deve estar presente
3. Adicione comentários explicativos em cada arquivo
4. Crie o .gitignore apropriado para Python
5. Crie o .env.example com as variáveis necessárias
6. Crie o requirements.txt com as dependências iniciais
7. Crie o main.py com a inicialização básica do Flask
8. Crie o README.md com instruções de setup

DEPENDÊNCIAS INICIAIS (requirements.txt):
- Flask==3.0.0
- Flask-CORS==4.0.0
- python-dotenv==1.0.0
- SQLAlchemy==2.0.23
- psycopg2-binary==2.9.9
- PyJWT==2.8.0
- bcrypt==4.1.1
- marshmallow==3.20.1
- requests==2.31.0
- beautifulsoup4==4.12.2
- redis==5.0.1
- google-generativeai==0.3.1
- gunicorn==21.2.0

IMPORTANTE:
- Use type hints em todas as funções
- Adicione docstrings em todos os módulos
- Siga PEP 8
- Prepare para ambiente de produção
```

---

### Prompt 2: Configurar Variáveis de Ambiente

```
Você é um especialista em segurança e configuração de aplicações Python.

TAREFA: Criar o sistema de configuração com variáveis de ambiente.

ARQUIVOS A CRIAR/EDITAR:
1. .env.example (template)
2. src/config/settings.py (carregamento de configs)

CONTEÚDO DO .env.example:
# Aplicação
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Banco de Dados (Supabase PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Redis (Upstash)
REDIS_URL=redis://default:password@host:6379

# IA (Google Gemini)
GEMINI_API_KEY=your-gemini-api-key

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_HOURS=24

# Scraping
USER_AGENT=MercAI/1.0 (Educational Project)
SCRAPING_DELAY_MIN=1
SCRAPING_DELAY_MAX=3

CONTEÚDO DO src/config/settings.py:
- Carregar variáveis com python-dotenv
- Validar variáveis obrigatórias
- Criar classe Settings com todas as configs
- Adicionar método para verificar se está em produção

IMPORTANTE:
- Nunca commitar o arquivo .env real
- Validar todas as variáveis obrigatórias no startup
- Usar valores padrão seguros quando apropriado
```

---

### Prompt 3: Criar Conexão com Banco de Dados

```
Você é um especialista em SQLAlchemy e bancos de dados PostgreSQL.

TAREFA: Configurar a conexão com o banco de dados PostgreSQL (Supabase).

ARQUIVO: src/config/database.py

REQUISITOS:
1. Criar engine do SQLAlchemy
2. Criar session factory
3. Criar Base para os models
4. Adicionar função init_db() para criar tabelas
5. Adicionar função get_db() para dependency injection
6. Configurar pool de conexões
7. Adicionar tratamento de erros

EXEMPLO DE USO:
```python
from src.config.database import get_db

def some_function():
    db = next(get_db())
    try:
        # usar db
        pass
    finally:
        db.close()
```

IMPORTANTE:
- Usar context manager para sessões
- Configurar pool_size e max_overflow
- Adicionar logging de queries em desenvolvimento
- Preparar para migrations com Alembic (futuro)
```

---

## 🎯 FASE 2: Modelos de Dados (SQLAlchemy)

### Prompt 4: Criar Model de Usuário

```
Você é um especialista em modelagem de dados e segurança.

TAREFA: Criar o model User com autenticação segura.

ARQUIVO: src/models/user.py

CAMPOS:
- id: UUID (primary key)
- email: String(255), unique, not null
- password_hash: String(255), not null
- name: String(100)
- created_at: DateTime, default now
- updated_at: DateTime, onupdate now

MÉTODOS:
- set_password(password): Hash da senha com bcrypt
- check_password(password): Verificar senha
- to_dict(): Serializar (sem senha!)
- generate_token(): Gerar JWT

IMPORTANTE:
- NUNCA retornar password_hash em to_dict()
- Usar bcrypt com salt rounds = 12
- Validar formato de email
- JWT deve conter: user_id, email, exp
```

---

### Prompt 5: Criar Models de Produtos e Lojas

```
Você é um especialista em modelagem de dados para e-commerce.

TAREFA: Criar os models Store, Product e Offer.

ARQUIVOS:
1. src/models/store.py
2. src/models/product.py
3. src/models/offer.py

MODEL Store:
- id: Integer (primary key)
- name: String(100), not null
- url: String(255)
- logo_url: String(255)
- latitude: Decimal(10, 8)
- longitude: Decimal(11, 8)
- address: Text
- phone: String(20)
- created_at: DateTime

MODEL Product:
- id: Integer (primary key)
- name: String(255), not null
- category: String(50)
- brand: String(100)
- image_url: String(255)
- created_at: DateTime

MODEL Offer:
- id: Integer (primary key)
- product_id: FK -> Product
- store_id: FK -> Store
- price: Decimal(10, 2), not null
- original_price: Decimal(10, 2)
- discount_percentage: Decimal(5, 2)
- in_stock: Boolean, default True
- valid_until: Date
- scraped_at: DateTime, default now
- UNIQUE constraint (product_id, store_id)

RELACIONAMENTOS:
- Offer.product -> Product
- Offer.store -> Store

ÍNDICES:
- idx_offers_product (product_id)
- idx_offers_store (store_id)
- idx_offers_scraped (scraped_at)

IMPORTANTE:
- Adicionar método to_dict() em todos
- Adicionar validações de preço (> 0)
- Calcular discount_percentage automaticamente
```

---

### Prompt 6: Criar Models de Lista de Compras

```
Você é um especialista em modelagem de dados.

TAREFA: Criar os models ShoppingList e ListItem.

ARQUIVOS:
1. src/models/shopping_list.py
2. src/models/list_item.py

MODEL ShoppingList:
- id: UUID (primary key)
- user_id: FK -> User
- name: String(100)
- latitude: Decimal(10, 8)
- longitude: Decimal(11, 8)
- created_at: DateTime
- updated_at: DateTime

MODEL ListItem:
- id: Integer (primary key)
- list_id: FK -> ShoppingList (cascade delete)
- product_id: FK -> Product
- quantity: Integer, default 1
- added_at: DateTime

RELACIONAMENTOS:
- ShoppingList.user -> User
- ShoppingList.items -> List[ListItem]
- ListItem.list -> ShoppingList
- ListItem.product -> Product

MÉTODOS:
- ShoppingList.calculate_total(): Calcular total estimado
- ShoppingList.get_best_stores(): Retornar melhores lojas

IMPORTANTE:
- Cascade delete nos itens quando lista é deletada
- Validar quantity > 0
- Adicionar índice em user_id
```

---

## 🎯 FASE 3: Autenticação e API Básica

### Prompt 7: Criar Sistema de JWT

```
Você é um especialista em segurança e autenticação JWT.

TAREFA: Criar utilitários para JWT.

ARQUIVO: src/utils/jwt.py

FUNÇÕES:
1. generate_token(user_id: str, email: str) -> str
   - Criar JWT com payload: {user_id, email, exp}
   - Expiração configurável (padrão 24h)

2. decode_token(token: str) -> dict
   - Decodificar e validar JWT
   - Retornar payload ou None se inválido
   - Tratar expiração

3. token_required (decorator)
   - Decorator para proteger rotas
   - Extrair token do header Authorization
   - Validar e adicionar user_id ao request

EXEMPLO DE USO:
```python
from src.utils.jwt import token_required

@app.route('/api/protected')
@token_required
def protected_route(current_user_id):
    return {"user_id": current_user_id}
```

IMPORTANTE:
- Usar algoritmo HS256
- Tratar todos os erros (token inválido, expirado, etc.)
- Logging de tentativas de acesso inválidas
```

---

### Prompt 8: Criar Endpoints de Autenticação

```
Você é um especialista em APIs REST e autenticação.

TAREFA: Criar endpoints de registro e login.

ARQUIVO: src/api/auth.py

ENDPOINTS:

1. POST /api/auth/register
   - Body: {email, password, name}
   - Validar email único
   - Validar senha (mín 8 caracteres)
   - Criar usuário
   - Retornar token JWT

2. POST /api/auth/login
   - Body: {email, password}
   - Validar credenciais
   - Retornar token JWT

3. GET /api/auth/me
   - Header: Authorization: Bearer <token>
   - Retornar dados do usuário logado

VALIDAÇÕES:
- Email: formato válido, único
- Senha: mínimo 8 caracteres, pelo menos 1 número
- Nome: opcional, máximo 100 caracteres

RESPOSTAS:
- 200: Sucesso
- 400: Validação falhou
- 401: Credenciais inválidas
- 409: Email já existe
- 500: Erro interno

IMPORTANTE:
- Usar marshmallow para validação
- Retornar mensagens de erro claras
- Nunca retornar password_hash
- Logging de tentativas de login
```

---

### Prompt 9: Configurar CORS e Main

```
Você é um especialista em Flask e configuração de APIs.

TAREFA: Configurar o arquivo main.py com Flask e CORS.

ARQUIVO: main.py

REQUISITOS:
1. Inicializar Flask app
2. Configurar CORS para aceitar requests do mobile
3. Registrar blueprints (auth, products, lists, ranking)
4. Adicionar endpoint /health para monitoramento
5. Adicionar tratamento global de erros
6. Configurar logging
7. Inicializar banco de dados

ENDPOINTS BÁSICOS:
- GET /health -> {status: "healthy", timestamp: "..."}
- GET / -> Redirect para /health

TRATAMENTO DE ERROS:
- 404: Not Found
- 500: Internal Server Error
- Logging de todos os erros

IMPORTANTE:
- CORS deve permitir origens específicas em produção
- Logging estruturado (JSON)
- Graceful shutdown
```

---

## 🎯 FASE 4: Web Scraping

### Prompt 10: Criar Scraper do encartesdf.com.br

```
Você é um especialista em web scraping ético e responsável.

TAREFA: Criar scraper para o site encartesdf.com.br.

ARQUIVO: src/services/scraper.py

CLASSE: EncartesDFScraper

MÉTODOS:

1. get_latest_encartes(limit=10) -> List[dict]
   - Buscar últimos encartes da home
   - Retornar: [{title, url, date, store_name}]

2. get_encarte_images(encarte_url) -> List[str]
   - Extrair URLs das imagens de um encarte
   - Retornar lista de URLs

3. download_image(image_url, save_path) -> str
   - Baixar imagem
   - Salvar localmente
   - Retornar caminho do arquivo

BOAS PRÁTICAS:
- User-Agent: "MercAI/1.0 (Educational Project)"
- Rate limiting: 1-3 segundos entre requests
- Retry em caso de erro (máx 3 tentativas)
- Timeout de 10 segundos
- Logging de todas as operações
- Tratamento de erros (404, timeout, etc.)

IMPORTANTE:
- Respeitar robots.txt
- Não sobrecarregar o servidor
- Cache de resultados (Redis)
- Executar em horários de baixo tráfego
```

---

### Prompt 11: Criar Processador de Imagens com OCR

```
Você é um especialista em OCR e processamento de imagens.

TAREFA: Criar processador de imagens de encartes com OCR.

ARQUIVO: src/services/ocr_processor.py

CLASSE: OCRProcessor

MÉTODOS:

1. extract_text_from_image(image_path) -> str
   - Usar Tesseract OCR
   - Idioma: português
   - Pré-processamento da imagem (contraste, binarização)
   - Retornar texto extraído

2. extract_text_from_url(image_url) -> str
   - Baixar imagem da URL
   - Extrair texto
   - Retornar texto

PRÉ-PROCESSAMENTO:
- Converter para escala de cinza
- Aumentar contraste
- Binarização (threshold)
- Remover ruído

IMPORTANTE:
- Instalar: pip install pytesseract pillow
- Tesseract deve estar instalado no sistema
- Tratar imagens de baixa qualidade
- Logging de erros de OCR
```

---

### Prompt 12: Criar Estruturador com IA (Gemini)

```
Você é um especialista em integração com LLMs e processamento de dados.

TAREFA: Criar serviço de estruturação de dados com Gemini Flash.

ARQUIVO: src/services/ai.py

CLASSE: AIService

MÉTODOS:

1. structure_encarte_data(ocr_text, store_name, valid_until) -> dict
   - Enviar texto para Gemini Flash
   - Prompt: extrair produtos, preços, marcas, pesos
   - Retornar JSON estruturado

2. categorize_product(product_name) -> str
   - Categorizar produto automaticamente
   - Categorias: Alimentos, Bebidas, Limpeza, Higiene, etc.

3. clean_and_parse_json(raw_response) -> dict
   - Limpar markdown (```json)
   - Fazer parse do JSON
   - Validar estrutura

PROMPT PARA ESTRUTURAÇÃO:
```
Você é um extrator de dados de encartes de supermercado.

Supermercado: {store_name}
Validade: {valid_until}

Texto extraído:
{ocr_text}

Extraia TODOS os produtos com preços e retorne JSON:
{
  "products": [
    {
      "name": "Nome completo",
      "brand": "Marca",
      "weight": "5kg",
      "price": 12.99,
      "original_price": 15.99,
      "discount_percentage": 20
    }
  ]
}

REGRAS:
- Apenas produtos com preços visíveis
- Preços em formato decimal
- Se não houver desconto, omitir campos
```

IMPORTANTE:
- Usar modelo gemini-1.5-flash
- Tratar erros de API (rate limit, timeout)
- Validar JSON retornado
- Logging de todas as chamadas
```

---

## 🎯 FASE 5: Algoritmo de Ranking

### Prompt 13: Criar Serviço de Ranking

```
Você é um especialista em algoritmos e otimização.

TAREFA: Criar o algoritmo de ranking de ofertas.

ARQUIVO: src/services/ranking.py

FUNÇÕES:

1. calculate_offer_score(offer: dict, user_location: dict = None) -> float
   - Calcular score de 0-100
   - Pesos:
     * Preço: 40%
     * Desconto: 30%
     * Disponibilidade: 20%
     * Proximidade: 10% (opcional)
   - Retornar score

2. generate_ranking(shopping_list_id: str, user_location: dict = None) -> dict
   - Buscar itens da lista
   - Para cada produto, buscar ofertas
   - Calcular score de cada oferta
   - Ordenar por score
   - Retornar ranking completo

3. optimize_store_combination(ranking: list) -> dict
   - Encontrar melhor combinação de lojas
   - Minimizar custo total
   - Considerar número de lojas diferentes
   - Retornar recomendação

CÁLCULO DE SCORE:
```python
score = 0

# 1. Preço (40 pontos)
price_score = (1 - (price / max_price)) * 40
score += price_score

# 2. Desconto (30 pontos)
score += (discount_percentage / 100) * 30

# 3. Disponibilidade (20 pontos)
if in_stock:
    score += 20

# 4. Proximidade (10 pontos)
if user_location:
    distance_km = calculate_distance(...)
    proximity_score = max(0, 10 - (distance_km / 2))
    score += proximity_score

return round(score, 2)
```

IMPORTANTE:
- Normalizar preços corretamente
- Tratar casos sem ofertas
- Cache de rankings (Redis, TTL 1h)
- Logging de cálculos
```

---

### Prompt 14: Criar Serviço de Geolocalização

```
Você é um especialista em geolocalização e cálculos geográficos.

TAREFA: Criar serviço de geolocalização.

ARQUIVO: src/services/geo.py

FUNÇÕES:

1. geocode_address(address: str) -> dict
   - Usar Nominatim (OpenStreetMap)
   - Retornar {lat, lon}
   - Cache de resultados

2. calculate_distance(lat1, lon1, lat2, lon2) -> float
   - Fórmula de Haversine
   - Retornar distância em km
   - Precisão de 2 casas decimais

3. find_nearest_stores(user_location: dict, stores: list, max_distance: float = 20) -> list
   - Filtrar lojas dentro do raio
   - Ordenar por distância
   - Retornar lista de lojas

FÓRMULA DE HAVERSINE:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return round(km, 2)
```

IMPORTANTE:
- User-Agent para Nominatim
- Rate limiting (1 req/segundo)
- Cache de geocoding (Redis)
- Tratamento de endereços não encontrados
```

---

## 🎯 FASE 6: Endpoints da API

### Prompt 15: Criar Endpoints de Produtos

```
Você é um especialista em APIs REST.

TAREFA: Criar endpoints de busca de produtos.

ARQUIVO: src/api/products.py

ENDPOINTS:

1. GET /api/products/search?q=arroz&category=alimentos
   - Buscar produtos por nome
   - Filtrar por categoria (opcional)
   - Paginação (page, per_page)
   - Retornar: {products: [...], total, page, pages}

2. GET /api/products/:id
   - Retornar detalhes de um produto
   - Incluir ofertas atuais

3. GET /api/products/:id/offers
   - Retornar todas as ofertas de um produto
   - Ordenar por preço
   - Incluir informações da loja

VALIDAÇÕES:
- Query mínima: 3 caracteres
- Per_page: máximo 50
- Category: valores válidos

IMPORTANTE:
- Cache de buscas populares
- Full-text search no banco
- Retornar imagem do produto
```

---

### Prompt 16: Criar Endpoints de Listas

```
Você é um especialista em APIs REST e CRUD.

TAREFA: Criar endpoints de listas de compras.

ARQUIVO: src/api/lists.py

ENDPOINTS:

1. POST /api/lists
   - Body: {name, latitude, longitude}
   - Criar lista vazia
   - Retornar lista criada

2. GET /api/lists
   - Listar todas as listas do usuário
   - Ordenar por created_at desc

3. GET /api/lists/:id
   - Retornar detalhes da lista
   - Incluir itens

4. PUT /api/lists/:id
   - Atualizar nome ou localização

5. DELETE /api/lists/:id
   - Deletar lista (cascade items)

6. POST /api/lists/:id/items
   - Body: {product_id, quantity}
   - Adicionar item à lista

7. DELETE /api/lists/:id/items/:item_id
   - Remover item da lista

8. PUT /api/lists/:id/items/:item_id
   - Atualizar quantidade

VALIDAÇÕES:
- Usuário só pode acessar suas próprias listas
- Quantity > 0
- Product_id deve existir

IMPORTANTE:
- Todas as rotas protegidas com JWT
- Validar ownership da lista
- Retornar 404 se não encontrado
```

---

### Prompt 17: Criar Endpoints de Ranking

```
Você é um especialista em APIs REST e algoritmos.

TAREFA: Criar endpoints de geração de ranking.

ARQUIVO: src/api/ranking.py

ENDPOINTS:

1. GET /api/ranking?list_id=xxx
   - Gerar ranking para uma lista
   - Retornar melhores ofertas por produto
   - Incluir recomendação de loja

2. GET /api/ranking/:list_id/detailed
   - Ranking detalhado
   - Todas as ofertas por produto (top 5)
   - Cálculo de economia total

RESPOSTA:
```json
{
  "list_id": "uuid",
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
    "total_savings": 32.50,
    "alternatives": [...]
  }
}
```

IMPORTANTE:
- Cache de rankings (1 hora)
- Processar de forma assíncrona se > 20 itens
- Incluir tempo de processamento
- Logging de rankings gerados
```

---

## 🎯 FASE 7: Cache e Performance

### Prompt 18: Criar Wrapper do Redis

```
Você é um especialista em cache e performance.

TAREFA: Criar wrapper para Redis com funções úteis.

ARQUIVO: src/services/cache.py

CLASSE: CacheService

MÉTODOS:

1. get(key: str) -> any
   - Buscar valor no cache
   - Deserializar JSON
   - Retornar None se não existir

2. set(key: str, value: any, ttl: int = 3600)
   - Salvar valor no cache
   - Serializar para JSON
   - TTL em segundos

3. delete(key: str)
   - Remover chave do cache

4. exists(key: str) -> bool
   - Verificar se chave existe

5. invalidate_pattern(pattern: str)
   - Invalidar múltiplas chaves
   - Ex: invalidate_pattern("ranking:*")

DECORATORS:

1. @cached(ttl=3600, key_prefix="")
   - Decorator para cachear funções
   - Gerar chave automaticamente
   - Exemplo:
   ```python
   @cached(ttl=3600, key_prefix="product")
   def get_product(product_id):
       # ...
   ```

IMPORTANTE:
- Tratar erros de conexão
- Logging de hits/misses
- Serialização segura (JSON)
- Namespace por tipo de dado
```

---

## 🎯 FASE 8: Testes e Documentação

### Prompt 19: Criar Testes Unitários

```
Você é um especialista em testes automatizados com pytest.

TAREFA: Criar testes unitários para as principais funções.

ARQUIVOS:
- tests/unit/test_auth.py
- tests/unit/test_ranking.py
- tests/unit/test_geo.py

TESTES PARA AUTH:
- test_register_user_success
- test_register_duplicate_email
- test_login_success
- test_login_invalid_credentials
- test_generate_token
- test_decode_token

TESTES PARA RANKING:
- test_calculate_offer_score
- test_calculate_offer_score_with_location
- test_generate_ranking
- test_optimize_store_combination

TESTES PARA GEO:
- test_haversine_distance
- test_geocode_address
- test_find_nearest_stores

IMPORTANTE:
- Usar fixtures para dados de teste
- Mock de APIs externas (Gemini, Nominatim)
- Cobertura mínima: 80%
- Testes rápidos (< 1s cada)
```

---

### Prompt 20: Criar Documentação da API

```
Você é um especialista em documentação técnica.

TAREFA: Criar documentação completa da API no README.md.

SEÇÕES:

1. Visão Geral
   - O que é o MercAI
   - Arquitetura

2. Setup
   - Pré-requisitos
   - Instalação
   - Configuração (.env)
   - Executar localmente

3. Endpoints
   - Autenticação
   - Produtos
   - Listas
   - Ranking

4. Modelos de Dados
   - User
   - Product
   - Store
   - Offer
   - ShoppingList

5. Algoritmo de Ranking
   - Como funciona
   - Pesos
   - Exemplos

6. Deploy
   - Render.com
   - Variáveis de ambiente
   - Monitoramento

FORMATO:
- Markdown
- Exemplos de curl para cada endpoint
- Códigos de resposta
- Exemplos de JSON

IMPORTANTE:
- Linguagem clara e objetiva
- Exemplos práticos
- Troubleshooting comum
```

---

## 🎯 FASE 9: Deploy

### Prompt 21: Preparar para Deploy no Render.com

```
Você é um especialista em DevOps e deploy de aplicações Python.

TAREFA: Preparar o projeto para deploy no Render.com.

ARQUIVOS A CRIAR:

1. render.yaml
```yaml
services:
  - type: web
    name: mercai-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        sync: false
      - key: REDIS_URL
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: JWT_SECRET_KEY
        sync: false
```

2. Procfile
```
web: gunicorn main:app --workers 2 --bind 0.0.0.0:$PORT
```

3. runtime.txt
```
python-3.11.0
```

AJUSTES NO main.py:
- Usar PORT do ambiente
- Configurar workers do gunicorn
- Desabilitar debug em produção

CHECKLIST:
- [ ] requirements.txt atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados criado no Supabase
- [ ] Redis criado no Upstash
- [ ] API key do Gemini obtida
- [ ] .gitignore correto

IMPORTANTE:
- Testar localmente com gunicorn antes
- Configurar CORS para domínio de produção
- Habilitar HTTPS
- Configurar health check
```

---

## 📚 Resumo da Ordem de Execução

Execute os prompts nesta ordem:

**FASE 1: Setup (Prompts 1-3)**
1. Estrutura do projeto
2. Variáveis de ambiente
3. Conexão com banco

**FASE 2: Models (Prompts 4-6)**
4. Model User
5. Models Product, Store, Offer
6. Models ShoppingList, ListItem

**FASE 3: Auth (Prompts 7-9)**
7. Sistema JWT
8. Endpoints de autenticação
9. Configurar Flask e CORS

**FASE 4: Scraping (Prompts 10-12)**
10. Scraper encartesdf
11. OCR Processor
12. IA Estruturador

**FASE 5: Ranking (Prompts 13-14)**
13. Algoritmo de ranking
14. Geolocalização

**FASE 6: API (Prompts 15-17)**
15. Endpoints de produtos
16. Endpoints de listas
17. Endpoints de ranking

**FASE 7: Performance (Prompt 18)**
18. Cache Redis

**FASE 8: Qualidade (Prompts 19-20)**
19. Testes unitários
20. Documentação

**FASE 9: Deploy (Prompt 21)**
21. Preparar deploy

---

## 💡 Dicas para Usar no Cursor

1. **Execute um prompt por vez**
2. **Revise o código gerado** antes de prosseguir
3. **Teste cada fase** antes de avançar
4. **Faça commits frequentes** no Git
5. **Use o chat do Cursor** para ajustes e dúvidas
6. **Peça explicações** se algo não estiver claro

---

**Boa sorte com o desenvolvimento! 🚀**
