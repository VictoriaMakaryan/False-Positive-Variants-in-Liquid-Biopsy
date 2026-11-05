from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from liquid_biopsy import classify_variants

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["variant_qual", "t_alt_count", "Avg_Min_Distance_ALT_reads"]


@pytest.mark.parametrize(
    "values, expected",
    [
        ((381, 32, 25), "AUTO-PASS"),
        ((380, 32, 25), "MANUAL_REVIEW"),
        ((381, 31, 25), "MANUAL_REVIEW"),
        ((100, 10, 20), "MANUAL_REVIEW"),
        ((100, 10, 19.99), "AUTO-REJECT"),
        ((381, 32, 1), "AUTO-PASS"),
        ((np.nan, np.nan, np.nan), "MANUAL_REVIEW"),
        ((np.nan, 40, 5), "AUTO-REJECT"),
        ((500, 40, np.nan), "AUTO-PASS"),
        ((0, 0, 0), "AUTO-REJECT"),
    ],
)
def test_rules_at_boundaries(values, expected):
    result = classify_variants(pd.DataFrame([values], columns=COLUMNS))
    assert result["final_classification"].tolist() == [expected]


def test_nullable_missing_quality_still_allows_independent_reject_rule():
    frame = pd.DataFrame([[pd.NA, 40, 5]], columns=COLUMNS, dtype="Float64")
    assert classify_variants(frame)["final_classification"].tolist() == ["AUTO-REJECT"]


def test_does_not_mutate_reorder_or_multiply_rows():
    frame = pd.DataFrame(
        [[500, 40, 35], [100, 10, 5], [380, 32, 25]], columns=COLUMNS, index=[7, 7, 3]
    )
    frame["example_id"] = ["demo_a", "demo_b", "demo_c"]
    before = frame.copy(deep=True)
    result = classify_variants(frame)
    assert_frame_equal(frame, before)
    assert_frame_equal(result[frame.columns], before)
    assert result["final_classification"].tolist() == ["AUTO-PASS", "AUTO-REJECT", "MANUAL_REVIEW"]


@pytest.mark.parametrize("bad", [float("inf"), float("-inf"), -1, "not-a-number"])
def test_invalid_numeric_evidence_is_rejected(bad):
    with pytest.raises(ValueError):
        classify_variants(pd.DataFrame([[bad, 40, 25]], columns=COLUMNS))


def test_fractional_read_count_is_rejected():
    with pytest.raises(ValueError, match="whole read counts"):
        classify_variants(pd.DataFrame([[500, 31.5, 25]], columns=COLUMNS))


def test_required_columns_are_checked():
    with pytest.raises(ValueError, match="Missing required columns"):
        classify_variants(pd.DataFrame({"variant_qual": [500]}))


def test_preexisting_classification_is_not_silently_overwritten():
    frame = pd.DataFrame([[500, 40, 25]], columns=COLUMNS)
    frame["final_classification"] = "existing"
    with pytest.raises(ValueError, match="already contains"):
        classify_variants(frame)


def test_duplicate_columns_are_rejected():
    frame = pd.DataFrame([[500, 40, 25, 500]], columns=COLUMNS + ["variant_qual"])
    with pytest.raises(ValueError, match="unique"):
        classify_variants(frame)


def test_empty_input_retains_schema():
    result = classify_variants(pd.DataFrame(columns=COLUMNS))
    assert result.empty
    assert list(result.columns) == COLUMNS + ["final_classification"]


def test_cli_demo_and_overwrite_protection(tmp_path):
    output = tmp_path / "triaged.csv"
    command = [sys.executable, "-m", "liquid_biopsy", str(ROOT / "examples/synthetic_variants.csv"), "--output", str(output)]
    run = subprocess.run(command, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    result = pd.read_csv(output)
    assert len(result) == 7
    assert result["final_classification"].value_counts().to_dict() == {
        "MANUAL_REVIEW": 4, "AUTO-PASS": 2, "AUTO-REJECT": 1
    }
    original_bytes = output.read_bytes()
    repeat = subprocess.run(command, capture_output=True, text=True)
    assert repeat.returncode == 2
    assert "already exists" in repeat.stderr
    assert output.read_bytes() == original_bytes


def test_invalid_cli_input_does_not_create_output_or_log_row_value(tmp_path):
    source = tmp_path / "invalid.csv"
    source.write_text(
        "variant_qual,t_alt_count,Avg_Min_Distance_ALT_reads\nprivate_invalid_value,40,25\n"
    )
    output = tmp_path / "output.csv"
    run = subprocess.run(
        [sys.executable, "-m", "liquid_biopsy", str(source), "--output", str(output)],
        capture_output=True, text=True,
    )
    assert run.returncode == 2
    assert not output.exists()
    assert "private_invalid_value" not in run.stderr
