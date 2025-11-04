# 🧠 Projeto MercAI — Análise Técnica Completa

**Data:** 01/11/2025

---

## 📌 Visão Geral

O **MercAI** é um aplicativo de comparação de preços e ofertas, com foco em inteligência artificial e experiência do usuário.  
O sistema é dividido entre:

- **Backend (IA e algoritmo de busca)** — Responsável por comparar preços e gerar rankings.  
- **Frontend (App Mobile)** — Interface usada pelo cliente para cadastro, busca e visualização dos resultados.

---

## 📦 Estrutura do Projeto (ZIP)

| Pasta / Arquivo | Conteúdo | Observação |
|------------------|-----------|-------------|
| `/assets/` | Imagens e ícones das telas | Ex: Logo, Login, Cadastro |
| `/src/` | Código principal do app | Estrutura modular |
| `/components/` | Componentes de UI reutilizáveis | Botões, inputs, cards |
| `/services/` | Integrações externas | API de preços, IA |
| `/screens/` | Telas principais | Login, Cadastro, Home, Lista, Dashboard |
| `/data/` | Arquivo JSON de mock de produtos | Usado para simulação de ranking |
| `/models/` | Estruturas de dados | Produto, Loja, Oferta |

---

## ⚙️ Requisitos Funcionais (Resumo)

### 🔹 Algoritmo / Backend (Kássia e Ryan)

| Função | Status | Observação |
|---------|--------|-------------|
| Receber lista de compras | ✅ | Simulado via formulário |
| Comparar preços entre lojas | ⚠️ | Mock — sem integração real |
| Identificar melhores ofertas | ⚠️ | Ordenação simples por preço |
| Retornar ranking de preços | ✅ | Implementado de forma básica |
| Atualizar dashboard com resultados | ✅ | Mostra ranking estático |
| Otimizar sugestões (preço + proximidade) | 🚧 | Não implementado |

### 🔹 App / Front-end (Gabriel e Mayara)

| Tela | Cumpre requisitos? | Comentário |
|------|--------------------|-------------|
| Splash / Logo | ✅ | Exibe logo MercAI |
| Boas-vindas / Tutorial | ✅ | Contém botão “Entrar” |
| Login | ✅ | Campos e botões corretos |
| Cadastro | ✅ | Campos e navegação corretos |
| Início (Home) | ✅ | Exibe categorias e ofertas |
| Pesquisar Produtos | ✅ | Filtro e botão “Ver mais” |
| Lista de Compras | ✅ | Itens e botão “Calcular” |
| Tela de carregamento | ⚠️ | Placeholder simples |
| Dashboard de preços | ✅ | Ranking de ofertas |

---

## 🧩 Avaliação Técnica

### 🔧 Linguagem / Framework
Provável uso de **React Native** (ou Expo).  
Backend ainda não implementado — simulado com JSON local.

### ⚙️ Pontos Fortes
- Estrutura modular clara.
- Navegação entre telas funcional.
- Cumprimento de quase todos os requisitos de UI.

### ⚠️ Melhorias Necessárias

| Categoria | Problema | Solução |
|------------|-----------|---------|
| Integração IA | Lógica apenas simulada | Criar API Node.js/Python para ranking real |
| Localização | Sem uso do campo “Adicionar localização” | Integrar Google Maps API |
| Dashboard | Ranking estático | Alimentar via endpoint `/api/ofertas` |
| Sugestões inteligentes | Não implementadas | Adicionar peso entre preço e distância |
| UX / Feedback visual | Tela de carregamento básica | Adicionar animação Lottie |

---

## 📊 Grau de Atendimento aos Requisitos

| Categoria | Cumprimento |
|------------|--------------|
| Algoritmo | **60%** |
| Front-end | **90%** |
| Não Funcionais | **80%** |
| Documentação | **85%** |

**Média Geral: 79% (projeto sólido, IA simulada).**

---

## 🚀 Próximos Passos

1. **Implementar backend real (API REST)**  
   - Endpoint `/api/ranking` com cálculo de preços e descontos.

2. **Adicionar IA de recomendação**  
   - Combinar preço + distância + estoque em score ponderado.

3. **Integrar com n8n / Webhooks**  
   - Automação de coleta de preços e atualização em tempo real.

4. **Usar banco de dados real (Firebase / Supabase)**  
   - Armazenar listas de compras e histórico de pesquisas.

5. **Melhorar Dashboard**  
   - Exibir economia total e recomendação de loja mais vantajosa.

---

## 🧱 Conclusão

O **MercAI** é um projeto promissor, com base sólida no front-end e boa documentação de requisitos.  
A principal evolução necessária é a **implementação real da camada de IA e integração com APIs externas de preço**.

---

**Autor da análise:** ChatGPT (GPT‑5)  
**Baseado em:** `Requisitos - MercAI.pdf` e `MercAI.zip`  
