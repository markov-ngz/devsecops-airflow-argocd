"""
Parse a ruff format --diff output and write a Markdown summary
to $GITHUB_STEP_SUMMARY.

Usage:
    python tools/ci/ruff_format_summary.py /tmp/ruff-format.diff
"""

from __future__ import annotations

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_diff(path: str) -> str:
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("Diff file not found: %s", path)
        sys.exit(2)


def extract_filenames(diff: str) -> list[str]:
    """
    Extract filenames from unified diff '+++ ' header lines.

    Ruff format --diff produces standard unified diff headers:
        --- a/path/to/file.py
        +++ b/path/to/file.py
    We strip the 'b/' prefix that ruff may prepend.
    """
    return [
        line.removeprefix("+++ ").removeprefix("b/")
        for line in diff.splitlines()
        if line.startswith("+++ ")
    ]


def write_summary(diff: str, filenames: list[str], summary_path: str) -> None:
    with open(summary_path, "a") as out:
        if not diff:
            out.write("## ✅ Ruff Format\n\nAll files are correctly formatted.\n\n")
            return

        out.write("## ❌ Ruff Format Violations\n\n")
        out.write("The following file(s) are not correctly formatted.\n")
        out.write(
            "Run `ruff format ./airflow-cicd/` locally (or let pre-commit handle it).\n\n"
        )

        out.write("| File |\n")
        out.write("| ---- |\n")
        out.writelines(f"| `{filename}` |\n" for filename in filenames)

        out.write(
            f"\n<details><summary>Show full diff ({len(filenames)} file(s))</summary>\n\n"
            f"```diff\n{diff}\n```\n\n</details>\n\n"
        )


def main() -> None:
    if len(sys.argv) != 2:
        logger.error("Usage: ruff_format_summary.py <ruff-format.diff>")
        sys.exit(2)

    diff_path = sys.argv[1]

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        logger.error(
            "GITHUB_STEP_SUMMARY is not set — are you running outside of GitHub Actions?"
        )
        sys.exit(2)

    diff = load_diff(diff_path)

    if not diff:
        logger.info(
            "No formatting diff found in %s — writing clean summary.", diff_path
        )
        write_summary("", [], summary_path)
        logger.info("Ruff format passed.")
        return

    filenames = extract_filenames(diff)
    logger.warning("%d file(s) have formatting issues.", len(filenames))

    write_summary(diff, filenames, summary_path)
    sys.exit(1)


if __name__ == "__main__":
    main()
