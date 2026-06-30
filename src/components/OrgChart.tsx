import React from 'react';
import { Agent } from './AgentCard';

interface OrgChartProps {
  agents: Agent[];
  selectedAgentIds: string[];
  onSelectAgent: (id: string) => void;
}

export const OrgChart: React.FC<OrgChartProps> = ({ agents, selectedAgentIds, onSelectAgent }) => {
  // Group agents by their levels
  const levels = ['C-Level', 'Diretor', 'Gerente', 'Coordenador', 'Analista SR'];
  
  const groupedAgents = levels.reduce((acc, lvl) => {
    acc[lvl] = agents.filter(a => a.level === lvl);
    return acc;
  }, {} as Record<string, Agent[]>);

  const getLevelBadgeColor = (level: string) => {
    switch (level) {
      case 'C-Level': return '#f59e0b';
      case 'Diretor': return '#9ca3af';
      case 'Gerente': return '#b45309';
      case 'Coordenador': return '#3b82f6';
      case 'Analista SR': return '#10b981';
      default: return '#8b5cf6';
    }
  };

  return (
    <div className="glass" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px', overflowX: 'auto' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>🏛️ Organograma & Níveis Hierárquicos</h2>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '-12px' }}>
        Clique nos agentes para selecioná-los para debater os tickets e dilemas da startup.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', minWidth: '800px', position: 'relative' }}>
        {levels.map((level, levelIdx) => (
          <div key={level} style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'center' }}>
            {/* Level Label */}
            <div style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '1px',
              color: getLevelBadgeColor(level),
              background: `${getLevelBadgeColor(level)}1A`,
              border: `1px solid ${getLevelBadgeColor(level)}33`,
              padding: '2px 10px',
              borderRadius: '20px'
            }}>
              {level}
            </div>

            {/* Level Grid */}
            <div style={{
              display: 'flex',
              gap: '16px',
              justifyContent: 'center',
              width: '100%',
              flexWrap: 'wrap'
            }}>
              {groupedAgents[level]?.map(agent => {
                const isSelected = selectedAgentIds.includes(agent.id);
                return (
                  <div
                    key={agent.id}
                    onClick={() => onSelectAgent(agent.id)}
                    style={{
                      padding: '10px 16px',
                      borderRadius: '12px',
                      background: isSelected ? 'hsla(var(--hue-primary), 90%, 65%, 0.15)' : 'var(--bg-tertiary)',
                      border: `1px solid ${isSelected ? 'var(--color-primary)' : 'var(--border-color)'}`,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      transition: 'all 0.2s ease',
                      boxShadow: isSelected ? '0 0 12px hsla(var(--hue-primary), 90%, 65%, 0.25)' : 'none',
                      minWidth: '200px'
                    }}
                  >
                    <span style={{ fontSize: '1.5rem' }}>{agent.avatar}</span>
                    <div style={{ textAlign: 'left' }}>
                      <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>{agent.name}</div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{agent.role}</div>
                    </div>
                  </div>
                );
              })}
            </div>
            
            {levelIdx < levels.length - 1 && (
              <div style={{
                width: '2px',
                height: '16px',
                background: 'linear-gradient(to bottom, var(--border-color), transparent)',
                marginTop: '4px'
              }}/>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
