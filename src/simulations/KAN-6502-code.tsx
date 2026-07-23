import React from 'react';

interface Agent {
  id: number;
  name: string;
  rank: number;
  performanceScore: number; // e.g., 0 to 100
}

interface PerformanceCardProps {
  agent: Agent;
  position: number;
}

const PerformanceCard: React.FC<PerformanceCardProps> = ({ agent, position }) => {
  // Simple logic for performance recognition based on score
  const performanceClass = agent.performanceScore >= 85 ? 'bg-green-100 border-green-500' : agent.performanceScore >= 60 ? 'bg-yellow-100 border-yellow-500' : 'bg-red-100 border-red-500';

  return (
    <div className={`p-4 border-l-4 shadow-md rounded-lg transition duration-300 ${performanceClass}`}>
      <div className="flex justify-between items-start">
        <h3 className="text-xl font-semibold text-gray-800">{agent.name}</h3>
        <span className={`px-3 py-1 text-sm font-bold rounded-full ${position === 1 ? 'bg-blue-500 text-white' : position === 2 ? 'bg-yellow-500 text-gray-800' : 'bg-red-500 text-white'}`}>
          #{position}
        </span>
      </div>
      <p className="mt-2 text-sm text-gray-600">Performance Score: {agent.performanceScore}%</p>
    </div>
  );
};

const TeamPerformanceDashboard: React.FC<{ agents: Agent[] }> = ({ agents }) => {
  // Ensure data is sorted by rank before rendering (assuming input might not always be sorted)
  const sortedAgents = [...agents].sort((a, b) => a.rank - b.rank);

  return (
    <div className="p-6 bg-white shadow-xl rounded-xl max-w-4xl mx-auto">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-6 border-b pb-2">
        Ranking e Desempenho da Equipe
      </h1>
      
      {sortedAgents.length === 0 ? (
        <div className="text-center py-10 bg-gray-50 rounded-lg">
          Nenhum agente encontrado para exibir o ranking.
        </div>
      ) : (
        <div className="space-y-4">
          {sortedAgents.map((agent, index) => (
            <PerformanceCard 
              key={agent.id} 
              agent={agent} 
              position={index + 1} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TeamPerformanceDashboard;

// --- Exemplo de Uso (Para fins de teste, não deve ser parte do componente exportado) ---
/*
const mockAgents: Agent[] = [
  { id: 1, name: "Alice Smith", rank: 1, performanceScore: 92 },
  { id: 2, name: "Bob Johnson", rank: 2, performanceScore: 78 },
  { id: 3, name: "Charlie Brown", rank: 3, performanceScore: 55 },
  { id: 4, name: "Diana Prince", rank: 4, performanceScore: 88 },
];

const App = () => (
    <div className="min-h-screen bg-gray-100 p-8">
        <TeamPerformanceDashboard agents={mockAgents} />
    </div>
);
// export default App;
*/