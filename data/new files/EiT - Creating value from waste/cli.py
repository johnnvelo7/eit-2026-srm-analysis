#!/usr/bin/env python3
"""CLI tool for managing SRM company assessments via OpenAI Codex."""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "prompts" / "base_v2.md"
SCHEMA = ROOT / "prompts" / "schema_v2.json"
COMPANIES_DIR = ROOT / "companies"


def slugify(name: str) -> str:
    """Turn a company name into a filesystem-safe folder name."""
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9æøå]+", "_", slug)
    slug = slug.strip("_")
    return slug


def cmd_prepare(args):
    """Read a CSV of company names and create a folder + prompt for each."""
    template_text = TEMPLATE.read_text(encoding="utf-8")
    csv_path = Path(args.csv)

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    COMPANIES_DIR.mkdir(exist_ok=True)

    created = 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue
            name = row[0].strip()
            slug = slugify(name)
            folder = COMPANIES_DIR / slug
            folder.mkdir(exist_ok=True)

            prompt_text = template_text.replace("{{COMPANY NAME}}", name)
            prompt_path = folder / "prompt.md"
            prompt_path.write_text(prompt_text, encoding="utf-8")
            created += 1
            print(f"  Created: {folder.relative_to(ROOT)}")

    print(f"\nPrepared {created} companies in {COMPANIES_DIR.relative_to(ROOT)}/")


def cmd_run(args):
    """Run the Codex assessment for a single company."""
    slug = slugify(args.company)
    folder = COMPANIES_DIR / slug

    prompt_path = folder / "prompt.md"
    if not prompt_path.exists():
        answer = input(
            f"Company '{args.company}' is not prepared yet. "
            f"Prepare and run? [y/N] "
        ).strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            sys.exit(0)

        # Prepare the company folder and prompt
        template_text = TEMPLATE.read_text(encoding="utf-8")
        folder.mkdir(parents=True, exist_ok=True)
        prompt_text = template_text.replace("{{COMPANY NAME}}", args.company)
        prompt_path.write_text(prompt_text, encoding="utf-8")
        print(f"  Prepared: {folder.relative_to(ROOT)}")

    output_json = folder / "output.json"
    events_jsonl = folder / "events.jsonl"

    # Build the command
    # Get-Content .\<folder>\prompt.md -Raw | codex exec ... > events.jsonl
    # We use PowerShell via subprocess for the pipeline
    ps_command = (
        f"Get-Content '{prompt_path}' -Raw"
        f" | codex exec --skip-git-repo-check"
        f" --output-last-message '{output_json}'"
        f" --output-schema '{SCHEMA}'"
        f" --json -"
        f" > '{events_jsonl}'"
    )

    print(f"Running Codex for: {args.company}")
    print(f"  Folder : {folder.relative_to(ROOT)}")
    print(f"  Output : {output_json.relative_to(ROOT)}")
    print(f"  Events : {events_jsonl.relative_to(ROOT)}")
    print()

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_command],
        cwd=str(ROOT),
    )

    if result.returncode != 0:
        print(f"\nCodex exited with code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)

    print(f"\nDone. Results in {folder.relative_to(ROOT)}/")


def _run_single(company_name: str) -> tuple[str, bool, str]:
    """Run Codex for one company. Returns (name, success, message).

    This is a thread-safe helper that does not call sys.exit.
    """
    slug = slugify(company_name)
    folder = COMPANIES_DIR / slug
    prompt_path = folder / "prompt.md"

    if not prompt_path.exists():
        return (company_name, False, "Not prepared – skipping")

    output_json = folder / "output.json"
    events_jsonl = folder / "events.jsonl"

    ps_command = (
        f"Get-Content '{prompt_path}' -Raw"
        f" | codex exec --skip-git-repo-check"
        f" --output-last-message '{output_json}'"
        f" --output-schema '{SCHEMA}'"
        f" --json -"
        f" > '{events_jsonl}'"
    )

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_command],
        cwd=str(ROOT),
        capture_output=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.decode(errors="replace").strip()
        return (company_name, False, f"Exit code {result.returncode}: {stderr}")

    return (company_name, True, f"Done → {folder.relative_to(ROOT)}/")


DEFAULT_WORKERS = 10
AGGREGATED_PATH = ROOT / "aggregated.json"


def cmd_aggregate(args):
    """Merge all companies/*/output.json into a single aggregated.json."""
    if not COMPANIES_DIR.exists():
        print("No companies directory found. Run 'prepare' first.", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else AGGREGATED_PATH
    results = []
    skipped = []

    for folder in sorted(COMPANIES_DIR.iterdir()):
        if not folder.is_dir():
            continue
        output_file = folder / "output.json"
        if not output_file.exists():
            skipped.append(folder.name)
            continue
        try:
            data = json.loads(output_file.read_text(encoding="utf-8"))
            results.append(data)
        except json.JSONDecodeError as exc:
            print(f"  Warning: Could not parse {output_file.relative_to(ROOT)}: {exc}", file=sys.stderr)
            skipped.append(folder.name)

    aggregated = {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "total": len(results),
        "companies": results,
    }

    output_path.write_text(json.dumps(aggregated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Aggregated {len(results)} companies → {output_path.relative_to(ROOT)}")
    if skipped:
        print(f"Skipped {len(skipped)} folders with no output: {', '.join(skipped)}")


def cmd_run_all(args):
    """Run Codex for all prepared companies (parallel, 10 workers)."""
    if not COMPANIES_DIR.exists():
        print("No companies directory found. Run 'prepare' first.", file=sys.stderr)
        sys.exit(1)

    folders = sorted(
        p for p in COMPANIES_DIR.iterdir()
        if p.is_dir() and (p / "prompt.md").exists()
    )

    if not folders:
        print("No prepared companies found.", file=sys.stderr)
        sys.exit(1)

    skip_existing = not args.force

    # Build list of company names to run
    to_run: list[str] = []
    for folder in folders:
        if skip_existing and (folder / "output.json").exists():
            print(f"  Skipping {folder.name} (output exists)")
            continue
        prompt_text = (folder / "prompt.md").read_text(encoding="utf-8")
        match = re.search(r"Company name:\s*\n(.+)", prompt_text)
        to_run.append(match.group(1).strip() if match else folder.name)

    if not to_run:
        print("Nothing to run – all companies already have output.")
        return

    workers = args.workers
    total = len(to_run)
    print(f"\nRunning {total} companies with {workers} parallel workers…\n")

    succeeded = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_run_single, name): name for name in to_run}
        for future in as_completed(futures):
            name, ok, msg = future.result()
            status = "✓" if ok else "✗"
            idx = succeeded + failed + 1
            print(f"[{idx}/{total}] {status} {name}: {msg}")
            if ok:
                succeeded += 1
            else:
                failed += 1

    print(f"\nFinished: {succeeded} succeeded, {failed} failed out of {total}.")


def main():
    parser = argparse.ArgumentParser(
        description="SRM Company Assessment CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- prepare --
    p_prepare = sub.add_parser(
        "prepare",
        help="Create company folders and prompts from a CSV file",
    )
    p_prepare.add_argument(
        "csv",
        help="Path to a CSV file with company names (one per row, first column)",
    )

    # -- run --
    p_run = sub.add_parser(
        "run",
        help="Run Codex assessment for a single company",
    )
    p_run.add_argument(
        "company",
        help="Company name (must match a prepared folder)",
    )

    # -- aggregate --
    p_aggregate = sub.add_parser(
        "aggregate",
        help="Merge all output.json files into a single aggregated.json",
    )
    p_aggregate.add_argument(
        "--output",
        default=None,
        help=f"Output path (default: {AGGREGATED_PATH.name})",
    )

    # -- run-all --
    p_run_all = sub.add_parser(
        "run-all",
        help="Run Codex for all prepared companies",
    )
    p_run_all.add_argument(
        "--force",
        action="store_true",
        help="Re-run even if output.json already exists",
    )
    p_run_all.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of parallel workers (default: {DEFAULT_WORKERS})",
    )

    args = parser.parse_args()

    if args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "run-all":
        cmd_run_all(args)
    elif args.command == "aggregate":
        cmd_aggregate(args)


if __name__ == "__main__":
    main()
