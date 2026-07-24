import { useState, useEffect } from 'react';
import { Activity, BarChart3, CheckCircle2, ShieldCheck, Users, Cpu, Layers } from 'lucide-react';

export function KpiDashboard() {
  const [kpis, setKpis] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const [config, setConfig] = useState<any>({
    autoDevExecutionEnabled: true,
    autoHiringEnabled: false,
    autoCardCreationEnabled: false
  });

  const fetchKpis = async () => {
    try {
      const [resKpis, resHealth, resConfig] = await Promise.all([
        fetch('http://localhost:5001/api/kpis').then(r => r.json()),
        fetch('http://localhost:5001/api/health/gemma4').then(r => r.json()),
        fetch('http://localhost:5001/api/company-config').then(r => r.json())
      ]);
      setKpis(resKpis);
      setHealth(resHealth);
      if (resConfig) setConfig(resConfig);
    } catch (e) {
      console.error('Erro ao carregar KPIs:', e);
    } finally {
      setLoading(false);
    }
  };

  const toggleMotor = async (key: string, currentValue: boolean) => {
    try {
      const updatedValue = !currentValue;
      setConfig((prev: any) => ({ ...prev, [key]: updatedValue }));
      await fetch('http://localhost:5001/api/company-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ [key]: updatedValue })
      });
    } catch (e) {
      console.error('Erro ao alterar chave do motor:', e);
    }
  };

  useEffect(() => {
    fetchKpis();
    const interval = setInterval(fetchKpis, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400">
        <Activity className="w-8 h-8 animate-spin mx-auto mb-2 text-indigo-500" />
        Carregando métricas em tempo real...
      </div>
    );
  }

  const company = kpis?.company || {};
  const jira = kpis?.jira || {};
  const areas = kpis?.areas || {};

  return (
    <div className="space-y-6">
      {/* Header Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-sm font-medium">Agentes Ativos</span>
            <Users className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-bold text-white">{company.activeAgents || 0}</span>
            <span className="text-xs text-slate-500">Escala sem Limite</span>
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${Math.min(100, ((company.activeAgents || 0) / 60) * 100)}%` }}></div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-sm font-medium">Score Médio da Equipe</span>
            <BarChart3 className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-bold text-white">{company.averageScore || 0}/100</span>
            <span className="text-xs text-emerald-400 font-medium">Alta Produtividade</span>
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${company.averageScore || 0}%` }}></div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-sm font-medium">Cards Entregues (7d)</span>
            <CheckCircle2 className="w-5 h-5 text-blue-400" />
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-bold text-white">{jira.doneLast7Days || 0}</span>
            <span className="text-xs text-slate-400">Em progresso: {jira.inProgress || 0}</span>
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-blue-500 h-full rounded-full" style={{ width: '70%' }}></div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-sm font-medium">Status Gemma 4 (Ollama)</span>
            <Cpu className="w-5 h-5 text-purple-400" />
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-lg font-bold text-white flex items-center gap-2">
              {health?.available ? (
                <>
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  Conectado
                </>
              ) : (
                <>
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                  Circuit Breaker
                </>
              )}
            </span>
            <span className="text-xs text-purple-400 font-mono">gemma4-fast</span>
          </div>
          <div className="mt-2 text-xs text-slate-500 flex justify-between">
            <span>Modelos disponíveis: {health?.models?.length || 0}</span>
          </div>
        </div>
      </div>

      {/* Governança & Alertas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 col-span-1">
          <h3 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-indigo-400" />
            Governança & PIP
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
              <span className="text-sm text-slate-300">Colaboradores em PIP</span>
              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${company.pipActive > 0 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-slate-700 text-slate-300'}`}>
                {company.pipActive || 0} Ativo(s)
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
              <span className="text-sm text-slate-300">Proteção de CEO</span>
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Ativada
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
              <span className="text-sm text-slate-300">Total de Desligamentos</span>
              <span className="text-sm font-semibold text-slate-300">
                {company.firedAgents || 0}
              </span>
            </div>
          </div>
        </div>

        {/* Carga por Área */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 col-span-2">
          <h3 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-400" />
            Carga Operacional por Área
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {Object.entries(areas).map(([areaName, data]: [string, any]) => {
              const pct = data.capacity > 0 ? Math.round((data.load / data.capacity) * 100) : 0;
              return (
                <div key={areaName} className="p-3 bg-slate-800/40 rounded-lg border border-slate-800">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-slate-200">{areaName}</span>
                    <span className="text-xs text-slate-400">{data.agents} Agente(s)</span>
                  </div>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Carga: {data.load}/{data.capacity}</span>
                    <span className={pct > 80 ? 'text-amber-400 font-semibold' : 'text-slate-400'}>{pct}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${pct > 80 ? 'bg-amber-500' : 'bg-indigo-500'}`}
                      style={{ width: `${Math.min(100, pct)}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Controles de Ligar/Desligar Motores (Dev, PO, Contratação) */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 backdrop-blur-sm">
        <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-400" />
          Controle Central de Operação dos Motores IA
        </h3>
        <p className="text-xs text-slate-400 mb-6">
          Ligue ou desligue a atuação autônoma dos Desenvolvedores, Contratações e POs em tempo real.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Engine Dev */}
          <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="text-sm font-semibold text-white">Motor de Desenvolvedores (Devs)</h4>
              <p className="text-xs text-slate-400 mt-1">
                {config?.autoDevExecutionEnabled !== false ? '🟢 Codificando cards pendentes no Jira' : '🔴 Execução de Devs Pausada'}
              </p>
            </div>
            <button
              onClick={() => toggleMotor('autoDevExecutionEnabled', config?.autoDevExecutionEnabled !== false)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                config?.autoDevExecutionEnabled !== false
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 hover:bg-emerald-500/30'
                  : 'bg-rose-500/20 text-rose-400 border border-rose-500/40 hover:bg-rose-500/30'
              }`}
            >
              {config?.autoDevExecutionEnabled !== false ? 'LIGADO' : 'DESLIGADO'}
            </button>
          </div>

          {/* Engine Contratação */}
          <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="text-sm font-semibold text-white">Motor de Contratação (RH)</h4>
              <p className="text-xs text-slate-400 mt-1">
                {config?.autoHiringEnabled ? '🟢 Admitindo sob sobrecarga' : '🔴 Contratação Automática Desligada'}
              </p>
            </div>
            <button
              onClick={() => toggleMotor('autoHiringEnabled', !!config?.autoHiringEnabled)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                config?.autoHiringEnabled
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 hover:bg-emerald-500/30'
                  : 'bg-rose-500/20 text-rose-400 border border-rose-500/40 hover:bg-rose-500/30'
              }`}
            >
              {config?.autoHiringEnabled ? 'LIGADO' : 'DESLIGADO'}
            </button>
          </div>

          {/* Engine PO */}
          <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="text-sm font-semibold text-white">Motor de Produtos (PO)</h4>
              <p className="text-xs text-slate-400 mt-1">
                {config?.autoCardCreationEnabled ? '🟢 Criando cards por análise de código' : '🔴 Criação Autônoma Desligada'}
              </p>
            </div>
            <button
              onClick={() => toggleMotor('autoCardCreationEnabled', !!config?.autoCardCreationEnabled)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                config?.autoCardCreationEnabled
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 hover:bg-emerald-500/30'
                  : 'bg-rose-500/20 text-rose-400 border border-rose-500/40 hover:bg-rose-500/30'
              }`}
            >
              {config?.autoCardCreationEnabled ? 'LIGADO' : 'DESLIGADO'}
            </button>
          </div>
        </div>

        {/* Seleção do Modelo do Motor Dev */}
        <div className="mt-6 pt-6 border-t border-slate-800">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                🤖 Modelo do Motor Dev (Engenharia)
              </h4>
              <p className="text-xs text-slate-400 mt-0.5">
                Escolha qual LLM ou CLI os Desenvolvedores virtuais utilizarão para implementar o código.
              </p>
            </div>

            <div className="flex items-center gap-3 w-full sm:w-auto">
              <select
                value={config?.models?.devModel || 'qwen2.5-coder:32b'}
                onChange={async (e) => {
                  const val = e.target.value;
                  const updatedModels = { ...(config?.models || {}), devModel: val };
                  setConfig((prev: any) => ({ ...prev, models: updatedModels }));
                  await fetch('http://localhost:5001/api/company-config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ models: updatedModels })
                  });
                }}
                className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none w-full sm:w-auto font-mono"
              >
                <option value="qwen2.5-coder:32b">qwen2.5-coder:32b (Recomendado Coder)</option>
                <option value="gemma4-fast:latest">gemma4-fast:latest (Rápido)</option>
                <option value="gemma4:latest">gemma4:latest (Completo)</option>
                <option value="qwen2.5-coder:latest">qwen2.5-coder:latest</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
