# 🔐 Como Resolver Autenticação Git para Push

## ⚠️ Problema Encontrado

O push falhou porque o Git está usando credenciais de outro usuário (`kassiacosta-z`) e você precisa das credenciais do usuário `MayaraVieiraa`.

## ✅ O Que Já Foi Feito

Todos os commits foram criados com sucesso:

1. ✅ `docs: Adiciona documentacao e configuracao do projeto`
2. ✅ `feat: Implementa backend Flask completo com API REST`
3. ✅ `feat: Adiciona frontend Mobile (React Native/Expo)`
4. ✅ `feat: Adiciona frontend Web (HTML/CSS/JavaScript)`

**Total:** 4 commits organizados e padronizados prontos para push!

---

## 🔧 Soluções para Autenticação

### Método 1: Usar Personal Access Token (Recomendado)

1. **Criar um Personal Access Token no GitHub:**
   - Acesse: https://github.com/settings/tokens
   - Clique em "Generate new token" → "Generate new token (classic)"
   - Dê um nome (ex: "MercAI Project")
   - Selecione o escopo: **`repo`** (acesso completo aos repositórios)
   - Clique em "Generate token"
   - **COPIE O TOKEN** (você só verá ele uma vez!)

2. **Usar o token no push:**
   ```bash
   cd C:/Users/User/workspace/MercAI
   
   # Usar token no URL
   git remote set-url origin https://SEU_TOKEN@github.com/MayaraVieiraa/Mercai_.git
   
   # OU fazer push diretamente com token
   git push -u origin main
   # Quando pedir senha, use o TOKEN como senha
   ```

### Método 2: Atualizar Credenciais do Windows

1. **Remover credenciais antigas:**
   - Abra: Painel de Controle → Credenciais do Windows
   - Procure por "git:https://github.com"
   - Remova as credenciais antigas

2. **Fazer push novamente (irá pedir credenciais novas):**
   ```bash
   cd C:/Users/User/workspace/MercAI
   git push -u origin main
   ```
   - Use o username: `MayaraVieiraa`
   - Use o Personal Access Token como senha

### Método 3: Configurar Git Credential Manager

```bash
# Verificar credenciais atuais
git config --global credential.helper

# Limpar credenciais armazenadas
git credential-manager-core erase
# ou
git credential-manager erase

# Fazer push (irá pedir credenciais)
git push -u origin main
```

### Método 4: Usar SSH (Alternativa)

Se você tem chave SSH configurada:

```bash
# Mudar remote para SSH
git remote set-url origin git@github.com:MayaraVieiraa/Mercai_.git

# Fazer push
git push -u origin main
```

---

## 📝 Comandos Prontos para Copiar

Depois de resolver a autenticação, execute:

```bash
cd C:/Users/User/workspace/MercAI

# Verificar commits
git log --oneline

# Fazer push
git push -u origin main
```

---

## ✅ Verificação Após Push

Depois do push bem-sucedido, verifique no GitHub:

1. Acesse: https://github.com/MayaraVieiraa/Mercai_
2. Verifique se todos os arquivos estão lá
3. Verifique se o README.md está sendo exibido
4. Verifique os commits no histórico

---

## 🆘 Se Ainda Não Funcionar

1. **Verificar permissões no repositório:**
   - Certifique-se de que a conta `MayaraVieiraa` tem permissão de escrita
   - Se for um repositório de organização, verifique se você é colaborador

2. **Verificar URL do remote:**
   ```bash
   git remote -v
   ```
   Deve mostrar: `origin https://github.com/MayaraVieiraa/Mercai_.git`

3. **Tentar push forçado (CUIDADO - só se necessário):**
   ```bash
   git push -u origin main --force
   ```
   ⚠️ **ATENÇÃO:** Isso pode sobrescrever commits no repositório remoto!

---

## 📞 Próximos Passos

Após resolver a autenticação e fazer o push com sucesso:

1. ✅ Verificar que todos os arquivos estão no GitHub
2. ✅ Adicionar descrição ao repositório
3. ✅ Adicionar tags/topics (ex: `flask`, `python`, `react-native`, `comparador-precos`)
4. ✅ Configurar GitHub Pages (se necessário)
5. ✅ Adicionar badges ao README.md (opcional)

---

**Última atualização:** Novembro 2025
