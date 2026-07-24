import React, { useState, useEffect, useCallback } from 'react';

interface JiraIssue {
  id: string;
  summary: string;
  status: string;
  assignee: string;
  priority: 'High' | 'Medium' | 'Low';
}

interface JiraDashboardProps {
  jiraApiUrl: string;
}

interface DashboardState {
  issues: JiraIssue[];
  loading: boolean;
  error: string | null;
}

const JiraDashboard: React.FC<JiraDashboardProps> = ({ jiraApiUrl }) => {
  const [issues, setIssues] = useState<JiraIssue[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJiraData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(jiraApiUrl);

      if (!response.ok) {
        // Handle HTTP errors (4xx, 5xx)
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      // Assuming the API returns an array of issues directly or nested within a structure
      // Adjust this mapping based on actual API response structure
      setIssues(data.issues || []); 

    } catch (err) {
      // Handle network errors or errors thrown above
      const errorMessage = err instanceof Error ? err.message : "An unknown error occurred during data fetching.";
      setError(errorMessage);
      setIssues([]); // Clear any partial data on error
      console.error("Jira Data Fetch Error:", errorMessage);
    } finally {
      setLoading(false);
    }
  }, [jiraApiUrl]);

  useEffect(() => {
    fetchJiraData();
  }, [fetchJiraData]);

  if (loading) {
    return <div className="jira-dashboard loading">Carregando dados do Jira...</div>;
  }

  if (error) {
    return <div className="jira-dashboard error">Erro ao carregar o dashboard: {error}</div>;
  }

  return (
    <div className="jira-dashboard">
      <h1>Dashboard Jira</h1>
      {issues.length === 0 ? (
        <p>Nenhuma tarefa encontrada.</p>
      ) : (
        <div className="issues-list">
          {issues.map((issue) => (
            <div key={issue.id} className={`issue-card status-${issue.status.toLowerCase()}`}>
              <h2>{issue.summary}</h2>
              <p>ID: {issue.id}</p>
              <p>Status: {issue.status}</p>
              <p>Atribuído a: {issue.assignee}</p>
              <p>Prioridade: {issue.priority}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default JiraDashboard;