const axios = require('axios');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

const credentials = `${JIRA_USER}:${JIRA_TOKEN}`;
const headers = {
  'Authorization': `Basic ${Buffer.from(credentials).toString('base64')}`,
  'Accept': 'application/json'
};

async function fastClear() {
  let done = false;
  while (!done) {
    try {
      console.log("Fetching up to 100 issues...");
      const searchResponse = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
        headers,
        params: { jql: 'project = KAN', maxResults: 100 }
      });
      const issues = searchResponse.data.issues || [];
      if (issues.length === 0) {
        console.log("No issues left! ZERADO!");
        done = true;
        break;
      }
      console.log(`Found ${issues.length} issues. Wiping concurrently...`);
      const promises = issues.map(issue => 
        axios.delete(`${JIRA_HOST}/rest/api/3/issue/${issue.id}`, { headers })
          .catch(e => {
            if (e.response && e.response.status !== 404) {
              console.error(`Failed to delete ${issue.key}:`, e.message);
            }
          })
      );
      await Promise.all(promises);
      console.log(`Wiped ${issues.length} issues.`);
    } catch (e) {
      console.error("Search failed:", e.message);
      await new Promise(r => setTimeout(r, 2000));
    }
  }
}

fastClear();
