# 🛒 MercAI - Comparador de Preços Inteligente

> Aplicativo que ajuda usuários a encontrar os melhores preços e ofertas em mercados locais, comparando preços entre diferentes estabelecimentos próximos.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen.svg)](https://kassiamfcosta.github.io/MercAI/)

## 📋 Sobre o Projeto

O **MercAI** é uma aplicação completa de comparação de preços desenvolvida na disciplina de **Empreendedorismo** do curso de **Tecnologia em Sistemas para Internet (TSI)**.

O sistema permite que usuários criem listas de compras, pesquisem produtos, comparem preços entre diferentes lojas e recebam sugestões otimizadas baseadas em preço, disponibilidade e proximidade.

## 🌐 Acesso Online

- **Frontend Web**: [https://kassiamfcosta.github.io/MercAI/](https://kassiamfcosta.github.io/MercAI/) (GitHub Pages)
- **Repositório**: [https://github.com/kassiamfcosta/MercAI](https://github.com/kassiamfcosta/MercAI)

## 👥 Equipe de Desenvolvimento

- **Mayara Vieira**
- **Kássia**
- **Gabriel**
- **Ryan**
- **João**

## 🚀 Funcionalidades Principais

### ✅ Implementadas

- ✅ **Autenticação de Usuários**
  - Registro e login com JWT
  - Perfil de usuário

- ✅ **Gestão de Produtos**
  - Busca por nome e categoria
  - Detalhes de produtos
  - Visualização de ofertas por produto

- ✅ **Gestão de Lojas**
  - Listagem de lojas cadastradas
  - Busca por lojas próximas (geolocalização)
  - Detalhes e informações de cada loja

- ✅ **Listas de Compras**
  - Criação e gerenciamento de listas
  - Adição/remoção de itens
  - Listas personalizadas por usuário

- ✅ **Ranking de Ofertas**
  - Comparação automática de preços
  - Ranking por produto
  - Sugestões otimizadas considerando distância

- ✅ **Dashboard de Preços**
  - Visualização de melhores ofertas
  - Comparação entre lojas
  - Informações de disponibilidade

## 📁 Estrutura do Projeto

```
MercAI/
├── mercai-backend/          # Backend Flask (API REST)
│   ├── src/
│   │   ├── api/             # Endpoints da API
│   │   ├── models/          # Modelos de dados (SQLAlchemy)
│   │   ├── services/        # Lógica de negócio
│   │   ├── config/          # Configurações
│   │   └── utils/           # Utilitários
│   ├── tests/               # Testes automatizados
│   ├── main.py              # Entry point do servidor
│   ├── requirements.txt     # Dependências Python
│   └── README.md            # Documentação do backend
│
├── Contextro - MercAI/      # Frontend Web (HTML/CSS/JS)
│   └── Mercai_/             # Arquivos HTML estáticos
│       ├── index.html
│       ├── login.html
│       ├── cadastro.html
│       ├── inicio.html
│       ├── lista_de_compras.html
│       └── js/              # Scripts JavaScript
│
├── mercai-frontend/         # Frontend Mobile (React Native/Expo)
│   ├── src/
│   │   ├── screens/         # Telas do aplicativo
│   │   ├── services/        # Serviços de API
│   │   └── components/      # Componentes reutilizáveis
│   ├── App.js
│   └── package.json
│
└── README.md                # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **JWT** - Autenticação
- **Marshmallow** - Validação de dados
- **Redis** - Cache (opcional)
- **Google Gemini AI** - Integração com IA

### Frontend Web
- **HTML5/CSS3**
- **JavaScript (Vanilla)**
- **AJAX/Fetch** - Comunicação com API

### Frontend Mobile
- **React Native**
- **Expo**
- **AsyncStorage** - Armazenamento local

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção - suportado)

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 16+ (para frontend mobile)
- Git

### Backend

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/kassiamfcosta/MercAI.git
   cd MercAI/mercai-backend
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. **Inicialize o banco de dados:**
   ```bash
   python -c "from src.config.database import init_db; init_db()"
   ```

6. **Popule o banco com dados de exemplo (opcional):**
   ```bash
   python seed_data.py
   ```

7. **Inicie o servidor:**
   ```bash
   # Windows
   .\iniciar_servidor.bat
   
   # Linux/Mac
   python main.py
   ```

O servidor estará disponível em `http://localhost:8000`

### Frontend Web

1. **Abra o arquivo HTML no navegador:**
   ```bash
   cd "Contextro - MercAI/Mercai_"
   # Abra index.html ou login.html no navegador
   ```

2. **Ou use o servidor Flask (recomendado):**
   - O backend Flask já serve os arquivos estáticos do frontend
   - Acesse: `http://localhost:8000/login.html`

### Frontend Mobile

1. **Instale as dependências:**
   ```bash
   cd mercai-frontend
   npm install
   ```

2. **Inicie o Expo:**
   ```bash
   npm start
   # ou
   expo start
   ```

3. **Escaneie o QR code com o app Expo Go**

## 🧪 Testes

### Backend

```bash
cd mercai-backend

# Testes manuais
python test_manual.py

# Testes automáticos
python test_auto.py

# Testes completos
python test_full.py

# Testes com pytest
pytest tests/
```

## 📚 Documentação da API

A API REST completa está documentada em:

- **Postman Collection**: `mercai-backend/MercAI_API.postman_collection.json`
- **Funcionalidades**: `mercai-backend/FUNCIONALIDADES_BACKEND.md`
- **Status de Requisitos**: `STATUS_REQUISITOS.md`

### Endpoints Principais

- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Fazer login
- `GET /api/auth/me` - Dados do usuário
- `GET /api/products/search` - Buscar produtos
- `GET /api/stores/nearby` - Lojas próximas
- `POST /api/lists` - Criar lista
- `GET /api/ranking` - Gerar ranking de ofertas

Para ver todos os endpoints, consulte `FUNCIONALIDADES_BACKEND.md`.

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na pasta `mercai-backend/`:

```env
# Aplicação
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-secret-key-aqui

# Banco de Dados
DATABASE_URL=sqlite:///test.db

# Redis (opcional)
REDIS_URL=

# Google Gemini AI
GEMINI_API_KEY=sua-chave-api-aqui

# JWT
JWT_SECRET_KEY=sua-jwt-secret-key
JWT_EXPIRATION_HOURS=24

# Porta
PORT=8000
```

**⚠️ IMPORTANTE:** Nunca faça commit do arquivo `.env` no Git!

## 📊 Status do Projeto

### ✅ Funcionalidades Implementadas

- [x] Sistema de autenticação (JWT)
- [x] CRUD completo de produtos
- [x] CRUD completo de lojas
- [x] CRUD completo de listas de compras
- [x] Sistema de ranking de ofertas
- [x] Geolocalização (lojas próximas)
- [x] Cache com Redis (opcional)
- [x] Validação de dados
- [x] Paginação
- [x] Frontend Web básico
- [x] Frontend Mobile (React Native)

### 🚧 Em Desenvolvimento

- [ ] Web scraping do encartesdf.com.br
- [ ] Processamento OCR de recibos
- [ ] Integração completa com Gemini AI
- [ ] Sistema de notificações
- [ ] Testes automatizados completos

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Faça commit das suas alterações (`git commit -m 'feat: Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Commit

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Desenvolvimento

Desenvolvido como projeto acadêmico na disciplina de **Empreendedorismo** do curso **TSI** (Tecnologia em Sistemas para Internet).

---

**🎯 Objetivo:** Ajudar usuários a economizar tempo e dinheiro ao realizar compras em mercados locais, comparando preços de produtos em diferentes estabelecimentos próximos.

**📍 Localização:** Desenvolvido para o Distrito Federal (DF), Brasil

**🌐 Site de Referência:** https://encartesdf.com.br/

---

*Última atualização: Novembro 2025*
