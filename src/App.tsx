import { useState, useEffect } from 'react';
import type { Agent } from './components/AgentCard';
import { AgentCard } from './components/AgentCard';
import { OrgChart } from './components/OrgChart';
import { JiraDashboard } from './components/JiraDashboard';
import { GemmaConsole } from './components/GemmaConsole';
import { Briefcase, Cpu, FileText, Layers, Terminal, History, Users, Monitor, Home } from 'lucide-react';
import { CompanyPulse } from './components/CompanyPulse';
import { EmployeeRanking } from './components/EmployeeRanking';

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
  const [selectedScreenKey, setSelectedScreenKey] = useState<string>('');
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [dashboardMetrics, setDashboardMetrics] = useState({ users: 12490, conversion: 3.42, load: 24 });
  const [scanActive, setScanActive] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);
  const [selectedScreenContent, setSelectedScreenContent] = useState<string>('');
  const [visualizerTab, setVisualizerTab] = useState<'staging' | 'code'>('staging');
  const [memoryCards, setMemoryCards] = useState<{ id: number; symbol: string; flipped: boolean; matched: boolean }[]>([]);
  const [memorySelected, setMemorySelected] = useState<number[]>([]);
  const [gtaLog, setGtaLog] = useState<string[]>(['Bem-vindo a Flose Vice City. Selecione uma missão.']);
  const [gtaStats, setGtaStats] = useState({ money: 100, respect: 20, wanted: 0 });
  const [dataLakeSyncing, setDataLakeSyncing] = useState(false);
  const [dataLakeProgress, setDataLakeProgress] = useState(0);
  const [dataLakeStatus, setDataLakeStatus] = useState('Pronto para replicação');
  const [assetsList, setAssetsList] = useState([
    { id: '1', name: 'Servidor Dell PowerEdge R760', category: 'Infraestrutura', cost: 'R$ 24.500' },
    { id: '2', name: 'MacBook Pro M3 Max (Felipe)', category: 'Equipamentos', cost: 'R$ 32.000' }
  ]);
  const [sapInvoices, setSapInvoices] = useState([
    { id: 'INV-4401', client: 'Petrobras Distribuidora', value: 'R$ 1.250.000', status: 'Aprovada' },
    { id: 'INV-4402', client: 'Vale S.A.', value: 'R$ 940.000', status: 'Pendente' }
  ]);
  const [gameBoard, setGameBoard] = useState<(string | null)[]>(Array(9).fill(null));
  const [gameXNext, setGameXNext] = useState(true);

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

  useEffect(() => {
    setGameBoard(Array(9).fill(null));
    setGameXNext(true);
    setGtaLog(['Bem-vindo a Flose Vice City. Selecione uma missão.']);
    setGtaStats({ money: 100, respect: 20, wanted: 0 });
    setDataLakeSyncing(false);
    setDataLakeProgress(0);
    setDataLakeStatus('Pronto para replicação');

    const symbols = ['🎮', '🕹️', '🛡️', '📊', '🎮', '🕹️', '🛡️', '📊'];
    const shuffled = symbols
      .map((symbol, idx) => ({ id: idx, symbol, flipped: false, matched: false }))
      .sort(() => Math.random() - 0.5);
    setMemoryCards(shuffled);
    setMemorySelected([]);

    const currentDec = decisions.find(d => d.id === selectedScreenKey) || decisions[0];
    if (currentDec?.generatedFile) {
      fetch(`http://localhost:5001/api/code?file=${currentDec.generatedFile}`)
        .then(res => res.json())
        .then(data => setSelectedScreenContent(data.content || ''))
        .catch(err => console.error('Erro ao buscar código:', err));
    } else {
      setSelectedScreenContent('');
    }
  }, [selectedScreenKey, decisions]);

  const handleSelectAgentToggle = (id: string) => {
    setSelectedAgentIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  return (
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

            {/* OrgChart Selection */}
            <OrgChart 
              agents={agents} 
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
            <CompanyPulse agents={agents} />
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
                        <div key={agent.id} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.01)', borderRadius: '8px', border: '1px solid var(--border-color)', opacity: 0.5 }}>
                          <span style={{ fontSize: '1.5rem', filter: 'grayscale(100%)' }}>{agent.avatar}</span>
                          <div>
                            <strong style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textDecoration: 'line-through' }}>{agent.name}</strong>
                            <p style={{ margin: 0, fontSize: '0.7rem', color: 'var(--text-muted)' }}>{agent.role}</p>
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
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h1 style={{ fontSize: '2.25rem', fontWeight: 800, textAlign: 'left' }}>
                Protótipos & <span className="text-gradient">Telas Autônomas</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Veja e interaja com os protótipos de interface gerados em tempo real pelos agentes de IA a partir de suas ordens no Chamber.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '24px', alignItems: 'start' }}>
              {/* Seletor de Telas */}
              <div className="glass" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
                <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-secondary)' }}>📄 Entregas Recentes</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '550px', overflowY: 'auto' }}>
                  {decisions.length === 0 ? (
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhum protótipo disponível. Envie um comando na Sala de Decisão primeiro.</span>
                  ) : (
                    decisions.map((dec) => (
                      <button
                        key={dec.id}
                        onClick={() => {
                          setSelectedScreenKey(dec.id);
                          setLoginSuccess(false);
                          setScanActive(false);
                          setScanProgress(0);
                        }}
                        style={{
                          padding: '10px 14px',
                          borderRadius: '8px',
                          border: selectedScreenKey === dec.id ? '1px solid var(--color-primary)' : '1px solid var(--border-color)',
                          background: selectedScreenKey === dec.id ? 'rgba(139, 92, 246, 0.05)' : 'var(--bg-secondary)',
                          color: selectedScreenKey === dec.id ? 'var(--color-primary)' : 'var(--text-primary)',
                          cursor: 'pointer',
                          textAlign: 'left',
                          width: '100%',
                          fontSize: '0.8rem',
                          fontWeight: selectedScreenKey === dec.id ? 700 : 500
                        }}
                      >
                        <div style={{ fontWeight: 600, color: selectedScreenKey === dec.id ? 'var(--color-primary)' : 'var(--text-muted)' }}>{dec.issueKey}</div>
                        <div style={{ marginTop: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{dec.issueSummary}</div>
                      </button>
                    ))
                  )}
                </div>
              </div>

              {/* Visualizador do Protótipo */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {(() => {
                  const currentDec = decisions.find(d => d.id === selectedScreenKey) || decisions[0];
                  if (!currentDec) {
                    return (
                      <div className="glass" style={{ padding: '40px', color: 'var(--text-muted)', fontStyle: 'italic', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        Nenhum protótipo selecionado. Escolha um item ao lado.
                      </div>
                    );
                  }

                  const textLower = currentDec.issueSummary.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
                  let screenType = 'general';
                  if (textLower.includes('login') || textLower.includes('autentic') || textLower.includes('senha')) {
                    screenType = 'login';
                  } else if (textLower.includes('dashboard') || textLower.includes('metricas') || textLower.includes('relatorio') || textLower.includes('grafic') || textLower.includes('dados')) {
                    screenType = 'dashboard';
                  } else if (textLower.includes('seguranca') || textLower.includes('secops') || textLower.includes('cyber') || textLower.includes('proteg') || textLower.includes('protect')) {
                    screenType = 'secops';
                  } else if (textLower.includes('memoria')) {
                    screenType = 'memory';
                  } else if (textLower.includes('gta')) {
                    screenType = 'gta';
                  } else if (textLower.includes('datalake') || textLower.includes('gcp') || textLower.includes('sqlserver') || textLower.includes('repli') || textLower.includes('etl')) {
                    screenType = 'datalake';
                  } else if (textLower.includes('ativo') || textLower.includes('patrimonio') || textLower.includes('inventar')) {
                    screenType = 'assets';
                  } else if (textLower.includes('sap') || textLower.includes('mm') || textLower.includes('sd') || textLower.includes('fatura') || textLower.includes('invoice')) {
                    screenType = 'sap';
                  } else if (textLower.includes('jogo') || textLower.includes('velha') || textLower.includes('game') || textLower.includes('tictactoe')) {
                    screenType = 'game';
                  }

                  return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                      {/* Metadados */}
                      <div className="glass" style={{ padding: '16px 20px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '12px', textAlign: 'left' }}>
                        <div>
                          <span style={{ fontSize: '0.75rem', background: 'var(--bg-tertiary)', padding: '2px 8px', borderRadius: '4px', color: 'var(--color-secondary)', fontWeight: 600 }}>{currentDec.issueKey || 'CUSTOM'}</span>
                          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, margin: '4px 0 0 0' }}>{currentDec.issueSummary}</h2>
                          <p style={{ margin: '4px 0 0 0', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                            Desenvolvido por <strong>{currentDec.executorName || 'David Dev'}</strong> ({currentDec.executorRole || 'Developer Sênior'})
                          </p>
                        </div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'right' }}>
                          <div>🌿 Branch: <code title={currentDec.gitBranchName}>{shortenBranch(currentDec.gitBranchName)}</code></div>
                          {currentDec.commitHash && <div>💾 Commit: <code style={{ color: '#fbbf24' }}>{currentDec.commitHash}</code></div>}
                        </div>
                      </div>

                      {/* Sprint Tickets da Entrega */}
                      {currentDec.sprintTickets && currentDec.sprintTickets.length > 0 && (
                        <div className="glass" style={{ padding: '12px 16px', display: 'flex', flexDirection: 'column', gap: '8px', textAlign: 'left', marginBottom: '8px' }}>
                          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>📋 Chamados Individuais da Sprint (Jira)</span>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                            {currentDec.sprintTickets.map((ticket: any, idx: number) => (
                              <div
                                key={idx}
                                style={{
                                  padding: '6px 12px',
                                  background: 'rgba(255, 255, 255, 0.02)',
                                  border: '1px solid var(--border-color)',
                                  borderRadius: '6px',
                                  fontSize: '0.7rem',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '8px'
                                }}
                              >
                                <span>{ticket.agentAvatar}</span>
                                <div>
                                  <strong style={{ color: '#fff' }}>{ticket.ticketKey}</strong>
                                  <span style={{ color: 'var(--text-muted)', marginLeft: '4px' }}>{ticket.agentName} ({ticket.status})</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Visualizer Tab Bar */}
                      <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
                        <button
                          onClick={() => setVisualizerTab('staging')}
                          style={{
                            padding: '8px 16px',
                            borderRadius: '6px',
                            border: 'none',
                            background: visualizerTab === 'staging' ? 'var(--color-primary)' : 'var(--bg-tertiary)',
                            color: '#fff',
                            fontWeight: 600,
                            fontSize: '0.8rem',
                            cursor: 'pointer',
                            transition: 'all 0.2s ease'
                          }}
                        >
                          🖥️ Protótipo Staging
                        </button>
                        <button
                          onClick={() => setVisualizerTab('code')}
                          style={{
                            padding: '8px 16px',
                            borderRadius: '6px',
                            border: 'none',
                            background: visualizerTab === 'code' ? 'var(--color-primary)' : 'var(--bg-tertiary)',
                            color: '#fff',
                            fontWeight: 600,
                            fontSize: '0.8rem',
                            cursor: 'pointer',
                            transition: 'all 0.2s ease'
                          }}
                        >
                          📜 Código Fonte (Gemma 4)
                        </button>
                      </div>

                      {visualizerTab === 'staging' ? (
                        <div style={{
                          background: '#090d16',
                          borderRadius: '12px',
                          border: '4px solid #1f2937',
                          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.6)',
                          overflow: 'hidden',
                          display: 'flex',
                          flexDirection: 'column',
                          minHeight: '480px'
                        }}>
                        {/* Browser Bar */}
                        <div style={{
                          background: '#1f2937',
                          padding: '10px 16px',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          borderBottom: '1px solid #374151'
                        }}>
                          <div style={{ display: 'flex', gap: '6px' }}>
                            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }}></span>
                            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b', display: 'inline-block' }}></span>
                            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
                          </div>
                          <div style={{
                            flex: 1,
                            background: '#111827',
                            borderRadius: '6px',
                            padding: '4px 12px',
                            color: '#9ca3af',
                            fontSize: '0.75rem',
                            textAlign: 'left',
                            fontFamily: 'monospace',
                            display: 'flex',
                            justifyContent: 'space-between'
                          }}>
                            <span>https://staging.flosestartup.ai/{currentDec.issueKey?.toLowerCase() || 'preview'}</span>
                            <span style={{ color: '#10b981', fontWeight: 600 }}>✓ SSL Ativo</span>
                          </div>
                        </div>

                        {/* Rendering Screen Content */}
                        <div style={{ flex: 1, padding: '24px', display: 'flex', justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(circle at top, #0f172a 0%, #020617 100%)' }}>
                          
                          {/* 1. Login Screen */}
                          {screenType === 'login' && (
                            <div className="glass" style={{
                              width: '100%',
                              maxWidth: '360px',
                              padding: '24px',
                              borderRadius: '12px',
                              border: '1px solid rgba(255, 255, 255, 0.08)',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '16px',
                              textAlign: 'left'
                            }}>
                              {loginSuccess ? (
                                <div style={{ textAlign: 'center', padding: '20px 0', display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'center' }}>
                                  <span style={{ fontSize: '3rem' }}>🎉</span>
                                  <h4 style={{ color: '#34d399', fontSize: '1.2rem', margin: 0 }}>Acesso Permitido!</h4>
                                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>Bem-vindo à área de staging protegida da Flose Startup.</p>
                                  <button onClick={() => setLoginSuccess(false)} style={{ padding: '6px 12px', borderRadius: '6px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.75rem', cursor: 'pointer', marginTop: '8px' }}>Sair</button>
                                </div>
                              ) : (
                                <>
                                  <div style={{ textAlign: 'center', marginBottom: '8px' }}>
                                    <strong style={{ fontSize: '1.25rem', color: '#fff' }}>Entrar na Plataforma</strong>
                                    <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>Staging Protegida por Gemma Autônoma</p>
                                  </div>
                                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Endereço de E-mail</label>
                                    <input type="email" placeholder="ceo@flosestartup.ai" defaultValue="ceo@flosestartup.ai" style={{ padding: '8px 12px', borderRadius: '6px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.8rem', outline: 'none' }} />
                                  </div>
                                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Senha de Acesso</label>
                                    <input type="password" placeholder="••••••••" defaultValue="123456" style={{ padding: '8px 12px', borderRadius: '6px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.8rem', outline: 'none' }} />
                                  </div>
                                  <button
                                    onClick={() => setLoginSuccess(true)}
                                    className="bg-gradient"
                                    style={{
                                      padding: '10px',
                                      borderRadius: '6px',
                                      border: 'none',
                                      color: '#fff',
                                      fontWeight: 600,
                                      cursor: 'pointer',
                                      textAlign: 'center',
                                      marginTop: '8px',
                                      width: '100%'
                                    }}
                                  >
                                    Autenticar no Sistema
                                  </button>
                                </>
                              )}
                            </div>
                          )}

                          {/* 2. Analytics Dashboard */}
                          {screenType === 'dashboard' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                  <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff' }}>Painel Executivo de Métricas</h4>
                                  <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Dados dinâmicos de performance da aplicação</p>
                                </div>
                                <button
                                  onClick={() => {
                                    setDashboardMetrics({
                                      users: Math.floor(10000 + Math.random() * 5000),
                                      conversion: +(2.5 + Math.random() * 2).toFixed(2),
                                      load: Math.floor(10 + Math.random() * 60)
                                    });
                                  }}
                                  style={{ padding: '6px 12px', borderRadius: '6px', background: 'var(--color-primary)', border: 'none', color: '#fff', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}
                                >
                                  🔄 Atualizar Métricas
                                </button>
                              </div>

                              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                                <div className="glass" style={{ padding: '16px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Usuários Ativos</span>
                                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-primary)', marginTop: '4px' }}>{dashboardMetrics.users.toLocaleString()}</div>
                                </div>
                                <div className="glass" style={{ padding: '16px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Taxa de Conversão</span>
                                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#10b981', marginTop: '4px' }}>{dashboardMetrics.conversion}%</div>
                                </div>
                                <div className="glass" style={{ padding: '16px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Carga do Servidor</span>
                                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: dashboardMetrics.load > 60 ? '#ef4444' : '#fbbf24', marginTop: '4px' }}>{dashboardMetrics.load}%</div>
                                </div>
                              </div>

                              {/* Simulated Graph Chart visual */}
                              <div className="glass" style={{ padding: '20px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Evolução de Tráfego Corporativo (Últimas 24h)</span>
                                <div style={{ height: '120px', display: 'flex', alignItems: 'flex-end', gap: '8px', paddingBottom: '10px', borderBottom: '1px solid var(--border-color)' }}>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '30%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '45%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '60%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '55%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '70%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-primary)', height: '90%', borderRadius: '4px' }}></div>
                                  <div style={{ flex: 1, background: 'var(--color-secondary)', height: `${dashboardMetrics.load}%`, borderRadius: '4px', transition: 'height 0.4s ease' }}></div>
                                </div>
                              </div>
                            </div>
                          )}

                          {/* 3. SecOps System Defense */}
                          {screenType === 'secops' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                              <div className="glass" style={{ padding: '20px', borderRadius: '12px', border: '1px solid rgba(239, 68, 68, 0.2)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                  <h4 style={{ margin: 0, color: '#ef4444', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }}></span>
                                    Flose SecOps Guard Center
                                  </h4>
                                  <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Proteção perimetral contra intrusões</p>
                                </div>
                                <span style={{ padding: '4px 10px', borderRadius: '4px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', color: '#10b981', fontSize: '0.8rem', fontWeight: 600 }}>SISTEMA SEGURO</span>
                              </div>

                              <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '12px' }}>
                                <div className="glass" style={{ padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                  <span style={{ fontSize: '0.75rem', fontWeight: 600 }}>Scanner de Vulnerabilidades</span>
                                  {scanActive ? (
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                      <div style={{ fontSize: '0.8rem', color: '#fbbf24' }}>Escaneando dependências npm... {scanProgress}%</div>
                                      <div style={{ width: '100%', height: '6px', background: 'var(--bg-tertiary)', borderRadius: '3px', overflow: 'hidden' }}>
                                        <div style={{ width: `${scanProgress}%`, height: '100%', background: '#fbbf24', transition: 'width 0.1s ease' }}></div>
                                      </div>
                                    </div>
                                  ) : (
                                    <button
                                      onClick={() => {
                                        setScanActive(true);
                                        setScanProgress(0);
                                        const interval = setInterval(() => {
                                          setScanProgress(p => {
                                            if (p >= 100) {
                                              clearInterval(interval);
                                              setTimeout(() => setScanActive(false), 1000);
                                              return 100;
                                            }
                                            return p + 10;
                                          });
                                        }, 200);
                                      }}
                                      style={{ padding: '8px', borderRadius: '6px', background: '#fbbf24', border: 'none', color: '#000', fontSize: '0.75rem', fontWeight: 700, cursor: 'pointer', width: '100%' }}
                                    >
                                      🛡️ Iniciar Varredura de Portas
                                    </button>
                                  )}
                                </div>
                                <div className="glass" style={{ padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                  <strong>Logs SecOps:</strong>
                                  <div style={{ marginTop: '4px', fontFamily: 'monospace', fontSize: '0.65rem', display: 'flex', flexDirection: 'column', gap: '2px' }}>
                                    <div>[info] Port 443 listening...</div>
                                    <div>[info] SSL handshake OK</div>
                                    <div>[info] DDoS Shield: Active</div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          )}

                          {/* 4. General Developer execution console */}
                          {screenType === 'general' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
                              <h4 style={{ margin: 0, fontSize: '0.95rem', color: '#fff' }}>Terminal de Execução do Código</h4>
                              <div style={{
                                background: '#020617',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                padding: '16px',
                                fontFamily: 'monospace',
                                fontSize: '0.8rem',
                                color: '#38bdf8',
                                display: 'flex',
                                flexDirection: 'column',
                                gap: '6px',
                                minHeight: '160px'
                              }}>
                                <div style={{ color: '#64748b' }}>// Executando script de staging gerado autonomamente</div>
                                <div>$ node src/simulations/{currentDec.issueKey || 'MOCK'}-code.ts</div>
                                <div style={{ color: '#10b981' }}>&gt; [Consenso Carregado] {currentDec.decision}</div>
                                <div style={{ color: '#f59e0b' }}>&gt; Autor: {currentDec.executorName || 'David Dev'} ({currentDec.executorRole})</div>
                                <div style={{ color: '#fff' }}>&gt; Status: Sucesso. Alterações commitadas no Git.</div>
                              </div>
                            </div>
                          )}

                          {/* 4. Memory Game Screen */}
                          {screenType === 'memory' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '14px', alignItems: 'center' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700 }}>Jogo da Memória</h4>
                              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-secondary)', textAlign: 'center' }}>Clique nas cartas para encontrar os pares.</p>
                              
                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', width: '260px' }}>
                                {memoryCards.map((card) => (
                                  <button
                                    key={card.id}
                                    onClick={() => {
                                      if (card.flipped || card.matched || memorySelected.length >= 2) return;
                                      const nextCards = memoryCards.map(c => c.id === card.id ? { ...c, flipped: true } : c);
                                      setMemoryCards(nextCards);
                                      
                                      const newSel = [...memorySelected, card.id];
                                      setMemorySelected(newSel);

                                      if (newSel.length === 2) {
                                        const first = memoryCards.find(c => c.id === newSel[0])!;
                                        const second = card;
                                        if (first.symbol === second.symbol) {
                                          setTimeout(() => {
                                            setMemoryCards(prev => prev.map(c => (c.id === first.id || c.id === second.id) ? { ...c, matched: true } : c));
                                            setMemorySelected([]);
                                          }, 500);
                                        } else {
                                          setTimeout(() => {
                                            setMemoryCards(prev => prev.map(c => (c.id === first.id || c.id === second.id) ? { ...c, flipped: false } : c));
                                            setMemorySelected([]);
                                          }, 1000);
                                        }
                                      }
                                    }}
                                    style={{
                                      height: '60px',
                                      background: card.flipped || card.matched ? 'var(--bg-tertiary)' : 'var(--color-primary)',
                                      border: '1px solid var(--border-color)',
                                      borderRadius: '8px',
                                      fontSize: '1.5rem',
                                      color: '#fff',
                                      cursor: 'pointer',
                                      transition: 'all 0.2s'
                                    }}
                                  >
                                    {card.flipped || card.matched ? card.symbol : '❓'}
                                  </button>
                                ))}
                              </div>
                              <div style={{ fontSize: '0.85rem', color: '#10b981', fontWeight: 600 }}>
                                  {memoryCards.every(c => c.matched) ? '🎉 Todos os pares encontrados!' : 'Encontre os pares correspondentes.'}
                              </div>
                            </div>
                          )}

                          {/* 5. GTA 6 Simulator Screen */}
                          {screenType === 'gta' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700, textAlign: 'center' }}>Flose Vice City Console</h4>
                              
                              <div style={{ display: 'flex', justifyContent: 'space-around', background: 'rgba(255,255,255,0.02)', padding: '8px', borderRadius: '8px', fontSize: '0.8rem' }}>
                                <div>💰 Dinheiro: <strong style={{ color: '#10b981' }}>${gtaStats.money}</strong></div>
                                <div>⭐ Respeito: <strong style={{ color: 'var(--color-primary)' }}>{gtaStats.respect}</strong></div>
                                <div>🚨 Nível: <strong style={{ color: '#ef4444' }}>{'★'.repeat(gtaStats.wanted) || 'Clean'}</strong></div>
                              </div>

                              <div style={{ background: '#020617', padding: '12px', borderRadius: '8px', height: '120px', overflowY: 'auto', fontSize: '0.75rem', fontFamily: 'monospace', color: '#38bdf8', border: '1px solid var(--border-color)' }}>
                                {gtaLog.map((log, i) => <div key={i} style={{ marginBottom: '4px' }}>&gt; {log}</div>)}
                              </div>

                              <div style={{ display: 'flex', gap: '8px' }}>
                                <button
                                  onClick={() => {
                                    setGtaStats(prev => ({ ...prev, money: prev.money + 50, respect: prev.respect + 5, wanted: Math.min(prev.wanted + 1, 5) }));
                                    setGtaLog(prev => [...prev, 'Roubou um carro esporte na avenida principal! +$50.']);
                                  }}
                                  style={{ flex: 1, padding: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '6px', fontSize: '0.75rem', cursor: 'pointer' }}
                                >
                                  🚗 Roubar Carro
                                </button>
                                <button
                                  onClick={() => {
                                    setGtaStats(prev => ({ ...prev, money: prev.money + 200, respect: prev.respect + 15, wanted: Math.min(prev.wanted + 2, 5) }));
                                    setGtaLog(prev => [...prev, 'Assaltou a joalheria de Vice Point! +$200.']);
                                  }}
                                  style={{ flex: 1, padding: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '6px', fontSize: '0.75rem', cursor: 'pointer' }}
                                >
                                  💰 Assaltar Loja
                                </button>
                                <button
                                  onClick={() => {
                                    setGtaStats(prev => ({ ...prev, wanted: 0, money: Math.max(prev.money - 30, 0) }));
                                    setGtaLog(prev => [...prev, 'Subornou a polícia local! -$30.']);
                                  }}
                                  style={{ flex: 1, padding: '8px', background: '#ef4444', color: '#fff', border: 'none', borderRadius: '6px', fontSize: '0.75rem', cursor: 'pointer' }}
                                >
                                  🚨 Subornar
                                </button>
                              </div>
                            </div>
                          )}

                          {/* 6. Data Lake GCP ETL Screen */}
                          {screenType === 'datalake' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '14px', textAlign: 'left' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700, textAlign: 'center' }}>Data Lake GCP Ingestor</h4>
                              
                              <div style={{ background: '#020617', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '0.8rem' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                                  <span>Origem:</span> <strong style={{ color: '#60a5fa' }}>SQL Server Local</strong>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                                  <span>Destino:</span> <strong style={{ color: '#34d399' }}>GCP BigQuery & GCS</strong>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                  <span>Status:</span> <strong style={{ color: dataLakeSyncing ? '#f59e0b' : '#10b981' }}>{dataLakeStatus}</strong>
                                </div>
                              </div>

                              {dataLakeSyncing && (
                                <div style={{ width: '100%', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', height: '16px', overflow: 'hidden', position: 'relative' }}>
                                  <div style={{ width: `${dataLakeProgress}%`, height: '100%', background: 'var(--color-primary)', transition: 'width 0.2s' }} />
                                  <span style={{ position: 'absolute', width: '100%', textAlign: 'center', fontSize: '0.65rem', color: '#fff', fontWeight: 'bold', top: 0 }}>{dataLakeProgress}%</span>
                                </div>
                              )}

                              <button
                                onClick={() => {
                                  if (dataLakeSyncing) return;
                                  setDataLakeSyncing(true);
                                  setDataLakeProgress(0);
                                  setDataLakeStatus('Iniciando handshake SQL Server...');
                                  
                                  const interval = setInterval(() => {
                                    setDataLakeProgress(prev => {
                                      if (prev >= 100) {
                                        clearInterval(interval);
                                        setDataLakeSyncing(false);
                                        setDataLakeStatus('Ingestão concluída! 12,490 linhas migradas para o BigQuery.');
                                        return 100;
                                      }
                                      if (prev === 30) setDataLakeStatus('Extraindo tabelas relacionais...');
                                      if (prev === 60) setDataLakeStatus('Efetuando upload para GCS Staging...');
                                      if (prev === 85) setDataLakeStatus('Efetuando merge no BigQuery DWH...');
                                      return prev + 10;
                                    });
                                  }, 300);
                                }}
                                style={{
                                  padding: '10px',
                                  background: 'var(--color-primary)',
                                  color: '#fff',
                                  border: 'none',
                                  borderRadius: '6px',
                                  fontWeight: 'bold',
                                  cursor: 'pointer',
                                  fontSize: '0.8rem'
                                }}
                              >
                                {dataLakeSyncing ? '⌛ Sincronizando...' : '🚀 Iniciar Replicação de Dados'}
                              </button>
                            </div>
                          )}

                          {/* 7. Asset Management Grid Screen */}
                          {screenType === 'assets' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700, textAlign: 'center' }}>Controle de Ativos Flose</h4>
                              
                              <div style={{ maxHeight: '150px', overflowY: 'auto', border: '1px solid var(--border-color)', borderRadius: '6px' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem' }}>
                                  <thead>
                                    <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border-color)' }}>
                                      <th style={{ padding: '6px' }}>Nome</th>
                                      <th style={{ padding: '6px' }}>Categoria</th>
                                      <th style={{ padding: '6px', textAlign: 'right' }}>Valor</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {assetsList.map((asset) => (
                                      <tr key={asset.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)' }}>
                                        <td style={{ padding: '6px' }}>{asset.name}</td>
                                        <td style={{ padding: '6px' }}>{asset.category}</td>
                                        <td style={{ padding: '6px', textAlign: 'right', color: '#10b981' }}>{asset.cost}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>

                              <button
                                onClick={() => {
                                  const name = prompt('Nome do novo ativo:');
                                  if (!name) return;
                                  const category = prompt('Categoria (ex: Equipamentos):') || 'Geral';
                                  const cost = prompt('Valor (ex: R$ 5.000):') || 'R$ 0';
                                  setAssetsList(prev => [...prev, { id: Date.now().toString(), name, category, cost }]);
                                }}
                                style={{
                                  padding: '8px',
                                  background: 'var(--color-primary)',
                                  color: '#fff',
                                  border: 'none',
                                  borderRadius: '6px',
                                  fontSize: '0.75rem',
                                  fontWeight: 'bold',
                                  cursor: 'pointer'
                                }}
                              >
                                ➕ Cadastrar Novo Ativo Patrimonial
                              </button>
                            </div>
                          )}

                          {/* 8. SAP MM/SD Procurement Screen */}
                          {screenType === 'sap' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700, textAlign: 'center' }}>SAP MM/SD Procurement</h4>
                              
                              <div style={{ border: '1px solid var(--border-color)', borderRadius: '6px', overflow: 'hidden' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem' }}>
                                  <thead>
                                    <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border-color)' }}>
                                      <th style={{ padding: '6px' }}>Fatura</th>
                                      <th style={{ padding: '6px' }}>Cliente</th>
                                      <th style={{ padding: '6px', textAlign: 'right' }}>Total</th>
                                      <th style={{ padding: '6px', textAlign: 'center' }}>Status</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {sapInvoices.map((inv) => (
                                      <tr key={inv.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)' }}>
                                        <td style={{ padding: '6px', fontWeight: 'bold' }}>{inv.id}</td>
                                        <td style={{ padding: '6px' }}>{inv.client}</td>
                                        <td style={{ padding: '6px', textAlign: 'right', color: '#38bdf8' }}>{inv.value}</td>
                                        <td style={{ padding: '6px', textAlign: 'center' }}>
                                          <span style={{
                                            padding: '2px 6px',
                                            borderRadius: '4px',
                                            fontSize: '0.62rem',
                                            background: inv.status === 'Aprovada' ? 'rgba(16,185,129,0.1)' : 'rgba(245,158,11,0.1)',
                                            color: inv.status === 'Aprovada' ? '#10b981' : '#f59e0b'
                                          }}>{inv.status}</span>
                                        </td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>

                              <button
                                onClick={() => {
                                  setSapInvoices(prev => prev.map(inv => inv.status !== 'Aprovada' ? { ...inv, status: 'Aprovada' } : inv));
                                  alert('Integração Cortex & SAP executada! Contas a receber atualizadas no GCP DWH.');
                                }}
                                style={{
                                  padding: '8px',
                                  background: '#10b981',
                                  color: '#fff',
                                  border: 'none',
                                  borderRadius: '6px',
                                  fontSize: '0.75rem',
                                  fontWeight: 'bold',
                                  cursor: 'pointer'
                                }}
                              >
                                ⚙️ Executar Integração de Cobranças
                              </button>
                            </div>
                          )}

                          {/* 9. Tic-Tac-Toe Game Screen */}
                          {screenType === 'game' && (
                            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center' }}>
                              <h4 style={{ margin: 0, fontSize: '1.1rem', color: '#fff', fontWeight: 700 }}>Jogo da Velha</h4>
                              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Instância interativa gerada autonomamente.</p>
                              
                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', width: '260px', height: '260px' }}>
                                {gameBoard.map((val, idx) => (
                                  <button
                                    key={idx}
                                    onClick={() => {
                                      const checkWin = (b: (string | null)[]) => {
                                        const lines = [
                                          [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]
                                        ];
                                        return lines.some(l => b[l[0]] && b[l[0]] === b[l[1]] && b[l[0]] === b[l[2]]);
                                      };
                                      if (val || checkWin(gameBoard)) return;
                                      
                                      const nextB = [...gameBoard];
                                      nextB[idx] = gameXNext ? 'X' : 'O';
                                      setGameBoard(nextB);
                                      setGameXNext(!gameXNext);
                                    }}
                                    style={{
                                      background: 'rgba(255,255,255,0.04)',
                                      border: '1px solid var(--border-color)',
                                      borderRadius: '8px',
                                      fontSize: '2rem',
                                      color: val === 'X' ? 'var(--color-primary)' : 'var(--color-secondary)',
                                      fontWeight: 'bold',
                                      cursor: 'pointer',
                                      outline: 'none',
                                      transition: 'all 0.2s ease'
                                    }}
                                  >
                                    {val}
                                  </button>
                                ))}
                              </div>

                              <div style={{ fontSize: '0.9rem', color: '#34d399', fontWeight: 600 }}>
                                {(() => {
                                  const checkWin = (b: (string | null)[]) => {
                                    const lines = [
                                      [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]
                                    ];
                                    for (const l of lines) {
                                      if (b[l[0]] && b[l[0]] === b[l[1]] && b[l[0]] === b[l[2]]) return b[l[0]];
                                    }
                                    return null;
                                  };
                                  const winner = checkWin(gameBoard);
                                  if (winner) return `🏆 Vencedor: ${winner}!`;
                                  if (gameBoard.every(v => v !== null)) return '🤝 Empate!';
                                  return `Vez de: ${gameXNext ? 'X' : 'O'}`;
                                })()}
                              </div>

                              <button
                                onClick={() => {
                                  setGameBoard(Array(9).fill(null));
                                  setGameXNext(true);
                                }}
                                style={{
                                  padding: '8px 16px',
                                  borderRadius: '6px',
                                  border: 'none',
                                  background: 'var(--color-primary)',
                                  color: '#fff',
                                  fontSize: '0.8rem',
                                  fontWeight: 'bold',
                                  cursor: 'pointer',
                                  marginTop: '4px'
                                }}
                              >
                                🔄 Reiniciar Partida
                              </button>
                            </div>
                          )}

                        </div>
                      </div>
                      ) : (
                        <div className="glass" style={{
                          background: '#020617',
                          borderRadius: '12px',
                          border: '1px solid var(--border-color)',
                          padding: '24px',
                          textAlign: 'left',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '12px',
                          minHeight: '480px',
                          maxHeight: '650px',
                          overflowY: 'auto'
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>📄 Arquivo: <code>{currentDec.generatedFile || 'default.ts'}</code></span>
                            <span style={{ fontSize: '0.72rem', background: '#10b981', padding: '2px 8px', borderRadius: '4px', color: '#fff', fontWeight: 600 }}>CÓDIGO DE PRODUÇÃO (GEMMA 4)</span>
                          </div>
                          <pre style={{
                            margin: 0,
                            fontFamily: 'monospace',
                            fontSize: '0.82rem',
                            color: '#e2e8f0',
                            whiteSpace: 'pre-wrap',
                            lineHeight: '1.5',
                            background: '#090d16',
                            padding: '16px',
                            borderRadius: '8px',
                            border: '1px solid rgba(255, 255, 255, 0.04)',
                            overflowX: 'auto'
                          }}>
                            {selectedScreenContent || '// Carregando código fonte...' }
                          </pre>
                        </div>
                      )}
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>
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
  );
}

export default App;
