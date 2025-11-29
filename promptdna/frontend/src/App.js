import React, { useState, useEffect } from "react";
import "./styles.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [resp, setResp] = useState(null);
  const [logs, setLogs] = useState([]);

  const analyze = async () => {
    const r = await fetch("http://localhost:8000/v1/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: "dev1", prompt })
    });
    const j = await r.json();
    setResp(j);
    fetchLogs();
  };

  const fetchLogs = async () => {
    const r = await fetch("http://localhost:8000/v1/logs");
    const j = await r.json();
    setLogs(j.logs || []);
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="container">
      <h1>PromptDNA — Demo</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={6}
      />
      <button onClick={analyze}>Check Prompt</button>

      {resp && (
        <div className="result">
          <h3>Decision: {resp.decision}</h3>
          <p>Risk Score: {resp.risk_score}</p>
          <p>Reasons: {resp.reasons}</p>
          <h4>LLM Response:</h4>
          <pre>{resp.response}</pre>
        </div>
      )}

      <h2>Recent Logs</h2>
      <ul>
        {logs.map((l) => (
          <li key={l._id}>
            <strong>{l.timestamp}</strong> — {l.user_id} — {l.decision} — {l.dna_hash}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
