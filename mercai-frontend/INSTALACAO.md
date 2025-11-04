# Guia de Instalação - MercAI Frontend

## Passos para Instalação e Execução

### 1. Instalar Dependências

```bash
cd mercai-frontend
npm install
```

Isso instalará todas as dependências, incluindo:
- React Native e Expo
- Navegação (React Navigation)
- AsyncStorage
- Axios
- react-native-dotenv (para variáveis de ambiente)

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

#### Para usar Mock Service (desenvolvimento com dados simulados):
```bash
EXPO_PUBLIC_USE_MOCK=true
EXPO_PUBLIC_API_BASE_URL=http://localhost:5000/api
```

#### Para usar API Real:
```bash
EXPO_PUBLIC_USE_MOCK=false
EXPO_PUBLIC_API_BASE_URL=http://localhost:5000/api
```

**Nota:** Para testar em dispositivo físico ou emulador, substitua `localhost` pelo IP da sua máquina na rede local:
```bash
EXPO_PUBLIC_API_BASE_URL=http://192.168.1.100:5000/api
```

### 3. Executar o Aplicativo

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

### 4. Testar com Mock Service

Com `EXPO_PUBLIC_USE_MOCK=true`, você pode testar sem o backend:

**Credenciais de teste:**
- Email: `teste@example.com`
- Senha: `123456`

**Dados disponíveis:**
- 12 produtos mock
- 4 lojas mock
- 11 ofertas mock
- 2 listas de compras mock

### 5. Alternar entre Mock e API Real

Para alternar entre mock e API real, basta alterar a variável `EXPO_PUBLIC_USE_MOCK` no arquivo `.env` e reiniciar o Expo.

### Troubleshooting

**Erro: "Module not found: @env"**
- Certifique-se de que `react-native-dotenv` foi instalado
- Reinicie o servidor Expo após instalar dependências

**Erro: "Cannot connect to API"**
- Verifique se o backend está rodando (se usando API real)
- Verifique a URL no `.env`
- Para dispositivo físico, use o IP local em vez de `localhost`

**Mock não funciona:**
- Verifique se `EXPO_PUBLIC_USE_MOCK=true` no `.env`
- Reinicie o Expo após alterar `.env`

