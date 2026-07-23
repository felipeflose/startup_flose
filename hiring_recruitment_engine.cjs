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
  } catch (e) {}
}

async function callGemma4(systemPrompt, userPrompt) {
  const models = ['gemma4-fast:latest', 'gemma4-prod:latest', 'gemma4:latest'];
  for (const model of models) {
    try {
      const response = await axios.post('http://localhost:11434/api/generate', {
        model,
        prompt: `${systemPrompt}\n\nUser: ${userPrompt}\nAssistant:`,
        stream: false,
        options: { temperature: 0.7 }
      }, { timeout: 120000 });
      return response.data.response;
    } catch (e) {
      console.log(`⚠️ Model ${model} failed in Recruitment Engine: ${e.message}`);
    }
  }
  return null;
}

// Map technical epics or summaries to candidate area keywords
function getAreaForSummary(summary) {
  const s = summary.toLowerCase();
  if (s.includes('qa') || s.includes('test') || s.includes('qualidade') || s.includes('homolog')) return 'qa';
  if (s.includes('layout') || s.includes('design') || s.includes('ui') || s.includes('ux') || s.includes('tela') || s.includes('css')) return 'design';
  return 'dev';
}

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
    console.error(`Error posting comment on ${issueKey}:`, e.message);
  }
}

async function transitionJiraIssue(issueKey, transitionName) {
  try {
    const res = await axios.get(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, { headers: getJiraAuthHeader() });
    const trans = res.data?.transitions || [];
    const target = trans.find(t => t.name.toLowerCase().includes(transitionName.toLowerCase()));
    if (target) {
      await axios.post(`${JIRA_HOST}/rest/api/3/issue/${issueKey}/transitions`, {
        transition: { id: target.id }
      }, { headers: getJiraAuthHeader() });
      console.log(`  ⚙️ transitioned ${issueKey} to '${transitionName}'`);
    }
  } catch (e) {
    console.error(`Error transitioning ${issueKey}:`, e.message);
  }
}

function ensureAgentIsHiredHierarchically(agentName) {
  if (!fs.existsSync(AGENTS_FILE)) return;
  const agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
  const agent = agents.find(a => a.name === agentName);
  if (!agent) return;

  if (!agent.fired) return; // already active

  const area = agent.area || '';
  let director = agents.find(a => a.id === 'cto');
  let manager = agents.find(a => a.role && a.role.includes('Gerente de Engenharia'));

  if (area.includes('Produto') || area.includes('Design')) {
    director = agents.find(a => a.role && a.role.includes('Diretora de Design'));
    manager = agents.find(a => a.role && (a.role.includes('Product Manager') || a.role.includes('PM')));
  } else if (area.includes('Qualidade') || area.includes('RH')) {
    director = agents.find(a => a.id === 'coo');
    manager = agents.find(a => a.role && (a.role.includes('QA Lead') || a.role.includes('Organizador')));
  }

  const activateAgent = (target, hiredBy) => {
    if (target && target.fired) {
      target.fired = false;
      target.status = 'Disponível';
      target.totalScore = 50;
      const logText = `${hiredBy.avatar} ${hiredBy.name} (${hiredBy.role}) contratou o colaborador ${target.name} (${target.role}) para compor a equipe.`;
      console.log(`[RECRUTAMENTO HIERÁRQUICO] ${logText}`);
      logActivityToBackend(hiredBy.id || 'recruiter', hiredBy.name, hiredBy.avatar, logText, '', '');
    }
  };

  const ceo = agents.find(a => a.id === 'felipe_intern') || agents.find(a => a.id === 'ceo');

  if (director && director.fired) activateAgent(director, ceo);
  if (manager && manager.fired) {
    const recruiter = (director && !director.fired) ? director : ceo;
    activateAgent(manager, recruiter);
  }

  const finalRecruiter = (manager && !manager.fired) ? manager : (director && !director.fired) ? director : ceo;
  activateAgent(agent, finalRecruiter);

  fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
}

async function runRecruitmentEngineCycle() {
  console.log('🤖 [Recruitment & Selection Engine] Analisando backlog de tickets para identificar necessidades de contratação...');
  
  try {
    // 1. Fetch active issues from Jira without indexing lags
    const searchUrl = `${JIRA_HOST}/rest/api/3/search/jql`;
    const res = await axios.get(searchUrl, {
      headers: getJiraAuthHeader(),
      params: {
        jql: 'project = KAN AND status in ("To Do", "A Fazer", "Backlog", "Backlog de Melhorias")',
        maxResults: 30,
        fields: 'summary,description,assignee'
      }
    });

    const issues = res.data?.issues || [];
    if (issues.length === 0) {
      console.log('🤖 [Recruitment & Selection Engine] Nenhum card técnico pendente no backlog.');
      return;
    }

    // Load assignments and database
    const assignmentsFile = path.join(__dirname, 'task_assignments.json');
    let assignments = {};
    if (fs.existsSync(assignmentsFile)) {
      try { assignments = JSON.parse(fs.readFileSync(assignmentsFile, 'utf8')); } catch (e) {}
    }

    const agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));

    for (const issue of issues) {
      const summary = issue.fields?.summary || '';
      const issueKey = issue.key;

      if (summary.includes('[Recrutamento]')) continue;

      const assigneeName = assignments[issueKey];
      const agent = agents.find(a => a.name === assigneeName);

      // If there is no assignee, or the assignee is fired, we need to hire!
      if (!assigneeName || (agent && agent.fired)) {
        console.log(`🤖 [Recruitment & Selection Engine] Card ${issueKey} ("${summary}") precisa de executor qualificado ativo.`);

        // Check if there is already a recruitment card in Jira
        const checkRecruitment = await axios.get(searchUrl, {
          headers: getJiraAuthHeader(),
          params: {
            jql: `project = KAN AND summary ~ "${issueKey}" AND summary ~ "[Recrutamento]"`,
            maxResults: 1
          }
        });

        const recruitmentIssue = checkRecruitment.data?.issues?.[0];

        if (!recruitmentIssue) {
          // A. Create the Recruitment Jira Card
          console.log(`🤖 [Recruitment & Selection Engine] Criando Jira Card de Recrutamento para ${issueKey}...`);
          
          const recruitSummary = `[Recrutamento] Contratação para ${issueKey}: "${summary.substring(0, 40)}..."`;
          const recruitDesc = `Análise de Backlog efetuada pelo comitê. Necessidade de contratar desenvolvedor qualificado para a tarefa técnica ${issueKey}.\n\nDemanda original: "${summary}"`;

          const createBody = {
            fields: {
              project: { key: 'KAN' },
              summary: recruitSummary,
              description: {
                type: 'doc', version: 1,
                content: [{
                  type: 'paragraph',
                  content: [{ text: recruitDesc, type: 'text' }]
                }]
              },
              issuetype: { name: 'Task' }
            }
          };

          try {
            const createRes = await axios.post(`${JIRA_HOST}/rest/api/3/issue`, createBody, { headers: getJiraAuthHeader() });
            const recruitKey = createRes.data.key;
            console.log(`  ✅ Jira Card de Recrutamento Criado: ${recruitKey}`);

            await logActivityToBackend(
              'felipe_intern', 'Felipe Viana Flose', '👑',
              `Identificou a carência de pessoal no backlog para ${issueKey} e abriu o processo seletivo ${recruitKey} no Jira.`,
              recruitKey,
              recruitSummary
            );
          } catch (err) {
            console.error('Error creating recruitment card:', err.message);
          }

        } else if (recruitmentIssue.fields?.status?.name !== 'Done' && recruitmentIssue.fields?.status?.name !== 'Concluído') {
          // B. A recruitment card exists! Let's run the Interview & Selection Process in the Chamber!
          const recruitKey = recruitmentIssue.key;
          console.log(`🤖 [Recruitment Debug] recruitmentIssue:`, JSON.stringify(recruitmentIssue));
          console.log(`🤖 [Recruitment & Selection Engine] Iniciando processo de Entrevistas no Chamber para ${recruitKey}...`);

          const area = getAreaForSummary(summary);
          const roleKeywords = {
            dev: ['Frontend', 'Backend', 'DevOps', 'DBA', 'SecOps', 'Developer', 'Desenvolvedor'],
            design: ['Designer', 'UX', 'UI', 'Design'],
            qa: ['QA', 'Test', 'Qualidade', 'Garantia']
          };

          const keywords = roleKeywords[area];
          const candidatesPool = agents.filter(a => a.fired && keywords.some(k => (a.role || '').toLowerCase().includes(k.toLowerCase())));

          if (candidatesPool.length < 2) {
            console.log(`🤖 [Recruitment & Selection Engine] Poucos candidatos demitidos da área ${area}. Buscando qualquer demitido...`);
            candidatesPool.push(...agents.filter(a => a.fired && a.id !== 'ceo'));
          }

          if (candidatesPool.length === 0) {
            console.log('🤖 [Recruitment & Selection Engine] Nenhum candidato disponível no pool.');
            continue;
          }

          // Pick 2 candidates to evaluate
          const cand1 = candidatesPool[0];
          const cand2 = candidatesPool[1] || cand1;

          console.log(`👥 Entrevistando Candidato 1: ${cand1.name} (${cand1.role}) vs Candidato 2: ${cand2.name} (${cand2.role || 'N/A'})`);

          // Call Gemma 4 to simulate the interview debate
          const systemPrompt = `Você é o mediador e redator da Ata da Entrevista de Seleção da Flose Startup.
O comitê é composto por:
1. Felipe Viana Flose (Dono & CEO) 👑
2. Gemma Tech (CTO) 💻
3. Hugo Organizador (Gerente de RH) 👔

Vaga aberta para atuar no ticket técnico: "${summary}"
Candidato 1: ${cand1.name} (${cand1.role}) - Pontos fortes: ${cand1.advantage || 'N/A'}. Limitação: ${cand1.disadvantage || 'N/A'}.
Candidato 2: ${cand2.name} (${cand2.role}) - Pontos fortes: ${cand2.advantage || 'N/A'}. Limitação: ${cand2.disadvantage || 'N/A'}.

Escreva um relato detalhado da entrevista de seleção no Chamber, contendo:
- A pergunta comportamental feita por Hugo (RH).
- O teste prático ou pergunta técnica aplicada por Gemma Tech (CTO).
- O feedback estratégico e a escolha decisiva feita por Felipe Viana Flose (Dono & CEO).
- O vencedor definitivo da vaga (que deve ser exatamente ou "${cand1.name}" ou "${cand2.name}").

O texto deve ser redigido em português, de forma profissional, direta e em formato de diálogo ou ata de decisão do comitê.`;

          const debateText = await callGemma4(systemPrompt, 'Realize o debate e declare o vencedor final para contratação.');

          if (debateText) {
            console.log(`  🧠 Entrevista concluída via Gemma 4. Declarando vencedor...`);

            // Determine winner by searching for their name in the LLM response
            let winner = cand1;
            if (debateText.includes(cand2.name)) {
              winner = cand2;
            }

            // 1. Post the interview transcript as a comment on the Recruitment Jira Card
            await postJiraComment(recruitKey, `✍️ [ATA DE ENTREVISTA DE SELEÇÃO]\n\n${debateText}`);

            // 2. Hire the winner hierarchically!
            ensureAgentIsHiredHierarchically(winner.name);

            // Hire corresponding Junior/Intern if Senior Dev is hired (Mentorship policy)
            if (area === 'dev') {
              const freshAgents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
              const juniorOrIntern = freshAgents.find(a => a.fired && (a.level === 'Júnior' || a.level === 'Estagiário'));
              if (juniorOrIntern) {
                console.log(`[RECRUTAMENTO MENTORIA] Contratando Júnior ${juniorOrIntern.name} para pareamento.`);
                ensureAgentIsHiredHierarchically(juniorOrIntern.name);
              }
            }

            // 3. Move Recruitment Card to Done
            await transitionJiraIssue(recruitKey, 'Done');
            await transitionJiraIssue(recruitKey, 'Concluído');

            // 4. Assign the original technical card to the hired candidate and transition it to To Do
            assignments[issueKey] = winner.name;
            fs.writeFileSync(assignmentsFile, JSON.stringify(assignments, null, 2), 'utf8');

            await postJiraComment(issueKey, `✅ [RECRUTAMENTO CONCLUÍDO] Vaga preenchida por ${winner.name} (${winner.role}) após processo seletivo conduzido sob a liderança do Dono Felipe Viana Flose no Chamber.`);
            await transitionJiraIssue(issueKey, 'To Do');
            await transitionJiraIssue(issueKey, 'A Fazer');

            await logActivityToBackend(
              'felipe_intern', 'Felipe Viana Flose', '👑',
              `Entrevistou os candidatos no Chamber e contratou ${winner.name} (${winner.role}) para o card ${issueKey}.`,
              issueKey,
              summary
            );

            console.log(`  🎉 Recrutamento finalizado. ${winner.name} contratado para atuar no card ${issueKey}.`);
          } else {
            console.log('⚠️ Falha ao obter transcrição da entrevista da IA.');
          }
        }
      }
    }

  } catch (e) {
    console.error('Error running recruitment engine cycle:', e.message);
  }
}

function startRecruitmentRoutine() {
  // Run on startup
  setTimeout(() => {
    runRecruitmentEngineCycle();
  }, 10000);

  // Run every 60 seconds
  setInterval(runRecruitmentEngineCycle, 60000);
}

module.exports = { startRecruitmentRoutine };

if (require.main === module) {
  startRecruitmentRoutine();
}
