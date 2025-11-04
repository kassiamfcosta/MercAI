# MercAI Frontend

Aplicativo React Native/Expo para o MercAI - Comparação de preços de supermercados com IA.

## 📋 Pré-requisitos

- Node.js 18+
- npm ou yarn
- Expo CLI instalado globalmente: `npm install -g expo-cli`

## 🚀 Setup

### 1. Instalar dependências

```bash
cd mercai-frontend
npm install
```

### 2. Configurar URL da API

Edite `src/services/api.js` e ajuste a `API_BASE_URL`:

```javascript
const API_BASE_URL = __DEV__ 
  ? 'http://localhost:5000/api'  // Para desenvolvimento local
  : 'https://seu-backend-render.com/api';  // Para produção
```

**Nota:** Para testar no dispositivo físico ou emulador, use o IP da sua máquina:
```javascript
const API_BASE_URL = 'http://SEU_IP_LOCAL:5000/api';
```

### 3. Executar aplicativo

```bash
# Iniciar Expo
npm start

# Executar no Android
npm run android

# Executar no iOS
npm run ios

# Executar no Web
npm run web
```

## 📱 Telas Implementadas

Baseadas nos designs do Figma:

- **SplashScreen**: Tela inicial de carregamento
- **TutorialScreen**: Tutorial de introdução com 4 páginas
- **LoginScreen**: Tela de login com gradiente verde
- **RegisterScreen**: Tela de cadastro
- **HomeScreen**: Tela principal com ações rápidas e listas
- **SearchProductsScreen**: Busca de produtos
- **ShoppingListScreen**: Gerenciamento de lista de compras
- **DashboardScreen**: Dashboard com ranking de ofertas

## 🔧 Estrutura do Projeto

```
mercai-frontend/
├── src/
│   ├── screens/         # Telas do aplicativo
│   │   ├── SplashScreen.js
│   │   ├── TutorialScreen.js
│   │   ├── LoginScreen.js
│   │   ├── RegisterScreen.js
│   │   ├── HomeScreen.js
│   │   ├── SearchProductsScreen.js
│   │   ├── ShoppingListScreen.js
│   │   └── DashboardScreen.js
│   ├── services/        # Integração com API
│   │   └── api.js       # Serviços centralizados
│   ├── components/      # Componentes reutilizáveis
│   ├── utils/           # Funções utilitárias
│   └── navigation/      # Configuração de navegação
├── assets/              # Imagens e recursos
├── App.js               # Entry point com navegação
├── package.json
├── app.json             # Configuração Expo
└── babel.config.js
```

## 🎨 Design

O aplicativo segue o design do Figma fornecido:
- Gradiente verde (#4CAF50) como cor principal
- Cards brancos com elevação
- Tipografia clara e hierarquia visual
- Animações suaves nas transições

## 🔐 Autenticação

O app usa JWT tokens armazenados no AsyncStorage. O token é automaticamente incluído em todas as requisições através do interceptor do axios.

## 📡 Integração com Backend

Todos os serviços estão implementados em `src/services/apiService.js`:

- **authService**: Login, registro, logout
- **productsService**: Busca de produtos e ofertas
- **listsService**: CRUD completo de listas e itens
- **rankingService**: Geração de ranking básico e detalhado

### Mock-First Strategy

O projeto segue a estratégia **Mock-First** do guia de desenvolvimento:

- **Mock API Service** (`src/services/mockApiService.js`): Dados simulados para desenvolvimento
- **Real API Service** (`src/services/realApiService.js`): Integração com backend real
- **API Service** (`src/services/apiService.js`): Barrel file que alterna entre mock e real

#### Usando Mock Service

Para usar dados mock durante desenvolvimento:

1. Configure o arquivo `.env`:
```bash
EXPO_PUBLIC_USE_MOCK=true
```

2. O app usará automaticamente dados mock do arquivo `src/data/mockData.js`

#### Usando Real API

Para usar a API real do backend:

1. Configure o arquivo `.env`:
```bash
EXPO_PUBLIC_USE_MOCK=false
EXPO_PUBLIC_API_BASE_URL=http://localhost:5000/api
```

2. O app se conectará ao backend real

#### Credenciais Mock

Para testar o login com dados mock:
- Email: `teste@example.com`
- Senha: `123456`

## 🚀 Próximos Passos

1. Adicionar imagens reais dos produtos
2. Implementar cache local para offline
3. Adicionar notificações push
4. Implementar busca por voz
5. Adicionar compartilhamento de listas

## 📝 Licença

Educational Project
