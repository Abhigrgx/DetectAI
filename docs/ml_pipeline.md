# ML Pipeline

## Training Flow
1. Load labeled corpora (`human.txt`, `ai.txt`).
2. Extract hybrid feature vectors:
- Approximate perplexity
- Burstiness
- Repetition and lexical diversity
- Stylometric signals
- Embedding uniformity proxy
3. Train baseline `LogisticRegression` and `RandomForestClassifier`.
4. Compute metrics: accuracy, precision, recall, F1.
5. Export bundle artifact used by FastAPI runtime.

## Deployment Path
- Training script writes model to `backend/artifacts/hybrid_detector.joblib`.
- Backend auto-loads the artifact on boot.
- If unavailable, fallback heuristic mode is used with reduced reliability.

## Optional Next Upgrades
- Replace perplexity approximation with true LM perplexity (`gpt2` or domain LM).
- Add transformer fine-tuning for sentence-level classification.
- Add adversarial/paraphrase robustness set in CI.
