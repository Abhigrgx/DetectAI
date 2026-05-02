from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from detectai.data_loader import load_dataset
from detectai.features import build_feature_frame


def train_and_save(
    human_path: Path,
    ai_path: Path,
    output_path: Path,
    metrics_path: Path,
) -> dict[str, float]:
    df = load_dataset(human_path, ai_path)
    x_df = build_feature_frame(df["text"].tolist())
    y = df["label"].to_numpy()

    x_train, x_test, y_train, y_test = train_test_split(
        x_df.to_numpy(), y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    logistic = LogisticRegression(max_iter=1000)
    random_forest = RandomForestClassifier(n_estimators=300, random_state=42, min_samples_leaf=2)

    logistic.fit(x_train_scaled, y_train)
    random_forest.fit(x_train, y_train)

    lr_probs = logistic.predict_proba(x_test_scaled)[:, 1]
    rf_probs = random_forest.predict_proba(x_test)[:, 1]
    probs = 0.55 * lr_probs + 0.45 * rf_probs
    preds = (probs >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, zero_division=0)),
        "recall": float(recall_score(y_test, preds, zero_division=0)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
        "n_samples": int(len(df)),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "feature_columns": list(x_df.columns),
            "scaler": scaler,
            "logistic_regression": logistic,
            "random_forest": random_forest,
            "metadata": {
                "ensemble_weights": {"logistic": 0.55, "random_forest": 0.45},
            },
        },
        output_path,
    )

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(
        "\n".join(f"{k}: {v}" for k, v in metrics.items()) + "\n",
        encoding="utf-8",
    )
    return metrics
