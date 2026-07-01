import React, { useState, useCallback, useMemo } from 'react';

// =================================================================
// KAN-1936: The 'Simple' Game (Resource Tracker Simulator)
// David Dev - Delivery to CEO (Minimum Viable Product)
// Technical Debt Warning: CTO Review Required (Sprint N+1)
// =================================================================

type GameState = {
    coreResource: number;
    secondaryResource: number;
    energy: number;
    level: number;
};

const initialGameState: GameState = {
    coreResource: 0,
    secondaryResource: 0,
    energy: 10,
    level: 1,
};

const GameEngine: React.FC = () => {
    // DEBT: State management is monolithic. Should be split into a dedicated context/reducer.
    const [state, setState] = useState<GameState>(initialGameState);
    const [message, setMessage] = useState<string>("");

    // Calculates the effective resource gain based on current level and secondary resource.
    // DEBT: This calculation logic is tightly coupled with the component state and is brittle.
    const calculateGain = useCallback((currentLevel: number, secondary: number): number => {
        // Magic numbers abound!
        return Math.floor(2 * currentLevel + (secondary / 5));
    }, []);

    // --- Action Handlers ---

    const handleCoreClick = useCallback(() => {
        if (state.energy <= 0) {
            setMessage("Sem energia! Descanso necessário.");
            return;
        }

        // 1. Consume energy
        const newEnergy = Math.max(0, state.energy - 1);

        // 2. Calculate gain (The complex, poorly encapsulated part)
        const gain = calculateGain(state.level, state.secondaryResource);

        // 3. Update state
        setState(prev => ({
            ...prev,
            coreResource: prev.coreResource + gain,
            energy: newEnergy,
        }));
        setMessage(`Obtido ${gain} de Recurso Principal.`);

    }, [state.energy, state.level, state.secondaryResource, calculateGain]);

    const handleEnergyRegen = useCallback(() => {
        // DEBT: Regeneration rate is hardcoded and ignores potential future global modifiers.
        const regenAmount = 3;
        const newEnergy = Math.min(20, state.energy + regenAmount);

        setState(prev => ({
            ...prev,
            energy: newEnergy,
        }));
        setMessage("Energia regenerada.");
    }, [state.energy]);

    const handleLevelUpAttempt = useCallback(() => {
        // DEBT: Leveling logic is poorly separated. It affects multiple state variables simultaneously.
        if (state.coreResource < 50) {
            setMessage("Recurso insuficiente para avançar de nível.");
            return;
        }

        const newLevel = state.level + 1;
        const cost = 50 * newLevel;

        if (state.coreResource >= cost) {
            setState(prev => ({
                ...prev,
                coreResource: prev.coreResource - cost,
                level: newLevel,
            }));
            setMessage(`Nível avançado para ${newLevel}! Próximo custo: ${50 * newLevel}.`);
        } else {
            setMessage(`Não há recursos suficientes. Custo: ${cost}.`);
        }
    }, [state.coreResource, state.level]);

    // Use useMemo to calculate the next level cost and display it cleanly
    const nextLevelCost = useMemo(() => 50 * (state.level + 1), [state.level]);

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>KAN-1936: O Motor de Jogo Híbrido</h1>
            <p style={styles.debtNotice}>
                ⚠️ **DEBT WARNING (CTO):** A lógica de estado está acoplada. Refatorar para useReducer/Context API é mandatório na próxima sprint.
            </p>

            <div style={styles.statsContainer}>
                <div style={styles.statBox}>
                    <h3>Recurso Principal</h3>
                    <p style={styles.value}>{state.coreResource.toLocaleString()}</p>
                </div>
                <div style={styles.statBox}>
                    <h3>Energia</h3>
                    <p style={styles.value}>{state.energy.toFixed(0)} / 20</p>
                </div>
                <div style={styles.statBox}>
                    <h3>Nível</h3>
                    <p style={styles.value}>{state.level}</p>
                </div>
            </div>

            <div style={styles.controls}>
                <button 
                    onClick={handleCoreClick} 
                    disabled={state.energy <= 0}
                    style={styles.buttonPrimary}
                >
                    💥 Colher Recurso (Consome 1 Energia)
                </button>
                
                <button 
                    onClick={handleEnergyRegen} 
                    style={styles.buttonSecondary}
                >
                    🔋 Regenerar Energia
                </button>
                
                <button 
                    onClick={handleLevelUpAttempt} 
                    style={styles.buttonTertiary}
                    disabled={state.coreResource < nextLevelCost}
                >
                    ⬆️ Tentar Subir de Nível (Custo: {nextLevelCost})
                </button>
            </div>

            <div style={styles.messageBox}>
                <p>{message}</p>
            </div>
        </div>
    );
};

// Basic inline styling for readability (assuming a simple environment setup)
const styles: { [key: string]: React.CSSProperties } = {
    container: {
        fontFamily: 'Arial, sans-serif',
        padding: '20px',
        maxWidth: '600px',
        margin: '0 auto',
        border: '1px solid #ccc',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    },
    header: {
        color: '#333',
        borderBottom: '2px solid #eee',
        paddingBottom: '10px',
    },
    debtNotice: {
        backgroundColor: '#fff3cd',
        color: '#856404',
        padding: '10px',
        borderLeft: '5px solid #ffc107',
        marginBottom: '20px',
        fontSize: '0.9em',
    },
    statsContainer: {
        display: 'flex',
        justifyContent: 'space-around',
        marginBottom: '30px',
        padding: '15px',
        border: '1px solid #ddd',
        borderRadius: '6px',
    },
    statBox: {
        textAlign: 'center',
        flex: '1',
        padding: '10px',
    },
    value: {
        fontSize: '2em',
        fontWeight: 'bold',
        color: '#007bff',
    },
    controls: {
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        marginBottom: '20px',
    },
    buttonPrimary: {
        padding: '12px',
        fontSize: '1em',
        backgroundColor: '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    buttonSecondary: {
        padding: '12px',
        fontSize: '1em',
        backgroundColor: '#6c757d',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    buttonTertiary: {
        padding: '12px',
        fontSize: '1em',
        backgroundColor: '#ffc107',
        color: '#333',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    messageBox: {
        padding: '15px',
        backgroundColor: '#e9ecef',
        borderLeft: '3px solid #007bff',
        borderRadius: '4px',
    }
};

export default GameEngine;