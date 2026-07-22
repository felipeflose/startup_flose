const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

function applyFeedback() {
  if (!fs.existsSync(AGENTS_FILE)) {
    console.error("Agents database not found.");
    return;
  }

  let agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));

  // 1. Give negative feedback to Product Managers / POs for creating cards without Epics
  const creators = ['mgr_prod', 'spec_po_pedro']; // Sarah Backlog and Pedro PO
  
  // 2. Give negative feedback to Developers / QAs for acting on issues without Epics
  const executors = ['sr_dev', 'sr_dev_mariana', 'sr_qa_juliana', 'sr_qa_roberto']; // David Dev, Mariana Python, Juliana QA, Roberto QA

  agents.forEach(agent => {
    if (!agent.feedbacks) {
      agent.feedbacks = [];
    }

    if (creators.includes(agent.id)) {
      agent.feedbacks.push({
        text: "Permitiu a criação de tarefas sem vinculação a um Épico no Jira (Falha de Governança).",
        rating: "negativo",
        date: new Date().toISOString()
      });
      console.log(`Negative feedback applied to creator: ${agent.name}`);
    }

    if (executors.includes(agent.id)) {
      agent.feedbacks.push({
        text: "Atuou na resolução de tarefa sem antes exigir a vinculação a um Épico no backlog.",
        rating: "negativo",
        date: new Date().toISOString()
      });
      console.log(`Negative feedback applied to executor: ${agent.name}`);
    }
  });

  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  console.log("Governance feedbacks applied successfully to agents database!");
}

applyFeedback();
