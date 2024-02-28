import React, { useState } from 'react';
import './App.css'; // Make sure to update this CSS file as per the instructions below
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [sqlQuery, setSqlQuery] = useState(''); // State for the SQL query
  const [queryResult, setQueryResult] = useState(''); // State for the raw query result
  const [formattedResponse, setFormattedResponse] = useState(''); // State for the formatted answer

  const sendQuery = async () => {
    try {
      const result = await axios.post('http://localhost:8000/query/', { text: query });
      // Assuming the backend response contains the SQL query, raw result, and formatted response
      console.log("sql query:", result.data.sqlquery);
      setSqlQuery(result.data.sqlquery);
      setQueryResult(result.data.rawresult);
      setFormattedResponse(result.data.formattedresponse);
    } catch (error) {
      console.error('Error sending query:', error);
      // Reset all responses on error
      setSqlQuery('');
      setQueryResult('');
      setFormattedResponse('Error processing your query');
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">Welcome to WanderWithDevesh!</h1>
        <input
          type="text"
          className="query-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
        />
        <button className="submit-btn" onClick={sendQuery}>Submit</button>
        <div className="explainer">
          <div className="step">
            <h2>1. Question Asked</h2>
            <p>{query || 'Your question will appear here...'}</p>
          </div>
          <div className="step">
            <h2>2. SQL Query</h2>
            <p>{sqlQuery || 'SQL query will appear here...'}</p>
          </div>
          <div className="step">
            <h2>3. Query Output</h2>
            <p>{queryResult || 'Query results will appear here...'}</p>
          </div>
          </div>
          <div className="query-output">
            <h4>4. Formatted Answer</h4>
            <p>{formattedResponse || 'The formatted response will appear here...'}</p>
          </div>
      </div>
    </div>
  );
}

export default App;
