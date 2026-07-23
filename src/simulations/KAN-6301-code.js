import React, { useState, useEffect } from 'react';

interface AppState {
  data: string | null;
  error: string | null;
  isLoading: boolean;
}

const initialAppState: AppState = {
  data: null,
  error: null,
  isLoading: true,
};

const App: React.FC = () => {
  const [state, setState] = useState<AppState>(initialAppState);

  // Simulate an asynchronous operation that might fail (e.g., API call)
  const fetchData = async () => {
    setState({ ...state, isLoading: true, error: null });
    try {
      // Simulate a network delay and potential failure
      await new Promise((resolve, reject) => {
        setTimeout(() => {
          // Uncomment the next line to test error handling:
          // reject(new Error("Falha ao buscar dados da API.")); 
          resolve();
        }, 1500);
      });

      // Simulate successful data retrieval
      const mockData = "Dados carregados com sucesso!";
      setState({ ...state, data: mockData, isLoading: false });

    } catch (error) {
      // Refactored error handling: Catch specific errors and set state clearly.
      const errorMessage = error instanceof Error ? error.message : "Erro desconhecido ao carregar os dados.";
      setState({ ...state, data: null, isLoading: false, error: errorMessage });
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Flose Application</h1>
      
      {state.isLoading && <p>Carregando dados...</p>}

      {state.error && (
        <div style={{ color: 'red', border: '1px solid red', padding: '10px', margin: '15px 0' }}>
          <h2>Erro!</h2>
          <p>{state.error}</p>
          <p>Tente recarregar a página.</p>
        </div>
      )}

      {state.data && (
        <div>
          <h2>Dados Carregados</h2>
          <p style={{ color: 'green', fontWeight: 'bold' }}>{state.data}</p>
        </div>
      )}
    </div>
  );
};

export default App;