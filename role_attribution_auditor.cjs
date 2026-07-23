const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const JIRA_HOST = process.env.JIRA_HOST;
const JIRA_USER = process.env.JIRA_USER;
const JIRA_TOKEN = process.env.JIRA_TOKEN;
const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

const getJiraAuthHeader = () => ({
  'Authorization': `Basic ${Buffer.from(`${JIRA_USER}:${JIRA_TOKEN}`).toString('base64')}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

async function logActivityToBackend(agentId, agentName, agentAvatar, action, ticketKey, ticketSummary) {
  try {
    await axios.post('http://localhost:5001/api/activity', {
      agentId, agentName, agentAvatar, action, ticketKey, ticketSummary
    });
  } catch (e) {
    // backend down or starting
  }
}

// Qualified Executor Lists per area to reassign cards when mismatch occurs
const EXECUTOR_MAP = {
  'infra': ['Lucas Cloud', 'Davi DBA', 'Carla SecOps', 'Mateus Augusto Silva'],
  'design': ['Elsa Pixel', 'Vibrant UI', 'Gabriel Augusto Silva'],
  'dev': ['David Dev', 'Mariana Python', 'Arthur GameDev', 'Mateus Augusto Silva', 'Pedro Augusto Silva'],
  'qa': ['Juliana QA Sênior', 'Marcos QA Lead', 'Diana Test']
};

async function postJiraComment(issueKey, commentText) {
  try {
    await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/comment`, {
      body: {
        type: 'doc', version: 1,
        content: [{
          type: 'paragraph',
          content: [{ text: commentText, type: 'text' }]
        }]
      }
    }, { headers: getJiraAuthHeader() });
  } catch (e) {
    console.error(`Error posting Jira comment for ${issueKey}:`, e.message);
  }
}

async function reassignJiraIssue(issueKey, newExecutorName) {
  try {
    // Save to task_assignments.json first
    const assignmentsFile = path.join(__dirname, 'task_assignments.json');
    let assignments = {};
    if (fs.existsSync(assignmentsFile)) {
      try { assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8')); } catch (e) {}
    }
    assignments[issueKey] = newExecutorName;
    fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');

    // Add Jira comment
    await postJiraComment(issueKey, `⚠️ [AUDITORIA AUTOMÁTICA DE ATRIBUIÇÕES] Esta tarefa foi identificada como fora da alocação de cargos do executor anterior. Reatribuída automaticamente para ${newExecutorName}.`);
    console.log(`  🔄 Card ${issueKey} reatribuído para ${newExecutorName} com sucesso.`);
  } catch (e) {
    console.error(`Error reassigning Jira issue ${issueKey}:`, e.message);
  }
}

// Check role boundary infraction
function checkInfraction(role, summaryText) {
  const cleanSummary = (summaryText || '').toLowerCase();
  const cleanRole = (role || '').toLowerCase();

  // 1. Non-Dev roles (PMs, Scrum Master, CEO, COO, facilities, HR) should NOT be assignees
  const nonDevRoles = ['owner', 'pm', 'ceo', 'cto', 'coo', 'design manager', 'scrum master', 'facilities', 'writer', 'governance', 'organizador'];
  if (nonDevRoles.some(r => cleanRole.includes(r))) {
    return { inf: true, reason: 'Gestores e cargos administrativos não devem executar tarefas de desenvolvimento/código diretamente.', type: 'gestao' };
  }

  // 2. Designer/UX should not work on backend, cloud, dba, or security
  if (cleanRole.includes('design') || cleanRole.includes('pixel') || cleanRole.includes('ux') || cleanRole.includes('ui')) {
    const backendKeywords = ['database', 'sql', 'query', 'migration', 'docker', 'kubernetes', 'ci/cd', 'aws', 'backend', 'api', 'server', 'monolito', 'endpoint'];
    if (backendKeywords.some(kw => cleanSummary.includes(kw))) {
      return { inf: true, reason: 'Designers não possuem atribuição para trabalhar em tarefas de Banco de Dados, APIs, Servidores ou Cloud.', type: 'infra' };
    }
  }

  // 3. DBA should not work on UI, UX, screens, css, design systems
  if (cleanRole.includes('dba') || cleanRole.includes('database')) {
    const frontendKeywords = ['layout', 'css', 'pixel', 'design system', 'componente', 'tela', 'mockup', 'frontend', 'ui', 'ux', 'cor', 'font', 'alinhamento'];
    if (frontendKeywords.some(kw => cleanSummary.includes(kw))) {
      return { inf: true, reason: 'DBAs não possuem atribuição para trabalhar em tarefas de Design, Frontend, Layouts ou Experiência de Usuário.', type: 'design' };
    }
  }

  // 4. SecOps should not work on design or basic frontend layouts
  if (cleanRole.includes('secops') || cleanRole.includes('segurança')) {
    const designKeywords = ['layout', 'css', 'design system', 'componente', 'tela', 'mockup', 'ux', 'ui'];
    if (designKeywords.some(kw => cleanSummary.includes(kw))) {
      return { inf: true, reason: 'Profissionais de SecOps não possuem atribuição para trabalhar em Design de Telas ou UI Layouts.', type: 'design' };
    }
  }

  // 5. QA should not write production feature code directly
  if (cleanRole.includes('qa') || cleanRole.includes('qualidade') || cleanRole.includes('teste')) {
    const featureKeywords = ['implementar funcionalidade', 'criar tela', 'novo modulo', 'desenvolver backend', 'criar api'];
    if (featureKeywords.some(kw => cleanSummary.includes(kw))) {
      return { inf: true, reason: 'Profissionais de QA não devem escrever códigos de produção ou implementar features comerciais diretamente.', type: 'dev' };
    }
  }

  return { inf: false };
}

async function runGovernanceAudit() {
  console.log('\n🔍 [AUDITORIA AUTOMÁTICA DE ATRIBUIÇÕES] Iniciando escaneamento de alocação de cargos...');
  
  if (!fs.existsSync(AGENTS_FILE)) return;
  let agents = [];
  try { agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8')); } catch (e) { return; }

  const activeAgents = agents.filter(a => !a.fired);

  try {
    // 1. Fetch active issues from Jira
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/search/jql`, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN AND status != Done AND status != Concluído AND status != Resolvido AND status != Fechado',
        maxResults: 50,
        fields: 'summary,status'
      }
    });

    const issues = res.data?.issues || [];
    
    // Load current assignments
    const assignmentsFile = path.join(__dirname, 'task_assignments.json');
    let assignments = {};
    if (fs.existsSync(assignmentsFile)) {
      try { assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8')); } catch (e) {}
    }

    let databaseUpdated = false;

    for (const issue of issues) {
      const summary = issue.fields?.summary || '';
      const executorName = assignments[issue.key] || 'David Dev';
      
      // Find matching agent
      const agent = activeAgents.find(a => a.name.includes(executorName) || executorName.includes(a.name));
      if (!agent) continue;

      // Check for infraction
      const auditResult = checkInfraction(agent.role, summary);
      if (auditResult.inf) {
        console.log(`⚠️ [INFRAÇÃO DE ATRIBUIÇÃO] ${agent.name} (${agent.role}) está alocado no card ${issue.key}: "${summary}"`);
        console.log(`   Motivo: ${auditResult.reason}`);

        // 1. Deduct points & add Warning to agent in database
        const feedbackEntry = {
          id: 'warn_' + Math.random().toString(36).substring(2, 9),
          timestamp: new Date().toISOString(),
          type: 'advertencia',
          text: `Governança cobrou ${agent.name} (${agent.role}) por atuar no card ${issue.key} ("${summary}"). Motivo: ${auditResult.reason}`,
          impact: 'Conformidade de Cargo',
          sprintTicket: issue.key
        };
        
        agent.feedbacks = agent.feedbacks || [];
        agent.feedbacks.unshift(feedbackEntry);
        agent.totalScore = Math.max(0, (agent.totalScore || 0) - 15); // penalize 15 points
        agent.penalty = `Advertência de Atribuição: ${auditResult.reason}`;
        databaseUpdated = true;

        // Log visual activity to live stream
        await logActivityToBackend(
          'governança', 'Arthur Auditor', '⚖️',
          `Governança cobrou ${agent.name}: "${auditResult.reason}" (Card ${issue.key} será reatribuído).`,
          issue.key,
          summary
        );

        // 2. Automatically select a qualified executor
        const pool = EXECUTOR_MAP[auditResult.type] || EXECUTOR_MAP.dev;
        const newExecutor = pool.find(name => activeAgents.some(a => a.name === name)) || 'David Dev';

        // 3. Reassign card and post comment
        await reassignJiraIssue(issue.key, newExecutor);
      }
    }

    // Mentorship & Promotion Auditor Check
    let agentsUpdated = false;

    // A. Check for Promotions first
    const activeJuniors = agents.filter(a => !a.fired && (a.level === 'Júnior' || a.level === 'Estagiário'));
    const activeManagers = agents.filter(a => !a.fired && ((a.role || '').includes('Gerente') || (a.role || '').includes('Lead') || (a.role || '').includes('Organizador')));

    for (const junior of activeJuniors) {
      if ((junior.totalScore || 0) >= 75) {
        const oldRole = junior.role;
        const oldLevel = junior.level;
        
        let newLevel = 'Júnior';
        let newRole = 'Desenvolvedor Júnior';
        if (oldLevel === 'Júnior') {
          newLevel = 'Analista SR';
          newRole = oldRole.replace('Júnior', 'Sênior');
        } else if (oldLevel === 'Estagiário') {
          newLevel = 'Júnior';
          newRole = oldRole.replace('Estagiário', 'Júnior');
        }

        junior.level = newLevel;
        junior.role = newRole;
        junior.totalScore = 50; // Reset score for new level
        agentsUpdated = true;

        // Find manager for the area
        const manager = activeManagers.find(m => m.area === junior.area) || activeManagers[0];
        const managerName = manager ? manager.name : 'Bob Delivery';
        const managerAvatar = manager ? manager.avatar : '⚙️';
        const managerRole = manager ? manager.role : 'Gerente de Engenharia';

        const promoMsg = `📈 [PROMOÇÃO] ${managerName} (${managerRole}) promoveu ${junior.name} de ${oldRole} para ${newRole} devido ao excelente score de performance de ${junior.totalScore}!`;
        console.log(promoMsg);

        // Track promotion on manager
        if (manager) {
          manager.promotionsGiven = (manager.promotionsGiven || 0) + 1;
        }

        await logActivityToBackend(
          manager ? manager.id : 'ceo',
          managerName,
          managerAvatar,
          promoMsg,
          '',
          ''
        );
      }
    }

    // B. Check if Managers are teaching and promoting.
    // If a junior has a score < 35, the manager of their area gets a penalty for lack of mentorship/teaching!
    for (const junior of activeJuniors) {
      if ((junior.totalScore || 0) < 35) {
        const manager = activeManagers.find(m => m.area === junior.area);
        if (manager) {
          console.log(`⚠️ [NEGLIGÊNCIA EDUCACIONAL] Junior/Estagiário ${junior.name} está com score baixo (${junior.totalScore}). Gestor ${manager.name} cobrado.`);
          
          manager.feedbacks = manager.feedbacks || [];
          const managerWarns = manager.feedbacks.filter(f => f.type === 'advertencia' && (f.text || '').includes('Mentoria')).length;

          if (managerWarns >= 2) {
            // FIRE MANAGER!
            manager.fired = true;
            manager.status = 'Desligado';
            manager.firedReason = `Demitido por negligenciar o treinamento de sua equipe de juniores e estagiários (Treinado ${junior.name} com score crítico).`;
            agentsUpdated = true;

            const fireMsg = `⚖️ Arthur de Flose (Diretor de Governança) demitiu o gestor ${manager.name} (${manager.role}) por descumprir a regra de ensino e promoção de juniores.`;
            console.log(fireMsg);

            await logActivityToBackend(
              'governança', 'Arthur de Flose', '⚖️',
              fireMsg,
              '',
              ''
            );
          } else {
            // Apply warning
            const warnEntry = {
              id: 'mentorship_warn_' + Math.random().toString(36).substring(2, 9),
              timestamp: new Date().toISOString(),
              type: 'advertencia',
              text: `Negligência de Mentoria: Seu treinado ${junior.name} está com score crítico de ${junior.totalScore}. Ensine-o e promova-o ou será desligado!`,
              impact: 'Gestão de Pessoas'
            };
            manager.feedbacks.unshift(warnEntry);
            manager.totalScore = Math.max(0, (manager.totalScore || 0) - 20);
            agentsUpdated = true;

            const warningMsg = `⚖️ Arthur de Flose deu advertência de mentoria para ${manager.name} (${manager.role}) devido ao baixo rendimento do treinado ${junior.name}.`;
            console.log(warningMsg);

            await logActivityToBackend(
              'governança', 'Arthur de Flose', '⚖️',
              warningMsg,
              '',
              ''
            );
          }
        }
      }
    }

    if (databaseUpdated || agentsUpdated) {
      fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
    }

  } catch (e) {
    console.error('Error running governance role audit:', e.message);
  }
}

// Export functions to trigger automatically
module.exports = { runGovernanceAudit };

if (require.main === module) {
  runGovernanceAudit();
}
