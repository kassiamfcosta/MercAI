# 📤 Guia: Upload do Projeto para GitHub

Este guia mostra como fazer upload do projeto MercAI para o repositório GitHub de forma segura e organizada.

## 📋 Pré-requisitos

1. ✅ Conta no GitHub
2. ✅ Git instalado no seu computador
3. ✅ Acesso ao repositório: https://github.com/MayaraVieiraa/Mercai_.git

## ⚠️ IMPORTANTE - Antes de Começar

### 1. Verificar Arquivos Sensíveis

**NUNCA** faça commit de:
- ❌ `.env` (contém chaves de API e senhas)
- ❌ `venv/` ou `node_modules/` (muito grandes)
- ❌ `*.db` (banco de dados local)
- ❌ `__pycache__/` (arquivos Python compilados)

O arquivo `.gitignore` já está configurado para ignorar esses arquivos automaticamente.

### 2. Verificar o .env

Certifique-se de que o arquivo `mercai-backend/.env` existe e contém suas configurações, mas **NÃO** será enviado para o Git (já está no .gitignore).

### 3. Criar .env.example (Recomendado)

Crie um arquivo `.env.example` como modelo para outros desenvolvedores:

```bash
# Copiar .env para .env.example e remover valores sensíveis
cp mercai-backend/.env mercai-backend/.env.example
# Depois edite o .env.example e remova valores reais
```

---

## 🚀 Método 1: Upload Inicial (Primeira Vez)

Se você ainda não tem o projeto no Git:

### Passo 1: Inicializar Git

```bash
cd C:/Users/User/workspace/MercAI
git init
```

### Passo 2: Adicionar Remote do GitHub

```bash
git remote add origin https://github.com/MayaraVieiraa/Mercai_.git
```

### Passo 3: Verificar Status

```bash
git status
```

Você deve ver todos os arquivos que serão adicionados (exceto os ignorados pelo .gitignore).

### Passo 4: Adicionar Arquivos

```bash
# Adicionar todos os arquivos
git add .
```

### Passo 5: Fazer Commit

```bash
git commit -m "feat: Adiciona projeto completo MercAI

- Backend Flask com API REST completa
- Frontend Web (HTML/CSS/JS)
- Frontend Mobile (React Native/Expo)
- Sistema de autenticação JWT
- CRUD completo de produtos, lojas e listas
- Sistema de ranking de ofertas
- Documentação completa"
```

### Passo 6: Configurar Branch Principal

```bash
git branch -M main
```

### Passo 7: Fazer Push

**⚠️ ATENÇÃO:** Se o repositório já tem arquivos, você pode precisar fazer merge:

```bash
# Se o repositório está vazio ou você quer substituir
git push -u origin main --force

# OU se quiser fazer merge com arquivos existentes
git pull origin main --allow-unrelated-histories
# Resolver conflitos se houver
git push -u origin main
```

---

## 🔄 Método 2: Upload Incremental (Atualizações)

Para adicionar novas mudanças:

### Passo 1: Verificar Status

```bash
cd C:/Users/User/workspace/MercAI
git status
```

### Passo 2: Adicionar Arquivos Específicos

```bash
# Adicionar todos os arquivos modificados
git add .

# OU adicionar arquivos específicos
git add mercai-backend/src/api/new_endpoint.py
git add mercai-frontend/src/screens/NewScreen.js
```

### Passo 3: Commit

```bash
git commit -m "feat: Adiciona nova funcionalidade X"
```

### Passo 4: Push

```bash
git push origin main
```

---

## 📁 Estrutura Recomendada no GitHub

Após o upload, sua estrutura deve ficar assim:

```
Mercai_/
├── .gitignore                  ✅ Já criado
├── README.md                   ✅ Já criado
├── GUIA_UPLOAD_GIT.md         ✅ Este arquivo
├── STATUS_REQUISITOS.md        ✅ Status do projeto
│
├── mercai-backend/            ✅ Backend completo
│   ├── .gitignore
│   ├── .env.example           ⚠️ Criar este arquivo
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── FUNCIONALIDADES_BACKEND.md
│   ├── EXECUTAR_TESTES.md
│   ├── src/
│   ├── tests/
│   └── ...
│
├── Contextro - MercAI/        ✅ Frontend Web existente
│   └── Mercai_/
│       ├── index.html
│       ├── login.html
│       └── ...
│
└── mercai-frontend/           ✅ Frontend Mobile
    ├── .gitignore
    ├── package.json
    ├── App.js
    └── ...
```

---

## 🔧 Solução de Problemas

### Erro: "fatal: remote origin already exists"

```bash
# Remover remote existente
git remote remove origin

# Adicionar novamente
git remote add origin https://github.com/MayaraVieiraa/Mercai_.git
```

### Erro: "fatal: refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

### Arquivo .env foi adicionado por engano

```bash
# Remover do Git (mas manter localmente)
git rm --cached mercai-backend/.env

# Adicionar ao .gitignore (já está lá)
# Fazer commit
git commit -m "fix: Remove .env do Git"

# Push
git push origin main
```

### Reverter último commit (antes do push)

```bash
git reset --soft HEAD~1
```

### Verificar o que será enviado

```bash
# Ver arquivos que serão commitados
git status

# Ver diferenças
git diff

# Ver arquivos que serão enviados no próximo push
git diff origin/main..HEAD --name-only
```

---

## ✅ Checklist Antes de Fazer Push

- [ ] ✅ `.env` está no `.gitignore` e não será enviado
- [ ] ✅ `venv/` e `node_modules/` estão no `.gitignore`
- [ ] ✅ `*.db` está no `.gitignore`
- [ ] ✅ `.env.example` foi criado (opcional mas recomendado)
- [ ] ✅ README.md está atualizado
- [ ] ✅ Testes passaram (se houver)
- [ ] ✅ Código está funcionando localmente
- [ ] ✅ Mensagem de commit é descritiva

---

## 📝 Boas Práticas

### 1. Commits Descritivos

**❌ Ruim:**
```bash
git commit -m "mudanças"
```

**✅ Bom:**
```bash
git commit -m "feat: Adiciona endpoint de busca de produtos

- Implementa GET /api/products/search
- Adiciona validação de query (mínimo 3 caracteres)
- Implementa cache Redis para melhor performance"
```

### 2. Commits Pequenos e Focados

Faça commits frequentes de pequenas mudanças, não um commit gigante de tudo de uma vez.

### 3. Branches para Features

```bash
# Criar branch para nova feature
git checkout -b feature/nova-funcionalidade

# Trabalhar na feature
# ... fazer commits ...

# Voltar para main
git checkout main

# Mergear feature
git merge feature/nova-funcionalidade

# Deletar branch
git branch -d feature/nova-funcionalidade
```

### 4. Pull Antes de Push

```bash
# Sempre puxar mudanças antes de fazer push
git pull origin main
git push origin main
```

---

## 🎯 Próximos Passos Após Upload

1. ✅ Verificar se todos os arquivos foram enviados corretamente
2. ✅ Testar se o README.md está sendo exibido no GitHub
3. ✅ Criar `.env.example` no backend
4. ✅ Adicionar badges ao README (opcional)
5. ✅ Configurar GitHub Actions para CI/CD (futuro)
6. ✅ Adicionar descrição ao repositório no GitHub
7. ✅ Adicionar tags/topics ao repositório

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs de erro
2. Consulte a documentação do Git: https://git-scm.com/doc
3. Verifique se está usando a branch correta: `git branch`
4. Verifique o remote: `git remote -v`

---

**Última atualização:** Novembro 2025
