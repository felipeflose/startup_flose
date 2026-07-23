const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const newLeads = [
  {
    "id": "tech_lead_laura",
    "name": "Laura Tech Lead",
    "role": "Tech Lead de Engenharia & Qualidade",
    "level": "Analista SR",
    "avatar": "🎓",
    "advantage": "Audita Pull Requests, detecta bad smells de código e faz revisões arquiteturais rigorosas.",
    "disadvantage": "Muito severa com cobertura de testes unitários; aplica advertências imediatas por regressões.",
    "dilemma": "Manter Padrão Técnico Impecável vs. Flexibilizar Processos em Sprints Rápidas.",
    "personality": "Rigorosa, analítica, focada em qualidade estrita de código e direta.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Engenharia & TI",
    "desk": "Mesa ENG-10",
    "feedbacks": []
  },
  {
    "id": "qa_lead_marcos",
    "name": "Marcos QA Lead",
    "role": "QA Lead de Integração & Estabilidade",
    "level": "Analista SR",
    "avatar": "🛡️",
    "advantage": "Estrutura cenários de teste complexos, previne quebras em produção e audita bugs reportados.",
    "disadvantage": "Pode barrar releases críticas se encontrar inconsistências de ambiente ou de layout secundárias.",
    "dilemma": "Zero Bugs em Produção vs. Agilidade na Entrega Comercial.",
    "personality": "Crítico, metódico, focado na prevenção de falhas e rigoroso.",
    "status": "Disponível",
    "schedule": "09:00 - 18:00",
    "area": "Qualidade, RH & Operações",
    "desk": "Mesa QUAL-10",
    "feedbacks": []
  }
];

function sync() {
  if (!fs.existsSync(AGENTS_FILE)) {
    console.error("Agents DB not found.");
    return;
  }
  let db = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  newLeads.forEach(l => {
    if (!db.some(a => a.id === l.id)) {
      db.push(l);
      console.log(`Lead added: ${l.name}`);
    }
  });
  fs.writeFileSync(AGENTS_FILE, JSON.stringify(db, null, 2), 'utf8');
}

sync();
