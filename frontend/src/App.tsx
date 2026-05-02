import { FormEvent, useMemo, useState } from "react";
import { ConfidenceMeter } from "./components/ConfidenceMeter";
import { ExplainabilityPanel } from "./components/ExplainabilityPanel";
import { SentenceHeatmap } from "./components/SentenceHeatmap";
import { AnalyzeResponse, analyzeText, analyzeUpload } from "./lib/api";

const EXAMPLE = `The report presents a concise overview of market dynamics and outlines practical recommendations for strategic planning. It maintains a neutral tone and a consistent structure throughout each section.`;

export function App() {
  const [text, setText] = useState(EXAMPLE);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const summary = useMemo(() => {
    if (!result) return "Paste text or upload a file to begin analysis.";
    const ai = Math.round(result.ai_probability * 100);
    const confidence = Math.round(result.confidence * 100);
    return `Estimated AI-likelihood: ${ai}% with ${confidence}% confidence.`;
  }, [result]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = file ? await analyzeUpload(file) : await analyzeText(text);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <header className="hero">
        <p className="badge">AuthentiText</p>
        <h1>AI Content Detection & Originality Analysis</h1>
        <p>{summary}</p>
      </header>

      <section className="grid">
        <form className="panel" onSubmit={onSubmit}>
          <h2>Analyze Content</h2>
          <label htmlFor="text">Text</label>
          <textarea
            id="text"
            rows={12}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste at least 50 characters"
            disabled={Boolean(file)}
          />

          <label htmlFor="upload">Or upload .txt/.docx/.pdf</label>
          <input
            id="upload"
            type="file"
            accept=".txt,.docx,.pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />

          <div className="actions">
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Run Analysis"}
            </button>
            <button
              type="button"
              onClick={() => {
                setFile(null);
                setText("");
                setResult(null);
                setError(null);
              }}
            >
              Reset
            </button>
          </div>

          <p className="disclaimer">
            This is an estimation, not proof. Always include human review before any high-stakes decision.
          </p>
          {error ? <p className="error">{error}</p> : null}
        </form>

        <section className="panel">
          <h2>Detection Results</h2>
          {result ? (
            <>
              <ConfidenceMeter label="AI probability" value={result.ai_probability} accent="ai" />
              <ConfidenceMeter label="Human probability" value={result.human_probability} accent="human" />

              <h3>Model Breakdown</h3>
              <div className="feature-grid">
                {Object.entries(result.model_breakdown).map(([model, score]) => (
                  <div key={model} className="feature-item">
                    <span>{model.replaceAll("_", " ")}</span>
                    <strong>{Math.round(score * 100)}%</strong>
                  </div>
                ))}
              </div>

              <p className="disclaimer">{result.disclaimer}</p>
            </>
          ) : (
            <p className="muted">No result yet.</p>
          )}
        </section>
      </section>

      {result ? (
        <section className="grid lower">
          <ExplainabilityPanel data={result.explainability} />
          <section className="panel">
            <h3>Sentence-level Heatmap</h3>
            <SentenceHeatmap segments={result.suspicious_segments} />
          </section>
        </section>
      ) : null}
    </main>
  );
}
