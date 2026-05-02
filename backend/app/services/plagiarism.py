from __future__ import annotations

from pathlib import Path

from app.core.config import DEFAULT_REFERENCE_CORPUS
from app.models.schemas import PlagiarismMatch
from app.services.text_utils import tokenize_words


def _ngrams(tokens: list[str], n: int = 4) -> set[str]:
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a.intersection(b)) / max(1, len(a.union(b)))


class PlagiarismChecker:
    def __init__(self, corpus_path: Path | None = None) -> None:
        self.corpus_path = corpus_path or DEFAULT_REFERENCE_CORPUS
        self.sources = self._load_sources()

    def _load_sources(self) -> dict[str, str]:
        if not self.corpus_path.exists():
            return {}

        data = self.corpus_path.read_text(encoding="utf-8")
        blocks = [b.strip() for b in data.split("\n\n===\n\n") if b.strip()]
        sources: dict[str, str] = {}
        for i, block in enumerate(blocks, start=1):
            sources[f"source_{i}"] = block
        return sources

    def check(self, text: str) -> tuple[float, list[PlagiarismMatch]]:
        text_ngrams = _ngrams(tokenize_words(text))
        matches: list[PlagiarismMatch] = []

        for source_id, source_text in self.sources.items():
            source_tokens = tokenize_words(source_text)
            source_ngrams = _ngrams(source_tokens)
            sim = _jaccard(text_ngrams, source_ngrams)
            if sim > 0.05:
                phrases = sorted(text_ngrams.intersection(source_ngrams))[:4]
                matches.append(
                    PlagiarismMatch(source_id=source_id, similarity=sim, matched_phrases=phrases)
                )

        matches.sort(key=lambda m: m.similarity, reverse=True)
        top = matches[:5]
        max_sim = top[0].similarity if top else 0.0
        originality = max(0.0, 1.0 - max_sim)
        return originality, top
