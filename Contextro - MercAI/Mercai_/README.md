# MercAI - Frontend Web

Frontend web do MercAI - Comparador de preços de supermercados.

## 📋 Sobre

Este é o frontend web do MercAI, desenvolvido com HTML, CSS e JavaScript vanilla. O frontend é servido via GitHub Pages e se comunica com o backend Flask via API REST.

## 🌐 Acesso

O frontend está disponível em: **https://kassiamfcosta.github.io/MercAI/**

## 🚀 Funcionalidades

- ✅ **Autenticação**: Login e cadastro de usuários
- ✅ **Listas de Compras**: Criação e gerenciamento de listas
- ✅ **Busca de Produtos**: Pesquisa de produtos por nome e categoria
- ✅ **Lojas Próximas**: Visualização de lojas próximas com geolocalização
- ✅ **Ranking de Ofertas**: Comparação de preços entre lojas
- ✅ **Dashboard**: Visualização de melhores ofertas

## 📁 Estrutura

```
Mercai_/
├── index.html              # Página inicial (splash screen)
├── login.html              # Tela de login
├── cadastro.html           # Tela de cadastro
├── inicio.html             # Tela principal (dashboard)
├── lista_de_compras.html   # Gerenciamento de listas
├── pesquisar_produto.html  # Busca de produtos
├── mercados_proximos.html  # Lojas próximas
├── perfil.html             # Perfil do usuário
├── js/
│   ├── api.js              # Cliente API
│   └── auth.js             # Gerenciamento de autenticação
├── img/                     # Imagens e assets
└── API_CONFIG.js           # Configuração da API
```

## 🔧 Configuração

### API Backend

O frontend se comunica com o backend Flask. Para configurar a URL do backend:

1. Edite o arquivo `API_CONFIG.js`
2. Altere a URL do backend para produção:

```javascript
// Para GitHub Pages
if (hostname.includes('github.io')) {
    return 'https://seu-backend.herokuapp.com/api'; // Altere aqui
}
```

### Variáveis de Ambiente

Para desenvolvimento local, o frontend usa `http://localhost:8000/api` automaticamente.

Para produção no GitHub Pages, configure a URL do backend no `API_CONFIG.js`.

## 📦 Deploy

O deploy é feito automaticamente via GitHub Actions quando há mudanças na pasta `Contextro - MercAI/Mercai_/`.

### Deploy Manual

1. As mudanças são automaticamente detectadas
2. O GitHub Actions faz o deploy
3. O site fica disponível em: `https://kassiamfcosta.github.io/MercAI/`

## 🛠️ Desenvolvimento Local

Para testar localmente:

1. Clone o repositório
2. Abra os arquivos HTML no navegador ou use um servidor local:

```bash
# Python
python -m http.server 8080

# Node.js
npx http-server

# PHP
php -S localhost:8080
```

3. Acesse: `http://localhost:8080/Contextro - MercAI/Mercai_/login.html`

## 📱 Compatibilidade

- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile (iOS/Android)

## 📚 Documentação

Para mais informações sobre a API, consulte:
- [FUNCIONALIDADES_BACKEND.md](../../mercai-backend/FUNCIONALIDADES_BACKEND.md)
- [README.md](../../README.md)

## 🔗 Links

- **Frontend**: https://kassiamfcosta.github.io/MercAI/
- **Repositório**: https://github.com/kassiamfcosta/MercAI
- **Backend**: (Configure no API_CONFIG.js)

---

**Desenvolvido por**: Equipe MercAI  
**Versão**: 1.0.0
