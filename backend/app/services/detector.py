from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.core.config import DEFAULT_MODEL_PATH
from app.models.schemas import ExplainabilityFeatures, SegmentScore
from app.services.text_utils import repetition_rate, split_sentences, tokenize_words, vocabulary_diversity


def _safe_std(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(np.std(values))


def _punctuation_entropy(text: str) -> float:
    punctuation = [ch for ch in text if ch in ".,;:!?-()\"'"]
    if not punctuation:
        return 0.0
    unique, counts = np.unique(punctuation, return_counts=True)
    probs = counts / counts.sum()
    entropy = -(probs * np.log2(probs + 1e-12)).sum()
    return float(entropy / np.log2(len(unique) + 1e-12))


def _passive_voice_frequency(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    markers = 0
    for s in sentences:
        low = s.lower()
        if " was " in low or " were " in low or " been " in low:
            markers += 1
    return markers / len(sentences)


@dataclass
class HybridPrediction:
    ai_probability: float
    human_probability: float
    confidence: float
    model_breakdown: dict[str, float]
    suspicious_segments: list[SegmentScore]
    explainability: ExplainabilityFeatures
    metadata: dict[str, Any]


class HybridDetector:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or DEFAULT_MODEL_PATH
        self.bundle: dict[str, Any] | None = None
        if self.model_path.exists():
            self.bundle = joblib.load(self.model_path)

    def _build_features(self, text: str) -> dict[str, float]:
        sentences = split_sentences(text)
        tokens = tokenize_words(text)
        sentence_lengths = [len(tokenize_words(s)) for s in sentences]

        burstiness = _safe_std(sentence_lengths)
        rep_rate = repetition_rate(tokens)
        lex_div = vocabulary_diversity(tokens)
        sent_var = float(np.var(sentence_lengths)) if sentence_lengths else 0.0
        passive_freq = _passive_voice_frequency(sentences)
        punct_entropy = _punctuation_entropy(text)

        # Approximate perplexity as inverse lexical diversity weighted by repetition.
        approx_perplexity = float((1.0 / max(lex_div, 1e-6)) * (1.0 + rep_rate))

        # Embedding uniformity proxy based on sentence length variation and overlap.
        uniformity = 1.0 / (1.0 + burstiness + sent_var / 50.0)

        return {
            "perplexity": approx_perplexity,
            "burstiness": burstiness,
            "repetition_rate": rep_rate,
            "vocabulary_diversity": lex_div,
            "sentence_length_variance": sent_var,
            "passive_voice_frequency": passive_freq,
            "punctuation_entropy": punct_entropy,
            "embedding_uniformity": uniformity,
        }

    def _score_segments(self, text: str, doc_ai_probability: float) -> list[SegmentScore]:
        sentences = split_sentences(text)
        if not sentences:
            return []

        scores: list[SegmentScore] = []
        for s in sentences[:30]:
            tokens = tokenize_words(s)
            rep = repetition_rate(tokens)
            lex = vocabulary_diversity(tokens)
            short_or_flat = 1.0 if len(tokens) < 7 else 0.0
            score = min(1.0, max(0.0, 0.35 * rep + 0.35 * (1 - lex) + 0.15 * short_or_flat + 0.15 * doc_ai_probability))

            reasons: list[str] = []
            if rep > 0.25:
                reasons.append("Repetition pattern is unusually high.")
            if lex < 0.55:
                reasons.append("Low vocabulary diversity compared to typical human writing.")
            if short_or_flat > 0:
                reasons.append("Very short sentence with limited stylistic variation.")
            if not reasons:
                reasons.append("Sentence-level indicators slightly align with AI-like consistency.")

            scores.append(SegmentScore(sentence=s, ai_likelihood=score, reasons=reasons))

        scores.sort(key=lambda x: x.ai_likelihood, reverse=True)
        return scores[:8]

    def predict(self, text: str) -> HybridPrediction:
        features = self._build_features(text)
        feature_vector = np.array([[v for v in features.values()]])

        if self.bundle is not None:
            scaler = self.bundle["scaler"]
            lr_model = self.bundle["logistic_regression"]
            rf_model = self.bundle["random_forest"]

            x_scaled = scaler.transform(feature_vector)
            lr_score = float(lr_model.predict_proba(x_scaled)[0][1])
            rf_score = float(rf_model.predict_proba(feature_vector)[0][1])
            heuristic = min(1.0, 0.4 * features["repetition_rate"] + 0.4 * features["embedding_uniformity"] + 0.2 * (1.0 / max(features["perplexity"], 1e-6)))
            ai_probability = float(np.clip(0.45 * lr_score + 0.35 * rf_score + 0.20 * heuristic, 0.0, 1.0))
            breakdown = {
                "logistic_regression": lr_score,
                "random_forest": rf_score,
                "heuristic_semantic": heuristic,
            }
        else:
            ai_probability = float(
                np.clip(
                    0.30 * (1.0 / max(features["perplexity"], 1e-6))
                    + 0.25 * features["embedding_uniformity"]
                    + 0.20 * features["repetition_rate"]
                    + 0.25 * (1 - features["vocabulary_diversity"]),
                    0.0,
                    1.0,
                )
            )
            breakdown = {
                "logistic_regression": ai_probability,
                "random_forest": ai_probability,
                "heuristic_semantic": ai_probability,
            }

        confidence = float(np.clip(abs(ai_probability - 0.5) * 2, 0.0, 1.0))
        suspicious_segments = self._score_segments(text, ai_probability)

        explainability = ExplainabilityFeatures(**features)
        metadata = {
            "model_available": self.bundle is not None,
            "feature_set_version": "1.0",
            "max_sentences_analyzed": 30,
        }

        return HybridPrediction(
            ai_probability=ai_probability,
            human_probability=1.0 - ai_probability,
            confidence=confidence,
            model_breakdown=breakdown,
            suspicious_segments=suspicious_segments,
            explainability=explainability,
            metadata=metadata,
        )
