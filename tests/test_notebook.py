import ast
from pathlib import Path

import nbformat
import pandas as pd
import pytest

NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks/variant_analysis.ipynb"


def test_notebook_is_valid_and_contains_no_recorded_outputs():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert len(code_cells) > 20
    for cell in code_cells:
        ast.parse(cell.source)
        assert cell.outputs == []
        assert cell.execution_count is None


def test_notebook_join_does_not_expand_repeated_annotations():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    join_cell = next(c.source for c in notebook.cells if "validate='one_to_one'" in c.source)
    frame = pd.DataFrame({
        "Order_ID_cfDNA": ["synthetic", "synthetic", "synthetic"],
        "HGVSc": ["demo", "demo", "demo"],
        "HGVSp_Short": ["demo", "demo", "demo"],
    }, index=[10, 11, 12])
    filtered = pd.DataFrame({"predicted_category": ["GOOD", "BAD"]}, index=[10, 12])
    namespace = {"df": frame, "df_filtered": filtered}
    exec(compile(join_cell, str(NOTEBOOK), "exec"), namespace)
    result = namespace["df_original_with_predictions_filtered"]
    assert result.index.tolist() == [10, 12]
    assert result["predicted_category"].tolist() == ["GOOD", "BAD"]


def test_historical_cluster_mapping_requires_opt_in():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    cell = next(c.source for c in notebook.cells if "if not REUSE_HISTORICAL_CLUSTER_LABELS:" in c.source)
    with pytest.raises(RuntimeError, match="not portable"):
        exec(compile(cell, str(NOTEBOOK), "exec"), {"REUSE_HISTORICAL_CLUSTER_LABELS": False})
