import { useState, useEffect } from 'react';
import type { Agent } from './components/AgentCard';
import { AgentCard } from './components/AgentCard';
import { OrgChart } from './components/OrgChart';
import { JiraDashboard } from './components/JiraDashboard';
import { GemmaConsole } from './components/GemmaConsole';
import { Briefcase, Cpu, FileText, Layers, Terminal, History, Users } from 'lucide-react';

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);
  const [selectedIssue, setSelectedIssue] = useState<{ key: string; summary: string; description: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'backlog' | 'agents' | 'docs' | 'decisions' | 'rh'>('dashboard');
  const [decisions, setDecisions] = useState<any[]>([]);

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
              allAgentIds={agents.map(a => a.id)}
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
                Painel de <span className="text-gradient">RH & Gestão Corporativa</span>
              </h1>
              <p style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                Simule a governança da startup: contrate inteligências, desligue colaboradores, emita feedbacks de desempenho e defina a escala de horários.
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start' }}>
              {/* Contratar Agente */}
              <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>➕ Contratar Novo Colaborador (IA)</h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.currentTarget);
                    const name = formData.get('name') as string;
                    const role = formData.get('role') as string;
                    const level = formData.get('level') as string;
                    const avatar = formData.get('avatar') as string;
                    const advantage = formData.get('advantage') as string;
                    const disadvantage = formData.get('disadvantage') as string;
                    const dilemma = formData.get('dilemma') as string;
                    const personality = formData.get('personality') as string;

                    try {
                      const res = await fetch('http://localhost:5001/api/agents/hire', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, role, level, avatar, advantage, disadvantage, dilemma, personality })
                      });
                      if (!res.ok) throw new Error('Falha ao contratar agente.');
                      const data = await res.json();
                      alert(`Colaborador ${name} contratado com sucesso! Sincronizado no Jira: ${data.jiraKey || 'N/A'}`);
                      fetchAgents();
                      e.currentTarget.reset();
                    } catch (err: any) {
                      alert(err.message);
                    }
                  }}
                  style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}
                >
                  <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '8px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Nome Completo</label>
                      <input type="text" name="name" required placeholder="Ex: Lucas Cloud" style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }} />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Avatar (Emoji)</label>
                      <input type="text" name="avatar" defaultValue="🤖" placeholder="Ex: 🤖" style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none', textAlign: 'center' }} />
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Cargo / Função</label>
                      <input type="text" name="role" required placeholder="Ex: Dev SecOps" style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }} />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Nível de Governança</label>
                      <select name="level" style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }}>
                        <option value="C-Level">C-Level</option>
                        <option value="Diretor">Diretor</option>
                        <option value="Gerente">Gerente</option>
                        <option value="Coordenador">Coordenador</option>
                        <option value="Analista SR">Analista SR</option>
                      </select>
                    </div>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Principal Vantagem</label>
                    <input type="text" name="advantage" required placeholder="Ex: Foco extremo em segurança e auditoria de código." style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }} />
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Desvantagem / Ponto Fraco</label>
                    <input type="text" name="disadvantage" required placeholder="Ex: Demora a liberar código devido a testes de penetração excessivos." style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }} />
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Dilema Essencial</label>
                    <input type="text" name="dilemma" required placeholder="Ex: Mitigação Total de Riscos vs. Time-to-Market." style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none' }} />
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Personalidade</label>
                    <textarea name="personality" rows={2} required placeholder="Ex: Cauteloso, detalhista, introvertido e fiel a conformidades de segurança." style={{ padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', outline: 'none', resize: 'none' }} />
                  </div>

                  <button type="submit" className="bg-gradient" style={{ padding: '10px', borderRadius: '8px', border: 'none', color: '#fff', fontWeight: 600, cursor: 'pointer', marginTop: '8px', boxShadow: '0 4px 12px rgba(139, 92, 246, 0.3)' }}>
                    Registrar Contratação
                  </button>
                </form>
              </div>

              {/* Lista e Controle de Agentes */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left' }}>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>👥 Quadro de Colaboradores Ativos</h2>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxHeight: '600px', overflowY: 'auto', paddingRight: '4px' }}>
                    {agents.map((agent) => (
                      <div key={agent.id} style={{ padding: '16px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '1.75rem' }}>{agent.avatar}</span>
                            <div>
                              <strong style={{ fontSize: '1rem', color: 'var(--color-primary)' }}>{agent.name}</strong>
                              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-muted)' }}>{agent.role} ({agent.level})</p>
                            </div>
                          </div>
                          
                          {/* Demitir */}
                          <button
                            onClick={async () => {
                              if (!confirm(`Deseja mesmo demitir o colaborador ${agent.name}?`)) return;
                              try {
                                const res = await fetch('http://localhost:5001/api/agents/fire', {
                                  method: 'POST',
                                  headers: { 'Content-Type': 'application/json' },
                                  body: JSON.stringify({ agentId: agent.id })
                                });
                                if (!res.ok) throw new Error('Falha ao demitir.');
                                const data = await res.json();
                                alert(`Colaborador ${agent.name} demitido. Sincronizado no Jira: ${data.jiraKey || 'N/A'}`);
                                fetchAgents();
                              } catch (err: any) {
                                alert(err.message);
                              }
                            }}
                            style={{ padding: '4px 8px', borderRadius: '4px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#f87171', fontSize: '0.7rem', fontWeight: 600, cursor: 'pointer' }}
                          >
                            Demitir
                          </button>
                        </div>

                        {/* Configurações de Jornada e Status */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', background: 'rgba(255, 255, 255, 0.02)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', fontSize: '0.75rem' }}>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <span>Jornada de Trabalho:</span>
                            <input
                              type="text"
                              defaultValue={agent.schedule || '09:00 - 18:00'}
                              onBlur={async (e) => {
                                try {
                                  await fetch('http://localhost:5001/api/agents/schedule', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ agentId: agent.id, schedule: e.target.value, status: agent.status || 'Disponível' })
                                  });
                                } catch (err) {}
                              }}
                              style={{ padding: '4px 8px', borderRadius: '4px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.75rem' }}
                            />
                          </div>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <span>Status Atual:</span>
                            <select
                              defaultValue={agent.status || 'Disponível'}
                              onChange={async (e) => {
                                try {
                                  await fetch('http://localhost:5001/api/agents/schedule', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ agentId: agent.id, schedule: agent.schedule || '09:00 - 18:00', status: e.target.value })
                                  });
                                  fetchAgents();
                                } catch (err) {}
                              }}
                              style={{ padding: '4px 8px', borderRadius: '4px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.75rem' }}
                            >
                              <option value="Disponível">Disponível</option>
                              <option value="Fora de Horário">Fora de Horário</option>
                              <option value="Férias">Férias</option>
                            </select>
                          </div>
                        </div>

                        {/* Enviar Feedback */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Emitir Avaliação de Performance (Feedback):</span>
                          <form
                            onSubmit={async (e) => {
                              e.preventDefault();
                              const fData = new FormData(e.currentTarget);
                              const text = fData.get('feedbackText') as string;
                              const rating = fData.get('rating') as string;
                              if (!text.trim()) return;

                              try {
                                const res = await fetch('http://localhost:5001/api/agents/feedback', {
                                  method: 'POST',
                                  headers: { 'Content-Type': 'application/json' },
                                  body: JSON.stringify({ agentId: agent.id, feedbackText: text, rating })
                                });
                                if (!res.ok) throw new Error('Erro ao enviar feedback.');
                                const data = await res.json();
                                alert(`Feedback registrado! Sincronizado no Jira: ${data.jiraKey || 'N/A'}`);
                                fetchAgents();
                                e.currentTarget.reset();
                              } catch (err: any) {
                                alert(err.message);
                              }
                            }}
                            style={{ display: 'flex', gap: '8px', alignItems: 'stretch' }}
                          >
                            <input
                              type="text"
                              name="feedbackText"
                              required
                              placeholder="Parabéns pela entrega rápida! / Precisa detalhar os testes..."
                              style={{ flex: 1, padding: '6px 10px', borderRadius: '4px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.75rem', outline: 'none' }}
                            />
                            <select name="rating" style={{ padding: '6px', borderRadius: '4px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', color: '#fff', fontSize: '0.75rem' }}>
                              <option value="positivo">👍 Positivo</option>
                              <option value="negativo">👎 Corretivo</option>
                            </select>
                            <button type="submit" style={{ padding: '6px 12px', borderRadius: '4px', background: 'var(--color-primary)', border: 'none', color: '#fff', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}>
                              Enviar
                            </button>
                          </form>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
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
