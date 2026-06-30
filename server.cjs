const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

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

// Agency Profile Database
const AGENTS = [
  {
    id: 'ceo',
    name: 'Felipe Flose',
    role: 'CEO (Chief Executive Officer)',
    level: 'C-Level',
    avatar: '💼',
    advantage: 'Visão de mercado disruptiva e altíssima liderança motivacional.',
    disadvantage: 'Falta de paciência para processos longos; foca demais no curto prazo.',
    dilemma: 'Crescimento Acelerado (Burn Rate Alto) vs. Sustentabilidade Financeira.',
    personality: 'Focado em resultados de impacto, impaciente, carismático e estratégico.'
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
    personality: 'Pragmático, analítico, defensor ferrenho de código limpo e escalabilidade.'
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
    personality: 'Focada em eficiência, métricas claras, metódica e orientada a processos.'
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
    personality: 'Criativa, atenta a detalhes, emotiva e apaixonada por design de ponta.'
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
    personality: 'Empático, mediador, protetor e voltado à gestão de pessoas.'
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
    personality: 'Comunicativa, focada em dados, orientada a negócios e flexível.'
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
    personality: 'Energético, otimista, focado em agilidade e facilitador de conversas.'
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
    personality: 'Meticulosa, cética de promessas de desenvolvedores, e direta.'
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
    personality: 'Introvertido, focado na resolução prática de problemas, e focado em código.'
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
    personality: 'Detalhista, questionadora, focada na usabilidade e orientada a feedbacks.'
  }
];

// 1. Get List of Agents
app.get('/api/agents', (req, res) => {
  res.json(AGENTS);
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
    const jql = req.query.jql || 'order by created DESC';
    const response = await axios.get(`${JIRA_HOST}/rest/api/3/search`, {
      headers: getJiraAuthHeader(),
      params: { jql, maxResults: 50 }
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

// 6. Simulate Gemma 4 / Agent Debate & Update Jira
app.post('/api/simulate-debate', async (req, res) => {
  try {
    const { issueKey, issueSummary, issueDescription, selectedAgentIds } = req.body;
    
    const activeAgents = AGENTS.filter(a => selectedAgentIds.includes(a.id));
    if (activeAgents.length === 0) {
      return res.status(400).json({ error: 'Nenhum agente selecionado para o debate.' });
    }

    // Simulate Agent responses based on Gemma 4 instructions
    // Gemma 4 engine simulation structure:
    const logs = [];
    let debateSummary = `🤖 **Gemma 4 Startup Debate Engine**\n\nDiscussão de decisão para o Ticket: [${issueKey}] - ${issueSummary}\n\n`;

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

    // Write comment to Jira if issueKey is valid
    let jiraCommentResult = null;
    if (issueKey && issueKey !== 'MOCK-KEY') {
      try {
        await axios.post(
          `${JIRA_HOST}/rest/api/3/issue/${issueKey}/comment`,
          {
            body: {
              type: 'doc',
              version: 1,
              content: [
                {
                  type: 'paragraph',
                  content: [
                    {
                      text: `DEBATE DE AGENTES AUTOMATIZADOS (Gemma 4 Motor)\n\nDecisão: ${decision}\n\nResumo dos Dilemas:\n${activeAgents.map(a => `- ${a.name} (${a.role}): ${a.dilemma}`).join('\n')}`,
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

    res.json({
      success: true,
      logs: logs,
      decision: decision,
      summary: debateSummary,
      jiraCommentResult: jiraCommentResult
    });

  } catch (error) {
    console.error('Error simulating debate:', error.message);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Flose Startup Backend running on port ${PORT}`);
});
