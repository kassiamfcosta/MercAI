# Status do Front-End MercAI

## Expo Rodando

O Expo está sendo executado em background. Para visualizar o aplicativo:

### Opções de Visualização:

1. **Expo Go no Celular:**
   - Baixe o app "Expo Go" na App Store (iOS) ou Google Play (Android)
   - Escaneie o QR code que aparece no terminal ou no navegador
   - O app será carregado automaticamente

2. **Emulador Android:**
   - Abra um emulador Android
   - Pressione `a` no terminal do Expo para abrir no Android

3. **Simulador iOS (Mac apenas):**
   - Abra o simulador iOS
   - Pressione `i` no terminal do Expo para abrir no iOS

4. **Navegador Web:**
   - Pressione `w` no terminal do Expo para abrir no navegador
   - O app será carregado em `http://localhost:19006`

### Configuração Atual:

- **Modo Mock:** Ativado (`EXPO_PUBLIC_USE_MOCK=true`)
- **Credenciais de Teste:**
  - Email: `teste@example.com`
  - Senha: `123456`

### Dados Mock Disponíveis:

- ✅ 12 produtos
- ✅ 4 lojas
- ✅ 11 ofertas
- ✅ 2 listas de compras pré-cadastradas

### Telas Implementadas:

1. ✅ SplashScreen - Tela inicial
2. ✅ TutorialScreen - Tutorial de introdução
3. ✅ LoginScreen - Login com gradiente verde
4. ✅ RegisterScreen - Cadastro
5. ✅ HomeScreen - Tela principal
6. ✅ SearchProductsScreen - Busca de produtos
7. ✅ ShoppingListScreen - Gerenciamento de listas
8. ✅ DashboardScreen - Ranking de ofertas

### Próximos Passos:

1. Abra o Expo Go no celular ou um emulador
2. Escaneie o QR code ou pressione a tecla correspondente
3. Teste o login com as credenciais mock
4. Explore as telas implementadas

### Troubleshooting:

**Se o Expo não aparecer:**
- Verifique se o processo Node está rodando: `Get-Process node`
- Execute manualmente: `cd mercai-frontend && npm start`

**Se houver erros:**
- Verifique se o arquivo `.env` existe e tem `EXPO_PUBLIC_USE_MOCK=true`
- Limpe o cache: `npm start -- --clear`

