import { useState } from "react";
import "./App.css";  // Import CSS

export default function App() {
  const [logData, setLogData] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const scanLogs = async () => {
    setLoading(true);
    setResponse(null);
    try {
      const res = await fetch("http://127.0.0.1:5000/scan_logs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ log_data: logData }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: "Failed to connect to the server" });
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>CyberSecurity AI Agent</h1>

      {/* Project Description Section */}
      <div className="project-details">
        <h2>About This Project</h2>
        <p>
          This AI-powered cybersecurity agent monitors system logs to detect potential threats 
          such as unauthorized access attempts, brute-force attacks, and suspicious activities.
        </p>

        <h3>How It Works</h3>
        <ul>
          <li>Enter a system log entry in the text box.</li>
          <li>Click "Scan Logs" to analyze the log for threats.</li>
          <li>The AI model will detect and alert any security risks.</li>
          <li>Safe logs return a success message.</li>
        </ul>

        <h3>Example Test Cases</h3>
        <p>Try entering the following log messages:</p>
        <ul>
          <li><code>Failed password for admin from 192.168.1.1 port 22</code> (Detects brute-force attack)</li>
          <li><code>sudo: incorrect password attempt</code> (Detects unauthorized access)</li>
          <li><code>Normal system operation</code> (No threat detected)</li>
        </ul>
      </div>

      {/* Log Entry Textarea */}
      <textarea
        placeholder="Enter system log data..."
        value={logData}
        onChange={(e) => setLogData(e.target.value)}
      />
      
      {/* Scan Logs Button */}
      <button onClick={scanLogs} disabled={loading}>
        {loading ? "Scanning..." : "Scan Logs"}
      </button>
      
      {/* Response Section */}
      {response && (
        <div className={`response ${response.alert ? "alert" : "success"}`}>
          {response.alert ? response.alert : response.message}
        </div>
      )}
    </div>
  );
}
