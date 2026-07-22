import React, { useState, useEffect } from 'react';

interface CardCreatorProps {
  onCreated?: () => void;
}

const EPICS = [
  { label: '🏗️ Infraestrutura & Tecnologia', value: 'Infraestrutura & Tecnologia' },
  { label: '🎨 Design & Produto', value: 'Design & Produto' },
  { label: '⚙️ Processos Ágeis', value: 'Processos Ágeis' },
  { label: '👥 Gestão de Pessoas', value: 'Gestão de Pessoas' },
  { label: '🎮 Entretenimento & Games', value: 'Entretenimento & Games' },
  { label: '🔧 Melhorias Internas', value: 'Melhorias Internas' },
  { label: '💰 Faturamento & Finanças', value: 'Faturamento & Finanças' },
];

const ISSUE_TYPES = [
  { label: '📋 Task', value: 'Task' },
  { label: '🐛 Bug', value: 'Bug' },
  { label: '📖 Story', value: 'Story' },
];

const CREATORS = [
  { label: '👑 Felipe Flose (CEO)', value: 'Felipe Flose (CEO)' },
  { label: '📋 Sarah Backlog (PM)', value: 'Sarah Backlog (PM)' },
  { label: '👑⚖️ Arthur de Flose (Governança)', value: 'Arthur de Flose (Governança)' },
  { label: '🧑‍💼 Hugo Organizador (RH)', value: 'Hugo Organizador (RH)' },
  { label: '🧑‍💻 David Dev', value: 'David Dev' },
  { label: '🎨 Elsa Pixel', value: 'Elsa Pixel' },
  { label: '🐍 Mariana Python', value: 'Mariana Python' },
  { label: '☁️ Lucas Cloud', value: 'Lucas Cloud' },
  { label: '🔍 Juliana QA Sênior', value: 'Juliana QA Sênior' },
];

const ASSIGNEES = [
  { label: '🧑‍💻 David Dev', value: 'David Dev' },
  { label: '🎨 Elsa Pixel', value: 'Elsa Pixel' },
  { label: '🐍 Mariana Python', value: 'Mariana Python' },
  { label: '☁️ Lucas Cloud', value: 'Lucas Cloud' },
  { label: '🔍 Juliana QA Sênior', value: 'Juliana QA Sênior' },
  { label: '🛡️ Carla SecOps', value: 'Carla SecOps' },
  { label: '🗄️ Davi DBA', value: 'Davi DBA' },
  { label: '📝 Sofia Tech Writer', value: 'Sofia Tech Writer' },
];

export const CardCreator: React.FC<CardCreatorProps> = ({ onCreated }) => {
  const [open, setOpen] = useState(false);
  const [summary, setSummary] = useState('');
  const [description, setDescription] = useState('');
  const [epic, setEpic] = useState('Infraestrutura & Tecnologia');
  const [issueType, setIssueType] = useState('Task');
  const [creator, setCreator] = useState('Felipe Flose (CEO)');
  const [assignee, setAssignee] = useState('David Dev');
  const [creating, setCreating] = useState(false);
  const [success, setSuccess] = useState(false);
  const [createdKey, setCreatedKey] = useState('');
  const [error, setError] = useState('');

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!summary.trim()) return;
    setCreating(true);
    setError('');
    try {
      const res = await fetch('http://localhost:5001/api/jira/issue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          summary,
          description,
          projectKey: 'KAN',
          issueType,
          epicName: epic,
          creatorName: creator,
          assigneeName: assignee,
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Erro ao criar card.');
      setCreatedKey(data.key || 'KAN-???');
      setSuccess(true);
      setSummary('');
      setDescription('');
      if (onCreated) onCreated();
      setTimeout(() => { setSuccess(false); setCreatedKey(''); setOpen(false); }, 2500);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  };

  const inputStyle: React.CSSProperties = {
    padding: '10px 14px',
    borderRadius: '10px',
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.12)',
    color: '#fff',
    outline: 'none',
    fontSize: '0.9rem',
    width: '100%',
    boxSizing: 'border-box',
    transition: 'border 0.2s',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '0.75rem',
    fontWeight: 700,
    color: 'var(--text-secondary)',
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
    marginBottom: '4px',
  };

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen(true)}
        title="Criar novo card no Jira"
        style={{
          position: 'fixed',
          bottom: '32px',
          right: '32px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #8b5cf6, #06b6d4)',
          border: 'none',
          color: '#fff',
          fontSize: '1.8rem',
          cursor: 'pointer',
          boxShadow: '0 8px 32px rgba(139,92,246,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          transition: 'transform 0.2s, box-shadow 0.2s',
        }}
        onMouseEnter={e => {
          (e.currentTarget as HTMLButtonElement).style.transform = 'scale(1.12)';
          (e.currentTarget as HTMLButtonElement).style.boxShadow = '0 12px 40px rgba(139,92,246,0.7)';
        }}
        onMouseLeave={e => {
          (e.currentTarget as HTMLButtonElement).style.transform = 'scale(1)';
          (e.currentTarget as HTMLButtonElement).style.boxShadow = '0 8px 32px rgba(139,92,246,0.5)';
        }}
      >
        ＋
      </button>

      {/* Backdrop */}
      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{
            position: 'fixed', inset: 0,
            background: 'rgba(0,0,0,0.6)',
            backdropFilter: 'blur(6px)',
            zIndex: 10000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
          }}
        >
          {/* Modal */}
          <div
            onClick={e => e.stopPropagation()}
            style={{
              width: '100%',
              maxWidth: '560px',
              background: 'linear-gradient(135deg, #1a1035, #0f172a)',
              border: '1px solid rgba(139,92,246,0.3)',
              borderRadius: '20px',
              padding: '32px',
              boxShadow: '0 24px 80px rgba(139,92,246,0.3)',
              display: 'flex',
              flexDirection: 'column',
              gap: '20px',
            }}
          >
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h2 style={{
                  fontSize: '1.4rem', fontWeight: 800, margin: 0,
                  background: 'linear-gradient(135deg, #a78bfa, #38bdf8)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
                }}>
                  ✍️ Criar Novo Card
                </h2>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', margin: '4px 0 0' }}>
                  Nasce em <strong style={{ color: '#34d399' }}>A fazer</strong> · Épico obrigatório
                </p>
              </div>
              <button
                onClick={() => setOpen(false)}
                style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '1.4rem', cursor: 'pointer', lineHeight: 1 }}
              >✕</button>
            </div>

            {success ? (
              <div style={{
                textAlign: 'center', padding: '32px',
                background: 'rgba(52,211,153,0.1)',
                border: '1px solid rgba(52,211,153,0.4)',
                borderRadius: '14px'
              }}>
                <div style={{ fontSize: '3rem' }}>🎉</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#34d399', marginTop: '8px' }}>
                  Card criado!
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  <strong style={{ color: '#34d399' }}>{createdKey}</strong> — nasceu em A fazer ✅
                </div>
              </div>
            ) : (
              <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

                {/* Title */}
                <div>
                  <div style={labelStyle}>Título do Card *</div>
                  <input
                    autoFocus
                    type="text"
                    value={summary}
                    onChange={e => setSummary(e.target.value)}
                    placeholder="Ex: Implementar autenticação com JWT"
                    required
                    style={inputStyle}
                  />
                </div>

                {/* Description */}
                <div>
                  <div style={labelStyle}>Descrição / Critério de Aceitação</div>
                  <textarea
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    placeholder="O que precisa ser feito? O que significa 'pronto'?"
                    rows={3}
                    style={{ ...inputStyle, resize: 'none' }}
                  />
                </div>

                {/* Row: Epic + Type */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div>
                    <div style={labelStyle}>Épico *</div>
                    <select value={epic} onChange={e => setEpic(e.target.value)} style={inputStyle}>
                      {EPICS.map(ep => (
                        <option key={ep.value} value={ep.value}>{ep.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <div style={labelStyle}>Tipo</div>
                    <select value={issueType} onChange={e => setIssueType(e.target.value)} style={inputStyle}>
                      {ISSUE_TYPES.map(t => (
                        <option key={t.value} value={t.value}>{t.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Row: Creator + Assignee */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div>
                    <div style={labelStyle}>✍️ Criado por *</div>
                    <select value={creator} onChange={e => setCreator(e.target.value)} style={inputStyle}>
                      {CREATORS.map(c => (
                        <option key={c.value} value={c.value}>{c.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <div style={labelStyle}>👤 Responsável *</div>
                    <select value={assignee} onChange={e => setAssignee(e.target.value)} style={inputStyle}>
                      {ASSIGNEES.map(a => (
                        <option key={a.value} value={a.value}>{a.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Governance info */}
                <div style={{
                  padding: '10px 14px',
                  borderRadius: '8px',
                  background: 'rgba(52,211,153,0.08)',
                  border: '1px solid rgba(52,211,153,0.2)',
                  fontSize: '0.75rem',
                  color: 'var(--text-secondary)',
                  display: 'flex', alignItems: 'center', gap: '8px'
                }}>
                  <span style={{ fontSize: '1rem' }}>🛡️</span>
                  <span>Card nasce em <strong style={{ color: '#34d399' }}>A fazer</strong> com Épico, Criador e Responsável obrigatórios — auditado por Arthur de Flose.</span>
                </div>

                {error && (
                  <div style={{
                    padding: '10px 14px', borderRadius: '8px',
                    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
                    color: '#f87171', fontSize: '0.8rem'
                  }}>
                    ❌ {error}
                  </div>
                )}

                {/* Submit */}
                <button
                  type="submit"
                  disabled={creating || !summary.trim()}
                  style={{
                    padding: '14px',
                    borderRadius: '12px',
                    border: 'none',
                    background: creating || !summary.trim()
                      ? 'rgba(255,255,255,0.1)'
                      : 'linear-gradient(135deg, #8b5cf6, #06b6d4)',
                    color: '#fff',
                    fontWeight: 700,
                    fontSize: '1rem',
                    cursor: creating || !summary.trim() ? 'not-allowed' : 'pointer',
                    boxShadow: creating || !summary.trim() ? 'none' : '0 4px 20px rgba(139,92,246,0.4)',
                    transition: 'all 0.2s'
                  }}
                >
                  {creating ? '⟳ Criando card...' : '✅ Criar Card no Jira'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
};
