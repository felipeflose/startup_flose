const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const newHires = [
  {
    "id": "spec_org_hugo",
    "name": "Hugo Organizador",
    "role": "Gestor de Estrutura Organizacional",
    "level": "Analista SR",
    "avatar": "📋",
    "advantage": "Excelente organizador de departamentos, fluxos de comunicação e divisões de times.",
    "disadvantage": "Tende a criar organogramas complexos que assustam equipes menores.",
    "dilemma": "Estrutura Rígida vs. Flexibilidade Funcional de Startup.",
    "personality": "Organizado, focado em metodologias de governança, comunicativo e analítico.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  },
  {
    "id": "spec_fac_enzo",
    "name": "Enzo Facilities",
    "role": "Engenheiro de Infraestrutura Física",
    "level": "Analista SR",
    "avatar": "🏗️",
    "advantage": "Otimiza layouts de escritório, ergonomia e alocação de estações de trabalho físicas.",
    "disadvantage": "Rígido com regras de layout e limpeza de mesas (clean desk policy).",
    "dilemma": "Layout Funcional Otimizado vs. Preferência Pessoal dos Colaboradores.",
    "personality": "Metódico, prático, perfeccionista com medições e focado em engenharia física.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "feedbacks": []
  }
];

function allocate() {
  if (!fs.existsSync(AGENTS_FILE)) {
    console.error("Agents DB not found.");
    return;
  }

  let agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));

  // 1. Add new hires if not present
  newHires.forEach(nh => {
    if (!agents.some(a => a.id === nh.id)) {
      agents.push(nh);
    }
  });

  // 2. Assign Area and Desk to all agents
  agents.forEach((agent, index) => {
    let area = "Engenharia";
    let desk = `Mesa ENG-${index + 1}`;

    if (agent.id === 'ceo' || agent.id === 'cto' || agent.id === 'dir_ops' || agent.id === 'dir_design') {
      area = "Diretoria & C-Suite";
      desk = `Sala Dirigente ${agent.id.toUpperCase()}`;
    } else if (agent.id === 'spec_po_pedro' || agent.id === 'mgr_prod' || agent.id === 'sr_ux' || agent.id === 'spec_tw_sofia' || agent.id.includes('game_designer')) {
      area = "Produto & Design";
      desk = `Mesa PROD-${index - 3}`;
    } else if (agent.id === 'mgr_eng' || agent.id === 'coord_scrum' || agent.id === 'coord_qa' || agent.id.includes('qa') || agent.id === 'spec_org_hugo') {
      area = "Qualidade, RH & Operações";
      desk = `Mesa QUAL-${index - 5}`;
    } else {
      area = "Engenharia & TI";
      desk = `Mesa ENG-${index - 7}`;
    }

    agent.area = area;
    agent.desk = desk;
  });

  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  console.log(`Allocated areas and desks for ${agents.length} agents.`);
}

allocate();
