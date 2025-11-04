# Guia de Prompts para Geração de Front-End com IA (Baseado em Figma)

**Autor:** Assistente Manus  
**Data:** Outubro 2024  
**Versão:** 1.0

---

## 📑 Índice

1. [Introdução: A Estratégia "Mock-First"](#introdução-a-estratégia-mock-first)
2. [Estrutura de um Prompt Eficaz](#estrutura-de-um-prompt-eficaz)
3. [Fase 1: Configuração Global e Estilo](#fase-1-configuração-global-e-estilo)
4. [Fase 2: Geração de Componentes (Estáticos)](#fase-2-geração-de-componentes-estáticos)
5. [Fase 3: Criação do Mock Service (Simulação do Back-end)](#fase-3-criação-do-mock-service-simulação-do-back-end)
6. [Fase 4: Integração e Interatividade](#fase-4-integração-e-interatividade)
7. [Fase 5: Preparação para Integração com Back-end Real](#fase-5-preparação-para-integração-com-back-end-real)
8. [Exemplo Completo: Tela de Login](#exemplo-completo-tela-de-login)
9. [Dicas e Boas Práticas](#dicas-e-boas-práticas)

---

## 1. Introdução: A Estratégia "Mock-First"

O desafio de desenvolver um front-end quando o back-end ainda não está pronto ou testável é comum. A melhor estratégia é o **Desenvolvimento "Mock-First"**. Isso significa que criaremos um "back-end falso" (mock) que simula as respostas da API real. 

**Vantagens:**
- **Desenvolvimento Paralelo:** Front-end e back-end podem ser desenvolvidos de forma independente e simultânea.
- **Testes de UI Isolados:** Permite testar a interface e a experiência do usuário sem depender de dados reais.
- **Contrato de API Claro:** O mock service serve como um "contrato" entre as equipes, definindo a estrutura de dados esperada.
- **Integração Rápida:** Quando o back-end estiver pronto, basta "trocar" o serviço de mock pelo serviço real.

Este guia fornecerá prompts estruturados para implementar essa estratégia usando ferramentas de IA generativa.

---

## 2. Estrutura de um Prompt Eficaz

Um bom prompt para geração de código deve conter:

- **`Persona`**: O papel que a IA deve assumir.
- **`Contexto`**: O objetivo geral e a tarefa específica.
- **`Input`**: Dados fornecidos (link do Figma, screenshots, estruturas de dados).
- **`Tecnologia`**: Stack a ser usada (React, Vue, Svelte, Tailwind CSS, etc.).
- **`Tarefa`**: A ação específica a ser executada.
- **`Critérios de Aceitação`**: Condições para o código ser considerado correto.

---

## 3. Fase 1: Configuração Global e Estilo

O primeiro passo é estabelecer a base do projeto.

### Prompt para Configuração do Projeto

```
Persona: Você é um engenheiro de front-end sênior, especialista em React e Tailwind CSS.

Contexto: Estamos iniciando um novo projeto de front-end para um aplicativo de gestão de tarefas. O design está disponível no Figma. O objetivo desta primeira etapa é configurar a estrutura do projeto e os estilos globais.

Input:
- Link do Figma (página de estilos): [URL_FIGMA_ESTILOS]
- Screenshot da paleta de cores e tipografia do Figma.

Tecnologia:
- Framework: React (usando Vite)
- Estilização: Tailwind CSS
- Linguagem: TypeScript

Tarefa:
1. Forneça os comandos para criar um novo projeto React com Vite e TypeScript.
2. Forneça os comandos para instalar e configurar o Tailwind CSS no projeto.
3. Analise a paleta de cores, fontes e espaçamentos do Figma e configure o arquivo `tailwind.config.js` para refletir exatamente o design system. Crie tokens para cores primárias, secundárias, de texto, de fundo, etc.
4. Configure o arquivo `index.css` global com as fontes principais e estilos de base (ex: cor de fundo do body).

Critérios de Aceitação:
- O arquivo `tailwind.config.js` deve conter uma seção `theme.extend` com as cores e fontes do Figma.
- O projeto deve ser inicializado sem erros.
- O `index.css` deve importar as fontes corretas (ex: do Google Fonts) e aplicar estilos globais básicos.
```

---

## 4. Fase 2: Geração de Componentes (Estáticos)

Nesta fase, focamos em traduzir os elementos visuais do Figma em componentes de código, sem interatividade.

### Prompt para Geração de Componente

```
Persona: Você é um desenvolvedor front-end especialista em React e na criação de componentes pixel-perfect a partir de designs.

Contexto: Estamos construindo a tela de dashboard. Precisamos criar o componente `CardDeTarefa` estático, baseado no design do Figma.

Input:
- Screenshot do componente `CardDeTarefa` no Figma.
- Especificações do Figma (dimensões, cores, fontes, espaçamentos, sombras).

Tecnologia:
- Framework: React com TypeScript
- Estilização: Tailwind CSS (usando os tokens definidos no `tailwind.config.js`)

Tarefa:
1. Crie um novo componente React chamado `TaskCard.tsx`.
2. O componente deve receber props para o título da tarefa, descrição, data de vencimento e status (ex: "Pendente", "Em Progresso", "Concluído").
3. Use as classes do Tailwind CSS para estilizar o componente de forma que ele seja visualmente idêntico ao screenshot do Figma.
4. Use os tokens de cores e fontes que já configuramos (ex: `bg-primary`, `text-gray-dark`).
5. O componente deve ser puramente visual, sem nenhuma lógica de estado ou eventos de clique por enquanto.

Critérios de Aceitação:
- O componente `TaskCard.tsx` deve ser criado.
- O componente deve ser exportado e renderizar corretamente quando importado em outra página.
- O visual do componente deve ser idêntico ao design do Figma em diferentes estados (ex: cores diferentes para cada status).
- O código deve ser limpo, bem estruturado e usar as classes do Tailwind CSS de forma semântica.
```

---

## 5. Fase 3: Criação do Mock Service (Simulação do Back-end)

Esta é a etapa crucial para desenvolver de forma independente.

### Prompt para Criação do Mock Service

```
Persona: Você é um desenvolvedor front-end com experiência em arquitetura de software e testes.

Contexto: Nosso back-end ainda não está pronto para ser consumido. Para desbloquear o desenvolvimento do front-end, precisamos criar um serviço de mock que simule as respostas da API.

Input:
- Documentação (ou rascunho) dos endpoints da API do back-end.
- Exemplo de payload JSON para os endpoints `/api/tasks` (GET) e `/api/tasks/:id` (GET).

Tecnologia:
- Linguagem: TypeScript

Tarefa:
1. Crie uma pasta `src/services`.
2. Dentro dela, crie um arquivo `mockApiService.ts`.
3. Neste arquivo, crie e exporte funções que simulam as chamadas da API real. Por exemplo:
   - `getTasks()`: Deve retornar uma Promise que resolve, após um atraso simulado (ex: 500ms), com uma lista de tarefas em formato JSON.
   - `getTaskById(id: string)`: Deve retornar uma Promise que resolve com os dados de uma única tarefa.
4. Crie um arquivo `src/data/mockData.ts` que contenha os dados JSON estáticos que serão retornados por essas funções. Inclua vários exemplos de tarefas com diferentes status.
5. As funções no `mockApiService.ts` devem importar os dados de `mockData.ts`.

Critérios de Aceitação:
- O arquivo `mockApiService.ts` deve existir e exportar as funções `getTasks` e `getTaskById`.
- As funções devem retornar Promises, simulando uma chamada de API assíncrona.
- Os dados retornados devem vir do arquivo `mockData.ts` e corresponder à estrutura esperada pelo front-end.
```

---

## 6. Fase 4: Integração e Interatividade

Agora, conectamos os componentes estáticos ao nosso mock service.

### Prompt para Integração de Dados e Estado

```
Persona: Você é um desenvolvedor React experiente, focado em gerenciamento de estado e componentização.

Contexto: Temos o componente `TaskCard.tsx` estático e o `mockApiService.ts`. Agora, vamos criar a página `Dashboard.tsx` que busca os dados do mock service e renderiza uma lista de cards de tarefa.

Input:
- Componente `TaskCard.tsx`.
- Serviço `mockApiService.ts`.

Tecnologia:
- Framework: React com TypeScript e Hooks (useState, useEffect)
- Estilização: Tailwind CSS

Tarefa:
1. Crie um novo componente de página chamado `Dashboard.tsx`.
2. Dentro de `Dashboard.tsx`, use o hook `useEffect` para chamar a função `getTasks()` do `mockApiService.ts` quando o componente for montado.
3. Use o hook `useState` para armazenar os dados das tarefas retornados pelo serviço.
4. Crie estados para `loading` e `error` para simular o ciclo de vida de uma requisição de dados.
5. Renderize uma mensagem de "Carregando..." enquanto os dados estão sendo buscados.
6. Renderize uma mensagem de erro se a Promise for rejeitada (você pode modificar o mock service para simular um erro).
7. Se os dados forem carregados com sucesso, use a função `.map()` para iterar sobre a lista de tarefas e renderizar um componente `TaskCard.tsx` para cada uma, passando os dados corretos como props.

Critérios de Aceitação:
- A página `Dashboard.tsx` deve ser criada.
- Ao carregar a página, uma chamada para `getTasks()` deve ser feita.
- Um estado de "Carregando..." deve ser exibido inicialmente.
- Uma lista de componentes `TaskCard` deve ser renderizada na tela com os dados do mock.
```

---

## 7. Fase 5: Preparação para Integração com Back-end Real

Preparamos o terreno para a futura substituição do mock.

### Prompt para Abstração do Serviço de API

```
Persona: Você é um arquiteto de software focado em criar código modular e de fácil manutenção.

Contexto: Atualmente, nossos componentes importam diretamente do `mockApiService.ts`. Para facilitar a transição para a API real no futuro, precisamos abstrair a camada de serviço.

Input:
- Código atual que usa `mockApiService.ts`.

Tecnologia:
- Linguagem: TypeScript

Tarefa:
1. Crie um novo arquivo `src/services/apiService.ts`.
2. Este arquivo atuará como um "barril" (barrel file) que exporta o serviço apropriado com base em uma variável de ambiente.
3. Crie um arquivo `src/services/realApiService.ts` com a mesma assinatura de funções do `mockApiService.ts`, mas com chamadas de API reais (usando `fetch` ou `axios`). Deixe as implementações comentadas por enquanto.
4. Modifique `apiService.ts` para exportar as funções do `mockApiService.ts` por padrão, mas com lógica para exportar do `realApiService.ts` se, por exemplo, `process.env.REACT_APP_USE_MOCK` for `false`.
5. Refatore todos os componentes (como `Dashboard.tsx`) para importar de `src/services/apiService.ts` em vez de diretamente do mock.

Critérios de Aceitação:
- Os componentes não devem mais ter referências diretas ao `mockApiService.ts`.
- Todas as importações de serviço devem apontar para `src/services/apiService.ts`.
- A aplicação deve continuar funcionando normalmente com o mock, provando que a abstração foi bem-sucedida.
- O código está pronto para a troca de serviço com a simples alteração de uma variável de ambiente.
```

---

## 8. Exemplo Completo: Tela de Login

Vamos aplicar a estratégia a uma tela de login.

### Prompt Único (Combinando Fases)

```
Persona: Você é um desenvolvedor full-stack encarregado de criar uma tela de login funcional de ponta a ponta (apenas front-end por enquanto).

Contexto: Precisamos criar a tela de login completa. O back-end não está pronto, então usaremos a estratégia "Mock-First".

Input:
- Screenshot da tela de login do Figma (campos: email, senha; botão: "Entrar").
- Endpoint da API de login (POST `/api/auth/login`) e sua estrutura de dados esperada (request e response).

Tecnologia:
- Framework: React com TypeScript e Vite
- Estilização: Tailwind CSS
- Gerenciamento de Formulário: React Hook Form

Tarefa:
1. **Componente Visual:** Crie o componente `LoginPage.tsx` com os campos de email, senha e o botão, estilizados conforme o Figma.
2. **Mock Service:** Crie um `mockApiService.ts` com uma função `login(email, password)`. Esta função deve:
   - Retornar uma Promise.
   - Simular um atraso de 1 segundo.
   - Se o email for `teste@email.com` e a senha `123456`, resolver a Promise com um token de usuário falso: `{ token: 'fake-jwt-token', user: { name: 'Usuário Teste' } }`.
   - Caso contrário, rejeitar a Promise com uma mensagem de erro "Credenciais inválidas".
3. **Gerenciamento de Estado e Formulário:**
   - Use o `React Hook Form` para gerenciar os campos do formulário, incluindo validação (ex: email válido, senha com mínimo de 6 caracteres).
   - Crie um estado para `isSubmitting` para desabilitar o botão durante a chamada da API.
   - Ao submeter o formulário, chame a função `login` do mock service.
4. **Feedback ao Usuário:**
   - Se o login for bem-sucedido, exiba um alerta de sucesso e redirecione o usuário (simule com `console.log`).
   - Se falhar, exiba a mensagem de erro abaixo do formulário.

Critérios de Aceitação:
- A tela de login deve ser visualmente idêntica ao Figma.
- A validação do formulário deve funcionar antes da submissão.
- O botão "Entrar" deve ficar desabilitado durante a submissão.
- O login com as credenciais corretas deve mostrar uma mensagem de sucesso.
- O login com credenciais erradas deve mostrar uma mensagem de erro.
- Toda a lógica de dados deve passar pelo mock service.
```

---

## 9. Dicas e Boas Práticas

- **Seja Específico:** Quanto mais detalhes do Figma você fornecer (cores exatas, nomes de fontes, valores de `rem` ou `px`), melhor será o resultado.
- **Itere:** Não espere que a IA acerte tudo de primeira. Gere um componente, veja o resultado e refine com um novo prompt: "Ótimo, agora ajuste o espaçamento entre o título e a descrição para 16px e aumente a sombra do card."
- **Use Ferramentas de Figma para Código:** Plugins como "Figma to Code" podem gerar um HTML/CSS básico que serve como um excelente ponto de partida para o seu prompt.
- **Separe Responsabilidades:** Use prompts diferentes para estrutura (HTML), estilo (CSS) e lógica (JavaScript/TypeScript). Isso geralmente produz resultados mais limpos.
- **Forneça o Código Existente:** Ao refinar ou adicionar features, sempre forneça o código atual no prompt para que a IA tenha o contexto completo.

---

*Documento criado por Manus AI Assistant*  
*Última atualização: Outubro 2024*  
*Versão: 1.0*

