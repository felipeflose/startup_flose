const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

const getJiraAuthHeader = () => ({
  'Authorization': `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

// Role-specific task templates per agent function
const ROLE_TASKS = {
  'CEO': {
    epic: 'Processos Ágeis',
    tasks: [
      { summary: 'Revisão estratégica de OKRs do trimestre', description: 'Avaliar progresso dos objetivos e ajustar metas conforme resultados.' },
      { summary: 'Reunião de alinhamento com stakeholders', description: 'Apresentar status da empresa e coletar feedback de investidores e parceiros.' },
      { summary: 'Definir roadmap de produto para próximo semestre', description: 'Consolidar prioridades de produto com base em dados de mercado e feedback de clientes.' },
    ]
  },
  'CTO': {
    epic: 'Infraestrutura & Tecnologia',
    tasks: [
      { summary: 'Revisão de arquitetura do sistema principal', description: 'Avaliar pontos de falha, gargalos e oportunidades de evolução da stack técnica.' },
      { summary: 'Auditoria de dívida técnica do repositório', description: 'Mapear todos os módulos com alta complexidade ciclomática e criar plano de refatoração.' },
      { summary: 'Definir padrões de engenharia e guardrails de código', description: 'Documentar e disseminar boas práticas, linters e CI gates obrigatórios.' },
    ]
  },
  'COO': {
    epic: 'Processos Ágeis',
    tasks: [
      { summary: 'Mapeamento de capacidade operacional do time', description: 'Calcular disponibilidade de horas por sprint por área.' },
      { summary: 'Revisão de processos internos de entrega', description: 'Identificar gargalos no fluxo de trabalho e propor melhorias.' },
      { summary: 'Plano de contingência para deploys em produção', description: 'Definir runbook de rollback e responsáveis por incidentes críticos.' },
    ]
  },
  'Diretora de Design': {
    epic: 'Design & Produto',
    tasks: [
      { summary: 'Auditoria do design system atual', description: 'Revisar tokens, componentes e consistência visual em todos os produtos.' },
      { summary: 'Pesquisa de UX com usuários reais', description: 'Conduzir 5 entrevistas de usabilidade e sintetizar insights.' },
      { summary: 'Criar protótipo de nova tela de onboarding', description: 'Redesenhar o fluxo de primeiro acesso com foco em retenção D1.' },
    ]
  },
  'Gerente de Engenharia': {
    epic: 'Processos Ágeis',
    tasks: [
      { summary: 'Conduzir Sprint Planning com o time de engenharia', description: 'Facilitar estimativas, definir meta da sprint e distribuir responsabilidades.' },
      { summary: 'Avaliação de performance dos desenvolvedores sênior', description: 'Compilar métricas de entrega, qualidade e colaboração para feedback individual.' },
      { summary: 'Definir critérios de promoção para Tech Lead', description: 'Documentar competências técnicas e comportamentais esperadas para evolução de carreira.' },
    ]
  },
  'Scrum Master': {
    epic: 'Processos Ágeis',
    tasks: [
      { summary: 'Facilitar retrospectiva da Sprint atual', description: 'Aplicar formato de retrospectiva e gerar plano de ação com itens rastreáveis.' },
      { summary: 'Remover impedimentos técnicos do backlog', description: 'Identificar dependências externas bloqueando entregas e acionar responsáveis.' },
      { summary: 'Atualizar métricas de velocity do time', description: 'Calcular velocity das últimas 3 sprints e projetar capacidade da próxima.' },
    ]
  },
  'QA': {
    epic: 'Melhorias Internas',
    tasks: [
      { summary: 'Implementar testes de regressão automatizados', description: 'Criar suite de testes E2E para os fluxos críticos de autenticação e pagamento.' },
      { summary: 'Análise de cobertura de código atual', description: 'Mapear módulos sem cobertura de testes e priorizar por risco de negócio.' },
      { summary: 'Elaborar plano de testes para próxima release', description: 'Detalhar cenários de teste, critérios de aceite e responsáveis.' },
    ]
  },
  'UX': {
    epic: 'Design & Produto',
    tasks: [
      { summary: 'Redesenhar fluxo de cadastro para mobile', description: 'Otimizar o formulário de criação de conta para dispositivos touch com foco em conversão.' },
      { summary: 'Criar biblioteca de ícones customizados', description: 'Desenvolver set de ícones no estilo da marca para uso no design system.' },
      { summary: 'Mapear jornada do usuário no painel administrativo', description: 'Identificar pontos de fricção no dashboard usando heatmaps e gravações.' },
    ]
  },
  'DBA': {
    epic: 'Infraestrutura & Tecnologia',
    tasks: [
      { summary: 'Otimizar queries lentas no banco de produção', description: 'Analisar slow query log e criar índices para as 10 consultas mais custosas.' },
      { summary: 'Implementar estratégia de backup automático diário', description: 'Configurar backup incremental com retenção de 30 dias e alertas de falha.' },
      { summary: 'Plano de migração de schema para nova versão', description: 'Elaborar script de migração reversível com zero downtime para produção.' },
    ]
  },
  'SecOps': {
    epic: 'Infraestrutura & Tecnologia',
    tasks: [
      { summary: 'Auditoria de vulnerabilidades OWASP Top 10', description: 'Executar varredura nas APIs públicas e gerar relatório de riscos com severidade.' },
      { summary: 'Implementar MFA obrigatório para acessos administrativos', description: 'Configurar autenticação multifator para todos os acessos ao painel de admin.' },
      { summary: 'Revisar permissões de acesso por perfil de usuário', description: 'Aplicar princípio do menor privilégio em todos os roles da aplicação.' },
    ]
  },
  'Tech Writer': {
    epic: 'Melhorias Internas',
    tasks: [
      { summary: 'Documentar API REST no formato OpenAPI 3.0', description: 'Gerar spec completa dos endpoints públicos com exemplos de request/response.' },
      { summary: 'Criar guia de início rápido para novos desenvolvedores', description: 'Redigir README com setup local, variáveis de ambiente e fluxo de contribuição.' },
      { summary: 'Atualizar documentação do fluxo de deploy', description: 'Revisar runbook de deploy e adicionar seção de troubleshooting com casos comuns.' },
    ]
  },
  'DevOps': {
    epic: 'Infraestrutura & Tecnologia',
    tasks: [
      { summary: 'Configurar pipeline CI/CD com testes automatizados', description: 'Implementar GitHub Actions com stages de lint, teste, build e deploy.' },
      { summary: 'Monitorar e otimizar custos de infraestrutura cloud', description: 'Analisar billing do mês e identificar recursos ociosos para redução de custo.' },
      { summary: 'Implementar alertas de SLA via Telegram', description: 'Configurar notificações automáticas para downtime, alta latência e erros 5xx.' },
    ]
  },
  'Game': {
    epic: 'Entretenimento & Games',
    tasks: [
      { summary: 'Implementar sistema de pontuação do jogo da velha', description: 'Desenvolver lógica de verificação de vitória, empate e placar persistente.' },
      { summary: 'Criar modo multiplayer online assíncrono', description: 'Implementar salas de jogo com websockets e sincronização de estado em tempo real.' },
      { summary: 'Adicionar animações e efeitos sonoros ao jogo', description: 'Integrar biblioteca de animação CSS e SFX para feedback visual nas jogadas.' },
    ]
  },
  'Game Designer': {
    epic: 'Entretenimento & Games',
    tasks: [
      { summary: 'Criar documento de design de novos modos de jogo', description: 'Especificar regras, mecânicas e balanceamento para modo torneio e modo co-op.' },
      { summary: 'Mapear jornada do jogador e progressão de dificuldade', description: 'Definir curva de dificuldade e sistema de recompensas para retenção de jogadores.' },
      { summary: 'Prototipar sistema de conquistas e badges', description: 'Criar especificação de 20 conquistas com critérios e arte conceitual.' },
    ]
  },
  'Organizador': {
    epic: 'Gestão de Pessoas',
    tasks: [
      { summary: 'Revisar estrutura organizacional do trimestre', description: 'Atualizar organograma, responsabilidades e linha de reporte de cada área.' },
      { summary: 'Implementar processo de onboarding estruturado', description: 'Criar trilha de onboarding de 30/60/90 dias para novos contratados.' },
      { summary: 'Organizar calendário de eventos internos da empresa', description: 'Planejar all-hands, team buildings e workshops para o próximo trimestre.' },
    ]
  },
  'Facilities': {
    epic: 'Gestão de Pessoas',
    tasks: [
      { summary: 'Vistoria e manutenção preventiva do escritório', description: 'Realizar checklist mensal de equipamentos, rede e infraestrutura física.' },
      { summary: 'Organizar layout das mesas por squad', description: 'Reorganizar espaço físico para otimizar colaboração entre times.' },
      { summary: 'Gestão de inventário de equipamentos de TI', description: 'Atualizar planilha de patrimônio com número de série, responsável e estado de cada equipamento.' },
    ]
  },
  'Tech Lead': {
    epic: 'Melhorias Internas',
    tasks: [
      { summary: 'Conduzir code review da feature branch principal', description: 'Revisar PRs abertos, dar feedback construtivo e garantir qualidade antes do merge.' },
      { summary: 'Definir padrões de arquitetura para novo módulo', description: 'Documentar decisões de design e ADRs (Architecture Decision Records) para o time.' },
      { summary: 'Mentoria técnica com desenvolvedores juniores', description: 'Realizar sessão de pair programming e code review comentado com foco em aprendizado.' },
    ]
  },
  'QA Lead': {
    epic: 'Melhorias Internas',
    tasks: [
      { summary: 'Estabelecer Definition of Done para o time de QA', description: 'Definir critérios mínimos de qualidade que toda entrega deve satisfazer.' },
      { summary: 'Implementar processo de QA gate no pipeline de CI', description: 'Bloquear merges que quebrem testes críticos ou reduzam cobertura abaixo do threshold.' },
      { summary: 'Criar relatório de qualidade semanal para gestão', description: 'Compilar métricas de bugs abertos, taxa de regressão e cobertura de testes por sprint.' },
    ]
  },
  'Product Owner': {
    epic: 'Processos Ágeis',
    tasks: [
      { summary: 'Priorizar backlog do produto para próxima sprint', description: 'Ordenar itens por valor de negócio, risco técnico e esforço estimado.' },
      { summary: 'Escrever user stories com critérios de aceite claros', description: 'Detalhar histórias em formato "Como X, quero Y, para Z" com ACs testáveis.' },
      { summary: 'Apresentar demo de features concluídas para stakeholders', description: 'Preparar demonstração da sprint com métricas de impacto e próximos passos.' },
    ]
  },
  'default': {
    epic: 'Melhorias Internas',
    tasks: [
      { summary: 'Documentar processos e responsabilidades do cargo', description: 'Criar documento descritivo das atividades, ferramentas e entregas esperadas da função.' },
      { summary: 'Identificar melhorias no processo de trabalho atual', description: 'Mapear ineficiências no fluxo diário e propor automações ou simplificações.' },
      { summary: 'Participar de treinamento técnico e atualização de skills', description: 'Completar curso ou workshop relevante para a área e compartilhar aprendizados com o time.' },
    ]
  }
};

function getRoleTemplate(agent) {
  const role = (agent.role || '').toLowerCase();
  if (role.includes('ceo') || role.includes('chief executive')) return ROLE_TASKS['CEO'];
  if (role.includes('cto') || role.includes('chief tech')) return ROLE_TASKS['CTO'];
  if (role.includes('coo') || role.includes('operações') || role.includes('operations')) return ROLE_TASKS['COO'];
  if (role.includes('design') && (role.includes('dir') || role.includes('ux') && !role.includes('sênior'))) return ROLE_TASKS['Diretora de Design'];
  if (role.includes('gerente') && role.includes('engenhar')) return ROLE_TASKS['Gerente de Engenharia'];
  if (role.includes('scrum') || role.includes('agile')) return ROLE_TASKS['Scrum Master'];
  if (role.includes('qa lead') || role.includes('lead') && role.includes('qa')) return ROLE_TASKS['QA Lead'];
  if (role.includes('qa') || role.includes('qualidade') || role.includes('garantia')) return ROLE_TASKS['QA'];
  if (role.includes('ux') || (role.includes('design') && role.includes('sênior'))) return ROLE_TASKS['UX'];
  if (role.includes('dba') || role.includes('banco de dados')) return ROLE_TASKS['DBA'];
  if (role.includes('sec') || role.includes('segurança') || role.includes('security')) return ROLE_TASKS['SecOps'];
  if (role.includes('tech writer') || role.includes('documentação') || role.includes('escritora')) return ROLE_TASKS['Tech Writer'];
  if (role.includes('devops') || role.includes('cloud') || role.includes('infraestrutura') && role.includes('engenh')) return ROLE_TASKS['DevOps'];
  if (role.includes('game') && role.includes('design')) return ROLE_TASKS['Game Designer'];
  if (role.includes('game') || role.includes('jogo')) return ROLE_TASKS['Game'];
  if (role.includes('organizacional') || role.includes('organizador')) return ROLE_TASKS['Organizador'];
  if (role.includes('facilities') || role.includes('infraestrutura física')) return ROLE_TASKS['Facilities'];
  if (role.includes('tech lead') || role.includes('lead de engenh')) return ROLE_TASKS['Tech Lead'];
  if (role.includes('product owner') || role.includes('po sênior')) return ROLE_TASKS['Product Owner'];
  if (role.includes('frontend') || role.includes('backend') || role.includes('fullstack') || role.includes('desenvolv')) return ROLE_TASKS['default'];
  if (role.includes('diretor') || role.includes('governança')) return ROLE_TASKS['Gerente de Engenharia'];
  return ROLE_TASKS['default'];
}

async function getOrCreateEpicKey(epicName, headers) {
  const search = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
    headers,
    params: { jql: `project = KAN AND issuetype = Epic AND summary ~ "${epicName}"`, maxResults: 1, fields: 'summary' }
  });
  if (search.data?.issues?.length > 0) return search.data.issues[0].key;
  return null;
}

async function createCard(summary, description, epicKey, agentName, headers) {
  const body = {
    fields: {
      project: { key: 'KAN' },
      summary,
      description: {
        type: 'doc', version: 1,
        content: [{ type: 'paragraph', content: [{ text: description, type: 'text' }] }]
      },
      parent: epicKey ? { key: epicKey } : undefined,
      issuetype: { name: 'Task' }
    }
  };
  const res = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, body, { headers });
  return res.data?.key;
}

async function main() {
  const headers = getJiraAuthHeader();
  const agents = JSON.parse(fs.readFileSync(path.join(__dirname, 'agents_db.json'), 'utf8')).filter(a => !a.fired);

  const assignmentsFile = path.join(__dirname, 'task_assignments.json');
  const creatorsFile = path.join(__dirname, 'task_creators.json');
  let assignments = {};
  let creators = {};
  try { assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8')); } catch (e) {}
  try { creators = JSON.parse(fs.readFileSync(creatorsFile, 'utf8')); } catch (e) {}

  // Count current tasks per agent
  const taskCounts = {};
  agents.forEach(a => { taskCounts[a.name] = 0; });
  Object.values(assignments).forEach(name => {
    if (taskCounts[name] !== undefined) taskCounts[name]++;
  });

  console.log('\n📊 Current task distribution:');
  agents.forEach(a => console.log(`  ${a.avatar} ${a.name} (${a.role.split('(')[0].trim()}): ${taskCounts[a.name] || 0} cards`));

  const epicCache = {};
  let totalCreated = 0;

  for (const agent of agents) {
    const currentCount = taskCounts[agent.name] || 0;
    if (currentCount >= 3) {
      console.log(`\n✅ ${agent.name} já tem ${currentCount} cards — ok`);
      continue;
    }

    const template = getRoleTemplate(agent);
    const needed = 3 - currentCount;
    const tasksToCreate = template.tasks.slice(0, needed);

    console.log(`\n🔨 Criando ${tasksToCreate.length} cards para ${agent.avatar} ${agent.name} (${agent.role.split('(')[0].trim()})...`);

    // Get epic key (cached)
    if (!epicCache[template.epic]) {
      epicCache[template.epic] = await getOrCreateEpicKey(template.epic, headers);
    }
    const epicKey = epicCache[template.epic];

    for (const task of tasksToCreate) {
      try {
        const key = await createCard(task.summary, task.description, epicKey, agent.name, headers);
        if (key) {
          assignments[key] = agent.name;
          creators[key] = agent.name;
          totalCreated++;
          console.log(`  ✅ ${key} — ${task.summary}`);
        }
      } catch (e) {
        console.error(`  ❌ Falha: ${e.message}`);
      }
    }
  }

  // Save assignments and creators
  fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');
  fs.writeFileSync(creatorsFile, JSON.stringify(creators, null, 2), 'utf8');

  console.log(`\n🎉 Concluído! ${totalCreated} cards criados e atribuídos no Jira.`);
}

main();
