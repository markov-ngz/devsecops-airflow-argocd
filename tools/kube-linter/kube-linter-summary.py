"""Parse kube-linter sarif output to produce a markdown table file with linting summary"""

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def extract_logical_location(logical_locations: list[dict], kind: str) -> str:
    return next(
        (loc.get("name", "") for loc in logical_locations if loc.get("kind") == kind),
        "",
    )


def parse_sarif(sarif_file_path: str) -> list[dict]:
    path = Path(sarif_file_path)
    if not path.exists():
        raise FileNotFoundError(f"SARIF file not found: {sarif_file_path}")

    with path.open("r", encoding="utf-8") as f:
        sarif = json.load(f)

    rows = []

    for run in sarif.get("runs", []):
        results = run.get("results", [])
        for result in results:
            rule_id = result.get("ruleId", "")
            message = result.get("message", {}).get("text", "").split("\n")[0].strip()

            for location in result.get("locations", []):
                physical = location.get("physicalLocation", {})
                file_path = physical.get("artifactLocation", {}).get("uri", "")

                logical_locations = location.get("logicalLocations", [])
                object_name = extract_logical_location(logical_locations, "Object Name")
                object_kind = extract_logical_location(logical_locations, "GVK/Kind")
                object_version = extract_logical_location(
                    logical_locations, "GVK/Version"
                )
                object_group = extract_logical_location(logical_locations, "GVK/Group")

                object_type = "/".join(
                    filter(None, [object_group, object_version, object_kind])
                )

                rows.append(
                    {
                        "file_path": file_path,
                        "object_name": object_name,
                        "object_type": object_type,
                        "rule_id": rule_id,
                        "message": message,
                    }
                )

    rows.sort(key=lambda r: r["file_path"])
    return rows


def generate_markdown_table(rows: list[dict]) -> str:
    headers = ["file_path", "object_name", "object_type", "rule_id", "message"]
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    lines = [
        "# Kube-Linter Summary\n",
        f"**Total issues found: {len(rows)}**\n",
        header_line,
        separator_line,
    ]

    for row in rows:
        cells = [row.get(h, "").replace("|", "\\|") for h in headers]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines) + "\n"


def generate_kube_linter_summary(sarif_file_path: str, output_file_path: str) -> None:
    """
    Produces a Markdown table file, with columns sorted by file:
    | file_path | object_name | object_type | rule_id | message |

    :param sarif_file_path: Path to the SARIF file produced by kube-linter
    :param output_file_path: Path to the output Markdown file
    """
    logger.info("Parsing SARIF file: %s", sarif_file_path)
    rows = parse_sarif(sarif_file_path)
    logger.info("Found %d linting result(s)", len(rows))

    markdown = generate_markdown_table(rows)

    output_path = Path(output_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(markdown)

    logger.info("Markdown summary written to: %s", output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse kube-linter SARIF output and generate a Markdown summary."
    )
    parser.add_argument(
        "--sarif-file", required=True, help="Path to the SARIF input file"
    )
    parser.add_argument(
        "--output-file", required=True, help="Path to the Markdown output file"
    )
    args = parser.parse_args()

    try:
        generate_kube_linter_summary(args.sarif_file, args.output_file)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse SARIF file as JSON: %s", str(e))
        sys.exit(1)
