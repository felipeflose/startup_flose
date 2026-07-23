import React, { useState, useEffect } from 'react';

interface RankEntry {
  rank: number;
  agentId: string;
  name: string;
  role: string;
  avatar: string;
  cardsCreated: number;
  cardsClosed: number;
  cardsExecuted: number;
  debatesWon: number;
  totalScore: number;
  prize: string | null;
  penalty: string | null;
}

export const EmployeeRanking: React.FC = () => {
  const [rankings, setRankings] = useState<RankEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  const [celebrating, setCelebrating] = useState(false);

  const fetchRankings = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5001/api/rankings');
      const data = await res.json();
      setRankings(data.rankings || []);
      setUpdatedAt(data.updatedAt);
      setCelebrating(true);
      setTimeout(() => setCelebrating(false), 3000);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
    const interval = setInterval(fetchRankings, 30000);
    return () => clearInterval(interval);
  }, []);

  const top3 = rankings.slice(0, 3);
  const last = rankings[rankings.length - 1];

  // Reorder for visual podium: 2nd, 1st, 3rd
  const podiumOrder = top3.length === 3
    ? [top3[1], top3[0], top3[2]]
    : top3;

  // Gold, Silver, Bronze styling
  const getPodiumConfig = (idx: number, isCenter: boolean) => {
    if (isCenter) {
      return {
        height: 200,
        gradient: 'linear-gradient(135deg, rgba(251, 191, 36, 0.25), rgba(245, 158, 11, 0.55))',
        border: '1px solid rgba(251, 191, 36, 0.7)',
        glow: '0 0 30px rgba(251, 191, 36, 0.45)',
        label: '🥇 1º Lugar',
        titleColor: '#fbbf24'
      };
    }
    // 2nd Place is left in podiumOrder [2nd, 1st, 3rd]
    if (idx === 0) {
      return {
        height: 140,
        gradient: 'linear-gradient(135deg, rgba(226, 232, 240, 0.2), rgba(148, 163, 184, 0.4))',
        border: '1px solid rgba(148, 163, 184, 0.5)',
        glow: '0 0 20px rgba(148, 163, 184, 0.25)',
        label: '🥈 2º Lugar',
        titleColor: '#cbd5e1'
      };
    }
    // 3rd Place is right
    return {
      height: 110,
      gradient: 'linear-gradient(135deg, rgba(254, 215, 170, 0.15), rgba(194, 65, 12, 0.35))',
      border: '1px solid rgba(194, 65, 12, 0.45)',
      glow: '0 0 20px rgba(194, 65, 12, 0.2)',
      label: '🥉 3º Lugar',
      titleColor: '#fb923c'
    };
  };

  const rankBadge = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const rankColor = (rank: number, total: number) => {
    if (rank === 1) return '#fbbf24';
    if (rank === 2) return '#cbd5e1';
    if (rank === 3) return '#fb923c';
    if (rank === total) return '#f87171';
    return 'var(--text-secondary)';
  };

  // Sparkle particles helper
  const sparkles = Array.from({ length: celebrating ? 25 : 8 });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', width: '100%' }}>
      {/* Header with glassmorphism */}
      <div style={{ textAlign: 'center', position: 'relative', overflow: 'hidden', borderRadius: '24px', padding: '24px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
        {/* Animated glowing backdrop */}
        <div style={{
          position: 'absolute', top: '-50%', left: '-50%', width: '200%', height: '200%',
          background: 'radial-gradient(circle, rgba(251,191,36,0.07) 0%, transparent 60%)',
          animation: 'rotateBg 20s linear infinite',
          pointerEvents: 'none'
        }} />

        <div style={{ position: 'relative', zIndex: 1, display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <div style={{ fontSize: '2.5rem', animation: 'float 3s ease-in-out infinite' }}>🏆</div>
          <h2 style={{ fontSize: '2rem', fontWeight: 800, background: 'linear-gradient(135deg, #fbbf24, #f97316)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', margin: '4px 0 0' }}>
            Quadro de Líderes e Medalhas
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0 }}>
            Rankings recalculados dinamicamente com base nas entregas · Última atualização: {updatedAt ? new Date(updatedAt).toLocaleTimeString('pt-BR') : '—'}
          </p>
        </div>
      </div>

      {/* Rules & Points Legend */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap' }}>
        {[
          { icon: '✍️', label: 'Card Criado', pts: 10, color: '#a78bfa' },
          { icon: '💻', label: 'Card Executado', pts: 15, color: '#38bdf8' },
          { icon: '✅', label: 'Card Fechado', pts: 25, color: '#34d399' },
          { icon: '💬', label: 'Atividade/Debates', pts: 5, color: '#fb923c' },
        ].map(item => (
          <div key={item.label} style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            background: 'rgba(255, 255, 255, 0.02)', borderRadius: '12px',
            padding: '8px 16px', fontSize: '0.8rem',
            border: `1px solid ${item.color}22`,
            backdropFilter: 'blur(8px)'
          }}>
            <span>{item.icon}</span>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>{item.label}</span>
            <span style={{ color: item.color, fontWeight: 700 }}>+{item.pts} pts</span>
          </div>
        ))}
      </div>

      {loading && rankings.length === 0 && (
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>Calculando rankings...</p>
      )}

      {/* PODIUM SECTION WITH FLOATING PARTICLES */}
      {top3.length > 0 && (
        <div style={{
          position: 'relative',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'flex-end',
          gap: '24px',
          padding: '40px 0 20px',
          minHeight: '340px',
          overflow: 'hidden',
          borderRadius: '24px',
          background: 'rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(255, 255, 255, 0.03)'
        }}>
          {/* Shine particles floating around */}
          {sparkles.map((_, i) => (
            <div
              key={i}
              className="sparkle-particle"
              style={{
                position: 'absolute',
                bottom: '10px',
                left: `${15 + Math.random() * 70}%`,
                width: `${4 + Math.random() * 6}px`,
                height: `${4 + Math.random() * 6}px`,
                background: '#fbbf24',
                borderRadius: '50%',
                boxShadow: '0 0 10px #fbbf24',
                animation: `floatSparkle ${3 + Math.random() * 4}s linear infinite`,
                animationDelay: `${Math.random() * 3}s`,
                opacity: 0,
                pointerEvents: 'none'
              }}
            />
          ))}

          {(top3.length === 3 ? podiumOrder : top3).map((entry, i) => {
            const isCenter = top3.length === 3 ? i === 1 : i === 0;
            const config = getPodiumConfig(i, isCenter);

            return (
              <div key={entry.agentId} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: 2 }}>
                {/* Crown for Champion */}
                {isCenter && (
                  <div style={{
                    fontSize: '2.5rem',
                    animation: 'bounceCrown 0.6s ease infinite alternate',
                    filter: 'drop-shadow(0 0 12px rgba(251,191,36,0.6))',
                    marginBottom: '-4px'
                  }}>
                    👑
                  </div>
                )}

                {/* Avatar container with metallic frames */}
                <div style={{
                  position: 'relative',
                  width: isCenter ? '90px' : '72px',
                  height: isCenter ? '90px' : '72px',
                  borderRadius: '50%',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: isCenter ? '3rem' : '2.25rem',
                  background: 'rgba(255, 255, 255, 0.03)',
                  boxShadow: config.glow,
                  border: config.border,
                  zIndex: 3,
                  transform: `translateY(${isCenter ? '-12px' : '0px'})`,
                  transition: 'all 0.3s'
                }}>
                  {entry.avatar}
                  <div style={{
                    position: 'absolute',
                    bottom: '-4px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    background: config.titleColor,
                    color: '#000',
                    fontSize: '0.62rem',
                    fontWeight: 800,
                    padding: '2px 8px',
                    borderRadius: '8px',
                    whiteSpace: 'nowrap',
                    textTransform: 'uppercase',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.3)'
                  }}>
                    {entry.totalScore} pts
                  </div>
                </div>

                {/* Name & Role tag */}
                <div style={{ textAlign: 'center', marginTop: '4px', marginBottom: '12px', maxWidth: '120px' }}>
                  <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--text-primary)', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                    {entry.name}
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{entry.role}</div>
                </div>

                {/* Podium Block */}
                <div style={{
                  width: isCenter ? '140px' : '110px',
                  height: `${config.height}px`,
                  background: config.gradient,
                  border: config.border,
                  borderRadius: '16px 16px 0 0',
                  display: 'flex', flexDirection: 'column',
                  alignItems: 'center', justifyContent: 'center', gap: '6px',
                  boxShadow: `0 10px 30px rgba(0,0,0,0.4), ${config.glow}`,
                  backdropFilter: 'blur(12px)',
                  transition: 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                }}>
                  <div style={{ fontSize: isCenter ? '1.15rem' : '0.9rem', fontWeight: 800, color: '#fff', textShadow: '0 2px 4px rgba(0,0,0,0.5)' }}>
                    {config.label}
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: 0.8 }}>
                    <span style={{ fontSize: '0.65rem', color: 'rgba(255,255,255,0.7)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Entregas</span>
                    <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#fff' }}>
                      ✅ {entry.cardsClosed}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Prize / Governance Awards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
        {rankings[0]?.prize && (
          <div style={{
            position: 'relative', overflow: 'hidden',
            background: 'linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(251, 191, 36, 0.02))',
            border: '1px solid rgba(251, 191, 36, 0.25)',
            borderRadius: '16px', padding: '16px 20px',
            display: 'flex', alignItems: 'center', gap: '16px',
            backdropFilter: 'blur(10px)'
          }}>
            <span style={{ fontSize: '2rem', filter: 'drop-shadow(0 0 8px rgba(251,191,36,0.5))' }}>👑</span>
            <div>
              <div style={{ fontWeight: 800, color: '#fbbf24', fontSize: '0.95rem' }}>Prêmio de Liderança (1º Lugar): {rankings[0].name}</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: 1.4 }}>{rankings[0].prize}</div>
            </div>
          </div>
        )}

        {last?.penalty && rankings.length > 1 && (
          <div style={{
            position: 'relative', overflow: 'hidden',
            background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(239, 68, 68, 0.02))',
            border: '1px solid rgba(239, 68, 68, 0.25)',
            borderRadius: '16px', padding: '16px 20px',
            display: 'flex', alignItems: 'center', gap: '16px',
            backdropFilter: 'blur(10px)'
          }}>
            <span style={{ fontSize: '2rem', filter: 'drop-shadow(0 0 8px rgba(239,68,68,0.5))' }}>🎓</span>
            <div>
              <div style={{ fontWeight: 800, color: '#f87171', fontSize: '0.95rem' }}>Alerta de Capacitação (Lanterna): {last.name}</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: 1.4 }}>{last.penalty}</div>
            </div>
          </div>
        )}
      </div>

      {/* Leaderboard Table with Custom Glass Rows */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          📊 Classificação Geral <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 500 }}>({rankings.length} agentes alocados)</span>
        </h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {rankings.map((entry) => {
            const isFirst = entry.rank === 1;
            const isLast = entry.rank === rankings.length && rankings.length > 1;
            const barWidth = rankings[0].totalScore > 0
              ? Math.max(5, Math.round((entry.totalScore / rankings[0].totalScore) * 100))
              : 0;

            return (
              <div key={entry.agentId} className="rank-row" style={{
                display: 'flex', alignItems: 'center', gap: '16px',
                padding: '16px 20px',
                borderRadius: '16px',
                background: isFirst
                  ? 'linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(251, 191, 36, 0.02))'
                  : isLast
                    ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.06), rgba(239, 68, 68, 0.01))'
                    : 'rgba(255, 255, 255, 0.02)',
                border: `1px solid ${isFirst ? 'rgba(251, 191, 36, 0.2)' : isLast ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255, 255, 255, 0.04)'}`,
                backdropFilter: 'blur(8px)',
                transition: 'all 0.2s ease-in-out'
              }}>
                {/* Rank Badge */}
                <div style={{
                  minWidth: '40px', textAlign: 'center',
                  fontSize: entry.rank <= 3 ? '1.5rem' : '0.95rem',
                  fontWeight: 800,
                  color: rankColor(entry.rank, rankings.length)
                }}>
                  {rankBadge(entry.rank)}
                </div>

                {/* Avatar with dynamic status indicator */}
                <div style={{ fontSize: '1.8rem', minWidth: '40px', textAlign: 'center', position: 'relative' }}>
                  {entry.avatar}
                </div>

                {/* Main statistics container */}
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 800, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                      {entry.name}
                      <span style={{ marginLeft: '8px', fontSize: '0.72rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
                        {entry.role}
                      </span>
                    </span>
                    <span style={{ fontWeight: 800, fontSize: '1.1rem', color: rankColor(entry.rank, rankings.length) }}>
                      {entry.totalScore} pts
                    </span>
                  </div>

                  {/* Glass progress bar */}
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.04)', borderRadius: '4px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.02)' }}>
                    <div style={{
                      height: '100%',
                      width: `${barWidth}%`,
                      borderRadius: '4px',
                      background: isFirst
                        ? 'linear-gradient(90deg, #fbbf24, #f97316)'
                        : isLast
                          ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                          : 'linear-gradient(90deg, var(--color-primary), var(--color-secondary))',
                      boxShadow: isFirst ? '0 0 10px rgba(251,191,36,0.5)' : 'none',
                      transition: 'width 1s cubic-bezier(0.19, 1, 0.22, 1)'
                    }} />
                  </div>

                  {/* Detailed counter icons */}
                  <div style={{ display: 'flex', gap: '16px', fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                    <span>✍️ {entry.cardsCreated} criados</span>
                    <span>💻 {entry.cardsExecuted} executados</span>
                    <span>✅ {entry.cardsClosed} fechados</span>
                    <span>💬 {entry.debatesWon} participações</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Control Buttons */}
      <div style={{ textAlign: 'center', marginTop: '12px' }}>
        <button
          onClick={fetchRankings}
          disabled={loading}
          className="glow-btn"
          style={{
            padding: '12px 36px',
            borderRadius: '12px',
            border: 'none',
            background: 'linear-gradient(135deg, #fbbf24, #f97316)',
            color: '#000',
            fontWeight: 800,
            fontSize: '0.9rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.6 : 1,
            boxShadow: '0 4px 20px rgba(251, 191, 36, 0.3)',
            transition: 'all 0.2s ease'
          }}
        >
          {loading ? '⟳ Recalculando...' : '⟳ Atualizar Placar'}
        </button>
      </div>

      {/* Scoped CSS animations for beautiful wow effects */}
      <style>{`
        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
          100% { transform: translateY(0px); }
        }
        @keyframes rotateBg {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        @keyframes floatSparkle {
          0% {
            transform: translateY(0px) scale(0) rotate(0deg);
            opacity: 0;
          }
          20% {
            opacity: 0.8;
          }
          80% {
            opacity: 0.8;
          }
          100% {
            transform: translateY(-260px) scale(1.2) rotate(180deg);
            opacity: 0;
          }
        }
        @keyframes bounceCrown {
          from { transform: translateY(0) scale(1); }
          to { transform: translateY(-6px) scale(1.05); }
        }
        .rank-row:hover {
          transform: translateX(4px);
          background: rgba(255, 255, 255, 0.04) !important;
          border-color: rgba(255, 255, 255, 0.08) !important;
        }
        .glow-btn:hover:not(:disabled) {
          transform: scale(1.03);
          boxShadow: 0 6px 25px rgba(251, 191, 36, 0.5) !important;
        }
      `}</style>
    </div>
  );
};
