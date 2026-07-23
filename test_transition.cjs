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

async function test() {
  try {
    const searchRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN AND status != Concluído order by created desc',
        maxResults: 5,
        fields: 'summary,status'
      }
    });
    
    const issues = searchRes.data?.issues || [];
    if (issues.length === 0) {
      console.log("No open issues found to test transition.");
      return;
    }
    
    const issue = issues[0];
    console.log(`Selected Issue: ${issue.key} - Status: ${issue.fields?.status?.name}`);
    
    // Fetch transitions
    const transRes = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`, {
      headers: getJiraAuthHeader()
    });
    
    const transitions = transRes.data?.transitions || [];
    console.log("Available transitions:");
    transitions.forEach(t => {
      console.log(`- ID: ${t.id} | Name: "${t.name}" | Target Status: "${t.to?.name}"`);
    });

    // Test transition to Concluído (Done)
    const targetStatusName = 'Done';
    const normTarget = targetStatusName.toLowerCase();
    
    const match = transitions.find(t => {
      const name = (t.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const toName = (t.to?.name || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      
      if (normTarget === 'done' || normTarget === 'concluido' || normTarget === 'fechado') {
        return name.includes('done') || name.includes('concluid') || name.includes('concluir') || name.includes('fechad') || name.includes('fechar') || name.includes('resolv') || name.includes('pronto') || name.includes('ready') || name.includes('finish') || name.includes('finaliz') ||
               toName.includes('done') || toName.includes('concluid') || toName.includes('fechad') || toName.includes('resolv') || toName.includes('pronto') || toName.includes('finaliz');
      }
      return name.includes(normTarget) || toName.includes(normTarget);
    });

    if (match) {
      console.log(`Transitioning ${issue.key} to "${targetStatusName}" using Transition ID: ${match.id} ("${match.name}")`);
      const transitionRes = await axios.post(
        `${JIRA_HOST}/rest/api/3/issue/${issue.key}/transitions`,
        { transition: { id: match.id } },
        { headers: getJiraAuthHeader() }
      );
      console.log(`Successfully transitioned! Response Status:`, transitionRes.status);
    } else {
      console.log("No matching transition found.");
    }
  } catch (err) {
    console.error("Error during test:", err.response ? err.response.data : err.message);
  }
}

test();
