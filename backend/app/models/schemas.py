from typing import Any

from pydantic import BaseModel, Field


class AnalyzeTextRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=25000)
    language: str = Field(default="en")


class SegmentScore(BaseModel):
    sentence: str
    ai_likelihood: float = Field(..., ge=0.0, le=1.0)
    reasons: list[str]


class ExplainabilityFeatures(BaseModel):
    perplexity: float
    burstiness: float
    repetition_rate: float
    vocabulary_diversity: float
    sentence_length_variance: float
    passive_voice_frequency: float
    punctuation_entropy: float
    embedding_uniformity: float


class AnalyzeTextResponse(BaseModel):
    ai_probability: float = Field(..., ge=0.0, le=1.0)
    human_probability: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_breakdown: dict[str, float]
    suspicious_segments: list[SegmentScore]
    explainability: ExplainabilityFeatures
    disclaimer: str
    metadata: dict[str, Any]


class PlagiarismRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=25000)


class PlagiarismMatch(BaseModel):
    source_id: str
    similarity: float
    matched_phrases: list[str]


class PlagiarismResponse(BaseModel):
    originality_score: float = Field(..., ge=0.0, le=1.0)
    top_matches: list[PlagiarismMatch]
    disclaimer: str
