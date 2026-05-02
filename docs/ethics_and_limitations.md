# Ethics, Risk, and Limitations

## Why AI Detection Is Hard
- Modern human and AI writing overlap strongly in style and topic.
- Paraphrasing can suppress detectable signals.
- Domain mismatch can inflate false positives.

## Mandatory Usage Guardrails
- Never present scores as proof.
- Never use automated flags alone for punishment.
- Require human review, context, and appeal process.

## Failure Modes
- False positives: polished human writing can appear AI-like.
- False negatives: heavily edited AI text may evade detection.
- Dataset bias: non-native writing styles can be unfairly flagged.

## Turnitin-Style Comparison
- Similar systems also rely on probabilistic signals and corpus matching.
- Production-grade governance should include confidence calibration and policy-level safeguards.

## Security and Abuse Controls
- Rate limiting is enabled at API level.
- Input size validation and sanitization are applied.
- Logging should avoid storing sensitive content by default.
