# AuthentiText System Architecture

```mermaid
flowchart LR
    A[Web Frontend - React] --> B[FastAPI Gateway]
    B --> C[Hybrid Detection Engine]
    C --> C1[Statistical + Linguistic Features]
    C --> C2[Stylometric Features]
    C --> C3[ML Classifiers - LR + RF]
    C --> C4[Embedding Uniformity Heuristic]
    B --> D[Plagiarism Similarity Module]
    B --> E[(PostgreSQL)]
    C --> F[Model Artifacts]
    G[ML Training Pipeline] --> F
    H[Monitoring/Logs] --> B
```

## Key Decisions
- Hybrid scoring is used to reduce over-reliance on one detector family.
- API outputs probabilities and confidence, not a binary accusation.
- Explainability payload exposes internal features for transparency.
- Sentence-level highlights support human reviewer workflows.
