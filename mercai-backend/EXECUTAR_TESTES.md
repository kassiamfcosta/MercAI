# Como Executar os Testes - GUIA SIMPLES

## 📋 Resumo do que foi criado

✅ **Testes Unitários** - `tests/unit/test_auth.py` (15 testes)
✅ **Script de Teste Manual** - `test_manual.py`
✅ **Script de Servidor** - `test_server.py`
✅ **Scripts de Inicialização** - `iniciar_servidor.bat` e `iniciar_servidor.ps1`

---

## 🚀 MÉTODO MAIS SIMPLES - Use os Scripts Criados

### ⚡ Opção A: Duplo Clique (Mais Fácil)

1. **Navegue até a pasta `mercai-backend`**
2. **Clique duas vezes em `iniciar_servidor.bat`**
3. O servidor iniciará automaticamente em `http://localhost:8000`

### ⚡ Opção B: PowerShell

```powershell
cd C:\Users\User\workspace\MercAI\mercai-backend
.\iniciar_servidor.ps1
```

---

## 🚀 Método Manual (Se os scripts não funcionarem)

### Passo 1: Iniciar o servidor

**IMPORTANTE:** Você precisa ativar o ambiente virtual primeiro!

```powershell
# Navegar até a pasta do backend
cd C:\Users\User\workspace\MercAI\mercai-backend

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar servidor de testes
python test_server.py
```

O servidor iniciará em `http://localhost:8000`

**⚠️ Mantenha este terminal aberto!** O servidor precisa continuar rodando.

### Passo 2: Testar o Frontend

1. Abra o navegador e acesse:
   ```
   http://localhost:8000/login.html
   ```

2. Teste o cadastro e login através da interface web

### Passo 3: Executar testes automáticos (Opcional)

Em **outro terminal**:

```powershell
# Navegar até a pasta do backend
cd C:\Users\User\workspace\MercAI\mercai-backend

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar script de testes
python test_manual.py
```

---

## 🚀 Opção 3: Testes Automatizados (Pytest)

Execute os testes unitários com pytest:

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar todos os testes
pytest tests/unit/test_auth.py -v

# Executar com cobertura
pytest tests/unit/test_auth.py --cov=src --cov-report=html
```

---

## 🚀 Opção 3: Postman ou cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Registrar Usuário
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Obter Dados do Usuário (/me)
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## ⚠️ Importante

1. **Banco de Dados**: O servidor de teste usa SQLite (`test.db`) - não precisa de PostgreSQL
2. **Redis**: Opcional para testes básicos - o cache funciona sem Redis (apenas loga warning)
3. **Variáveis de Ambiente**: O `test_server.py` configura automaticamente para desenvolvimento

---

## 📊 Resultados Esperados

### Endpoints que devem funcionar:

✅ `GET /health` - Retorna status healthy
✅ `POST /api/auth/register` - Cria usuário e retorna token
✅ `POST /api/auth/login` - Autentica e retorna token
✅ `GET /api/auth/me` - Retorna dados do usuário (requer token)

### Testes que devem passar:

✅ Registro bem-sucedido
✅ Registro com email duplicado (deve retornar 409)
✅ Login bem-sucedido
✅ Login com credenciais inválidas (deve retornar 401)
✅ Obter dados com token válido
✅ Obter dados sem token (deve retornar 401)

---

## 🔧 Troubleshooting

### ❌ Erro: "ModuleNotFoundError: No module named 'flask_cors'"

**Problema:** O Python do sistema está sendo usado ao invés do ambiente virtual.

**Solução:**
```powershell
# 1. Certifique-se de estar na pasta correta
cd C:\Users\User\workspace\MercAI\mercai-backend

# 2. Ative o ambiente virtual PRIMEIRO
.\venv\Scripts\Activate.ps1

# 3. Verifique se o ambiente virtual está ativo (deve mostrar "venv" antes do prompt)
# Você deve ver algo como: (venv) PS C:\Users\User\workspace\MercAI\mercai-backend>

# 4. Instale as dependências se necessário
pip install -r requirements.txt

# 5. Agora execute o servidor
python test_server.py
```

**OU use o script:** `iniciar_servidor.bat` ou `iniciar_servidor.ps1` que faz isso automaticamente!

### ❌ Erro: "Cannot activate virtual environment" ou "ExecutionPolicy"

**Solução:**
```powershell
# Permitir execução de scripts no PowerShell (apenas uma vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois tente ativar novamente
.\venv\Scripts\Activate.ps1
```

### ❌ Erro: "Address already in use"

**Problema:** A porta 5000 já está em uso (outro servidor rodando).

**Solução:**
```powershell
# Encontrar processo usando a porta 5000
netstat -ano | findstr :5000

# Matar o processo (substitua <PID> pelo número encontrado)
taskkill /PID <PID> /F

# OU simplesmente feche o terminal onde o servidor anterior está rodando
```

### ❌ Erro: "Database connection failed"

**Problema:** Erro ao conectar ao banco de dados.

**Solução:**
```powershell
# O SQLite cria automaticamente - verifique permissões de escrita
# Se persistir, tente deletar o arquivo test.db e rodar novamente
```

### ❌ Frontend não carrega ou mostra erro

**Verifique:**
1. O servidor está rodando? (você deve ver logs no terminal)
2. Acessou `http://localhost:5000/login.html` (não `file:///`)
3. Abra o Console do navegador (F12) e veja se há erros
4. Verifique se o caminho do frontend está correto no `main.py`

---

## ✅ Próximos Passos

Após validar que os testes estão passando, podemos continuar com:
1. Fase 4: Web Scraping e IA
2. Fase 5: Algoritmo de Ranking
3. Fase 6: Endpoints REST adicionais

