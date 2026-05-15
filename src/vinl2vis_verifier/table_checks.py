"""Validation and reporting utilities for released paper-facing tables."""

from __future__ import annotations

from pathlib import Path

from .io import read_csv


REQUIRED_TABLES = {
    "main_before_after_results.csv",
    "paired_sample_delta_summary.csv",
    "strict_transform_flags_before_repair.csv",
    "strict_transform_results_after_repair.csv",
    "english_repair_chain_failure_reduction.csv",
    "watchdog_stop_cases.csv",
    "verifier_guided_repair_ledger.csv",
}


def validate_tables(table_dir: Path) -> list[str]:
    errors: list[str] = []
    missing = sorted(name for name in REQUIRED_TABLES if not (table_dir / name).exists())
    errors.extend(f"missing table: {name}" for name in missing)
    if errors:
        return errors

    before_after = read_csv(table_dir / "main_before_after_results.csv")
    for row in before_after:
        base = float(row["baseline_faithfulness"])
        final = float(row["final_faithfulness"])
        delta = float(row["delta_faithfulness"])
        if round(final - base, 3) != round(delta, 3):
            errors.append(f"faithfulness delta mismatch: {row['experiment']}")

    paired = read_csv(table_dir / "paired_sample_delta_summary.csv")
    for row in paired:
        total = int(row["improved"]) + int(row["unchanged"]) + int(row["degraded"])
        if total != int(row["paired_n"]):
            errors.append(f"paired count mismatch: {row['experiment']}")

    flags = read_csv(table_dir / "strict_transform_flags_before_repair.csv")
    for row in flags:
        total = int(row["missing_filter"]) + int(row["missing_sort"]) + int(row["missing_aggregation"])
        if total != int(row["total_flags"]):
            errors.append(f"strict-transform total mismatch: {row['run']}")
    return errors


def summary_markdown(table_dir: Path) -> str:
    before_after = read_csv(table_dir / "main_before_after_results.csv")
    paired = read_csv(table_dir / "paired_sample_delta_summary.csv")
    after = read_csv(table_dir / "strict_transform_results_after_repair.csv")

    lines = [
        "# Verifier-Guided Repair Table Summary",
        "",
        "## Main Before/After",
        "",
        "| Setting | n | Base faith. | Final faith. | Delta | Base render | Final render |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in before_after:
        lines.append(
            f"| {row['experiment']} | {row['n']} | {row['baseline_faithfulness']} | "
            f"{row['final_faithfulness']} | {row['delta_faithfulness']} | "
            f"{row['baseline_render_ok_pct']} | {row['final_render_ok_pct']} |"
        )

    lines.extend(
        [
            "",
            "## Paired Outcomes",
            "",
            "| Setting | Improved | Unchanged | Degraded | Mean delta | Median delta |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        lines.append(
            f"| {row['experiment']} | {row['improved']} | {row['unchanged']} | "
            f"{row['degraded']} | {row['mean_delta']} | {row['median_delta']} |"
        )

    lines.extend(
        [
            "",
            "## Final Strict-Transform Audit",
            "",
            "| Setting | Faithfulness | Failure taxonomy |",
            "| --- | ---: | --- |",
        ]
    )
    for row in after:
        lines.append(f"| {row['setting']} | {row['faithfulness']} | {row['failure_taxonomy']} |")

    return "\n".join(lines) + "\n"
