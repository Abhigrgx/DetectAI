# Evaluation Results

## Current Status
- Training/evaluation script is implemented at `ml_pipeline/scripts/train_model.py`.
- Metrics are exported to `ml_pipeline/artifacts/evaluation_metrics.txt` after training.

## Reported Metrics
- Accuracy
- Precision
- Recall
- F1-score

## How to Reproduce
```bash
cd ml_pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python scripts/train_model.py
cat artifacts/evaluation_metrics.txt
```

## Notes
- Included sample datasets are illustrative and small.
- For production use, train on larger, diverse, and regularly refreshed datasets.
- Calibrate thresholds per domain (academic, enterprise, journalism) to reduce false positives.
