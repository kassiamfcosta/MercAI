# 🌐 GitHub Pages - MercAI

Guia de configuração e uso do GitHub Pages para o frontend web do MercAI.

## 📋 O Que Foi Implementado

✅ **GitHub Actions Workflow** para deploy automático  
✅ **Configuração de API** para funcionar com GitHub Pages  
✅ **Documentação** completa do frontend  
✅ **Deploy automático** quando há mudanças no frontend

## 🚀 Como Funciona

### 1. Deploy Automático

O GitHub Actions detecta mudanças na pasta `Contextro - MercAI/Mercai_/` e faz o deploy automaticamente para o GitHub Pages.

### 2. Workflow

O arquivo `.github/workflows/deploy-pages.yml` contém a configuração do deploy:

- **Trigger**: Push na branch `main` com mudanças no frontend
- **Ação**: Deploy automático para GitHub Pages
- **URL**: `https://kassiamfcosta.github.io/MercAI/`

### 3. Configuração Inicial

Para ativar o GitHub Pages:

1. Acesse: https://github.com/kassiamfcosta/MercAI/settings/pages
2. Em **Source**, selecione: **GitHub Actions**
3. O deploy será feito automaticamente pelo workflow

## 🔧 Configuração da API

O frontend precisa se comunicar com o backend Flask. O arquivo `API_CONFIG.js` foi configurado para:

- **Desenvolvimento local**: `http://localhost:8000/api`
- **GitHub Pages**: URL do backend em produção (configure no `API_CONFIG.js`)

### Como Configurar a URL do Backend

1. Abra: `Contextro - MercAI/Mercai_/API_CONFIG.js`
2. Altere a URL do backend para produção:

```javascript
// Para GitHub Pages
if (hostname.includes('github.io')) {
    return 'https://seu-backend.herokuapp.com/api'; // Altere aqui
}
```

Substitua `https://seu-backend.herokuapp.com/api` pela URL real do seu backend em produção.

## 📁 Estrutura de Arquivos

```
.github/
└── workflows/
    └── deploy-pages.yml     # Workflow de deploy

Contextro - MercAI/
└── Mercai_/
    ├── index.html           # Página inicial
    ├── login.html           # Login
    ├── cadastro.html        # Cadastro
    ├── inicio.html          # Dashboard
    ├── API_CONFIG.js        # Configuração da API
    ├── js/                  # Scripts JavaScript
    ├── img/                 # Imagens
    └── README.md            # Documentação do frontend
```

## 🌐 URLs Disponíveis

Após o deploy, o site estará disponível em:

- **Página inicial**: https://kassiamfcosta.github.io/MercAI/
- **Login**: https://kassiamfcosta.github.io/MercAI/login.html
- **Cadastro**: https://kassiamfcosta.github.io/MercAI/cadastro.html
- **Dashboard**: https://kassiamfcosta.github.io/MercAI/inicio.html

## 🔄 Deploy Manual

Você também pode fazer deploy manual:

1. Acesse: https://github.com/kassiamfcosta/MercAI/actions
2. Selecione o workflow: **Deploy to GitHub Pages**
3. Clique em **Run workflow**
4. Selecione a branch: **main**
5. Clique em **Run workflow**

## ✅ Verificação do Deploy

Após o push ou deploy manual:

1. Acesse: https://github.com/kassiamfcosta/MercAI/actions
2. Verifique se o workflow **Deploy to GitHub Pages** foi executado com sucesso
3. Acesse: https://kassiamfcosta.github.io/MercAI/
4. Verifique se o site está carregando corretamente

## 🐛 Troubleshooting

### Deploy não está funcionando

1. Verifique se o GitHub Pages está ativado:
   - Settings → Pages → Source: **GitHub Actions**

2. Verifique se o workflow está configurado corretamente:
   - Arquivo `.github/workflows/deploy-pages.yml` existe
   - Sintaxe YAML está correta

3. Verifique os logs do workflow:
   - Actions → Deploy to GitHub Pages → Ver logs

### Site não está acessível

1. Aguarde alguns minutos (deploy pode levar 1-2 minutos)
2. Verifique se o workflow foi executado com sucesso
3. Limpe o cache do navegador (Ctrl+F5)
4. Verifique se a URL está correta: `https://kassiamfcosta.github.io/MercAI/`

### API não está funcionando

1. Verifique se a URL do backend está configurada no `API_CONFIG.js`
2. Verifique se o backend está rodando em produção
3. Verifique se o CORS está configurado no backend para permitir `github.io`

## 📝 Próximos Passos

1. ✅ Configurar URL do backend em produção no `API_CONFIG.js`
2. ✅ Testar todas as funcionalidades no GitHub Pages
3. ✅ Configurar domínio personalizado (opcional)
4. ✅ Adicionar analytics (opcional)

## 🔗 Links Úteis

- **GitHub Pages**: https://pages.github.com/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Deploy Pages Action**: https://github.com/actions/deploy-pages

---

**Status**: ✅ Implementado e configurado  
**URL**: https://kassiamfcosta.github.io/MercAI/  
**Última atualização**: Novembro 2025

