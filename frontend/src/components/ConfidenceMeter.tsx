type Props = {
  label: string;
  value: number;
  accent: "ai" | "human";
};

export function ConfidenceMeter({ label, value, accent }: Props) {
  return (
    <div className="meter">
      <div className="meter-head">
        <span>{label}</span>
        <strong>{Math.round(value * 100)}%</strong>
      </div>
      <div className="meter-track">
        <div
          className={`meter-fill ${accent}`}
          style={{ width: `${Math.round(value * 100)}%` }}
          aria-hidden
        />
      </div>
    </div>
  );
}
