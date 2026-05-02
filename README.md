# AuthentiText - AI Content Detection & Originality Analysis System

AuthentiText is a production-oriented, hybrid AI-generated text detection platform focused on transparency, explainability, and responsible use.

## What It Does
- Estimates probability that submitted text is AI-generated vs human-written.
- Returns confidence score and model-level breakdown.
- Highlights suspicious sentence segments with reasons.
- Provides explainability features (perplexity proxy, burstiness, repetition, stylometrics, embedding uniformity).
- Includes optional plagiarism similarity checks.

## Ethical Position
- The system does not claim 100% accuracy.
- All outputs are estimations, not proof.
- Scores must not be used as a sole basis for punishment without human review.

## Monorepo Structure
```
backend/       FastAPI inference APIs and runtime services
ml_pipeline/   Feature extraction, model training, evaluation scripts
frontend/      React + Vite user interface
docs/          Architecture, ML pipeline, ethics and limitations
```

## Core Hybrid Detection Strategy
1. Statistical and linguistic analysis:
- Approximate perplexity
- Burstiness and sentence variation
- Repetition and vocabulary diversity

2. Machine learning ensemble:
- Logistic Regression baseline
- Random Forest model
- Weighted probability fusion

3. Embedding consistency proxy:
- Uniformity/consistency indicator to catch overly regular semantic flow

4. Stylometric features:
- Sentence-length variance
- Passive voice frequency
- Punctuation entropy/patterns

## API Endpoints
- `POST /analyze-text`
- `POST /detect-ai`
- `POST /analyze-upload` (`.txt`, `.docx`, `.pdf`)
- `POST /plagiarism-check`
- `GET /health`

## Quick Start

### 1) Train model artifact
```bash
cd ml_pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python scripts/train_model.py
```

This creates:
- `backend/artifacts/hybrid_detector.joblib`
- `ml_pipeline/artifacts/evaluation_metrics.txt`

### 2) Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Run frontend
```bash
cd frontend
npm install
npm run dev
```

Set API URL if needed:
```bash
export VITE_API_BASE=http://localhost:8000
```

## Docker Deployment
```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Evaluation Metrics
The training pipeline exports:
- Accuracy
- Precision
- Recall
- F1-score

See `ml_pipeline/artifacts/evaluation_metrics.txt` after training.

## Security and Reliability Controls
- API rate limiting using `slowapi`
- Input sanitization and max-length checks
- Structured response schema with disclaimers

## Distinction-Level Features Included
- Sentence-level detection heatmap
- Confidence visualization and model breakdown
- Explainable AI feature panel
- File upload analysis (`txt`, `docx`, `pdf`)

## Important Limitations
- Detection quality depends on training data scope.
- Approximate perplexity in this baseline should be replaced with true LM perplexity for stronger fidelity.
- Multilingual accuracy requires language-specific calibration and datasets.

For deeper details, see:
- `docs/architecture.md`
- `docs/ml_pipeline.md`
- `docs/ethics_and_limitations.md`