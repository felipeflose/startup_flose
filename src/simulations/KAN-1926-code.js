import React, { useState, useCallback, useMemo } from 'react';

// --- Types ---
interface UserProfile {
  username: string;
  points: number;
  level: number;
  badges: string[];
  progress: number; // e.g., tasks completed
}

interface Achievement {
  id: string;
  name: string;
  pointsRequired: number;
  description: string;
}

// --- Constants ---
const INITIAL_PROFILE: UserProfile = {
  username: 'daviddev',
  points: 0,
  level: 1,
  badges: [],
  progress: 0,
};

const ACHIEVEMENTS: Achievement[] = [
  { id: 'first_login', name: 'Novato', pointsRequired: 10, description: 'Bem-vindo à Flose!' },
  { id: 'task_completer', name: 'Mestre da Tarefa', pointsRequired: 50, description: 'Complete 5 tarefas.' },
  { id: 'power_user', name: 'Ninja do Código', pointsRequired: 150, description: 'Alcance 150 pontos.' },
];

/**
 * Hook para gerenciar a lógica de gamificação (MVP).
 * @returns [profile, updateProfile]
 */
const useGamificationLogic = () => {
  const [profile, setProfile] = useState<UserProfile>(INITIAL_PROFILE);

  const calculateLevel = useCallback((points: number): number => {
    // Lógica simplificada: Níveis aumentam a cada 100 pontos.
    return Math.floor(points / 100) + 1;
  }, []);

  const updateProfile = useCallback((newPoints: number, newProgress: number) => {
    setProfile(prev => {
      let newProfile: UserProfile = {
        ...prev,
        points: prev.points + newPoints,
        progress: newProgress,
        level: calculateLevel(prev.points + newPoints),
      };

      // 1. Awarding Points
      // (Implementação Simplificada: Apenas adiciona pontos)

      // 2. Checking Achievements
      const awardedBadges: string[] = [];
      let updatedBadges = [...prev.badges];

      ACHIEVEMENTS.forEach(achievement => {
        if (newProfile.points >= achievement.pointsRequired && !prev.badges.includes(achievement.id)) {
          updatedBadges.push(achievement.id);
          awardedBadges.push(achievement.name);
        }
      });

      newProfile.badges = updatedBadges;

      return newProfile;
    });
  }, [calculateLevel]);

  /**
   * Simula a ação de um usuário (ex: completar uma tarefa).
   * @param pointsGained Pontos a serem ganhos.
   * @param progressIncrement Incremento de progresso.
   */
  const performAction = useCallback((pointsGained: number, progressIncrement: number) => {
    console.log(`[KAN-1926] Performing action: +${pointsGained} points, +${progressIncrement} progress.`);
    updateProfile(pointsGained, progressIncrement);
  }, [updateProfile]);

  // Technical Debt Note:
  // ---------------------------------------------------------------------------
  // DEBT: A persistência de dados (setProfile) atualmente simula o estado.
  // DEBT: É necessária a integração com o serviço de usuário (API/Backend)
  //       para garantir que os pontos e badges sejam salvos de forma transacional.
  // DEBT: A lógica de cálculo de nível e achievement deve ser movida para um
  //       serviço de regras de negócio (Rule Engine Service) para testes unitários e escalabilidade.
  // ---------------------------------------------------------------------------

  return { profile, performAction };
};

// --- Components ---

const BadgeCard: React.FC<{ name: string; description: string }> = ({ name, description }) => (
  <div style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '8px', flex: 1, minWidth: '150px' }}>
    <h4 style={{ margin: '0 0 5px', color: '#4CAF50' }}>🏆 {name}</h4>
    <p style={{ fontSize: '0.9em', margin: 0 }}>{description}</p>
  </div>
);

const DashboardHeader: React.FC<{ profile: UserProfile }> = ({ profile }) => (
  <div style={{ display: 'flex', justifyContent: 'space-around', padding: '20px', backgroundColor: '#f9f9ff', borderRadius: '12px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
    <div style={{ textAlign: 'center' }}>
      <h2 style={{ margin: 0, color: '#333' }}>{profile.username}</h2>
      <p style={{ fontSize: '1.2em', color: '#666' }}>Engenheiro de Software</p>
    </div>

    <div style={{ flex: 1, textAlign: 'center', padding: '0 20px' }}>
      <h3 style={{ margin: '0 0 5px' }}>Nível {profile.level}</h3>
      <div style={{ fontSize: '3em', color: '#FF9800' }}>⭐</div>
      <p style={{ color: '#888' }}>Status</p>
    </div>

    <div style={{ flex: 1, textAlign: 'center', padding: '0 20px' }}>
      <h3 style={{ margin: '0 0 5px' }}>{profile.points}</h3>
      <div style={{ fontSize: '3em', color: '#2196F3' }}>✨</div>
      <p style={{ color: '#888' }}>Pontos</p>
    </div>
  </div>
);

const Dashboard: React.FC = () => {
  const { profile, performAction } = useGamificationLogic();

  const handleTaskCompletion = () => {
    // Simula a conclusão de uma tarefa que rende 30 pontos e 1 unidade de progresso.
    performAction(30, 1);
  };

  const handleProjectMilestone = () => {
    // Simula um grande marco, rendendo 80 pontos e 5 unidades de progresso.
    performAction(80, 5);
  };

  const renderBadges = useMemo(() => {
    return ACHIEVEMENTS.filter(ach => profile.badges.includes(ach.id)).map(ach => (
      <BadgeCard key={ach.id} name={ach.name} description={ach.description} />
    ));
  }, [profile.badges]);

  return (
    <div style={{ maxWidth: '900px', margin: '50px auto', padding: '20px', fontFamily: 'Arial, sans-serif', background: '#fff', borderRadius: '15px', boxShadow: '0 4px 15px rgba(0,0,0,0.1)' }}>
      <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '30px' }}>🚀 Gamificação Flose Startup (KAN-1926)</h1>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
        MVP Implementado. Próxima Sprint: Refatoração e Integração Backend (CTO).
      </p>

      <DashboardHeader profile={profile} />

      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
        {/* Coluna de Ações */}
        <div style={{ flex: 2, padding: '20px', border: '1px solid #e0e0e0', borderRadius: '10px', backgroundColor: '#fafafa' }}>
          <h2 style={{ color: '#333', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>📈 Ações e Progressão</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>
            Simule ações para testar o sistema de pontuação e níveis.
          </p>

          <button
            onClick={handleTaskCompletion}
            style={{
              padding: '12px 25px',
              marginRight: '15px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1em',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#1976D2'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#2196F3'}
          >
            ✅ Concluir Tarefa (30 pts)
          </button>

          <button
            onClick={handleProjectMilestone}
            style={{
              padding: '12px 25px',
              backgroundColor: '#FF9800',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1em',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#F57C00'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FF9800'}
          >
            🚀 Marco de Projeto (80 pts)
          </button>
        </div>

        {/* Coluna de Badges */}
        <div style={{ flex: 1, padding: '20px', border: '1px solid #e0e0e0', borderRadius: '10px', backgroundColor: '#fafafa' }}>
          <h2 style={{ color: '#333', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>🏆 Badges Conquistados</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '15px' }}>
            {renderBadges.length > 0 ? renderBadges : <p style={{ color: '#999' }}>Nenhum badge ainda. Continue progredindo!</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;