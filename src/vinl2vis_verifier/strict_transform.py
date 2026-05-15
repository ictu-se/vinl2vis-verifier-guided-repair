"""Strict transformation audit for generated NL2Vis artifacts."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .io import read_jsonl, write_csv
from .spec import has_aggregate, has_filter, has_sort


def extract_spec(output_row: dict[str, Any]) -> Any:
    response = output_row.get("response")
    if not isinstance(response, dict):
        return None
    return response.get("vega_lite_spec") or response.get("spec") or response.get("chart_spec")


def audit_rows(run_name: str, split_path: Path, outputs_path: Path) -> list[dict[str, object]]:
    samples = {row["sample_id"]: row for row in read_jsonl(split_path)}
    rows: list[dict[str, object]] = []
    for output in read_jsonl(outputs_path):
        sample = samples.get(output.get("sample_id"))
        if not sample:
            continue
        intent = sample.get("intent") if isinstance(sample.get("intent"), dict) else {}
        spec = extract_spec(output)
        nonempty_spec = isinstance(spec, dict) and bool(spec)
        issues: list[str] = []
        if nonempty_spec and intent.get("filters") and not has_filter(spec):
            issues.append("missing_filter_transform")
        if nonempty_spec and intent.get("sort") and not has_sort(spec):
            issues.append("missing_sort_transform")
        if nonempty_spec and intent.get("aggregation") and not has_aggregate(spec):
            issues.append("missing_aggregation_transform")
        rows.append(
            {
                "run": run_name,
                "sample_id": sample["sample_id"],
                "query_type": sample.get("query_type", ""),
                "chart_family": sample.get("chart_family", ""),
                "requires_filter": bool(intent.get("filters")),
                "requires_sort": bool(intent.get("sort")),
                "requires_aggregation": bool(intent.get("aggregation")),
                "has_filter": has_filter(spec),
                "has_sort": has_sort(spec),
                "has_aggregate": has_aggregate(spec),
                "issues": "|".join(issues),
            }
        )
    return rows


def summarize_issues(rows: list[dict[str, object]]) -> Counter[tuple[str, str]]:
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        run = str(row.get("run", ""))
        for issue in str(row.get("issues", "")).split("|"):
            if issue:
                counts[(run, issue)] += 1
    return counts


def write_audit_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "run",
        "sample_id",
        "query_type",
        "chart_family",
        "requires_filter",
        "requires_sort",
        "requires_aggregation",
        "has_filter",
        "has_sort",
        "has_aggregate",
        "issues",
    ]
    write_csv(path, rows, fieldnames)
