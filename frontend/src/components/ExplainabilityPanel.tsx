import type { Explainability } from "../lib/api";

type Props = {
  data: Explainability;
};

const labels: Array<{ key: keyof Explainability; label: string }> = [
  { key: "perplexity", label: "Perplexity (approx.)" },
  { key: "burstiness", label: "Burstiness" },
  { key: "repetition_rate", label: "Repetition rate" },
  { key: "vocabulary_diversity", label: "Vocabulary diversity" },
  { key: "sentence_length_variance", label: "Sentence length variance" },
  { key: "passive_voice_frequency", label: "Passive voice frequency" },
  { key: "punctuation_entropy", label: "Punctuation entropy" },
  { key: "embedding_uniformity", label: "Embedding uniformity" },
];

export function ExplainabilityPanel({ data }: Props) {
  return (
    <section className="panel">
      <h3>Explainability Signals</h3>
      <div className="feature-grid">
        {labels.map((item) => (
          <div key={item.key} className="feature-item">
            <span>{item.label}</span>
            <strong>{Number(data[item.key]).toFixed(3)}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
