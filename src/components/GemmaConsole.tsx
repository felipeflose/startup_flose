import React, { useState } from 'react';

interface DebateLog {
  agentId: string;
  name: string;
  role: string;
  avatar: string;
  dilemma: string;
  opinion: string;
  replica?: string;
}

interface GemmaConsoleProps {
  selectedIssue: { key: string; summary: string; description: string } | null;
  selectedAgentIds: string[];
  onDebateComplete?: () => void;
}

export const GemmaConsole: React.FC<GemmaConsoleProps> = ({ selectedIssue, selectedAgentIds, onDebateComplete }) => {
  const [debating, setDebating] = useState(false);
  const [logs, setLogs] = useState<DebateLog[]>([]);
  const [decision, setDecision] = useState<string | null>(null);
  const [jiraResult, setJiraResult] = useState<string | null>(null);
  const [customIdea, setCustomIdea] = useState('');
  const [gitBranch, setGitBranch] = useState<string | null>(null);
  const [githubUrl, setGithubUrl] = useState<string | null>(null);
  const [commandResult, setCommandResult] = useState<{
    actionType: string;
    reasoning: string;
    details: string;
    jiraKey?: string;
  } | null>(null);
  const [executorName, setExecutorName] = useState<string | null>(null);
  const [executorRole, setExecutorRole] = useState<string | null>(null);
  const [generatedFile, setGeneratedFile] = useState<string | null>(null);
  const [commitHash, setCommitHash] = useState<string | null>(null);
  const [sprintTickets, setSprintTickets] = useState<any[]>([]);

  const startDebate = async () => {
    if (!selectedIssue) {
      alert('Selecione um ticket do Jira para debater primeiro!');
      return;
    }
    if (selectedAgentIds.length === 0) {
      alert('Selecione pelo menos um agente no organograma!');
      return;
    }

    setDebating(true);
    setLogs([]);
    setDecision(null);
    setJiraResult(null);
    setGitBranch(null);
    setGithubUrl(null);
    setExecutorName(null);
    setExecutorRole(null);
    setGeneratedFile(null);
    setCommitHash(null);
    setSprintTickets([]);

    try {
      const res = await fetch('http://localhost:5001/api/simulate-debate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issueKey: selectedIssue.key,
          issueSummary: selectedIssue.summary,
          issueDescription: selectedIssue.description,
          selectedAgentIds: selectedAgentIds
        })
      });

      if (!res.ok) throw new Error('Falha no motor de simulação.');
      const data = await res.json();
      
      setLogs(data.logs || []);
      setDecision(data.decision || '');
      setJiraResult(data.jiraCommentResult || '');
      setGitBranch(data.gitBranchName || null);
      setGithubUrl(data.githubIssueUrl || null);
      setExecutorName(data.executorName || null);
      setExecutorRole(data.executorRole || null);
      setGeneratedFile(data.generatedFile || null);
      setCommitHash(data.commitHash || null);
      setSprintTickets(data.sprintTickets || []);
      if (onDebateComplete) {
        onDebateComplete();
      }
    } catch (err: any) {
      alert(err.message);
    } finally {
      setDebating(false);
    }
  };

  const handleSendCommand = async () => {
    if (!customIdea.trim()) {
      alert('Por favor, digite um pedido/comando primeiro!');
      return;
    }

    setDebating(true);
    setLogs([]);
    setDecision(null);
    setJiraResult(null);
    setGitBranch(null);
    setGithubUrl(null);
    setExecutorName(null);
    setExecutorRole(null);
    setGeneratedFile(null);
    setCommitHash(null);
    setCommandResult(null);
    setSprintTickets([]);

    try {
      const res = await fetch('http://localhost:5001/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          commandText: customIdea
        })
      });

      if (!res.ok) throw new Error('Falha no motor de comando da empresa.');
      const data = await res.json();
      
      setCommandResult({
        actionType: data.actionType,
        reasoning: data.reasoning,
        details: data.details,
        jiraKey: data.jiraKey
      });

      if (data.actionType === 'DEBATE') {
        setLogs(data.logs || []);
        setDecision(data.decision || '');
        setJiraResult(data.jiraCommentResult || '');
        setGitBranch(data.gitBranchName || null);
        setGithubUrl(data.githubIssueUrl || null);
        setExecutorName(data.executorName || null);
        setExecutorRole(data.executorRole || null);
        setGeneratedFile(data.generatedFile || null);
        setCommitHash(data.commitHash || null);
        setSprintTickets(data.sprintTickets || []);
      }
      
      setCustomIdea(''); // Limpar
      if (onDebateComplete) {
        onDebateComplete();
      }
    } catch (err: any) {
      alert(err.message);
    } finally {
      setDebating(false);
    }
  };

  return (
    <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px', textAlign: 'left' }}>
      
      {/* Central de Comando da Empresa (Pedir Algo) */}
      <div style={{
        padding: '16px',
        background: 'var(--bg-secondary)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        <strong style={{ fontSize: '0.95rem', color: 'var(--color-primary)' }}>💡 Central de Comando da Empresa (Pedir Algo)</strong>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>
          Digite qualquer ordem ou ideia em linguagem natural. Os agentes de IA interpretarão o pedido e executarão as ações (contratar colaboradores, demissões, dar feedbacks, ajustar horários ou debater e comitar códigos).
        </p>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          <span style={{ fontWeight: 600 }}>Exemplos:</span>
          <code style={{ cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px' }} onClick={() => setCustomIdea("Contrate um dev Python backend")}>"Contrate um dev Python backend"</code>
          <code style={{ cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px' }} onClick={() => setCustomIdea("Dar feedback positivo para o David Dev")}>"Dar feedback positivo para o David Dev"</code>
          <code style={{ cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px' }} onClick={() => setCustomIdea("Demitir o Charlie Agile")}>"Demitir o Charlie Agile"</code>
          <code style={{ cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px' }} onClick={() => setCustomIdea("Precisamos de um novo design escuro para a tela de login")}>"Novo design de tela de login"</code>
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'stretch' }}>
          <textarea
            value={customIdea}
            onChange={e => setCustomIdea(e.target.value)}
            placeholder="Digite o comando para a sua empresa..."
            rows={2}
            style={{
              flex: 1,
              padding: '10px 14px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-tertiary)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              fontFamily: 'inherit',
              fontSize: '0.85rem',
              resize: 'none',
              outline: 'none'
            }}
          />
          <button
            onClick={handleSendCommand}
            disabled={debating || !customIdea.trim()}
            className="bg-gradient"
            style={{
              padding: '0 24px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              color: '#fff',
              fontWeight: 700,
              cursor: 'pointer',
              opacity: debating || !customIdea.trim() ? 0.6 : 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(139, 92, 246, 0.3)',
              fontSize: '0.85rem'
            }}
          >
            {debating ? 'Processando...' : 'Enviar Pedido'}
          </button>
        </div>
      </div>

      <div style={{ borderTop: '1px dashed var(--border-color)', margin: '10px 0' }}></div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>🤖 Sala de Decisão (Motor Gemma 4)</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Clique abaixo para rodar a simulação com os agentes selecionados no ticket ativo.
          </p>
        </div>
        <button
          onClick={startDebate}
          disabled={debating || !selectedIssue || selectedAgentIds.length === 0}
          className="bg-gradient"
          style={{
            padding: '10px 20px',
            borderRadius: 'var(--radius-sm)',
            border: 'none',
            color: '#fff',
            fontWeight: 700,
            cursor: 'pointer',
            opacity: (!selectedIssue || selectedAgentIds.length === 0) ? 0.5 : 1,
            boxShadow: '0 0 15px hsla(var(--hue-primary), 90%, 65%, 0.3)'
          }}
        >
          {debating ? 'Simulando debate...' : 'Iniciar Debate'}
        </button>
      </div>

      {selectedIssue ? (
        <div style={{
          padding: '12px 16px',
          background: 'var(--bg-secondary)',
          borderRadius: '8px',
          borderLeft: '4px solid var(--color-secondary)',
          fontSize: '0.9rem'
        }}>
          <strong>Ticket Ativo:</strong> {selectedIssue.key} - {selectedIssue.summary}
        </div>
      ) : (
        <div style={{
          padding: '12px 16px',
          background: 'rgba(245, 158, 11, 0.1)',
          borderRadius: '8px',
          borderLeft: '4px solid #f59e0b',
          fontSize: '0.9rem',
          color: '#f59e0b'
        }}>
          Nenhum ticket Jira selecionado. Selecione um no backlog acima.
        </div>
      )}

      {/* Debate Chat Feed */}
      {logs.length > 0 && (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          maxHeight: '350px',
          overflowY: 'auto',
          padding: '8px 4px'
        }}>
          {logs.map((log, index) => (
            <div key={index} style={{
              display: 'flex',
              gap: '12px',
              background: 'var(--bg-tertiary)',
              padding: '14px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-color)'
            }}>
              <span style={{ fontSize: '2rem' }}>{log.avatar}</span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <strong style={{ fontSize: '0.9rem', color: 'var(--color-primary)' }}>{log.name}</strong>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{log.role}</span>
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', fontStyle: 'italic', margin: 0 }}>
                  "{log.opinion}"
                </p>
                {log.replica && (
                  <p style={{ fontSize: '0.85rem', color: 'var(--color-secondary)', fontStyle: 'italic', borderTop: '1px dashed var(--border-color)', paddingTop: '6px', marginTop: '6px', margin: '6px 0 0 0' }}>
                    <strong>Réplica (Round 2):</strong> "{log.replica}"
                  </p>
                )}
                <div style={{
                  fontSize: '0.75rem',
                  color: '#f59e0b',
                  marginTop: '4px',
                  background: 'rgba(245, 158, 11, 0.08)',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  display: 'inline-block',
                  width: 'fit-content'
                }}>
                  Dilema considerado: {log.dilemma}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {commandResult && (
        <div style={{
          padding: '16px',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid var(--border-color)',
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          fontSize: '0.85rem'
        }}>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{ background: 'var(--color-primary)', color: '#fff', padding: '2px 8px', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 600 }}>
              {commandResult.actionType}
            </span>
            <strong style={{ color: 'var(--text-primary)' }}>Linha de Raciocínio dos Agentes:</strong>
          </div>
          <p style={{ margin: 0, color: 'var(--text-secondary)', fontStyle: 'italic' }}>{commandResult.reasoning}</p>
          <div style={{ color: '#34d399', fontWeight: 500, marginTop: '4px' }}>✓ {commandResult.details}</div>
          {commandResult.jiraKey && (
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              🔗 Ticket Jira Criado: <strong style={{ color: 'var(--color-secondary)' }}>{commandResult.jiraKey}</strong>
            </div>
          )}
        </div>
      )}

      {/* Sprint Timeline / Chamados Autônomos de Cada Agente */}
      {sprintTickets.length > 0 && (
        <div className="glass" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'left', marginTop: '16px', marginBottom: '16px' }}>
          <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            🔄 Ciclo de Vida da Sprint Autônoma (Chamados Jira)
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
            {sprintTickets.map((ticket, idx) => (
              <div
                key={idx}
                style={{
                  padding: '12px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px',
                  position: 'relative'
                }}
              >
                {/* Status indicator */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '1.2rem' }}>{ticket.agentAvatar}</span>
                  <span style={{
                    fontSize: '0.65rem',
                    background: '#10b981',
                    color: '#fff',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontWeight: 700
                  }}>
                    {ticket.status}
                  </span>
                </div>
                <div>
                  <strong style={{ fontSize: '0.75rem', color: '#fff', display: 'block' }}>{ticket.agentName}</strong>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{ticket.agentRole}</span>
                </div>
                <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '6px', fontSize: '0.7rem' }}>
                  <div style={{ color: 'var(--text-secondary)', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {ticket.ticketSummary}
                  </div>
                  <div style={{ color: '#fbbf24', marginTop: '2px', fontWeight: 700 }}>
                    🎫 {ticket.ticketKey}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Decision Output & Jira Sync Indicator */}
      {decision && (
        <div style={{
          padding: '20px',
          background: 'hsla(var(--hue-secondary), 90%, 55%, 0.08)',
          border: '1px solid var(--color-secondary)',
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          <h3 style={{ color: 'var(--color-secondary)', fontSize: '1.05rem', fontWeight: 700 }}>🏆 Consenso Gemma 4:</h3>
          <p style={{ fontSize: '0.9rem', lineHeight: '1.4' }}>{decision}</p>

          {jiraResult && (
            <div style={{
              marginTop: '8px',
              padding: '8px 12px',
              background: 'rgba(52, 211, 153, 0.1)',
              border: '1px solid #34d399',
              borderRadius: '6px',
              color: '#34d399',
              fontSize: '0.8rem',
              fontWeight: 500
            }}>
              🔗 Atlassian Jira: {jiraResult}
            </div>
          )}

          {gitBranch && (
            <div style={{
              marginTop: '8px',
              padding: '8px 12px',
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid #6366f1',
              borderRadius: '6px',
              color: '#a5b4fc',
              fontSize: '0.8rem',
              fontWeight: 500,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span>🌿 Branch Git Criada: <code>{gitBranch}</code></span>
              <span style={{ fontSize: '0.7rem', opacity: 0.8, background: '#6366f1', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>Criada</span>
            </div>
          )}

          {githubUrl && (
            <div style={{
              marginTop: '8px',
              padding: '8px 12px',
              background: 'rgba(31, 41, 55, 0.5)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              color: '#e5e7eb',
              fontSize: '0.8rem',
              fontWeight: 500
            }}>
              🐙 GitHub Issue: <a href={githubUrl} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-primary)', textDecoration: 'underline' }}>{githubUrl}</a>
            </div>
          )}

          {executorName && (
            <div style={{
              marginTop: '8px',
              padding: '12px',
              background: 'rgba(251, 191, 36, 0.05)',
              border: '1px dashed #fbbf24',
              borderRadius: '6px',
              color: '#fef3c7',
              fontSize: '0.8rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}>
              <div><strong>🔧 Executado Autonomamente por:</strong> {executorName} ({executorRole})</div>
              {generatedFile && <div><strong>📄 Arquivo Gerado:</strong> <code>{generatedFile}</code></div>}
              {commitHash && (
                <div>
                  <strong>💾 Git Commit:</strong> <code style={{ color: '#fbbf24' }}>{commitHash}</code>
                  <span style={{ marginLeft: '8px', fontSize: '0.7rem', color: '#34d399', background: 'rgba(52, 211, 153, 0.1)', padding: '1px 6px', borderRadius: '4px' }}>Comitado por Agente</span>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
