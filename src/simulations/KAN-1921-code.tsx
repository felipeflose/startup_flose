import React, { useState, useEffect, useCallback } from 'react';

// --- Types and Constants ---

type EntityType = 'player' | 'vehicle' | 'npc';

interface Position {
    x: number;
    y: number;
}

interface Entity {
    id: string;
    type: EntityType;
    name: string;
    position: Position;
    health: number;
    isControlled: boolean;
}

interface GameState {
    entities: Entity[];
    player: Entity;
    isDriving: boolean;
    mapScale: number; // Used for movement speed/world size
    time: number; // Simulates game time
}

const INITIAL_STATE: GameState = {
    entities: [
        { id: 'car1', type: 'vehicle', name: 'Police Cruiser', position: { x: 50, y: 150 }, health: 100, isControlled: false },
        { id: 'npc1', type: 'npc', name: 'Pedestrian', position: { x: 20, y: 200 }, health: 100, isControlled: false },
    ],
    player: { id: 'player', type: 'player', name: 'You', position: { x: 10, y: 10 }, health: 100, isControlled: true },
    isDriving: false,
    mapScale: 10,
    time: 0,
};

// --- Component Implementation ---

const GameSimulation: React.FC = () => {
    const [gameState, setGameState] = useState<GameState>(INITIAL_STATE);
    const [message, setMessage] = useState<string>("Bem-vindo à Los Santos. O crime espera.");

    // --- Core Game Logic (The Technical Debt Area) ---
    // TODO: CRITICAL DEBT: Physics, collision detection, and AI pathfinding are stubbed out.
    // Refactor this entire block into a dedicated 'PhysicsEngine' service module.
    const updateGamePhysics = useCallback((currentState: GameState): GameState => {
        let newEntities = [...currentState.entities];
        let newPlayer = { ...currentState.player };
        let newGameState = { ...currentState, entities: [...newEntities] };

        // 1. Player Movement (Simplified Input Handling)
        let newX = newPlayer.position.x;
        let newY = newPlayer.position.y;

        // Simulate movement based on simple directional input (e.g., key presses handled by useEffect)
        // For the prototype, we just simulate a slight drift.
        if (currentState.isDriving) {
            newX += 0.5;
            newY -= 0.2;
        } else {
            // Simple drift simulation if not in vehicle
            newX += 0.1;
            newY += 0.05;
        }

        newPlayer = { ...newPlayer, position: { x: newX, y: newY } };
        newGameState = { ...newGameState, player: newPlayer };

        // 2. Entity Updates (Very basic AI simulation)
        newEntities = newEntities.map(entity => {
            // TODO: Implement proper pathfinding and threat assessment here.
            if (entity.type === 'npc' && Math.random() < 0.01) {
                return { ...entity, position: { x: entity.position.x + 1, y: entity.position.y } };
            }
            return entity;
        });

        // 3. Collision Check (Placeholder)
        // TODO: Implement AABB or SAT collision checks.
        // If collision detected, adjust health/position.

        return { ...newGameState, entities: newEntities };
    }, []);

    // --- Game Loop Effect (The Engine) ---
    useEffect(() => {
        // Using setInterval for simplified game loop simulation (less performant than requestAnimationFrame, but faster for prototype)
        const intervalId = setInterval(() => {
            setGameState(currentState => {
                const nextState = updateGamePhysics(currentState);
                return {
                    ...nextState,
                    time: nextState.time + 1,
                };
            });
        }, 50); // ~20 FPS simulation

        return () => clearInterval(intervalId);
    }, [updateGamePhysics]);

    // --- Input Handling (The Interface) ---
    const handleKeyDown = useCallback((e: KeyboardEvent) => {
        let newGameState = { ...gameState };
        let newPlayer = { ...gameState.player };

        // Simplified Input Mapping
        switch (e.key) {
            case 'ArrowUp':
            case 'w':
                newPlayer.position = { x: newPlayer.position.x, y: Math.max(0, newPlayer.position.y - 1) };
                setMessage("Movendo para o Norte.");
                break;
            case 'ArrowDown':
            case 's':
                newPlayer.position = { x: newPlayer.position.x, y: Math.min(100, newPlayer.position.y + 1) };
                setMessage("Movendo para o Sul.");
                break;
            case 'ArrowLeft':
            case 'a':
                newPlayer.position = { x: Math.max(0, newPlayer.position.x - 1), y: newPlayer.position.y };
                setMessage("Movendo para o Oeste.");
                break;
            case 'ArrowRight':
            case 'd':
                newPlayer.position = { x: Math.min(200, newPlayer.position.x + 1), y: newPlayer.position.y };
                setMessage("Movendo para o Leste.");
                break;
            case 'e':
                // Simulated interaction (e.g., enter car)
                if (!gameState.isDriving) {
                    setMessage("Interagindo com o ambiente...");
                    // Logic to detect nearby vehicle and change state
                    setGameState(prev => ({ ...prev, isDriving: true }));
                } else {
                    setMessage("Você já está dirigindo. Pressione ESC para sair.");
                }
                break;
            case 'Escape':
                // Exit vehicle
                setGameState(prev => ({ ...prev, isDriving: false }));
                setMessage("Saiu do veículo. Voltando a caminhar.");
                break;
            default:
                setMessage("");
        }

        // Force state update after key press to reflect movement immediately
        setGameState(prev => ({ ...prev, player: newPlayer }));

    }, [gameState]);

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [handleKeyDown]);

    // --- Rendering Helpers ---

    const renderEntity = (entity: Entity) => {
        const style = {
            left: `${entity.position.x}%`,
            top: `${entity.position.y}%`,
            transform: `translate(-50%, -50%)`,
            opacity: entity.type === 'player' ? 1 : 0.8,
        };

        let icon = '';
        if (entity.type === 'player') icon = '👤';
        else if (entity.type === 'vehicle') icon = '🚗';
        else if (entity.type === 'npc') icon = '🚶';

        return (
            <div key={entity.id} style={style} className="entity-marker">
                {icon} {entity.name} ({entity.health}%)
            </div>
        );
    };

    return (
        <div className="game-container">
            <div className="game-map-area">
                <div style={{
                    position: 'absolute',
                    left: `${gameState.player.position.x}%`,
                    top: `${gameState.player.position.y}%`,
                    transform: `translate(-50%, -50%)`,
                    transition: 'all 0.1s linear',
                    width: '20px',
                    height: '20px',
                    backgroundColor: 'rgba(0, 255, 0, 0.7)',
                    borderRadius: '50%',
                    boxShadow: '0 0 10px green',
                }}></div>
                {gameState.entities.map(renderEntity)}
            </div>

            <div className="info-panel">
                <div className="status-box">
                    <h2>Status do Jogo</h2>
                    <p><strong>Tempo:</strong> {Math.floor(gameState.time / 60)} Min</p>
                    <p><strong>Modo:</strong> {gameState.isDriving ? 'DIRIGINDO' : 'A PEDESTRE'}</p>
                    <p><strong>Mensagem:</strong> {message}</p>
                </div>
                <div className="controls-box">
                    <h3>Controles (Tecla)</h3>
                    <p>Movimento: WASD / Setas</p>
                    <p>Interagir/Entrar: E</p>
                    <p>Sair do Carro: ESC</p>
                    <p class="debt-warning">
                        ⚠️ DÉBITO TÉCNICO (CTO): Física e IA complexa devem ser refatoradas.
                    </p>
                </div>
            </div>
        </div>
    );
};

// --- Global Styles (Simplified CSS for Prototype) ---
// Note: In a real project, this would be a CSS module or styled-components.
const StyleInjector = () => (
    <style>{`
        .game-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            font-family: 'Arial', sans-serif;
            background-color: #222;
            color: #eee;
        }
        .game-map-area {
            flex-grow: 1;
            background-color: #444;
            position: relative;
            overflow: hidden;
            /* Simulates the open world map area */
            border-bottom: 1px solid #666;
        }
        .entity-marker {
            position: absolute;
            cursor: pointer;
            font-size: 1.2em;
            padding: 5px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 5px;
            white-space: nowrap;
            transform: translate(-50%, -50%);
            transition: all 0.3s ease-out;
        }
        .info-panel {
            display: flex;
            padding: 20px;
            background-color: #1a1a1a;
            border-top: 3px solid #333;
            gap: 30px;
        }
        .status-box, .controls-box {
            flex: 1;
            padding: 15px;
            background-color: #2c2c2c;
            border-radius: 8px;
        }
        .debt-warning {
            color: #ff8800;
            font-weight: bold;
            margin-top: 10px;
        }
    `}</style>
);

// --- Export the main application component ---
const App: React.FC = () => (
    <>
        <StyleInjector />
        <GameSimulation />
    </>
);

export default App;