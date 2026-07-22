const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const AGENTS_FILE = path.join(__dirname, 'agents_db.json');
const CANDIDATES_FILE = path.join(__dirname, 'profiles_bank.json');

const getJiraAuthHeader = () => {
  const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
  return {
    'Authorization': `Basic ${Buffer.from(credentials).toString('base64')}`,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
};

// Activity logger helper
function logActivity(agentId, name, avatar, text, jiraKey = '', jiraSummary = '') {
  const logFile = path.join(__dirname, 'activity_log.json');
  let logs = [];
  if (fs.existsSync(logFile)) {
    try { logs = JSON.parse(fs.readFileSync(logFile, 'utf8')); } catch (e) {}
  }
  logs.unshift({
    timestamp: new Date().toISOString(),
    agentId,
    name,
    avatar,
    text,
    jiraKey,
    jiraSummary
  });
  fs.writeFileSync(logFile, JSON.stringify(logs.slice(0, 100), null, 2), 'utf8');
}

async function auditAndFireAll() {
  console.log("Checking for tasks created without Epics...");
  const headers = getJiraAuthHeader();
  
  if (!fs.existsSync(AGENTS_FILE)) {
    console.error("Agents database not found.");
    return;
  }
  let agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  
  if (!fs.existsSync(CANDIDATES_FILE)) {
    console.error("Candidates bank not found.");
    return;
  }
  const candidates = JSON.parse(fs.readFileSync(CANDIDATES_FILE, 'utf8'));

  try {
    // Search issues with no parent (no Epic)
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: {
        jql: 'project = KAN AND parent = null AND issuetype != Epic',
        maxResults: 100,
        fields: 'summary,status'
      }
    });
    
    const issues = searchRes.data?.issues || [];
    console.log(`Found ${issues.length} issues without Epic.`);
    
    if (issues.length === 0) {
      console.log("No issues found without Epic. All clean.");
      return;
    }

    // Targets: product creators and developers acting on them
    const targetsToFire = ['mgr_prod', 'spec_po_pedro', 'sr_dev', 'sr_dev_mariana', 'sr_qa_juliana', 'sr_qa_roberto'];
    let firedCount = 0;

    for (let i = 0; i < agents.length; i++) {
      const agent = agents[i];
      if (agent.fired) continue;
      
      if (targetsToFire.includes(agent.id)) {
        console.log(`[GOVERNANÇA AUDITORIA] Demitindo imediatamente: ${agent.name} (${agent.role}) por falha grave de Épicos.`);
        agent.fired = true;
        agent.status = 'Desligado';
        firedCount++;
        
        const fireMsg = `💼 Felipe Flose (CEO) demitiu sumariamente ${agent.name} (${agent.role}) por infração gravíssima de governança (Tarefas sem Épico identificadas).`;
        logActivity('ceo', 'Felipe Flose', '💼', fireMsg, '', '');

        // Find candidate replacement
        const matchedCandidates = candidates.filter(c => 
          c.role.toLowerCase() === agent.role.toLowerCase() && 
          !agents.some(a => a.id === c.id)
        );
        const replacement = matchedCandidates[0] || candidates.find(c => c.role.toLowerCase().includes('sênior') && !agents.some(a => a.id === c.id));
        
        if (replacement) {
          const newAgent = {
            id: replacement.id,
            name: replacement.name,
            role: replacement.role,
            level: "Analista SR",
            avatar: replacement.avatar,
            advantage: replacement.advantage,
            disadvantage: replacement.disadvantage,
            dilemma: replacement.dilemma,
            personality: replacement.personality,
            status: 'Disponível',
            schedule: '09:00 - 18:00',
            area: agent.area || "Engenharia & TI",
            desk: agent.desk || "Mesa",
            feedbacks: []
          };
          agents.push(newAgent);
          console.log(`[GOVERNANÇA] Contratando substituto: ${newAgent.name} (${newAgent.role}) para a ${newAgent.desk}`);
          
          const hireMsg = `🤝 Novo colaborador sênior contratado: ${newAgent.name} (${newAgent.role}) para assumir as responsabilidades na ${newAgent.desk} sob rígida conformidade.`;
          logActivity('ceo', 'Felipe Flose', '💼', hireMsg, '', '');
        }
      }
    }

    fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
    console.log(`Audited! Demitidos: ${firedCount} colaboradores. Novos contratados foram alocados.`);

    // Automatically link epics to clean the board
    console.log("Cleaning board linking Épicos to orphan tasks...");
    const epicMap = {};
    const epicSearch = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: { jql: 'project = KAN AND issuetype = Epic', maxResults: 50, fields: 'summary' }
    });
    (epicSearch.data?.issues || []).forEach(issue => {
      epicMap[issue.fields.summary] = issue.key;
    });

    for (const issue of issues) {
      const summaryText = (issue.fields.summary || '').toLowerCase();
      let targetEpic = 'Infraestrutura & Tecnologia';
      if (summaryText.includes('contrat') || summaryText.includes('colaborador') || summaryText.includes('demiss') || summaryText.includes('rh')) {
        targetEpic = 'Gestão de Pessoas';
      } else if (summaryText.includes('sap') || summaryText.includes('faturam') || summaryText.includes('invoice') || summaryText.includes('financ')) {
        targetEpic = 'Faturamento & Finanças';
      } else if (summaryText.includes('jogo') || summaryText.includes('game') || summaryText.includes('velha')) {
        targetEpic = 'Entretenimento & Games';
      }
      const epicKey = epicMap[targetEpic];
      if (epicKey) {
        await axios.put(`${JIRA_HOST}/rest/api/3/issue/${issue.key}`, {
          fields: { parent: { key: epicKey } }
        }, { headers });
      }
    }
    console.log("All orphan issues linked to Epics successfully.");

  } catch (err) {
    console.error("Auditor error:", err.message);
  }
}

auditAndFireAll();
