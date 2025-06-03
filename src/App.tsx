import  { useState } from "react";
import './App.css';
import  {ClipLoader}  from "react-spinners";

function App() {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateSummary = async () => {
    setLoading(true);
    setSummary("");
    setError("");

    try {
      
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      const currentUrl = tabs[0]?.url;

      if (!currentUrl) {
        throw new Error("Unable to get current tab URL");
      }

      const res = await fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: currentUrl }),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch summary");
      }

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setSummary(data.summary);
      }
    } catch (err : any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 w-[350px] flex flex-col gap-3">
      <h2 className="text-lg font-bold mb-2">YouTube Video Summarizer</h2>

      <button
        onClick={generateSummary}
        disabled={loading}
        className="bg-blue-600 text-white p-2 rounded disabled:opacity-50"
      >
        Generate Summary
      </button>

      {loading && <ClipLoader />}

      {error && <p className="text-red-600">Error: {error}</p>}

      {summary && (
        <div className="mt-4 p-3 bg-gray-100 rounded whitespace-pre-line text-sm max-h-48 overflow-y-auto">
          {summary}
        </div>
      )}
    </div>
  );
}

export default App;
