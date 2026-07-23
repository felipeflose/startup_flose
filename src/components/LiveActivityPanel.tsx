import React, { useState, useEffect, useRef } from 'react';

export interface ActivityEntry {
  id: string;
  agentId: string;
  agentName: string;
  agentAvatar: string;
  action: string;
  ticketKey?: string;
  ticketSummary?: string;
  at: string;
}

export const LiveActivityPanel: React.FC = () => {
  const [activities, setActivities] = useState<ActivityEntry[]>([]);
  const [connected, setConnected] = useState(false);
  const feedEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 1. Fetch initial activities
    fetch('http://localhost:5001/api/activity')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setActivities(data);
        }
      })
      .catch(err => console.error('Error fetching activities:', err));

    // 2. Connect to SSE Stream
    const eventSource = new EventSource('http://localhost:5001/api/activity/stream');

    eventSource.onopen = () => {
      setConnected(true);
    };

    eventSource.onmessage = (event) => {
      try {
        const newEntry: ActivityEntry = JSON.parse(event.data);
        setActivities(prev => {
          // Prevent duplicates
          if (prev.some(a => a.id === newEntry.id)) return prev;
          return [newEntry, ...prev].slice(0, 100);
        });
      } catch (err) {
        console.error('Error parsing SSE event:', err);
      }
    };

    eventSource.onerror = () => {
      setConnected(false);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="glass" style={{
      padding: '16px',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      textAlign: 'left',
      height: '100%',
      maxHeight: '780px',
      overflow: 'hidden',
      position: 'relative'
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '10px' }}>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 700, margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>⚡ Pulse da Empresa</span>
          <span style={{
            display: 'inline-block',
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: connected ? '#10b981' : '#ef4444',
            boxShadow: connected ? '0 0 8px #10b981' : '0 0 8px #ef4444',
            transition: 'all 0.3s ease'
          }}></span>
        </h3>
        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
          {connected ? 'Conectado ao vivo' : 'Desconectado'}
        </span>
      </div>

      {/* Feed Container */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        paddingRight: '4px',
        maxHeight: '700px'
      }}>
        {activities.length === 0 ? (
          <div style={{ padding: '24px 0', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic' }}>
            Nenhuma atividade registrada ainda.
          </div>
        ) : (
          activities.map((act) => (
            <div key={act.id} style={{
              display: 'flex',
              gap: '10px',
              padding: '10px',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px solid rgba(255, 255, 255, 0.04)',
              transition: 'all 0.2s ease',
              animation: 'fadeIn 0.3s ease-out'
            }}>
              {/* Avatar / Icon */}
              <div style={{
                fontSize: '1.4rem',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'rgba(255,255,255,0.05)',
                borderRadius: '50%'
              }}>
                {act.agentAvatar || '🤖'}
              </div>

              {/* Details */}
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '3px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong style={{ fontSize: '0.78rem', color: '#fff' }}>{act.agentName}</strong>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                    {new Date(act.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  </span>
                </div>
                <div style={{ fontSize: '0.78rem', color: '#e4e4e7', lineHeight: '1.25' }}>
                  {act.action}
                </div>
                {act.ticketKey && (
                  <div style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    marginTop: '2px',
                    fontSize: '0.7rem',
                    background: 'rgba(139, 92, 246, 0.1)',
                    border: '1px solid rgba(139, 92, 246, 0.2)',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    color: '#c084fc',
                    alignSelf: 'flex-start',
                    maxWidth: '100%'
                  }}>
                    <span style={{ fontWeight: 700 }}>{act.ticketKey}</span>
                    <span style={{
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      color: '#a78bfa'
                    }}>{act.ticketSummary}</span>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={feedEndRef} />
      </div>
    </div>
  );
};
