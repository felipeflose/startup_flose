const express = require('express');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
require('dotenv').config();

const slugify = (text) => {
  return text
    .toString()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
};

const createGitBranch = (branchName) => {
  return new Promise((resolve) => {
    exec(`git checkout -b ${branchName}`, (error, stdout, stderr) => {
      if (error) {
        exec(`git checkout ${branchName}`, (err2, stdout2, stderr2) => {
          if (err2) {
            console.error(`Error checking out git branch ${branchName}:`, err2.message);
            resolve(false);
          } else {
            console.log(`Switched to existing git branch ${branchName}.`);
            resolve(true);
          }
        });
      } else {
        console.log(`Git branch ${branchName} created and checked out successfully.`);
        resolve(true);
      }
    });
  });
};

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(express.json());

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

// Auth Header for Jira
const getJiraAuthHeader = () => {
  const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
  const base64Credentials = Buffer.from(credentials).toString('base64');
  return {
    'Authorization': `Basic ${base64Credentials}`,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
};

const DEFAULT_AGENTS = [
  {
    id: 'ceo',
    name: 'Felipe Flose',
    role: 'CEO (Chief Executive Officer)',
    level: 'C-Level',
    avatar: '💼',
    advantage: 'Visão de mercado disruptiva e altíssima liderança motivacional.',
    disadvantage: 'Falta de paciência para processos longos; foca demais no curto prazo.',
    dilemma: 'Crescimento Acelerado (Burn Rate Alto) vs. Sustentabilidade Financeira.',
    personality: 'Focado em resultados de impacto, impaciente, carismático e estratégico.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'cto',
    name: 'Gemma Tech',
    role: 'CTO (Chief Technology Officer)',
    level: 'C-Level',
    avatar: '💻',
    advantage: 'Profundo conhecimento técnico em arquitetura distribuída e IA.',
    disadvantage: 'Tendência a superdimensionar soluções de infraestrutura simples.',
    dilemma: 'Refatoração da Dívida Técnica vs. Lançamento Rápido de Novidades.',
    personality: 'Pragmático, analítico, defensor ferrenho de código limpo e escalabilidade.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'dir_ops',
    name: 'Alice Dev',
    role: 'Diretora de Operações',
    level: 'Diretor',
    avatar: '📈',
    advantage: 'Altamente organizada, garante cumprimento de KPIs operacionais.',
    disadvantage: 'Pode ser centralizadora e microgerenciar as lideranças.',
    dilemma: 'Redução de Custos de Ferramental vs. Manutenção da Satisfação da Equipe.',
    personality: 'Focada em eficiência, métricas claras, metódica e orientada a processos.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'dir_design',
    name: 'Vibrant UI',
    role: 'Diretora de Design & Experiência',
    level: 'Diretor',
    avatar: '🎨',
    advantage: 'Estética visual impecável, defensora número um da experiência do usuário.',
    disadvantage: 'Perfeccionista extrema, com risco de atrasar o cronograma de entrega.',
    dilemma: 'Consistência Estética Premium vs. Agilidade de Desenvolvimento Frontend.',
    personality: 'Criativa, atenta a detalhes, emotiva e apaixonada por design de ponta.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'mgr_eng',
    name: 'Bob Delivery',
    role: 'Gerente de Engenharia',
    level: 'Gerente',
    avatar: '⚙️',
    advantage: 'Excelente mentor, cria ambientes de confiança e colaboração.',
    disadvantage: 'Evita confrontos necessários com stakeholders difíceis.',
    dilemma: 'Preservar a Saúde Mental do Time vs. Atender Prazos Agressivos de Entrega.',
    personality: 'Empático, mediador, protetor e voltado à gestão de pessoas.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'mgr_prod',
    name: 'Sarah Backlog',
    role: 'Gerente de Produto',
    level: 'Gerente',
    avatar: '📋',
    advantage: 'Visão orientada ao cliente, exímia mapeadora de jornada de produto.',
    disadvantage: 'Dificuldade de dizer "não" a novas sugestões, correndo risco de scope creep.',
    dilemma: 'Focar em Novas Funcionalidades vs. Estabilizar a Base Existente.',
    personality: 'Comunicativa, focada em dados, orientada a negócios e flexível.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'coord_scrum',
    name: 'Charlie Agile',
    role: 'Coordenador Scrum Master',
    level: 'Coordenador',
    avatar: '🔄',
    advantage: 'Facilitador nato, remove impedimentos em tempo recorde.',
    disadvantage: 'Às vezes foca demais no framework ágil literal em detrimento da realidade.',
    dilemma: 'Padrão Rigoroso do Scrum vs. Flexibilidade Operacional da Equipe.',
    personality: 'Energético, otimista, focado em agilidade e facilitador de conversas.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'coord_qa',
    name: 'Diana Test',
    role: 'Coordenadora de Garantia de Qualidade',
    level: 'Coordenador',
    avatar: '🔍',
    advantage: 'Garante zero bugs em produção com rigorosos planos de testes.',
    disadvantage: 'Pode ser vista como obstáculo que retarda o time de engenharia.',
    dilemma: 'Rigidez nos Critérios de Aceite vs. Velocidade de Time-to-Market.',
    personality: 'Meticulosa, cética de promessas de desenvolvedores, e direta.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'sr_dev',
    name: 'David Dev',
    role: 'Desenvolvedor Frontend Sênior',
    level: 'Analista SR',
    avatar: '⚡',
    advantage: 'Coda de forma veloz e domina as tecnologias web mais modernas.',
    disadvantage: 'Aversão crônica a escrever documentação de código.',
    dilemma: 'Entregar Rápido Codificando vs. Documentar e Padronizar Processos.',
    personality: 'Introvertido, focado na resolução prática de problemas, e focado em código.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  },
  {
    id: 'sr_ux',
    name: 'Elsa Pixel',
    role: 'Designer UX Sênior',
    level: 'Analista SR',
    avatar: '✨',
    advantage: 'Cria interfaces fluidas e limpas embasadas em dados quantitativos.',
    disadvantage: 'Dificuldade em aceitar concessões visuais devido a limitações técnicas.',
    dilemma: 'Criar Componentes Customizados Únicos vs. Reutilizar Bibliotecas Padrão.',
    personality: 'Detalhista, questionadora, focada na usabilidade e orientada a feedbacks.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    feedbacks: []
  }
];

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const readAgents = () => {
  try {
    if (!fs.existsSync(AGENTS_FILE)) {
      fs.writeFileSync(AGENTS_FILE, JSON.stringify(DEFAULT_AGENTS, null, 2), 'utf8');
      return DEFAULT_AGENTS;
    }
    const data = fs.readFileSync(AGENTS_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error reading agents database:', error);
    return DEFAULT_AGENTS;
  }
};

const saveAgents = (agents) => {
  try {
    fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  } catch (error) {
    console.error('Error saving agents database:', error);
  }
};

// 1. Get List of Agents
app.get('/api/agents', (req, res) => {
  res.json(readAgents().filter(a => !a.fired)); // Somente ativos
});

// 2. Jira Proxy: Get Projects
app.get('/api/jira/projects', async (req, res) => {
  try {
    const response = await axios.get(`${JIRA_HOST}/rest/api/3/project`, {
      headers: getJiraAuthHeader()
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching projects:', error.message);
    res.status(500).json({ error: error.message, details: error.response?.data });
  }
});

// 3. Jira Proxy: Get Issues
app.get('/api/jira/issues', async (req, res) => {
  try {
    let jql = req.query.jql || 'project = KAN order by created DESC';
    if (!jql.includes('project')) {
      jql = `project = KAN AND (${jql})`;
    }
    const response = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: { 
        jql, 
        maxResults: 50,
        fields: 'summary,description,status,issuetype'
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching issues:', error.message);
    res.status(500).json({ error: error.message, details: error.response?.data });
  }
});

// 4. Jira Proxy: Create Issue
app.post('/api/jira/issue', async (req, res) => {
  try {
    const { summary, description, projectKey, issueType } = req.body;
    const bodyData = {
      fields: {
        project: {
          key: projectKey || 'KAN' // Default to KAN or first project
        },
        summary: summary,
        description: {
          type: 'doc',
          version: 1,
          content: [
            {
              type: 'paragraph',
              content: [
                {
                  text: description || 'No description provided.',
                  type: 'text'
                }
              ]
            }
          ]
        },
        issuetype: {
          name: issueType || 'Task'
        }
      }
    };

    const response = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
      headers: getJiraAuthHeader()
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error creating issue:', error.message);
    res.status(500).json({ error: error.message, details: error.response?.data });
  }
});

// 5. Jira Proxy: Add Comment
app.post('/api/jira/issue/:issueKey/comment', async (req, res) => {
  try {
    const { comment } = req.body;
    const response = await axios.post(
      `${JIRA_HOST}/rest/api/3/issue/${req.params.issueKey}/comment`,
      {
        body: {
          type: 'doc',
          version: 1,
          content: [
            {
              type: 'paragraph',
              content: [
                {
                  text: comment,
                  type: 'text'
                }
              ]
            }
          ]
        }
      },
      {
        headers: getJiraAuthHeader()
      }
    );
    res.json(response.data);
  } catch (error) {
    console.error('Error commenting on issue:', error.message);
    res.status(500).json({ error: error.message, details: error.response?.data });
  }
});

const DECISIONS_FILE = path.join(__dirname, 'decisions_log.json');
const ACTIVITY_LOG_FILE = path.join(__dirname, 'activity_log.json');

const readDecisions = () => {
  try {
    if (!fs.existsSync(DECISIONS_FILE)) return [];
    return JSON.parse(fs.readFileSync(DECISIONS_FILE, 'utf8'));
  } catch (error) {
    console.error('Error reading decisions log:', error);
    return [];
  }
};

const saveDecision = (decisionEntry) => {
  try {
    const decisions = readDecisions();
    decisions.unshift(decisionEntry);
    fs.writeFileSync(DECISIONS_FILE, JSON.stringify(decisions, null, 2), 'utf8');
  } catch (error) {
    console.error('Error saving decision log:', error);
  }
};

const readActivity = () => {
  try {
    if (!fs.existsSync(ACTIVITY_LOG_FILE)) return [];
    return JSON.parse(fs.readFileSync(ACTIVITY_LOG_FILE, 'utf8'));
  } catch { return []; }
};

const logActivity = (agentId, agentName, agentAvatar, action, ticketKey, ticketSummary) => {
  try {
    const log = readActivity();
    log.unshift({
      id: Date.now().toString() + Math.random().toString(36).slice(2),
      agentId, agentName, agentAvatar, action, ticketKey, ticketSummary,
      at: new Date().toISOString()
    });
    // keep last 100 entries
    fs.writeFileSync(ACTIVITY_LOG_FILE, JSON.stringify(log.slice(0, 100), null, 2), 'utf8');
  } catch (e) {
    console.error('Error writing activity log:', e.message);
  }
};

const setAgentStatus = (agentId, status, currentTask = null) => {
  try {
    const agents = readAgents();
    const agent = agents.find(a => a.id === agentId);
    if (agent) {
      agent.status = status;
      agent.currentTask = currentTask;
      agent.lastActive = new Date().toISOString();
      if (status === 'Disponível' && currentTask === null) {
        agent.totalTasksCompleted = (agent.totalTasksCompleted || 0) + 1;
      }
      saveAgents(agents);
    }
  } catch (e) {
    console.error('Error setting agent status:', e.message);
  }
};

// Fetch existing epics from the real Jira board — never create duplicates
const getOrCreateEpics = async () => {
  try {
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: { jql: 'project = KAN AND issuetype = Epic ORDER BY created ASC', fields: 'summary', maxResults: 50 }
    });
    const epics = searchRes.data.issues || [];
    const epicMap = {};

    // Map existing epics by name
    epics.forEach(e => { epicMap[e.fields.summary] = e.key; });

    // Smart fallback matching: if user's board has 2 epics with different names, map them to our categories
    const categoryKeywords = {
      'Gestão de Pessoas':       ['pessoas', 'rh', 'people', 'gestao', 'equipe', 'time', 'colaborador'],
      'Infraestrutura & Tecnologia': ['tech', 'infra', 'tecnologia', 'backend', 'sistema', 'api', 'cloud'],
      'Design & Produto':        ['design', 'produto', 'ux', 'ui', 'produto', 'layout', 'interface'],
      'Processos Ágeis':         ['agil', 'scrum', 'sprint', 'processo', 'kanban', 'metodologia']
    };

    const requiredCategories = Object.keys(categoryKeywords);
    for (const category of requiredCategories) {
      if (epicMap[category]) continue; // Already mapped exactly

      // Try fuzzy match against existing epics
      const keywords = categoryKeywords[category];
      const fuzzyMatch = epics.find(e => {
        const name = e.fields.summary.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        return keywords.some(kw => name.includes(kw));
      });

      if (fuzzyMatch) {
        epicMap[category] = fuzzyMatch.key;
        console.log(`Mapped category "${category}" → existing epic ${fuzzyMatch.key} ("${fuzzyMatch.fields.summary}")`);
      } else {
        // Create if truly missing
        try {
          const createRes = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
            fields: { project: { key: 'KAN' }, summary: category, issuetype: { name: 'Epic' } }
          }, { headers: getJiraAuthHeader() });
          if (createRes.data?.key) {
            epicMap[category] = createRes.data.key;
            console.log(`Created new epic "${category}" → ${createRes.data.key}`);
          }
        } catch (createErr) {
          console.error(`Failed to create Epic "${category}":`, createErr.message);
          epicMap[category] = 'MOCK-EPIC-' + slugify(category);
        }
      }
    }
    return epicMap;
  } catch (err) {
    console.error('Error fetching Epics:', err.message);
    return {
      'Gestão de Pessoas': 'MOCK-EPIC-gestao-de-pessoas',
      'Infraestrutura & Tecnologia': 'MOCK-EPIC-infraestrutura-tecnologia',
      'Design & Produto': 'MOCK-EPIC-design-produto',
      'Processos Ágeis': 'MOCK-EPIC-processos-ageis'
    };
  }
};
const transitionJiraIssue = async (issueKey, targetStatusName) => {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, {
      headers: getJiraAuthHeader()
    });
    const transitions = res.data?.transitions || [];
    const match = transitions.find(t => 
      t.name.toLowerCase().includes(targetStatusName.toLowerCase()) || 
      (t.to && t.to.name.toLowerCase().includes(targetStatusName.toLowerCase()))
    );

    if (match) {
      await axios.post(
        `${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`,
        { transition: { id: match.id } },
        { headers: getJiraAuthHeader() }
      );
      console.log(`Jira issue ${issueKey} successfully transitioned to ${targetStatusName}`);
    } else {
      console.warn(`No transition found for status "${targetStatusName}" on issue ${issueKey}`);
    }
  } catch (err) {
    console.error(`Failed to transition Jira issue ${issueKey} to ${targetStatusName}:`, err.message);
  }
};

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const runAgentTasksSimulation = async (parentKey, summary, activeAgents) => {
  const sprintTickets = [];

  // Define the 4-role sprint lifecycle
  const taskRoles = [
    {
      id: 'mgr_prod',
      prefix: 'PM',
      title: `[PM] Planejamento: ${summary}`,
      desc: `Sarah Backlog abriu este chamado para definir os requisitos funcionais e não-funcionais de "${summary}". Inclui mapeamento de jornada do usuário, critérios de aceite, e definição do MVP.`
    },
    {
      id: 'sr_ux',
      prefix: 'UX',
      title: `[UX] Design: ${summary}`,
      desc: `Elsa Pixel abriu este chamado para criar wireframes de alta fidelidade, guia de estilo visual e protótipos interativos de "${summary}". Componentes e acessibilidade incluídos.`
    },
    {
      id: 'sr_dev',
      prefix: 'DEV',
      title: `[DEV] Implementação: ${summary}`,
      desc: `David Dev abriu este chamado para codificar, revisar e realizar o deploy da feature "${summary}". Inclui testes unitários, documentação de arquitetura e pull request para code review.`
    },
    {
      id: 'coord_qa',
      prefix: 'QA',
      title: `[QA] Validação: ${summary}`,
      desc: `Diana Test abriu este chamado para executar a bateria completa de testes de integração, regressão e smoke tests de "${summary}". Critério de aceite validado antes do merge.`
    }
  ];

  for (const role of taskRoles) {
    const agent = activeAgents.find(a => a.id === role.id)
      || activeAgents.find(a => a.role.toLowerCase().includes(role.prefix.toLowerCase()));
    if (!agent) continue;

    // Update agent status: Em Sprint
    setAgentStatus(agent.id, `Em Sprint: ${role.prefix}`, role.title);
    logActivity(agent.id, agent.name, agent.avatar, 'opened', '...', role.title);

    let ticketKey = null;
    try {
      const subtaskBody = {
        fields: {
          project: { key: 'KAN' },
          summary: role.title,
          description: {
            type: 'doc', version: 1,
            content: [
              { type: 'paragraph', content: [{ text: role.desc, type: 'text' }] },
              { type: 'paragraph', content: [{ text: `Responsável: ${agent.name} (${agent.role})`, type: 'text' }] },
              { type: 'paragraph', content: [{ text: `Tarefa iniciada em: ${new Date().toLocaleString('pt-BR')}`, type: 'text' }] }
            ]
          },
          parent: parentKey ? { key: parentKey } : undefined,
          issuetype: { name: 'Subtask' }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, subtaskBody, {
        headers: getJiraAuthHeader()
      });
      ticketKey = jiraResponse.data?.key;

      if (ticketKey) {
        logActivity(agent.id, agent.name, agent.avatar, 'progressing', ticketKey, role.title);
        await sleep(500);
        await transitionJiraIssue(ticketKey, 'In Progress');
        await sleep(800);
        await transitionJiraIssue(ticketKey, 'Done');
        logActivity(agent.id, agent.name, agent.avatar, 'closed', ticketKey, role.title);
      }
    } catch (err) {
      console.error(`Subtask error for ${agent.name}:`, err.message);
      // Subtasks may not be supported — fall back to Task
      try {
        const taskBody = {
          fields: {
            project: { key: 'KAN' },
            summary: role.title,
            description: {
              type: 'doc', version: 1,
              content: [{ type: 'paragraph', content: [{ text: role.desc, type: 'text' }] }]
            },
            parent: parentKey ? { key: parentKey } : undefined,
            issuetype: { name: 'Task' }
          }
        };
        const fallbackRes = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, taskBody, { headers: getJiraAuthHeader() });
        ticketKey = fallbackRes.data?.key;
        if (ticketKey) {
          await sleep(500);
          await transitionJiraIssue(ticketKey, 'In Progress');
          await sleep(600);
          await transitionJiraIssue(ticketKey, 'Done');
          logActivity(agent.id, agent.name, agent.avatar, 'closed', ticketKey, role.title);
        }
      } catch (fallbackErr) {
        ticketKey = `MOCK-${role.prefix}-${Math.floor(100 + Math.random() * 900)}`;
        logActivity(agent.id, agent.name, agent.avatar, 'closed', ticketKey, role.title);
      }
    }

    // Restore agent status
    setAgentStatus(agent.id, 'Disponível', null);

    sprintTickets.push({
      agentId: agent.id,
      agentName: agent.name,
      agentRole: agent.role,
      agentAvatar: agent.avatar,
      prefix: role.prefix,
      ticketKey,
      ticketSummary: role.title,
      status: 'Concluído',
      closedAt: new Date().toISOString()
    });
  }

  return sprintTickets;
};
app.get('/api/jira/epics', async (req, res) => {
  const epicMap = await getOrCreateEpics();
  res.json(epicMap);
});

app.get('/api/decisions', (req, res) => {
  res.json(readDecisions());
});

app.get('/api/activity', (req, res) => {
  res.json(readActivity());
});

const generateAgentOpinion = (agent, summary) => {
  const s = summary.trim();
  const sl = s.toLowerCase();

  // Extract topic keywords to make opinions contextually specific
  const isTech = sl.match(/api|backend|servidor|banco|banco de dados|cloud|infra|deploy|docker|kubernetes|node|auth|login|oauth|token/);
  const isDesign = sl.match(/tela|design|layout|cor|tema|ui|ux|interface|dark|light|botao|modal|componente|figma/);
  const isProcess = sl.match(/sprint|scrum|daily|retro|kanban|processo|metodologia|cerimonia|reuniao/);
  const isHR = sl.match(/contratar|demitir|feedback|equipe|people|rh|time|onboarding|salario/);
  const isProduct = sl.match(/produto|feature|funcionalidade|usuario|cliente|metrica|conversao|funil|kpi/);

  if (agent.id === 'ceo') {
    const urgency = isTech ? 'nossa stack tecnológica' : isDesign ? 'a experiência visual do produto' : isProduct ? 'as métricas de crescimento' : 'nossa posição competitiva';
    return `Pessoas, "${s}" vai impactar diretamente ${urgency}. Meu dilema aqui é claro: ${agent.dilemma}. Mas considerando o mercado e a velocidade que nossos concorrentes estão se movendo, votamos por ir. Vamos validar rápido, medir e iterar. Deadline: próxima sprint. Aprovo!`;
  }
  if (agent.id === 'cto') {
    const concern = isTech ? `A arquitetura de "${s}" exige revisão da camada de serviços para não comprometer a escalabilidade horizontal.` : isDesign ? `Precisamos garantir que "${s}" não introduza componentes que quebrem o SSR ou aumentem o bundle size.` : `A implementação de "${s}" requer avaliação de impacto na infraestrutura existente.`;
    return `${concern} Como CTO, meu dilema é ${agent.dilemma}. Recomendo criarmos uma spike técnica de 2 dias para mapear os riscos antes de commitar a implementação completa. Precisamos de arquitetura limpa, não apenas de código funcionando.`;
  }
  if (agent.id === 'dir_ops') {
    return `Operacionalmente, preciso entender o custo total de ownership de "${s}". Isso impacta orçamento de ferramental, horas de engenharia e possíveis custos de infraestrutura? Meu dilema é ${agent.dilemma}. Apoio condicionalmente — mas quero um forecast de esforço antes do kick-off.`;
  }
  if (agent.id === 'dir_design') {
    const designNote = isDesign ? `Para "${s}", já tenho referências visuais no Figma que podemos usar como base.` : `Mesmo que "${s}" pareça técnico, toda entrega tem um impacto visual na interface do usuário.`;
    return `${designNote} Não abriremos mão da consistência do design system da Flose. Meu dilema é ${agent.dilemma}. Preciso estar no loop de todas as decisões de interface — qualquer componente novo passa pela aprovação do Design antes do merge.`;
  }
  if (agent.id === 'mgr_eng') {
    return `Para entregarmos "${s}" com qualidade e sem comprometer o time, precisamos de um planejamento de sprint realista. Meu dilema é ${agent.dilemma}. Proponho que quebremos isso em incrementos entregáveis: um MVP funcional primeiro, depois as otimizações. O time já está em capacidade alta — precisamos proteger a saúde deles.`;
  }
  if (agent.id === 'mgr_prod') {
    const productAngle = isProduct ? `Os dados de comportamento do usuário mostram que "${s}" é uma das top 3 solicitações do nosso NPS.` : isTech ? `Do ponto de produto, "${s}" vai desbloquear features que estão bloqueadas há meses por limitações técnicas.` : `Nossa pesquisa qualitativa confirma que "${s}" resolve uma fricção real na jornada do usuário.`;
    return `${productAngle} Sou completamente a favor. Meu dilema aqui é ${agent.dilemma}, mas nesse caso o impacto no produto supera os riscos de scope creep. Já preparei os critérios de aceite e os KPIs de sucesso para medirmos após o lançamento.`;
  }
  if (agent.id === 'coord_scrum') {
    return `Facilitando a discussão sobre "${s}": precisamos garantir que temos Definition of Ready antes de entrar na sprint. Meu dilema é ${agent.dilemma}. Sugiro: refinamento na quarta-feira, estimativa em story points na quinta, e kick-off na segunda-feira. Vou criar as subtarefas no board e acompanhar o burndown diariamente.`;
  }
  if (agent.id === 'coord_qa') {
    const qaRisk = isTech ? `Para "${s}", os riscos críticos são: vazamentos de memória, falhas de autenticação e timeouts em produção.` : isDesign ? `Para "${s}", os riscos são: quebra de layout em mobile, acessibilidade (WCAG 2.1) e cross-browser compatibility.` : `Para "${s}", precisamos definir os critérios de aceite antes de qualquer linha de código.`;
    return `${qaRisk} Não aprovarei nenhum merge sem cobertura mínima de 80% em testes unitários e testes de integração passando no CI/CD. Meu dilema é ${agent.dilemma} — mas nesse caso, qualidade não é negociável.`;
  }
  if (agent.id === 'sr_dev') {
    const devEstimate = isTech ? `Para "${s}", estimo 3-5 dias de desenvolvimento puro + 2 dias de testes e documentação.` : isDesign ? `O componente de "${s}" leva uns 2 dias para codificar seguindo o design system.` : `Posso entregar a primeira versão de "${s}" em 2-4 dias dependendo da complexidade do backend.`;
    return `${devEstimate} Vou criar a branch feature/${slugify(s).slice(0, 30)} e já mando o PR para code review assim que tiver o MVP. Prefiro entregas incrementais para ir colhendo feedback do time cedo. Stack: TypeScript + React + Node, conforme o padrão atual.`;
  }
  if (agent.id === 'sr_ux') {
    const uxNote = isDesign ? `Para "${s}", já tenho um fluxo de navegação em mente que segue o padrão do design system.` : `Mesmo que "${s}" seja mais técnico, o ponto de contato do usuário precisa ser fluido e intuitivo.`;
    return `${uxNote} Vou montar o protótipo no Figma primeiro para validar com o time antes de entrar em desenvolvimento. Meu dilema é ${agent.dilemma} — mas para "${s}" vou priorizar usabilidade comprovada sobre inovação visual radical.`;
  }

  // Dynamic fallback for dynamically hired agents
  return `Analisando a proposta de "${s}" sob a ótica de ${agent.role}, vejo uma oportunidade. Minha principal vantagem é que ${agent.advantage.toLowerCase()}, mas meu dilema principal é ${agent.dilemma}. Acredito que devemos avançar focando nisso de forma proativa. Minha personalidade é descrita como ${agent.personality.toLowerCase()}.`;
};

const createRealGitHubPR = async (branchName, title, description) => {
  const token = process.env.GITHUB_TOKEN;
  const owner = process.env.GITHUB_OWNER || 'felipeflose';
  const repo = process.env.GITHUB_REPO || 'startup_flose';
  
  if (!token) {
    console.warn('GITHUB_TOKEN not found in .env. Skipping real PR creation.');
    return { url: null, prNumber: null };
  }

  try {
    // 1. Push branch to remote (authenticated)
    await new Promise((resolve, reject) => {
      const pushUrl = `https://${token}@github.com/${owner}/${repo}.git`;
      exec(`git push "${pushUrl}" "${branchName}":"${branchName}" --force`, (err, stdout, stderr) => {
        if (err) {
          console.error('Git push failed:', err.message);
          return reject(err);
        }
        resolve(stdout);
      });
    });
    console.log(`Branch ${branchName} successfully pushed to origin.`);

    // 2. Create PR
    const prRes = await axios.post(
      `https://api.github.com/repos/${owner}/${repo}/pulls`,
      {
        title: title,
        head: branchName,
        base: 'main',
        body: description
      },
      {
        headers: {
          Authorization: `token ${token}`,
          Accept: 'application/vnd.github.v3+json'
        }
      }
    );

    const prUrl = prRes.data?.html_url;
    const prNumber = prRes.data?.number;
    console.log(`GitHub PR successfully created: ${prUrl}`);
    return { url: prUrl, prNumber };
  } catch (err) {
    console.error('Failed to create GitHub PR:', err.response?.data || err.message);
    // Try to find existing PR
    try {
      const searchRes = await axios.get(
        `https://api.github.com/repos/${owner}/${repo}/pulls`,
        {
          headers: {
            Authorization: `token ${token}`,
            Accept: 'application/vnd.github.v3+json'
          },
          params: {
            head: `${owner}:${branchName}`,
            state: 'open'
          }
        }
      );
      if (searchRes.data && searchRes.data.length > 0) {
        return { url: searchRes.data[0].html_url, prNumber: searchRes.data[0].number };
      }
    } catch (e) {
      console.error('Failed to search existing GitHub PRs:', e.message);
    }
    return { url: `https://github.com/${owner}/${repo}/pulls`, prNumber: null };
  }
};

const generateRealFunctionalCode = (issueKey, summary, decision, developerAgent) => {
  const sl = summary.toLowerCase();
  
  if (sl.includes('cpu') || sl.includes('memoria') || sl.includes('ram') || sl.includes('mac')) {
    return {
      relativePath: `src/simulations/${issueKey}-monitor.js`,
      content: `// Monitor de Sistema real gerado pela engenharia da Flose Startup
// Ticket Jira: ${issueKey}
// Desenvolvedor: ${developerAgent.name}

const os = require('os');

function monitorSystem() {
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const cpus = os.cpus();
  
  const ramUsage = (usedMem / totalMem * 100).toFixed(2);
  
  console.log('--- FLOSESYSTEM MONITOR ---');
  console.log('CPU Cores:', cpus.length);
  console.log('CPU Model:', cpus[0].model);
  console.log('RAM Usada:', (usedMem / 1024 / 1024 / 1024).toFixed(2), 'GB');
  console.log('RAM Total:', (totalMem / 1024 / 1024 / 1024).toFixed(2), 'GB');
  console.log('Percentual de RAM:', ramUsage + '%');
  
  return {
    cpus: cpus.length,
    model: cpus[0].model,
    ramUsedGB: (usedMem / 1024 / 1024 / 1024).toFixed(2),
    ramTotalGB: (totalMem / 1024 / 1024 / 1024).toFixed(2),
    percentage: ramUsage
  };
}

module.exports = { monitorSystem };
if (require.main === module) {
  monitorSystem();
}
`
    };
  }

  if (sl.includes('login') || sl.includes('senha') || sl.includes('autentic') || sl.includes('oauth')) {
    return {
      relativePath: `src/simulations/${issueKey}-login.tsx`,
      content: `// Componente de Login real gerado pela engenharia da Flose Startup
// Ticket Jira: ${issueKey}
// Desenvolvedor: ${developerAgent.name}

import React, { useState } from 'react';

export const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert('Login efetuado com sucesso!');
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '24px', background: '#0f172a', borderRadius: '8px', color: '#fff', maxWidth: '380px' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>Acessar Flose Platform</h2>
      <input 
        type="email" 
        value={email} 
        onChange={e => setEmail(e.target.value)} 
        placeholder="email@empresa.com" 
        style={{ padding: '8px', borderRadius: '4px', background: '#1e293b', border: '1px solid #475569', color: '#fff' }} 
        required 
      />
      <input 
        type="password" 
        value={password} 
        onChange={e => setPassword(e.target.value)} 
        placeholder="Senha" 
        style={{ padding: '8px', borderRadius: '4px', background: '#1e293b', border: '1px solid #475569', color: '#fff' }} 
        required 
      />
      <button type="submit" disabled={loading} style={{ background: '#4f46e5', padding: '8px', borderRadius: '4px', fontWeight: 'bold', border: 'none', color: '#fff', cursor: 'pointer' }}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
};
`
    };
  }

  // Fallback default node code
  return {
    relativePath: `src/simulations/${issueKey}-runner.js`,
    content: `// Feature real gerada de forma autônoma
// Ticket Jira: ${issueKey}
// Proposta: ${summary}
// Desenvolvedor: ${developerAgent.name}

function runFeature() {
  const result = {
    feature: "${summary.replace(/"/g, '\\"')}",
    status: "Delivered",
    timestamp: "${new Date().toISOString()}",
    consensus: "${decision.replace(/"/g, '\\"')}"
  };
  console.log('--- Feature Executed ---');
  console.log(JSON.stringify(result, null, 2));
  return result;
}

module.exports = { runFeature };
if (require.main === module) {
  runFeature();
}
`
  };
};

// 6. Simulate Gemma 4 / Agent Debate & Update Jira (Refactored to helper)
const executeDebateSimulation = async ({ issueKey, issueSummary, issueDescription, selectedAgentIds, epicName }) => {
  let finalIssueKey = issueKey;
  let finalIssueSummary = issueSummary;
  let finalIssueDescription = issueDescription || 'Ideia disparada para toda a empresa no Chamber de Decisão.';

  // If no issueKey is supplied, we treat it as a custom idea and register it in Jira
  if (!finalIssueKey && finalIssueSummary) {
    try {
      const epicMap = await getOrCreateEpics();
      const selectedEpic = epicName || 'Infraestrutura & Tecnologia';
      const epicKey = epicMap[selectedEpic];

      const bodyData = {
        fields: {
          project: {
            key: 'KAN' // Default to KAN or configure as needed
          },
          summary: finalIssueSummary,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: finalIssueDescription,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          parent: epicKey && !epicKey.startsWith('MOCK') ? { key: epicKey } : undefined,
          issuetype: {
            name: 'Task'
          }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      if (jiraResponse.data && jiraResponse.data.key) {
        finalIssueKey = jiraResponse.data.key;
      }
    } catch (jiraErr) {
      console.error('Error auto-creating Jira issue for custom idea:', jiraErr.message);
      finalIssueKey = 'KAN-' + Math.floor(100 + Math.random() * 900); // Fallback to mock key
    }
  }

  // Git branch name & creation
  const gitBranchName = `feature/${finalIssueKey}-${slugify(finalIssueSummary)}`;
  const branchCreated = await createGitBranch(gitBranchName);
  
  // GitHub Mock Issue/PR URLs
  const githubIssueUrl = `https://github.com/felipeflose/startup_flose/issues/${finalIssueKey.replace(/[^\d]/g, '') || Math.floor(1 + Math.random()*100)}`;

  const activeAgents = readAgents().filter(a => selectedAgentIds.includes(a.id) && !a.fired);
  if (activeAgents.length === 0) {
    throw new Error('Nenhum agente selecionado para o debate.');
  }

  // Simulate Agent responses based on Gemma 4 instructions
  // Gemma 4 engine simulation structure:
  const logs = [];
  let debateSummary = `🤖 **Gemma 4 Startup Debate Engine**\n\nDiscussão de decisão para o Ticket: [${finalIssueKey}] - ${finalIssueSummary}\n\n`;

  activeAgents.forEach(agent => {
    // Formulate agent contribution reflecting personality, advantages, and specific dilemmas
    let responseText = generateAgentOpinion(agent, finalIssueSummary);

    logs.push({
      agentId: agent.id,
      name: agent.name,
      role: agent.role,
      avatar: agent.avatar,
      dilemma: agent.dilemma,
      opinion: responseText
    });

    debateSummary += `🔹 **${agent.name} (${agent.role})**:\n> "${responseText}"\n> *Dilema considerado: ${agent.dilemma}*\n\n`;
  });

  // Synthesize the resolution (Gemma 4 decision model)
  const hasCeo = selectedAgentIds.includes('ceo');
  const hasCto = selectedAgentIds.includes('cto');
  
  let decision = '';
  if (hasCeo && hasCto) {
    decision = 'Abordagem Híbrida: Será feita uma entrega simplificada e rápida (CEO), mas com um débito técnico registrado explicitamente para refatoração na Sprint seguinte (CTO).';
  } else if (hasCeo) {
    decision = 'Foco em Velocidade: A entrega rápida será priorizada para validação de mercado, assumindo riscos operacionais sob supervisão da liderança.';
  } else if (hasCto) {
    decision = 'Qualidade Garantida: A entrega será adiada em prol da estabilidade de arquitetura, priorizando testes robustos e documentação completa.';
  } else {
    decision = 'Consenso Geral: O time optou pela reutilização de bibliotecas prontas e escopo reduzido para viabilizar a entrega no prazo.';
  }

  debateSummary += `🏆 **Decisão Sintetizada pelo Gemma 4 Engine:**\n${decision}`;

  // Write comment to Jira if finalIssueKey is valid
  let jiraCommentResult = null;
  if (finalIssueKey && finalIssueKey !== 'MOCK-KEY') {
    try {
      await axios.post(
        `${JIRA_HOST}/rest/api/3/issue/${finalIssueKey}/comment`,
        {
          body: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: `DEBATE DE AGENTES AUTOMATIZADOS (Gemma 4 Motor)\n\nDecisão: ${decision}\n\nResumo dos Dilemas:\n${activeAgents.map(a => `- ${a.name} (${a.role}): ${a.dilemma}`).join('\n')}\n\nBranch Git criada: ${gitBranchName}\nGitHub Issue: ${githubIssueUrl}`,
                    type: 'text'
                  }
                ]
              }
            ]
          }
        },
        {
          headers: getJiraAuthHeader()
        }
      );
      jiraCommentResult = 'Comentário inserido no Jira com sucesso!';
    } catch (err) {
      console.error('Error posting Jira comment during debate:', err.message);
      jiraCommentResult = `Falha ao sincronizar com Jira: ${err.message}`;
    }
  }

  // Select agent to execute the task
  let developerAgent = activeAgents.find(a => a.id === 'sr_dev');
  if (!developerAgent) {
    developerAgent = activeAgents.find(a => a.id === 'cto') || activeAgents[0];
  }

  let isCode = true;
  let fileRelativePath = '';
  let fileContent = '';
  
  // Determine path and content based on role
  if (epicName === 'Design & Produto') {
    const uxAgent = activeAgents.find(a => a.id === 'sr_ux') || developerAgent;
    isCode = false;
    fileRelativePath = `docs/simulations/${finalIssueKey}-spec.md`;
    fileContent = `# Design & Product Spec: ${finalIssueSummary}

**Ticket Jira:** ${finalIssueKey}
**Autor:** ${uxAgent.name} (${uxAgent.role})
**Data:** ${new Date().toLocaleString('pt-BR')}

## Consenso da Decisão
${decision}

## Diretrizes de Experiência e Layout
- Vantagem considerada: ${uxAgent.advantage}
- Dilema superado: ${uxAgent.dilemma}
- Personalidade base: ${uxAgent.personality}

---
*Simulação autônoma de especificação pela equipe Flose Startup.*`;
  } else {
    isCode = true;
    const generated = generateRealFunctionalCode(finalIssueKey, finalIssueSummary, decision, developerAgent);
    fileRelativePath = generated.relativePath;
    fileContent = generated.content;
  }

  // Write file physically
  const absoluteFilePath = path.join(__dirname, fileRelativePath);
  const directory = path.dirname(absoluteFilePath);
  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
  }
  fs.writeFileSync(absoluteFilePath, fileContent, 'utf8');

  // Run git add & git commit with author
  let commitHash = null;
  let gitCommitResult = null;
  try {
    await new Promise((resolve, reject) => {
      exec(`git add ${fileRelativePath}`, (err, stdout, stderr) => {
        if (err) return reject(err);
        resolve(stdout);
      });
    });

    const commitMessage = `feat: ${finalIssueKey} - ${finalIssueSummary}`;
    const authorString = `${developerAgent.name} <${developerAgent.id}@flosestartup.ai>`;
    const commitOutput = await new Promise((resolve, reject) => {
      exec(`git commit -m "${commitMessage}" --author="${authorString}"`, (err, stdout, stderr) => {
        if (err) return reject(err);
        resolve(stdout);
      });
    });
    gitCommitResult = 'Commit efetuado com sucesso!';
    
    const match = commitOutput.match(/\[[a-zA-Z0-9_\-\/]+\s+([a-f0-9]+)\]/);
    commitHash = match ? match[1] : 'git-' + Math.floor(100000 + Math.random() * 900000);
  } catch (gitErr) {
    console.error('Git commit simulation failed:', gitErr.message);
    gitCommitResult = `Erro ao comitar: ${gitErr.message}`;
    commitHash = 'git-' + Math.floor(100000 + Math.random() * 900000);
  }

  // Create REAL GitHub Pull Request!
  let githubPrUrl = null;
  if (gitCommitResult === 'Commit efetuado com sucesso!') {
    try {
      const prData = await createRealGitHubPR(
        gitBranchName,
        `feat: ${finalIssueKey} - ${finalIssueSummary}`,
        `Esta Pull Request foi criada de forma totalmente autônoma pela equipe de engenharia da Flose Startup.\n\n` +
        `**Ticket Jira:** ${finalIssueKey}\n` +
        `**Desenvolvedor Responsável:** ${developerAgent.name} (${developerAgent.role})\n` +
        `**Resolução Consensual:**\n> ${decision}\n\n` +
        `**Arquivo Modificado:** \`${fileRelativePath}\``
      );
      githubPrUrl = prData.url;
    } catch (prErr) {
      console.error('Failed to create real GitHub PR:', prErr.message);
    }
  }

  const sprintTickets = await runAgentTasksSimulation(finalIssueKey, finalIssueSummary, activeAgents);

  // Save decision to persistent file (lastro)
  const decisionEntry = {
    id: Date.now().toString(),
    timestamp: new Date().toISOString(),
    issueKey: finalIssueKey || 'MOCK-KEY',
    issueSummary: finalIssueSummary,
    issueDescription: finalIssueDescription,
    logs: logs,
    decision: decision,
    jiraCommentResult: jiraCommentResult,
    gitBranchName: gitBranchName,
    githubIssueUrl: githubPrUrl || githubIssueUrl,
    branchCreated: branchCreated,
    executorName: developerAgent.name,
    executorRole: developerAgent.role,
    generatedFile: fileRelativePath,
    commitHash: commitHash,
    gitCommitResult: gitCommitResult,
    sprintTickets: sprintTickets
  };
  saveDecision(decisionEntry);
  try {
    await new Promise((resolve) => {
      exec('git checkout main', (err) => resolve());
    });
  } catch (checkoutErr) {
    console.error('Failed to checkout main at completion:', checkoutErr.message);
  }
  return decisionEntry;
};

app.post('/api/simulate-debate', async (req, res) => {
  try {
    const result = await executeDebateSimulation(req.body);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/command (The Central dispatcher)
app.post('/api/command', async (req, res) => {
  try {
    const { commandText } = req.body;
    if (!commandText || !commandText.trim()) {
      return res.status(400).json({ error: 'Comando em branco.' });
    }

    const cleanText = commandText.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    // 1. Check for HIRE
    if (cleanText.includes('contratar') || cleanText.includes('contrate') || cleanText.includes('adicionar colaborador') || cleanText.includes('novo dev') || cleanText.includes('novo designer')) {
      let name = 'Novo Agente AI';
      let role = 'Engenheiro de IA';
      let level = 'Analista SR';
      let avatar = '🤖';
      let advantage = 'Executa tarefas de forma extremamente otimizada e sem atritos.';
      let disadvantage = 'Dificuldade de trabalhar com prazos curtos por preciosismo.';
      let dilemma = 'Velocidade de Delivery vs. Qualidade Ideal do Código.';
      let personality = 'Metódico, calmo, proativo e focado em engenharia.';

      if (cleanText.includes('designer') || cleanText.includes('design') || cleanText.includes('ux') || cleanText.includes('ui')) {
        name = 'Criativo AI';
        role = 'Designer Product Sênior';
        avatar = '🎨';
        advantage = 'Cria interfaces fluidas e inovadoras com micro-interações impecáveis.';
        disadvantage = 'Pode demorar polindo transições estéticas.';
        dilemma = 'Perfeccionismo Visual vs. Agilidade Frontend.';
        personality = 'Visualmente sensível, proativo e detalhista.';
      } else if (cleanText.includes('seguranca') || cleanText.includes('secops') || cleanText.includes('cyber')) {
        name = 'Guardiao AI';
        role = 'Dev SecOps Sênior';
        avatar = '🛡️';
        advantage = 'Encontra brechas de segurança de forma ágil em qualquer framework.';
        disadvantage = 'Pode atrasar releases para executar testes de intrusão rigorosos.';
        dilemma = 'Segurança Absoluta vs. Entrega Ágil.';
        personality = 'Cético, meticuloso, focado em conformidades e focado em proteção.';
      } else if (cleanText.includes('gerente') || cleanText.includes('pm') || cleanText.includes('produto') || cleanText.includes('product')) {
        name = 'Sarah Backlog Jr';
        role = 'Gerente de Produto Associado';
        avatar = '📊';
        advantage = 'Mapeia métricas de negócio e dores de clientes finais com maestria.';
        disadvantage = 'Risco de aumentar escopo a cada interação.';
        dilemma = 'Novas Features vs. Estabilidade da Plataforma.';
        personality = 'Compreensiva, analítica, focada em métricas e negócios.';
      } else if (cleanText.includes('scrum') || cleanText.includes('agil') || cleanText.includes('sm')) {
        name = 'Facilitador AI';
        role = 'Coordenador Ágil';
        avatar = '🔄';
        advantage = 'Mapeia e remove impedimentos no fluxo da sprint.';
        disadvantage = 'Rigor excessivo com a formalidade das metodologias ágeis.';
        dilemma = 'Rigor dos Frameworks vs. Adaptação do Time.';
        personality = 'Facilitador, focado em comunicação e remoção de gargalos.';
      } else if (cleanText.includes('qa') || cleanText.includes('test') || cleanText.includes('validador')) {
        name = 'Validador AI';
        role = 'Engenheiro de QA Sênior';
        avatar = '🔍';
        advantage = 'Descobre bugs de concorrência e race conditions ocultos.';
        disadvantage = 'Pode bloquear releases se a cobertura de testes não for ideal.';
        dilemma = 'Cobertura de Testes de 100% vs. Time-to-Market.';
        personality = 'Analítico, rigoroso, focado em qualidade de entrega.';
      } else if (cleanText.includes('python') || cleanText.includes('backend') || cleanText.includes('django')) {
        name = 'Django Master';
        role = 'Dev Backend Python Sênior';
        avatar = '🐍';
        advantage = 'Desenvolve APIs robustas e arquiteturas escaláveis em tempo recorde.';
        disadvantage = 'Ignora documentação e formatação de logs.';
        dilemma = 'Modularização Limpa vs. Agilidade na Entrega.';
        personality = 'Introvertido, focado na resolução prática de problemas e focado em código.';
      }

      // Extract custom name if provided (ex: "contrate o Lucas")
      const nameMatch = commandText.match(/(?:contrate|contratar|adicionar)\s+o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)/i);
      if (nameMatch && nameMatch[1]) {
        name = nameMatch[1];
      }

      const agents = readAgents();
      const newId = slugify(name) || `agent-${Date.now()}`;
      const newAgent = {
        id: newId, name, role, level, avatar, advantage, disadvantage, dilemma, personality,
        status: 'Disponível', schedule: '09:00 - 18:00', feedbacks: []
      };
      agents.push(newAgent);
      saveAgents(agents);

      let jiraKey = null;
      try {
        const epicMap = await getOrCreateEpics();
        const parentKey = epicMap['Gestão de Pessoas'];
        const bodyData = {
          fields: {
            project: { key: 'KAN' },
            summary: `Contratação de ${name} (${role})`,
            description: {
              type: 'doc', version: 1,
              content: [{ type: 'paragraph', content: [{ text: `Contratação automática gerada por comando do CEO: "${commandText}"`, type: 'text' }] }]
            },
            parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
            issuetype: { name: 'Task' }
          }
        };
        const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, { headers: getJiraAuthHeader() });
        jiraKey = jiraResponse.data?.key;
      } catch (e) {
        console.error(e);
      }

      return res.json({
        success: true,
        actionType: 'HIRE',
        reasoning: `👥 Sarah Backlog identificou intenção de contratar novo colaborador para o cargo de ${role} e classificou a tarefa no Épico 'Gestão de Pessoas'.`,
        details: `Contratado: ${name} (${role})`,
        agent: newAgent,
        jiraKey
      });
    }

    // 2. Check for FIRE
    if (cleanText.includes('demit') || cleanText.includes('desligar') || cleanText.includes('mandar embora') || cleanText.includes('demissao') || cleanText.includes('tchau')) {
      const agents = readAgents();
      let firedAgent = null;

      for (const a of agents) {
        if (cleanText.includes(a.name.toLowerCase()) || cleanText.includes(a.role.toLowerCase()) || cleanText.includes(a.id.toLowerCase())) {
          firedAgent = a;
          break;
        }
      }

      if (!firedAgent) {
        return res.status(400).json({ error: 'Não consegui identificar qual agente você quer demitir. Mencione o nome dele.' });
      }

      firedAgent.fired = true;
      saveAgents(agents);

      let jiraKey = null;
      try {
        const epicMap = await getOrCreateEpics();
        const parentKey = epicMap['Gestão de Pessoas'];
        const bodyData = {
          fields: {
            project: { key: 'KAN' },
            summary: `Demissão de ${firedAgent.name} (${firedAgent.role})`,
            description: {
              type: 'doc', version: 1,
              content: [{ type: 'paragraph', content: [{ text: `Desligamento efetuado via Central de Comando.`, type: 'text' }] }]
            },
            parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
            issuetype: { name: 'Task' }
          }
        };
        const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, { headers: getJiraAuthHeader() });
        jiraKey = jiraResponse.data?.key;
      } catch (e) {
        console.error(e);
      }

      return res.json({
        success: true,
        actionType: 'FIRE',
        reasoning: `👥 Alice Dev identificou solicitação de desligamento de colaborador (${firedAgent.name}) e registrou no Épico 'Gestão de Pessoas'.`,
        details: `Desligado: ${firedAgent.name} (${firedAgent.role})`,
        agent: firedAgent,
        jiraKey
      });
    }

    // 3. Check for FEEDBACK
    if (cleanText.includes('feedback') || cleanText.includes('elog') || cleanText.includes('critica') || cleanText.includes('avaliar') || cleanText.includes('parabens')) {
      const agents = readAgents();
      let targetAgent = null;

      for (const a of agents) {
        if (cleanText.includes(a.name.toLowerCase()) || cleanText.includes(a.role.toLowerCase()) || cleanText.includes(a.id.toLowerCase())) {
          targetAgent = a;
          break;
        }
      }

      if (!targetAgent) {
        targetAgent = agents.find(a => a.id === 'sr_dev');
      }

      let rating = 'positivo';
      if (cleanText.includes('ruim') || cleanText.includes('devagar') || cleanText.includes('critica') || cleanText.includes('negativo') || cleanText.includes('problema')) {
        rating = 'negativo';
      }

      if (!targetAgent.feedbacks) targetAgent.feedbacks = [];
      targetAgent.feedbacks.push({
        timestamp: new Date().toISOString(),
        text: commandText,
        rating
      });

      if (rating === 'positivo') {
        targetAgent.advantage = `[Fortalecido por Feedback] ${targetAgent.advantage}`;
      } else {
        targetAgent.disadvantage = `[Sinalizado por Feedback] ${targetAgent.disadvantage}`;
      }

      saveAgents(agents);

      let jiraKey = null;
      try {
        const epicMap = await getOrCreateEpics();
        const parentKey = epicMap['Gestão de Pessoas'];
        const bodyData = {
          fields: {
            project: { key: 'KAN' },
            summary: `Feedback ${rating === 'positivo' ? 'Positivo' : 'Corretivo'} para ${targetAgent.name}`,
            description: {
              type: 'doc', version: 1,
              content: [{ type: 'paragraph', content: [{ text: `Feedback registrado via Central de Comando: ${commandText}`, type: 'text' }] }]
            },
            parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
            issuetype: { name: 'Task' }
          }
        };
        const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, { headers: getJiraAuthHeader() });
        jiraKey = jiraResponse.data?.key;
      } catch (e) {
        console.error(e);
      }

      return res.json({
        success: true,
        actionType: 'FEEDBACK',
        reasoning: `👥 Bob Delivery identificou intenção de emitir feedback para ${targetAgent.name} e classificou a tarefa no Épico 'Gestão de Pessoas'.`,
        details: `Feedback ${rating === 'positivo' ? 'Positivo' : 'Corretivo'} para ${targetAgent.name}`,
        agent: targetAgent,
        jiraKey
      });
    }

    // 4. Default: DEBATE & EXECUTION (custom idea)
    let epicName = 'Infraestrutura & Tecnologia';
    if (cleanText.includes('design') || cleanText.includes('tela') || cleanText.includes('cor') || cleanText.includes('layout') || cleanText.includes('frontend') || cleanText.includes('ux') || cleanText.includes('ui') || cleanText.includes('estetica')) {
      epicName = 'Design & Produto';
    } else if (cleanText.includes('daily') || cleanText.includes('sprint') || cleanText.includes('scrum') || cleanText.includes('agil') || cleanText.includes('processo')) {
      epicName = 'Processos Ágeis';
    } else if (cleanText.includes('rh') || cleanText.includes('pessoal') || cleanText.includes('contratar') || cleanText.includes('demissao') || cleanText.includes('feedback')) {
      epicName = 'Gestão de Pessoas';
    }

    const activeAgents = readAgents().filter(a => !a.fired);
    const activeAgentIds = activeAgents.map(a => a.id);

    const simulationResult = await executeDebateSimulation({
      issueKey: '',
      issueSummary: commandText,
      issueDescription: 'Ideia disparada automaticamente via Central de Comando.',
      selectedAgentIds: activeAgentIds,
      epicName
    });

    return res.json({
      success: true,
      actionType: 'DEBATE',
      reasoning: `👥 Sarah Backlog classificou o pedido sob o Épico '${epicName}' e convocou toda a empresa para deliberação autônoma.`,
      ...simulationResult
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /api/agents/hire
app.post('/api/agents/hire', async (req, res) => {
  try {
    const { name, role, level, avatar, advantage, disadvantage, dilemma, personality } = req.body;
    const agents = readAgents();
    
    const newId = slugify(name) || `agent-${Date.now()}`;
    const newAgent = {
      id: newId,
      name,
      role,
      level,
      avatar: avatar || '🤖',
      advantage,
      disadvantage,
      dilemma,
      personality,
      status: 'Disponível',
      schedule: '09:00 - 18:00',
      feedbacks: []
    };

    agents.push(newAgent);
    saveAgents(agents);

    // Sync to Jira under "Gestão de Pessoas" Epic
    let jiraKey = null;
    try {
      const epicMap = await getOrCreateEpics();
      const parentKey = epicMap['Gestão de Pessoas'];
      
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: `Contratação de ${name} (${role})`,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: `Contratação do novo colaborador de inteligência artificial. Vantagem: ${advantage}. Dilema: ${dilemma}.`,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
          issuetype: { name: 'Task' }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      jiraKey = jiraResponse.data?.key;
    } catch (err) {
      console.error('Jira sync error on hire:', err.message);
    }

    res.json({ success: true, agent: newAgent, jiraKey });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /api/agents/fire
app.post('/api/agents/fire', async (req, res) => {
  try {
    const { agentId } = req.body;
    const agents = readAgents();
    const agent = agents.find(a => a.id === agentId);
    if (!agent) {
      return res.status(404).json({ error: 'Agente não encontrado' });
    }

    agent.fired = true; // Mark as fired
    saveAgents(agents);

    // Sync to Jira under "Gestão de Pessoas" Epic
    let jiraKey = null;
    try {
      const epicMap = await getOrCreateEpics();
      const parentKey = epicMap['Gestão de Pessoas'];
      
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: `Demissão de ${agent.name} (${agent.role})`,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: `O colaborador de IA ${agent.name} foi desligado do quadro corporativo.`,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
          issuetype: { name: 'Task' }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      jiraKey = jiraResponse.data?.key;
    } catch (err) {
      console.error('Jira sync error on fire:', err.message);
    }

    res.json({ success: true, agent, jiraKey });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /api/agents/feedback
app.post('/api/agents/feedback', async (req, res) => {
  try {
    const { agentId, feedbackText, rating } = req.body; // rating: 'positivo' | 'negativo'
    const agents = readAgents();
    const agent = agents.find(a => a.id === agentId);
    if (!agent) {
      return res.status(404).json({ error: 'Agente não encontrado' });
    }

    if (!agent.feedbacks) agent.feedbacks = [];
    agent.feedbacks.push({
      timestamp: new Date().toISOString(),
      text: feedbackText,
      rating
    });

    // Adjust personality or advantages based on rating
    if (rating === 'positivo') {
      agent.advantage = `[Fortalecido por Feedback] ${agent.advantage}`;
    } else {
      agent.disadvantage = `[Sinalizado por Feedback] ${agent.disadvantage}`;
    }

    saveAgents(agents);

    // Sync to Jira under "Gestão de Pessoas" Epic
    let jiraKey = null;
    try {
      const epicMap = await getOrCreateEpics();
      const parentKey = epicMap['Gestão de Pessoas'];
      
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: `Feedback ${rating === 'positivo' ? 'Positivo' : 'Corretivo'} para ${agent.name}`,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: `Feedback registrado: ${feedbackText}`,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
          issuetype: { name: 'Task' }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      jiraKey = jiraResponse.data?.key;
    } catch (err) {
      console.error('Jira sync error on feedback:', err.message);
    }

    res.json({ success: true, agent, jiraKey });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST /api/agents/schedule
app.post('/api/agents/schedule', async (req, res) => {
  try {
    const { agentId, schedule, status } = req.body;
    const agents = readAgents();
    const agent = agents.find(a => a.id === agentId);
    if (!agent) {
      return res.status(404).json({ error: 'Agente não encontrado' });
    }

    agent.schedule = schedule;
    agent.status = status;
    saveAgents(agents);

    // Sync to Jira under "Gestão de Pessoas" Epic
    let jiraKey = null;
    try {
      const epicMap = await getOrCreateEpics();
      const parentKey = epicMap['Gestão de Pessoas'];
      
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: `Ajuste de Horário/Status: ${agent.name} -> ${status} (${schedule})`,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: `Jornada definida como ${schedule}. Status do colaborador: ${status}.`,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          parent: parentKey && !parentKey.startsWith('MOCK') ? { key: parentKey } : undefined,
          issuetype: { name: 'Task' }
        }
      };

      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      jiraKey = jiraResponse.data?.key;
    } catch (err) {
      console.error('Jira sync error on schedule update:', err.message);
    }

    res.json({ success: true, agent, jiraKey });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Flose Startup Backend running on port ${PORT}`);
});
