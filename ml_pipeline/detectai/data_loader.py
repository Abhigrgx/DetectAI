from __future__ import annotations

from pathlib import Path

import pandas as pd


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_dataset(human_path: Path, ai_path: Path) -> pd.DataFrame:
    human = _read_lines(human_path)
    ai = _read_lines(ai_path)

    df_h = pd.DataFrame({"text": human, "label": 0})
    df_a = pd.DataFrame({"text": ai, "label": 1})
    df = pd.concat([df_h, df_a], ignore_index=True)
    return df.sample(frac=1.0, random_state=42).reset_index(drop=True)
