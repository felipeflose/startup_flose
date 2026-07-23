/**
 * gemma4_company_analyst.cjs
 *
 * Gemma 4 lê o que a empresa realmente faz (código, backlog, logs),
 * entende os problemas, decide quais áreas e cargos existem,
 * e cria cards de contratação no Jira — sem nada hardcoded.
 *
 * Felipe Viana Flose (DONO) é o único ponto fixo.
 * Todo o resto é decidido pelo Gemma 4.
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const AGENTS_FILE = path.join(__dirname, 'agents_db.json');
const COMPANY_MAP_FILE = path.join(__dirname, 'company_map.json');
const ROOT = __dirname;

const getJiraAuthHeader = () => ({
  'Authorization': `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

// ─────────────────────────────────────────────────────────────
// Gemma 4 — único motor de decisão
// ─────────────────────────────────────────────────────────────
async function gemma4(prompt) {
  const models = ['gemma4-fast:latest', 'gemma4-prod:latest', 'gemma4:latest'];
  for (const model of models) {
    try {
      console.log(`  🧠 Gemma 4 [${model}] pensando...`);
      const res = await axios.post('http://localhost:11434/api/generate', {
        model,
        prompt,
        stream: false,
        options: { temperature: 0.7, num_predict: 2048 }
      }, { timeout: 120000 });
      return res.data.response || '';
    } catch (e) {
      console.log(`  ⚠️ ${model} falhou: ${e.message}`);
    }
  }
  return '';
}

// ─────────────────────────────────────────────────────────────
// Coleta evidências reais da empresa
// ─────────────────────────────────────────────────────────────
async function collectCompanyEvidence() {
  console.log('\n🔍 [Analista] Coletando evidências reais da empresa...');

  const evidence = {};

  // 1. Lê arquivos chave do código
  const filesToRead = [
    'package.json',
    'server.cjs',
    'src/App.tsx',
    'gemma4_autonomous_pipeline.cjs',
    'po_frenetic_analyzer.cjs',
    'hiring_recruitment_engine.cjs',
    'README.md'
  ];

  let codeSnippets = '';
  for (const f of filesToRead) {
    try {
      const content = fs.readFileSync(path.join(ROOT, f), 'utf8');
      // Only take first 300 lines to avoid token overflow
      const lines = content.split('\n').slice(0, 300).join('\n');
      codeSnippets += `\n\n=== ARQUIVO: ${f} ===\n${lines}`;
    } catch (e) {}
  }
  evidence.code = codeSnippets;

  // 2. Lê os últimos cards do Jira (problemas reais)
  let jiraProblems = '';
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN order by created DESC',
        maxResults: 40,
        fields: 'summary,description,status,issuetype'
      }
    });
    const issues = res.data?.issues || [];
    jiraProblems = issues.map(i => {
      const desc = i.fields?.description?.content?.[0]?.content?.[0]?.text || '';
      return `[${i.key}] ${i.fields?.status?.name} | ${i.fields?.summary} ${desc ? '— ' + desc.substring(0, 100) : ''}`;
    }).join('\n');
  } catch (e) {
    jiraProblems = 'Não foi possível buscar cards do Jira: ' + e.message;
  }
  evidence.jira = jiraProblems;

  // 3. Lê os últimos logs de atividade
  let recentActivity = '';
  try {
    const activityFile = path.join(ROOT, 'activity_log.json');
    if (fs.existsSync(activityFile)) {
      const acts = JSON.parse(fs.readFileSync(activityFile, 'utf8'));
      recentActivity = acts.slice(-20).map(a => `${a.agentName}: ${a.action}`).join('\n');
    }
  } catch (e) {}
  evidence.activity = recentActivity;

  // 4. Lista scripts existentes (diz o que o sistema faz)
  const scripts = fs.readdirSync(ROOT)
    .filter(f => f.endsWith('.cjs') || f.endsWith('.ts') || f.endsWith('.tsx'))
    .join(', ');
  evidence.scripts = scripts;

  return evidence;
}

// ─────────────────────────────────────────────────────────────
// Gemma 4 analisa a empresa e gera o mapa de áreas + cargos
// ─────────────────────────────────────────────────────────────
async function gemma4AnalyzeCompany(evidence) {
  console.log('\n🧠 [Gemma 4] Analisando a empresa para mapear áreas e cargos necessários...');

  const prompt = `Você é um consultor sênior de estrutura organizacional e People & Culture.

Você recebeu acesso completo a uma empresa de tecnologia chamada "Flose Startup".
Seu objetivo é analisar tudo que a empresa faz e criar uma estrutura organizacional REAL e NECESSÁRIA — não genérica, não inventada. Baseada 100% nas evidências abaixo.

=== CÓDIGO DA EMPRESA (primeiras linhas dos arquivos principais) ===
${evidence.code.substring(0, 8000)}

=== PROBLEMAS REAIS NO BACKLOG (Jira) ===
${evidence.jira.substring(0, 3000)}

=== ATIVIDADE RECENTE DOS AGENTES ===
${evidence.activity.substring(0, 1500)}

=== SCRIPTS/SISTEMAS EM EXECUÇÃO ===
${evidence.scripts}

Com base exclusivamente nestas evidências, responda em JSON puro (sem markdown, sem texto extra):
{
  "company_summary": "O que esta empresa faz em 2-3 frases objetivas, baseado nos arquivos e problemas reais",
  "areas": [
    {
      "name": "Nome da Área",
      "purpose": "Para que serve esta área, baseado em problemas reais encontrados",
      "open_positions": [
        {
          "title": "Cargo exato",
          "level": "Estagiário | Júnior | Pleno | Sênior | Coordenador | Gerente | Diretor",
          "why_needed": "Por que este cargo é necessário baseado nos problemas/código acima",
          "skills_needed": "Habilidades específicas baseadas nos problemas reais",
          "priority": "alta | média | baixa"
        }
      ]
    }
  ]
}`;

  const raw = await gemma4(prompt);
  if (!raw) return null;

  try {
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (jsonMatch) return JSON.parse(jsonMatch[0]);
  } catch (e) {
    console.log('⚠️ [Gemma 4] Falha ao parsear JSON do mapa da empresa. Raw:', raw.substring(0, 200));
  }
  return null;
}

// ─────────────────────────────────────────────────────────────
// Gemma 4 cria perfil real do candidato para o cargo
// ─────────────────────────────────────────────────────────────
async function gemma4CreateCandidateProfile(position, area, companyContext) {
  console.log(`\n🧠 [Gemma 4] Criando perfil real para: ${position.title}...`);

  const prompt = `Você é um recrutador especialista da Flose Startup.

A empresa faz: ${companyContext}

Você precisa criar o perfil REAL de um candidato para a vaga:
- Cargo: ${position.title}
- Área: ${area.name}
- Nível: ${position.level}
- Por que foi criada: ${position.why_needed}
- Habilidades necessárias: ${position.skills_needed}

Crie um perfil de candidato com nome brasileiro realista e características ESPECÍFICAS para este cargo.
Responda em JSON puro (sem markdown):
{
  "name": "Nome Completo Brasileiro",
  "avatar": "um único emoji que representa bem este cargo",
  "advantage": "O que este profissional faz muito bem — específico para os problemas da empresa",
  "disadvantage": "Limitação real deste profissional no contexto desta empresa",
  "dilemma": "Dilema profissional real que este cargo enfrenta nesta empresa",
  "personality": "Como esta pessoa age no trabalho — específico e realista"
}`;

  const raw = await gemma4(prompt);
  if (!raw) return null;

  try {
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (jsonMatch) return JSON.parse(jsonMatch[0]);
  } catch (e) {}
  return null;
}

// ─────────────────────────────────────────────────────────────
// Cria card de contratação no Jira
// ─────────────────────────────────────────────────────────────
async function createHiringCardOnJira(position, area, epicMap) {
  const summary = `[Vaga] ${position.title} — ${area.name} (${position.level})`;
  const description = `🎯 POR QUE PRECISAMOS: ${position.why_needed}\n\n📋 SKILLS NECESSÁRIAS: ${position.skills_needed}\n\n🏢 ÁREA: ${area.name} — ${area.purpose}\n\n⚡ PRIORIDADE: ${position.priority}`;

  try {
    const body = {
      fields: {
        project: { key: 'KAN' },
        summary,
        description: {
          type: 'doc', version: 1,
          content: [{ type: 'paragraph', content: [{ text: description, type: 'text' }] }]
        },
        issuetype: { name: 'Task' }
      }
    };

    // Link to "Gestão de Pessoas" epic if it exists
    if (epicMap?.['Gestão de Pessoas']) {
      body.fields.parent = { key: epicMap['Gestão de Pessoas'] };
    }

    const res = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, body, { headers: getJiraAuthHeader() });
    return res.data.key;
  } catch (e) {
    console.error(`  ❌ Erro ao criar card no Jira: ${e.message}`);
    return null;
  }
}

// ─────────────────────────────────────────────────────────────
// CICLO PRINCIPAL
// ─────────────────────────────────────────────────────────────
async function runCompanyAnalysis() {
  console.log('\n════════════════════════════════════════════════════════');
  console.log('🏢 FLOSE STARTUP — ANÁLISE ORGANIZACIONAL VIA GEMMA 4');
  console.log('════════════════════════════════════════════════════════');

  // 1. Coletar evidências reais
  const evidence = await collectCompanyEvidence();

  // 2. Gemma 4 analisa e mapeia a empresa
  const companyMap = await gemma4AnalyzeCompany(evidence);
  if (!companyMap) {
    console.log('❌ [Gemma 4] Não conseguiu gerar mapa da empresa.');
    return;
  }

  console.log('\n📊 [Gemma 4] Mapa da empresa gerado:');
  console.log(`  Empresa: ${companyMap.company_summary}`);
  console.log(`  Áreas identificadas: ${companyMap.areas?.length || 0}`);
  companyMap.areas?.forEach(a => {
    console.log(`  └─ ${a.name} (${a.open_positions?.length || 0} vagas)`);
  });

  // Salvar mapa da empresa
  fs.writeFileSync(COMPANY_MAP_FILE, JSON.stringify(companyMap, null, 2), 'utf8');
  console.log('\n💾 Mapa da empresa salvo em company_map.json');

  // Notificar backend via activity log
  try {
    await axios.post('http://localhost:5001/api/activity', {
      agentId: 'gemma4_analyst',
      agentName: 'Gemma 4 (Analista Organizacional)',
      agentAvatar: '🧠',
      action: `Analisou o código, backlog e logs da empresa. Identificou ${companyMap.areas?.length} áreas e ${companyMap.areas?.reduce((s, a) => s + (a.open_positions?.length || 0), 0)} vagas necessárias. Empresa: ${companyMap.company_summary}`,
      ticketKey: '',
      ticketSummary: ''
    });
  } catch (e) {}

  // 3. Para cada área e cargo, Gemma 4 cria um candidato real e um card no Jira
  const agents = JSON.parse(fs.existsSync(AGENTS_FILE) ? fs.readFileSync(AGENTS_FILE, 'utf8') : '[]');
  const newAgents = [];
  const hiringCards = [];

  // Buscar epic map para linkar cards
  let epicMap = {};
  try {
    const epicRes = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: { jql: 'project = KAN AND issuetype = Epic', maxResults: 20, fields: 'summary' }
    });
    (epicRes.data?.issues || []).forEach(e => {
      epicMap[e.fields.summary] = e.key;
    });
  } catch (e) {}

  for (const area of (companyMap.areas || [])) {
    const highPriorityPositions = (area.open_positions || [])
      .filter(p => p.priority === 'alta' || p.priority === 'high')
      .slice(0, 2); // Max 2 high priority per area to avoid flooding

    for (const position of highPriorityPositions) {
      // Check if we already have an active agent for this role
      const roleExists = agents.find(a =>
        !a.fired &&
        a.role?.toLowerCase().includes(position.title.split(' ')[0].toLowerCase())
      );
      if (roleExists) {
        console.log(`  ✅ Já temos ${roleExists.name} para ${position.title}`);
        continue;
      }

      // Gemma 4 cria o perfil do candidato
      const profile = await gemma4CreateCandidateProfile(position, area, companyMap.company_summary);

      if (profile) {
        const agentId = `gemma_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
        const newAgent = {
          id: agentId,
          name: profile.name,
          role: position.title,
          level: position.level,
          avatar: profile.avatar || '👤',
          area: area.name,
          advantage: profile.advantage,
          disadvantage: profile.disadvantage,
          dilemma: profile.dilemma,
          personality: profile.personality,
          status: 'Aguardando Contratação',
          schedule: '09:00 - 18:00',
          fired: true, // starts as candidate, not hired yet
          hireLevel: position.level,
          whyNeeded: position.why_needed,
          feedbacks: []
        };

        newAgents.push(newAgent);
        console.log(`  👤 Candidato criado pelo Gemma 4: ${profile.name} (${position.title})`);

        // Log activity
        try {
          await axios.post('http://localhost:5001/api/activity', {
            agentId: 'gemma4_analyst',
            agentName: 'Gemma 4 (Analista Organizacional)',
            agentAvatar: '🧠',
            action: `Identificou necessidade de "${position.title}" na área ${area.name}: ${position.why_needed}. Criou candidato ${profile.name} no pool.`,
            ticketKey: '',
            ticketSummary: ''
          });
        } catch (e) {}
      }

      // Criar card de contratação no Jira
      const jiraKey = await createHiringCardOnJira(position, area, epicMap);
      if (jiraKey) {
        hiringCards.push({ key: jiraKey, position, area });
        console.log(`  📋 Card de vaga criado no Jira: ${jiraKey} — ${position.title}`);
      }

      // Rate limit — don't flood Gemma or Jira
      await new Promise(r => setTimeout(r, 1500));
    }
  }

  // 4. Salvar candidatos no pool de agentes
  if (newAgents.length > 0) {
    const allAgents = JSON.parse(fs.existsSync(AGENTS_FILE) ? fs.readFileSync(AGENTS_FILE, 'utf8') : '[]');
    const merged = [...allAgents, ...newAgents.filter(na =>
      !allAgents.find(a => a.name === na.name)
    )];
    fs.writeFileSync(AGENTS_FILE, JSON.stringify(merged, null, 2), 'utf8');
    console.log(`\n✅ ${newAgents.length} candidatos adicionados ao pool pelo Gemma 4.`);
  }

  console.log(`\n✅ Análise completa. ${hiringCards.length} vagas abertas no Jira.`);
  console.log('════════════════════════════════════════════════════════\n');

  return companyMap;
}

// ─────────────────────────────────────────────────────────────
// Export & startup
// ─────────────────────────────────────────────────────────────
function startCompanyAnalyst() {
  // Run once on startup (after 20s for backend to be ready)
  setTimeout(() => {
    runCompanyAnalysis();
  }, 20000);

  // Re-analyze every 30 minutes to adapt the org as the company evolves
  setInterval(runCompanyAnalysis, 30 * 60 * 1000);
}

module.exports = { startCompanyAnalyst, runCompanyAnalysis };

if (require.main === module) {
  runCompanyAnalysis();
}
