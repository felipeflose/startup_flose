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
        cursor: 'pointer',
        borderWidth: isSelected ? '2px' : '1px',
        borderColor: isSelected ? 'var(--color-primary)' : 'var(--border-color)',
        position: 'relative',
        overflow: 'hidden'
      }}
      onClick={onSelectToggle}
    >
      <div 
        style={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: '6px',
          height: '100%',
          background: getLevelColor(agent.level)
        }}
      />
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontSize: '2rem' }}>{agent.avatar}</span>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, color: 'var(--text-primary)' }}>{agent.name}</h3>
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

      <div style={{
        marginTop: 'auto',
        paddingTop: '12px',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        fontSize: '0.8rem',
        borderTop: '1px solid var(--border-color)'
      }}>
        <span style={{ color: isSelected ? 'var(--color-primary)' : 'var(--text-muted)' }}>
          {isSelected ? '✓ Selecionado para Debate' : 'Selecionar'}
        </span>
      </div>
    </div>
  );
};
