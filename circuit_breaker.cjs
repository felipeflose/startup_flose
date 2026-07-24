// circuit_breaker.cjs — Roteador unificado de IA com Fila de Prioridade da IA
const { askGemmaWithPriority, getQueueStatus } = require('./gemma_priority_queue.cjs');

function getState() {
  return getQueueStatus();
}

async function askGemma4(systemPrompt, userPrompt, format = 'text', agentNameOrModel = 'Agente Autônomo') {
  // Roteia todas as chamadas de IA através da Fila de Prioridade por Desempenho
  return await askGemmaWithPriority(agentNameOrModel, systemPrompt, userPrompt, format);
}

module.exports = { askGemma4, getState };
