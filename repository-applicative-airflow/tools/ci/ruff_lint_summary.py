"""
Parse a ruff JSON lint report and write a Markdown summary table
to $GITHUB_STEP_SUMMARY.

Usage:
    python tools/ci/ruff_lint_summary.py /tmp/ruff-lint.json
"""

from __future__ import annotations

import json
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_results(path: str) -> list[dict]:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Report file not found: %s", path)
        sys.exit(2)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON from %s: %s", path, e)
        sys.exit(2)


def group_by_file(results: list[dict]) -> dict[str, list[dict]]:
    by_file: dict[str, list[dict]] = {}
    for item in results:
        by_file.setdefault(item["filename"], []).append(item)
    return by_file


def write_summary(by_file: dict[str, list[dict]], summary_path: str) -> None:
    with open(summary_path, "a") as out:
        if not by_file:
            out.write("## ✅ Ruff Lint\n\nNo lint violations found.\n\n")
            return

        total_violations = sum(len(v) for v in by_file.values())
        total_files = len(by_file)

        out.write("## ❌ Ruff Lint Violations\n\n")
        out.write("| File | Violations | Rules |\n")
        out.write("| ---- | :--------: | ----- |\n")

        for filename, items in sorted(by_file.items()):
            rules = ", ".join(
                f"`{code}`"
                for code in sorted({i["code"] for i in items if i.get("code")})
            )
            out.write(f"| `{filename}` | {len(items)} | {rules} |\n")

        out.write(
            f"\n**{total_violations}** violation(s) across **{total_files}** file(s).\n\n"
        )


def main() -> None:
    if len(sys.argv) != 2:
        logger.error("Usage: ruff_lint_summary.py <ruff-lint.json>")
        sys.exit(2)

    report_path = sys.argv[1]

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        logger.error(
            "GITHUB_STEP_SUMMARY is not set — are you running outside of GitHub Actions?"
        )
        sys.exit(2)

    results = load_results(report_path)

    if not results:
        logger.info(
            "No lint violations found in %s — writing clean summary.", report_path
        )
        by_file = {}
    else:
        logger.info("Found results in %s — parsing violations.", report_path)
        by_file = group_by_file(results)

    write_summary(by_file, summary_path)

    if by_file:
        total = sum(len(v) for v in by_file.values())
        logger.warning("%d violation(s) across %d file(s).", total, len(by_file))
        sys.exit(1)

    logger.info("Ruff lint passed.")


if __name__ == "__main__":
    main()
