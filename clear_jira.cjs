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
  'Accept': 'application/json'
};

async function clearJira() {
  try {
    console.log("Fetching issues from Jira...");
    const searchUrl = `${JIRA_HOST}/rest/api/3/search/jql`;
    const searchResponse = await axios.get(searchUrl, {
      headers,
      params: {
        jql: 'created != null',
        maxResults: 100
      }
    });
    const issues = searchResponse.data.issues || [];
    
    console.log(`Found ${issues.length} issues.`);
    if (issues.length === 0) {
      console.log("No issues to clear.");
      return;
    }

    for (const issue of issues) {
      console.log(`Deleting issue ${issue.key} (ID: ${issue.id})...`);
      const deleteUrl = `${JIRA_HOST}/rest/api/3/issue/${issue.id}`;
      try {
        await axios.delete(deleteUrl, { headers });
        console.log(`Deleted ${issue.key} successfully.`);
      } catch (err) {
        if (err.response && err.response.status === 404) {
          console.log(`Issue ${issue.key} already deleted or not found (404). Ignoring.`);
        } else {
          throw err;
        }
      }
    }
    
    console.log("This batch cleared successfully!");
  } catch (error) {
    console.error("Error clearing Jira issues:", error.message);
    if (error.response) {
      console.error(JSON.stringify(error.response.data, null, 2));
    }
  }
}

clearJira();
