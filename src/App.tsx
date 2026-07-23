import { useState, useEffect } from 'react';
import type { Agent } from './components/AgentCard';
import { AgentCard } from './components/AgentCard';
import { OrgChart } from './components/OrgChart';
import { JiraDashboard } from './components/JiraDashboard';
import { GemmaConsole } from './components/GemmaConsole';
import { Briefcase, Cpu, FileText, Layers, Terminal, History, Users, Monitor, Home } from 'lucide-react';
import { CompanyPulse } from './components/CompanyPulse';
import { EmployeeRanking } from './components/EmployeeRanking';
import { CardCreator } from './components/CardCreator';
import { PrototypeViewer } from './components/PrototypeViewer';
import { OfficeMap } from './components/OfficeMap';

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [candidatesList, setCandidatesList] = useState<any[]>([]);
  const [candidatesSearch, setCandidatesSearch] = useState<string>('');
  const [candidatesPage, setCandidatesPage] = useState<number>(1);
  const [candidatesTotal, setCandidatesTotal] = useState<number>(0);
  const [hrTargetRole, setHrTargetRole] = useState<string>('React Sênior');
  const [hrRecruiterId, setHrRecruiterId] = useState<string>('coord_scrum');
  const [hrShortlist, setHrShortlist] = useState<any[]>([]);
  const [hrSearching, setHrSearching] = useState<boolean>(false);
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);
  const [selectedIssue, setSelectedIssue] = useState<{ key: string; summary: string; description: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'backlog' | 'agents' | 'docs' | 'decisions' | 'rh' | 'screens' | 'office' | 'ranking'>('dashboard');
  const [decisions, setDecisions] = useState<any[]>([]);
  const [jiraIssues, setJiraIssues] = useState<any[]>([]);
  const [commits, setCommits] = useState<Record<string, any>>({});

  const shortenBranch = (name: string) => {
    if (!name) return '';
    if (name.length <= 25) return name;
    return name.substring(0, 22) + '...';
  };

  const shortenUrl = (url: string) => {
    if (!url) return '';
    try {
      const parts = url.split('/');
      const num = parts[parts.length - 1];
      if (url.includes('/issues/')) return `Issue #${num}`;
      if (url.includes('/pull/')) return `PR #${num}`;
      return `Link #${num}`;
    } catch {
      return 'Link';
    }
  };

  const getFilename = (path: string) => {
    if (!path) return '';
    return path.split('/').pop() || path;
  };

  const fetchDecisions = () => {
    fetch('http://localhost:5001/api/decisions')
      .then(res => res.json())
      .then(data => setDecisions(data))
      .catch(err => console.error('Erro ao buscar decisões:', err));

    fetch('http://localhost:5001/api/jira/issues')
      .then(res => res.json())
      .then(data => setJiraIssues(data.issues || []))
      .catch(() => {});

    fetch('http://localhost:5001/api/card-commits')
      .then(res => res.json())
      .then(data => setCommits(data || {}))
      .catch(() => {});
  };

  const fetchAgents = () => {
    fetch('http://localhost:5001/api/agents')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
      })
      .catch(err => console.error('Erro ao buscar agentes:', err));
  };

  useEffect(() => {
    fetch('http://localhost:5001/api/agents')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
        const defaultIds = data.map((a: Agent) => a.id);
        setSelectedAgentIds(defaultIds);
      })
      .catch(err => console.error('Erro ao buscar agentes:', err));

    fetchDecisions();
    fetchAgents();

    const polling = setInterval(() => {
      fetchDecisions();
      fetchAgents();
    }, 4000);

    return () => clearInterval(polling);
  }, []);

  useEffect(() => {
    fetch(`http://localhost:5001/api/candidates?search=${candidatesSearch}&page=${candidatesPage}&limit=10`)
      .then(res => res.json())
      .then(data => {
        setCandidatesList(data.candidates || []);
        setCandidatesTotal(data.total || 0);
      })
      .catch(err => console.error('Erro ao buscar candidatos:', err));
  }, [candidatesSearch, candidatesPage]);



  const handleSelectAgentToggle = (id: string) => {
    setSelectedAgentIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  return (
    <>
      <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="logo-container">
          <div className="logo-icon">🚀</div>
          <div>
            <h1 className="logo-text text-gradient" style={{ margin: 0, fontSize: '1.25rem' }}>FLOSE STARTUP</h1>
            <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', letterSpacing: '2px', fontWeight: 700 }}>AI AGENT WORKPLACE</span>
          </div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '20px' }}>
          <button
            onClick={() => setActiveTab('dashboard')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'dashboard' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'dashboard' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Cpu size={18} />
            Chamber de Decisão
          </button>

          <button
            onClick={() => setActiveTab('backlog')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'backlog' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'backlog' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Briefcase size={18} />
            Backlog Jira
          </button>

          <button
            onClick={() => setActiveTab('agents')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'agents' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'agents' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Layers size={18} />
            Perfis de Agentes
          </button>

          <button
            onClick={() => setActiveTab('decisions')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'decisions' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'decisions' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <History size={18} />
            Lastro de Decisões
          </button>

          <button
            onClick={() => setActiveTab('screens')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'screens' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'screens' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Monitor size={18} />
            Protótipos & Telas
          </button>

          <button
            onClick={() => setActiveTab('rh')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'rh' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'rh' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Users size={18} />
            RH & Gestão (Empresa)
          </button>

          <button
            onClick={() => setActiveTab('office')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'office' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'office' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <Home size={18} />
            Escritório & Áreas
          </button>

          <button
            onClick={() => setActiveTab('docs')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'docs' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'docs' ? 'var(--color-primary)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            <FileText size={18} />
            Fundação & Docs
          </button>
          <button
            onClick={() => setActiveTab('ranking')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: activeTab === 'ranking' ? 'var(--bg-tertiary)' : 'transparent',
              color: activeTab === 'ranking' ? '#fbbf24' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              textAlign: 'left',
              width: '100%'
            }}
          >
            🏆 Ranking
          </button>
        </nav>

        <div style={{ marginTop: 'auto', padding: '16px', borderRadius: '12px', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', fontSize: '0.75rem', textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <Terminal size={14} className="text-gradient" />
            <strong style={{ color: 'var(--color-secondary)' }}>Status Conexão</strong>
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>Jira: <span style={{ color: '#34d399' }}>Conectado</span></p>
          <p style={{ color: 'var(--text-secondary)' }}>Motor: <span style={{ color: 'var(--color-primary)' }}>Gemma 4</span></p>
        </div>
      </aside>

      {/* Main Panel */}
      <main className="main-content">
        {activeTab === 'dashboard' && (
          <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
              <div>
                <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                  Decisões Autônomas com <span className="text-gradient">Gemma 4</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                  Selecione um Ticket do Jira, defina os Agentes participantes e execute a simulação do debate corporativo.
                </p>
              </div>
            </div>

            {/* Control Panel (Metrics & Actions) */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginTop: '20px', marginBottom: '28px', width: '100%' }}>
              
              {/* Operational Metrics Card */}
              <div className="glass" style={{ padding: '20px', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                  📊 Métricas de Controle de Sprint
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block' }}>Backlog Ativo</span>
                    <strong style={{ fontSize: '1.4rem', color: '#fb923c' }}>
                      {jiraIssues.filter(j => {
                        const statusName = j.fields?.status?.name?.toLowerCase() || '';
                        return !statusName.includes('done') && !statusName.includes('concluid');
                      }).length} cards
                    </strong>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block' }}>Vazão (Concluídos)</span>
                    <strong style={{ fontSize: '1.4rem', color: '#34d399' }}>
                      {jiraIssues.filter(j => {
                        const statusName = j.fields?.status?.name?.toLowerCase() || '';
                        return statusName.includes('done') || statusName.includes('concluid');
                      }).length} cards
                    </strong>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block' }}>Devs Ativos</span>
                    <strong style={{ fontSize: '1.4rem', color: 'var(--color-primary)' }}>
                      {agents.filter(a => !a.fired && ['frontend', 'backend', 'devops', 'dba', 'secops', 'developer', 'desenvolvedor', 'ux', 'ui'].some(r => (a.role || '').toLowerCase().includes(r))).length}
                    </strong>
                  </div>
                  <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block' }}>QAs Ativos</span>
                    <strong style={{ fontSize: '1.4rem', color: 'var(--color-secondary)' }}>
                      {agents.filter(a => !a.fired && ['qa', 'test', 'qualidade', 'garantia'].some(r => (a.role || '').toLowerCase().includes(r))).length}
                    </strong>
                  </div>
                </div>
              </div>

              {/* Quick Operation Triggers */}
              <div className="glass" style={{ padding: '20px', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                  ⚙️ Operação Rápida de Governança
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', margin: 0 }}>
                  Ações de saneamento rápido para restaurar a vazão das entregas e aumentar a força produtiva do time de engenharia.
                </p>
                <div style={{ display: 'flex', gap: '12px', marginTop: 'auto' }}>
                  <button
                    onClick={() => {
                      if (!confirm('Deseja realmente zerar todos os cards do backlog ativos transicionando-os para Concluído?')) return;
                      const btn = document.getElementById('btn-resolve-all');
                      if (btn) btn.innerText = '🕒 Processando...';
                      fetch('http://localhost:5001/api/issues/resolve-all', { method: 'POST' })
                        .then(res => res.json())
                        .then(data => {
                          alert(`Saneamento efetuado! ${data.resolvedCount} cards transicionados para Concluído.`);
                          fetchDecisions();
                        })
                        .catch(err => alert('Erro: ' + err.message))
                        .finally(() => { if (btn) btn.innerText = '⚡ Zerar Backlog'; });
                    }}
                    id="btn-resolve-all"
                    style={{
                      flex: 1, padding: '12px', borderRadius: '10px', border: '1px solid rgba(239, 68, 68, 0.4)',
                      background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05))',
                      color: '#f87171', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer', transition: 'all 0.2s'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.25)'}
                    onMouseOut={(e) => e.currentTarget.style.background = 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05))'}
                  >
                    ⚡ Zerar Backlog
                  </button>

                  <button
                    onClick={() => {
                      const btn = document.getElementById('btn-bulk-hire');
                      if (btn) btn.innerText = '🕒 Contratando...';
                      fetch('http://localhost:5001/api/hiring/bulk', { method: 'POST' })
                        .then(res => res.json())
                        .then(data => {
                          alert(`Contratação concluída! ${data.hiredCount} engenheiros reativados para a sprint.`);
                          fetchAgents();
                        })
                        .catch(err => alert('Erro: ' + err.message))
                        .finally(() => { if (btn) btn.innerText = '👥 Contratar Devs & QAs'; });
                    }}
                    id="btn-bulk-hire"
                    style={{
                      flex: 1, padding: '12px', borderRadius: '10px', border: '1px solid rgba(52, 211, 153, 0.4)',
                      background: 'linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(52, 211, 153, 0.05))',
                      color: '#34d399', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer', transition: 'all 0.2s'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.background = 'rgba(52, 211, 153, 0.25)'}
                    onMouseOut={(e) => e.currentTarget.style.background = 'linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(52, 211, 153, 0.05))'}
                  >
                    👥 Contratar Devs & QAs
                  </button>
                </div>
              </div>

            </div>

            {/* OrgChart Selection */}
            <OrgChart 
              agents={agents.filter(a => !a.fired)} 
              selectedAgentIds={selectedAgentIds} 
              onSelectAgent={handleSelectAgentToggle} 
            />

            {/* Simulation Chamber */}
            <GemmaConsole 
              selectedIssue={selectedIssue}
              selectedAgentIds={selectedAgentIds}
              onDebateComplete={fetchDecisions}
            />

            {/* Company Activity Stream Panel */}
            <CompanyPulse agents={agents.filter(a => !a.fired)} />
          </>
        )}

        {activeTab === 'backlog' && (
          <>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                Gerenciamento de Integração <span className="text-gradient">Jira</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Crie novos problemas ou selecione issues importados diretamente do board do Jira para envio à sala de decisões.
              </p>
            </div>

            <JiraDashboard 
              onSelectIssue={(issue) => {
                setSelectedIssue(issue);
                setActiveTab('dashboard');
              }}
              selectedIssueKey={selectedIssue?.key || null}
            />
          </>
        )}

        {activeTab === 'agents' && (
          <>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                Perfis Completos dos <span className="text-gradient">Agentes Flose</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Todos os perfis são providos de vantagens, desvantagens, dilemas essenciais e personalidade base.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
              {agents.map(agent => (
                <AgentCard 
                  key={agent.id}
                  agent={agent}
                  isSelected={selectedAgentIds.includes(agent.id)}
                  onSelectToggle={() => handleSelectAgentToggle(agent.id)}
                />
              ))}
            </div>
          </>
        )}

        {activeTab === 'decisions' && (
          <>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                Lastro de <span className="text-gradient">Decisões Corporativas</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left', marginBottom: '24px' }}>
                Histórico completo e rastreável de todas as propostas enviadas e debatidas pelos agentes da startup.
              </p>
            </div>

            {decisions.length === 0 ? (
              <div className="glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
                Nenhuma decisão registrada no lastro ainda. Vá para a Chamber de Decisão e proponha uma ideia!
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {decisions.map((dec) => (
                  <div key={dec.id} className="glass" style={{ padding: '24px', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <span style={{
                          background: 'var(--color-secondary)',
                          color: '#fff',
                          padding: '4px 10px',
                          borderRadius: 'var(--radius-sm)',
                          fontSize: '0.8rem',
                          fontWeight: 700
                        }}>
                          {dec.issueKey}
                        </span>
                        <strong style={{ fontSize: '1.2rem' }}>{dec.issueSummary}</strong>
                      </div>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {new Date(dec.timestamp).toLocaleString('pt-BR')}
                      </span>
                    </div>

                    {dec.issueDescription && (
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0, paddingLeft: '8px', borderLeft: '2px solid var(--border-color)' }}>
                        {dec.issueDescription}
                      </p>
                    )}

                    <div style={{
                      padding: '16px',
                      background: 'hsla(var(--hue-secondary), 90%, 55%, 0.08)',
                      border: '1px solid var(--color-secondary)',
                      borderRadius: 'var(--radius-md)'
                    }}>
                      <strong style={{ color: 'var(--color-secondary)', fontSize: '0.9rem', display: 'block', marginBottom: '6px' }}>🏆 Consenso Aprovado:</strong>
                      <p style={{ fontSize: '0.9rem', margin: 0, lineHeight: 1.4 }}>{dec.decision}</p>
                    </div>

                    {/* Rastreabilidade de Agentes */}
                    <div>
                      <strong style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '10px' }}>
                        👥 Contribuições Individuais (Empresa):
                      </strong>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {dec.logs?.map((log: any, idx: number) => (
                          <div key={idx} style={{
                            display: 'flex',
                            gap: '10px',
                            background: 'var(--bg-secondary)',
                            padding: '10px 14px',
                            borderRadius: '8px',
                            border: '1px solid var(--border-color)',
                            fontSize: '0.8rem'
                          }}>
                            <span style={{ fontSize: '1.5rem' }}>{log.avatar}</span>
                            <div>
                              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                                <strong>{log.name}</strong>
                                <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>{log.role}</span>
                              </div>
                              <p style={{ margin: '4px 0 0 0', fontStyle: 'italic', color: 'var(--text-primary)' }}>
                                "{log.opinion}"
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Git Branch & GitHub details */}
                    {(dec.gitBranchName || dec.githubIssueUrl) && (
                      <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px',
                        background: 'rgba(255, 255, 255, 0.02)',
                        padding: '12px',
                        borderRadius: '6px',
                        border: '1px dashed var(--border-color)',
                        fontSize: '0.8rem',
                        marginTop: '12px'
                      }}>
                        {dec.gitBranchName && (
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span>🌿 Branch Git: <code style={{ color: '#a5b4fc' }} title={dec.gitBranchName}>{shortenBranch(dec.gitBranchName)}</code></span>
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(`git checkout ${dec.gitBranchName}`);
                                alert('Comando copiado para a área de transferência!');
                              }}
                              style={{
                                background: 'var(--bg-tertiary)',
                                border: '1px solid var(--border-color)',
                                color: 'var(--text-primary)',
                                padding: '2px 8px',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '0.7rem'
                              }}
                            >
                              Copiar Comando
                            </button>
                          </div>
                        )}
                        {dec.githubIssueUrl && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <span>🐙 GitHub Issue: </span>
                            <a href={dec.githubIssueUrl} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-primary)', textDecoration: 'underline' }}>
                              {shortenUrl(dec.githubIssueUrl)}
                            </a>
                          </div>
                        )}
                      </div>
                    )}

                    {dec.executorName && (
                      <div style={{
                        marginTop: '8px',
                        padding: '10px 12px',
                        background: 'rgba(251, 191, 36, 0.05)',
                        border: '1px dashed #fbbf24',
                        borderRadius: '6px',
                        fontSize: '0.8rem',
                        color: '#fef3c7'
                      }}>
                        <strong>🔧 Executado por:</strong> {dec.executorName} ({dec.executorRole}) 
                        {dec.generatedFile && <span> | 📄 <code title={dec.generatedFile}>{getFilename(dec.generatedFile)}</code></span>}
                        {dec.commitHash && <span> | 💾 Git Commit: <code style={{ color: '#fbbf24' }}>{dec.commitHash}</code></span>}
                      </div>
                    )}

                    {dec.jiraCommentResult && (
                      <div style={{
                        fontSize: '0.75rem',
                        color: '#34d399',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        marginTop: '12px'
                      }}>
                        <span>✓ Sincronizado no Atlassian Jira</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'rh' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                Quadro de <span className="text-gradient">Colaboradores & Performance</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Monitore a governança autônoma da sua startup. Contratações, demissões e feedbacks são processados diretamente pelos agentes a partir dos seus comandos na Sala de Decisão.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px', alignItems: 'start' }}>
              {/* Quadro de Colaboradores Ativos */}
              <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>👥 Equipe Ativa ({agents.filter(a => !a.fired).length})</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxHeight: '700px', overflowY: 'auto', paddingRight: '4px' }}>
                  {agents.filter(a => !a.fired).map((agent) => (
                    <div key={agent.id} style={{ padding: '20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span style={{ fontSize: '2.25rem' }}>{agent.avatar}</span>
                          <div>
                            <strong style={{ fontSize: '1.15rem', color: 'var(--color-primary)' }}>{agent.name}</strong>
                            <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>{agent.role} • <strong>{agent.level}</strong></p>
                          </div>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '4px' }}>
                          <span style={{
                            fontSize: '0.7rem',
                            padding: '3px 8px',
                            borderRadius: '12px',
                            background: agent.status === 'Disponível' ? 'rgba(52, 211, 153, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                            border: agent.status === 'Disponível' ? '1px solid #34d399' : '1px solid #ef4444',
                            color: agent.status === 'Disponível' ? '#34d399' : '#f87171',
                            fontWeight: 600
                          }}>
                            {agent.status || 'Disponível'}
                          </span>
                          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>⏱ Jornada: {agent.schedule || '09:00 - 18:00'}</span>
                        </div>
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.8rem', borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
                        <div>
                          <strong style={{ color: 'var(--color-secondary)' }}>✓ Vantagem:</strong>
                          <p style={{ margin: '2px 0 0 0', color: 'var(--text-secondary)' }}>{agent.advantage}</p>
                        </div>
                        <div>
                          <strong style={{ color: '#ef4444' }}>✗ Desvantagem:</strong>
                          <p style={{ margin: '2px 0 0 0', color: 'var(--text-secondary)' }}>{agent.disadvantage}</p>
                        </div>
                      </div>

                      <div style={{ fontSize: '0.8rem', background: 'rgba(255,255,255,0.01)', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                        <strong>⚠️ Dilema Estratégico:</strong> {agent.dilemma}
                      </div>

                      {/* Feedbacks list */}
                      {agent.feedbacks && agent.feedbacks.length > 0 && (
                        <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
                          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Histórico de Feedbacks:</span>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                            {agent.feedbacks.map((f: any, idx: number) => (
                              <div key={idx} style={{ padding: '6px 10px', borderRadius: '4px', background: 'var(--bg-tertiary)', borderLeft: f.rating === 'positivo' ? '3px solid #34d399' : '3px solid #ef4444', fontSize: '0.75rem', display: 'flex', justifyContent: 'space-between' }}>
                                <span>"{f.text}"</span>
                                <span style={{ color: f.rating === 'positivo' ? '#34d399' : '#f87171', fontWeight: 600 }}>{f.rating === 'positivo' ? '👍' : '👎'}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Lado direito - Colaboradores desligados */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-secondary)' }}>❌ Desligados ({agents.filter(a => a.fired).length})</h2>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '400px', overflowY: 'auto' }}>
                    {agents.filter(a => a.fired).length === 0 ? (
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhum colaborador desligado no momento.</span>
                    ) : (
                      agents.filter(a => a.fired).map((agent) => (
                        <div key={agent.id} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.01)', borderRadius: '8px', border: '1px solid var(--border-color)', opacity: 0.65 }}>
                          <span style={{ fontSize: '1.5rem', filter: 'grayscale(100%)' }}>{agent.avatar}</span>
                          <div style={{ flex: 1, textAlign: 'left' }}>
                            <strong style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textDecoration: 'line-through' }}>{agent.name}</strong>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: 'var(--text-muted)' }}>{agent.role}</p>
                            <p style={{ margin: '4px 0 0 0', fontSize: '0.65rem', color: '#f87171', fontStyle: 'italic', fontWeight: 500 }}>
                              🚫 {agent.firedReason || 'Demissão em massa para reestruturação hierárquica pelo CEO.'}
                            </p>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Seção Banco de Candidatos & IA Recrutamento */}
            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px', marginTop: '32px', alignItems: 'start' }}>
              
              {/* IA Recrutamento & Seleção (Shortlist) */}
              <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '1.5rem' }}>🎯</span>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Recrutamento Autônomo (Gemma 4 RH)</h2>
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '-8px' }}>
                  Selecione um cargo alvo e o recrutador encarregado de buscar no banco de 45.000 perfis.
                </p>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: '8px' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Cargo Alvo</label>
                    <select
                      value={hrTargetRole}
                      onChange={e => setHrTargetRole(e.target.value)}
                      style={{
                        padding: '8px 12px',
                        borderRadius: '8px',
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        color: '#fff',
                        outline: 'none'
                      }}
                    >
                      <option value="React Sênior">Frontend React Sênior</option>
                      <option value="Node.js Sênior">Backend Node.js Sênior</option>
                      <option value="DevOps Cloud Sênior">DevOps Cloud Sênior</option>
                      <option value="Banco de Dados Sênior">Administrador de Banco (DBA)</option>
                      <option value="IA & Machine Learning">Engenheiro de IA/ML</option>
                      <option value="Garantia de Qualidade">Analista de QA Sênior</option>
                      <option value="Product Owner Sênior">Product Owner (PO)</option>
                      <option value="Recursos Humanos">Tech Recruiter Sênior</option>
                    </select>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Recrutador Responsável</label>
                    <select
                      value={hrRecruiterId}
                      onChange={e => setHrRecruiterId(e.target.value)}
                      style={{
                        padding: '8px 12px',
                        borderRadius: '8px',
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        color: '#fff',
                        outline: 'none'
                      }}
                    >
                      {agents.filter(a => !a.fired).map(a => (
                        <option key={a.id} value={a.id}>{a.name} ({a.role})</option>
                      ))}
                    </select>
                  </div>
                </div>

                <button
                  onClick={async () => {
                    setHrSearching(true);
                    setHrShortlist([]);
                    try {
                      const res = await fetch('http://localhost:5001/api/hr/recruitment', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ targetRole: hrTargetRole, recruiterAgentId: hrRecruiterId })
                      });
                      const data = await res.json();
                      if (data.success) {
                        setHrShortlist(data.shortlist);
                      } else {
                        alert(data.error);
                      }
                    } catch (e) {
                      alert('Falha na triagem de candidatos.');
                    } finally {
                      setHrSearching(false);
                    }
                  }}
                  disabled={hrSearching}
                  className="bg-gradient"
                  style={{
                    padding: '10px 20px',
                    borderRadius: '8px',
                    border: 'none',
                    color: '#fff',
                    fontWeight: 700,
                    cursor: 'pointer',
                    marginTop: '8px',
                    boxShadow: '0 0 15px hsla(var(--hue-primary), 90%, 65%, 0.2)'
                  }}
                >
                  {hrSearching ? 'IA Escaneando 45.000 Perfis...' : 'Filtrar Candidatos com IA'}
                </button>

                {/* Shortlist Results */}
                {hrShortlist.length > 0 && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '16px' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-secondary)' }}>🏆 Melhores Candidatos Recomendados:</h3>
                    {hrShortlist.map((item, idx) => (
                      <div key={idx} style={{
                        background: 'var(--bg-secondary)',
                        padding: '16px',
                        borderRadius: '12px',
                        border: '1px solid var(--border-color)',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontSize: '1.5rem' }}>{item.candidate.avatar}</span>
                            <div>
                              <strong style={{ fontSize: '0.95rem' }}>{item.candidate.name}</strong>
                              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-muted)' }}>{item.candidate.role}</p>
                            </div>
                          </div>
                          <span style={{
                            fontSize: '0.8rem',
                            fontWeight: 700,
                            padding: '3px 8px',
                            borderRadius: '8px',
                            background: 'rgba(52, 211, 153, 0.1)',
                            color: '#34d399',
                            border: '1px solid #34d399'
                          }}>
                            Score: {item.score}
                          </span>
                        </div>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontStyle: 'italic', background: 'rgba(255,255,255,0.02)', padding: '8px', borderRadius: '6px' }}>
                          💬 Evaluation: {item.recruiterEvaluation}
                        </p>
                        <button
                          onClick={async () => {
                            try {
                              const res = await fetch('http://localhost:5001/api/hr/hire', {
                                method: 'POST',
                                  headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ candidateId: item.candidate.id })
                              });
                              const data = await res.json();
                              if (data.success) {
                                alert(`Contratado com sucesso! Ticket de Onboarding criado no Jira: ${data.jiraKey}`);
                                // Refresh active agents
                                fetch('http://localhost:5001/api/agents')
                                  .then(r => r.json())
                                  .then(a => setAgents(a));
                              } else {
                                alert(data.error);
                              }
                            } catch (e) {
                              alert('Erro ao efetuar contratação.');
                            }
                          }}
                          className="bg-gradient"
                          style={{
                            padding: '6px 12px',
                            borderRadius: '6px',
                            border: 'none',
                            color: '#fff',
                            fontWeight: 600,
                            fontSize: '0.8rem',
                            cursor: 'pointer',
                            alignSelf: 'flex-end'
                          }}
                        >
                          Admitir & Criar Onboarding Jira
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Busca e Listagem no Banco de 45 Mil Candidatos */}
              <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>🗄️ Banco de Talentos (45k Perfis)</h2>
                  <span style={{ fontSize: '0.75rem', background: 'hsla(var(--hue-primary), 15%, 25%, 0.5)', padding: '2px 8px', borderRadius: '10px', color: 'var(--text-muted)' }}>
                    Total: {candidatesTotal.toLocaleString()}
                  </span>
                </div>
                
                <input
                  type="text"
                  placeholder="Pesquisar por nome ou cargo no banco..."
                  value={candidatesSearch}
                  onChange={e => {
                    setCandidatesSearch(e.target.value);
                    setCandidatesPage(1);
                  }}
                  style={{
                    padding: '8px 12px',
                    borderRadius: '8px',
                    background: 'var(--bg-secondary)',
                    border: '1px solid var(--border-color)',
                    color: '#fff',
                    outline: 'none',
                    width: '100%'
                  }}
                />

                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '430px', overflowY: 'auto' }}>
                  {candidatesList.map(cand => (
                    <div key={cand.id} style={{
                      padding: '10px 14px',
                      background: 'rgba(255,255,255,0.01)',
                      borderRadius: '8px',
                      border: '1px solid var(--border-color)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span style={{ fontSize: '1.5rem' }}>{cand.avatar}</span>
                        <div>
                          <strong style={{ fontSize: '0.85rem' }}>{cand.name}</strong>
                          <p style={{ margin: 0, fontSize: '0.7rem', color: 'var(--text-muted)' }}>{cand.role}</p>
                        </div>
                      </div>
                      <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-secondary)' }}>
                        R$ {cand.expectedSalary.toLocaleString()}/mês
                      </span>
                    </div>
                  ))}
                </div>

                {/* Pagination */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
                  <button
                    disabled={candidatesPage <= 1}
                    onClick={() => setCandidatesPage(p => p - 1)}
                    style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-color)',
                      color: '#fff',
                      cursor: 'pointer',
                      fontSize: '0.75rem'
                    }}
                  >
                    Anterior
                  </button>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Página {candidatesPage}</span>
                  <button
                    disabled={candidatesPage * 10 >= candidatesTotal}
                    onClick={() => setCandidatesPage(p => p + 1)}
                    style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-color)',
                      color: '#fff',
                      cursor: 'pointer',
                      fontSize: '0.75rem'
                    }}
                  >
                    Próxima
                  </button>
                </div>
              </div>

            </div>
          </div>

        )}
        {activeTab === 'office' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                🏢 Mapa de <span className="text-gradient">Áreas & Estações de Trabalho</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Layout projetado pelo **Enzo Facilities** (Infraestrutura) e organizado pelo **Hugo Organizador** (RH/Estrutura) para acomodar todos os colaboradores da Flose Startup.
              </p>
            </div>

            {/* Organizadores Info */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="glass" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: '16px', background: 'rgba(96, 165, 250, 0.1)', border: '1px solid #60a5fa' }}>
                <span style={{ fontSize: '2.5rem' }}>📋</span>
                <div style={{ textAlign: 'left' }}>
                  <strong style={{ color: '#60a5fa', fontSize: '1rem' }}>Hugo Organizador (RH & Processos)</strong>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Estruturou os colaboradores em 4 departamentos distintos para otimizar os fluxos de comunicação e debates.
                  </p>
                </div>
              </div>
              <div className="glass" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: '16px', background: 'rgba(52, 211, 153, 0.1)', border: '1px solid #34d399' }}>
                <span style={{ fontSize: '2.5rem' }}>🏗️</span>
                <div style={{ textAlign: 'left' }}>
                  <strong style={{ color: '#34d399', fontSize: '1rem' }}>Enzo Facilities (Engenharia Física)</strong>
                  <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Alocou as mesas físicas e salas garantindo a ergonomia e sinergia de mesa (clean desk policy ativa).
                  </p>
                </div>
              </div>
            </div>

            {/* Live Interactive Office Map */}
            <OfficeMap 
              agents={agents} 
              selectedAgentIds={selectedAgentIds} 
              jiraIssues={jiraIssues}
            />

            {/* Department Grid Layout */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(480px, 1fr))', gap: '24px', marginTop: '12px' }}>
              {[
                { name: "Diretoria & C-Suite", color: "#ffd700", desc: "Sala executiva da presidência e diretoria." },
                { name: "Engenharia & TI", color: "#3b82f6", desc: "Ilha de desenvolvimento backend, frontend e nuvem." },
                { name: "Produto & Design", color: "#f59e0b", desc: "Espaço criativo para UI/UX e roadmap." },
                { name: "Qualidade, RH & Operações", color: "#34d399", desc: "Área de testes, facilitação ágil e gestão de pessoas." }
              ].map(dept => {
                const deptAgents = agents.filter(a => !a.fired && (a.area === dept.name || (!a.area && dept.name === "Engenharia & TI")));
                return (
                  <div key={dept.name} className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left', minHeight: '380px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: `2px solid ${dept.color}`, paddingBottom: '8px' }}>
                      <div>
                        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>{dept.name}</h2>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{dept.desc}</span>
                      </div>
                      <span style={{ fontSize: '0.8rem', fontWeight: 700, color: dept.color, background: `${dept.color}1A`, padding: '2px 8px', borderRadius: '12px' }}>
                        {deptAgents.length} pessoas
                      </span>
                    </div>

                    {/* Mesas list */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', overflowY: 'auto', maxHeight: '350px' }}>
                      {deptAgents.map(agent => (
                        <div key={agent.id} style={{
                          padding: '12px',
                          background: 'var(--bg-secondary)',
                          borderRadius: '8px',
                          border: '1px solid var(--border-color)',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '6px',
                          position: 'relative'
                        }}>
                          <span style={{
                            position: 'absolute',
                            top: '8px',
                            right: '8px',
                            fontSize: '0.65rem',
                            fontWeight: 700,
                            padding: '2px 6px',
                            borderRadius: '4px',
                            background: 'rgba(255,255,255,0.03)',
                            color: 'var(--color-secondary)',
                            border: '1px solid var(--border-color)'
                          }}>
                            {agent.desk || 'Mesa'}
                          </span>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontSize: '1.5rem' }}>{agent.avatar}</span>
                            <div style={{ overflow: 'hidden' }}>
                              <strong style={{ fontSize: '0.85rem', color: 'var(--text-primary)', whiteSpace: 'nowrap', textOverflow: 'ellipsis', display: 'block' }}>{agent.name}</strong>
                              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', whiteSpace: 'nowrap', textOverflow: 'ellipsis' }}>{agent.role}</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
        {activeTab === 'screens' && (
          <PrototypeViewer decisions={decisions} jiraIssues={jiraIssues} commits={commits} />
        )}

        {activeTab === 'docs' && (
          <div className="glass" style={{ padding: '32px', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <h1 className="text-gradient" style={{ fontSize: '2.5rem', fontWeight: 800 }}>Documentação de Fundação</h1>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              A <strong>Flose Startup</strong> foi projetada como uma fundação autónoma para alinhar decisões técnicas e de produto através de debate inteligente entre perfis corporativos extremos.
            </p>

            <h2 style={{ fontSize: '1.5rem', marginTop: '16px' }}>🛠️ Níveis de Governança</h2>
            <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
              <li><strong>C-Level:</strong> Visão macro de mercado e arquitetura de tecnologia (CEO, CTO).</li>
              <li><strong>Diretores:</strong> Gerenciamento tático de recursos e experiência de usuário (Operações, UX/Design).</li>
              <li><strong>Gerentes:</strong> Conexão entre o operacional e o estratégico (Gerente de Engenharia, Gerente de Produto).</li>
              <li><strong>Coordenadores:</strong> Facilitadores de processos e guardiões de qualidade ágil/QA (Scrum Master, QA).</li>
              <li><strong>Analistas SR:</strong> Engenharia pura e design detalhados (Dev Sênior, Designer UI/UX Sênior).</li>
            </ul>

            <h2 style={{ fontSize: '1.5rem', marginTop: '16px' }}>⚡ Integração Contínua com Jira</h2>
            <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', fontSize: '0.95rem' }}>
              As discussões e resoluções criadas pelas inteligências Gemma 4 são sincronizadas de volta com o Atlassian Jira na forma de comentários formais no ticket selecionado. Isso garante transparência e rastreabilidade total de auditoria da startup.
            </p>
          </div>
        )}

        {activeTab === 'ranking' && (
          <div className="glass" style={{ padding: '32px' }}>
            <EmployeeRanking />
          </div>
        )}
      </main>
    </div>
    <CardCreator onCreated={() => {}} />
    </>
  );
}

export default App;
