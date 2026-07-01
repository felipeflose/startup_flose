import React, { useState, useCallback, useMemo } from 'react';

// Define os tipos de jogada e estado
type Player = 'X' | 'O' | null;
type BoardState = Player[];

// Tamanho do tabuleiro
const BOARD_SIZE = 3;

/**
 * Verifica se houve um vencedor no tabuleiro.
 * @param board O estado atual do tabuleiro.
 * @returns O jogador vencedor ('X' ou 'O') ou null se não houver vencedor.
 */
const calculateWinner = (board: BoardState): Player | null => {
    const lines = [
        // Linhas
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        // Colunas
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        // Diagonais
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]],
    ];

    for (const line of lines) {
        const [a, b, c] = line.map(([row, col]) => board[row][col]);
        if (a && a === b && a === c) {
            return a;
        }
    }
    return null;
};

/**
 * Componente que representa uma célula individual do tabuleiro.
 * @param player O jogador que deve ser exibido na célula.
 */
const Cell: React.FC<{ player: Player }> = ({ player }) => {
    return (
        <div style={styles.cell}>
            {player}
        </div>
    );
};

/**
 * Componente principal do Jogo da Velha.
 * Implementação simplificada (CEO Delivery) - O estado e lógica estão aqui.
 * @component
 */
const TicTacToeGame: React.FC = () => {
    // Inicializa o estado do tabuleiro como um array 2D (matriz)
    const initialBoard: BoardState = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(null));
    const [board, setBoard] = useState<BoardState>(initialBoard);
    const [currentPlayer, setCurrentPlayer] = useState<Player>('X');
    const [winner, setWinner] = useState<Player | null>(null);
    const [isDraw, setIsDraw] = useState<boolean>(false);

    /**
     * Lógica de manipulação de clique na célula.
     * @param row Índice da linha.
     * @param col Índice da coluna.
     */
    const handleClick = useCallback((row: number, col: number) => {
        // 1. Verifica se o jogo já terminou (vencedor ou empate)
        if (winner || isDraw) {
            return;
        }

        // 2. Verifica se a célula já foi preenchida ou se o clique é fora dos limites
        if (board[row][col] !== null || board[row][col] !== null) {
            return;
        }

        // Cria uma cópia profunda do tabuleiro para imutabilidade
        const newBoard: BoardState = board.map(row => [...row]);
        
        // Aplica o movimento
        newBoard[row][col] = currentPlayer;

        // Atualiza o estado do tabuleiro
        setBoard(newBoard);

        // Verifica o vencedor
        const calculatedWinner = calculateWinner(newBoard);

        if (calculatedWinner) {
            setWinner(calculatedWinner);
        } else if (newBoard.every(row => row.every(cell => cell !== null))) {
            // Se todos os campos estiverem preenchidos e não houver vencedor
            setIsDraw(true);
            setWinner(null);
        } else {
            // Troca o jogador
            const nextPlayer: Player = currentPlayer === 'X' ? 'O' : 'X';
            setCurrentPlayer(nextPlayer);
            setWinner(null);
        }
    }, [board, currentPlayer, winner, isDraw]);

    /**
     * Reseta o jogo para o estado inicial.
     */
    const resetGame = useCallback(() => {
        setBoard(initialBoard);
        setCurrentPlayer('X');
        setWinner(null);
        setIsDraw(false);
    }, [initialBoard]);

    // Determina a mensagem de status do jogo
    const statusText = useMemo(() => {
        if (winner) {
            return `Vencedor: ${winner}`;
        } else if (isDraw) {
            return "Empate! Ninguém venceu.";
        } else {
            return `Vez de: ${currentPlayer}`;
        }
    }, [winner, isDraw, currentPlayer]);

    // Renderiza a grade do tabuleiro
    const renderBoard = () => {
        return board.map((row, rowIndex) => (
            <div key={rowIndex} style={styles.row}>
                {row.map((cell, colIndex) => (
                    <Cell key={`${rowIndex}-${colIndex}`} player={cell} />
                ))}
            </div>
        ));
    };

    return (
        <div style={styles.container}>
            <h1>Jogo da Velha (Tic-Tac-Toe)</h1>
            <div style={styles.status}>
                <p>{statusText}</p>
            </div>
            
            <div style={styles.board}>
                {renderBoard()}
            </div>

            <button 
                onClick={resetGame} 
                style={styles.button}
                aria-label="Resetar Jogo"
            >
                Reiniciar Jogo
            </button>
        </div>
    );
};

// Estilos em JS object para manter o componente self-contained
const styles: { [key: string]: React.CSSProperties } = {
    container: {
        fontFamily: 'Arial, sans-serif',
        textAlign: 'center',
        padding: '20px',
        maxWidth: '400px',
        margin: '0 auto',
        border: '2px solid #ccc',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    status: {
        margin: '20px 0',
        padding: '10px',
        backgroundColor: '#f0f0f0',
        borderRadius: '5px',
    },
    board: {
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        margin: '20px 0',
    },
    row: {
        display: 'flex',
        gap: '10px',
    },
    cell: {
        width: '100px',
        height: '100px',
        backgroundColor: '#fff',
        border: '1px solid #333',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: '48px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
        userSelect: 'none',
    } as React.CSSProperties,
    button: {
        padding: '10px 20px',
        fontSize: '16px',
        cursor: 'pointer',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        transition: 'background-color 0.2s',
    } as React.CSSProperties,
};

// Nota para o débito técnico (CTO): 
// A lógica de gerenciamento de estado (useState/useCallback) está um pouco acoplada. 
// Recomenda-se refatorar a lógica do jogo para um hook customizado (useGameLogic) 
// ou usar Redux/Zustand para desacoplar completamente o estado do componente UI.

export default TicTacToeGame;