import { useState, useEffect } from 'react';
import { Agent, AgentCard } from './components/AgentCard';
import { OrgChart } from './components/OrgChart';
import { JiraDashboard } from './components/JiraDashboard';
import { GemmaConsole } from './components/GemmaConsole';
import { Award, Briefcase, Cpu, FileText, Layers, Terminal } from 'lucide-react';

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);
  const [selectedIssue, setSelectedIssue] = useState<{ key: string; summary: string; description: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'backlog' | 'agents' | 'docs'>('dashboard');

  useEffect(() => {
    fetch('http://localhost:5001/api/agents')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
        // Pre-select C-Levels and Directors by default to make it ready to go
        const defaultIds = data.filter((a: Agent) => a.level === 'C-Level' || a.level === 'Diretor').map((a: Agent) => a.id);
        setSelectedAgentIds(defaultIds);
      })
      .catch(err => console.error('Erro ao buscar agentes:', err));
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
