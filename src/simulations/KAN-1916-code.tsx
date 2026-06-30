import React, { useState, useCallback, useMemo } from 'react';

/**
 * Define o tipo para o estado do tabuleiro
 * Um tabuleiro 3x3 é representado por um array de 9 posições.
 */
type BoardState = (string | null)[];

/**
 * Define os possíveis valores do jogo
 */
type Player = 'X' | 'O';

/**
 * Determina o vencedor do jogo com base no tabuleiro atual.
 * @param board O estado atual do tabuleiro.
 * @returns O jogador vencedor ('X', 'O'), ou null se ninguém venceu.
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
 * Componente de célula do tabuleiro
 */
const Square: React.FC<{ value: string | null; onClick: () => void }> = ({ value, onClick }) => (
    <button
        className={`square ${value ? `winner-${value.toLowerCase()}` : ''}`}
        onClick={onClick}
        disabled={!!value}
        aria-label={`Célula com valor ${value || 'vazio'}`}
    >
        {value}
    </button>
);

/**
 * Componente principal do Jogo da Velha
 */
const TicTacToeGame: React.FC = () => {
    const [board, setBoard] = useState<BoardState>(Array(9).fill(null));
    const [currentPlayer, setCurrentPlayer] = useState<Player>('X');
    const [winner, setWinner] = useState<Player | null>(null);

    /**
     * Reseta o estado do jogo
     */
    const resetGame = useCallback(() => {
        setBoard(Array(9).fill(null));
        setCurrentPlayer('X');
        setWinner(null);
    }, []);

    /**
     * Lógica principal ao clicar em uma célula.
     * Nota: Esta implementação é funcional e rápida (CEO), mas o tratamento de estado
     * e a lógica de ciclo de vida poderiam ser encapsulados em um Reducer/Context
     * para melhor separação de responsabilidades (CTO Debt).
     */
    const handleSquareClick = useCallback((index: number) => {
        if (board[index] || winner) {
            return; // Ignora cliques em células preenchidas ou jogo finalizado
        }

        // 1. Criar novo estado do tabuleiro
        const newBoard = [...board];
        newBoard[index] = currentPlayer;
        
        // 2. Atualizar estado
        setBoard(newBoard);

        // 3. Verificar vitória
        const newWinner = calculateWinner(newBoard);
        
        if (newWinner) {
            setWinner(newWinner);
        } else if (!newBoard.includes(null)) {
            // 4. Verificar empate (Tabuleiro cheio e sem vencedor)
            setWinner(null); // Não define um "empate" explicitamente no estado, mas o jogo para
        } else {
            // 5. Trocar jogador
            setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
        }
    }, [board, currentPlayer, winner]);

    // Determinar a mensagem de status
    const status = useMemo(() => {
        if (winner) {
            return `Vencedor: ${winner}!`;
        } else if (board.every(cell => cell !== null)) {
            return "Empate!";
        } else {
            return `Vez de ${currentPlayer === 'X' ? 'X' : 'O'}`;
        }
    }, [winner, board, currentPlayer]);

    return (
        <div style={styles.container}>
            <h1>Jogo da Velha (Tic-Tac-Toe)</h1>
            <div style={styles.status}>{status}</div>
            <div style={styles.board}>
                {Array(9).fill(null).map((_, i) => (
                    <Square
                        key={i}
                        value={board[i]}
                        onClick={() => handleSquareClick(i)}
                    />
                ))}
            </div>
            <button onClick={resetGame} style={styles.button}>
                Reiniciar Jogo
            </button>
        </div>
    );
};

export default TicTacToeGame;

// Estilos simples para garantir a funcionalidade e visualização
const styles: { [key: string]: React.CSSProperties } = {
    container: {
        fontFamily: 'Arial, sans-serif',
        textAlign: 'center',
        padding: '20px',
        maxWidth: '400px',
        margin: '0 auto',
        border: '1px solid #ccc',
        borderRadius: '8px',
    },
    status: {
        fontSize: '1.5em',
        marginBottom: '20px',
        fontWeight: 'bold',
    },
    board: {
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gridTemplateRows: 'repeat(3, 1fr)',
        gap: '10px',
        marginBottom: '20px',
    },
    button: {
        padding: '10px 20px',
        fontSize: '1em',
        cursor: 'pointer',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
    },
    square: {
        backgroundColor: '#f0f0f0',
        border: '1px solid #aaa',
        fontSize: '3em',
        fontWeight: 'bold',
        cursor: 'pointer',
        padding: '0',
        margin: 0,
        transition: 'background-color 0.2s';
        appearance: 'none', /* Remove estilos padrão de botão */
    }
};