import React, { useState, useEffect } from 'react';

interface RecruitmentSession {
  ticketKey: string;
  ticketSummary: string;
  applicant1: string;
  applicant2: string;
  winner: string;
  transcript: string;
  timestamp: string;
}

export const RecruitmentChamberViewer: React.FC = () => {
  const [sessions, setSessions] = useState<RecruitmentSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSession, setSelectedSession] = useState<RecruitmentSession | null>(null);

  const fetchRecruitmentHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5001/api/decisions');
      const data = await res.json();
      // Filtrar decisões de recrutamento
      const recruitmentData = data.filter((d: any) => 
        (d.action && d.action.includes('entrevista')) || 
        (d.ticketSummary && d.ticketSummary.includes('Recrutamento')) ||
        (d.ticketKey && d.ticketKey.includes('KAN'))
      ).map((d: any) => ({
        ticketKey: d.ticketKey || 'RECRUTAMENTO',
        ticketSummary: d.ticketSummary || 'Processo Seletivo de Seleção de Colaborador',
        applicant1: 'Candidato 1 (Pool Técnico)',
        applicant2: 'Candidato 2 (Pool Técnico)',
        winner: d.agentName || 'Vencedor do Processo',
        transcript: d.action || 'Ata de seleção realizada com sucesso no Chamber sob mediação do CEO e CTO.',
        timestamp: d.timestamp || new Date().toISOString()
      }));

      setSessions(recruitmentData);
      if (recruitmentData.length > 0) setSelectedSession(recruitmentData[0]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecruitmentHistory();
    const interval = setInterval(fetchRecruitmentHistory, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '100%' }}>
      {/* Header Visual Premium */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(59, 130, 246, 0.15))',
        border: '1px solid rgba(168, 85, 247, 0.3)',
        borderRadius: '20px',
        padding: '24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ fontSize: '2.5rem', background: 'rgba(168, 85, 247, 0.2)', padding: '12px', borderRadius: '16px' }}>👔</div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 800, color: '#f3e8ff' }}>
              Câmara de Entrevistas & Recrutamento Real
            </h2>
            <p style={{ margin: '4px 0 0', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Acompanhamento ao vivo das atas de seleção, testes práticos e aprovação hierárquica por cargo no Jira
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{
            background: 'rgba(34, 197, 94, 0.2)',
            color: '#4ade80',
            border: '1px solid rgba(34, 197, 94, 0.4)',
            padding: '6px 14px',
            borderRadius: '20px',
            fontSize: '0.75rem',
            fontWeight: 700
          }}>
            ● PROCESSO SELETIVO ATIVO
          </span>
        </div>
      </div>

      {loading && sessions.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>Carregando atas de entrevistas...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '350px 1fr', gap: '20px' }}>
          {/* Lista Lateral de Processos Seletivos */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px', margin: '0 0 4px' }}>
              Processos Seletivos Concluídos ({sessions.length})
            </h3>
            {sessions.map((session, idx) => (
              <div
                key={idx}
                onClick={() => setSelectedSession(session)}
                style={{
                  padding: '16px',
                  borderRadius: '14px',
                  background: selectedSession === session ? 'rgba(168, 85, 247, 0.2)' : 'rgba(255, 255, 255, 0.02)',
                  border: selectedSession === session ? '1px solid rgba(168, 85, 247, 0.5)' : '1px solid rgba(255, 255, 255, 0.05)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ color: '#c084fc', fontWeight: 700, fontSize: '0.8rem' }}>{session.ticketKey}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>
                    {new Date(session.timestamp).toLocaleTimeString('pt-BR')}
                  </span>
                </div>
                <div style={{ fontWeight: 600, fontSize: '0.85rem', color: '#f3e8ff', marginBottom: '8px' }}>
                  {session.ticketSummary.slice(0, 45)}...
                </div>
                <div style={{ fontSize: '0.75rem', color: '#4ade80', fontWeight: 600 }}>
                  🏆 Vencedor: {session.winner}
                </div>
              </div>
            ))}
          </div>

          {/* Leitor da Ata da Entrevista */}
          {selectedSession ? (
            <div style={{
              background: 'rgba(15, 17, 26, 0.8)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: '16px',
              padding: '24px',
              display: 'flex',
              flexDirection: 'column',
              gap: '16px'
            }}>
              <div style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ background: '#c084fc22', color: '#c084fc', padding: '4px 10px', borderRadius: '6px', fontSize: '0.75rem', fontWeight: 700 }}>
                    CARD JIRA: {selectedSession.ticketKey}
                  </span>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                    {new Date(selectedSession.timestamp).toLocaleString('pt-BR')}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.25rem', color: '#fff', margin: '12px 0 4px' }}>
                  {selectedSession.ticketSummary}
                </h3>
              </div>

              {/* Ata da Entrevista em Markdown Styled */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <h4 style={{ margin: 0, color: '#f3e8ff', fontSize: '0.95rem' }}>📄 Ata Transcrita da Seleção no Chamber</h4>
                <div style={{
                  background: 'rgba(0, 0, 0, 0.4)',
                  border: '1px solid rgba(168, 85, 247, 0.2)',
                  borderRadius: '12px',
                  padding: '16px',
                  color: '#e9d5ff',
                  fontSize: '0.9rem',
                  lineHeight: '1.6',
                  whiteSpace: 'pre-wrap',
                  maxHeight: '400px',
                  overflowY: 'auto'
                }}>
                  {selectedSession.transcript}
                </div>
              </div>

              {/* Status de Admissão Hierárquica */}
              <div style={{
                background: 'rgba(34, 197, 94, 0.1)',
                border: '1px solid rgba(34, 197, 94, 0.3)',
                borderRadius: '12px',
                padding: '12px 16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '1.2rem' }}>🎉</span>
                  <div>
                    <div style={{ color: '#4ade80', fontWeight: 700, fontSize: '0.85rem' }}>CONTRATAÇÃO HOMOLOGADA E SALVA NO JIRA</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>Colaborador {selectedSession.winner} admitido e atribuído ao chamado técnico.</div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-secondary)' }}>Selecione um processo seletivo ao lado.</p>
          )}
        </div>
      )}
    </div>
  );
};
