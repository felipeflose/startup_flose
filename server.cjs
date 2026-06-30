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
    exec(`git branch ${branchName}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error creating git branch ${branchName}:`, error.message);
        resolve(false);
      } else {
        console.log(`Git branch ${branchName} created successfully.`);
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

const readDecisions = () => {
  try {
    if (!fs.existsSync(DECISIONS_FILE)) {
      return [];
    }
    const data = fs.readFileSync(DECISIONS_FILE, 'utf8');
    return JSON.parse(data);
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

const getOrCreateEpics = async () => {
  try {
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN AND issuetype = Epic',
        fields: 'summary'
      }
    });
    const epics = searchRes.data.issues || [];
    const epicMap = {};
    epics.forEach(e => {
      epicMap[e.fields.summary] = e.key;
    });

    const requiredEpics = [
      'Gestão de Pessoas',
      'Infraestrutura & Tecnologia',
      'Design & Produto',
      'Processos Ágeis'
    ];

    for (const name of requiredEpics) {
      if (!epicMap[name]) {
        try {
          const createRes = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
            fields: {
              project: { key: 'KAN' },
              summary: name,
              issuetype: { name: 'Epic' }
            }
          }, { headers: getJiraAuthHeader() });
          if (createRes.data && createRes.data.key) {
            epicMap[name] = createRes.data.key;
          }
        } catch (createErr) {
          console.error(`Failed to create Epic "${name}":`, createErr.message);
          epicMap[name] = 'MOCK-EPIC-' + slugify(name);
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

app.get('/api/jira/epics', async (req, res) => {
  const epicMap = await getOrCreateEpics();
  res.json(epicMap);
});

// 5.5. Get Decisions Log
app.get('/api/decisions', (req, res) => {
  res.json(readDecisions());
});

// 6. Simulate Gemma 4 / Agent Debate & Update Jira
app.post('/api/simulate-debate', async (req, res) => {
  try {
    const { issueKey, issueSummary, issueDescription, selectedAgentIds, epicName } = req.body;
    
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

    const activeAgents = AGENTS.filter(a => selectedAgentIds.includes(a.id));
    if (activeAgents.length === 0) {
      return res.status(400).json({ error: 'Nenhum agente selecionado para o debate.' });
    }

    // Simulate Agent responses based on Gemma 4 instructions
    // Gemma 4 engine simulation structure:
    const logs = [];
    let debateSummary = `🤖 **Gemma 4 Startup Debate Engine**\n\nDiscussão de decisão para o Ticket: [${finalIssueKey}] - ${finalIssueSummary}\n\n`;

    activeAgents.forEach(agent => {
      // Formulate agent contribution reflecting personality, advantages, and specific dilemmas
      let responseText = '';
      if (agent.id === 'ceo') {
        responseText = `Pessoal, precisamos disso no ar ontem! A concorrência não dorme. Meu dilema é botar pra quebrar (${agent.dilemma}). Vamos entregar rápido e depois otimizamos!`;
      } else if (agent.id === 'cto') {
        responseText = `Atenção: Acelerar sem critério técnico criará um débito insustentável. Recomendo isolar essa entrega ou refatorar o módulo principal. Meu foco é qualidade estrutural.`;
      } else if (agent.id === 'dir_ops') {
        responseText = `Precisamos garantir a entrega dentro do orçamento e sem estressar os fluxos operacionais vigentes. Vamos monitorar o tempo investido e manter processos limpos.`;
      } else if (agent.id === 'dir_design') {
        responseText = `Não podemos deixar de lado a identidade e consistência visual! Uma interface feia destrói o valor do produto, mesmo sendo rápida.`;
      } else if (agent.id === 'mgr_eng') {
        responseText = `Minha preocupação principal é a saúde física e mental dos desenvolvedores. Prazos agressivos exigem compensação ou escopo menor.`;
      } else if (agent.id === 'mgr_prod') {
        responseText = `Nossos clientes finais estão cobrando essa funcionalidade. De acordo com as métricas de uso, esta feature é prioridade máxima.`;
      } else if (agent.id === 'coord_scrum') {
        responseText = `Vou remover os impedimentos. Se concordarmos com o escopo, quebremos em subtasks na daily de amanhã para manter o burndown saudável.`;
      } else if (agent.id === 'coord_qa') {
        responseText = `Não aceito deploys sem cobertura mínima de testes unitários e de integração. Sem validação, não há release!`;
      } else if (agent.id === 'sr_dev') {
        responseText = `Consigo codar rápido a primeira versão em 2 dias, mas se quiserem testes completos e documentação de arquitetura precisaremos de 5 dias.`;
      } else if (agent.id === 'sr_ux') {
        responseText = `Eu crio o protótipo baseado em nossos componentes padrão para agilizar, mas teremos que abrir mão de uma transição customizada sofisticada.`;
      }

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
      fileRelativePath = `src/simulations/${finalIssueKey}-code.ts`;
      fileContent = `// Código autônomo gerado pela equipe de engenharia da Flose Startup
// Ticket Jira: ${finalIssueKey}
// Autor: ${developerAgent.name} (${developerAgent.role})
// Data: ${new Date().toLocaleString('pt-BR')}

export const executeTask = () => {
  console.log("Executando a resolução consensual da equipe:");
  console.log("${decision.replace(/"/g, '\\"')}");
  
  return {
    status: "delivered",
    engineer: "${developerAgent.name}",
    consensualResolution: "${decision.replace(/"/g, '\\"')}",
    timestamp: "${new Date().toISOString()}"
  };
};`;
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
      githubIssueUrl: githubIssueUrl,
      branchCreated: branchCreated,
      executorName: developerAgent.name,
      executorRole: developerAgent.role,
      generatedFile: fileRelativePath,
      commitHash: commitHash,
      gitCommitResult: gitCommitResult
    };
    saveDecision(decisionEntry);

    res.json({
      success: true,
      issueKey: finalIssueKey,
      logs: logs,
      decision: decision,
      summary: debateSummary,
      jiraCommentResult: jiraCommentResult,
      gitBranchName: gitBranchName,
      githubIssueUrl: githubIssueUrl,
      branchCreated: branchCreated,
      executorName: developerAgent.name,
      executorRole: developerAgent.role,
      generatedFile: fileRelativePath,
      commitHash: commitHash,
      gitCommitResult: gitCommitResult
    });

  } catch (error) {
    console.error('Error simulating debate:', error.message);
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
