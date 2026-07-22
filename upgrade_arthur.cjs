const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const upgradedArthur = {
  "id": "auditor_arthur",
  "name": "Arthur Tech Lead & Auditor",
  "role": "Tech Lead & Auditor de Conformidade Sênior",
  "level": "Analista SR",
  "avatar": "⚖️",
  "advantage": "Auditoria técnica implacável e automatizada. Garantia absoluta de cobertura de testes, clean code e conformidade Jira.",
  "disadvantage": "Intolerância crônica a desvios (400% mais exigente que a média). Aplica penalizações severas e imediatas ao menor sinal de regressão de código ou processo.",
  "dilemma": "Governança e Qualidade Absoluta vs. Velocidade de Entrega Comercial.",
  "personality": "Crítico implacável, obsessivo por conformidade técnica, punitivo, metódico e intransigente com falhas.",
  "status": "Disponível",
  "schedule": "09:00 - 18:00",
  "area": "Qualidade, RH & Operações",
  "desk": "Mesa QUAL-11",
  "feedbacks": []
};

function upgradeArthur() {
  if (!fs.existsSync(AGENTS_FILE)) {
    console.error("Agents database not found.");
    return;
  }

  let agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  const arthurIndex = agents.findIndex(a => a.id === 'auditor_arthur');

  if (arthurIndex === -1) {
    console.log("Arthur Auditor not found in database. Creating him fresh...");
    agents.push(upgradedArthur);
  } else {
    agents[arthurIndex] = {
      ...agents[arthurIndex],
      ...upgradedArthur
    };
  }

  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  console.log("Arthur upgraded to Tech Lead & Auditor successfully!");
}

upgradeArthur();
