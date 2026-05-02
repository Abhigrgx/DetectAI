from pathlib import Path

from detectai.train import train_and_save


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    project_root = base_dir.parent

    human_path = base_dir / "data" / "samples" / "human.txt"
    ai_path = base_dir / "data" / "samples" / "ai.txt"
    out_model = project_root / "backend" / "artifacts" / "hybrid_detector.joblib"
    out_metrics = base_dir / "artifacts" / "evaluation_metrics.txt"

    metrics = train_and_save(human_path=human_path, ai_path=ai_path, output_path=out_model, metrics_path=out_metrics)
    print("Training complete:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
