const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const getJiraAuthHeader = () => {
  const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
  return {
    'Authorization': `Basic ${Buffer.from(credentials).toString('base64')}`,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
};

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

async function transitionIssue(issueKey, transitionId) {
  try {
    await axios.post(
      `${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`,
      { transition: { id: transitionId } },
      { headers: getJiraAuthHeader() }
    );
    return true;
  } catch (err) {
    return false;
  }
}

async function executeGovernanceCleanup() {
  console.log("Promoting Arthur to Director of Governance...");
  
  if (fs.existsSync(AGENTS_FILE)) {
    let agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
    const arthurIndex = agents.findIndex(a => a.id === 'auditor_arthur');
    if (arthurIndex !== -1) {
      agents[arthurIndex] = {
        ...agents[arthurIndex],
        name: "Arthur de Flose",
        role: "Diretor de Governança & Conformidade C-Level",
        level: "C-Level",
        avatar: "👑⚖️",
        advantage: "Auditoria técnica implacável, poder absoluto de demissão e de moderação de processos corporativos.",
        personality: "Implacável, líder supremo de processos, perfeccionista e punitivo."
      };
      fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
      console.log("Arthur promoted successfully in agents_db.json!");
    }
  }

  console.log("Starting targeted JQL Epic orphan cleanup...");
  const headers = getJiraAuthHeader();

  try {
    // 1. Get Epics map
    const epicMap = {};
    const epicSearch = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: { jql: 'project = KAN AND issuetype = Epic', maxResults: 100, fields: 'summary' }
    });
    (epicSearch.data?.issues || []).forEach(issue => {
      epicMap[issue.fields.summary] = issue.key;
    });

    let loop = true;
    let totalCleaned = 0;

    while (loop) {
      console.log("Fetching next batch of orphan issues (parent = null)...");
      const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
        headers,
        params: {
          jql: 'project = KAN AND parent = null AND issuetype != Epic',
          maxResults: 100,
          fields: 'summary,status'
        }
      });

      const orphans = searchRes.data?.issues || [];
      if (orphans.length === 0) {
        console.log("No more orphan issues found!");
        break;
      }

      console.log(`Cleaning batch of ${orphans.length} orphan issues...`);
      for (const issue of orphans) {
        const summaryText = (issue.fields.summary || '').toLowerCase();
        let statusName = issue.fields.status?.name;
        
        let targetEpic = 'Infraestrutura & Tecnologia';
        if (summaryText.includes('contrat') || summaryText.includes('colaborador') || summaryText.includes('demiss') || summaryText.includes('rh') || summaryText.includes('onboarding')) {
          targetEpic = 'Gestão de Pessoas';
        } else if (summaryText.includes('sap') || summaryText.includes('faturam') || summaryText.includes('invoice') || summaryText.includes('financ')) {
          targetEpic = 'Faturamento & Finanças';
        } else if (summaryText.includes('jogo') || summaryText.includes('game') || summaryText.includes('velha')) {
          targetEpic = 'Entretenimento & Games';
        } else if (summaryText.includes('melhoria') || summaryText.includes('refator') || summaryText.includes('cache') || summaryText.includes('boundary') || summaryText.includes('rate limit')) {
          targetEpic = 'Melhorias Internas';
        }
        
        const epicKey = epicMap[targetEpic];
        if (epicKey) {
          console.log(`  Linking orphan ${issue.key} to Epic: ${targetEpic} (${epicKey})`);
          try {
            await axios.put(`${JIRA_HOST}/rest/api/3/issue/${issue.key}`, {
              fields: { parent: { key: epicKey } }
            }, { headers });
            totalCleaned++;
          } catch (e) {
            console.error(`  Failed to link ${issue.key}:`, e.message);
          }
        }

        // Also ensure status starts in "A fazer" if stuck in others (excluding resolved/done ones)
        if (statusName !== 'A fazer' && statusName !== 'To Do' && statusName !== 'Concluído' && statusName !== 'Done') {
          console.log(`  Resetting status of ${issue.key} to "A fazer" (Current: "${statusName}")`);
          try {
            const transRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`, { headers });
            const transitions = transRes.data?.transitions || [];
            const todoTrans = transitions.find(t => {
              const name = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
              return name.includes('fazer') || name.includes('todo');
            });

            if (todoTrans) {
              await transitionIssue(issue.key, todoTrans.id);
            }
          } catch (e) {
            console.error(`  Failed to reset status for ${issue.key}:`, e.message);
          }
        }
      }

      // Safeguard to prevent infinite loops if something fails to update
      if (totalCleaned > 5000) {
        console.warn("Safety limit reached. Stopping loop.");
        break;
      }
    }

    console.log(`Governance cleanup complete! Cleaned total of ${totalCleaned} orphan cards.`);
  } catch (err) {
    console.error("Cleanup failed:", err.message);
  }
}

executeGovernanceCleanup();
