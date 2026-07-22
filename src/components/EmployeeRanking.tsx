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

  const podiumOrder = top3.length === 3
    ? [top3[1], top3[0], top3[2]]
    : top3;

  const podiumHeights = [120, 180, 90];
  const podiumColors = [
    'linear-gradient(135deg, #94a3b8, #64748b)',
    'linear-gradient(135deg, #fbbf24, #f59e0b)',
    'linear-gradient(135deg, #cd7c2e, #a0522d)'
  ];
  const podiumLabels = ['🥈 2º', '🥇 1º', '🥉 3º'];
  const podiumGlow = [
    '0 0 20px rgba(148,163,184,0.4)',
    '0 0 40px rgba(251,191,36,0.6)',
    '0 0 20px rgba(205,124,46,0.4)'
  ];

  const rankBadge = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const rankColor = (rank: number, total: number) => {
    if (rank === 1) return '#fbbf24';
    if (rank === 2) return '#94a3b8';
    if (rank === 3) return '#cd7c2e';
    if (rank === total) return '#ef4444';
    return 'var(--text-secondary)';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>

      {/* Header */}
      <div style={{ textAlign: 'center' }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '12px',
          background: 'linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.05))',
          border: '1px solid rgba(251,191,36,0.3)',
          borderRadius: '16px', padding: '16px 32px'
        }}>
          <span style={{ fontSize: '2rem' }}>🏆</span>
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, background: 'linear-gradient(135deg, #fbbf24, #f97316)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Funcionário do Minuto
            </h2>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', margin: 0 }}>
              Rankings atualizam a cada 30s · {updatedAt ? new Date(updatedAt).toLocaleTimeString('pt-BR') : '—'}
            </p>
          </div>
          <span style={{ fontSize: '2rem' }}>⚡</span>
        </div>
      </div>

      {/* Score legend */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', flexWrap: 'wrap' }}>
        {[
          { icon: '✍️', label: 'Card Criado', pts: 10, color: '#a78bfa' },
          { icon: '💻', label: 'Card Executado', pts: 15, color: '#38bdf8' },
          { icon: '✅', label: 'Card Fechado', pts: 25, color: '#34d399' },
          { icon: '💬', label: 'Debate/Atividade', pts: 5, color: '#fb923c' },
        ].map(item => (
          <div key={item.label} style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            background: 'var(--bg-secondary)', borderRadius: '8px',
            padding: '6px 12px', fontSize: '0.75rem',
            border: `1px solid ${item.color}33`
          }}>
            <span>{item.icon}</span>
            <span style={{ color: 'var(--text-secondary)' }}>{item.label}</span>
            <span style={{ color: item.color, fontWeight: 700 }}>+{item.pts}pts</span>
          </div>
        ))}
      </div>

      {loading && rankings.length === 0 && (
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>Calculando rankings...</p>
      )}

      {/* PODIUM */}
      {top3.length > 0 && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: '16px', padding: '24px 0 0' }}>
          {(top3.length === 3 ? podiumOrder : top3).map((entry, i) => {
            const isCenter = top3.length === 3 ? i === 1 : i === 0;
            return (
              <div key={entry.agentId} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                {/* Champion crown */}
                {isCenter && <div style={{ fontSize: '2rem', animation: celebrating ? 'bounce 0.5s ease infinite alternate' : 'none' }}>👑</div>}

                {/* Avatar bubble */}
                <div style={{
                  width: isCenter ? '80px' : '64px',
                  height: isCenter ? '80px' : '64px',
                  borderRadius: '50%',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: isCenter ? '2.5rem' : '2rem',
                  background: podiumColors[i],
                  boxShadow: podiumGlow[i],
                  border: `3px solid ${isCenter ? '#fbbf24' : 'transparent'}`,
                  transition: 'all 0.3s'
                }}>
                  {entry.avatar}
                </div>

                {/* Name */}
                <div style={{ textAlign: 'center', maxWidth: '100px' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.2 }}>
                    {entry.name.split(' ')[0]}
                  </div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{entry.role.split(' ')[0]}</div>
                </div>

                {/* Podium block */}
                <div style={{
                  width: isCenter ? '120px' : '96px',
                  height: `${podiumHeights[i]}px`,
                  background: podiumColors[i],
                  borderRadius: '8px 8px 0 0',
                  display: 'flex', flexDirection: 'column',
                  alignItems: 'center', justifyContent: 'center', gap: '4px',
                  boxShadow: podiumGlow[i],
                  transition: 'all 0.5s ease'
                }}>
                  <div style={{ fontSize: isCenter ? '1.5rem' : '1.2rem' }}>{podiumLabels[i]}</div>
                  <div style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>{entry.totalScore}</div>
                  <div style={{ fontSize: '0.65rem', color: 'rgba(255,255,255,0.8)' }}>pontos</div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Prize alert for 1st */}
      {rankings[0]?.prize && (
        <div style={{
          background: 'linear-gradient(135deg, rgba(251,191,36,0.15), rgba(251,191,36,0.05))',
          border: '1px solid rgba(251,191,36,0.5)',
          borderRadius: '12px', padding: '14px 20px',
          display: 'flex', alignItems: 'center', gap: '12px'
        }}>
          <span style={{ fontSize: '1.5rem' }}>🏆</span>
          <div>
            <div style={{ fontWeight: 700, color: '#fbbf24', fontSize: '0.9rem' }}>{rankings[0].name} — CAMPEÃO!</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{rankings[0].prize}</div>
          </div>
        </div>
      )}

      {/* School penalty for last */}
      {last?.penalty && (
        <div style={{
          background: 'linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.04))',
          border: '1px solid rgba(239,68,68,0.4)',
          borderRadius: '12px', padding: '14px 20px',
          display: 'flex', alignItems: 'center', gap: '12px'
        }}>
          <span style={{ fontSize: '1.5rem' }}>🎓</span>
          <div>
            <div style={{ fontWeight: 700, color: '#ef4444', fontSize: '0.9rem' }}>{last.name} — ESCOLA OBRIGATÓRIA</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{last.penalty}</div>
          </div>
        </div>
      )}

      {/* Full Leaderboard */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          📊 Placar Completo
        </h3>
        {rankings.map((entry) => {
          const isFirst = entry.rank === 1;
          const isLast = entry.rank === rankings.length && rankings.length > 1;
          const barWidth = rankings[0].totalScore > 0
            ? Math.max(4, Math.round((entry.totalScore / rankings[0].totalScore) * 100))
            : 0;

          return (
            <div key={entry.agentId} style={{
              display: 'flex', alignItems: 'center', gap: '14px',
              padding: '14px 16px',
              borderRadius: '12px',
              background: isFirst
                ? 'linear-gradient(135deg, rgba(251,191,36,0.12), rgba(251,191,36,0.04))'
                : isLast
                  ? 'linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.03))'
                  : 'var(--bg-secondary)',
              border: `1px solid ${isFirst ? 'rgba(251,191,36,0.35)' : isLast ? 'rgba(239,68,68,0.3)' : 'var(--border-color)'}`,
              transition: 'all 0.2s'
            }}>
              {/* Rank badge */}
              <div style={{
                minWidth: '36px', textAlign: 'center',
                fontSize: entry.rank <= 3 ? '1.4rem' : '0.9rem',
                fontWeight: 800,
                color: rankColor(entry.rank, rankings.length)
              }}>
                {rankBadge(entry.rank)}
              </div>

              {/* Avatar */}
              <div style={{ fontSize: '1.5rem', minWidth: '32px', textAlign: 'center' }}>{entry.avatar}</div>

              {/* Name + bar */}
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-primary)' }}>
                    {entry.name}
                    {isFirst && <span style={{ marginLeft: '6px', fontSize: '0.7rem', background: 'rgba(251,191,36,0.2)', color: '#fbbf24', padding: '2px 6px', borderRadius: '4px' }}>CAMPEÃO</span>}
                    {isLast && <span style={{ marginLeft: '6px', fontSize: '0.7rem', background: 'rgba(239,68,68,0.2)', color: '#ef4444', padding: '2px 6px', borderRadius: '4px' }}>ESCOLA</span>}
                  </span>
                  <span style={{ fontWeight: 800, fontSize: '1rem', color: rankColor(entry.rank, rankings.length) }}>
                    {entry.totalScore} pts
                  </span>
                </div>

                {/* Progress bar */}
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${barWidth}%`,
                    borderRadius: '3px',
                    background: isFirst
                      ? 'linear-gradient(90deg, #fbbf24, #f97316)'
                      : isLast
                        ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                        : 'linear-gradient(90deg, var(--color-primary), var(--color-secondary))',
                    transition: 'width 0.8s ease'
                  }} />
                </div>

                {/* Stats */}
                <div style={{ display: 'flex', gap: '12px', fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                  <span>✍️ {entry.cardsCreated} criados</span>
                  <span>💻 {entry.cardsExecuted} executados</span>
                  <span>✅ {entry.cardsClosed} fechados</span>
                  <span>💬 {entry.debatesWon} atividades</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Refresh button */}
      <div style={{ textAlign: 'center' }}>
        <button
          onClick={fetchRankings}
          disabled={loading}
          style={{
            padding: '10px 28px',
            borderRadius: '8px',
            border: 'none',
            background: 'linear-gradient(135deg, #fbbf24, #f97316)',
            color: '#000',
            fontWeight: 700,
            fontSize: '0.85rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.6 : 1,
            transition: 'all 0.2s'
          }}
        >
          {loading ? '⟳ Calculando...' : '⟳ Atualizar Ranking'}
        </button>
      </div>

      <style>{`
        @keyframes bounce {
          from { transform: translateY(0); }
          to { transform: translateY(-8px); }
        }
      `}</style>
    </div>
  );
};
