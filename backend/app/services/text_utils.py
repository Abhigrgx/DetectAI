import re
from collections import Counter


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"\b\w+\b")


def sanitize_text(text: str) -> str:
    text = text.replace("\x00", " ").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_sentences(text: str) -> list[str]:
    chunks = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    if not chunks and text.strip():
        return [text.strip()]
    return chunks


def tokenize_words(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def repetition_rate(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    repeated = sum(c for c in counts.values() if c > 1)
    return repeated / len(tokens)


def vocabulary_diversity(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)
