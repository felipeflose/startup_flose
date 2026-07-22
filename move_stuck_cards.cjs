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
    console.log(`  Moved ${issueKey} to Concluído!`);
    return true;
  } catch (err) {
    console.error(`  Failed transition for ${issueKey} with ID ${transitionId}:`, err.message);
    return false;
  }
}

async function resolveStuckCards() {
  console.log("Searching for cards in 'Em andamento' status to transition to Concluído...");
  const headers = getJiraAuthHeader();
  
  try {
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers,
      params: {
        jql: 'project = KAN AND status = "Em andamento" order by created desc',
        maxResults: 50,
        fields: 'summary,status'
      }
    });
    
    const issues = searchRes.data?.issues || [];
    console.log(`Found ${issues.length} cards in "Em andamento".`);
    
    for (const issue of issues) {
      const transRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`, { headers });
      const transitions = transRes.data?.transitions || [];
      
      const doneTrans = transitions.find(t => {
        const normName = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        return normName.includes('concluid') || normName.includes('done');
      });
      
      if (doneTrans) {
        await transitionIssue(issue.key, doneTrans.id);
      } else {
        console.log(`  No "Concluído" transition found for ${issue.key}. Available: ${transitions.map(t => t.name).join(', ')}`);
      }
    }
    
    console.log("Resolution finished!");
  } catch (err) {
    console.error("Error during resolution:", err.message);
  }
}

resolveStuckCards();
