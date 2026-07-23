import React, { useState, useEffect, useCallback } from 'react';

interface Employee {
  id: number;
  name: string;
  score: number;
}

interface EmployeeRankingProps {
  apiUrl: string;
}

interface RankingError {
  message: string;
  details?: any;
}

const EmployeeRanking: React.FC<EmployeeRankingProps> = ({ apiUrl }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<RankingError | null>(null);

  const fetchRankings = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(apiUrl);

      if (!response.ok) {
        // Handle HTTP errors (4xx, 5xx)
        let errorMessage = `Failed to fetch data. Status: ${response.status}`;
        try {
          const errorData = await response.json();
          if (errorData.message) {
            errorMessage = errorData.message;
          }
        } catch (e) {
          // Fallback if response body is not JSON
          errorMessage = `Failed to fetch data. Server responded with status: ${response.status}`;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      
      // Assume the API returns an array of employee objects directly for simplicity
      if (Array.isArray(data)) {
        setEmployees(data);
      } else {
        throw new Error("Invalid data format received from the server.");
      }

    } catch (err) {
      // Handle network errors or errors thrown above
      const errorMsg = err instanceof Error ? err.message : "An unknown error occurred during data fetching.";
      setError({ message: errorMsg });
      setEmployees([]); // Clear any potentially partial data
      console.error("EmployeeRanking Fetch Error:", err);
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchRankings();
  }, [fetchRankings]);

  if (loading) {
    return <div>Loading employee rankings...</div>;
  }

  if (error) {
    // Display user-friendly error message
    return (
      <div style={{ color: 'red', border: '1px solid red', padding: '10px', backgroundColor: '#ffeeee' }}>
        <h2>Error Loading Rankings</h2>
        <p>{error.message}</p>
        <p>Please check the API endpoint or your connection.</p>
      </div>
    );
  }

  if (employees.length === 0) {
    return <div style={{ color: 'gray' }}>No employee rankings found.</div>;
  }

  return (
    <div>
      <h1>Employee Rankings</h1>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((employee, index) => (
            <tr key={employee.id}>
              <td>{index + 1}</td>
              <td>{employee.name}</td>
              <td>{employee.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EmployeeRanking;