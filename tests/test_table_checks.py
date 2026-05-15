from pathlib import Path

from vinl2vis_verifier.table_checks import validate_tables


def test_released_tables_are_consistent() -> None:
    errors = validate_tables(Path("data/tables"))
    assert errors == []
