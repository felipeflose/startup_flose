// emergency_restore.cjs — Fase 0: Ressuscitar empresa
const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const agentsFile = path.join(__dirname, 'agents_db.json');
const configFile = path.join(__dirname, 'company_config.json');

async function main() {
  const agents = JSON.parse(fs.readFileSync(agentsFile, 'utf8'));

  // 1. Reativar CEO e Diretores demitidos
  const restored = [];
  agents.forEach(a => {
    const role = (a.role || '').toLowerCase();
    const isCLevel = role.includes('dono') || role.includes('ceo') || role.includes('chief') || role.includes('diretor') || role.includes('director') || role.includes('vp ');
    if (a.fired && isCLevel) {
      a.fired = false;
      a.firedReason = null;
      a.status = 'Disponível';
      a.totalScore = 80;
      a.feedbacks = (a.feedbacks || []).filter(f => f.type !== 'warning' && f.type !== 'fire');
      a.pip = { active: false, warnings: 0, maxWarnings: 3, reason: null };
      restored.push(a.name);
    }
  });

  // 2. Garantir que o CEO (Felipe) nunca pode ser demitido novamente
  const ceo = agents.find(a =>
    (a.role || '').toLowerCase().includes('dono') ||
    (a.name || '').toLowerCase().includes('felipe viana')
  );
  if (ceo) {
    ceo.fired = false;
    ceo.protected = true; // flag: nunca pode ser demitido
    ceo.status = 'Disponível';
    ceo.totalScore = 100;
    if (!restored.includes(ceo.name)) restored.push(ceo.name + ' (CEO protegido)');
  }

  fs.writeFileSync(agentsFile, JSON.stringify(agents, null, 2), 'utf8');

  console.log('\n✅ EMPRESA RESTAURADA!');
  console.log('Agentes reativados:', restored);
  console.log('Total ativos:', agents.filter(a => !a.fired).length);

  // 3. Notificar via API (se server estiver rodando)
  try {
    for (const name of restored) {
      await axios.post('http://localhost:5001/api/activity', {
        agentId: ceo?.id || 'system',
        agentName: '⚡ Sistema',
        agentAvatar: '⚡',
        action: `Restauração de emergência: ${name} reativado(a) e pronto(a) para trabalhar.`,
        ticketKey: '',
        ticketSummary: ''
      }).catch(() => {});
    }
  } catch (e) { /* server pode não estar up */ }
}

main().catch(console.error);
