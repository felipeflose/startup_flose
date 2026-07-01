import React, { useState, useCallback, useMemo } from 'react';

// Define os tipos de estado e jogada
type Player = 'X' | 'O' | null;
type BoardState = Player[];

// Componente de célula individual
const Square: React.FC<{ value: Player; onClick: () => void; disabled: boolean }> = ({ value, onClick, disabled }) => {
    return (
        <button
            className={`square ${value ? (value === 'X' ? 'winner-x' : 'winner-o') : ''}`}
            onClick={disabled ? undefined : onClick}
            disabled={disabled}
        >
            {value}
        </button>
    );
};

// Componente principal do Jogo da Velha
const TicTacToeGame: React.FC = () => {
    // Estado do tabuleiro inicializado com 9 nulos
    const [board, setBoard] = useState<BoardState>(Array(9).fill(null));
    // Estado do jogador atual
    const [currentPlayer, setCurrentPlayer] = useState<'X' | 'O'>('X');
    // Estado do vencedor
    const [winner, setWinner] = useState<Player | null>(null);

    // Função para verificar se houve vencedor ou empate
    const calculateWinner = useCallback((boardState: BoardState): Player | null => {
        const lines = [
            [0, 1, 2], // Linha 1
            [3, 4, 5], // Linha 2
            [6, 7, 8], // Linha 3
            [0, 3, 6], // Coluna 1
            [1, 4, 7], // Coluna 2
            [2, 5, 8], // Coluna 3
            [0, 4, 8], // Diagonal 1
            [2, 4, 6]  // Diagonal 2
        ];

        for (const [a, b, c] of lines) {
            if (boardState[a] && boardState[a] === boardState[b] && boardState[a] === boardState[c]) {
                return boardState[a]; // Retorna o jogador vencedor
            }
        }
        return null; // Sem vencedor
    }, []);

    // Manipulador de clique (Lógica principal do jogo)
    const handleClick = useCallback((index: number) => {
        // 1. Se houver um vencedor ou o jogo já estiver cheio, não faz nada.
        if (winner || board[index] !== null) {
            return;
        }

        // 2. Criar um novo estado de tabuleiro (imutabilidade)
        const newBoard = [...board];
        newBoard[index] = currentPlayer;
        
        // 3. Atualizar o estado do tabuleiro
        setBoard(newBoard);

        // 4. Verificar o vencedor
        const newWinner = calculateWinner(newBoard);
        setWinner(newWinner);

        // 5. Se não houver vencedor, alternar o jogador
        if (!newWinner) {
            setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
        }
    }, [board, currentPlayer, winner, calculateWinner]);

    // Função de resetar o jogo
    const resetGame = useCallback(() => {
        setBoard(Array(9).fill(null));
        setCurrentPlayer('X');
        setWinner(null);
    }, []);

    // Determinar o texto de status do jogo
    const status = useMemo(() => {
        if (winner) {
            return `Vencedor: ${winner === 'X' ? 'X' : 'O'}`;
        } else if (board.every(cell => cell !== null)) {
            return 'Empate!';
        } else {
            return `Vez de: ${currentPlayer === 'X' ? 'X' : 'O'}`;
        }
    }, [winner, board, currentPlayer]);

    return (
        <div style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
            <h1>Jogo da Velha (Tic-Tac-Toe)</h1>
            <div style={{ marginBottom: '20px' }}>
                <p style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{status}</p>
                <button onClick={resetGame} style={{ padding: '10px 20px', fontSize: '1em', cursor: 'pointer' }}>
                    Reiniciar Jogo
                </button>
            </div>
            
            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(3, 1fr)', 
                gap: '10px', 
                maxWidth: '400px', 
                margin: '0 auto' 
            }}>
                {[0, 1, 2].map(i => (
                    <Square 
                        key={i} 
                        value={board[i]} 
                        onClick={() => handleClick(i)} 
                        disabled={!!winner || board[i] !== null}
                    />
                ))}
                {[3, 4, 5].map(i => (
                    <Square 
                        key={i} 
                        value={board[i]} 
                        onClick={() => handleClick(i)} 
                        disabled={!!winner || board[i] !== null}
                    />
                ))}
                {[6, 7, 8].map(i => (
                    <Square 
                        key={i} 
                        value={board[i]} 
                        onClick={() => handleClick(i)} 
                        disabled={!!winner || board[i] !== null}
                    />
                ))}
            </div>
            
            {/* 
              NOTA TÉCNICA (Débito Técnico KAN-1969):
              A gestão de estado poderia ser encapsulada em um Hook customizado (useGameLogic) 
              para separar completamente a lógica de negócio da UI (Separation of Concerns), 
              melhorando a testabilidade e a reusabilidade em futuras sprints.
            */}
        </div>
    );
}

export default TicTacToeGame;