from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DEFAULT_MODEL_PATH = ARTIFACTS_DIR / "hybrid_detector.joblib"
DEFAULT_REFERENCE_CORPUS = ARTIFACTS_DIR / "reference_corpus.txt"
MAX_TEXT_CHARS = 25000
