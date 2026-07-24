import React, { useState, useEffect, useCallback } from 'react';

interface JiraIssue {
  id: string;
  summary: string;
  status: string;
  priority: string;
}

interface JiraDashboardProps {
  jiraQuery: string;
}

/**
 * Custom error type for better error management.
 */
interface DashboardError extends Error {
  type: 'FETCH_ERROR' | 'VALIDATION_ERROR' | 'UNKNOWN_ERROR';
  details?: any;
}

const JiraDashboard: React.FC<JiraDashboardProps> = ({ jiraQuery }) => {
  const [issues, setIssues] = useState<JiraIssue[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<DashboardError | null>(null);

  const fetchJiraData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Simulate an API call
      const response = await fetch(`/api/jira?query=${jiraQuery}`);
      
      if (!response.ok) {
        // Handle HTTP errors (4xx, 5xx)
        throw new Error(`API responded with status: ${response.status}`);
      }

      const data = await response.json();
      
      // Simulate data validation
      if (!Array.isArray(data.issues)) {
        throw new Error('Data structure invalid: Expected an array of issues.');
      }

      setIssues(data.issues);

    } catch (err) {
      console.error('Error fetching Jira data:', err);
      
      // Determine the type of error for better UI feedback
      if (err instanceof Error) {
        setError({ type: 'FETCH_ERROR', message: err.message });
      } else {
        setError({ type: 'UNKNOWN_ERROR', message: 'An unknown error occurred during data retrieval.' });
      }
      setIssues([]); // Clear issues on error
    } finally {
      setLoading(false);
    }
  }, [jiraQuery]);

  useEffect(() => {
    fetchJiraData();
  }, [fetchJiraData]);

  if (loading) {
    return <div className="dashboard-loading">Loading Jira data...</div>;
  }

  if (error) {
    // Optimized error display: show specific error details
    return (
      <div className="dashboard-error">
        <h2>Error Loading Dashboard</h2>
        <p>Type: {error.type}</p>
        <p>Message: {error.message}</p>
        <p>Please check the query or try again later.</p>
      </div>
    );
  }

  return (
    <div className="jira-dashboard">
      <h1>Jira Dashboard for: {jiraQuery}</h1>
      {issues.length === 0 ? (
        <p>No issues found matching your criteria.</p>
      ) : (
        <div className="issue-list">
          {issues.map(issue => (
            <div key={issue.id} className={`issue-card status-${issue.status.toLowerCase()}`}>
              <h3>{issue.summary}</h3>
              <p>ID: {issue.id}</p>
              <p>Status: {issue.status}</p>
              <p>Priority: {issue.priority}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default JiraDashboard;