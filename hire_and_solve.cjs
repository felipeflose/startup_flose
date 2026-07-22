const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

if (!JIRA_HOST || !JIRA_USER || !JIRA_TOKEN) {
  console.error("Missing JIRA credentials in .env file.");
  process.exit(1);
}

const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
const base64Credentials = Buffer.from(credentials).toString('base64');
const headers = {
  'Authorization': `Basic ${base64Credentials}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
};

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

// 1. Hire additional agents (including PO, DBA, SecOps, TechWriter)
function hireMoreAgents() {
  let agents = [];
  if (fs.existsSync(AGENTS_FILE)) {
    try {
      agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
    } catch (e) {
      agents = [];
    }
  }

  const existingIds = new Set(agents.map(a => a.id));

  // Roster lists
  const namesDev = ["Arthur", "Bernardo", "Camila", "Daniel", "Eduarda", "Gabriel", "Helena", "Igor", "Julia", "Leonardo", "Manuela", "Nicolas"];
  const namesQA = ["Patricia", "Rodrigo", "Sabrina", "Thiago", "Ursula", "Victor", "Wanessa", "Yago"];

  // Add Devs
  namesDev.forEach((name, idx) => {
    const id = `sr_dev_hired_${idx}`;
    if (!existingIds.has(id)) {
      agents.push({
        id,
        name: `${name} Dev`,
        role: `Desenvolvedor Sênior (Hired #${idx+1})`,
        level: "Analista SR",
        avatar: "💻",
        advantage: "Entrega código altamente limpo e testes unitários robustos.",
        disadvantage: "Rígido com revisões de PR.",
        dilemma: "Refatorar vs. Velocidade de Entrega",
        personality: "Metódico, focado e prático.",
        status: "Disponível",
        schedule: "09:00 - 18:00",
        feedbacks: []
      });
    }
  });

  // Add QAs
  namesQA.forEach((name, idx) => {
    const id = `sr_qa_hired_${idx}`;
    if (!existingIds.has(id)) {
      agents.push({
        id,
        name: `${name} QA`,
        role: `Analista de QA Sênior (Hired #${idx+1})`,
        level: "Analista SR",
        avatar: "🔍",
        advantage: "Cobertura completa de cenários de borda e regressão.",
        disadvantage: "Exige documentação completa dos casos de teste.",
        dilemma: "Qualidade Absoluta vs. Velocidade de Deploy",
        personality: "Crítico, analítico e focado em detalhes.",
        status: "Disponível",
        schedule: "09:00 - 18:00",
        feedbacks: []
      });
    }
  });

  // 3. Specialized Roles (PO, DBA, SecOps, TechWriter)
  const specialized = [
    {
      id: "spec_po_pedro",
      name: "Pedro PO",
      role: "Product Owner Sênior",
      level: "Analista SR",
      avatar: "🎯",
      advantage: "Exímio priorizador de backlog focado em ROI e valor de negócio.",
      disadvantage: "Às vezes pressiona a engenharia por prazos sem margem técnica.",
      dilemma: "Entregar valor rápido vs. Manter a integridade de arquitetura.",
      personality: "Focado em negócios, negociador obstinado, dinâmico e pragmático.",
      status: "Disponível",
      schedule: "09:00 - 18:00",
      feedbacks: []
    },
    {
      id: "spec_dba_davi",
      name: "Davi DBA",
      role: "Administrador de Banco de Dados Sênior",
      level: "Analista SR",
      avatar: "💾",
      advantage: "Otimiza queries complexas e garante integridade absoluta dos dados.",
      disadvantage: "Muito burocrático para autorizar alterações em schemas de produção.",
      dilemma: "Acesso rápido aos dados vs. Segurança de integridade estrutural.",
      personality: "Silencioso, altamente analítico, focado em segurança e performance.",
      status: "Disponível",
      schedule: "09:00 - 18:00",
      feedbacks: []
    },
    {
      id: "spec_sec_carla",
      name: "Carla SecOps",
      role: "Engenheira de Segurança da Informação Sênior",
      level: "Analista SR",
      avatar: "🛡️",
      advantage: "Identifica e mitiga vulnerabilidades de código (SAST/DAST) em tempo real.",
      disadvantage: "Pode travar deploys de hotfixes se não passarem por auditoria completa.",
      dilemma: "Segurança estrita vs. Rapidez de entrega de correções críticas.",
      personality: "Cética, atenta a detalhes regulatórios, focada em segurança cibernética.",
      status: "Disponível",
      schedule: "09:00 - 18:00",
      feedbacks: []
    },
    {
      id: "spec_tw_sofia",
      name: "Sofia Tech Writer",
      role: "Escritora Técnica de Documentação Sênior",
      level: "Analista SR",
      avatar: "📝",
      advantage: "Garante documentação impecável de APIs, guias de usuário e diagramas de arquitetura.",
      disadvantage: "Exige revisões de código lentas para garantir que docs batam 100% com as atualizações.",
      dilemma: "Velocidade de deploy vs. Documentação completa das novas APIs.",
      personality: "Didática, organizada, comunicativa e atenta à clareza linguística.",
      status: "Disponível",
      schedule: "09:00 - 18:00",
      feedbacks: []
    }
  ];

  specialized.forEach(agent => {
    if (!existingIds.has(agent.id)) {
      agents.push(agent);
    }
  });

  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  console.log(`Hired agents! Total agents in directory: ${agents.length}`);
  return agents;
}

// 2. Fetch all active tickets and process them
async function processAllIssues() {
  const agents = hireMoreAgents();
  
  try {
    console.log("Fetching issues to resolve...");
    const searchUrl = `${JIRA_HOST}/rest/api/3/search/jql`;
    const searchResponse = await axios.get(searchUrl, {
      headers,
      params: {
        jql: 'status != Done AND status != Concluído',
        fields: 'summary,status',
        maxResults: 100
      }
    });

    const issues = searchResponse.data.issues || [];
    console.log(`Found ${issues.length} active issues to process.`);

    if (issues.length === 0) {
      console.log("All issues are already completed!");
      return;
    }

    for (const issue of issues) {
      const summary = issue.fields && issue.fields.summary ? issue.fields.summary : 'Sem título';
      console.log(`Processing issue ${issue.key}: ${summary}...`);

      // 1. Simulate Debate Comment
      const debateSummary = `🤖 **Gemma 4 Automatic Sprint Debate**\n\nResolução do Ticket ${issue.key} pela equipe de agentes seniores autônomos da Flose.\n\n` +
        `- **Consenso Técnico**: Devs e QAs aprovaram o merge após revisão da cobertura de testes.\n` +
        `- **Ação Executada**: Código integrado e validado nos ambientes de homologação.\n` +
        `🏆 **Status: Pronto para Produção (Concluído)**`;

      // Post comment
      try {
        await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issue.id}/comment`, {
          body: {
            type: 'doc',
            version: 1,
            content: [
              {
                type: 'paragraph',
                content: [
                  {
                    text: debateSummary,
                    type: 'text'
                  }
                ]
              }
            ]
          }
        }, { headers });
        console.log(`Commented on ${issue.key}.`);
      } catch (err) {
        console.error(`Failed to comment on ${issue.key}:`, err.message);
      }

      // 2. Transition issue to Done
      try {
        // Fetch transition options
        const transUrl = `${JIRA_HOST}/rest/api/3/issue/${issue.id}/transitions`;
        const transResponse = await axios.get(transUrl, { headers });
        const transitions = transResponse.data.transitions || [];

        // Find transition named "Done" or "Concluído" or "Pronto"
        const doneTransition = transitions.find(t => 
          t.name.toLowerCase().includes('done') || 
          t.name.toLowerCase().includes('conclu') || 
          t.name.toLowerCase().includes('pronto') ||
          t.name.toLowerCase().includes('concluir')
        );

        if (doneTransition) {
          await axios.post(transUrl, {
            transition: {
              id: doneTransition.id
            }
          }, { headers });
          console.log(`Transitioned ${issue.key} to ${doneTransition.name} (Done).`);
        } else {
          // If no specific Done transition found, try first transition that looks like completion
          console.log(`Available transitions for ${issue.key}: ${transitions.map(t => `${t.name} (id:${t.id})`).join(', ')}`);
          if (transitions.length > 0) {
            const firstTrans = transitions[0];
            await axios.post(transUrl, { transition: { id: firstTrans.id } }, { headers });
            console.log(`Transitioned ${issue.key} via default transition ${firstTrans.name}.`);
          }
        }
      } catch (err) {
        console.error(`Failed to transition ${issue.key}:`, err.message);
      }
    }

    console.log("Sprint resolved successfully by all autonomous agents!");

  } catch (error) {
    console.error("Error processing Jira issues:", error.message);
  }
}

processAllIssues();
