const axios = require('axios');
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

async function fixTransitions() {
  try {
    console.log("Searching for issues to fix transitions...");
    const searchUrl = `${JIRA_HOST}/rest/api/3/search/jql`;
    const searchResponse = await axios.get(searchUrl, {
      headers,
      params: {
        jql: 'status != Done AND status != Concluído',
        maxResults: 100
      }
    });

    const issues = searchResponse.data.issues || [];
    console.log(`Checking ${issues.length} active issues for missed transitions...`);

    for (const issue of issues) {
      // Fetch transitions
      const transUrl = `${JIRA_HOST}/rest/api/3/issue/${issue.id}/transitions`;
      const transResponse = await axios.get(transUrl, { headers });
      const transitions = transResponse.data.transitions || [];

      const doneTransition = transitions.find(t => 
        t.name.toLowerCase().includes('done') || 
        t.name.toLowerCase().includes('conclu') || 
        t.name.toLowerCase().includes('pronto')
      );

      if (doneTransition) {
        console.log(`Fixing KAN/issue ${issue.key}: transitioning to Concluído (Done)...`);
        await axios.post(transUrl, {
          transition: { id: doneTransition.id }
        }, { headers });
        console.log(`Successfully fixed transition for ${issue.key}.`);
      }
    }
    console.log("Missed transitions fixed successfully!");
  } catch (error) {
    console.error("Error fixing transitions:", error.message);
  }
}

fixTransitions();
