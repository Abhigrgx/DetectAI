export type SegmentScore = {
  sentence: string;
  ai_likelihood: number;
  reasons: string[];
};

export type Explainability = {
  perplexity: number;
  burstiness: number;
  repetition_rate: number;
  vocabulary_diversity: number;
  sentence_length_variance: number;
  passive_voice_frequency: number;
  punctuation_entropy: number;
  embedding_uniformity: number;
};

export type AnalyzeResponse = {
  ai_probability: number;
  human_probability: number;
  confidence: number;
  model_breakdown: Record<string, number>;
  suspicious_segments: SegmentScore[];
  explainability: Explainability;
  disclaimer: string;
  metadata: Record<string, unknown>;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function analyzeText(text: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE}/analyze-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language: "en" }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Unknown server error" }));
    throw new Error(body.detail || "Unable to analyze text.");
  }

  return response.json();
}

export async function analyzeUpload(file: File): Promise<AnalyzeResponse> {
  const fd = new FormData();
  fd.append("file", file);

  const response = await fetch(`${API_BASE}/analyze-upload`, {
    method: "POST",
    body: fd,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Unknown server error" }));
    throw new Error(body.detail || "Unable to analyze file.");
  }

  return response.json();
}
