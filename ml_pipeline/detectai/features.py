from __future__ import annotations

import re
from collections import Counter

import numpy as np
import pandas as pd


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"\b\w+\b")


def split_sentences(text: str) -> list[str]:
    items = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    if not items and text.strip():
        return [text.strip()]
    return items


def tokenize(text: str) -> list[str]:
    return [x.lower() for x in WORD_RE.findall(text)]


def repetition_rate(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    c = Counter(tokens)
    repeated = sum(v for v in c.values() if v > 1)
    return repeated / len(tokens)


def lexical_diversity(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_entropy(text: str) -> float:
    punct = [ch for ch in text if ch in ".,;:!?-()\"'"]
    if not punct:
        return 0.0
    unique, counts = np.unique(punct, return_counts=True)
    probs = counts / counts.sum()
    entropy = -(probs * np.log2(probs + 1e-12)).sum()
    return float(entropy / np.log2(len(unique) + 1e-12))


def passive_voice_frequency(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    passive_hits = 0
    for s in sentences:
        low = f" {s.lower()} "
        if " was " in low or " were " in low or " been " in low:
            passive_hits += 1
    return passive_hits / len(sentences)


def extract_feature_row(text: str) -> dict[str, float]:
    sentences = split_sentences(text)
    tokens = tokenize(text)
    lengths = [len(tokenize(s)) for s in sentences]

    burstiness = float(np.std(lengths)) if lengths else 0.0
    rep = repetition_rate(tokens)
    lex = lexical_diversity(tokens)
    sent_var = float(np.var(lengths)) if lengths else 0.0
    passive = passive_voice_frequency(sentences)
    punct = punctuation_entropy(text)

    approx_perplexity = float((1.0 / max(lex, 1e-6)) * (1.0 + rep))
    embedding_uniformity = 1.0 / (1.0 + burstiness + sent_var / 50.0)

    return {
        "perplexity": approx_perplexity,
        "burstiness": burstiness,
        "repetition_rate": rep,
        "vocabulary_diversity": lex,
        "sentence_length_variance": sent_var,
        "passive_voice_frequency": passive,
        "punctuation_entropy": punct,
        "embedding_uniformity": embedding_uniformity,
    }


def build_feature_frame(texts: list[str]) -> pd.DataFrame:
    rows = [extract_feature_row(t) for t in texts]
    return pd.DataFrame(rows)
