# Flose Startup Simulator Enhancement Walkthrough

Toda a simulação de agentes autônomos e controle corporativo foi otimizada para ser robusta, dinâmica e real. Abaixo estão os detalhes das entregas realizadas:

---

## 🛠️ Mudanças Realizadas

### 1. Robustez do Motor de IA (Gemma 4)
- **Timeouts estendidos**: O limite de espera das chamadas ao Ollama foi ampliado de 25s/30s para **120s**, garantindo que inferências mais lentas em hardware sem GPU dedicada não sejam abortadas de forma precoce.
- **Lista de Prioridades de Modelo**: Adicionado um fallback automático estruturado: `['gemma4-fast:latest', 'gemma4-prod:latest', 'gemma4:latest']`.
- **Prevenção de Swapping**: Padronizado o uso de `gemma4-fast:latest` como modelo preferencial em todos os scripts (`server.cjs`, `gemma4_autonomous_pipeline.cjs`, `po_frenetic_analyzer.cjs`) para garantir que o modelo permaneça carregado na RAM do Ollama, eliminando atrasos causados pelo carregamento e descarregamento de múltiplos modelos da memória física.

### 2. Evidência & Git Concurrency Fixes
- **Patch de Heads com Retry**: A gravação de commits no GitHub via API REST agora conta com um algoritmo robusto de **auto-retry de até 5 tentativas**. Se múltiplos scripts tentarem atualizar o ponteiro do branch `feature/KAN-5648-implementar-melhorias-continuas` simultaneamente, a falha de "not a fast-forward" é capturada, a última referência é re-obtida, a árvore de commit é reconstruída e a atualização é enviada novamente, garantindo que nenhum card fique sem commit de evidência no GitHub.

### 3. Painel de Atividade em Tempo Real (Live Pulse)
- **Server-Sent Events (SSE)**: Implementado canal SSE nativo no backend (`GET /api/activity/stream`) com gerenciamento automático de conexão e desconexão de clientes.
- **Log centralizado**: Criado endpoint `POST /api/activity` que permite que os scripts de background (pipeline e analisador de PO) registrem suas ações em tempo real no servidor central.
- **CompanyPulse Upgraded**: O componente de status da empresa no Dashboard foi atualizado para escutar o stream SSE. As ações de POs, Desenvolvedores e QA aparecem instantaneamente na tela sem a necessidade de polling de 4 segundos.

### 4. Debates Automáticos Agendados
- **Auto-Debate Scheduler**: Adicionado um scheduler em background no backend (`runAutoDebateScheduler`) que executa a cada 120s. Ele localiza as tarefas pendentes (`To Do / Backlog`) geradas pelo Gemma 4 no Jira, reúne automaticamente o CEO, o CTO, o PO criador do card, o desenvolvedor designado e inicia a "Chamber de Decisão" de forma totalmente autônoma, gerando as discussões e movendo os cards pela esteira sem intervenção do usuário.

### 5. Visualizador de Protótipos 100% Dinâmico
- **Preview Endpoint**: Criado endpoint `/api/prototype/:cardId` no backend que mapeia o código escrito pelos agentes nos arquivos de simulação.
- **Babel Standalone Compilation**: Se o código gerado for um componente React (`.tsx` / `.jsx`), o endpoint serve uma página especial que carrega React, ReactDOM e o **Babel Compiler** no browser dentro do iframe, compilando o TypeScript in-browser e montando o componente raiz dinamicamente!
- **Leitura Real de Código**: Atualizado o `PrototypeViewer.tsx` para carregar esse iframe com CSP segura (`sandbox="allow-scripts allow-same-origin"`).
- **Aba de Código Fonte Real**: Atualizada a aba "Código" no visualizador para fazer uma requisição real a `/api/code` e renderizar na tela o código gerado pela IA.

### 6. 🏢 Simulador Virtual de Escritório 2D Interativo (Office Map)
- **Movimento e Vida Real**: Criado o componente `OfficeMap.tsx` que simula a planta baixa do escritório. Cada agente é representado por um avatar de emoji que se move dinamicamente pela tela de acordo com seu status operacional real.
- **Balões de Pensamento (Speech Bubbles)**: Os colaboradores exibem balões de pensamento com reflexões reais baseadas no status de seus cards de demanda.
- **Bobbing Walking Effect**: Adicionada física visual leve com animação de passada de passos (bobbing vertical) nos avatares que estão caminhando.
- **Gaveta de Informações**: Ao passar o mouse sobre qualquer avatar, uma gaveta flutuante exibe a foto do colaborador, cargo, nível de senioridade e status de disponibilidade ao vivo.

### 7. 🎯 Ativação do Analisador Frenético de POs
- **Ativação no Startup**: Integramos e ativamos a rotina `startRoutine()` do analisador diretamente na inicialização do `server.cjs`. Agora, os POs analisam o código do próprio simulador a cada 60 segundos e geram continuamente demandas reais de melhorias para a empresa.

### 8. ⚖️ Auditoria Automática de Cargos e Atribuições
- **O Motor de Auditoria (`role_attribution_auditor.cjs`)**: Criamos um analisador de governança que roda a cada 60s no servidor. Ele verifica todos os cards ativos no Jira e valida se o executor alocado tem atribuição técnica para aquele tipo de tarefa de acordo com seu cargo.
- **Ações de Cobrança e Correção**: Reatribui automaticamente o card no Jira para um executor qualificado, aplica uma advertência ao colaborador no perfil dele no banco e penaliza o score.

### 9. 👑 O CEO Supremo e Recrutamento Dinâmico (Sob Demanda)
- **Fired de Todos os Agentes**: Demitimos todos os 35 funcionários originais da Flose Startup de forma global, deixando única e exclusivamente o **CEO Felipe Flose** ativo na empresa.
- **Capacidade Autônoma de Contratação e Delegação**: Se houver alguma demanda sem executor ativo, o CEO reativa dinamicamente os colaboradores sob demanda para atuar.

### 10. 🕸️ Recrutamento Hierárquico em Cascata (C-Level -> Diretor -> Coordenador -> Especialista)
- **A Regra Corporativa**: Respeitando a estrutura da cadeia de comando, a contratação de profissionais técnicos não ocorre mais de forma direta pelo CEO. O fluxo é recursivo de cima para baixo.
- **Notificação em Tempo Real**: Cada contratação da cadeia de comando dispara um evento SSE que aparece no feed do simulador com o responsável real pela admissão.

### 11. ⚡ Sincronização SSE em Tempo Real no Mapa do Escritório (Live Feedback)
- **Comportamento ao Vivo**: No exato milissegundo em que a IA (PO, Dev, QA) executa uma ação no pipeline em background e envia para os logs do servidor, o avatar correspondente no mapa do escritório **exibe instantaneamente o balão com o texto exato da ação** que está executando ao vivo e **caminha imediatamente para o local da ação**.

### 12. 🔧 Correção de Listagem de Desligados (Fired Members Bug)
- **A Correção**: Modificado o endpoint `GET /api/agents` no `server.cjs` para retornar a lista de agentes na íntegra. Atualizado `App.tsx` para filtrar os ativos onde for pertinente (`OrgChart`, `CompanyPulse`).

### 13. 📑 Motivo Detalhado de Desligamento (Fired Reason Tracking)
- **A Solução**: Adicionado o campo `firedReason` na estrutura de dados do colaborador. O sistema grava o motivo exato em todos os fluxos de demissão.

### 14. 👶 Contratação de Juniores & Estagiários e Formação Pair-Programming (Mentoria Ativa)
- **Novo Colaborador**: Cadastrado **Felipe Viana Flose** no banco sob o cargo de **Estagiário de Engenharia & IA** (`id: felipe_intern`).
- **Cadastramento de Juniores**: Adicionados novos perfis de desenvolvedores Juniores ao banco (ex: `Ana Clara Junior` e `Lucas Junior`).
- **Política de Formação (`junior_training_policy.md`)**: Criado o documento [junior_training_policy.md](file:///Users/felipeflose/Startup_Flose/junior_training_policy.md) e implementado o pair-programming autônomo.
- **Atualização do Organograma**: Expandido o componente `OrgChart.tsx` para renderizar os níveis de **Júnior** e **Estagiário** no final da árvore organizacional, com cores dedicadas (Roxo e Rosa).

### 15. ⚖️ Regra de Mentoria Rígida e Promoção (Demissão de Gestores Negligentes)
- **A Regra de Ouro**: Gestores, Coordenadores e Gerentes são inteiramente responsáveis pelo ensino e evolução de seus juniores e estagiários. Se falharem, são demitidos de forma sumária pela Governança.
- **Promoções Automáticas**: Toda vez que o score de performance de um Júnior ou Estagiário atinge **75 pontos**, o Auditor realiza a promoção automática de nível.
- **Demissão de Gestores por Negligência**: Se um Júnior/Estagiário tiver rendimento crítico (score inferior a **35 pontos**), o Gestor da respectiva área recebe advertência de mentoria. Ao acumular 2 advertências, é demitido sumariamente.

### 16. 👑 Promoção a Dono & CEO e Reset Corporativo Completo (Zerar Empresa)
- **Promoção de Felipe Viana Flose**: O colaborador `Felipe Viana Flose` (antigo estagiário) foi promovido ao cargo mais alto da corporação: **Dono & CEO (Chief Executive Officer)**, com nível `C-Level` e avatar de coroa real `👑`.
- **Desligamento do Ex-CEO**: O antigo executivo simulado `Felipe Flose` foi sumariamente demitido e rebaixado para `Ex-CEO`.
- **Reset Geral (Zerar Empresa)**: Todos os outros 35+ agentes foram desligados de forma global.
- **Nova Esteira de Contratação Autônoma**: Com a empresa zerada, apenas o Dono `Felipe Viana Flose` inicia o dia de trabalho. A esteira autônoma cria novos cards e contrata os diretores, gerentes, seniores e juniores de forma gradual e hierárquica em cascata a partir do zero absoluto.

### 17. 🤝 Motor de Recrutamento & Seleção com Entrevistas e Transcrições (Gemma 4 a Todo Vapor)
- **O Problema**: A contratação ocorria de forma instantânea e silenciosa no banco de dados, sem visibilidade das dinâmicas de decisão e análises de backlog da startup.
- **A Solução**: Criado o novo motor [hiring_recruitment_engine.cjs](file:///Users/felipeflose/Startup_Flose/hiring_recruitment_engine.cjs) integrado no boot do servidor.
- **Backlog Analysis**: O motor varre o backlog analiticamente. Se encontra um card técnico sem executor ativo (ou atribuído a um funcionário desligado), ele abre uma **Tarefa de Recrutamento Oficial no Jira** com a etiqueta `[Recrutamento]`.
- **Comitê de Seleção & Entrevistas**: Em seguida, o motor aciona o comitê no Chamber, convocando:
  1. **Felipe Viana Flose** (Dono & CEO) `👑`
  2. **Gemma Tech** (CTO) `💻`
  3. **Hugo Organizador** (Gerente de RH) `👔`
- **Simulação da Entrevista Técnica e Comportamental**: Através do Gemma 4, o comitê entrevista e avalia detalhadamente os perfis e currículos de dois candidatos desligados qualificados para a vaga. O comitê debate, argumenta sobre os pontos fortes e limitações de cada um, e o Dono e CEO toma a decisão final.
- **Transcrições no Jira**: O comitê **posta a transcrição completa da entrevista de seleção em formato de diálogo diretamente nos comentários da tarefa de Recrutamento no Jira**, move o card de Recrutamento para Concluído, admite o candidato vencedor no banco, recontrata o junior correspondente para pareamento de mentoria (se for dev) e delega o card técnico original para ele começar a trabalhar!
