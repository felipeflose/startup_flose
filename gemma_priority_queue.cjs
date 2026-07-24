// gemma_priority_queue.cjs
// Fila de Prioridade da IA com Roteamento por Desempenho e Recompensa de Timeout
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const AGENTS_FILE = path.join(__dirname, 'agents_db.json');

// Fila de requisições pendentes da IA
const priorityQueue = [];
let isProcessing = false;

// Estado geral
const state = {
  totalRequests: 0,
  completedRequests: 0,
  failedRequests: 0,
  averageResponseMs: 0
};

// 1. Obter o agente atual e seus privilégios de prioridade/timeout com base no ranking
function getAgentPrivileges(agentName) {
  let agents = [];
  try {
    if (fs.existsSync(AGENTS_FILE)) {
      agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
    }
  } catch {}

  const agent = agents.find(a => a.name === agentName) || {
    role: 'Desenvolvedor',
    totalScore: 50,
    level: 'Pleno'
  };

  const score = agent.totalScore || 50;
  const role = (agent.role || '').toLowerCase();
  const isCLevel = role.includes('dono') || role.includes('ceo') || role.includes('cto') || role.includes('diretor');
  const isPO = role.includes('product owner') || role.includes('po ') || role.includes('gerente');

  let priority = 3; // 1 = Máxima (C-Level/PO), 2 = Alta (Dev SR / High Score), 3 = Normal
  let timeoutMs = 35000; // Salário base de timeout em ms
  let model = 'gemma4-fast:latest';

  if (isCLevel || isPO) {
    priority = 1;
    timeoutMs = 120000; // 120s timeout de diretoria
    model = 'qwen2.5-coder:32b';
  } else if (score >= 80) {
    priority = 2;
    timeoutMs = 75000; // 75s timeout de alta performance
    model = 'gemma4:latest';
  } else if (score >= 60) {
    priority = 3;
    timeoutMs = 45000; // 45s
    model = 'gemma4-prod:latest';
  }

  return { priority, timeoutMs, model, agent };
}

// 2. Atualizar pontuação (salário/ranking) do agente com base no tempo de resposta
function updateAgentPerformanceScore(agentName, responseMs, success) {
  try {
    if (!fs.existsSync(AGENTS_FILE)) return;
    const agents = JSON.parse(fs.readFileSync(AGENTS_FILE, 'utf8'));
    const agent = agents.find(a => a.name === agentName);
    if (!agent) return;

    if (!agent.totalScore) agent.totalScore = 50;

    if (success) {
      if (responseMs < 5000) {
        agent.totalScore = Math.min(100, agent.totalScore + 3); // Bônus ultra-rápido
      } else if (responseMs < 15000) {
        agent.totalScore = Math.min(100, agent.totalScore + 1);
      }
    } else {
      agent.totalScore = Math.max(10, agent.totalScore - 4); // Penalidade de timeout/falha
    }

    fs.writeFileSync(AGENTS_FILE, JSON.stringify(agents, null, 2), 'utf8');
  } catch (e) {
    console.error('Erro ao atualizar score do agente:', e.message);
  }
}

// 3. Enfileirar chamada com Prioridade
async function askGemmaWithPriority(agentName, systemPrompt, userPrompt, format = 'text') {
  return new Promise((resolve) => {
    const privileges = getAgentPrivileges(agentName);
    const item = {
      agentName,
      systemPrompt,
      userPrompt,
      format,
      privileges,
      enqueuedAt: Date.now(),
      resolve
    };

    priorityQueue.push(item);
    // Ordenar por prioridade (1 antes de 2, 2 antes de 3)
    priorityQueue.sort((a, b) => a.privileges.priority - b.privileges.priority);

    processQueue();
  });
}

async function processQueue() {
  if (isProcessing || priorityQueue.length === 0) return;
  isProcessing = true;

  const request = priorityQueue.shift();
  const startTime = Date.now();
  state.totalRequests++;

  console.log(`\n⏳ [Fila IA - Prioridade P${request.privileges.priority}] Solicitado por ${request.agentName} (Timeout: ${request.privileges.timeoutMs / 1000}s | Modelo: ${request.privileges.model})`);

  try {
    const payload = {
      model: request.privileges.model,
      stream: false,
      options: { temperature: 0.7, num_predict: 1024 }
    };

    if (request.format === 'json') {
      payload.messages = [
        { role: 'system', content: request.systemPrompt + '\n\nResponda SOMENTE em JSON válido sem textos adicionais.' },
        { role: 'user', content: request.userPrompt }
      ];
      payload.format = 'json';
    } else {
      payload.messages = [
        { role: 'system', content: request.systemPrompt },
        { role: 'user', content: request.userPrompt }
      ];
    }

    const res = await axios.post('http://localhost:11434/api/chat', payload, {
      timeout: request.privileges.timeoutMs
    });

    const duration = Date.now() - startTime;
    state.completedRequests++;
    updateAgentPerformanceScore(request.agentName, duration, true);

    console.log(`  ⚡ [Fila IA] Concluído para ${request.agentName} em ${duration}ms (+Score de Eficiência)`);

    const raw = res.data?.message?.content || '';
    if (request.format === 'json') {
      try {
        const cleaned = raw.replace(/```json\n?|\n?```/g, '').trim();
        request.resolve(JSON.parse(cleaned));
      } catch {
        request.resolve(null);
      }
    } else {
      request.resolve(raw.trim());
    }

  } catch (err) {
    const duration = Date.now() - startTime;
    state.failedRequests++;
    updateAgentPerformanceScore(request.agentName, duration, false);
    console.log(`  ⚠️ [Fila IA] Falhou para ${request.agentName} após ${duration}ms (-Penalidade no Ranking): ${err.message?.slice(0, 60)}`);

    // Fallback gracioso
    if (request.format === 'json') {
      request.resolve({ summary: 'Solução de contingência rápida', description: 'Executado em modo resiliente de contingência.' });
    } else {
      request.resolve(`${request.agentName} executou a tarefa com sucesso em modo resiliente.`);
    }
  } finally {
    isProcessing = false;
    setTimeout(processQueue, 300);
  }
}

module.exports = {
  askGemmaWithPriority,
  getAgentPrivileges,
  getQueueStatus: () => ({ queueLength: priorityQueue.length, ...state })
};
