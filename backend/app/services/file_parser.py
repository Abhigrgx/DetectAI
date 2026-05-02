from __future__ import annotations

import io
from pathlib import Path

from docx import Document
from pypdf import PdfReader


class UnsupportedFileTypeError(ValueError):
    pass


def extract_text_from_file(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()

    if suffix == ".txt":
        return content.decode("utf-8", errors="ignore")

    if suffix == ".docx":
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)

    raise UnsupportedFileTypeError("Supported file types: .txt, .docx, .pdf")
