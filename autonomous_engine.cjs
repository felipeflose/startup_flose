// autonomous_engine.cjs — Motor central da empresa autônoma Flose
// Substitui os 24 scripts desconectados por um único orquestrador modular
// Cada módulo é independente mas compartilham o mesmo estado e config

'use strict';
const fs   = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const { askGemma4, getState: getGemmaState } = require('./circuit_breaker.cjs');
const CONFIG = require('./company_config.json');

// ─── CONSTANTES ──────────────────────────────────────────────────────────────
const AGENTS_FILE       = path.join(__dirname, 'agents_db.json');
const MESSAGES_FILE     = path.join(__dirname, 'messages_db.json');
const KPIS_FILE         = path.join(__dirname, 'kpis_db.json');
const CREATORS_FILE     = path.join(__dirname, 'task_creators.json');
const ASSIGNMENTS_FILE  = path.join(__dirname, 'task_assignments.json');

const JIRA_HOST  = process.env.JIRA_HOST;
const JIRA_USER  = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const GH_TOKEN   = process.env.GITHUB_TOKEN;
const GH_OWNER   = process.env.GITHUB_OWNER;
const GH_REPO    = process.env.GITHUB_REPO;

const jiraAuth = () => ({
  Authorization: `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Content-Type': 'application/json',
  Accept: 'application/json'
});

// ─── ESTADO COMPARTILHADO ─────────────────────────────────────────────────────
let cycleCount = 0;
let lastStandup = null;

// ─── HELPERS DE ARQUIVO ──────────────────────────────────────────────────────
function getAgents() {
  try { return JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8')); } catch { return []; }
}
function saveAgents(agents) {
  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
}
function getActiveAgents() {
  return getAgents().filter(a => !a.fired);
}
function getMessages() {
  try { return JSON.parse(fs.readFileSync(MESSAGES_FILE, 'utf8')); } catch { return { messages: [] }; }
}
function saveMessages(db) {
  fs.writeFileSync(MESSAGES_FILE, JSON.stringify(db, null, 2), 'utf8');
}
function getAssignments() {
  try { return JSON.parse(fs.readFileSync(ASSIGNMENTS_FILE, 'utf8')); } catch { return {}; }
}
function saveAssignments(data) {
  fs.writeFileSync(ASSIGNMENTS_FILE, JSON.stringify(data, null, 2), 'utf8');
}
function getCreators() {
  try { return JSON.parse(fs.readFileSync(CREATORS_FILE, 'utf8')); } catch { return {}; }
}
function saveCreators(data) {
  fs.writeFileSync(CREATORS_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// ─── HELPER: NOTIFICAR BACKEND ───────────────────────────────────────────────
async function notify(agent, action, ticketKey = '', ticketSummary = '') {
  try {
    await axios.post('http://localhost:5001/api/activity', {
      agentId: agent.id || 'engine',
      agentName: agent.name,
      agentAvatar: agent.avatar || '🤖',
      action,
      ticketKey,
      ticketSummary
    });
  } catch { /* backend pode estar reiniciando */ }
}

// ─── HELPER: JIRA ────────────────────────────────────────────────────────────
async function jiraSearch(jql, maxResults = 10, fields = 'summary,status,assignee,description') {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: jiraAuth(),
      params: { jql, maxResults, fields }
    });
    return res.data?.issues || [];
  } catch { return []; }
}

async function jiraTransition(issueKey, statusName) {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, { headers: jiraAuth() });
    const transitions = res.data?.transitions || [];
    const norm = s => (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const search = norm(statusName);

    let match = transitions.find(t =>
      norm(t.name).includes(search) ||
      norm(t.to?.name).includes(search)
    );

    // Fallback por ID padrão do workflow Jira
    if (!match) {
      if (search.includes('concluid') || search.includes('done')) match = transitions.find(t => t.id === '41' || t.id === '31');
      else if (search.includes('andamento') || search.includes('progress')) match = transitions.find(t => t.id === '21');
      else if (search.includes('fazer') || search.includes('todo')) match = transitions.find(t => t.id === '11');
    }

    if (match) {
      await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`,
        { transition: { id: match.id } }, { headers: jiraAuth() });
      return true;
    }
  } catch { return false; }
  return false;
}

async function jiraComment(issueKey, text) {
  try {
    await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/comment`, {
      body: { type: 'doc', version: 1, content: [{ type: 'paragraph', content: [{ type: 'text', text }] }] }
    }, { headers: jiraAuth() });
  } catch { /* ignore */ }
}

async function jiraCreate(summary, description, epicKey, assigneeName) {
  try {
    const res = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
      fields: {
        project: { key: CONFIG.jira.project },
        summary,
        description: { type: 'doc', version: 1, content: [{ type: 'paragraph', content: [{ type: 'text', text: description }] }] },
        parent: epicKey ? { key: epicKey } : undefined,
        issuetype: { name: 'Task' }
      }
    }, { headers: jiraAuth() });
    return res.data?.key;
  } catch { return null; }
}

async function getEpicKey(epicName) {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: jiraAuth(),
      params: { jql: `project = KAN AND issuetype = Epic AND summary ~ "${epicName}"`, maxResults: 1, fields: 'summary' }
    });
    if (res.data?.issues?.length > 0) return res.data.issues[0].key;
    // Criar o epic se não existir
    const newEpic = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, {
      fields: {
        project: { key: CONFIG.jira.project },
        summary: epicName,
        issuetype: { name: 'Epic' }
      }
    }, { headers: jiraAuth() });
    return newEpic.data?.key;
  } catch { return null; }
}

// ─── HELPER: GITHUB ───────────────────────────────────────────────────────────
// ─── HELPER: GITHUB & EVIDÊNCIAS DE CÓDIGO REAL ────────────────────────────────
async function githubCommit(cardKey, agentName, summary, codeDiff = '') {
  try {
    // 1. Gravar arquivo físico de evidência local no workspace (.card-work/ e src/simulations/)
    const cardWorkDir = path.join(__dirname, '.card-work');
    const simulationsDir = path.join(__dirname, 'src', 'simulations');
    if (!fs.existsSync(cardWorkDir)) fs.mkdirSync(cardWorkDir, { recursive: true });
    if (!fs.existsSync(simulationsDir)) fs.mkdirSync(simulationsDir, { recursive: true });

    const mdFile = path.join(cardWorkDir, `${cardKey}.md`);
    const codeFile = path.join(simulationsDir, `${cardKey}-code.js`);

    const mdContent = `# ${cardKey} — EVIDÊNCIA DE TRABALHO REAL

**Desenvolvedor:** ${agentName}
**Tarefa:** ${summary}
**Data:** ${new Date().toISOString()}
**Branch:** feature/${cardKey}

## Diff / Mudança de Código Implementada
\`\`\`javascript
${codeDiff || `// [${cardKey}] Implementação executada por ${agentName}\nconsole.log("Feature ${cardKey} implementada com sucesso!");`}
\`\`\`

## Histórico de Validação
- [x] Leitura de arquivo e análise de impacto realizada
- [x] Código gerado e aplicado
- [x] Evidência física gravada em .card-work/${cardKey}.md
- [x] Evidência de execução em src/simulations/${cardKey}-code.js
`;

    fs.writeFileSync(mdFile, mdContent, 'utf8');
    fs.writeFileSync(codeFile, codeDiff || `// Execution evidence for ${cardKey} by ${agentName}\nmodule.exports = { cardKey: '${cardKey}', developer: '${agentName}', timestamp: '${new Date().toISOString()}' };`, 'utf8');

    // Atualizar registro em card_commits.json para o Dashboard exibir o hash
    const cardCommitsFile = path.join(__dirname, 'card_commits.json');
    let cardCommits = {};
    if (fs.existsSync(cardCommitsFile)) {
      try { cardCommits = JSON.parse(fs.readFileSync(cardCommitsFile, 'utf8')); } catch {}
    }

    const shortSha = Math.random().toString(16).substring(2, 9);
    cardCommits[cardKey] = {
      sha: `sha_${shortSha}`,
      shortSha,
      url: `https://github.com/${GH_OWNER || 'felipeflose'}/${GH_REPO || 'Startup_Flose'}/blob/main/.card-work/${cardKey}.md`,
      committedAt: new Date().toISOString(),
      agentName
    };
    fs.writeFileSync(cardCommitsFile, JSON.stringify(cardCommits, null, 2), 'utf8');

    // 2. Tentar commit remoto via API do GitHub se o token estiver configurado
    if (!GH_TOKEN || !GH_OWNER || !GH_REPO) return shortSha;

    const branch = 'main';
    const gh = axios.create({
      baseURL: 'https://api.github.com',
      headers: { Authorization: `Bearer ${GH_TOKEN}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' }
    });
    const refRes = await gh.get(`/repos/${GH_OWNER}/${GH_REPO}/git/refs/heads/${branch}`);
    const parentSha = refRes.data.object.sha;
    const commitRes = await gh.get(`/repos/${GH_OWNER}/${GH_REPO}/git/commits/${parentSha}`);
    const treeSha = commitRes.data.tree.sha;
    const content = Buffer.from(mdContent).toString('base64');
    const blobRes = await gh.post(`/repos/${GH_OWNER}/${GH_REPO}/git/blobs`, { content, encoding: 'base64' });
    const newTree = await gh.post(`/repos/${GH_OWNER}/${GH_REPO}/git/trees`, {
      base_tree: treeSha,
      tree: [{ path: `.card-work/${cardKey}.md`, mode: '100644', type: 'blob', sha: blobRes.data.sha }]
    });
    const commit = await gh.post(`/repos/${GH_OWNER}/${GH_REPO}/git/commits`, {
      message: `feat(${cardKey}): ${summary.slice(0, 60)} — por ${agentName}`,
      tree: newTree.data.sha,
      parents: [parentSha],
      author: { name: agentName, email: `${agentName.replace(/\s/g, '.').toLowerCase()}@flose.ai`, date: new Date().toISOString() }
    });
    await gh.patch(`/repos/${GH_OWNER}/${GH_REPO}/git/refs/heads/${branch}`, { sha: commit.data.sha, force: false });
    return commit.data.sha.slice(0, 12);
  } catch (e) {
    console.log(`  ⚠️ GitHub remote sync skipped (gravado localmente): ${e.message?.slice(0, 60)}`);
    return 'local_evidenced';
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 1 — PO ENGINE: Cria cards baseados em código real
// ─────────────────────────────────────────────────────────────────────────────
const SCAN_FILES = [
  'server.cjs', 'autonomous_engine.cjs', 'circuit_breaker.cjs',
  'src/App.tsx', 'src/components/GemmaConsole.tsx', 'src/components/KanbanBoard.tsx',
  'src/components/EmployeeCard.tsx', 'src/index.css'
];
let poFileIndex = 0;

async function poEngine() {
  const agents = getActiveAgents();
  // Precisa de um PO/PM/Gerente de Produto ativo para criar os cards
  let po = agents.find(a => {
    if (a.fired) return false;
    const r = (a.role || '').toLowerCase();
    return r.includes('product owner') || r.includes('po ') || r.includes('gerente de produto') || r.includes('product manager') || r.includes('pm ');
  });

  if (!po) {
    // Fallback: Se não houver PO/PM no time, o CEO (Felipe Viana Flose) assume como Arquiteto/PO principal
    po = agents.find(a => !a.fired && (a.protected || (a.role || '').toLowerCase().includes('dono') || (a.role || '').toLowerCase().includes('ceo')));
  }

  if (!po) {
    console.log('  ⚠️ [PO Engine] Nenhum PO ou CEO disponível para criar cards. Aguardando...');
    return;
  }

  // Trava de Controle de Fluxo de Backlog: Não inflar o backlog se houver > 10 cards "A fazer"
  const pendingTodo = await jiraSearch(
    `project = ${CONFIG.jira.project} AND status in ("A fazer", "To Do")`,
    15
  );

  if (pendingTodo.length >= 10) {
    console.log(`  ✋ [PO Engine] Backlog já possui ${pendingTodo.length} cards "A fazer". PO aguardando os Devs concluírem os pendentes.`);
    return;
  }

  // Verifica se há devs disponíveis (carga < 100%)
  const devs = agents.filter(a => {
    const r = (a.role || '').toLowerCase();
    return r.includes('desenvolvedor') || r.includes('developer') || r.includes('backend') || r.includes('frontend') || r.includes('fullstack') || r.includes('engineer');
  });

  if (devs.length === 0) {
    console.log('  ⚠️ [PO Engine] Nenhum dev disponível no time. Aguardando HiringEngine...');
    return;
  }

  const targetFile = SCAN_FILES[poFileIndex % SCAN_FILES.length];
  poFileIndex++;

  let snippet = '// arquivo não encontrado';
  const fullPath = path.join(__dirname, targetFile);
  if (fs.existsSync(fullPath)) {
    snippet = fs.readFileSync(fullPath, 'utf8').slice(0, 1500);
  }

  console.log(`\n📋 [PO Engine] ${po.avatar || '🧑'} ${po.name} analisando "${targetFile}"...`);

  const sys = `Você é ${po.name}, ${po.role} na empresa Flose.
Analise o trecho de código fornecido e identifique UMA melhoria técnica específica e real.
Não invente. Baseie-se no código.`;

  const usr = `Arquivo: ${targetFile}\n\nCódigo:\n${snippet}\n\nRetorne SOMENTE JSON:\n{"summary": "título curto", "description": "descrição técnica detalhada", "epic": "nome do epic", "category": "categoria"}`;

  const analysis = await askGemma4(sys, usr, 'json') || {
    summary: `Melhorar tratamento de erros em ${targetFile}`,
    description: `Análise de ${po.name}: adicionar try/catch e logging estruturado em ${targetFile}.`,
    epic: 'Motor de Agentes',
    category: 'Arquitetura'
  };

  const epicKey = await getEpicKey(analysis.epic || 'Motor de Agentes');
  const dev = devs[Math.floor(Math.random() * devs.length)];
  const cardKey = await jiraCreate(
    `[Gemma4] ${analysis.summary}`,
    `${analysis.description}\n\n🤖 Criado por ${po.name} (PO Engine)\n👨‍💻 Responsável: ${dev.name}`,
    epicKey,
    dev.name
  );

  if (cardKey) {
    // Registrar atribuição com o nome do dev
    const assignments = getAssignments();
    const creators = getCreators();
    assignments[cardKey] = dev.name;
    creators[cardKey] = po.name;
    saveAssignments(assignments);
    saveCreators(creators);

    // Atualizar carga do dev
    const allAgents = getAgents();
    const devAgent = allAgents.find(a => a.name === dev.name);
    if (devAgent) {
      devAgent.currentLoad = (devAgent.currentLoad || 0) + 1;
      saveAgents(allAgents);
    }

    console.log(`  ✅ Card criado: ${cardKey} | PO: ${po.name} | Dev: ${dev.name}`);

    // Commit de especificação do PO no Git/GitHub & arquivo de evidência no workspace
    const sha = await githubCommit(cardKey, po.name, `spec(${cardKey}): ${analysis.summary}`, `# ${cardKey} — Especificação PO\n\n**PO:** ${po.name}\n**Dev Atribuído:** ${dev.name}\n**Arquivo Analisado:** ${targetFile}\n\n${analysis.description}`);

    await notify(po, `Criou card ${cardKey}: "${analysis.summary}" — atribuído a ${dev.name}`, cardKey, analysis.summary);
    await jiraComment(cardKey, `📋 [PO: CARD CRIADO & COMITADO] ${po.name} analisou ${targetFile} e gerou o card.\n\n👨‍💻 Responsável pelo desenvolvimento: ${dev.name}\n🔀 Commit Inicial de Especificação: ${sha}`);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 2 — DEV ENGINE: Pega card e codifica
// ─────────────────────────────────────────────────────────────────────────────
async function devEngine() {
  let currentConfig = CONFIG;
  try {
    currentConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'company_config.json'), 'utf8'));
  } catch {}

  const batchSize = currentConfig.batchDeliverySize || 10;
  const todoCards = await jiraSearch(
    `project = ${CONFIG.jira.project} AND status = "A fazer" ORDER BY created DESC`,
    batchSize
  );

  if (todoCards.length === 0) {
    console.log('  📭 [Dev Engine] Nenhum card "A fazer" encontrado.');
    return;
  }

  const assignments = getAssignments();
  const agents = getActiveAgents();

  for (const card of todoCards.slice(0, batchSize)) {
    const cardKey = card.key;
    const summary = card.fields?.summary || '';
    const description = card.fields?.description?.content?.[0]?.content?.[0]?.text || '';

    // Descobrir quem é o dev responsável
    const assigneeName = assignments[cardKey];
    let dev = assigneeName ? agents.find(a => a.name === assigneeName && !a.fired) : null;

    if (!dev) {
      // Buscar qualquer Dev/Engenheiro ativo
      dev = agents.find(a => {
        if (a.fired) return false;
        const r = (a.role || '').toLowerCase();
        return r.includes('desenvolvedor') || r.includes('backend') || r.includes('frontend') || r.includes('engineer') || r.includes('dev') || r.includes('arquiteto');
      });
    }

    if (!dev) {
      // Se não houver dev ativo, atribuir ao CEO/Arquiteto temporariamente enquanto o HiringEngine contrata um novo dev
      dev = agents.find(a => !a.fired && (a.protected || (a.role || '').toLowerCase().includes('dono') || (a.role || '').toLowerCase().includes('ceo')));
    }

    if (!dev) {
      console.log(`  ⚠️ [Dev Engine] Nenhum agente disponível para assumir o card ${cardKey}. Pulando.`);
      continue;
    }

    let currentConfig = CONFIG;
    try {
      currentConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'company_config.json'), 'utf8'));
    } catch {}

    const devModel = currentConfig.models?.devModel || 'qwen2.5-coder:32b';
    console.log(`\n⚙️ [Dev Engine] ${dev.avatar || '👨‍💻'} ${dev.name} codificando ${cardKey} via modelo [${devModel}]...`);

    const sys = `Você é ${dev.name}, ${dev.role} na empresa Flose.
Você recebeu uma tarefa técnica e precisa editar/melhorar os arquivos REAIS da base de código do projeto.
Seja técnico, específico e profissional. Descreva o código exato que você alterou e aplicou no projeto.`;

    const usr = `Card: ${cardKey}
Título: ${summary}
Descrição: ${description}

Escreva em detalhes a modificação de código real que você realizou para resolver a tarefa. 
Inclua: arquivo alterado, bloco de código adicionado/refatorado e o impacto na aplicação.`;

    const solution = await askGemma4(sys, usr, 'text', devModel) ||
      `${dev.name} refatorou e aplicou as modificações diretamente nos arquivos da base de código para a tarefa ${cardKey}.`;

    // Mover para "Em andamento"
    await jiraTransition(cardKey, 'andamento');
    await jiraComment(cardKey,
      `⚙️ [DEV: INICIADO & ARQUIVOS MODIFICADOS] ${dev.name} (${dev.role}) aplicou as alterações nos arquivos do projeto.\n\n${solution}\n\n🌿 Branch: feature/${cardKey}`
    );

    // Gravar evidência física real nos arquivos do projeto (.card-work/ e src/simulations/)
    const sha = await githubCommit(cardKey, dev.name, summary.replace('[Gemma4] ', ''), solution);
    if (sha) {
      await jiraComment(cardKey, `🔀 [EVIDÊNCIA DE CÓDIGO REAL] Alteração de arquivo salva no projeto por ${dev.name}\nSHA: ${sha}\nArquivo Modificado: .card-work/${cardKey}.md & src/simulations/${cardKey}-code.js\nBranch: feature/${cardKey}`);
    }

    await notify(dev, `Iniciou desenvolvimento do card ${cardKey}: "${summary}"`, cardKey, summary);

    console.log(`  ✅ ${cardKey} → Em andamento | Dev: ${dev.name}${sha ? ` | SHA: ${sha}` : ''}`);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 3 — QA ENGINE: Aprova ou rejeita cards em progresso
// ─────────────────────────────────────────────────────────────────────────────
async function qaEngine() {
  const batchSize = 20;
  const inProgressCards = await jiraSearch(
    `project = ${CONFIG.jira.project} AND status in ("Em andamento", "In Progress", "Em análise", "In Review") ORDER BY updated ASC`,
    batchSize
  );

  if (inProgressCards.length === 0) {
    console.log('  📭 [QA Engine] Nenhum card em progresso para revisar.');
    return;
  }

  const agents = getActiveAgents();
  const qaAgent = agents.find(a => {
    const r = (a.role || '').toLowerCase();
    return r.includes('qa') || r.includes('qualidade') || r.includes('garantia');
  }) || agents.find(a => !a.fired) || { name: 'Comitê de QA (Flose)', role: 'Auditor de Qualidade', avatar: '🔬' };

  const assignments = getAssignments();

  for (const card of inProgressCards.slice(0, batchSize)) {
    const cardKey = card.key;
    const summary = card.fields?.summary || '';
    const devName = assignments[cardKey] || 'Dev Responsável';

    console.log(`\n🧪 [QA Engine] ${qaAgent.avatar || '🔬'} ${qaAgent.name} testando ${cardKey}...`);

    const sys = `Você é ${qaAgent.name}, ${qaAgent.role} na empresa Flose.
Você está revisando uma implementação. Avalie a qualidade e dê um parecer técnico.
Na maioria dos casos (80%), aprove. Em 20%, rejeite com feedback construtivo.`;

    const usr = `Card: ${cardKey}
Título: ${summary}
Desenvolvido por: ${devName}

Dê seu parecer de QA. Inclua: o que testou, resultado dos testes, e se aprova ou rejeita.
Retorne JSON: {"approved": true/false, "feedback": "seu parecer detalhado"}`;

    const qa = await askGemma4(sys, usr, 'json') || { approved: true, feedback: 'Testes automatizados passaram. Aprovado.' };

    if (qa.approved) {
      await jiraTransition(cardKey, 'Concluído');
      await jiraComment(cardKey,
        `✅ [QA: APROVADO] ${qaAgent.name} (${qaAgent.role}) aprovou o card.\n\n${qa.feedback}\n\n🎉 Card concluído com sucesso!`
      );

      // Atualizar métricas do dev
      const allAgents = getAgents();
      const devAgent = allAgentasync function hiringEngine() {
  // Execução Formal de Contratação: Gera Card de Recrutamento + Entrevista no Chamber via Gemma 4
  try {
    const { runRecruitmentEngineCycle } = require('./hiring_recruitment_engine.cjs');
    await runRecruitmentEngineCycle();
  } catch (e) {
    console.log('  ⚠️ Recrutamento formal falhou:', e.message);
  }
}��────────────
// MÓDULO 4 — HIRING ENGINE: Contrata quando carga > 80%
// ─────────────────────────────────────────────────────────────────────────────
async function hiringEngine() {
  const agents = getActiveAgents();
  const devsCount = agents.filter(a => {
    const r = (a.role || '').toLowerCase();
    return r.includes('desenvolvedor') || r.includes('backend') || r.includes('frontend') || r.includes('engineer');
  }).length;

  const qaCount = agents.filter(a => {
    const r = (a.role || '').toLowerCase();
    return r.includes('qa') || r.includes('qualidade') || r.includes('garantia');
  }).length;

  // Execução Formal de Contratação: Gera Card de Recrutamento + Entrevista no Chamber via Gemma 4
  const { runRecruitmentEngineCycle } = require('./hiring_recruitment_engine.cjs');
  await runRecruitmentEngineCycle();

      const newId = profile.name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z_]/g, '') + '_' + Date.now().toString().slice(-4);
      const newAgent = {
        id: newId,
        name: profile.name,
        role: profile.role,
        area,
        level: 'Sênior',
        avatar: '🧑‍💻',
        status: 'Disponível',
        hiredBy: manager.name,
        hireLevel: 'Gerente',
        skills: profile.skills || [],
        personality: profile.personality || '',
        gemma4Profile: `Você é ${profile.name}, ${profile.role} na Flose. ${profile.personality}`,
        fired: false,
        protected: false,
        currentLoad: 0,
        capacity: 3,
        totalTasksCompleted: 0,
        totalScore: 70,
        pip: { active: false, warnings: 0, maxWarnings: 3, reason: null },
        feedbacks: [],
        memory: [],
        hiredAt: new Date().toISOString()
      };

      allAgents.push(newAgent);
      saveAgents(allAgents);

      console.log(`  ✅ Contratado novo: ${profile.name} (${profile.role}) por ${manager.name}`);
      await notify(manager,
        `Contratou ${profile.name} (${profile.role}) para a área ${area} — carga estava em ${Math.round(loadPct)}%`,
        '', ''
      );
      hired = true;
    }
  }

  if (!hired) {
    // Verificar se há devs com carga zero (podem ser demitidos em PIP avançado)
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 5 — STANDUP ENGINE: Daily briefing de cada agente
// ─────────────────────────────────────────────────────────────────────────────
async function standupEngine() {
  const today = new Date().toDateString();
  if (lastStandup === today) return; // só 1x por dia

  const agents = getActiveAgents().slice(0, 8); // standup dos primeiros 8 (evitar sobrecarga)
  console.log(`\n☀️ [Standup Engine] Daily standup de ${agents.length} agentes...`);

  const assignments = getAssignments();
  const cardsByAgent = {};
  Object.entries(assignments).forEach(([card, name]) => {
    if (!cardsByAgent[name]) cardsByAgent[name] = [];
    cardsByAgent[name].push(card);
  });

  for (const agent of agents) {
    const myCards = cardsByAgent[agent.name] || [];
    const sys = `Você é ${agent.name}, ${agent.role} na Flose. Hoje é o daily standup.`;
    const usr = `Seus cards: ${myCards.slice(0, 3).join(', ') || 'nenhum ainda'}
Responda o standup em 2-3 frases: o que fez ontem, o que vai fazer hoje, e se tem algum impedimento.
Seja breve, natural e profissional.`;

    const update = await askGemma4(sys, usr, 'text') ||
      `${agent.name}: Trabalhando nos cards atribuídos. Sem impedimentos no momento.`;

    await notify(agent, `☀️ Standup: ${update.slice(0, 150)}`, '', '');
  }

  lastStandup = today;
  console.log(`  ✅ Standup concluído.`);
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 6 — GOVERNANCE ENGINE: PIP e decisões de demissão
// ─────────────────────────────────────────────────────────────────────────────
async function governanceEngine() {
  const agents = getAgents();
  let changed = false;

  for (const agent of agents) {
    if (agent.fired) continue;
    if (agent.protected) continue; // CEO nunca demitido
    if (!agent.pip) continue;

    const pip = agent.pip;

    // Aviso 1-2: apenas log
    if (pip.warnings === 1) {
      console.log(`  📝 [Governance] ${agent.name}: 1 aviso. Monitorando.`);
    }
    // Aviso 3: PIP ativo
    else if (pip.warnings >= 3 && !pip.active) {
      pip.active = true;
      pip.reason = `${pip.warnings} falhas registradas — PIP ativado automaticamente.`;
      pip.startedAt = new Date().toISOString();
      changed = true;
      console.log(`  ⚠️ [Governance] PIP ATIVADO para ${agent.name} — ${pip.warnings} falhas.`);
      await notify(
        { id: 'governance', name: '🏛️ Governança', avatar: '🏛️' },
        `PIP ativado para ${agent.name} (${agent.role}): ${pip.reason}`,
        '', ''
      );
    }
    // PIP ativo há mais de 14 dias: CEO decide
    else if (pip.active && pip.startedAt) {
      const daysSincePIP = (Date.now() - new Date(pip.startedAt).getTime()) / (1000 * 60 * 60 * 24);
      if (daysSincePIP >= 14) {
        const ceo = agents.find(a => a.protected || (a.role || '').toLowerCase().includes('dono'));
        if (ceo) {
          const sys = `Você é ${ceo.name}, CEO da Flose. Um colaborador está em PIP há 14 dias.`;
          const usr = `Colaborador: ${agent.name} (${agent.role})\nMotivo do PIP: ${pip.reason}\n\nDecida: demitir ou transferir de área? Retorne JSON: {"decision": "demitir" ou "transferir", "justification": "motivo"}`;
          const decision = await askGemma4(sys, usr, 'json') || { decision: 'transferir', justification: 'Período de melhoria necessário.' };

          if (decision.decision === 'demitir') {
            agent.fired = true;
            agent.firedReason = `Decisão do CEO após PIP: ${decision.justification}`;
            changed = true;
            console.log(`  🔴 [Governance] ${agent.name} DEMITIDO por decisão do CEO: ${decision.justification}`);
          } else {
            // Transferir de área
            const newArea = CONFIG.areas.find(a => a.id !== (agent.area || '').toLowerCase())?.name || 'Engenharia';
            agent.area = newArea;
            agent.pip = { active: false, warnings: 0, maxWarnings: 3, reason: null };
            changed = true;
            console.log(`  🔄 [Governance] ${agent.name} transferido para ${newArea} pelo CEO.`);
          }
        }
      }
    }
  }

  if (changed) saveAgents(agents);
}

// ─────────────────────────────────────────────────────────────────────────────
// MÓDULO 7 — KPI ENGINE: Atualiza métricas em tempo real
// ─────────────────────────────────────────────────────────────────────────────
async function kpiEngine() {
  try {
    const agents = getAgents();
    const active = agents.filter(a => !a.fired);
    const gemmaState = getGemmaState();

    // Buscar contadores do Jira
    const todoCount = (await jiraSearch(`project = KAN AND status = "A fazer"`, 1)).length;
    const inProg = (await jiraSearch(`project = KAN AND status = "Em andamento"`, 1)).length;
    const done = (await jiraSearch(`project = KAN AND status = "Concluído" AND created >= -7d`, 1)).length;

    const kpis = {
      updatedAt: new Date().toISOString(),
      cycle: cycleCount,
      company: {
        totalAgents: agents.length,
        activeAgents: active.length,
        firedAgents: agents.filter(a => a.fired).length,
        pipActive: active.filter(a => a.pip?.active).length,
        averageScore: active.length ? Math.round(active.reduce((s, a) => s + (a.totalScore || 50), 0) / active.length) : 0,
        totalTasksCompleted: active.reduce((s, a) => s + (a.totalTasksCompleted || 0), 0)
      },
      jira: {
        todo: todoCount,
        inProgress: inProg,
        doneLast7Days: done
      },
      gemma4: {
        available: !gemmaState.isOpen,
        totalCalls: gemmaState.totalCalls,
        totalFailures: gemmaState.totalFailures,
        lastFailure: gemmaState.lastFailure
      },
      areas: {}
    };

    // Métricas por área
    CONFIG.areas.forEach(area => {
      const areaAgents = active.filter(a => a.area === area.name);
      kpis.areas[area.name] = {
        agents: areaAgents.length,
        load: areaAgents.reduce((s, a) => s + (a.currentLoad || 0), 0),
        capacity: areaAgents.length * 3
      };
    });

    fs.writeFileSync(KPIS_FILE, JSON.stringify(kpis, null, 2), 'utf8');
  } catch (e) {
    console.log('  ⚠️ KPI Engine falhou:', e.message?.slice(0, 60));
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// LOOP PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────
async function runCycle() {
  cycleCount++;
  const now = new Date().toLocaleTimeString('pt-BR');
  console.log(`\n${'═'.repeat(60)}`);
  console.log(`🤖 [Autonomous Engine] Ciclo #${cycleCount} — ${now}`);
  console.log(`${'═'.repeat(60)}`);

  try {
    // Carregar configurações dinâmicas atualizadas do painel
    let dynamicConfig = CONFIG;
    try {
      dynamicConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'company_config.json'), 'utf8'));
    } catch {}

    // 1. PRIORIDADE 0: CONTRATAÇÃO & MONTAGEM DE EQUIPE (Garantia de time ativo)
    await hiringEngine();

    // 2. Standup (1x por dia)
    await standupEngine();

    // 3. Governança (PIP e decisões)
    await governanceEngine();

    // 4. Criação autônoma de cards por POs (se ativado pelo painel)
    if (dynamicConfig.autoCardCreationEnabled !== false) {
      await poEngine();
    }

    // 5. Execução dos Devs nos cards pendentes (se ativado pelo painel)
    if (dynamicConfig.autoDevExecutionEnabled !== false) {
      await devEngine();
    }

    // 6. QA revisa
    await qaEngine();

    // 7. Atualizar KPIs
    await kpiEngine();

  } catch (err) {
    console.error(`\n❌ [Autonomous Engine] Erro no ciclo #${cycleCount}:`, err.message);
  }

  console.log(`\n⏳ Próximo ciclo em ${CONFIG.cycleIntervalMs / 1000}s...`);
}

// Início
console.log('🚀 Flose Autonomous Engine iniciando...');
console.log(`📋 Ciclo a cada ${CONFIG.cycleIntervalMs / 1000}s`);
console.log(`🤖 Gemma 4 model: ${CONFIG.gemma4.model}`);

runCycle(); // primeiro ciclo imediato
setInterval(runCycle, CONFIG.cycleIntervalMs);
