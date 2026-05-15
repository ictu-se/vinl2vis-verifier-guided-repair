"""Command line interface for the verifier-guided repair release."""

from __future__ import annotations

import json
from pathlib import Path

import click

from .io import write_text
from .strict_transform import audit_rows, summarize_issues, write_audit_csv
from .table_checks import summary_markdown, validate_tables


@click.group()
def main() -> None:
    """Utilities for verifier-guided NL2Vis repair artifacts."""


@main.command("validate-tables")
@click.option("--tables", "table_dir", type=click.Path(path_type=Path), default=Path("data/tables"))
def validate_tables_cmd(table_dir: Path) -> None:
    """Check internal consistency of released CSV tables."""
    errors = validate_tables(table_dir)
    if errors:
        for error in errors:
            click.echo(f"ERROR: {error}", err=True)
        raise SystemExit(1)
    click.echo(f"OK: validated tables in {table_dir}")


@main.command("summarize")
@click.option("--tables", "table_dir", type=click.Path(path_type=Path), default=Path("data/tables"))
@click.option("--out", "out_path", type=click.Path(path_type=Path), default=Path("reports/TABLE_SUMMARY.md"))
def summarize_cmd(table_dir: Path, out_path: Path) -> None:
    """Write a compact Markdown summary from the released tables."""
    write_text(out_path, summary_markdown(table_dir))
    click.echo(f"Wrote {out_path}")


@main.command("strict-audit")
@click.option("--name", "run_name", required=True, help="Run label used in the output CSV.")
@click.option("--split", "split_path", type=click.Path(path_type=Path, exists=True), required=True)
@click.option("--outputs", "outputs_path", type=click.Path(path_type=Path, exists=True), required=True)
@click.option("--out", "out_path", type=click.Path(path_type=Path), default=Path("results/strict_audit.csv"))
def strict_audit_cmd(run_name: str, split_path: Path, outputs_path: Path, out_path: Path) -> None:
    """Audit missing explicit filter/sort/aggregation commitments in one output JSONL."""
    rows = audit_rows(run_name, split_path, outputs_path)
    write_audit_csv(out_path, rows)
    counts = {f"{run}::{issue}": count for (run, issue), count in summarize_issues(rows).items()}
    click.echo(json.dumps({"rows": len(rows), "issue_counts": counts}, indent=2))


if __name__ == "__main__":
    main()
