const axios = require('axios');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

const getJiraAuthHeader = () => {
  const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
  return {
    'Authorization': `Basic ${Buffer.from(credentials).toString('base64')}`,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
};

const EPIC_NAMES = [
  'Gestão de Pessoas',
  'Infraestrutura & Tecnologia',
  'Faturamento & Finanças',
  'Entretenimento & Games',
  'Melhorias Internas'
];

async function getOrCreateEpics() {
  const headers = getJiraAuthHeader();
  const epicMap = {};
  
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: {
        jql: 'project = KAN AND issuetype = Epic',
        maxResults: 50,
        fields: 'summary'
      }
    });
    
    const existing = res.data?.issues || [];
    existing.forEach(issue => {
      epicMap[issue.fields.summary] = issue.key;
    });
  } catch (err) {
    console.error('Error fetching epics:', err.message);
  }

  for (const name of EPIC_NAMES) {
    if (!epicMap[name]) {
      try {
        const bodyData = {
          fields: {
            project: { key: 'KAN' },
            summary: name,
            issuetype: { name: 'Epic' }
          }
        };
        const createRes = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, bodyData, { headers });
        epicMap[name] = createRes.data.key;
        console.log(`Created Epic: "${name}" -> ${createRes.data.key}`);
      } catch (err) {
        console.error(`Failed to create Epic "${name}":`, err.message);
      }
    }
  }

  return epicMap;
}

async function organizeBoard() {
  console.log("Analyzing board issues to categorize and link Epics...");
  const headers = getJiraAuthHeader();
  const epics = await getOrCreateEpics();
  
  try {
    // Fetch issues in "A fazer" (To Do) or missing parent link
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: {
        jql: 'project = KAN AND parent = null AND issuetype != Epic',
        maxResults: 100,
        fields: 'summary,description,status'
      }
    });
    
    const issues = searchRes.data?.issues || [];
    console.log(`Found ${issues.length} issues without a linked Epic (parent).`);
    
    for (const issue of issues) {
      const summary = (issue.fields.summary || '').toLowerCase();
      let targetEpic = 'Infraestrutura & Tecnologia';
      
      if (summary.includes('contrat') || summary.includes('colaborador') || summary.includes('demiss') || summary.includes('rh') || summary.includes('gestao de pessoas')) {
        targetEpic = 'Gestão de Pessoas';
      } else if (summary.includes('sap') || summary.includes('faturam') || summary.includes('invoice') || summary.includes('financ') || summary.includes('custo')) {
        targetEpic = 'Faturamento & Finanças';
      } else if (summary.includes('jogo') || summary.includes('game') || summary.includes('velha') || summary.includes('gta') || summary.includes('cobeinha')) {
        targetEpic = 'Entretenimento & Games';
      } else if (summary.includes('melhoria') || summary.includes('refator') || summary.includes('boundary') || summary.includes('rate limit') || summary.includes('cache')) {
        targetEpic = 'Melhorias Internas';
      }
      
      const epicKey = epics[targetEpic];
      if (epicKey) {
        try {
          await axios.put(`${JIRA_HOST}/rest/api/3/issue/${issue.key}`, {
            fields: {
              parent: { key: epicKey }
            }
          }, { headers });
          console.log(`Linked Issue ${issue.key} ("${issue.fields.summary}") -> Epic: "${targetEpic}" (${epicKey})`);
        } catch (err) {
          console.error(`Failed to link issue ${issue.key} to epic ${epicKey}:`, err.message);
        }
      }
    }
    
    console.log("Epic synchronization completed successfully!");
  } catch (err) {
    console.error("Error organizing board:", err.message);
  }
}

organizeBoard();
