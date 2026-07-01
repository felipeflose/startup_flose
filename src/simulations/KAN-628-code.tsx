import React, { useState, useCallback, useEffect } from 'react';

// --- TYPES ---

/** Define the type of game interaction */
type GameType = 'multiplayer' | 'singleplayer' | 'none';

/** Define the structure of a single game card */
interface GameCard {
    id: string;
    gameId: string; // Used for matching (e.g., 'snake')
    name: string;
    type: GameType;
}

/** Define the structure of the full game state */
interface MemoryGameState {
    cards: GameCard[];
    firstSelection: { id: string; gameId: string } | null;
    secondSelection: { id: string; gameId: string } | null;
    matches: Set<string>; // Set of gameId that have been matched
    isProcessing: boolean; // If cards are flipped or game logic is running
    currentTurn: number;
}

// --- DATA DEFINITIONS ---

// Mapeamento de jogos disponíveis. A complexidade dos jogos reais é o débito técnico.
const GAME_DEFINITIONS: Record<string, { name: string; type: GameType }> = {
    snake: { name: 'Cobrinha', type: 'multiplayer' },
    checkers: { name: 'Dama', type: 'multiplayer' },
    tictactoe: { name: 'Velha', type: 'multiplayer' },
    pente: { name: 'Pente', type: 'multiplayer' },
    solitaire: { name: 'Solitaire', type: 'singleplayer' },
    jokenpo: { name: 'Pedra-Papel-Tesoura', type: 'multiplayer' },
};

// Cria o conjunto inicial de cartões (deve haver pares)
const generateInitialCards = (): GameCard[] => {
    const gameKeys = Object.keys(GAME_DEFINITIONS);
    const cardList: GameCard[] = [];
    
    // Adiciona cada jogo duas vezes para garantir os pares
    gameKeys.forEach(key => {
        const definition = GAME_DEFINITIONS[key];
        cardList.push({ id: `card-1-${key}`, gameId: key, name: definition.name, type: definition.type });
        cardList.push({ id: `card-2-${key}`, gameId: key, name: definition.name, type: definition.type });
    });
    
    // Embaralha o array de cartões
    return cardList.sort(() => Math.random() - 0.5);
};

// --- COMPONENTS PLACEHOLDERS (DÉBITO TÉCNICO) ---

/**
 * Componente Placeholder para jogos multiplayer.
 * A lógica real de jogo seria implementada aqui.
 */
const MultiplayerGameComponent: React.FC<{ gameId: string; turn: number }> = ({ gameId, turn }) => {
    const definition = GAME_DEFINITIONS[gameId];
    return (
        <div style={styles.gameArea}>
            <h3>{definition.name} (Multiplayer)</h3>
            <p>Turno Atual: {turn}</p>
            <p style={{ color: 'orange' }}>[DEBT: Implementar lógica completa de jogo multiplayer aqui]</p>
            <button onClick={() => alert('Simulando fim de rodada de jogo multiplayer.')}>Finalizar Rodada</button>
        </div>
    );
};

/**
 * Componente Placeholder para jogos singleplayer.
 * A lógica real de jogo seria implementada aqui.
 */
const SinglePlayerGameComponent: React.FC<{ gameId: string; turn: number }> = ({ gameId, turn }) => {
    const definition = GAME_DEFINITIONS[gameId];
    return (
        <div style={styles.gameArea}>
            <h3>{definition.name} (Singleplayer)</h3>
            <p>Turno de {definition.name}: {turn}</p>
            <p style={{ color: 'red' }}>[DEBT: Implementar lógica de jogo singleplayer e contagem de turnos aqui]</p>
            <button onClick={() => alert('Simulando fim de rodada de jogo singleplayer.')}>Finalizar Rodada</button>
        </div>
    );
};

// --- CARD COMPONENT ---

interface CardProps {
    card: GameCard;
    isFlipped: boolean;
    isSelected: boolean;
    onClick: (card: GameCard) => void;
}

const Card: React.FC<CardProps> = ({ card, isFlipped, isSelected, onClick }) => {
    const baseStyle = {
        width: '100px',
        height: '150px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '2px solid #333',
        background: isFlipped ? '#f0f0f0' : (isSelected ? '#ccf' : '#ddd'),
        transition: 'transform 0.3s, background 0.3s';
        fontSize: '14px';
        userSelect: 'none';
    };

    const handleClick = () => {
        if (!isProcessing && !isFlipped) {
            onClick(card);
        }
    };

    return (
        <div style={{ ...baseStyle, transform: isFlipped ? 'rotateY(0deg)' : 'rotateY(0deg)' }}>
            {isFlipped ? (
                <div>
                    <p style={{ margin: 0, fontSize: '18px', color: '#007bff' }}>{card.name}</p>
                    <p style={{ margin: '5px 0 0', fontSize: '12px', color: '#666' }}>ID: {card.gameId}</p>
                </div>
            ) : (
                <div style={{ fontSize: '20px', color: '#888' }}>?</div>
            )}
        </div>
    );
};

// --- MAIN GAME COMPONENT ---

const MemoryGame: React.FC = () => {
    const [gameState, setGameState] = useState<MemoryGameState>(() => ({
        cards: generateInitialCards(),
        firstSelection: null,
        secondSelection: null,
        matches: new Set<string>(),
        isProcessing: false,
        currentTurn: 1,
    }));
    
    // Lógica de manipulação do estado de seleção
    const handleCardClick = useCallback((card: GameCard) => {
        setGameState(prev => {
            if (prev.isProcessing) return prev; // Ignora cliques enquanto processando

            const newFirstSelection = prev.firstSelection || { id: card.id, gameId: card.gameId };
            
            if (prev.firstSelection && prev.secondSelection) {
                // Já fez uma jogada, deve esperar o resultado
                return prev;
            }
            
            if (prev.firstSelection && prev.firstSelection.id === card.id) {
                // Clicou no mesmo cartão
                return prev;
            }

            let newSecondSelection = prev.secondSelection;

            if (prev.firstSelection) {
                // É a segunda seleção
                newSecondSelection = { id: card.id, gameId: card.gameId };
                
                // Verifica o par
                const isMatch = prev.firstSelection.gameId === newSecondSelection.gameId;
                
                if (isMatch) {
                    // PARACHO: Inicia a fase de jogo
                    return {
                        ...prev,
                        secondSelection: newSecondSelection,
                        isProcessing: true, // Bloqueia o board enquanto o jogo é jogado
                        matches: new Set(prev.matches).add(newSecondSelection.gameId),
                    };
                } else {
                    // NÃO É PAR: Volta as cartas
                    return {
                        ...prev,
                        secondSelection: newSecondSelection,
                        isProcessing: true, // Mantém o processamento para o efeito de flip
                    };
                }
            } else {
                // É a primeira seleção
                return {
                    ...prev,
                    firstSelection: { id: card.id, gameId: card.gameId },
                    secondSelection: null,
                    isProcessing: true, // Bloqueia temporariamente para mostrar a primeira carta
                };
            }
        });
    }, []);

    // Efeito para processar o resultado da seleção (Match ou No Match)
    useEffect(() => {
        const { firstSelection, secondSelection, matches, cards } = gameState;

        if (!firstSelection || !secondSelection) return;

        const isMatch = firstSelection.gameId === secondSelection.gameId;

        if (isMatch) {
            // 1. PARACHO: Executa a lógica do jogo
            handleGameMatch(firstSelection.gameId, secondSelection.gameId);
        } else {
            // 2. NÃO É PAR: Espera e vira as cartas
            setTimeout(() => {
                setGameState(prev => ({
                    ...prev,
                    firstSelection: null,
                    secondSelection: null,
                    isProcessing: false,
                }));
            }, 1000);
        }
    }, [gameState.firstSelection, gameState.secondSelection]);

    // Lógica central para acionar o jogo
    const handleGameMatch = (gameId1: string, gameId2: string) => {
        setGameState(prev => ({
            ...prev,
            firstSelection: null,
            secondSelection: null,
            isProcessing: false, // Desbloqueia o board
            currentTurn: prev.currentTurn + 1,
        }));
        
        // Aqui o débito técnico é visível: em vez de apenas atualizar o estado, 
        // chamamos um componente de jogo que simula o fluxo.
        console.log(`[GAME START] Jogo ${gameId1} iniciado. Tipo: ${GAME_DEFINITIONS[gameId1].type}`);
    };

    // Determinar se um cartão está "matchado" (para desabilitá-lo)
    const isCardMatched = useCallback((cardId: string, gameId: string) => {
        return gameState.matches.has(gameId);
    }, [gameState.matches]);

    // Determinar se o estado está pronto para cliques
    const canClick = !gameState.isProcessing && !gameState.firstSelection && !gameState.secondSelection;

    // Renderização da área de jogo (Game Play)
    const renderGameArea = () => {
        // Encontra o primeiro par encontrado para simular o jogo ativo
        const activeGameId = gameState.matches.size > 0 ? Array.from(gameState.matches)[0] : null;

        if (!activeGameId) {
            return null;
        }

        const gameDefinition = GAME_DEFINITIONS[activeGameId];

        if (gameDefinition.type === 'multiplayer') {
            return <MultiplayerGameComponent key={activeGameId} gameId={activeGameId} turn={gameState.currentTurn} />;
        } else if (gameDefinition.type === 'singleplayer') {
            return <SinglePlayerGameComponent key={activeGameId} gameId={activeGameId} turn={gameState.currentTurn} />;
        }
        return null;
    };


    return (
        <div style={styles.container}>
            <h1>🎮 Memory Game: Os Jogos Clássicos 🏆</h1>
            <p>Turno: {gameState.currentTurn}</p>
            
            {/* Área de Jogabilidade do Jogo */}
            {renderGameArea()}

            <div style={styles.board}>
                {gameState.cards.map((card) => (
                    <React.Fragment key={card.id}>
                        <Card
                            card={card}
                            isFlipped={!!gameState.firstSelection?.id === card.id || !!gameState.secondSelection?.id === card.id}
                            isSelected={gameState.firstSelection?.id === card.id || gameState.secondSelection?.id === card.id}
                            isProcessing={gameState.isProcessing}
                            onClick={handleCardClick}
                        />
                    </React.Fragment>
                ))}
            </div>
            
            <p style={{ marginTop: '20px', color: '#666' }}>
                Dica: Encontre pares de jogos (ex: Cobrinha, Cobrinha) para jogar!
            </p>
        </div>
    );
};

// --- STYLES ---
const styles: { [key: string]: React.CSSProperties } = {
    container: {
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
        fontFamily: 'Arial, sans-serif',
    },
    board: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '15px',
        justifyContent: 'center',
        padding: '20px 0';
        minHeight: '300px',
    },
    gameArea: {
        padding: '20px',
        border: '3px solid #28a745',
        borderRadius: '8px',
        marginBottom: '30px',
        backgroundColor: '#e9f7ec',
        textAlign: 'center',
        maxWidth: '600px',
    }
};

export default MemoryGame;