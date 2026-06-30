import React, { useState, useCallback } from 'react';

// Define types for clarity
type BoardState = (string | null)[];
type Player = 'X' | 'O';

/**
 * Função utilitária para verificar se houve um vencedor no tabuleiro.
 * @param board O estado atual do tabuleiro.
 * @returns O jogador vencedor ('X', 'O') ou null se ninguém venceu.
 */
const calculateWinner = (board: BoardState): Player | null => {
    const lines = [
        [0, 1, 2], // Linha 1
        [3, 4, 5], // Linha 2
        [6, 7, 8], // Linha 3
        [0, 3, 6], // Coluna 1
        [1, 4, 7], // Coluna 2
        [2, 5, 8], // Coluna 3
        [0, 4, 8], // Diagonal 1
        [2, 4, 6], // Diagonal 2
    ];

    for (const [a, b, c] of lines) {
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            return board[a] as Player;
        }
    }
    return null;
};

/**
 * Componente de célula do jogo da velha.
 */
const Square: React.FC<{ value: string | null; onClick: () => void }> = ({ value, onClick }) => (
    <button
        className="square"
        onClick={onClick}
        disabled={!!value}
        style={{
            width: '100px',
            height: '100px',
            fontSize: '48px',
            cursor: 'pointer',
            border: '1px solid #ccc',
            background: '#f9f9f9'
        }}
    >
        {value}
    </button>
);

/**
 * Componente principal do Jogo da Velha (Tic-Tac-Toe).
 * Implementação simplificada para entrega rápida (CEO).
 */
const TicTacToeGame: React.FC = () => {
    const [board, setBoard] = useState<BoardState>(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState<boolean>(true);
    const [winner, setWinner] = useState<Player | null>(null);

    // Função que lida com o clique em uma célula
    const handleClick = useCallback((index: number) => {
        if (winner || board[index] !== null) {
            return; // Jogo finalizado ou célula já ocupada
        }

        const newBoard = [...board];
        newBoard[index] = isXNext ? 'X' : 'O';
        setBoard(newBoard);

        const gameWinner = calculateWinner(newBoard);
        if (gameWinner) {
            setWinner(gameWinner);
        } else if (newBoard.every(cell => cell !== null)) {
            // Empate
            setWinner(null); // O estado do vencedor é nulo, mas o jogo está cheio
        } else {
            setIsXNext(!isXNext);
        }
    }, [board, isXNext, winner]);

    // Determina o status do jogo
    const status = winner ? `Vencedor: ${winner === 'X' ? 'X' : 'O'}` :
                   board.every(cell => cell !== null) ? 'Empate!' :
                   `Vez de ${isXNext ? 'X' : 'O'}`;

    // Função para reiniciar o jogo
    const resetGame = useCallback(() => {
        setBoard(Array(9).fill(null));
        setIsXNext(true);
        setWinner(null);
    }, []);

    return (
        <div style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif', padding: '20px' }}>
            <h1>Jogo da Velha (Tic-Tac-Toe)</h1>
            <div style={{ marginBottom: '20px', fontWeight: 'bold' }}>
                Status: {status}
            </div>
            <div 
                style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(3, 1fr)', 
                    gap: '10px', 
                    maxWidth: '450px', 
                    margin: '0 auto' 
                }}
            >
                {board.map((value, i) => (
                    <Square 
                        key={i} 
                        value={value} 
                        onClick={() => handleClick(i)} 
                    />
                ))}
            </div>
            <button 
                onClick={resetGame}
                style={{ 
                    marginTop: '30px', 
                    padding: '10px 20px', 
                    fontSize: '16px', 
                    cursor: 'pointer',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px'
                }}
            >
                Reiniciar Jogo
            </button>
        </div>
    );
};

export default TicTacToeGame;