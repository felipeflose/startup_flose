import { useState, useEffect } from 'react';
import type { Agent } from './components/AgentCard';
import { AgentCard } from './components/AgentCard';
import { OrgChart } from './components/OrgChart';
import { JiraDashboard } from './components/JiraDashboard';
import { GemmaConsole } from './components/GemmaConsole';
import { Briefcase, Cpu, FileText, Layers, Terminal, History, Users, Monitor } from 'lucide-react';

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);
  const [selectedIssue, setSelectedIssue] = useState<{ key: string; summary: string; description: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'backlog' | 'agents' | 'docs' | 'decisions' | 'rh' | 'screens'>('dashboard');
  const [decisions, setDecisions] = useState<any[]>([]);
  const [selectedScreenKey, setSelectedScreenKey] = useState<string>('');
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [dashboardMetrics, setDashboardMetrics] = useState({ users: 12490, conversion: 3.42, load: 24 });
  const [scanActive, setScanActive] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);

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
        const defaultIds = data.filter((a: Agent) => a.level === 'C-Level' || a.level === 'Diretor').map((a: Agent) => a.id);
        setSelectedAgentIds(defaultIds);
      })
      .catch(err => console.error('Erro ao buscar agentes:', err));

    fetchDecisions();
    fetchAgents();
  }, []);

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
                            <span>🌿 Branch Git: <code style={{ color: '#a5b4fc' }}>{dec.gitBranchName}</code></span>
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
                              {dec.githubIssueUrl}
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
                        {dec.generatedFile && <span> | 📄 <code>{dec.generatedFile}</code></span>}
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
                          <div>🌿 Branch: <code>{currentDec.gitBranchName}</code></div>
                          {currentDec.commitHash && <div>💾 Commit: <code style={{ color: '#fbbf24' }}>{currentDec.commitHash}</code></div>}
                        </div>
                      </div>

                      {/* Device Simulator Frame */}
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

                        </div>
                      </div>
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
      </main>
    </div>
  );
}

export default App;
