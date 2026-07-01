import React, { useState, useEffect, useCallback, useRef } from 'react';

// --- Constantes do Jogo ---
const GRID_SIZE = 20; // Tamanho do grid (20x20)
const INITIAL_SPEED = 150; // Velocidade inicial (ms)

// Tipo para coordenadas
type Position = { x: number; y: number };

// Tipo para direções
type Direction = 'Up' | 'Down' | 'Left' | 'Right';

// --- Componente Principal do Jogo ---
const SnakeGame: React.FC = () => {
    const [snake, setSnake] = useState<Position[]>([{ x: 10, y: 10 }, { x: 10, y: 11 }]);
    const [food, setFood] = useState<Position>({ x: 5, y: 5 });
    const [direction, setDirection] = useState<Direction>('Up');
    const [isGameOver, setIsGameOver] = useState(false);
    const [score, setScore] = useState(0);
    const intervalRef = useRef<number | null>(null);

    // Função para gerar nova comida em uma posição aleatória e não ocupada
    const generateFood = useCallback((currentSnake: Position[]): Position => {
        let newFood: Position;
        do {
            newFood = {
                x: Math.floor(Math.random() * GRID_SIZE),
                y: Math.floor(Math.random() * GRID_SIZE),
            };
        } while (currentSnake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
        return newFood;
    }, []);

    // Lógica para mover a cobra
    const moveSnake = useCallback(() => {
        if (isGameOver) return;

        setSnake(prevSnake => {
            const head = prevSnake[0];
            let newHead: Position;

            // 1. Calcular nova cabeça baseada na direção
            switch (direction) {
                case 'Up':
                    newHead = { x: head.x, y: head.y - 1 };
                    break;
                case 'Down':
                    newHead = { x: head.x, y: head.y + 1 };
                    break;
                case 'Left':
                    newHead = { x: head.x - 1, y: head.y };
                    break;
                case 'Right':
                    newHead = { x: head.x + 1, y: head.y };
                    break;
            }

            // 2. Checar Colisões (Muros)
            if (newHead.x < 0 || newHead.x >= GRID_SIZE || newHead.y < 0 || newHead.y >= GRID_SIZE) {
                setIsGameOver(true);
                return prevSnake;
            }

            // 3. Checar Colisões (Corpo)
            if (prevSnake.some((segment, index) => index !== 0 && segment.x === newHead.x && segment.y === newHead.y)) {
                setIsGameOver(true);
                return prevSnake;
            }

            // 4. Criar novo corpo
            const newSnake = [newHead, ...prevSnake];
            let ateFood = false;
            let newScore = score;

            // 5. Checar se comeu a comida
            if (newHead.x === food.x && newHead.y === food.y) {
                ateFood = true;
                setFood(generateFood(newSnake)); // Gera nova comida
                newScore += 10;
                setScore(newScore);
            }

            // 6. Atualizar o corpo
            let nextSnake = ateFood ? newSnake : newSnake.slice(0, newSnake.length - 1);

            // Atualiza o estado da cobra
            setSnake(nextSnake);
            return nextSnake;
        });
    }, [direction, food, score, isGameOver, generateFood]);

    // Efeito para o Loop do Jogo (Game Loop)
    useEffect(() => {
        if (isGameOver) return;

        // Limpa o intervalo anterior e inicia um novo
        if (intervalRef.current !== null) {
            clearInterval(intervalRef.current);
        }

        // A velocidade pode ser ajustada aqui para aumentar a dificuldade
        const gameInterval = setInterval(moveSnake, INITIAL_SPEED);
        intervalRef.current = gameInterval;

        // Cleanup function: Limpa o intervalo quando o componente for desmontado ou isGameOver mudar
        return () => {
            if (intervalRef.current !== null) {
                clearInterval(intervalRef.current);
            }
        };
    }, [moveSnake, isGameOver]);

    // Efeito para o Controle de Teclado (Input Handling)
    useEffect(() => {
        const handleKeydown = (e: KeyboardEvent) => {
            const currentDirection: Direction = direction;
            let newDirection: Direction;

            // Previne que o jogador vire 180 graus instantaneamente
            if (e.key === 'ArrowUp' && currentDirection !== 'Down') {
                newDirection = 'Up';
            } else if (e.key === 'ArrowDown' && currentDirection !== 'Up') {
                newDirection = 'Down';
            } else if (e.key === 'ArrowLeft' && currentDirection !== 'Right') {
                newDirection = 'Left';
            } else if (e.key === 'ArrowRight' && currentDirection !== 'Left') {
                newDirection = 'Right';
            } else {
                return; // Ignora input inválido
            }

            // Atualiza a direção apenas se for válida e diferente da atual
            setDirection(newDirection);
        };

        window.addEventListener('keydown', handleKeydown);

        return () => {
            window.removeEventListener('keydown', handleKeydown);
        };
    }, [direction]);

    // Função para reiniciar o jogo
    const restartGame = () => {
        setSnake([{ x: 10, y: 10 }, { x: 10, y: 11 }]);
        setFood(generateFood(Array(GRID_SIZE).fill({ x: 0, y: 0 })));
        setDirection('Up');
        setIsGameOver(false);
        setScore(0);
    };

    // --- Renderização ---

    const renderGrid = () => {
        const cells: React.ReactNode[] = [];
        for (let y = 0; y < GRID_SIZE; y++) {
            for (let x = 0; x < GRID_SIZE; x++) {
                let content: React.ReactNode = null;
                let className = 'cell';

                if (x === food.x && y === food.y) {
                    content = <div className="food">🍎</div>;
                    className += ' food-cell';
                } else if (snake.some(segment => segment.x === x && segment.y === y)) {
                    // Diferencia a cabeça do corpo
                    const isHead = snake[0].x === x && snake[0].y === y;
                    className += isHead ? ' head-cell' : ' body-cell';
                    content = null;
                }

                cells.push(
                    <div key={`${x}-${y}`} className={className}>
                        {content}
                    </div>
                );
            }
        }
        return cells;
    };

    return (
        <div className="game-container">
            <h1>🐍 Cobrinha Clássica (KAN-1927)</h1>
            <div className="score-board">
                Score: {score} | 
                Status: {isGameOver ? 'Game Over!' : 'Jogando...'}
            </div>

            <div 
                className="game-grid" 
                style={{ 
                    gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)`, 
                    gridTemplateRows: `repeat(${GRID_SIZE}, 1fr)` 
                }}
            >
                {renderGrid()}
            </div>

            <button 
                className="restart-button" 
                onClick={restartGame}
                disabled={!isGameOver && intervalRef.current !== null}
            >
                {isGameOver ? 'Jogar Novamente' : 'Reiniciar Jogo'}
            </button>

            <div className="controls-info">
                Use as setas direcionais (↑ ↓ ← →) para jogar.
            </div>
        </div>
    );
};

export default SnakeGame;