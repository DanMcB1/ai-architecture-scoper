"""CLI: generate a Statement of Work without opening the Streamlit UI.

Examples:
  python -m scoper --sample auto-dealer --out examples/auto-dealer-group.md
  python -m scoper --all-samples --outdir examples
  python -m scoper --ask "We want AI for claims intake" --industry insurance
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scoper.detect import build_profile
from scoper.engine import generate_sow
from scoper.render import render_markdown
from scoper.samples import SAMPLES, get_sample


def _build_from_args(args: argparse.Namespace):
    if args.sample:
        sample = get_sample(args.sample)
        profile = build_profile(
            ask=sample["ask"],
            industry=sample.get("industry", ""),
            data_sensitivity=sample.get("data_sensitivity", ""),
            team_size=sample.get("team_size", ""),
            existing_systems=sample.get("existing_systems", ""),
            customer_name=sample.get("customer_name", ""),
        )
    else:
        if not args.ask:
            raise SystemExit("Provide --ask or --sample (or --all-samples).")
        profile = build_profile(
            ask=args.ask,
            industry=args.industry or "",
            data_sensitivity=args.sensitivity or "",
            team_size=args.team_size or "",
            existing_systems=args.systems or "",
            customer_name=args.customer or "",
        )
    return generate_sow(profile, polish_summary=not args.no_llm)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a 4-week AI scoping Statement of Work (portfolio demo)."
    )
    parser.add_argument("--ask", help="Free-text customer ask")
    parser.add_argument("--sample", choices=sorted(SAMPLES), help="Use a built-in sample")
    parser.add_argument("--all-samples", action="store_true", help="Write all samples to --outdir")
    parser.add_argument("--outdir", default="examples", help="Directory for --all-samples")
    parser.add_argument("--out", help="Output Markdown path (default: stdout)")
    parser.add_argument("--customer", default="", help="Customer / project name")
    parser.add_argument("--industry", default="", help="Industry override")
    parser.add_argument("--sensitivity", default="", help="Data sensitivity override")
    parser.add_argument("--team-size", default="", dest="team_size")
    parser.add_argument("--systems", default="", help="Existing systems (comma-separated)")
    parser.add_argument("--no-llm", action="store_true", help="Skip optional LLM polish even if a key is set")
    parser.add_argument("--list-samples", action="store_true")
    args = parser.parse_args(argv)

    if args.list_samples:
        for key, sample in SAMPLES.items():
            print(f"{key}: {sample['title']}")
        return 0

    if args.all_samples:
        outdir = Path(args.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        mapping = {
            "auto-dealer": "auto-dealer-group.md",
            "regional-hospital": "regional-hospital.md",
            "mid-size-insurer": "mid-size-insurer.md",
        }
        for key, filename in mapping.items():
            sample = get_sample(key)
            profile = build_profile(
                ask=sample["ask"],
                industry=sample.get("industry", ""),
                data_sensitivity=sample.get("data_sensitivity", ""),
                team_size=sample.get("team_size", ""),
                existing_systems=sample.get("existing_systems", ""),
                customer_name=sample.get("customer_name", ""),
            )
            sow = generate_sow(profile, polish_summary=not args.no_llm)
            path = outdir / filename
            path.write_text(render_markdown(sow), encoding="utf-8")
            print(f"Wrote {path}")
        return 0

    sow = _build_from_args(args)
    markdown = render_markdown(sow)
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
        print(f"Wrote {path}")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
