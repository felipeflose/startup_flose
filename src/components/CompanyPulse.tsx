import React, { useEffect, useState } from 'react';
import type { Agent } from './AgentCard';

interface ActivityItem {
  id: string;
  agentId: string;
  agentName: string;
  agentAvatar: string;
  action: 'opened' | 'progressing' | 'closed';
  ticketKey: string;
  ticketSummary: string;
  at: string;
}

interface CompanyPulseProps {
  agents: Agent[];
}

export const CompanyPulse: React.FC<CompanyPulseProps> = ({ agents }) => {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchActivity = () => {
    fetch('http://localhost:5001/api/activity')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setActivities(data);
        }
        setLoading(false)
      })
      .catch(err => console.error('Error fetching activities:', err));
  };

  useEffect(() => {
    fetchActivity();

    // Connect to live SSE Stream
    const eventSource = new EventSource('http://localhost:5001/api/activity/stream');

    eventSource.onmessage = (event) => {
      try {
        const newEntry = JSON.parse(event.data);
        setActivities(prev => {
          if (prev.some(a => a.id === newEntry.id)) return prev;
          return [newEntry, ...prev].slice(0, 100);
        });
      } catch (err) {
        console.error('Error parsing SSE event:', err);
      }
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const getActionLabel = (action: string) => {
    const act = (action || '').toLowerCase();
    if (act.includes('criou') || act.includes('abriu')) {
      return { text: action, color: '#fbbf24', icon: '🎫' };
    }
    if (act.includes('progresso') || act.includes('codificou') || act.includes('andamento') || act.includes('desenvolv') || act.includes('resolveu')) {
      return { text: action, color: '#60a5fa', icon: '💻' };
    }
    if (act.includes('concluiu') || act.includes('fechou') || act.includes('aprov') || act.includes('homolog')) {
      return { text: action, color: '#10b981', icon: '✅' };
    }
    if (act.includes('demitiu') || act.includes('demiss')) {
      return { text: action, color: '#ef4444', icon: '❌' };
    }
    if (act.includes('admitiu') || act.includes('contrat')) {
      return { text: action, color: '#34d399', icon: '👥' };
    }
    return { text: action, color: '#e4e4e7', icon: '⚙️' };
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px', textAlign: 'left', marginTop: '24px' }}>
      {/* Lado esquerdo: Painel de Presença dos Agentes */}
      <div className="glass" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#fff' }}>👥 Status do Time (Em Tempo Real)</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '420px', overflowY: 'auto' }}>
          {agents.map(agent => {
            const isWorking = agent.status && agent.status !== 'Disponível';
            return (
              <div 
                key={agent.id} 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px', 
                  padding: '10px 14px', 
                  background: isWorking ? 'rgba(96, 165, 250, 0.05)' : 'rgba(255, 255, 255, 0.01)',
                  borderRadius: '8px',
                  border: isWorking ? '1px solid rgba(96, 165, 250, 0.3)' : '1px solid var(--border-color)',
                  transition: 'all 0.3s ease'
                }}
              >
                <span style={{ fontSize: '1.5rem' }}>{agent.avatar}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.85rem', color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{agent.name}</strong>
                    <span style={{ 
                      width: '8px', 
                      height: '8px', 
                      borderRadius: '50%', 
                      background: isWorking ? '#3b82f6' : '#10b981', 
                      boxShadow: isWorking ? '0 0 8px #3b82f6' : '0 0 8px #10b981'
                    }} />
                  </div>
                  <p style={{ margin: 0, fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{agent.role}</p>
                  <p style={{ margin: '4px 0 0 0', fontSize: '0.65rem', color: isWorking ? '#60a5fa' : '#34d399', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {isWorking ? `⚙️ ${agent.status}` : '✓ Disponível'}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Lado direito: Feed de Atividades Recentes */}
      <div className="glass" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#fff' }}>⚡ Atividade Recente da Empresa</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '420px', overflowY: 'auto' }}>
          {loading ? (
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic' }}>Carregando feed de atividades...</span>
          ) : activities.length === 0 ? (
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic' }}>Nenhuma atividade registrada hoje. Envie um comando para iniciar.</span>
          ) : (
            activities.map(act => {
              const actDetail = getActionLabel(act.action);
              return (
                <div 
                  key={act.id} 
                  style={{ 
                    display: 'flex', 
                    gap: '12px', 
                    padding: '12px', 
                    borderBottom: '1px solid var(--border-color)',
                    alignItems: 'flex-start',
                    fontSize: '0.8rem'
                  }}
                >
                  <span style={{ fontSize: '1.25rem', marginTop: '2px' }}>{act.agentAvatar}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ color: '#fff' }}>
                      <strong>{act.agentName}</strong> {actDetail.icon} <span style={{ color: actDetail.color, fontWeight: 500 }}>{actDetail.text}</span>
                    </div>
                    <div style={{ color: 'var(--text-secondary)', marginTop: '4px', fontSize: '0.75rem', fontFamily: 'monospace' }}>
                      {act.ticketKey !== '...' && <span style={{ color: '#fbbf24', marginRight: '6px' }}>[{act.ticketKey}]</span>}
                      {act.ticketSummary}
                    </div>
                  </div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                    {new Date(act.at).toLocaleTimeString('pt-BR')}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
