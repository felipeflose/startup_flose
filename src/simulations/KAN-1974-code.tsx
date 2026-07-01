import React, { useState, useCallback } from 'react';

interface BoardState {
  [key: string]: string | null;
}

const initialBoard: BoardState = {
  '0': null,
  '1': null,
  '2': null,
  '3': null,
  '4': null,
  '5': null,
  '6': null,
  '7': null,
  '8': null,
};

const checkWinner = (board: BoardState): string | null => {
  const lines = [
    ['0', '1', '2'],
    ['3', '4', '5'],
    ['6', '7', '8'],
    ['0', '3', '6'],
    ['1', '4', '7'],
    ['2', '5', '8'],
  ];

  for (const line of lines) {
    const [a, b, c] = line;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a]; // Returns 'X' or 'O'
    }
  }

  if (board['0'] && board['1'] && board['2'] && board['0'] === board['1'] && board['0'] === board['2']) return board['0'];
  if (board['3'] && board['4'] && board['5'] && board['3'] === board['4'] && board['3'] === board['5']) return board['3'];
  if (board['6'] && board['7'] && board['8'] && board['6'] === board['7'] && board['6'] === board['8']) return board['6'];

  return null;
};

const JogoDaVelha7: React.FC = () => {
  const [board, setBoard] = useState<BoardState>(initialBoard);
  const [isXNext, setIsXNext] = useState<boolean>(true);
  const [winner, setWinner] = useState<string | null>(null);

  const handleCellClick = useCallback((index: string) => {
    if (board[index] || winner) {
      return;
    }

    const newBoard = { ...board };
    newBoard[index] = isXNext ? 'X' : 'O';
    setBoard(newBoard);

    const gameWinner = checkWinner(newBoard);
    if (gameWinner) {
      setWinner(gameWinner);
    } else if (!newBoard['0'] && !newBoard['1'] && !newBoard['2'] && !newBoard['3'] && !newBoard['4'] && !newBoard['5'] && !newBoard['6'] && !newBoard['7'] && !newBoard['8']) {
      // Check for draw (if no winner and board is full)
      setWinner('Draw');
    } else {
      // Switch player
      setIsXNext(!isXNext);
    }
  }, [board, isXNext, winner]);

  const renderSquare = (index: string) => (
    <button
      key={index}
      onClick={() => handleCellClick(index)}
      style={{
        width: '100%',
        height: '100px',
        fontSize: '2em',
        textAlign: 'center',
        border: '1px solid #ccc',
        margin: '5px',
        cursor: board[index] ? 'default' : 'pointer',
        backgroundColor: board[index] === 'X' ? '#f0f8ff' : board[index] === 'O' ? '#fff0f0' : '#ffffff',
        fontWeight: board[index] ? 'bold' : 'normal',
      }}
    >
      {board[index]}
    </button>
  );

  return (
    <div style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
      <h1>Jogo da Velha 7</h1>
      {winner && (
        <h2 style={{ color: winner === 'Draw' ? 'blue' : 'red', fontSize: '2em' }}>
          {winner === 'Draw' ? 'Empate!' : `${winner} venceu!`}
        </h2>
      )}
      <div style={{ display: 'grid', gridTemplateColumns: '3fr 1fr', gap: '10px', maxWidth: '400px', margin: '20px auto' }}>
        {renderSquare('0')}
        {renderSquare('1')}
        {renderSquare('2')}
        {renderSquare('3')}
        {renderSquare('4')}
        {renderSquare('5')}
        {renderSquare('6')}
        {renderSquare('7')}
        {renderSquare('8')}
      </div>
      <p>Vez do: {isXNext ? 'X' : 'O'}</p>
      <button onClick={() => {
        setBoard(initialBoard);
        setIsXNext(true);
        setWinner(null);
      }} style={{ marginTop: '20px', padding: '10px 20px', cursor: 'pointer' }}>
        Reiniciar Jogo
      </button>
    </div>
  );
};

export default JogoDaVelha7;