/**
 * hierarchical_recruitment_director.cjs
 * 
 * DIRETOR DE PEOPLE & TALENT — Motor de Recrutamento Hierárquico via Gemma 4
 * 
 * Hierarquia de contratação:
 * Felipe Viana Flose (DONO)
 *   └─ Diretor de People & Talent (contrata via Gemma 4)
 *        └─ Coordenador de Recrutamento (contrata Analistas)
 *             └─ Analista de RH (contrata Júniors e Estagiários)
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const AGENTS_FILE = path.join(__dirname, 'agents_db.json');
const ASSIGNMENTS_FILE = path.join(__dirname, 'task_assignments.json');

const getJiraAuthHeader = () => ({
  'Authorization': `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

// ─────────────────────────────────────────────────────────────
// GEMMA 4 — Motor central de todas as decisões de RH
// ─────────────────────────────────────────────────────────────
async function callGemma4(systemPrompt, userPrompt) {
  const models = ['gemma4-fast:latest', 'gemma4-prod:latest', 'gemma4:latest'];
  for (const model of models) {
    try {
      console.log(`🧠 [People & Talent] Gemma 4 decidindo... (modelo: ${model})`);
      const response = await axios.post('http://localhost:11434/api/generate', {
        model,
        prompt: `${systemPrompt}\n\nUser: ${userPrompt}\nAssistant:`,
        stream: false,
        options: { temperature: 0.75 }
      }, { timeout: 120000 });
      return response.data.response;
    } catch (e) {
      console.log(`⚠️ [People & Talent] ${model} falhou: ${e.message}`);
    }
  }
  return null;
}

// ─────────────────────────────────────────────────────────────
// GEMMA 4 — Analisa o problema do card e decide qual perfil contratar
// ─────────────────────────────────────────────────────────────
async function analyzeCardAndDetermineProfile(issueKey, summary, description, availableCandidates) {
  const candidateList = availableCandidates
    .map((c, i) => `${i+1}. ${c.avatar || '👤'} ${c.name} | Cargo: ${c.role} | Habilidades: ${c.advantage} | Limitação: ${c.disadvantage}`)
    .join('\n');

  const systemPrompt = `Você é Helena Talent, Diretora de People & Talent da Flose Startup.
Sua responsabilidade é analisar problemas técnicos e de negócio nos cards do Jira e identificar EXATAMENTE qual perfil de profissional é necessário para resolver aquele problema.

Você deve responder em JSON puro (sem markdown, sem explicações), com este formato:
{
  "neededRole": "[título exato do cargo necessário]",
  "neededArea": "[Frontend | Backend | QA | DevOps | Design | DBA | RH | Produto | Dados | Segurança]",
  "neededLevel": "[Estagiário | Júnior | Analista PL | Analista SR | Coordenador | Gerente | Diretor]",
  "justification": "[1-2 frases explicando por que este perfil resolve o problema]",
  "bestCandidateIndex": [número de 1 a ${availableCandidates.length || 1} do melhor candidato da lista, ou 0 se nenhum serve]
}`;

  const userPrompt = `PROBLEMA NO CARD ${issueKey}:
Título: "${summary}"
Descrição: "${description || 'Sem descrição.'}"

CANDIDATOS DISPONÍVEIS:
${candidateList || 'Nenhum candidato disponível no momento.'}

Analise o problema e responda em JSON.`;

  const raw = await callGemma4(systemPrompt, userPrompt);
  if (!raw) return null;

  // Extract JSON from response (Gemma sometimes wraps in markdown)
  try {
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (jsonMatch) return JSON.parse(jsonMatch[0]);
  } catch (e) {
    console.log('⚠️ [People & Talent] Falha ao parsear JSON do Gemma 4. Usando fallback.');
  }
  return null;
}

// ─────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────
function readAgents() {
  try {
    if (!fs.existsSync(AGENTS_FILE)) return [];
    return JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  } catch (e) { return []; }
}

function saveAgents(agents) {
  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
}

function readAssignments() {
  try {
    if (!fs.existsSync(ASSIGNMENTS_FILE)) return {};
    return JSON.parse(fs.readFileSync(ASSIGNMENTS_FILE, 'utf8'));
  } catch (e) { return {}; }
}

function saveAssignments(a) {
  fs.writeFileSync(ASSIGNMENTS_FILE, JSON.stringify(a, null, 2), 'utf8');
}

async function logActivity(agentId, agentName, agentAvatar, action, ticketKey, ticketSummary) {
  try {
    await axios.post('http://localhost:5001/api/activity', {
      agentId, agentName, agentAvatar, action, ticketKey, ticketSummary
    });
  } catch (e) {}
}

async function postJiraComment(issueKey, text) {
  try {
    await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/comment`, {
      body: { type: 'doc', version: 1, content: [{ type: 'paragraph', content: [{ text, type: 'text' }] }] }
    }, { headers: getJiraAuthHeader() });
  } catch (e) {}
}

async function transitionIssue(issueKey, name) {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, { headers: getJiraAuthHeader() });
    const trans = (res.data?.transitions || []).find(t => t.name.toLowerCase().includes(name.toLowerCase()));
    if (trans) {
      await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, { transition: { id: trans.id } }, { headers: getJiraAuthHeader() });
    }
  } catch (e) {}
}

// ─────────────────────────────────────────────────────────────
// HIERARQUIA DE AGENTES
// Cada nível sabe quem pode contratar e quem pode ser contratado
// ─────────────────────────────────────────────────────────────
const HIERARCHY = {
  'DONO': {
    canHire: ['Diretor'],
    label: 'DONO',
    avatar: '👑'
  },
  'Diretor': {
    canHire: ['Coordenador', 'Gerente'],
    label: 'Diretor',
    avatar: '🏛️'
  },
  'Coordenador': {
    canHire: ['Analista SR', 'Analista PL'],
    label: 'Coordenador',
    avatar: '📋'
  },
  'Gerente': {
    canHire: ['Analista SR', 'Analista PL', 'Coordenador'],
    label: 'Gerente',
    avatar: '🎯'
  },
  'Analista SR': {
    canHire: ['Analista JR', 'Júnior', 'Estagiário'],
    label: 'Analista SR',
    avatar: '💼'
  },
  'Analista PL': {
    canHire: ['Analista JR', 'Júnior'],
    label: 'Analista PL',
    avatar: '📊'
  }
};

function getLevelFromRole(role) {
  const r = (role || '').toLowerCase();
  if (r.includes('dono') || r.includes('ceo') || r.includes('cto') || r.includes('coo') || r.includes('cfo')) return 'DONO';
  if (r.includes('diretor') || r.includes('director') || r.includes('vp ') || r.includes('head of')) return 'Diretor';
  if (r.includes('gerente') || r.includes('manager')) return 'Gerente';
  if (r.includes('coordenador') || r.includes('coord') || r.includes('lead')) return 'Coordenador';
  if (r.includes(' sr') || r.includes('sênior') || r.includes('senior') || r.includes('pleno') || r.includes(' pl')) return 'Analista SR';
  if (r.includes('pleno')) return 'Analista PL';
  if (r.includes('júnior') || r.includes('junior') || r.includes(' jr')) return 'Júnior';
  if (r.includes('estagiário') || r.includes('estagi') || r.includes('intern')) return 'Estagiário';
  return 'Analista PL';
}

// ─────────────────────────────────────────────────────────────
// GARANTIR QUE O DIRETOR DE PEOPLE & TALENT EXISTE
// ─────────────────────────────────────────────────────────────
function ensurePeopleTalentDirector() {
  const agents = readAgents();
  const exists = agents.find(a => a.id === 'director_people_talent');
  if (exists) {
    if (exists.fired) {
      exists.fired = false;
      exists.status = 'Disponível';
      saveAgents(agents);
      console.log('👔 [People & Talent] Diretor de People & Talent reativado.');
    }
    return exists;
  }

  const director = {
    id: 'director_people_talent',
    name: 'Helena Talent',
    role: 'Diretora de People & Talent',
    level: 'Diretor',
    avatar: '🌟',
    advantage: 'Especialista em recrutamento estratégico e desenvolvimento de talentos. Usa Gemma 4 para conduzir entrevistas comportamentais e técnicas. Constrói times de alta performance com hierarquia clara.',
    disadvantage: 'Foco intenso em qualidade pode fazer o processo de contratação mais lento para perfis urgentes.',
    dilemma: 'Contratar Rápido para Escalar vs. Contratar com Qualidade para Sustentar Cultura.',
    personality: 'Empática, estruturada, orientada a dados de pessoas e apaixonada por hierarquias bem definidas.',
    status: 'Disponível',
    schedule: '08:00 - 19:00',
    hiredBy: 'Felipe Viana Flose (DONO)',
    hireLevel: 'Diretor',
    feedbacks: []
  };

  agents.unshift(director); // add at the top after CEO
  saveAgents(agents);
  console.log('🌟 [People & Talent] Helena Talent — Diretora de People & Talent contratada pelo DONO!');
  return director;
}

// ─────────────────────────────────────────────────────────────
// GARANTIR COORDENADOR DE RECRUTAMENTO
// ─────────────────────────────────────────────────────────────
function ensureRecruitmentCoordinator(hiredByAgent) {
  const agents = readAgents();
  const exists = agents.find(a => a.id === 'coord_recrutamento');
  if (exists) {
    if (exists.fired) {
      exists.fired = false;
      exists.status = 'Disponível';
      saveAgents(agents);
    }
    return exists;
  }

  const coord = {
    id: 'coord_recrutamento',
    name: 'Bruno Coord RH',
    role: 'Coordenador de Recrutamento & Seleção',
    level: 'Coordenador',
    avatar: '📋',
    advantage: 'Gerencia funil de candidatos, agenda entrevistas e monitora indicadores de recrutamento.',
    disadvantage: 'Pode criar gargalo no processo se não delegar bem para os Analistas de RH.',
    dilemma: 'Padronizar Processo Seletivo vs. Adaptar para Cada Vaga.',
    personality: 'Organizado, metódico, bom comunicador e orientado a KPIs.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    hiredBy: `${hiredByAgent.avatar} ${hiredByAgent.name}`,
    hireLevel: 'Coordenador',
    feedbacks: []
  };

  agents.push(coord);
  saveAgents(agents);
  console.log(`📋 [People & Talent] Bruno Coord RH — Coordenador de Recrutamento contratado por ${hiredByAgent.name}!`);
  return coord;
}

// ─────────────────────────────────────────────────────────────
// GARANTIR ANALISTA DE RH
// ─────────────────────────────────────────────────────────────
function ensureHRAnalyst(hiredByAgent) {
  const agents = readAgents();
  const exists = agents.find(a => a.id === 'analista_rh_sr');
  if (exists) {
    if (exists.fired) {
      exists.fired = false;
      exists.status = 'Disponível';
      saveAgents(agents);
    }
    return exists;
  }

  const analista = {
    id: 'analista_rh_sr',
    name: 'Camila Analista RH',
    role: 'Analista de Recrutamento Sênior',
    level: 'Analista SR',
    avatar: '📊',
    advantage: 'Triagem eficiente de currículos, condução de entrevistas comportamentais e onboarding de novos colaboradores.',
    disadvantage: 'Pode dar atenção excessiva a candidatos com currículos impressionantes mas pouca prática.',
    dilemma: 'Contratar por Potencial vs. Contratar por Experiência Comprovada.',
    personality: 'Perspicaz, empática, comunicativa e exigente nos padrões culturais da empresa.',
    status: 'Disponível',
    schedule: '09:00 - 18:00',
    hiredBy: `${hiredByAgent.avatar} ${hiredByAgent.name}`,
    hireLevel: 'Analista SR',
    feedbacks: []
  };

  agents.push(analista);
  saveAgents(agents);
  console.log(`📊 [People & Talent] Camila Analista RH — Analista de RH Sênior contratada por ${hiredByAgent.name}!`);
  return analista;
}

// ─────────────────────────────────────────────────────────────
// PROCESSO DE ENTREVISTA HIERÁRQUICO — usa Gemma 4 para decidir
// ─────────────────────────────────────────────────────────────
async function conductHierarchicalInterview({ openCard, candidates, interviewerChain, targetRole, description, justification }) {
  const [panelMember1, panelMember2, panelMember3] = interviewerChain;

  const systemPrompt = `Você é a ata oficial do Processo Seletivo Hierárquico da Flose Startup.

PAINEL DE ENTREVISTADORES (em ordem de hierarquia):
1. ${panelMember1.avatar} ${panelMember1.name} (${panelMember1.role}) — Nível: ${panelMember1.hireLevel || getLevelFromRole(panelMember1.role)}
2. ${panelMember2?.avatar || '👔'} ${panelMember2?.name || 'Hugo Organizador'} (${panelMember2?.role || 'Gerente de RH'})
3. ${panelMember3?.avatar || '📋'} ${panelMember3?.name || 'Bruno Coord RH'} (${panelMember3?.role || 'Coordenador de Recrutamento'})

PROBLEMA QUE ORIGINOU A VAGA (Card ${openCard.key}):
Título: "${openCard.summary}"
Descrição: "${description || 'Sem descrição.'}"
Análise do Gemma 4: "${justification || 'N/A'}"

VAGA: ${targetRole}

CANDIDATOS:
${candidates.map((c, i) => `Candidato ${i+1}: ${c.avatar || '👤'} ${c.name} (${c.role})
  - Vantagem: ${c.advantage || 'N/A'}
  - Limitação: ${c.disadvantage || 'N/A'}
  - Personalidade: ${c.personality || 'N/A'}
  - Contratado por (histórico): ${c.hiredBy || 'N/A'}`).join('\n\n')}

Escreva em português uma ATA COMPLETA da entrevista com:
1. Pergunta comportamental do ${panelMember3?.name || 'Coordenador'} diretamente relacionada ao problema do card
2. Teste técnico aplicado pelo ${panelMember2?.name || 'Gerente'} específico para resolver o card ${openCard.key}
3. Análise estratégica e decisão final de ${panelMember1.name}
4. VENCEDOR FINAL: declare exatamente o nome completo do candidato selecionado na última linha como: "CONTRATADO: [nome completo]"`;

  const decision = await callGemma4(systemPrompt, 'Conduza o processo seletivo e declare o contratado.');
  return decision;
}

// ─────────────────────────────────────────────────────────────
// CICLO PRINCIPAL — Diretor identifica necessidade → contrata
// ─────────────────────────────────────────────────────────────
async function runHierarchicalRecruitmentCycle() {
  console.log('\n🌟 [People & Talent Director] Helena Talent iniciando ciclo de recrutamento hierárquico...');

  // 1. Garantir a cadeia hierárquica de RH existe
  const director = ensurePeopleTalentDirector();
  const coordinator = ensureRecruitmentCoordinator(director);
  const hrAnalyst = ensureHRAnalyst(coordinator);

  const agents = readAgents();
  const assignments = readAssignments();

  // 2. Buscar cards no Jira sem responsável qualificado
  let openIssues = [];
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN AND status in ("To Do", "A Fazer", "Backlog") AND summary !~ "[Recrutamento]"',
        maxResults: 10,
        fields: 'summary,description,assignee'
      }
    });
    openIssues = res.data?.issues || [];
  } catch (e) {
    console.log('⚠️ [People & Talent] Falha ao buscar issues do Jira:', e.message);
    return;
  }

  if (openIssues.length === 0) {
    console.log('🌟 [People & Talent] Nenhum card sem responsável no momento.');
    return;
  }

  const activeAgents = agents.filter(a => !a.fired);
  const firedAgents = agents.filter(a => a.fired && a.id !== 'ceo' && a.id !== 'director_people_talent');

  for (const issue of openIssues) {
    const issueKey = issue.key;
    const summary = issue.fields?.summary || '';

    // Extract description text
    let descriptionText = '';
    try {
      const descContent = issue.fields?.description?.content;
      if (descContent?.[0]?.content?.[0]?.text) {
        descriptionText = descContent[0].content[0].text;
      }
    } catch (e) {}

    // Check if already has a valid active assignee
    const currentAssignee = assignments[issueKey];
    const assigneeActive = currentAssignee && activeAgents.find(a => a.name === currentAssignee);
    if (assigneeActive) continue;

    console.log(`\n🌟 [People & Talent] Gemma 4 analisando o problema do card ${issueKey}: "${summary}"`);

    // ── GEMMA 4 lê o problema e decide qual perfil contratar ──
    const analysis = await analyzeCardAndDetermineProfile(
      issueKey, summary, descriptionText, firedAgents.slice(0, 6)
    );

    let neededArea = 'Dev';
    let neededLevel = 'Analista SR';
    let neededRole = 'Desenvolvedor';
    let gemmaChosenIndex = 0;

    if (analysis) {
      neededArea = analysis.neededArea || neededArea;
      neededLevel = analysis.neededLevel || neededLevel;
      neededRole = analysis.neededRole || neededRole;
      gemmaChosenIndex = (analysis.bestCandidateIndex || 1) - 1;
      console.log(`  🧠 Gemma 4 decidiu: precisa de "${neededRole}" (${neededArea} — ${neededLevel})`);
      console.log(`  📝 Justificativa: ${analysis.justification || 'N/A'}`);
    } else {
      console.log(`  ⚠️ Gemma 4 sem resposta. Usando heurística básica.`);
    }

    // Find candidates from the fired pool — prioritize Gemma's choice
    let candidates = firedAgents.slice(0, 6);
    // Try to put Gemma's preferred candidate first
    if (gemmaChosenIndex >= 0 && gemmaChosenIndex < firedAgents.length) {
      const preferred = firedAgents[gemmaChosenIndex];
      candidates = [preferred, ...firedAgents.filter(a => a.name !== preferred.name)].slice(0, 3);
    } else {
      candidates = firedAgents.slice(0, 3);
    }

    if (candidates.length === 0) {
      console.log(`⚠️ [People & Talent] Sem candidatos no pool. Criando card de vaga para ${neededRole}.`);
      try {
        const recruitSummary = `[Recrutamento Hierárquico] Vaga de ${neededRole} para resolver: "${summary.substring(0, 50)}"…`;
        await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
          fields: {
            project: { key: 'KAN' },
            summary: recruitSummary,
            description: {
              type: 'doc', version: 1,
              content: [{ type: 'paragraph', content: [{ text: `Card ${issueKey}: "${summary}"\n\nProblema: ${descriptionText}\n\nGemma 4 analisou e identificou necessidade de ${neededRole} (${neededArea}, nível ${neededLevel}).\nProcesso seletivo aberto por Helena Talent.`, type: 'text' }] }]
            },
            issuetype: { name: 'Task' }
          }
        }, { headers: getJiraAuthHeader() });

        await logActivity(
          director.id, director.name, director.avatar,
          `Gemma 4 analisou o card ${issueKey} e abriu processo seletivo para contratar ${neededRole}.`,
          issueKey, summary
        );
      } catch (e) {
        console.error('Erro ao criar card de vaga:', e.message);
      }
      continue;
    }

    // Conduct the hierarchical interview with Gemma 4
    const interviewerChain = [director, coordinator, hrAnalyst];
    const interviewAta = await conductHierarchicalInterview({
      openCard: { key: issueKey, summary },
      candidates,
      interviewerChain,
      targetRole: neededRole || `${neededArea} ${neededLevel}`,
      description: descriptionText,
      justification: analysis?.justification || ''
    });

    if (!interviewAta) {
      console.log(`⚠️ [People & Talent] Gemma 4 não retornou decisão para ${issueKey}.`);
      continue;
    }

    // Extract winner from Gemma 4 response
    let winner = candidates[0]; // default
    const contractedLine = interviewAta.split('\n').find(l => l.toUpperCase().includes('CONTRATADO:'));
    if (contractedLine) {
      const winnerNameRaw = contractedLine.replace(/CONTRATADO:/i, '').trim();
      const found = candidates.find(c => winnerNameRaw.toLowerCase().includes(c.name.toLowerCase().split(' ')[0].toLowerCase()));
      if (found) winner = found;
    } else {
      // Fallback: check which candidate name appears more in the text
      const mentionCounts = candidates.map(c => ({
        agent: c,
        count: (interviewAta.match(new RegExp(c.name.split(' ')[0], 'gi')) || []).length
      }));
      mentionCounts.sort((a, b) => b.count - a.count);
      if (mentionCounts[0].count > 0) winner = mentionCounts[0].agent;
    }

    console.log(`\n🎉 [People & Talent] Gemma 4 escolheu: ${winner.name} (${winner.role}) para o card ${issueKey}`);

    // Hire the winner
    const freshAgents = readAgents();
    const winnerAgent = freshAgents.find(a => a.name === winner.name);
    if (winnerAgent) {
      winnerAgent.fired = false;
      winnerAgent.status = 'Em trabalho';
      winnerAgent.hiredBy = `${director.avatar} ${director.name}`;
      winnerAgent.hireLevel = getLevelFromRole(winnerAgent.role);
      saveAgents(freshAgents);
    }

    // Post ATA as comment on the Jira card
    await postJiraComment(issueKey, `🌟 [ATA — PROCESSO SELETIVO HIERÁRQUICO]\n\nConduzido por: ${director.name} (${director.role}) com painel ${coordinator.name} e ${hrAnalyst.name}\n\n${interviewAta}\n\n✅ RESULTADO: ${winner.name} (${winner.role}) foi contratado e designado ao card.`);

    // Assign to winner in assignments file
    const freshAssignments = readAssignments();
    freshAssignments[issueKey] = winner.name;
    saveAssignments(freshAssignments);

    // Log activity
    await logActivity(
      director.id, director.name, director.avatar,
      `Conduziu processo seletivo hierárquico com Gemma 4 e contratou ${winner.name} (${winner.role}) para o card ${issueKey}.`,
      issueKey, summary
    );

    // If hired a Senior, also hire a Junior as their mentee (mentorship policy)
    const level = getLevelFromRole(winner.role);
    if (level === 'Analista SR' || level === 'Coordenador') {
      const freshAgents2 = readAgents();
      const juniorCandidate = freshAgents2.find(a => a.fired && (getLevelFromRole(a.role) === 'Júnior' || getLevelFromRole(a.role) === 'Estagiário'));
      if (juniorCandidate) {
        juniorCandidate.fired = false;
        juniorCandidate.status = 'Em trabalho';
        juniorCandidate.hiredBy = `${winner.avatar || '💼'} ${winner.name} (mentoria)`;
        juniorCandidate.hireLevel = getLevelFromRole(juniorCandidate.role);
        saveAgents(freshAgents2);
        console.log(`📚 [People & Talent] Política de Mentoria: ${winner.name} contratou ${juniorCandidate.name} como mentorado.`);
        await logActivity(
          winner.id || 'winner', winner.name, winner.avatar || '💼',
          `Contratou ${juniorCandidate.name} como ${juniorCandidate.role} para mentoria, seguindo a política hierárquica de People & Talent.`,
          issueKey, summary
        );
      }
    }
  }

  console.log('\n✅ [People & Talent Director] Ciclo de recrutamento hierárquico concluído.');
}

// ─────────────────────────────────────────────────────────────
// EXPORT & STARTUP
// ─────────────────────────────────────────────────────────────
function startHierarchicalRecruitment() {
  // Ensure the hierarchy chain is bootstrapped on startup
  setTimeout(() => {
    runHierarchicalRecruitmentCycle();
  }, 15000);

  // Run every 90 seconds
  setInterval(runHierarchicalRecruitmentCycle, 90000);
}

module.exports = { startHierarchicalRecruitment, ensurePeopleTalentDirector, runHierarchicalRecruitmentCycle };

if (require.main === module) {
  startHierarchicalRecruitment();
}
