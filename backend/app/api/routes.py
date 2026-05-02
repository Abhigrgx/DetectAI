from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.config import MAX_TEXT_CHARS
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.db_models import AnalysisRecord
from app.models.schemas import (
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    PlagiarismRequest,
    PlagiarismResponse,
)
from app.services.detector import HybridDetector
from app.services.file_parser import UnsupportedFileTypeError, extract_text_from_file
from app.services.plagiarism import PlagiarismChecker
from app.services.text_utils import sanitize_text


router = APIRouter()

detector = HybridDetector()
plagiarism_checker = PlagiarismChecker()

DISCLAIMER = (
    "This result is an estimation, not proof. Do not use automated scores as the sole basis "
    "for disciplinary, legal, or academic punishment without human review."
)


def _analyze_payload(text: str) -> AnalyzeTextResponse:
    clean = sanitize_text(text)
    if len(clean) < 50:
        raise HTTPException(status_code=400, detail="Text is too short for reliable analysis.")
    if len(clean) > MAX_TEXT_CHARS:
        raise HTTPException(status_code=400, detail="Text exceeds maximum length.")

    result = detector.predict(clean)
    return AnalyzeTextResponse(
        ai_probability=result.ai_probability,
        human_probability=result.human_probability,
        confidence=result.confidence,
        model_breakdown=result.model_breakdown,
        suspicious_segments=result.suspicious_segments,
        explainability=result.explainability,
        disclaimer=DISCLAIMER,
        metadata=result.metadata,
    )


@router.post("/analyze-text", response_model=AnalyzeTextResponse)
@limiter.limit("20/minute")
def analyze_text(
    request: Request,
    payload: AnalyzeTextRequest,
    db: Session = Depends(get_db),
) -> AnalyzeTextResponse:
    response = _analyze_payload(payload.text)
    db.add(
        AnalysisRecord(
            endpoint="analyze-text",
            input_text=payload.text[:5000],
            ai_probability=response.ai_probability,
            confidence=response.confidence,
            payload_metadata={"language": payload.language, "model_breakdown": response.model_breakdown},
        )
    )
    db.commit()
    return response


@router.post("/detect-ai", response_model=AnalyzeTextResponse)
@limiter.limit("20/minute")
def detect_ai(
    request: Request,
    payload: AnalyzeTextRequest,
    db: Session = Depends(get_db),
) -> AnalyzeTextResponse:
    response = _analyze_payload(payload.text)
    db.add(
        AnalysisRecord(
            endpoint="detect-ai",
            input_text=payload.text[:5000],
            ai_probability=response.ai_probability,
            confidence=response.confidence,
            payload_metadata={"language": payload.language, "model_breakdown": response.model_breakdown},
        )
    )
    db.commit()
    return response


@router.post("/analyze-upload", response_model=AnalyzeTextResponse)
@limiter.limit("10/minute")
async def analyze_upload(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> AnalyzeTextResponse:
    raw = await file.read()
    try:
        text = extract_text_from_file(file.filename or "input.txt", raw)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    response = _analyze_payload(text)
    db.add(
        AnalysisRecord(
            endpoint="analyze-upload",
            input_text=text[:5000],
            ai_probability=response.ai_probability,
            confidence=response.confidence,
            payload_metadata={"filename": file.filename or "unknown"},
        )
    )
    db.commit()
    return response


@router.post("/plagiarism-check", response_model=PlagiarismResponse)
@limiter.limit("15/minute")
def plagiarism_check(
    request: Request,
    payload: PlagiarismRequest,
    db: Session = Depends(get_db),
) -> PlagiarismResponse:
    clean = sanitize_text(payload.text)
    originality, matches = plagiarism_checker.check(clean)
    response = PlagiarismResponse(
        originality_score=originality,
        top_matches=matches,
        disclaimer="Plagiarism similarity is indicative and may miss paraphrased or private sources.",
    )
    db.add(
        AnalysisRecord(
            endpoint="plagiarism-check",
            input_text=payload.text[:5000],
            originality_score=response.originality_score,
            payload_metadata={"matches": [m.source_id for m in matches]},
        )
    )
    db.commit()
    return response
