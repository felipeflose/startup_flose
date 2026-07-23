import React, { useState, useEffect, useRef } from 'react';

interface Agent {
  id: string;
  name: string;
  role: string;
  avatar: string;
  level: string;
  status?: string;
  area?: string;
  desk?: string;
  fired?: boolean;
}

interface OfficeMapProps {
  agents: Agent[];
  selectedAgentIds: string[];
  jiraIssues: any[];
}

interface AgentSimState {
  id: string;
  x: number;
  y: number;
  targetX: number;
  targetY: number;
  state: 'desk' | 'coffee' | 'meeting' | 'toilet';
  bubbleText?: string;
  bubbleTime?: number; // timestamp until bubble hides
  lastLiveEventTime?: number;
}

export const OfficeMap: React.FC<OfficeMapProps> = ({ agents, selectedAgentIds, jiraIssues = [] }) => {
  const [agentStates, setAgentStates] = useState<Record<string, AgentSimState>>({});
  const [hoveredAgent, setHoveredAgent] = useState<Agent | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Define coordinate zones on our 800x500 map
  const ZONES = {
    csuite: { x: 40, y: 40, w: 260, h: 180, name: '💼 Diretoria & C-Suite', color: '#ffd700' },
    engineering: { x: 480, y: 40, w: 280, h: 200, name: '💻 Engenharia & TI', color: '#3b82f6' },
    product: { x: 40, y: 280, w: 320, h: 180, name: '🎨 Produto & Design', color: '#f59e0b' },
    operations: { x: 420, y: 300, w: 180, h: 160, name: '⚖️ Qualidade & RH', color: '#34d399' },
    chamber: { x: 310, y: 160, w: 160, h: 120, name: '🔮 Chamber de Decisão', color: '#8b5cf6' },
    coffee: { x: 620, y: 320, w: 140, h: 140, name: '☕ Coffee Lounge', color: '#ec4899' },
    restroom: { x: 720, y: 260, w: 60, h: 50, name: '🚾 WC', color: '#6b7280' }
  };

  // Generate unique desk coordinates for each agent on load
  const deskPositionsRef = useRef<Record<string, { x: number; y: number }>>({});

  useEffect(() => {
    const active = agents.filter(a => !a.fired);
    const newDesks: Record<string, { x: number; y: number }> = {};

    // Group counters to distribute desks cleanly in zones
    let csuiteCount = 0;
    let engCount = 0;
    let prodCount = 0;
    let opsCount = 0;

    active.forEach(agent => {
      const area = agent.area || '';
      let deskX = 100;
      let deskY = 100;

      if (area.includes('Diretoria') || area.includes('C-Suite')) {
        const row = Math.floor(csuiteCount / 3);
        const col = csuiteCount % 3;
        deskX = ZONES.csuite.x + 30 + col * 75;
        deskY = ZONES.csuite.y + 40 + row * 60;
        csuiteCount++;
      } else if (area.includes('Engenharia') || area.includes('TI')) {
        const row = Math.floor(engCount / 4);
        const col = engCount % 4;
        deskX = ZONES.engineering.x + 25 + col * 65;
        deskY = ZONES.engineering.y + 45 + row * 55;
        engCount++;
      } else if (area.includes('Produto') || area.includes('Design')) {
        const row = Math.floor(prodCount / 3);
        const col = prodCount % 3;
        deskX = ZONES.product.x + 35 + col * 85;
        deskY = ZONES.product.y + 45 + row * 60;
        prodCount++;
      } else {
        // QA, HR & Operations
        const row = Math.floor(opsCount / 2);
        const col = opsCount % 2;
        deskX = ZONES.operations.x + 30 + col * 75;
        deskY = ZONES.operations.y + 45 + row * 55;
        opsCount++;
      }

      newDesks[agent.id] = { x: deskX, y: deskY };
    });

    deskPositionsRef.current = newDesks;
  }, [agents]);

  // Main simulation tick loop (smooth animation towards target coordinates)
  useEffect(() => {
    // Initialize states
    setAgentStates(prev => {
      const next: Record<string, AgentSimState> = { ...prev };
      agents.forEach(agent => {
        if (agent.fired) {
          delete next[agent.id];
          return;
        }
        if (!next[agent.id]) {
          const desk = deskPositionsRef.current[agent.id] || { x: 400, y: 250 };
          next[agent.id] = {
            id: agent.id,
            x: desk.x,
            y: desk.y,
            targetX: desk.x,
            targetY: desk.y,
            state: 'desk'
          };
        }
      });
      return next;
    });

    const interval = setInterval(() => {
      setAgentStates(prev => {
        const next = { ...prev };
        const now = Date.now();

        Object.keys(next).forEach(id => {
          const state = next[id];
          const agent = agents.find(a => a.id === id);
          if (!agent) return;

          // 1. Check if there was a recent live activity event (within 15 seconds)
          const hasRecentEvent = state.lastLiveEventTime && (now - state.lastLiveEventTime < 15000);

          let targetX = state.targetX;
          let targetY = state.targetY;
          let targetState = state.state;

          if (hasRecentEvent) {
            // Keep targets set by the live SSE stream event
            targetX = state.targetX;
            targetY = state.targetY;
            targetState = state.state;
          } else {
            // 2. Fallback: Find active card assigned to this agent or created by this agent
            const activeCard = jiraIssues.find(issue => {
              const status = (issue.fields?.status?.name || '').toLowerCase();
              const isClosed = status === 'done' || status === 'concluido' || status === 'resolvido' || status === 'fechado';
              if (isClosed) return false;
              
              const execName = issue.executorName || '';
              const creatName = issue.creatorName || '';
              return execName.includes(agent.name) || agent.name.includes(execName) || 
                     creatName.includes(agent.name) || agent.name.includes(creatName);
            });

            const isWorkingOnCard = !!activeCard;
            const isParticipating = selectedAgentIds.includes(id);

            if (isParticipating) {
              targetState = 'meeting';
              const idx = selectedAgentIds.indexOf(id);
              const radius = 40;
              const angle = (idx / selectedAgentIds.length) * 2 * Math.PI;
              targetX = ZONES.chamber.x + ZONES.chamber.w / 2 + Math.cos(angle) * radius;
              targetY = ZONES.chamber.y + ZONES.chamber.h / 2 + Math.sin(angle) * radius;
            } else if (isWorkingOnCard) {
              targetState = 'desk';
              const desk = deskPositionsRef.current[id] || { x: 400, y: 250 };
              targetX = desk.x;
              targetY = desk.y;
            } else {
              // Available / idle agents can wander around
              const rand = Math.random();
              if (state.state === 'desk' && rand < 0.01) {
                targetState = 'coffee';
                targetX = ZONES.coffee.x + 30 + Math.random() * (ZONES.coffee.w - 60);
                targetY = ZONES.coffee.y + 30 + Math.random() * (ZONES.coffee.h - 60);
              } else if (state.state === 'desk' && rand < 0.015) {
                targetState = 'toilet';
                targetX = ZONES.restroom.x + 15 + Math.random() * (ZONES.restroom.w - 30);
                targetY = ZONES.restroom.y + 15 + Math.random() * (ZONES.restroom.h - 30);
              } else if (state.state !== 'desk' && rand < 0.05) {
                targetState = 'desk';
                const desk = deskPositionsRef.current[id] || { x: 400, y: 250 };
                targetX = desk.x;
                targetY = desk.y;
              }
            }
          }

          // 3. Linear Interpolation towards targets (smooth walks)
          const dx = targetX - state.x;
          const dy = targetY - state.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const speed = 4; // speed in pixels per tick

          let newX = state.x;
          let newY = state.y;

          if (dist > speed) {
            newX += (dx / dist) * speed;
            newY += (dy / dist) * speed;
          } else {
            newX = targetX;
            newY = targetY;
          }

          // 4. Thoughts / Speech Bubbles
          let bubbleText = state.bubbleText;
          let bubbleTime = state.bubbleTime;

          if (!hasRecentEvent) {
            // Standard card or idle thoughts if no live SSE activity
            if ((!bubbleText || now > (bubbleTime || 0)) && Math.random() < 0.015) {
              const activeCard = jiraIssues.find(issue => {
                const status = (issue.fields?.status?.name || '').toLowerCase();
                const isClosed = status === 'done' || status === 'concluido' || status === 'resolvido' || status === 'fechado';
                if (isClosed) return false;
                const execName = issue.executorName || '';
                const creatName = issue.creatorName || '';
                return execName.includes(agent.name) || agent.name.includes(execName) || 
                       creatName.includes(agent.name) || agent.name.includes(creatName);
              });

              if (selectedAgentIds.includes(id)) {
                bubbleText = `Debatendo no Chamber...`;
              } else if (activeCard) {
                const summary = activeCard.fields?.summary || 'card';
                const cleanSummary = summary.replace('[Gemma4] ', '');
                const statusName = activeCard.fields?.status?.name || 'A Fazer';
                const execName = activeCard.executorName || '';
                const isExecutor = execName.includes(agent.name) || agent.name.includes(execName);

                if (isExecutor) {
                  if (statusName.toLowerCase().includes('progress') || statusName.toLowerCase().includes('andamento') || statusName.toLowerCase().includes('desenvolv')) {
                    bubbleText = `Desenvolvendo ${activeCard.key}: "${cleanSummary.substring(0, 30)}..."`;
                  } else if (statusName.toLowerCase().includes('homolog') || statusName.toLowerCase().includes('qa') || statusName.toLowerCase().includes('test')) {
                    bubbleText = `Validando QA em ${activeCard.key}: "${cleanSummary.substring(0, 30)}..."`;
                  } else {
                    bubbleText = `Analisando card ${activeCard.key}: "${cleanSummary.substring(0, 30)}..."`;
                  }
                } else {
                  bubbleText = `Monitoreando ${activeCard.key} (eu criei como PO)`;
                }
              } else {
                const thoughts = {
                  desk: [
                    'Sem demandas ativas no momento. Aguardando novo card...',
                    'Frenesi de commits no GitHub? Sempre com card!',
                    'Nenhum card aberto para mim. Hora de ler documentações.',
                    'Gemma 4 está gerando ótimos planos de produto.',
                    'Hugo/Arthur me disseram que quem não cria card roda!'
                  ],
                  coffee: [
                    'Facilities caprichou nesse café expresso!',
                    'Precisava dessa pausa para recarregar.',
                    'Café quente e sem bugs na cabeça.',
                    'Quem quer conversar sobre a sprint na copa?'
                  ],
                  meeting: [
                    'Concordo com o ponto levantado.',
                    'Temos que manter a governança alta.',
                    'Precisamos de critério de aceitação claro.'
                  ],
                  toilet: [
                    'Lavando as mãos rapidamente...',
                    'Clean desk policy vale para a pia também?'
                  ]
                };
                const pool = thoughts[targetState] || thoughts.desk;
                bubbleText = pool[Math.floor(Math.random() * pool.length)];
              }
              bubbleTime = now + 5000;
            }
          }

          next[id] = {
            id,
            x: newX,
            y: newY,
            targetX,
            targetY,
            state: targetState as any,
            bubbleText: (bubbleText && now < (bubbleTime || 0)) ? bubbleText : undefined,
            bubbleTime,
            lastLiveEventTime: state.lastLiveEventTime
          };
        });

        return next;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [agents, selectedAgentIds, jiraIssues]);

  // Connect to live activity stream directly to synchronize map coordinates and thoughts at SSE speed!
  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/api/activity/stream');

    eventSource.onmessage = (event) => {
      try {
        const newEntry = JSON.parse(event.data);
        const agentId = newEntry.agentId;
        if (!agentId) return;

        // Failsafe: Ignore event if the agent is fired or not in current list
        const agent = agents.find(a => a.id === agentId);
        if (!agent || agent.fired) {
          setAgentStates(prev => {
            if (prev[agentId]) {
              const next = { ...prev };
              delete next[agentId];
              return next;
            }
            return prev;
          });
          return;
        }

        setAgentStates(prev => {
          const next = { ...prev };
          const current = next[agentId];
          
          // Failsafe in case state hasn't initialized this agent yet
          const initialX = current ? current.x : 400;
          const initialY = current ? current.y : 250;

          const actionText = (newEntry.action || '').toLowerCase();
          let targetState = 'desk';

          if (actionText.includes('debat') || actionText.includes('reun') || actionText.includes('chamber') || actionText.includes('discuss')) {
            targetState = 'meeting';
          } else if (actionText.includes('cafe') || actionText.includes('copa') || actionText.includes('break')) {
            targetState = 'coffee';
          } else if (actionText.includes('banheiro') || actionText.includes('wc') || actionText.includes('lavar')) {
            targetState = 'toilet';
          }

          // Determine coordinates based on targetState
          let targetX = initialX;
          let targetY = initialY;

          if (targetState === 'meeting') {
            const idx = selectedAgentIds.indexOf(agentId);
            const activeIndex = idx >= 0 ? idx : Math.floor(Math.random() * 4);
            const radius = 35;
            const angle = (activeIndex / 4) * 2 * Math.PI;
            targetX = ZONES.chamber.x + ZONES.chamber.w / 2 + Math.cos(angle) * radius;
            targetY = ZONES.chamber.y + ZONES.chamber.h / 2 + Math.sin(angle) * radius;
          } else if (targetState === 'coffee') {
            targetX = ZONES.coffee.x + 30 + Math.random() * (ZONES.coffee.w - 60);
            targetY = ZONES.coffee.y + 30 + Math.random() * (ZONES.coffee.h - 60);
          } else if (targetState === 'toilet') {
            targetX = ZONES.restroom.x + 15 + Math.random() * (ZONES.restroom.w - 30);
            targetY = ZONES.restroom.y + 15 + Math.random() * (ZONES.restroom.h - 30);
          } else {
            const desk = deskPositionsRef.current[agentId] || { x: 400, y: 250 };
            targetX = desk.x;
            targetY = desk.y;
          }

          // Shorten action string if it's too long for speech bubble
          let cleanAction = newEntry.action || '';
          if (cleanAction.length > 70) {
            cleanAction = cleanAction.substring(0, 67) + '...';
          }

          next[agentId] = {
            id: agentId,
            x: initialX,
            y: initialY,
            targetX,
            targetY,
            state: targetState as any,
            bubbleText: cleanAction,
            bubbleTime: Date.now() + 10000, // Show live event bubble for 10 seconds
            lastLiveEventTime: Date.now()
          };
          return next;
        });
      } catch (err) {
        console.error('Error handling SSE message in OfficeMap:', err);
      }
    };

    return () => {
      eventSource.close();
    };
  }, [selectedAgentIds, agents]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', width: '100%' }}>
      {/* Simulation Info */}
      <div className="glass" style={{ padding: '12px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', textAlign: 'left' }}>
        <div>
          <span style={{ fontSize: '0.75rem', background: '#34d399', padding: '2px 8px', borderRadius: '4px', color: '#000', fontWeight: 700, marginRight: '8px' }}>LIVE SIMULATION</span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Os colaboradores se movimentam de acordo com suas atribuições reais no Jira e debates no Chamber.
          </span>
        </div>
        <div style={{ fontSize: '0.75rem', display: 'flex', gap: '16px', color: 'var(--text-muted)' }}>
          <span>💻 Mesa = Trabalhando</span>
          <span>☕ Café = Break</span>
          <span>🔮 Chamber = Em Debate</span>
        </div>
      </div>

      {/* Office Floor Plan Layout Container */}
      <div 
        ref={containerRef}
        style={{
          width: '100%',
          height: '500px',
          background: '#040711',
          borderRadius: '16px',
          border: '1px solid var(--border-color)',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: 'inset 0 0 40px rgba(0, 0, 0, 0.9)'
        }}
      >
        {/* Draw Zones Background panels */}
        {Object.entries(ZONES).map(([key, zone]) => (
          <div
            key={key}
            style={{
              position: 'absolute',
              left: `${zone.x}px`,
              top: `${zone.y}px`,
              width: `${zone.w}px`,
              height: `${zone.h}px`,
              border: `1px dashed ${zone.color}40`,
              background: `${zone.color}05`,
              borderRadius: '12px',
              pointerEvents: 'none',
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'flex-start',
              padding: '8px 12px'
            }}
          >
            <span style={{ fontSize: '0.75rem', color: zone.color, fontWeight: 700, opacity: 0.8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {zone.name}
            </span>
          </div>
        ))}

        {/* Meeting Table in Center of Chamber */}
        <div style={{
          position: 'absolute',
          left: `${ZONES.chamber.x + ZONES.chamber.w / 2 - 25}px`,
          top: `${ZONES.chamber.y + ZONES.chamber.h / 2 - 25}px`,
          width: '50px',
          height: '50px',
          background: 'rgba(139, 92, 246, 0.15)',
          border: '2px solid rgba(139, 92, 246, 0.4)',
          borderRadius: '50%',
          boxShadow: '0 0 15px rgba(139, 92, 246, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          pointerEvents: 'none'
        }}>
          <span style={{ fontSize: '0.9rem', opacity: 0.7 }}>🔮</span>
        </div>

        {/* Coffee Table in Coffee Lounge */}
        <div style={{
          position: 'absolute',
          left: `${ZONES.coffee.x + ZONES.coffee.w / 2 - 20}px`,
          top: `${ZONES.coffee.y + ZONES.coffee.h / 2 - 20}px`,
          width: '40px',
          height: '40px',
          background: 'rgba(236, 72, 153, 0.15)',
          border: '2px solid rgba(236, 72, 153, 0.4)',
          borderRadius: '50%',
          pointerEvents: 'none'
        }} />

        {/* Render Agents Avatars walking */}
        {Object.values(agentStates).map((state) => {
          const agent = agents.find(a => a.id === state.id);
          if (!agent) return null;

          const isHovered = hoveredAgent?.id === agent.id;

          return (
            <div
              key={state.id}
              onMouseEnter={() => setHoveredAgent(agent)}
              onMouseLeave={() => setHoveredAgent(null)}
              style={{
                position: 'absolute',
                left: `${state.x - 16}px`,
                top: `${state.y - 16}px`,
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.4rem',
                borderRadius: '50%',
                background: selectedAgentIds.includes(state.id) ? 'rgba(139, 92, 246, 0.25)' : 'rgba(255, 255, 255, 0.05)',
                border: selectedAgentIds.includes(state.id) ? '2px solid #8b5cf6' : '1px solid rgba(255, 255, 255, 0.2)',
                boxShadow: selectedAgentIds.includes(state.id) ? '0 0 10px #8b5cf6' : 'none',
                cursor: 'pointer',
                transition: 'transform 0.1s ease, border-color 0.2s',
                zIndex: isHovered || state.bubbleText ? 100 : 10,
                animation: state.x !== state.targetX || state.y !== state.targetY ? 'bobbing 0.5s infinite alternate' : 'none'
              }}
            >
              {/* Character Avatar */}
              {agent.avatar || '👤'}

              {/* Speech Bubble */}
              {state.bubbleText && (
                <div style={{
                  position: 'absolute',
                  bottom: '38px',
                  background: '#fff',
                  color: '#000',
                  padding: '6px 10px',
                  borderRadius: '10px',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  whiteSpace: 'nowrap',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  border: '1px solid #e4e4e7',
                  pointerEvents: 'none',
                  animation: 'fadeIn 0.2s ease-out'
                }}>
                  {state.bubbleText}
                  <div style={{
                    position: 'absolute',
                    top: '100%',
                    left: '50%',
                    marginLeft: '-5px',
                    borderWidth: '5px',
                    borderStyle: 'solid',
                    borderColor: '#fff transparent transparent transparent'
                  }} />
                </div>
              )}

              {/* Status Dot */}
              {agent.status && agent.status !== 'Disponível' && (
                <span style={{
                  position: 'absolute',
                  bottom: '-2px',
                  right: '-2px',
                  width: '10px',
                  height: '10px',
                  borderRadius: '50%',
                  background: '#fbbf24',
                  border: '2px solid #040711',
                  boxShadow: '0 0 6px #fbbf24'
                }} />
              )}
            </div>
          );
        })}

        {/* Hover Agent Details Drawer Overlay */}
        {hoveredAgent && (
          <div className="glass" style={{
            position: 'absolute',
            bottom: '16px',
            left: '16px',
            padding: '12px 16px',
            zIndex: 200,
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: 'rgba(15, 23, 42, 0.85)',
            border: '1px solid rgba(255,255,255,0.15)',
            textAlign: 'left',
            animation: 'fadeIn 0.2s ease-out'
          }}>
            <span style={{ fontSize: '2rem' }}>{hoveredAgent.avatar}</span>
            <div>
              <strong style={{ fontSize: '0.85rem', color: '#fff', display: 'block' }}>{hoveredAgent.name}</strong>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', display: 'block' }}>{hoveredAgent.role} ({hoveredAgent.level})</span>
              <span style={{
                fontSize: '0.68rem',
                color: hoveredAgent.status && hoveredAgent.status !== 'Disponível' ? '#fbbf24' : '#34d399',
                fontWeight: 700
              }}>
                {hoveredAgent.status ? `⚙️ ${hoveredAgent.status}` : '✓ Disponível'}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* bobbing walking animation styles */}
      <style>{`
        @keyframes bobbing {
          from { transform: translateY(0); }
          to { transform: translateY(-4px); }
        }
      `}</style>
    </div>
  );
};
