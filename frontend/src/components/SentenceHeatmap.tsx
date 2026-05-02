import type { SegmentScore } from "../lib/api";

type Props = {
  segments: SegmentScore[];
};

export function SentenceHeatmap({ segments }: Props) {
  if (!segments.length) {
    return <p className="muted">No sentence-level flags available yet.</p>;
  }

  return (
    <div className="heatmap-list">
      {segments.map((segment, idx) => (
        <article key={`${segment.sentence.slice(0, 24)}-${idx}`} className="heatmap-card">
          <header>
            <h4>Flag {idx + 1}</h4>
            <span>{Math.round(segment.ai_likelihood * 100)}%</span>
          </header>
          <p>{segment.sentence}</p>
          <ul>
            {segment.reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </article>
      ))}
    </div>
  );
}
