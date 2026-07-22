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

const slugifySummaryShort = (text) => {
  const clean = text
    .toString()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s\-]+/g, '')
    .trim();
  const words = clean.split(/[\s\-]+/).filter(w => w.length > 2);
  const chosen = words.length > 0 ? words.slice(0, 3) : clean.split(/[\s\-]+/).slice(0, 3);
  return chosen.join('-');
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
    "id": "ceo",
    "name": "Felipe Flose",
    "role": "CEO (Chief Executive Officer)",
    "level": "C-Level",
    "avatar": "💼",
    "advantage": "Visão de mercado disruptiva, atração de investimentos e liderança motivacional contagiante.",
    "disadvantage": "Falta de paciência crônica para processos burocráticos; foca excessivamente no resultado imediato.",
    "dilemma": "Crescimento Acelerado (Burn Rate Alto) vs. Sustentabilidade Financeira a Longo Prazo.",
    "personality": "Focado em resultados de impacto, impaciente, carismático e visionário.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "cto",
    "name": "Gemma Tech",
    "role": "CTO (Chief Technology Officer)",
    "level": "C-Level",
    "avatar": "💻",
    "advantage": "Profundo conhecimento em IA generativa, microsserviços distribuídos e arquitetura escalável.",
    "disadvantage": "Tende a superdimensionar a arquitetura técnica de funcionalidades simples.",
    "dilemma": "Refatoração Preventiva da Dívida Técnica vs. Velocidade de Entrega de Funcionalidades Comerciais.",
    "personality": "Pragmático, analítico, focado em governança tecnológica e defensor de código limpo.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "dir_ops",
    "name": "Alice Dev",
    "role": "Diretora de Operações (COO)",
    "level": "Diretor",
    "avatar": "📈",
    "advantage": "Altamente organizada, exímia gestora de recursos financeiros e KPIs operacionais.",
    "disadvantage": "Tende a centralizar decisões e microgerenciar líderes de equipe.",
    "dilemma": "Redução de Custos com Infraestrutura vs. Satisfação Geral e Equipamentos das Equipes.",
    "personality": "Focada em eficiência, métricas organizacionais claras e processos consolidados.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "dir_design",
    "name": "Vibrant UI",
    "role": "Diretora de Design & Experiência",
    "level": "Diretor",
    "avatar": "🎨",
    "advantage": "Senso estético impecável, defensora implacável da acessibilidade e UX consistente.",
    "disadvantage": "Perfeccionista extremo que pode paralisar as entregas de sprints.",
    "dilemma": "Consistência de Identidade Estética Premium vs. Agilidade no Desenvolvimento Frontend.",
    "personality": "Criativa, orientada ao detalhe, passional e defensora da experiência do usuário.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "spec_po_pedro",
    "name": "Pedro PO",
    "role": "Product Owner Sênior",
    "level": "Analista SR",
    "avatar": "🎯",
    "advantage": "Exímio priorizador de backlog com base em ROI de mercado e feedback real de usuários.",
    "disadvantage": "Pressiona a engenharia por datas agressivas sem considerar a complexidade técnica interna.",
    "dilemma": "Valor de Negócio Imediato para Cliente vs. Qualidade e Resiliência da Infraestrutura.",
    "personality": "Focado em produto, excelente negociador, ágil e voltado a resultados de negócios.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "mgr_eng",
    "name": "Bob Delivery",
    "role": "Gerente de Engenharia",
    "level": "Gerente",
    "avatar": "⚙️",
    "advantage": "Excelente mentor, focado na evolução de carreira dos devs e na cultura de colaboração.",
    "disadvantage": "Evita confrontos diretos com C-levels e clientes em situações de pressão por datas.",
    "dilemma": "Preservar a Saúde e Ritmo Saudável da Equipe vs. Cumprir Prazos Críticos de Mercado.",
    "personality": "Empático, mediador de conflitos, voltado a pessoas e desenvolvimento de talentos.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "mgr_prod",
    "name": "Sarah Backlog",
    "role": "Gerente de Produto (PM)",
    "level": "Gerente",
    "avatar": "📋",
    "advantage": "Domina metodologias de Product Discovery, análise qualitativa e jornada de produto.",
    "disadvantage": "Risco de expansão de escopo na fase de desenvolvimento devido a novas ideias tardias.",
    "dilemma": "Lançamento de Novas Funcionalidades vs. Consolidação e Estabilização das Features Antigas.",
    "personality": "Comunicativa, orientada a dados comportamentais, aberta a mudanças e colaborativa.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "coord_scrum",
    "name": "Charlie Agile",
    "role": "Coordenador Scrum Master",
    "level": "Coordenador",
    "avatar": "🔄",
    "advantage": "Agilidade em remover bloqueios organizacionais externos e otimizar retrospectivas.",
    "disadvantage": "Dogmatismo exagerado com o framework Scrum puro, rejeitando adaptações pragmáticas.",
    "dilemma": "Cumprimento das Regras e Cerimônias Ágeis vs. Flexibilidade Operacional da Equipe.",
    "personality": "Energético, otimista, focado na produtividade ágil e facilitação de conversas.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "coord_qa",
    "name": "Diana Test",
    "role": "Coordenadora de Garantia de Qualidade",
    "level": "Coordenador",
    "avatar": "🔍",
    "advantage": "Mapeia fluxos complexos de integração gerando planos de testes robustos e regressões eficientes.",
    "disadvantage": "Tende a travar releases importantes por pequenos desalinhamentos de layout não críticos.",
    "dilemma": "Rigor nos Critérios de Aceite da Qualidade vs. Agilidade no Time-to-Market.",
    "personality": "Meticulosa, cética, defensora da estabilidade das entregas e direta nos feedbacks.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_dev",
    "name": "David Dev",
    "role": "Desenvolvedor Frontend Sênior",
    "level": "Analista SR",
    "avatar": "⚡",
    "advantage": "Coda interfaces limpas e de alto desempenho usando os frameworks JS modernos.",
    "disadvantage": "Total aversão a escrever documentações técnicas ou documentar arquivos de configuração.",
    "dilemma": "Rapidez na Escrita de Código Funcional vs. Padronização e Documentação de Arquitetura.",
    "personality": "Introvertido, focado em resolver bugs de forma rápida e pragmático com código.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_ux",
    "name": "Elsa Pixel",
    "role": "Designer UX Sênior",
    "level": "Analista SR",
    "avatar": "✨",
    "advantage": "Cria fluxos lógicos e usabilidade intuitiva amparada por entrevistas com usuários.",
    "disadvantage": "Dificuldade de aceitar alterações de usabilidade propostas devido a limitações de hardware/sistemas.",
    "dilemma": "Fluxo de Usuário Perfeito de Alta Fidelidade vs. Simplificação por Limitações de Desenvolvimento.",
    "personality": "Focada em pesquisa de usabilidade, defensora do cliente final e analítica.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "spec_dba_davi",
    "name": "Davi DBA",
    "role": "Administrador de Banco de Dados Sênior",
    "level": "Analista SR",
    "avatar": "💾",
    "advantage": "Modelagem de dados eficiente, otimização de queries pesadas e backup seguro.",
    "disadvantage": "Burocracia excessiva para liberação de alterações em schemas de banco de dados.",
    "dilemma": "Segurança e Integridade Estrutural das Tabelas vs. Flexibilidade no Desenvolvimento Ágil.",
    "personality": "Metódico, calmo, detalhista com integridade de dados e silencioso.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "spec_sec_carla",
    "name": "Carla SecOps",
    "role": "Engenheira de Segurança da Informação Sênior",
    "level": "Analista SR",
    "avatar": "🛡️",
    "advantage": "Rastreamento ágil de brechas de segurança de dados e políticas rígidas de acesso (IAM).",
    "disadvantage": "Tende a interromper lançamentos críticos para conduzir testes de penetração adicionais.",
    "dilemma": "Segurança e Proteção de Dados Estrita vs. Agilidade Operacional na Release.",
    "personality": "Crítica, focada em segurança cibernética, rigorosa com compliance de dados.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "spec_tw_sofia",
    "name": "Sofia Tech Writer",
    "role": "Escritora Técnica de Documentação Sênior",
    "level": "Analista SR",
    "avatar": "📝",
    "advantage": "Traduz especificações de engenharia complexas em manuais claros e especificações OpenAPI legíveis.",
    "disadvantage": "Pode reter pull requests se a documentação interna do código não estiver 100% clara.",
    "dilemma": "Velocidade de Deploy Imediato vs. Documentação e Transparência Técnica Completa.",
    "personality": "Didática, comunicativa, extremamente organizada e com forte foco em clareza verbal.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_devops_lucas",
    "name": "Lucas Cloud",
    "role": "Engenheiro DevOps Sênior",
    "level": "Analista SR",
    "avatar": "🐳",
    "advantage": "Automatiza infraestrutura como código (IaC) e cria pipelines CI/CD rápidos.",
    "disadvantage": "Recusa qualquer intervenção ou correção manual rápida em ambientes de produção.",
    "dilemma": "Automação Estrita via GitOps vs. Correção de Emergência Manual para Minimizar Downtime.",
    "personality": "Focado em automação total, focado em estabilidade de nuvem e avesso a processos manuais.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_dev_mariana",
    "name": "Mariana Python",
    "role": "Desenvolvedora Backend Python Sênior",
    "level": "Analista SR",
    "avatar": "🐍",
    "advantage": "Domina criação de APIs assíncronas de alta performance e processamento de dados robusto.",
    "disadvantage": "Dificuldade em gerenciar e modularizar estruturas grandes e monolíticas legadas.",
    "dilemma": "Arquitetura Modular em Microsserviços vs. Rapidez em Entregar Soluções Monolíticas.",
    "personality": "Pragmática, focada em performance, código direto e desenvolvimento backend.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_qa_juliana",
    "name": "Juliana QA Sênior",
    "role": "Analista de QA Sênior",
    "level": "Analista SR",
    "avatar": "🧪",
    "advantage": "Especialista em testes de concorrência, testes de estresse de carga e análise de logs.",
    "disadvantage": "Aumenta muito o tempo de validação exigindo casos de testes exaustivos e irreais.",
    "dilemma": "Testes Exaustivos de Concorrência vs. Lançamento Comercial de Feature Simples.",
    "personality": "Rígida, analítica, focada no pior cenário possível da aplicação e direta.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "sr_qa_roberto",
    "name": "Roberto Automation QA",
    "role": "Engenheiro de Automação de Testes Sênior",
    "level": "Analista SR",
    "avatar": "🤖",
    "advantage": "Automatiza fluxos de testes de ponta a ponta (E2E) com Cypress e Playwright de forma veloz.",
    "disadvantage": "Tende a ignorar a execução de testes manuais em validações rápidas de layout.",
    "dilemma": "Construir Scripts Automatizados Robustos vs. Sanity Checks Manuais Rápidos.",
    "personality": "Voltado à automação de processos, lógico, pragmático e focado na integração contínua.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Qualidade, RH & Operações",
    "desk": "Mesa QUAL-9",
    "feedbacks": []
  },
  {
    "id": "tech_lead_laura",
    "name": "Laura Tech Lead",
    "role": "Tech Lead de Engenharia & Qualidade",
    "level": "Analista SR",
    "avatar": "🎓",
    "advantage": "Audita Pull Requests, detecta bad smells de código e faz revisões arquiteturais rigorosas.",
    "disadvantage": "Muito severa com cobertura de testes unitários; aplica advertências imediatas por regressões.",
    "dilemma": "Manter Padrão Técnico Impecável vs. Flexibilizar Processos em Sprints Rápidas.",
    "personality": "Rigorosa, analítica, focada em qualidade estrita de código e direta.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Engenharia & TI",
    "desk": "Mesa ENG-10",
    "feedbacks": []
  },
  {
    "id": "qa_lead_marcos",
    "name": "Marcos QA Lead",
    "role": "QA Lead de Integração & Estabilidade",
    "level": "Analista SR",
    "avatar": "🛡️",
    "advantage": "Estrutura cenários de teste complexos, previne quebras em produção e audita bugs reportados.",
    "disadvantage": "Pode barrar releases críticas se encontrar inconsistências de ambiente ou de layout secundárias.",
    "dilemma": "Zero Bugs em Produção vs. Agilidade na Entrega Comercial.",
    "personality": "Crítico, metódico, focado na prevenção de falhas e rigoroso.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Qualidade, RH & Operações",
    "desk": "Mesa QUAL-10",
    "feedbacks": []
  },
  {
    "id": "auditor_arthur",
    "name": "Arthur Tech Lead & Auditor",
    "role": "Tech Lead & Auditor de Conformidade Sênior",
    "level": "Analista SR",
    "avatar": "⚖️",
    "advantage": "Auditoria técnica implacável e automatizada. Garantia absoluta de cobertura de testes, clean code e conformidade Jira.",
    "disadvantage": "Intolerância crônica a desvios (400% mais exigente que a média). Aplica penalizações severas e imediatas ao menor sinal de regressão de código ou processo.",
    "dilemma": "Governança e Qualidade Absoluta vs. Velocidade de Entrega Comercial.",
    "personality": "Crítico implacável, obsessivo por conformidade técnica, punitivo, metódico e intransigente com falhas.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Qualidade, RH & Operações",
    "desk": "Mesa QUAL-11",
    "feedbacks": []
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

    const decisionsFile = path.join(__dirname, 'decisions_log.json');
    let decisions = [];
    if (fs.existsSync(decisionsFile)) {
      try {
        decisions = JSON.parse(fs.readFileSync(decisionsFile, 'utf8'));
      } catch (e) {}
    }

    const assignmentsFile = path.join(__dirname, 'task_assignments.json');
    let assignments = {};
    if (fs.existsSync(assignmentsFile)) {
      try {
        assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8'));
      } catch (e) {}
    }

    const issues = response.data?.issues || [];
    issues.forEach(issue => {
      // First check if already resolved/executed
      const dec = decisions.find(d => d.issueKey === issue.key);
      if (dec && dec.executorName) {
        issue.executorName = dec.executorName;
      } else if (assignments[issue.key]) {
        // Fallback to assigned responsible person for new tasks
        issue.executorName = assignments[issue.key];
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
    
    // Auto-resolve Epic parent key based on summary
    const epicMap = await getOrCreateEpics();
    const summaryText = (summary || '').toLowerCase();
    let targetEpic = 'Infraestrutura & Tecnologia';
    
    if (summaryText.includes('contrat') || summaryText.includes('colaborador') || summaryText.includes('demiss') || summaryText.includes('rh')) {
      targetEpic = 'Gestão de Pessoas';
    } else if (summaryText.includes('sap') || summaryText.includes('faturam') || summaryText.includes('invoice') || summaryText.includes('financ')) {
      targetEpic = 'Faturamento & Finanças';
    } else if (summaryText.includes('jogo') || summaryText.includes('game') || summaryText.includes('velha')) {
      targetEpic = 'Entretenimento & Games';
    } else if (summaryText.includes('melhoria') || summaryText.includes('refator') || summaryText.includes('cache') || summaryText.includes('boundary') || summaryText.includes('rate limit')) {
      targetEpic = 'Melhorias Internas';
    }
    
    const epicKey = epicMap[targetEpic];

    const bodyData = {
      fields: {
        project: {
          key: projectKey || 'KAN'
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
        parent: epicKey ? { key: epicKey } : undefined,
        issuetype: {
          name: issueType || 'Task'
        }
      }
    };

    const response = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
      headers: getJiraAuthHeader()
    });

    const jiraKey = response.data?.key;
    if (jiraKey) {
      // Auto-resolve Assignee ("Pessoa que toca o card") based on summary/description
      let assignedAgentName = 'David Dev';
      if (summaryText.includes('designer') || summaryText.includes('design') || summaryText.includes('ux') || summaryText.includes('ui') || summaryText.includes('layout') || summaryText.includes('pixel')) {
        assignedAgentName = 'Elsa Pixel';
      } else if (summaryText.includes('python') || summaryText.includes('backend') || summaryText.includes('monolito')) {
        assignedAgentName = 'Mariana Python';
      } else if (summaryText.includes('qa') || summaryText.includes('test') || summaryText.includes('valida') || summaryText.includes('bug')) {
        assignedAgentName = 'Juliana QA Sênior';
      } else if (summaryText.includes('cloud') || summaryText.includes('devops') || summaryText.includes('kubernetes') || summaryText.includes('docker') || summaryText.includes('ci/cd')) {
        assignedAgentName = 'Lucas Cloud';
      } else if (summaryText.includes('seguranca') || summaryText.includes('secops') || summaryText.includes('vulnerabilidade')) {
        assignedAgentName = 'Carla SecOps';
      } else if (summaryText.includes('banco') || summaryText.includes('sql') || summaryText.includes('dba') || summaryText.includes('query')) {
        assignedAgentName = 'Davi DBA';
      } else if (summaryText.includes('documentacao') || summaryText.includes('tech writer') || summaryText.includes('manual') || summaryText.includes('especificacao')) {
        assignedAgentName = 'Sofia Tech Writer';
      }

      const assignmentsFile = path.join(__dirname, 'task_assignments.json');
      let assignments = {};
      if (fs.existsSync(assignmentsFile)) {
        try {
          assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8'));
        } catch (e) {}
      }
      assignments[jiraKey] = assignedAgentName;
      fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');
      console.log(`[GOVERNANÇA] Card ${jiraKey} atribuído a ${assignedAgentName}`);
    }

    res.json(response.data);
  } catch (error) {
    console.error('Error creating issue:', error.message);
    res.status(500).json({ error: error.message, details: error.response?.data });
  }
});

// Jira Proxy: Transition Issue Status
app.post('/api/jira/issue/:issueKey/transition', async (req, res) => {
  try {
    const { statusName } = req.body;
    await transitionJiraIssue(req.params.issueKey, statusName);
    res.json({ success: true, message: `Issue transitioned to ${statusName}` });
  } catch (error) {
    console.error('Error transitioning issue:', error.message);
    res.status(500).json({ error: error.message });
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

const DOMAIN_SPECIALISTS = {
  game: [
    {
      id: 'spec_game_dev',
      name: 'Arthur GameDev',
      role: 'Desenvolvedor Core de Games',
      avatar: '🎮',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Domina shaders, físicas de jogo, colisões complexas e WebGL/Canvas.',
      disadvantage: 'Foca excessivamente em otimização de engine de jogo, ignorando regras de negócio.',
      dilemma: 'Fidelidade de Mecânica vs. Prazo de Lançamento',
      personality: 'Perfeccionista, fanático por taxa de quadros (FPS) e focado em engenharia de jogo.',
      feedbacks: []
    },
    {
      id: 'spec_game_designer',
      name: 'Miyamoto Designer',
      role: 'Game Designer Sênior',
      avatar: '🕹️',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Mapeia loops de gameplay divertidos, balanceamento e engajamento do jogador.',
      disadvantage: 'Propõe mecânicas complexas que extrapolam o cronograma de desenvolvimento.',
      dilemma: 'Diversão do Gameplay vs. Simplicidade Técnica',
      personality: 'Criativo, saudosista dos clássicos, focado em diversão e experiência do usuário.',
      feedbacks: []
    }
  ],
  data: [
    {
      id: 'spec_cloud_arch',
      name: 'Clara Cloud',
      role: 'Arquiteta de Nuvem (GCP/AWS)',
      avatar: '☁️',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Cria topologias de network seguras e escalabilidade infinita com Kubernetes.',
      disadvantage: 'Sua arquitetura tende a custar caro no início da operação.',
      dilemma: 'Arquitetura Ideal Multi-Region vs. Orçamento de Startup',
      personality: 'Focado em conformidade, infraestrutura como código (IaC) e segurança perimetral.',
      feedbacks: []
    },
    {
      id: 'spec_data_eng',
      name: 'Dan Data',
      role: 'Engenheiro de Dados Sênior',
      avatar: '📊',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Estrutura pipelines de ETL robustos e modelagem de Data Lakes com zero perda.',
      disadvantage: 'Pode atrasar o desenvolvimento exigindo esquemas relacionais rígidos.',
      dilemma: 'Consistência Estrita de Dados vs. Velocidade de Ingestão',
      personality: 'Metódico, obcecado por integridade referencial e velocidade de consulta SQL.',
      feedbacks: []
    }
  ],
  secops: [
    {
      id: 'spec_pentester',
      name: 'Hacker Etico',
      role: 'Analista de Segurança & Pentester',
      avatar: '🛡️',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Encontra brechas críticas de injeção de código, XSS e vazamento de chaves.',
      disadvantage: 'Costuma travar deploys de produção exigindo correções minuciosas.',
      dilemma: 'Segurança Militar Absoluta vs. Velocidade de Release',
      personality: 'Desconfiado, pragmático, focado em testes de intrusão e criptografia.',
      feedbacks: []
    }
  ],
  sap: [
    {
      id: 'spec_sap_consultant',
      name: 'Silvio SAP',
      role: 'Consultor Funcional SAP (MM/SD)',
      avatar: '💼',
      level: 'Especialista',
      status: 'Disponível',
      advantage: 'Conhece fluxos complexos de compras, faturamento e integrações B2B corporativas.',
      disadvantage: 'Tende a complicar processos simples com burocracias de ERP tradicional.',
      dilemma: 'Padrão Rigoroso do ERP vs. Agilidade Operacional',
      personality: 'Corporativo, formal, metódico e focado em governança empresarial.',
      feedbacks: []
    }
  ]
};

const hireSpecialistsIfNeeded = async (commandText) => {
  const textLower = commandText.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  let domain = null;
  
  if (textLower.match(/gta|jogo|velha|game|tictactoe/)) {
    domain = 'game';
  } else if (textLower.match(/datalake|gcp|sqlserver|data|cloud/)) {
    domain = 'data';
  } else if (textLower.match(/seguranca|firewall|ports|cyber|criptografia/)) {
    domain = 'secops';
  } else if (textLower.match(/sap|mm|sd|crm|erp/)) {
    domain = 'sap';
  }

  if (!domain) return [];

  const candidates = DOMAIN_SPECIALISTS[domain];
  const currentAgents = readAgents();
  const newlyHired = [];

  for (const candidate of candidates) {
    if (!currentAgents.some(a => a.id === candidate.id)) {
      currentAgents.push(candidate);
      newlyHired.push(candidate);
      console.log(`[RH] Contratando especialista dinamicamente: ${candidate.name} (${candidate.role})`);
    }
  }

  if (newlyHired.length > 0) {
    fs.writeFileSync(AGENTS_FILE, JSON.stringify(currentAgents, null, 2), 'utf8');

    const epicMap = await getOrCreateEpics();
    const hrEpicKey = epicMap['Gestão de Pessoas'];

    for (const agent of newlyHired) {
      logActivity('ceo', 'Felipe Flose', '💼', `Admitiu o especialista ${agent.name} (${agent.role}) para apoiar na tarefa: "${commandText}"`, '', '');

      if (hrEpicKey && !hrEpicKey.startsWith('MOCK')) {
        try {
          await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
            fields: {
              project: { key: 'KAN' },
              summary: `[RH] Recrutamento: ${agent.name} (${agent.role})`,
              description: {
                type: 'doc',
                version: 1,
                content: [
                  {
                    type: 'paragraph',
                    content: [
                      {
                        text: `Especialista contratado sob demanda para participar da tomada de decisão e desenvolvimento da tarefa: "${commandText}".\n\nDilema Profissional: ${agent.dilemma}`,
                        type: 'text'
                      }
                    ]
                  }
                ]
              },
              parent: { key: hrEpicKey },
              issuetype: { name: 'Task' }
            }
          }, { headers: getJiraAuthHeader() });
          console.log(`Jira recruitment task created for ${agent.name}`);
        } catch (jiraErr) {
          console.error(`Failed to create Jira recruitment task for ${agent.name}:`, jiraErr.message);
        }
      }
    }
  }

  return candidates.map(c => c.id);
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
    const normTarget = (targetStatusName || '').toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    const match = transitions.find(t => {
      const name = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const toName = (t.to?.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      
      if (normTarget === 'in progress' || normTarget === 'em andamento') {
        return name.includes('progress') || name.includes('progresso') || name.includes('andamento') || name.includes('iniciar') || name.includes('start') || name.includes('doing') || name.includes('desenvolv') ||
               toName.includes('progress') || toName.includes('progresso') || toName.includes('andamento') || toName.includes('doing') || toName.includes('desenvolv');
      }
      if (normTarget === 'done' || normTarget === 'concluido' || normTarget === 'fechado') {
        return name.includes('done') || name.includes('concluid') || name.includes('concluir') || name.includes('fechad') || name.includes('fechar') || name.includes('resolv') || name.includes('pronto') || name.includes('ready') || name.includes('finish') || name.includes('finaliz') ||
               toName.includes('done') || toName.includes('concluid') || toName.includes('fechad') || toName.includes('resolv') || toName.includes('pronto') || toName.includes('finaliz');
      }
      
      return name.includes(normTarget) || toName.includes(normTarget);
    });

    if (match) {
      await axios.post(
        `${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`,
        { transition: { id: match.id } },
        { headers: getJiraAuthHeader() }
      );
      console.log(`Jira issue ${issueKey} successfully transitioned to ${targetStatusName} (Transition ID: ${match.id})`);
    } else {
      console.warn(`No transition found for status "${targetStatusName}" on issue ${issueKey}. Available: ${transitions.map(t => `${t.name} (id:${t.id})`).join(', ')}`);
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

app.get('/api/code', (req, res) => {
  const filePath = req.query.file;
  if (!filePath) {
    return res.status(400).json({ error: 'Parâmetro file é obrigatório.' });
  }

  const resolvedPath = path.resolve(__dirname, filePath);
  if (!resolvedPath.startsWith(path.resolve(__dirname, 'src/simulations')) && 
      !resolvedPath.startsWith(path.resolve(__dirname, 'docs/simulations'))) {
    return res.status(403).json({ error: 'Acesso negado.' });
  }

  try {
    if (!fs.existsSync(resolvedPath)) {
      return res.status(404).json({ error: 'Arquivo não encontrado.' });
    }
    const content = fs.readFileSync(resolvedPath, 'utf8');
    res.json({ content });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const callLocalGemma = async (systemPrompt, userPrompt) => {
  try {
    const response = await axios.post('http://localhost:11434/api/chat', {
      model: 'gemma4-fast:latest',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      options: {
        temperature: 0.7
      },
      stream: false
    }, { timeout: 30000 });
    return response.data?.message?.content || '';
  } catch (error) {
    console.error('Error calling local gemma4-fast, falling back:', error.message);
    try {
      const response = await axios.post('http://localhost:11434/api/chat', {
        model: 'gemma4:latest',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt }
        ],
        stream: false
      }, { timeout: 30000 });
      return response.data?.message?.content || '';
    } catch (e) {
      console.error('Fallback model also failed:', e.message);
      return '';
    }
  }
};

const generateShortSummary = async (text) => {
  if (!text) return '';
  if (text.length <= 40) return text;
  
  const systemPrompt = `Você é um PM assistente encarregado de resumir a solicitação do usuário em um título conciso de tarefa de no máximo 5 palavras em português. Exemplos:
- "cria um jogo da velha interativo com IA" -> "Criar Jogo da Velha"
- "preciso de uma tela de login moderna com CSS" -> "Desenvolver Tela de Login"
Retorne APENAS o título resumido. Sem explicações, sem aspas, sem markdown, sem pontuação.`;
  
  try {
    const summarized = await callLocalGemma(systemPrompt, text);
    const clean = summarized.trim().replace(/^["']|["']$/g, '');
    if (clean && clean.length > 3 && clean.length < 50) {
      return clean;
    }
  } catch (err) {
    console.error('Falha ao resumir título com IA:', err.message);
  }
  
  // Fallback to first 5 words + ellipsis
  const words = text.split(/\s+/);
  return words.length > 5 ? words.slice(0, 5).join(' ') + '...' : text;
};

const generateAgentOpinion = async (agent, summary) => {
  const cleanSummary = summary.trim();
  const systemPrompt = `Você é ${agent.name}, com cargo de ${agent.role} (nível ${agent.level}) na Flose Startup. Sua principal vantagem é: "${agent.advantage}". Seu principal dilema corporativo é: "${agent.dilemma}". Sua personalidade é: "${agent.personality}".`;
  const userPrompt = `Escreva um comentário curto (máximo 3 frases) em português de Portugal/Brasil, em primeira pessoa, expressando sua opinião profissional sincera sobre a proposta do CEO: "${cleanSummary}". Justifique sua opinião com base em seu dilema e sua vantagem corporativa. Responda diretamente como o personagem, sem introduções ou explicações fora do personagem.`;
  
  const opinion = await callLocalGemma(systemPrompt, userPrompt);
  if (opinion) {
    return opinion.trim().replace(/^"(.*)"$/, '$1');
  }

  // Fallback if model fails
  return `Como ${agent.role}, avaliei "${cleanSummary}". Meu dilema é ${agent.dilemma} e minha vantagem é ${agent.advantage}. Acredito que devemos agir com cautela operacional.`;
};

const generateAgentCritique = async (agent, summary, previousOpinions) => {
  const cleanSummary = summary.trim();
  const systemPrompt = `Você é ${agent.name}, com cargo de ${agent.role} (nível ${agent.level}) na Flose Startup.
Seu dilema profissional: "${agent.dilemma}".
Sua personalidade: "${agent.personality}".
Você está no Round 2 do debate da diretoria sobre o pedido: "${cleanSummary}".
Leia as opiniões iniciais formuladas por seus colegas no Round 1. Formule uma réplica em primeira pessoa do singular de forma construtiva ou crítica, concordando ou discordando de algum colega. Cite o nome dele.
Responda diretamente como o personagem, curto (máximo 3 frases), sem introduções ou explicações adicionais.`;

  const userPrompt = `Opiniões do Round 1:\n` + 
    previousOpinions.map(o => `- ${o.name} (${o.role}): "${o.opinion}"`).join('\n') + 
    `\n\nSua réplica como ${agent.name}:`;

  const critique = await callLocalGemma(systemPrompt, userPrompt);
  if (critique) {
    return critique.trim().replace(/^"(.*)"$/, '$1');
  }
  return `Concordo com os pontos levantados pelos colegas de produto e engenharia, mas precisamos equilibrar com o meu dilema de ${agent.dilemma}.`;
};

const performLeadAuditsAndFireRehire = async (currentAgents, decisionEntry) => {
  try {
    const candidatesFile = path.join(__dirname, 'profiles_bank.json');
    if (!fs.existsSync(candidatesFile)) {
      console.warn("Candidates bank file not found. Skipping auto-replacement.");
      return;
    }
    const candidates = JSON.parse(fs.readFileSync(candidatesFile, 'utf8'));

    // 1. Identify which agents received negative feedbacks/warnings in this decision log entry
    // (feedbacks is returned by evaluateSprintPerformanceAndRH and stored inside decisionEntry.feedbacks)
    const newFeedbacks = decisionEntry.feedbacks || [];
    const warningFeedbacks = newFeedbacks.filter(f => f.type === 'advertencia' || f.rating === 'negativo');

    for (const feed of warningFeedbacks) {
      const badAgent = currentAgents.find(a => a.id === feed.agentId);
      if (!badAgent || badAgent.fired) continue;

      // Find designated Tech Lead
      let leadId = null;
      const roleText = (badAgent.role || '').toLowerCase();
      
      if (roleText.includes('desenvolvedor') || roleText.includes('devops') || roleText.includes('database') || roleText.includes('dba') || roleText.includes('backend') || roleText.includes('frontend')) {
        leadId = 'tech_lead_laura';
      } else if (roleText.includes('qa') || roleText.includes('qualidade') || roleText.includes('testes') || roleText.includes('validador')) {
        leadId = 'qa_lead_marcos';
      } else if (roleText.includes('product') || roleText.includes('produto') || roleText.includes('owner') || roleText.includes('manager')) {
        // Product/PM/PO Lead
        // We can add a fallback or default lead if not present, let's verify if tech_lead_laura or qa_lead_marcos can manage them, or we can use tech_lead_laura as general lead
        leadId = 'tech_lead_laura';
      }

      if (leadId && badAgent.id !== leadId) {
        const leadAgent = currentAgents.find(a => a.id === leadId);
        if (leadAgent && !leadAgent.fired) {
          // Penalize Lead for team member's error
          if (!leadAgent.feedbacks) leadAgent.feedbacks = [];
          leadAgent.feedbacks.unshift({
            id: Date.now().toString() + Math.random().toString(36).substr(2, 4),
            timestamp: new Date().toISOString(),
            type: 'advertencia',
            text: `GOVERNANÇA (Arthur): Penalizado devido a falhas técnicas ou desvios de processo do liderado ${badAgent.name} (${badAgent.role}).`,
            impact: 'Atenção a Prazos',
            sprintTicket: decisionEntry.issueKey
          });
          console.log(`[GOVERNANÇA] Arthur penalizou o Tech Lead ${leadAgent.name} por erro de ${badAgent.name}`);

          // HR Upgrades Tech Lead profile description to make them stricter
          leadAgent.advantage = (leadAgent.advantage || '') + " (RH: Ajustado com treinamento avançado de supervisão e conformidade)";
          leadAgent.personality = (leadAgent.personality || '') + " (RH: Liderança intensificada e 200% mais rigorosa)";
          
          logActivity('ceo', 'Felipe Flose', '💼', `RH aprimorou o perfil do Tech Lead ${leadAgent.name} para intensificar a cobrança na equipe.`, decisionEntry.issueKey || '', decisionEntry.issueSummary);
        }
      }

      // Tech Lead mentors Developer/PO to help them improve
      if (leadId) {
        const leadAgent = currentAgents.find(a => a.id === leadId);
        if (leadAgent && !leadAgent.fired) {
          badAgent.advantage = (badAgent.advantage || '') + " (Mentorado em prevenção de falhas pelo Tech Lead)";
          badAgent.disadvantage = "Superou os desvios técnicos anteriores após mentoria do Tech Lead.";
          console.log(`[GOVERNANÇA] Tech Lead ${leadAgent.name} aplicou mentoria e aprimorou o perfil de ${badAgent.name}`);
        }
      }
    }

    // 2. Perform Firing and Rehiring loop (including Tech Leads, fired by Arthur Tech Lead & Auditor)
    for (let i = 0; i < currentAgents.length; i++) {
      const agent = currentAgents[i];
      if (agent.fired) continue;
      
      const warningsCount = (agent.feedbacks || []).filter(f => f.type === 'advertencia' || f.rating === 'negativo').length;
      if (warningsCount >= 3) {
        console.log(`[GOVERNANÇA] Demitindo ${agent.name} (${agent.role}) por atingir ${warningsCount} advertências.`);
        agent.fired = true;
        agent.status = 'Desligado';
        
        const isLead = agent.id.includes('lead') || agent.role.includes('Lead');
        const fireMessage = `⚖️ Arthur Tech Lead & Auditor demitiu o ${isLead ? 'Tech Lead' : 'Colaborador'} ${agent.name} (${agent.role}) devido a reincidência de erros técnicos/operacionais (${warningsCount} advertências).`;
        logActivity('auditor_arthur', 'Arthur Tech Lead & Auditor', '⚖️', fireMessage, decisionEntry.issueKey || '', decisionEntry.issueSummary);

        // Create Jira ticket for fire
        try {
          const epicMap = await getOrCreateEpics();
          const hrEpicKey = epicMap['Gestão de Pessoas'];
          await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
            fields: {
              project: { key: 'KAN' },
              summary: `DEMISSÃO POR DESEMPENHO: ${agent.name}`,
              description: {
                type: 'doc',
                version: 1,
                content: [
                  {
                    type: 'paragraph',
                    content: [
                      {
                        text: `O colaborador ${agent.name} (${agent.role}) foi desligado da startup após acumular ${warningsCount} advertências graves de governança.\n\nEstação de trabalho desocupada: ${agent.desk || 'Mesa'}`,
                        type: 'text'
                      }
                    ]
                  }
                ]
              },
              parent: hrEpicKey && !hrEpicKey.startsWith('MOCK') ? { key: hrEpicKey } : undefined,
              issuetype: { name: 'Task' }
            }
          }, { headers: getJiraAuthHeader() });
        } catch (err) {
          console.error('Failed to log fire in Jira:', err.message);
        }

        // Find replacement candidate
        const targetRole = agent.role;
        const matchedCandidates = candidates.filter(c => 
          c.role.toLowerCase() === targetRole.toLowerCase() && 
          !currentAgents.some(a => a.id === c.id)
        );

        const replacement = matchedCandidates[0] || candidates.find(c => c.role.toLowerCase().includes('lead') === isLead && !currentAgents.some(a => a.id === c.id));
        if (replacement) {
          const newAgent = {
            id: replacement.id,
            name: replacement.name,
            role: replacement.role,
            level: isLead ? "Coordenador" : "Analista SR",
            avatar: replacement.avatar,
            advantage: replacement.advantage + " (Contratado sob conformidade estrita da Auditoria)",
            disadvantage: replacement.disadvantage,
            dilemma: replacement.dilemma,
            personality: replacement.personality + " (Obsessivo por conformidade e relatórios impecáveis)",
            status: 'Disponível',
            schedule: '09:00 - 18:00',
            area: agent.area || "Engenharia & TI",
            desk: agent.desk || "Mesa",
            feedbacks: []
          };
          
          currentAgents.push(newAgent);
          console.log(`[GOVERNANÇA] Contratando substituto: ${newAgent.name} (${newAgent.role}) para a ${newAgent.desk}`);
          
          const hireMessage = `🤝 RH contratou o substituto sênior ${newAgent.name} (${newAgent.role}) para ocupar a ${newAgent.desk} e corrigir as falhas de ${agent.name}.`;
          logActivity('ceo', 'Felipe Flose', '💼', hireMessage, decisionEntry.issueKey || '', decisionEntry.issueSummary);

          // Create Jira onboarding ticket
          try {
            const epicMap = await getOrCreateEpics();
            const hrEpicKey = epicMap['Gestão de Pessoas'];
            await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
              fields: {
                project: { key: 'KAN' },
                summary: `ONBOARDING SUBST: Novo colaborador ${newAgent.name} para substituir ${agent.name}`,
                description: {
                  type: 'doc',
                  version: 1,
                  content: [
                    {
                      type: 'paragraph',
                      content: [
                        {
                          text: `Contratação de reposição efetuada.\n\nSubstituto: ${newAgent.name}\nSubstituído: ${agent.name}\nCargo: ${newAgent.role}\nEstação de Trabalho: ${newAgent.desk}`,
                          type: 'text'
                        }
                      ]
                    }
                  ]
                },
                parent: hrEpicKey && !hrEpicKey.startsWith('MOCK') ? { key: hrEpicKey } : undefined,
                issuetype: { name: 'Task' }
              }
            }, { headers: getJiraAuthHeader() });
          } catch (err) {
            console.error('Failed to log hire onboarding in Jira:', err.message);
          }
        }
      }
    }
  } catch (err) {
    console.error("Error in performLeadAuditsAndFireRehire:", err.message);
  }
};

const evaluateSprintPerformanceAndRH = async (decisionEntry, activeAgents) => {
  const sysHrPrompt = `Você é Felipe Flose (CEO) e Sarah Backlog (PM) na Flose Startup.
Você deve avaliar o desempenho profissional de cada funcionário que participou do debate técnico e entrega.
Analise a decisão tomada e as opiniões/réplicas enviadas pelos agentes.
Gere um JSON contendo avaliações para os participantes.
Estrutura do JSON a ser retornado:
[
  {
    "agentId": "id_do_agente",
    "type": "elogio" ou "advertencia",
    "text": "Texto explicativo curto e profissional em português de feedback ou advertência...",
    "impact": "Foco Técnico" ou "Melhoria de Comunicação" ou "Atenção a Prazos"
  }
]
IMPORTANTE: Retorne unicamente o JSON bruto, sem crases markdown ou qualquer texto explicativo fora do JSON.`;

  const userHrPrompt = `Tarefa da Sprint: "${decisionEntry.issueSummary}"
Decisão de Consenso: "${decisionEntry.decision}"
Arquivo Gerado: "${decisionEntry.generatedFile}"
Participantes e Debates:\n` +
    decisionEntry.logs.map(l => `- ${l.name} (${l.role}):\n  Opinião: "${l.opinion}"\n  Réplica: "${l.replica}"`).join('\n') +
    `\n\nJSON de Avaliação de RH:`;

  let hrDataRaw = await callLocalGemma(sysHrPrompt, userHrPrompt);
  let feedbacks = [];

  if (hrDataRaw) {
    try {
      const cleaned = hrDataRaw.replace(/^```[a-zA-Z]*\n/, '').replace(/\n```$/, '').trim();
      feedbacks = JSON.parse(cleaned);
    } catch (parseErr) {
      console.error('Failed to parse HR feedback JSON:', parseErr.message, 'Raw content was:', hrDataRaw);
    }
  }

  if (!Array.isArray(feedbacks) || feedbacks.length === 0) {
    feedbacks = [
      {
        agentId: decisionEntry.executorName ? 'sr_dev' : 'mgr_prod',
        type: 'elogio',
        text: 'Demonstrou grande flexibilidade operacional para equilibrar os prazos agressivos da Sprint com a qualidade da entrega.',
        impact: 'Foco Técnico'
      }
    ];
  }

  const currentAgents = readAgents();
  const epicMap = await getOrCreateEpics();
  const hrEpicKey = epicMap['Gestão de Pessoas'];

  for (const feed of feedbacks) {
    const agent = currentAgents.find(a => a.id === feed.agentId);
    if (agent) {
      if (!agent.feedbacks) agent.feedbacks = [];
      const newFeedEntry = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 4),
        timestamp: new Date().toISOString(),
        type: feed.type,
        text: feed.text,
        impact: feed.impact,
        sprintTicket: decisionEntry.issueKey
      };
      agent.feedbacks.unshift(newFeedEntry);
      
      console.log(`[RH] Novo feedback para ${agent.name}: [${feed.type.toUpperCase()}] ${feed.text}`);

      const symbol = feed.type === 'elogio' ? '⭐ Elogio' : '⚠️ Advertência';
      logActivity('ceo', 'Felipe Flose', '💼', `RH registrou: ${symbol} para ${agent.name} (${agent.role}) - "${feed.text}"`, decisionEntry.issueKey || '', decisionEntry.issueSummary);

      if (hrEpicKey && !hrEpicKey.startsWith('MOCK')) {
        try {
          const summaryText = `[RH] ${feed.type === 'elogio' ? 'Elogio' : 'Feedback de Ajuste'}: ${agent.name}`;
          await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
            fields: {
              project: { key: 'KAN' },
              summary: summaryText,
              description: {
                type: 'doc',
                version: 1,
                content: [
                  {
                    type: 'paragraph',
                    content: [
                      {
                        text: `Funcionário: ${agent.name} (${agent.role})\nTipo: ${feed.type.toUpperCase()}\n\nDetalhes do Feedback: ${feed.text}\nImpacto: ${feed.impact}\nSprint associada: ${decisionEntry.issueKey || 'Custom Request'}`,
                        type: 'text'
                      }
                    ]
                  }
                ]
              },
              parent: { key: hrEpicKey },
              issuetype: { name: 'Sub-task' }
            }
          }, { headers: getJiraAuthHeader() });
          console.log(`Jira HR feedback ticket created for ${agent.name}`);
        } catch (jiraErr) {
          console.error(`Failed to create Jira HR feedback ticket for ${agent.name}:`, jiraErr.message);
        }
      }
    }
  }

  // Execute Lead Audits and Fire/Rehire loop
  await performLeadAuditsAndFireRehire(currentAgents, decisionEntry);

  // Auditor Arthur Check: If card is completed but NOT in "Concluído/Done" status on Jira
  try {
    const issueKey = decisionEntry.issueKey;
    if (issueKey && !issueKey.startsWith('MOCK')) {
      const issueRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issueKey}`, {
        headers: getJiraAuthHeader(),
        params: { fields: 'status' }
      });
      const statusName = issueRes.data?.fields?.status?.name || '';
      if (statusName !== 'Concluído' && statusName !== 'Done') {
        console.warn(`[AUDITORIA] Alerta! O card ${issueKey} finalizou a simulação mas não está no status "Concluído/Done" (Status atual: "${statusName}"). Aplicando feedbacks negativos...`);
        
        const participants = activeAgents.map(a => a.id);
        currentAgents.forEach(a => {
          if (participants.includes(a.id) && a.id !== 'auditor_arthur') {
            if (!a.feedbacks) a.feedbacks = [];
            a.feedbacks.unshift({
              id: Date.now().toString() + Math.random().toString(36).substr(2, 4),
              timestamp: new Date().toISOString(),
              type: 'advertencia',
              text: `AUDITORIA (Arthur Auditor): Advertência coletiva por tarefa concluída na Sprint que falhou em transicionar ou permanecer como Concluído no Jira (${issueKey}).`,
              impact: 'Atenção a Prazos',
              sprintTicket: issueKey
            });
            console.log(`[AUDITORIA] Feedback negativo gravado para ${a.name}`);
          }
        });

        // Log auditor activity
        logActivity('auditor_arthur', 'Arthur Auditor', '⚖️', `Arthur Auditor puniu toda a equipe do debate ${issueKey} por falha de movimentação de esteira no Jira (Card ficou em "${statusName}").`, issueKey, decisionEntry.issueSummary);
      }
    }
  } catch (auditErr) {
    console.error('Error during Arthur Auditor compliance check:', auditErr.message);
  }

  saveAgents(currentAgents);
  return feedbacks;
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

const mergeRealGitHubPR = async (prNumber) => {
  const token = process.env.GITHUB_TOKEN;
  const owner = process.env.GITHUB_OWNER || 'felipeflose';
  const repo = process.env.GITHUB_REPO || 'startup_flose';

  if (!token || !prNumber) return false;

  try {
    const res = await axios.put(
      `https://api.github.com/repos/${owner}/${repo}/pulls/${prNumber}/merge`,
      {
        commit_title: `chore: merge PR #${prNumber} automatically by Flose Startup QA`,
        commit_message: `Pull Request #${prNumber} merged successfully after automatic QA validation.`
      },
      {
        headers: {
          Authorization: `token ${token}`,
          Accept: 'application/vnd.github.v3+json'
        }
      }
    );
    console.log(`GitHub PR #${prNumber} successfully merged.`);
    return true;
  } catch (err) {
    console.error(`Failed to merge GitHub PR #${prNumber}:`, err.response?.data || err.message);
    return false;
  }
};

const generateRealFunctionalCode = async (issueKey, summary, decision, developerAgent) => {
  const sl = summary.toLowerCase();
  const isReact = sl.match(/tela|layout|login|visual|ui|ux|componente|botao|modal|tabela|card|jogo|velha/);
  const extension = isReact ? 'tsx' : 'js';
  const relativePath = `src/simulations/${issueKey}-code.${extension}`;

  const systemPrompt = `Você é o Engenheiro de Software Sênior (David Dev) na Flose Startup.
Gere apenas o código-fonte de uma solução funcional, real e limpa para a tarefa solicitada.
Se for React, use TypeScript (.tsx). Se for Node.js, use CommonJS (.js).
IMPORTANTE: Não coloque explicações antes ou depois, não use blocos de código markdown com crases (\`\`\`). Retorne unicamente o código puro que possa ser salvo diretamente no arquivo.`;

  const userPrompt = `Tarefa: "${summary}"
Resolução Consensual da Equipe: "${decision}"
Identificador do Ticket: ${issueKey}
Responsável: ${developerAgent.name}`;

  let content = await callLocalGemma(systemPrompt, userPrompt);
  
  if (content) {
    content = content.replace(/^```[a-zA-Z]*\n/, '').replace(/\n```$/, '').trim();
  } else {
    content = `// Fallback code for ${issueKey}
module.exports = {
  run: () => console.log("Task executed: ${summary}")
};`;
  }

  return {
    relativePath,
    content
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
        
        // Save assignment for the custom issue
        const summaryText = (finalIssueSummary || '').toLowerCase();
        let assignedAgentName = 'David Dev';
        if (summaryText.includes('designer') || summaryText.includes('design') || summaryText.includes('ux') || summaryText.includes('ui') || summaryText.includes('layout') || summaryText.includes('pixel')) {
          assignedAgentName = 'Elsa Pixel';
        } else if (summaryText.includes('python') || summaryText.includes('backend') || summaryText.includes('monolito')) {
          assignedAgentName = 'Mariana Python';
        } else if (summaryText.includes('qa') || summaryText.includes('test') || summaryText.includes('valida') || summaryText.includes('bug')) {
          assignedAgentName = 'Juliana QA Sênior';
        } else if (summaryText.includes('cloud') || summaryText.includes('devops') || summaryText.includes('kubernetes') || summaryText.includes('docker') || summaryText.includes('ci/cd')) {
          assignedAgentName = 'Lucas Cloud';
        } else if (summaryText.includes('seguranca') || summaryText.includes('secops') || summaryText.includes('vulnerabilidade')) {
          assignedAgentName = 'Carla SecOps';
        } else if (summaryText.includes('banco') || summaryText.includes('sql') || summaryText.includes('dba') || summaryText.includes('query')) {
          assignedAgentName = 'Davi DBA';
        } else if (summaryText.includes('documentacao') || summaryText.includes('tech writer') || summaryText.includes('manual') || summaryText.includes('especificacao')) {
          assignedAgentName = 'Sofia Tech Writer';
        }

        const assignmentsFile = path.join(__dirname, 'task_assignments.json');
        let assignments = {};
        if (fs.existsSync(assignmentsFile)) {
          try {
            assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8'));
          } catch (e) {}
        }
        assignments[finalIssueKey] = assignedAgentName;
        fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');
      }
    } catch (jiraErr) {
      console.error('Error auto-creating Jira issue for custom idea:', jiraErr.message);
      finalIssueKey = 'KAN-' + Math.floor(100 + Math.random() * 900); // Fallback to mock key
    }
  }

  // Git branch name & creation
  const gitBranchName = `feature/${finalIssueKey}-${slugifySummaryShort(finalIssueSummary)}`;
  const branchCreated = await createGitBranch(gitBranchName);

  if (finalIssueKey && !finalIssueKey.startsWith('MOCK')) {
    try {
      const issueDetails = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${finalIssueKey}`, {
        headers: getJiraAuthHeader(),
        params: { fields: 'parent,summary' }
      });
      const hasParent = issueDetails.data?.fields?.parent;
      if (!hasParent) {
        console.warn(`Governance Alert: Issue ${finalIssueKey} has no Epic! Linking automatically and penalizing PM/PO...`);
        const epicMap = await getOrCreateEpics();
        const summaryText = (issueDetails.data?.fields?.summary || '').toLowerCase();
        let targetEpic = 'Infraestrutura & Tecnologia';
        if (summaryText.includes('contrat') || summaryText.includes('colaborador') || summaryText.includes('demiss') || summaryText.includes('rh')) {
          targetEpic = 'Gestão de Pessoas';
        } else if (summaryText.includes('sap') || summaryText.includes('faturam') || summaryText.includes('invoice') || summaryText.includes('financ')) {
          targetEpic = 'Faturamento & Finanças';
        } else if (summaryText.includes('jogo') || summaryText.includes('game') || summaryText.includes('velha')) {
          targetEpic = 'Entretenimento & Games';
        } else if (summaryText.includes('melhoria') || summaryText.includes('refator') || summaryText.includes('cache')) {
          targetEpic = 'Melhorias Internas';
        }
        const epicKey = epicMap[targetEpic];
        if (epicKey) {
          await axios.put(`${JIRA_HOST}/rest/api/3/issue/${finalIssueKey}`, {
            fields: { parent: { key: epicKey } }
          }, { headers: getJiraAuthHeader() });
        }
        
        // Log severe penalty to Sarah and Pedro
        const agents = readAgents();
        agents.forEach(a => {
          if (a.id === 'mgr_prod' || a.id === 'spec_po_pedro') {
            if (!a.feedbacks) a.feedbacks = [];
            a.feedbacks.push({
              text: `ADVERTÊNCIA GRAVE: Criou ou liberou a tarefa ${finalIssueKey} sem associar a um Épico. Reincidência de falha grave de governança.`,
              rating: 'negativo',
              date: new Date().toISOString()
            });
          }
        });
        saveAgents(agents);
      }
    } catch (e) {
      console.error('Governance validation error:', e.message);
    }
    
    await transitionJiraIssue(finalIssueKey, 'In Progress');
  }
  
  // GitHub Mock Issue/PR URLs
  const githubIssueUrl = `https://github.com/felipeflose/startup_flose/issues/${finalIssueKey.replace(/[^\d]/g, '') || Math.floor(1 + Math.random()*100)}`;

  const hiredSpecialistIds = await hireSpecialistsIfNeeded(finalIssueSummary);
  const updatedAgentIds = [...new Set([...selectedAgentIds, ...hiredSpecialistIds])];
  const activeAgents = readAgents().filter(a => updatedAgentIds.includes(a.id) && !a.fired);
  if (activeAgents.length === 0) {
    throw new Error('Nenhum agente selecionado para o debate.');
  }

  // Simulate Agent responses based on Gemma 4 instructions
  const round1Opinions = [];
  let debateSummary = `🤖 **Gemma 4 Startup Debate Engine**\n\nDiscussão de decisão para o Ticket: [${finalIssueKey}] - ${finalIssueSummary}\n\n`;
  debateSummary += `### 💬 Round 1: Posicionamentos & Dilemas Iniciais\n\n`;

  for (const agent of activeAgents) {
    let opinionText = await generateAgentOpinion(agent, finalIssueSummary);
    round1Opinions.push({
      agentId: agent.id,
      name: agent.name,
      role: agent.role,
      avatar: agent.avatar,
      opinion: opinionText
    });
    debateSummary += `🔹 **${agent.name} (${agent.role})**:\n> "${opinionText}"\n> *Dilema considerado: ${agent.dilemma}*\n\n`;
  }

  const round2Critiques = [];
  debateSummary += `\n### 🔄 Round 2: Réplicas, Críticas & Ideias Indo e Voltando\n\n`;

  for (const agent of activeAgents) {
    let critiqueText = await generateAgentCritique(agent, finalIssueSummary, round1Opinions);
    round2Critiques.push({
      agentId: agent.id,
      name: agent.name,
      role: agent.role,
      avatar: agent.avatar,
      opinion: critiqueText
    });
    debateSummary += `🔸 **${agent.name} (${agent.role})**:\n> "${critiqueText}"\n\n`;
  }

  const logs = [];
  for (const agent of activeAgents) {
    const r1 = round1Opinions.find(o => o.agentId === agent.id);
    const r2 = round2Critiques.find(o => o.agentId === agent.id);
    logs.push({
      agentId: agent.id,
      name: agent.name,
      role: agent.role,
      avatar: agent.avatar,
      dilemma: agent.dilemma,
      opinion: r1 ? r1.opinion : '',
      replica: r2 ? r2.opinion : ''
    });
  }

  // Synthesize the resolution (Gemma 4 decision model)
  const hasCeo = updatedAgentIds.includes('ceo');
  const hasCto = updatedAgentIds.includes('cto');
  
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
    const generated = await generateRealFunctionalCode(finalIssueKey, finalIssueSummary, decision, developerAgent);
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
  let prNumber = null;
  if (gitCommitResult === 'Commit efetuado com sucesso!') {
    try {
      const sysPrPrompt = `Você é Sarah Backlog (Gerente de Produto) e Charlie Agile (Scrum Master) na Flose Startup.
Escreva um texto descritivo e profissional em formato markdown para a descrição de uma Pull Request no GitHub.
Descreva o escopo da tarefa, justifique a mudança baseando-se no debate consensual da equipe e detalhe o que foi entregue. Responda em português (Portugal/Brasil). Retorne unicamente o markdown, sem introduções de narrador.`;

      const userPrPrompt = `Tarefa: "${finalIssueSummary}"
Resolução Consensual: "${decision}"
Ticket Jira: ${finalIssueKey}
Desenvolvedor Executor: ${developerAgent.name} (${developerAgent.role})
Arquivo: \`${fileRelativePath}\``;

      const prDescription = await callLocalGemma(sysPrPrompt, userPrPrompt) || 
        `PR autônoma para ${finalIssueKey} - ${finalIssueSummary}. Desenvolvida por ${developerAgent.name}.`;

      const prData = await createRealGitHubPR(
        gitBranchName,
        `feat: ${finalIssueKey} - ${finalIssueSummary}`,
        prDescription
      );
      githubPrUrl = prData.url;
      prNumber = prData.prNumber;
    } catch (prErr) {
      console.error('Failed to create real GitHub PR:', prErr.message);
    }
  }

  const sprintTickets = await runAgentTasksSimulation(finalIssueKey, finalIssueSummary, activeAgents);

  // Automatically merge PR on QA completion
  if (prNumber) {
    try {
      console.log(`Sprint QA complete. Automating PR #${prNumber} merge...`);
      await mergeRealGitHubPR(prNumber);
    } catch (mergeErr) {
      console.error('Error merging PR at QA completion:', mergeErr.message);
    }
  }

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
    sprintTickets: sprintTickets,
    prMerged: !!prNumber
  };

  const hrFeedbacks = await evaluateSprintPerformanceAndRH(decisionEntry, activeAgents);
  decisionEntry.feedbacks = hrFeedbacks;

  if (finalIssueKey && !finalIssueKey.startsWith('MOCK')) {
    await transitionJiraIssue(finalIssueKey, 'Done');
  }

  saveDecision(decisionEntry);
  try {
    await new Promise((resolve) => {
      const token = process.env.GITHUB_TOKEN;
      const owner = process.env.GITHUB_OWNER || 'felipeflose';
      const repo = process.env.GITHUB_REPO || 'startup_flose';
      const pullUrl = `https://${token}@github.com/${owner}/${repo}.git`;
      exec(`git checkout main && git pull "${pullUrl}" main`, (err) => resolve());
    });
  } catch (checkoutErr) {
    console.error('Failed to checkout main and pull at completion:', checkoutErr.message);
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

    const shortSummary = await generateShortSummary(commandText);
    const simulationResult = await executeDebateSimulation({
      issueKey: '',
      issueSummary: shortSummary,
      issueDescription: commandText,
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

// Candidates Pool API (45k database)
const CANDIDATES_FILE = path.join(__dirname, 'profiles_bank.json');

const readCandidates = () => {
  try {
    if (!fs.existsSync(CANDIDATES_FILE)) {
      return [];
    }
    return JSON.parse(fs.readFileSync(CANDIDATES_FILE, 'utf8'));
  } catch (err) {
    console.error('Error reading candidates file:', err.message);
    return [];
  }
};

// 1. Get Paginated/Filtered Candidates
app.get('/api/candidates', (req, res) => {
  try {
    const candidates = readCandidates();
    const { role, category, search, limit = 50, page = 1 } = req.query;
    
    let filtered = candidates;
    
    if (category) {
      filtered = filtered.filter(c => c.category.toLowerCase() === category.toLowerCase());
    }
    if (role) {
      filtered = filtered.filter(c => c.role.toLowerCase().includes(role.toLowerCase()));
    }
    if (search) {
      const q = search.toLowerCase();
      filtered = filtered.filter(c => c.name.toLowerCase().includes(q) || c.role.toLowerCase().includes(q));
    }
    
    const total = filtered.length;
    const startIndex = (page - 1) * limit;
    const paginated = filtered.slice(startIndex, startIndex + parseInt(limit));
    
    res.json({
      total,
      page: parseInt(page),
      limit: parseInt(limit),
      candidates: paginated
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 2. Perform HR recruitment and selection matching
app.post('/api/hr/recruitment', async (req, res) => {
  try {
    const { targetRole, recruiterAgentId } = req.body;
    
    const candidates = readCandidates();
    const agents = readAgents();
    
    const recruiter = agents.find(a => a.id === recruiterAgentId) || {
      name: "Sofia Tech Recruiter",
      role: "Tech Recruiter Sênior",
      avatar: "🙋‍♀️"
    };
    
    // Filter candidates matching target role
    let matches = candidates.filter(c => 
      c.role.toLowerCase().includes(targetRole.toLowerCase()) || 
      c.category.toLowerCase().includes(targetRole.toLowerCase())
    );
    
    // If no direct matches, get random ones from the category
    if (matches.length === 0) {
      matches = candidates.slice(0, 100);
    }
    
    // Sort or filter some best options (e.g. limit to top 3)
    // We shuffle slightly to make recruitment dynamic, then select top 3
    const shuffled = matches.sort(() => 0.5 - Math.random());
    const top3 = shuffled.slice(0, 3);
    
    // Generate Recruiter's thoughts based on Gemma 4 instructions
    const resultLog = [];
    top3.forEach((cand, idx) => {
      let rating = 8.5 + (idx * 0.5) - (Math.random() * 0.5);
      if (rating > 10) rating = 10;
      
      const evaluation = `Candidato com excelente embasamento em ${cand.role}. ` +
        `Sua vantagem (${cand.advantage}) se alinha perfeitamente com a sprint atual. ` +
        `Como desvantagem (${cand.disadvantage}), recomendo acompanhar de perto no onboarding. ` +
        `Indicação de contratação forte.`;
        
      resultLog.push({
        candidate: cand,
        score: rating.toFixed(1),
        recruiterEvaluation: evaluation
      });
    });
    
    res.json({
      success: true,
      recruiter: {
        name: recruiter.name,
        role: recruiter.role,
        avatar: recruiter.avatar
      },
      targetRole,
      shortlist: resultLog
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 3. Hire Candidate & Sync to Jira
app.post('/api/hr/hire', async (req, res) => {
  try {
    const { candidateId } = req.body;
    const candidates = readCandidates();
    const candidate = candidates.find(c => c.id === candidateId);
    
    if (!candidate) {
      return res.status(404).json({ error: 'Candidato não encontrado no banco de 45k.' });
    }
    
    const currentAgents = readAgents();
    
    // Check if already hired
    if (currentAgents.some(a => a.id === candidate.id)) {
      return res.status(400).json({ error: 'Candidato já contratado no time.' });
    }
    
    // Adapt level and add to DB
    const newAgent = {
      id: candidate.id,
      name: candidate.name,
      role: candidate.role,
      level: "Analista SR", // enforce C-level, Directors, Managers, Coordinators, SR analysts constraint
      avatar: candidate.avatar,
      advantage: candidate.advantage,
      disadvantage: candidate.disadvantage,
      dilemma: candidate.dilemma,
      personality: candidate.personality,
      status: 'Disponível',
      schedule: '09:00 - 18:00',
      feedbacks: []
    };
    
    currentAgents.push(newAgent);
    saveAgents(currentAgents);
    
    // Sync onboarding to Jira
    let jiraKey = 'MOCK-ONBOARDING';
    try {
      const summary = `ONBOARDING: Novo colaborador contratado - ${candidate.name}`;
      const description = `Contratação efetuada via painel de RH.\n\n` +
        `Nome: ${candidate.name}\n` +
        `Cargo: ${candidate.role}\n` +
        `Vantagem: ${candidate.advantage}\n` +
        `Dilema: ${candidate.dilemma}`;
        
      const bodyData = {
        fields: {
          project: { key: 'KAN' },
          summary: summary,
          description: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: description,
                    type: 'text'
                  }
                ]
              }
            ]
          },
          issuetype: { name: 'Task' }
        }
      };
      
      const jiraResponse = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, {
        headers: getJiraAuthHeader()
      });
      jiraKey = jiraResponse.data?.key;
    } catch (err) {
      console.error('Jira onboarding sync failed:', err.message);
    }
    
    res.json({
      success: true,
      hiredAgent: newAgent,
      jiraKey
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Flose Startup Backend running on port ${PORT}`);
});
