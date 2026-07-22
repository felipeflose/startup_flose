import React, { useState, useEffect } from 'react';

export interface JiraIssue {
  key: string;
  fields: {
    summary: string;
    description?: {
      content?: Array<{
        content?: Array<{
          text: string;
        }>;
      }>;
    };
    issuetype: {
      name: string;
      iconUrl?: string;
    };
    status: {
      name: string;
    };
  };
  executorName?: string;
  creatorName?: string;
}

interface JiraDashboardProps {
  onSelectIssue: (issue: { key: string; summary: string; description: string }) => void;
  selectedIssueKey: string | null;
}

export const JiraDashboard: React.FC<JiraDashboardProps> = ({ onSelectIssue, selectedIssueKey }) => {
  const [issues, setIssues] = useState<JiraIssue[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // New Issue Form State
  const [newSummary, setNewSummary] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newProjectKey, setNewProjectKey] = useState('KAN');
  const [newIssueType, setNewIssueType] = useState('Task');
  const [creating, setCreating] = useState(false);

  const fetchIssues = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('http://localhost:5001/api/jira/issues');
      if (!res.ok) throw new Error('Falha ao conectar com o backend local.');
      const data = await res.json();
      setIssues(data.issues || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIssues();
  }, []);

  const handleCreateIssue = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSummary.trim()) return;
    setCreating(true);
    try {
      const res = await fetch('http://localhost:5001/api/jira/issue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          summary: newSummary,
          description: newDescription,
          projectKey: newProjectKey,
          issueType: newIssueType,
          creatorName: 'Felipe Flose (CEO)'
        })
      });
      if (!res.ok) throw new Error('Erro ao criar ticket.');
      setNewSummary('');
      setNewDescription('');
      fetchIssues();
    } catch (err: any) {
      alert(err.message);
    } finally {
      setCreating(false);
    }
  };

  const getIssueDescriptionText = (issue: JiraIssue) => {
    try {
      const content = issue.fields.description?.content;
      if (content && content[0]?.content && content[0]?.content[0]?.text) {
        return content[0].content[0].text;
      }
    } catch (e) {}
    return 'Sem descrição.';
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '24px' }}>
      {/* Issues List */}
      <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>📋 Backlog do Jira</h2>
          <button 
            onClick={fetchIssues} 
            className="bg-gradient" 
            style={{
              padding: '6px 12px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              color: '#fff',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            Sincronizar
          </button>
        </div>

        {loading && <p style={{ color: 'var(--text-secondary)' }}>Carregando tickets do Jira...</p>}
        {error && (
          <div style={{ padding: '12px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '8px', color: '#f87171', fontSize: '0.85rem' }}>
            Não foi possível carregar do Jira. Usando tickets offline. {error}
          </div>
        )}

        {!loading && issues.length === 0 && (
          <div style={{
            padding: '24px',
            textAlign: 'center',
            border: '2px dashed var(--border-color)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--text-secondary)'
          }}>
            Nenhum ticket encontrado no Jira. Crie um novo usando o formulário ao lado.
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '450px', overflowY: 'auto' }}>
          {issues.map(issue => {
            const isSelected = selectedIssueKey === issue.key;
            const desc = getIssueDescriptionText(issue);
            return (
              <div
                key={issue.key}
                onClick={() => onSelectIssue({ key: issue.key, summary: issue.fields.summary, description: desc })}
                style={{
                  padding: '16px',
                  borderRadius: 'var(--radius-md)',
                  background: isSelected ? 'hsla(var(--hue-primary), 90%, 65%, 0.1)' : 'var(--bg-secondary)',
                  border: `1px solid ${isSelected ? 'var(--color-primary)' : 'var(--border-color)'}`,
                  cursor: 'pointer',
                  textAlign: 'left',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px',
                  transition: 'all 0.2s'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-secondary)' }}>{issue.key}</span>
                  <span style={{
                    fontSize: '0.75rem',
                    padding: '2px 8px',
                    borderRadius: '8px',
                    background: 'hsla(var(--hue-secondary), 20%, 30%, 0.3)',
                    color: 'var(--text-primary)'
                  }}>{issue.fields.status.name}</span>
                </div>
                <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>{issue.fields.summary}</h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', marginBottom: '4px' }}>
                  {desc}
                </p>
                {issue.creatorName && (
                  <div style={{ fontSize: '0.72rem', color: '#a78bfa', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                    ✍️ Criado por: {issue.creatorName}
                  </div>
                )}
                {issue.executorName && (
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-secondary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px', margin: '2px 0' }}>
                    👤 Responsável: {issue.executorName}
                  </div>
                )}
                <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }} onClick={e => e.stopPropagation()}>
                  {issue.fields.status.name !== 'Em andamento' && issue.fields.status.name !== 'In Progress' && (
                    <button
                      onClick={async () => {
                        try {
                          const res = await fetch(`http://localhost:5001/api/jira/issue/${issue.key}/transition`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ statusName: 'In Progress' })
                          });
                          if (res.ok) fetchIssues();
                        } catch (e) { console.error(e); }
                      }}
                      style={{
                        padding: '4px 8px',
                        fontSize: '0.7rem',
                        borderRadius: '4px',
                        background: 'rgba(59, 130, 246, 0.2)',
                        border: '1px solid #3b82f6',
                        color: '#60a5fa',
                        cursor: 'pointer'
                      }}
                    >
                      ▶ Iniciar
                    </button>
                  )}
                  {issue.fields.status.name !== 'Concluído' && issue.fields.status.name !== 'Done' && (
                    <button
                      onClick={async () => {
                        try {
                          const res = await fetch(`http://localhost:5001/api/jira/issue/${issue.key}/transition`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ statusName: 'Done' })
                          });
                          if (res.ok) fetchIssues();
                        } catch (e) { console.error(e); }
                      }}
                      style={{
                        padding: '4px 8px',
                        fontSize: '0.7rem',
                        borderRadius: '4px',
                        background: 'rgba(52, 211, 153, 0.2)',
                        border: '1px solid #34d399',
                        color: '#34d399',
                        cursor: 'pointer'
                      }}
                    >
                      ✔ Concluir
                    </button>
                  )}
                  {(issue.fields.status.name === 'Concluído' || issue.fields.status.name === 'Done' || issue.fields.status.name === 'Em andamento' || issue.fields.status.name === 'In Progress') && (
                    <button
                      onClick={async () => {
                        try {
                          const res = await fetch(`http://localhost:5001/api/jira/issue/${issue.key}/transition`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ statusName: 'To Do' })
                          });
                          if (res.ok) fetchIssues();
                        } catch (e) { console.error(e); }
                      }}
                      style={{
                        padding: '4px 8px',
                        fontSize: '0.7rem',
                        borderRadius: '4px',
                        background: 'rgba(239, 68, 68, 0.2)',
                        border: '1px solid #ef4444',
                        color: '#f87171',
                        cursor: 'pointer'
                      }}
                    >
                      ↩ Reiniciar
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Create Ticket Form */}
      <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>➕ Novo Ticket Jira</h2>
        
        <form onSubmit={handleCreateIssue} style={{ display: 'flex', flexDirection: 'column', gap: '12px', textAlign: 'left' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Título do Issue</label>
            <input
              type="text"
              value={newSummary}
              onChange={e => setNewSummary(e.target.value)}
              placeholder="Ex: Refatorar fluxo de login"
              required
              style={{
                padding: '8px 12px',
                borderRadius: '8px',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Descrição / Dilema</label>
            <textarea
              value={newDescription}
              onChange={e => setNewDescription(e.target.value)}
              placeholder="Ex: A integração está caindo com múltiplos acessos concorrentes."
              rows={3}
              style={{
                padding: '8px 12px',
                borderRadius: '8px',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                outline: 'none',
                resize: 'none'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Chave Projeto</label>
              <input
                type="text"
                value={newProjectKey}
                onChange={e => setNewProjectKey(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'var(--bg-tertiary)',
                  border: '1px solid var(--border-color)',
                  color: '#fff',
                  outline: 'none'
                }}
              />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Tipo</label>
              <select
                value={newIssueType}
                onChange={e => setNewIssueType(e.target.value)}
                style={{
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'var(--bg-tertiary)',
                  border: '1px solid var(--border-color)',
                  color: '#fff',
                  outline: 'none'
                }}
              >
                <option value="Task">Task</option>
                <option value="Bug">Bug</option>
                <option value="Story">Story</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={creating}
            className="bg-gradient"
            style={{
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              color: '#fff',
              fontWeight: 600,
              cursor: 'pointer',
              marginTop: '8px',
              boxShadow: '0 4px 12px rgba(139, 92, 246, 0.3)'
            }}
          >
            {creating ? 'Criando...' : 'Criar no Jira'}
          </button>
        </form>
      </div>
    </div>
  );
};
