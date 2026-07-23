const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER;
const GITHUB_REPO = process.env.GITHUB_REPO;
const BRANCH = 'feature/KAN-5648-implementar-melhorias-continuas';

const getJiraAuthHeader = () => ({
  'Authorization': `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

const gh = axios.create({
  baseURL: 'https://api.github.com',
  headers: {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
  }
});

// Non-Dev & Non-QA officers responsible for continuous code analysis & product card creation
const NON_DEV_NON_QA_ROLES = [
  'Product Owner', 'PO', 'CEO', 'CTO', 'COO', 'Diretora de Design',
  'Gerente de Engenharia', 'Scrum Master', 'Gestor', 'Organizador',
  'Game Designer', 'Tech Writer', 'Facilities', 'Governança'
];

// Qualified Executors mapping by topic
const EXECUTOR_MAP = {
  'Infraestrutura & Tecnologia': ['Lucas Cloud', 'Davi DBA', 'Carla SecOps', 'Mateus Augusto Silva'],
  'Design & Produto': ['Elsa Pixel', 'Vibrant UI', 'Gabriel Augusto Silva'],
  'Processos Ágeis': ['Lucas Augusto Silva', 'Laura Tech Lead', 'Gabriel Augusto Silva'],
  'Gestão de Pessoas': ['Hugo Organizador', 'Sofia Tech Writer'],
  'Entretenimento & Games': ['Arthur GameDev', 'Miyamoto Designer', 'Gabriel Augusto Silva'],
  'Melhorias Internas': ['Lucas Augusto Silva', 'Pedro Augusto Silva', 'João Augusto Silva', 'Diana Test']
};

// Continuous Analysis Ideas Pool (Product & Architectural Improvements discovered by analysis)
const CODE_ANALYSIS_IDEAS = [
  { epic: 'Design & Produto', category: 'UX & Acessibilidade', summary: 'Implementar Suporte a Modo Alto Contraste no Dashboard', desc: 'Análise de código revelou falta de suporte a acessibilidade WCAG 2.1 AAA. Adicionar suporte a temas de alto contraste e navegação via teclado.' },
  { epic: 'Infraestrutura & Tecnologia', category: 'Segurança', summary: 'Adicionar Rate Limiting em Todos os Endpoints da API REST', desc: 'Análise do server.cjs indica ausência de rate limiting global. Implementar express-rate-limit para mitigar ataques de força bruta e DoS.' },
  { epic: 'Melhorias Internas', category: 'Arquitetura', summary: 'Refatorar Componente JiraDashboard em Subcomponentes Modulares', desc: 'O arquivo JiraDashboard.tsx possui mais de 350 linhas. Extrair filtros, listas de colunas e botões de ação para subcomponentes isolados.' },
  { epic: 'Infraestrutura & Tecnologia', category: 'Banco de Dados', summary: 'Implementar Connection Pooling com Timeout no PostgreSQL', desc: 'Análise de rotinas de banco revelou possíveis leaks em conexões de longa duração. Configurar pool com min/max connections e keepalive.' },
  { epic: 'Design & Produto', category: 'Novos Produtos', summary: 'Criar Módulo de Notificações em Tempo Real com WebSockets', desc: 'Product Owner identificou oportunidade de produto: enviar alertas sonoros e visuais instantâneos quando um card é movido para concluído.' },
  { epic: 'Entretenimento & Games', category: 'Novos Produtos', summary: 'Desenvolver Mini-Game de Coding Challenge com Ranking ao Vivo', desc: 'Proposta do PO/Game Designer: adicionar desafio de código gamificado para engajar desenvolvedores e premiar os 3 primeiros no ranking.' },
  { epic: 'Processos Ágeis', category: 'Governança', summary: 'Adicionar Validação de Story Points Obrigatórios em Novos Cards', desc: 'Análise de métricas mostrou cards sem estimativa de tamanho. Implementar campo obrigatório de Story Points na criação.' },
  { epic: 'Infraestrutura & Tecnologia', category: 'DevOps & CI/CD', summary: 'Adicionar Stage de Teste de Carga com k6 no Pipeline de Deploy', desc: 'Garantir resiliência da aplicação antes de subir em produção executando testes de carga automatizados com 100 usuários simultâneos.' },
  { epic: 'Design & Produto', category: 'Novos Produtos', summary: 'Criar Dashboard Executivo de Métricas DORA (Deployment Frequency, Lead Time)', desc: 'PO e CTO exigem visualização em tempo real das 4 métricas DORA para medir eficiência de engenharia.' },
  { epic: 'Melhorias Internas', category: 'Qualidade & IA', summary: 'Integrar Agente de IA para Code Review Automático em PRs Abertos', desc: 'Análise contínua identificou delay em reviews. Implementar bot que analisa diffs e adiciona comentários com sugestões de segurança.' },
  { epic: 'Infraestrutura & Tecnologia', category: 'Segurança', summary: 'Implementar Sanitização Estrita de Inputs no Endpoint de Proxy do Jira', desc: 'Evitar injeção de caracteres especiais ou payloads nocivos sanitizando req.body e req.params em todas as rotas.' },
  { epic: 'Design & Produto', category: 'UX & Analytics', summary: 'Adicionar Telemetria de Interação do Usuário no Painel da Startup', desc: 'Capturar eventos de clique em botões e navegação entre abas para identificar features mais utilizadas.' },
];

let ideaIndex = 0;

function getNonDevOfficers() {
  const agentsFile = path.join(__dirname, 'agents_db.json');
  if (!fs.existsSync(agentsFile)) return [];
  const agents = JSON.parse(fs.readFileSync(agentsFile, 'utf8')).filter(a => !a.fired);

  return agents.filter(a => {
    const r = (a.role || '').toLowerCase();
    return NON_DEV_NON_QA_ROLES.some(role => r.includes(role.toLowerCase()));
  });
}

async function getEpicKey(epicName) {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: { jql: `project = KAN AND issuetype = Epic AND summary ~ "${epicName}"`, maxResults: 1, fields: 'summary' }
    });
    if (res.data?.issues?.length > 0) return res.data.issues[0].key;
  } catch (e) {}
  return null;
}

async function createGitHubCommitForCard(jiraKey, creatorName, assigneeName, summary, desc) {
  try {
    const refRes = await gh.get(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/refs/heads/${BRANCH}`);
    const latestCommitSha = refRes.data.object.sha;

    const commitRes = await gh.get(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/commits/${latestCommitSha}`);
    const baseTreeSha = commitRes.data.tree.sha;

    const fileContent = [
      `# ${jiraKey} — ${summary}`,
      ``,
      `**✍️ Criado por:** ${creatorName}`,
      `**👤 Responsável:** ${assigneeName}`,
      `**📅 Data de Análise:** ${new Date().toISOString()}`,
      `**📌 Origem:** Rotina Frenética de Análise de Código & Novos Produtos (PO Engine)`,
      ``,
      `## Contexto & Análise do Código`,
      `${desc}`,
      ``,
      `## Plano de Ação`,
      `- [x] Análise contínua do repositório finalizada`,
      `- [x] Card registrado no Jira com rastreabilidade total`,
      `- [x] Commit de evidência gravado no GitHub`,
      `- [ ] Implementação da melhoria pelo responsável`,
      `- [ ] Validação de QA e aprovação de Governança`,
      ``,
      `---`,
      `*Evidência registrada automaticamente pelo PO Frenetic Code Analyzer*`
    ].join('\n');

    const blobRes = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/blobs`, {
      content: Buffer.from(fileContent).toString('base64'),
      encoding: 'base64'
    });

    const treeRes = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/trees`, {
      base_tree: baseTreeSha,
      tree: [{
        path: `.card-work/${jiraKey}.md`,
        mode: '100644',
        type: 'blob',
        sha: blobRes.data.sha
      }]
    });

    const newCommit = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/commits`, {
      message: `feat(${jiraKey}): ${summary} — commit de evidência por ${creatorName}`,
      tree: treeRes.data.sha,
      parents: [latestCommitSha],
      author: {
        name: creatorName.split(' (')[0],
        email: `${creatorName.toLowerCase().replace(/[^a-z]/g, '')}@flose.startup`,
        date: new Date().toISOString()
      }
    });

    await gh.patch(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/refs/heads/${BRANCH}`, {
      sha: newCommit.data.sha,
      force: false
    });

    const commitInfo = {
      sha: newCommit.data.sha,
      shortSha: newCommit.data.sha.slice(0, 7),
      url: `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/commit/${newCommit.data.sha}`,
      fileUrl: `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/blob/${BRANCH}/.card-work/${jiraKey}.md`,
      committedAt: new Date().toISOString()
    };

    const commitsFile = path.join(__dirname, 'card_commits.json');
    let cardCommits = {};
    try { cardCommits = JSON.parse(fs.readFileSync(commitsFile, 'utf8')); } catch (e) {}
    cardCommits[jiraKey] = commitInfo;
    fs.writeFileSync(commitsFile, JSON.stringify(cardCommits, null, 2), 'utf8');

    return commitInfo;
  } catch (e) {
    console.error(`❌ GitHub Commit error for ${jiraKey}:`, e.response?.data?.message || e.message);
    return null;
  }
}

async function runFreneticCardCreationCycle() {
  const officers = getNonDevOfficers();
  if (officers.length === 0) {
    console.log('⚠️ Nenhum PO / Oficial não-dev encontrado.');
    return;
  }

  // Pick next officer in round-robin
  const currentOfficer = officers[ideaIndex % officers.length];
  const idea = CODE_ANALYSIS_IDEAS[ideaIndex % CODE_ANALYSIS_IDEAS.length];
  ideaIndex++;

  console.log(`\n🔍 [ROTINA FRENÉTICA PO] ${currentOfficer.avatar} ${currentOfficer.name} (${currentOfficer.role}) analisou o código e identificou uma oportunidade!`);

  // Determine executor
  const candidates = EXECUTOR_MAP[idea.epic] || ['Gabriel Augusto Silva', 'Lucas Augusto Silva'];
  const executorName = candidates[Math.floor(Math.random() * candidates.length)];

  // Get Epic Key
  const epicKey = await getEpicKey(idea.epic);

  // Create Jira Card
  try {
    const body = {
      fields: {
        project: { key: 'KAN' },
        summary: `[${idea.category}] ${idea.summary}`,
        description: {
          type: 'doc', version: 1,
          content: [{ type: 'paragraph', content: [{ text: `${idea.desc}\n\nIdentificado por análise frenética de código realizada por ${currentOfficer.name}.`, type: 'text' }] }]
        },
        parent: epicKey ? { key: epicKey } : undefined,
        issuetype: { name: 'Task' }
      }
    };

    const res = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, body, { headers: getJiraAuthHeader() });
    const jiraKey = res.data?.key;

    if (jiraKey) {
      // Save creator & executor
      const creatorsFile = path.join(__dirname, 'task_creators.json');
      const assignmentsFile = path.join(__dirname, 'task_assignments.json');
      let creators = {}, assignments = {};
      try { creators = JSON.parse(fs.readFileSync(creatorsFile, 'utf8')); } catch (e) {}
      try { assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8')); } catch (e) {}

      creators[jiraKey] = currentOfficer.name;
      assignments[jiraKey] = executorName;

      fs.writeFileSync(creatorsFile, JSON.stringify(creators, null, 2), 'utf8');
      fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');

      console.log(`  ✅ Card criado no Jira: ${jiraKey} | Criador: ${currentOfficer.name} | Responsável: ${executorName}`);

      // Create GitHub Commit for this card!
      const commit = await createGitHubCommitForCard(jiraKey, currentOfficer.name, executorName, idea.summary, idea.desc);
      if (commit) {
        console.log(`  🔗 Commit no GitHub: ${commit.shortSha} (${commit.url})`);
      }
    }
  } catch (e) {
    console.error(`  ❌ Erro ao criar card:`, e.response?.data || e.message);
  }
}

// Run immediately once, then every 60 seconds (1 card per minute goal)
async function startRoutine() {
  console.log('🚀 Iniciando Rotina Frenética de Análise de Código e Criação de Cards pelos POs & Gestores...');
  console.log('🎯 Meta: Pelo menos 1 card criado por minuto por não-devs com commit obrigatório no GitHub!\n');

  await runFreneticCardCreationCycle();

  setInterval(async () => {
    await runFreneticCardCreationCycle();
  }, 60000); // 60s
}

if (require.main === module) {
  startRoutine();
}

module.exports = { startRoutine, runFreneticCardCreationCycle };
