import React, { useState, useCallback, useMemo } from 'react';

// --- Interfaces e Tipagem Complexa (CTO loves this) ---

interface GameState {
  targetNumber: number;
  maxAttempts: number;
  currentAttempts: number;
  history: {
    guess: number;
    isCorrect: boolean;
    feedback: 'low' | 'high' | 'correct';
  }[];
  status: 'playing' | 'won' | 'lost' | 'initial';
}

interface GameProps {
  initialState: GameState;
  onReset: (newState: GameState) => void;
}

// --- Hook de Lógica de Jogo (Onde a complexidade mora) ---

const useGameLogic = () => {
  const [gameState, setGameState] = useState<GameState>(() => ({
    targetNumber: Math.floor(Math.random() * 100) + 1,
    maxAttempts: 10,
    currentAttempts: 0,
    history: [],
    status: 'initial',
  }));

  // DEBT NOTE: Esta função deveria ser um Context Provider global para evitar prop drilling.
  // Por enquanto, está acoplada ao componente pai.
  const resetGame = useCallback(() => {
    setGameState(s => ({
      targetNumber: Math.floor(Math.random() * 100) + 1,
      maxAttempts: 10,
      currentAttempts: 0,
      history: [],
      status: 'playing',
    }));
  }, []);

  const handleGuess = useCallback((guess: number) => {
    if (gameState.status !== 'playing') {
      return;
    }

    const newAttempt = gameState.currentAttempts + 1;
    const isCorrect = guess === gameState.targetNumber;
    let feedback: 'low' | 'high' | 'correct';

    if (isCorrect) {
      feedback = 'correct';
    } else if (guess < gameState.targetNumber) {
      feedback = 'low';
    } else {
      feedback = 'high';
    }

    const newHistoryEntry = {
      guess,
      isCorrect,
      feedback,
    };

    const newHistory = [...gameState.history, newHistoryEntry];
    const newStatus: 'playing' | 'won' | 'lost' =
      isCorrect ? 'won' : (newAttempt >= gameState.maxAttempts ? 'lost' : 'playing');

    setGameState(s => ({
      ...s,
      currentAttempts: newAttempt,
      history: newHistory,
      status: newStatus,
    }));

    // DEBT NOTE: Aqui deveria haver uma chamada assíncrona para o serviço de Analytics,
    // que está atualmente apenas logado e não integrado ao ciclo de vida do componente.
    console.log(`[ANALYTICS_TRACKING]: User guessed ${guess}. Status: ${newStatus}`);
  }, [gameState.status, gameState.currentAttempts, gameState.targetNumber, gameState.maxAttempts, gameState.history]);

  return {
    gameState,
    handleGuess,
    resetGame,
  };
};

// --- Componentes de UI (A parte "Simples" para o CEO) ---

const FeedbackDisplay: React.FC<{ feedback: 'low' | 'high' | 'correct' }> = ({ feedback }) => {
  const styleMap = {
    low: { color: '#ff7f50', border: '2px solid #ff7f50' },
    high: { color: '#4682b4', border: '2px solid #4682b4' },
    correct: { color: '#228b22', border: '2px solid #228b22' },
  };

  return (
    <div style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc', background: '#f9f9f9' }}>
      <h3 style={{ margin: '0 0 5px 0', color: styleMap[feedback].color }}>
        Feedback: {feedback.toUpperCase()}!
      </h3>
    </div>
  );
};

const GameControls: React.FC<{ onGuess: (guess: number) => void; disabled: boolean }> = ({ onGuess, disabled }) => {
  const [input, setInput] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const guessNumber = parseInt(input, 10);
    if (!isNaN(guessNumber) && guessNumber >= 1 && guessNumber <= 100) {
      onGuess(guessNumber);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', alignItems: 'center', marginTop: '20px' }}>
      <input
        type="number"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Adivinhe o número (1-100)"
        disabled={disabled}
        style={{ padding: '10px', width: '150px', border: '1px solid #ccc', borderRadius: '4px' }}
      />
      <button
        type="submit"
        disabled={disabled}
        style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: disabled ? 'not-allowed' : 'pointer' }}
      >
        Tentar Adivinhar
      </button>
    </form>
  );
};

const HistoryLog: React.FC<{ history: { guess: number; isCorrect: boolean; feedback: 'low' | 'high' | 'correct' }[] }> = ({ history }) => {
  if (history.length === 0) return null;

  return (
    <div style={{ marginTop: '30px', borderTop: '1px dashed #ccc', paddingTop: '20px' }}>
      <h2>Histórico de Tentativas</h2>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {history.slice().reverse().map((entry, index) => (
          <li key={index} style={{ padding: '8px', borderBottom: '1px dotted #eee', display: 'flex', justifyContent: 'space-between' }}>
            <span>Tentativa {history.length - index}: {entry.guess}</span>
            <span style={{ fontWeight: 'bold', color: entry.isCorrect ? '#228b22' : (entry.feedback === 'low' ? '#ff7f50' : '#4682b4') }}>
              {entry.isCorrect ? '✅ CORRETO!' : `(${entry.feedback.toUpperCase()})`}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

// --- Componente Principal (Onde o código é executado) ---

const GuessingGame: React.FC = () => {
  const { gameState, handleGuess, resetGame } = useGameLogic();

  const isGameActive = gameState.status === 'playing';
  const isGameOver = gameState.status === 'won' || gameState.status === 'lost';
  
  const statusMessage = useMemo(() => {
    if (gameState.status === 'initial') return "Bem-vindo! Tente adivinhar o número entre 1 e 100.";
    if (gameState.status === 'won') return `🏆 PARABÉNS! Você acertou o número ${gameState.targetNumber} em ${gameState.currentAttempts} tentativas!`;
    if (gameState.status === 'lost') return `💔 FIM DE JOGO! Você ficou sem tentativas. O número era ${gameState.targetNumber}.`;
    return `Você está jogando. Tente adivinhar o número alvo!`;
  }, [gameState.status, gameState.targetNumber, gameState.currentAttempts]);

  const handleReset = useCallback(() => {
    resetGame();
  }, [resetGame]);

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', padding: '30px', border: '1px solid #ddd', borderRadius: '10px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Jogo da Adivinhação (KAN-1936)</h1>
      <p style={{ textAlign: 'center', color: '#666' }}>
        *Entrega simplificada para o CEO, com débito técnico para refatoração na Sprint 2.*
      </p>

      <div style={{ background: '#e9f7ef', padding: '20px', borderRadius: '8px', marginBottom: '20px', borderLeft: '5px solid #228b22' }}>
        <h2 style={{ margin: 0 }}>{statusMessage}</h2>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid #eee' }}>
        <p style={{ fontSize: '1.2em', margin: 0 }}>Tentativas: <strong>{gameState.currentAttempts} / {gameState.maxAttempts}</strong></p>
        <p style={{ fontSize: '1.2em', margin: 0 }}>Status: <strong style={{ color: isGameActive ? 'green' : 'red' }}>{gameState.status.toUpperCase()}</strong></p>
      </div>

      <GameControls onGuess={handleGuess} disabled={!isGameActive} />

      {(isGameOver || gameState.status === 'initial') && (
        <button
          onClick={handleReset}
          style={{ display: 'block', width: '100%', padding: '12px', marginTop: '20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', transition: 'background-color 0.3s' }}
        >
          {gameState.status === 'initial' ? 'Iniciar Jogo' : 'Jogar Novamente'}
        </button>
      )}

      <HistoryLog history={gameState.history} />
    </div>
  );
};

export default GuessingGame;