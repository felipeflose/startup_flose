import React, { useState, useEffect, useCallback } from 'react';

interface JiraTicket {
  id: string;
  summary: string;
  status: 'To Do' | 'In Progress' | 'Review' | 'Done';
  priority: 'Low' | 'Medium' | 'High';
  assignee: string;
}

interface DashboardData {
  tickets: JiraTicket[];
  totalTickets: number;
  statusCounts: { [key: string]: number };
}

const mockFetchJiraData = (): Promise<DashboardData> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const data: JiraTicket[] = [
        { id: 'JIRA-101', summary: 'Implementar login OAuth', status: 'Done', priority: 'High', assignee: 'Alice' },
        { id: 'JIRA-102', summary: 'Refatorar componente principal', status: 'In Progress', priority: 'High', assignee: 'Bob' },
        { id: 'JIRA-103', summary: 'Testes de integração API', status: 'To Do', priority: 'Medium', assignee: 'Charlie' },
        { id: 'JIRA-104', summary: 'Documentação da API v2', status: 'Review', priority: 'Low', assignee: 'Alice' },
        { id: 'JIRA-105', summary: 'Melhorar UX do Dashboard', status: 'In Progress', priority: 'Medium', assignee: 'Bob' },
      ];
      resolve({
        tickets: data,
        totalTickets: data.length,
        statusCounts: {
          'To Do': 1,
          'In Progress': 2,
          'Review': 1,
          'Done': 1,
        },
      });
    }, 800);
  });
};

const JiraDashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const result = await mockFetchJiraData();
      setData(result);
    } catch (err) {
      setError("Falha ao carregar os dados do Jira.");
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return <div className="dashboard-container">Carregando dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-container error">Erro: {error}</div>;
  }

  if (!data) {
    return <div className="dashboard-container">Nenhum dado encontrado.</div>;
  }

  const getStatusClass = (status: JiraTicket['status']) => {
    switch (status) {
      case 'Done':
        return 'status-done';
      case 'In Progress':
        return 'status-in-progress';
      case 'Review':
        return 'status-review';
      case 'To Do':
        return 'status-todo';
      default:
        return 'status-default';
    }
  };

  const getPriorityClass = (priority: JiraTicket['priority']) => {
    switch (priority) {
      case 'High':
        return 'priority-high';
      case 'Medium':
        return 'priority-medium';
      case 'Low':
        return 'priority-low';
      default:
        return 'priority-default';
    }
  };

  return (
    <div className="dashboard-container">
      <h1>Jira Dashboard</h1>

      {/* Summary Metrics */}
      <div className="metrics-grid">
        <div className="metric-card status-todo">
          <h2>Pendentes</h2>
          <p>{data.statusCounts['To Do'] || 0}</p>
        </div>
        <div className="metric-card status-in-progress">
          <h2>Em Progresso</h2>
          <p>{data.statusCounts['In Progress'] || 0}</p>
        </div>
        <div className="metric-card status-review">
          <h2>Em Revisão</h2>
          <p>{data.statusCounts['Review'] || 0}</p>
        </div>
        <div className="metric-card status-done">
          <h2>Concluídos</h2>
          <p>{data.statusCounts['Done'] || 0}</p>
        </div>
      </div>

      {/* Ticket List */}
      <h2>Tickets Detalhados</h2>
      <div className="ticket-list">
        {data.tickets.map((ticket) => (
          <div key={ticket.id} className="ticket-item">
            <div className="ticket-header">
              <h3>{ticket.id}: {ticket.summary}</h3>
              <span className={`status-badge ${getStatusClass(ticket.status)}`}>
                {ticket.status}
              </span>
              <span className={`priority-badge ${getPriorityClass(ticket.priority)}`}>
                {ticket.priority}
              </span>
            </div>
            <p><strong>Atribuído a:</strong> {ticket.assignee}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JiraDashboard;