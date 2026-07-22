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

async function resolveAllTodo() {
  console.log("Fetching all cards in 'A fazer'...");
  const headers = getJiraAuthHeader();
  
  try {
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: {
        jql: 'project = KAN AND status = "A fazer" order by created desc',
        maxResults: 100,
        fields: 'summary,status'
      }
    });
    
    const issues = searchRes.data?.issues || [];
    console.log(`Found ${issues.length} cards in "A fazer". Resolving them now...`);
    
    for (const issue of issues) {
      console.log(`Resolving stuck card: ${issue.key} - "${issue.fields.summary}"`);
      
      const transRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`, { headers });
      const transitions = transRes.data?.transitions || [];
      
      const inProgressTrans = transitions.find(t => {
        const normName = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        return normName.includes('andamento') || normName.includes('progress');
      });
      
      if (inProgressTrans) {
        await transitionIssue(issue.key, inProgressTrans.id);
        
        // Fetch transitions again to move it to Concluído
        const refetchRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`, { headers });
        const refetchedTrans = refetchRes.data?.transitions || [];
        const doneTrans = refetchedTrans.find(t => {
          const normName = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
          return normName.includes('concluid') || normName.includes('done');
        });
        
        if (doneTrans) {
          const success = await transitionIssue(issue.key, doneTrans.id);
          if (success) {
            console.log(`  Successfully moved ${issue.key} to Concluído!`);
          } else {
            console.log(`  Failed to transition ${issue.key} to Concluído.`);
          }
        }
      }
    }
    console.log("All 'A fazer' cards have been processed and resolved!");
  } catch (err) {
    console.error("Error during resolution:", err.message);
  }
}

resolveAllTodo();
