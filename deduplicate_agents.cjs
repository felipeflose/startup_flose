const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

function deduplicate() {
  if (!fs.existsSync(AGENTS_FILE)) {
    console.log("No agents database found.");
    return;
  }

  const agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  console.log(`Original count: ${agents.length}`);

  const uniqueAgents = [];
  const seenIds = new Set();
  const seenNames = new Set();

  for (const agent of agents) {
    const id = agent.id.trim();
    const name = agent.name.trim();

    // Check if ID or Name is already added
    if (!seenIds.has(id) && !seenNames.has(name)) {
      seenIds.add(id);
      seenNames.add(name);
      uniqueAgents.push(agent);
    } else {
      console.log(`Removing duplicate agent: ${name} (ID: ${id})`);
    }
  }

  // Ensure all names and roles are fully distinct and styled nicely
  fs.writeFileSync(AGENTS_FILE, JSON.stringify(uniqueAgents, null, 2), 'utf8');
  console.log(`Deduplicated count: ${uniqueAgents.length}`);
}

deduplicate();
