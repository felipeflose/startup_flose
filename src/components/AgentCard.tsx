import React from 'react';

export interface Agent {
  id: string;
  name: string;
  role: string;
  level: string;
  avatar: string;
  advantage: string;
  disadvantage: string;
  dilemma: string;
  personality: string;
  status?: string;
  schedule?: string;
  feedbacks?: any[];
  fired?: boolean;
  firedReason?: string;
  area?: string;
  desk?: string;
}

interface AgentCardProps {
  agent: Agent;
  isSelected: boolean;
  onSelectToggle: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, isSelected, onSelectToggle }) => {
  const getLevelColor = (level: string) => {
    switch (level) {
      case 'C-Level':
        return 'linear-gradient(135deg, #ffd700, #ffa500)';
      case 'Diretor':
        return 'linear-gradient(135deg, #c0c0c0, #808080)';
      case 'Gerente':
        return 'linear-gradient(135deg, #cd7f32, #8b4513)';
      case 'Coordenador':
        return 'linear-gradient(135deg, #60a5fa, #3b82f6)';
      case 'Analista SR':
        return 'linear-gradient(135deg, #34d399, #059669)';
      default:
        return 'linear-gradient(135deg, #a78bfa, #7c3aed)';
    }
  };

  return (
    <div 
      className={`glass ${isSelected ? 'glow-active' : ''}`}
      style={{
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        textAlign: 'left',
        cursor: agent.fired ? 'default' : 'pointer',
        borderWidth: isSelected ? '2px' : '1px',
        borderColor: isSelected ? 'var(--color-primary)' : 'var(--border-color)',
        position: 'relative',
        overflow: 'hidden',
        opacity: agent.fired ? 0.6 : 1,
        pointerEvents: agent.fired ? 'none' : 'auto'
      }}
      onClick={agent.fired ? undefined : onSelectToggle}
    >
      <div 
        style={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: '6px',
          height: '100%',
          background: agent.fired ? '#6b7280' : getLevelColor(agent.level)
        }}
      />
      
      {agent.fired && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '16px',
          fontSize: '0.65rem',
          fontWeight: 700,
          background: '#ef444426',
          border: '1px solid #ef44444d',
          color: '#f87171',
          padding: '1px 6px',
          borderRadius: '4px',
          textTransform: 'uppercase'
        }}>
          Desligado
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontSize: '2rem', filter: agent.fired ? 'grayscale(100%)' : 'none' }}>{agent.avatar}</span>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, color: agent.fired ? 'var(--text-muted)' : 'var(--text-primary)', textDecoration: agent.fired ? 'line-through' : 'none' }}>{agent.name}</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>{agent.role}</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '4px' }}>
        <span style={{
          fontSize: '0.75rem',
          padding: '2px 8px',
          borderRadius: '12px',
          background: 'hsla(var(--hue-primary), 15%, 25%, 0.5)',
          border: '1px solid var(--border-color)',
          color: 'var(--text-secondary)'
        }}>
          {agent.level}
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px', fontSize: '0.85rem' }}>
        <div>
          <strong style={{ color: 'var(--color-secondary)' }}>✓ Vantagem:</strong>
          <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>{agent.advantage}</p>
        </div>
        <div>
          <strong style={{ color: '#ef4444' }}>✗ Desvantagem:</strong>
          <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>{agent.disadvantage}</p>
        </div>
        <div>
          <strong style={{ color: '#f59e0b' }}>⚠️ Dilema Principal:</strong>
          <p style={{ color: 'var(--text-secondary)', marginTop: '2px', fontStyle: 'italic' }}>{agent.dilemma}</p>
        </div>
        <div>
          <strong style={{ color: 'var(--color-primary)' }}>🎭 Personalidade:</strong>
          <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>{agent.personality}</p>
        </div>
      </div>

      {agent.fired && agent.firedReason && (
        <div style={{ marginTop: '8px', padding: '6px 10px', background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.1)', borderRadius: '6px', fontSize: '0.72rem' }}>
          <strong style={{ color: '#f87171' }}>🚫 Histórico de Desligamento:</strong>
          <p style={{ color: 'var(--text-secondary)', marginTop: '2px', margin: 0, fontStyle: 'italic' }}>{agent.firedReason}</p>
        </div>
      )}

      {agent.feedbacks && agent.feedbacks.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', borderTop: '1px dashed var(--border-color)', paddingTop: '12px', marginTop: '8px' }}>
          <strong style={{ fontSize: '0.8rem', color: '#10b981' }}>📋 Histórico de Performance (RH):</strong>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', maxHeight: '100px', overflowY: 'auto', paddingRight: '4px' }}>
            {agent.feedbacks.map((f: any, i: number) => (
              <div key={i} style={{
                background: f.type === 'elogio' ? 'rgba(16, 185, 129, 0.05)' : 'rgba(239, 68, 68, 0.05)',
                border: f.type === 'elogio' ? '1px solid rgba(16, 185, 129, 0.1)' : '1px solid rgba(239, 68, 68, 0.1)',
                padding: '6px 8px',
                borderRadius: '6px',
                fontSize: '0.72rem'
              }}>
                <div style={{ fontWeight: 600, color: f.type === 'elogio' ? '#10b981' : '#ef4444', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span>{f.type === 'elogio' ? '⭐ Elogio' : '⚠️ Advertência'} ({f.impact})</span>
                  <span style={{ fontSize: '0.62rem', color: 'var(--text-muted)' }}>{f.sprintTicket || 'Custom'}</span>
                </div>
                <div style={{ color: 'var(--text-secondary)', marginTop: '2px', lineHeight: '1.25' }}>{f.text}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{
        marginTop: 'auto',
        paddingTop: '12px',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        fontSize: '0.8rem',
        borderTop: '1px solid var(--border-color)'
      }}>
        <span style={{ color: agent.fired ? 'var(--text-muted)' : isSelected ? 'var(--color-primary)' : 'var(--text-muted)' }}>
          {agent.fired ? 'Desligado (Inativo)' : isSelected ? '✓ Selecionado para Debate' : 'Selecionar'}
        </span>
      </div>
    </div>
  );
};
