import React, { useState, useEffect, useCallback } from 'react';

// Define types for clarity
type Position = { x: number; y: number };
type Direction = 'up' | 'down' | 'left' | 'right';

// --- Componentes Simples ---

/**
 * Simula o personagem principal.
 * Responsável por exibir a posição e gerenciar o estado básico do jogador.
 */
const Character: React.FC<{ position: Position }> = ({ position }) => {
  return (
    <div style={{
      position: 'absolute',
      left: `${position.x}px`,
      top: `${position.y}px`,
      transform: 'translate(-50%, -50%)',
      width: '30px',
      height: '30px',
      backgroundColor: 'blue',
      borderRadius: '50%',
      border: '2px solid #000',
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.5)',
      zIndex: 10,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 'bold',
    }}>
      YOU
    </div>
  );
};

/**
 * Simula o mapa e o ambiente do jogo.
 * Contém pontos de interesse e limites.
 */
const Map: React.FC<{ playerPosition: Position }> = ({ playerPosition }) => {
  const containerStyle: React.CSSProperties = {
    width: '800px',
    height: '600px',
    backgroundColor: '#8bc34d', // Gramado/Cidade
    border: '5px solid #333',
    position: 'relative',
    overflow: 'hidden',
    cursor: 'crosshair',
  };

  const InterestPoint: React.FC<{ position: Position; name: string; description: string }> = ({ position, name, description }) => (
    <div
      style={{
        position: 'absolute',
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translate(-50%, -50%)',
        width: '15px',
        height: '15px',
        backgroundColor: '#e91e63', // Cor de interesse
        borderRadius: '50%',
        cursor: 'pointer',
        border: '2px solid #c2185b',
        zIndex: 5,
        transition: 'transform 0.2s',
      }}
      title={description}
    >
      <span style={{ fontSize: '10px', lineHeight: '1' }}>{name[0].toUpperCase()}</span>
    </div>
  );

  return (
    <div style={containerStyle}>
      <InterestPoint position={{ x: 200, y: 150 }} name="Rádio" description="Ponto de rádio frequência." />
      <InterestPoint position={{ x: 650, y: 400 }} name="Mundo" description="Área de atividade suspeita." />
      <InterestPoint position={{ x: 50, y: 500 }} name="Garagem" description="Local para veículos." />
    </div>
  );
};

/**
 * Componente principal do jogo.
 * Gerencia o estado e a lógica de movimento simplificada.
 */
const GTAPrototype: React.FC = () => {
  const [position, setPosition] = useState<Position>({ x: 100, y: 100 });
  const [money, setMoney] = useState<number>(1500);
  const [status, setStatus] = useState<string>("Bem-vindo à Los Santos. Use WASD ou as setas para se mover.");

  // Constantes do mapa
  const MAP_WIDTH = 800;
  const MAP_HEIGHT = 600;
  const MOVEMENT_SPEED = 10;

  // Lógica de movimento
  const handleMove = useCallback((direction: Direction) => {
    setPosition(prevPos => {
      let newX = prevPos.x;
      let newY = prevPos.y;

      switch (direction) {
        case 'up':
          newY -= MOVEMENT_SPEED;
          break;
        case 'down':
          newY += MOVEMENT_SPEED;
          break;
        case 'left':
          newX -= MOVEMENT_SPEED;
          break;
        case 'right':
          newX += MOVEMENT_SPEED;
          break;
      }

      // Limitar movimento dentro dos limites do mapa
      newX = Math.max(0, Math.min(MAP_WIDTH, newX));
      newY = Math.max(0, Math.min(MAP_HEIGHT, newY));

      return { x: newX, y: newY };
    });
  }, []);

  // Efeito para lidar com o teclado (Melhor UX para jogos)
  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      let direction: Direction | null = null;
      switch (e.key.toLowerCase()) {
        case 'w':
        case 'arrowup':
          direction = 'up';
          break;
        case 's':
        case 'arrowdown':
          direction = 'down';
          break;
        case 'a':
        case 'arrowleft':
          direction = 'left';
          break;
        case 'd':
        case 'arrowright':
          direction = 'right';
          break;
        default:
          return;
      }
      e.preventDefault();
      handleMove(direction);
    };

    window.addEventListener('keydown', handleKeydown);
    return () => {
      window.removeEventListener('keydown', handleKeydown);
    };
  }, [handleMove]);

  // Lógica de interação (Exemplo: Crime/Missão)
  const handleInteract = () => {
    if (money < 50) {
      setStatus("Você não tem dinheiro suficiente para iniciar esta missão.");
      return;
    }
    
    // Lógica simplificada de "crime"
    const success = Math.random() > 0.3;
    
    if (success) {
      const reward = Math.floor(Math.random() * 1000) + 500;
      setMoney(prev => prev + reward);
      setStatus(`SUCESSO! Você completou a missão e ganhou $${reward}.`);
    } else {
      const fine = 100;
      setMoney(prev => Math.max(0, prev - fine));
      setStatus(`FALHA. Você foi pego. Perdeu $${fine} em multas.`);
    }
  };

  // Estilos para a interface
  const gameContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    padding: '20px',
    maxWidth: '1000px',
    margin: '0 auto',
    fontFamily: 'Arial, sans-serif',
    border: '1px solid #ccc',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
  };

  const statusStyle: React.CSSProperties = {
    padding: '10px',
    backgroundColor: '#fff3e0',
    border: '1px solid #ff9800',
    borderRadius: '5px',
    minHeight: '30px',
  };
  
  // Renderização
  return (
    <div style={gameContainerStyle}>
      <h1>Los Santos Prototype (KAN-1921)</h1>
      <p>
        <span style={{ color: 'green', fontWeight: 'bold' }}>[Status]</span> {status}
      </p>

      {/* HUD / Status Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '2px solid #ddd' }}>
        <div>
          💰 Dinheiro: ${money.toLocaleString()}
        </div>
        <div>
          🗺️ Posição: ({Math.round(position.x)}, {Math.round(position.y)})
        </div>
      </div>

      {/* Mapa e Personagem */}
      <div style={{ position: 'relative' }}>
        <Map playerPosition={position} />
        <Character position={position} />
      </div>

      {/* Controles e Ações */}
      <div style={{ display: 'flex', gap: '20px' }}>
        
        {/* Controles de Movimento (Simplificação de UI) */}
        <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', width: '200px' }}>
          <h3>Controles (WASD/Setas)</h3>
          <p>Use as teclas de seta ou WASD para mover o personagem no mapa.</p>
          <button 
            onClick={() => handleMove('up')} 
            style={{ display: 'block', margin: '5px 0', padding: '10px', width: '100%' }}
          >
            ↑ Cima
          </button>
          <button 
            onClick={() => handleMove('left')} 
            style={{ display: 'block', margin: '5px 0', padding: '10px', width: '100%' }}
          >
            ← Esquerda
          </button>
          <button 
            onClick={() => handleMove('down')} 
            style={{ display: 'block', margin: '5px 0', padding: '10px', width: '100%' }}
          >
            ↓ Baixo
          </button>
          <button 
            onClick={() => handleMove('right')} 
            style={{ display: 'block', margin: '5px 0', padding: '10px', width: '100%' }}
          >
            → Direita
          </button>
        </div>

        {/* Ações de Jogo */}
        <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', flexGrow: 1 }}>
          <h3>Ações</h3>
          <p>Este é o local para implementar a lógica de interações complexas (ex: veículo, combate).</p>
          <button 
            onClick={handleInteract} 
            style={{ padding: '10px 20px', backgroundColor: '#d32f2f', color: 'white', border: 'none', cursor: 'pointer' }}
          >
            [E] Iniciar Missão Rápida (Debito Técnico)
          </button>
          <p style={{marginTop: '10px', fontSize: '0.9em', color: '#666'}}>
            * Esta funcionalidade simula a lógica de "Crime/Missão" que será refinada na próxima sprint (CTO).
          </p>
        </div>
      </div>
    </div>
  );
}

export default GTAPrototype;