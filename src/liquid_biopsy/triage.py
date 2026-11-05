"""The submitted notebook's original-scale, pass-first candidate rules."""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = (
    "variant_qual",
    "t_alt_count",
    "Avg_Min_Distance_ALT_reads",
)


def classify_variants(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with final_classification, preserving row identity.

    Missing values do not satisfy a rule. Reject malformed, negative, or
    infinite evidence. Counts must be whole numbers. A label does not imply
    clinical validity.
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if not frame.columns.is_unique:
        raise ValueError("Input column names must be unique")
    if "final_classification" in frame.columns:
        raise ValueError("Input already contains final_classification")

    numeric = pd.DataFrame(index=frame.index)
    for column in REQUIRED_COLUMNS:
        try:
            numeric[column] = pd.to_numeric(frame[column], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{column} must contain numeric evidence or missing values") from exc
    for column in REQUIRED_COLUMNS:
        values = numeric[column].dropna()
        if not np.isfinite(values).all() or (values < 0).any():
            raise ValueError(f"{column} must contain finite, nonnegative evidence")
    counts = numeric["t_alt_count"].dropna()
    if (counts % 1 != 0).any():
        raise ValueError("t_alt_count must contain whole read counts")

    passed = ((numeric["variant_qual"] > 380) & (numeric["t_alt_count"] > 31)).fillna(False)
    rejected = (~passed) & (numeric["Avg_Min_Distance_ALT_reads"] < 20).fillna(False)
    result = frame.copy()
    result["final_classification"] = "MANUAL_REVIEW"
    result.loc[passed, "final_classification"] = "AUTO-PASS"
    result.loc[rejected, "final_classification"] = "AUTO-REJECT"
    return result
