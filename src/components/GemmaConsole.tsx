import React, { useState } from 'react';

interface DebateLog {
  agentId: string;
  name: string;
  role: string;
  avatar: string;
  dilemma: string;
  opinion: string;
}

interface GemmaConsoleProps {
  selectedIssue: { key: string; summary: string; description: string } | null;
  selectedAgentIds: string[];
}

export const GemmaConsole: React.FC<GemmaConsoleProps> = ({ selectedIssue, selectedAgentIds }) => {
  const [debating, setDebating] = useState(false);
  const [logs, setLogs] = useState<DebateLog[]>([]);
  const [decision, setDecision] = useState<string | null>(null);
  const [jiraResult, setJiraResult] = useState<string | null>(null);

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
    } catch (err: any) {
      alert(err.message);
    } finally {
      setDebating(false);
    }
  };

  return (
    <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px', textAlign: 'left' }}>
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
                <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', fontStyle: 'italic' }}>
                  "{log.opinion}"
                </p>
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
              🔗 {jiraResult}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
