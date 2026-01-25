#!/usr/bin/env python
"""Calculate weighted hotspot scores from complexity and churn data.

Combines complexity.json and churn.json from OBSERVE phase to calculate
hotspot scores using the weighted formula:
    (CC_norm x 0.4) + (churn_norm x 0.3) + (coupling_norm x 0.3)

Usage:
    uv run python calculate_hotspots.py --complexity-file complexity.json --churn-file churn.json --output-file hotspots.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# Normalization constants from FORMULAS-ORIENT.md
CC_NORMALIZATION_DIVISOR = 25
CHURN_NORMALIZATION_DIVISOR = 30
COUPLING_NORMALIZATION_DIVISOR = 10


# Hotspot weights from FORMULAS-ORIENT.md
WEIGHT_CC = 0.4
WEIGHT_CHURN = 0.3
WEIGHT_COUPLING = 0.3

# Classification thresholds
THRESHOLD_CRITICAL = 0.7
THRESHOLD_HIGH = 0.5
THRESHOLD_MEDIUM = 0.3


@dataclass
class HotspotEntry:
    """A single file's hotspot score and components."""

    file: str
    score: float
    level: str
    cc_norm: float
    churn_norm: float
    coupling_norm: float


@dataclass
class HotspotSummary:
    """Summary of hotspot analysis."""

    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    total_files: int


@dataclass
class HotspotResult:
    """Complete result of hotspot calculation."""

    hotspots: list[HotspotEntry]
    summary: HotspotSummary


def classify_hotspot(score: float) -> str:
    """Classify a hotspot score into risk level.

    Args:
        score: Normalized hotspot score (0.0-1.0).

    Returns:
        Risk level: CRITICAL, HIGH, MEDIUM, or LOW.
    """
    if score >= THRESHOLD_CRITICAL:
        return "CRITICAL"
    elif score >= THRESHOLD_HIGH:
        return "HIGH"
    elif score >= THRESHOLD_MEDIUM:
        return "MEDIUM"
    else:
        return "LOW"


def normalize_value(value: float, divisor: float) -> float:
    """Normalize a value to 0.0-1.0 scale.

    Args:
        value: Raw metric value.
        divisor: Normalization divisor (max expected value).

    Returns:
        Normalized value capped at 1.0.
    """
    return min(value / divisor, 1.0) if divisor > 0 else 0.0


def load_json_file(file_path: Path) -> dict[str, Any]:
    """Load and parse a JSON file.

    Args:
        file_path: Path to JSON file.

    Returns:
        Parsed JSON data.

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If file is not valid JSON.
    """
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def extract_complexity_by_file(complexity_data: dict[str, Any]) -> dict[str, float]:
    """Extract max cyclomatic complexity per file from complexity data.

    Supports multiple input formats:
    - {"complexity_findings": [{"file": ..., "cc": ...}]}
    - {"files": [{"path": ..., "complexity": ...}]}
    - Direct list of findings

    Args:
        complexity_data: Complexity JSON data.

    Returns:
        Dict mapping file path to max cyclomatic complexity.
    """
    file_cc: dict[str, float] = {}

    # Try different possible structures
    findings = []
    if "complexity_findings" in complexity_data:
        findings = complexity_data["complexity_findings"]
    elif "files" in complexity_data:
        findings = complexity_data["files"]
    elif isinstance(complexity_data, list):
        findings = complexity_data

    for finding in findings:
        # Support both "file" and "path" keys
        file_path = finding.get("file") or finding.get("path", "")
        # Support both "cc" and "complexity" keys
        cc = finding.get("cc") or finding.get("complexity", 0)

        if file_path:
            # Keep max CC per file (handles multiple functions per file)
            file_cc[file_path] = max(file_cc.get(file_path, 0), float(cc))

    return file_cc


def extract_churn_by_file(churn_data: dict[str, Any]) -> dict[str, int]:
    """Extract commit count per file from churn data.

    Args:
        churn_data: Churn JSON data from git_churn.py.

    Returns:
        Dict mapping file path to commit count.
    """
    file_commits: dict[str, int] = {}

    # Try different possible structures
    files = []
    if "files" in churn_data:
        files = churn_data["files"]
    elif "churn_files" in churn_data:
        files = churn_data["churn_files"]
    elif isinstance(churn_data, list):
        files = churn_data

    for file_entry in files:
        file_path = file_entry.get("path") or file_entry.get("file", "")
        commits = file_entry.get("commits", 0)

        if file_path:
            file_commits[file_path] = int(commits)

    return file_commits


def extract_coupling_by_file(complexity_data: dict[str, Any]) -> dict[str, int]:
    """Extract coupling/dependency count per file.

    Coupling data may be embedded in complexity data or separate.

    Args:
        complexity_data: Complexity JSON data (may contain coupling).

    Returns:
        Dict mapping file path to external dependency count.
    """
    file_coupling: dict[str, int] = {}

    # Check for coupling data in various locations
    coupling_entries = []
    if "coupling" in complexity_data:
        coupling_entries = complexity_data["coupling"]
    elif "dependencies" in complexity_data:
        coupling_entries = complexity_data["dependencies"]

    for entry in coupling_entries:
        file_path = entry.get("file") or entry.get("path", "")
        deps = entry.get("external_deps") or entry.get("dependencies", 0)

        if file_path:
            file_coupling[file_path] = int(deps)

    return file_coupling


def calculate_hotspots(
    complexity_file: str | Path,
    churn_file: str | Path,
    output_file: str | Path | None = None,
) -> HotspotResult:
    """Calculate weighted hotspot scores from complexity and churn data.

    Formula: (CC_norm x 0.4) + (churn_norm x 0.3) + (coupling_norm x 0.3)

    Args:
        complexity_file: Path to complexity JSON from OBSERVE phase.
        churn_file: Path to churn JSON from git_churn.py.
        output_file: Optional path to write results JSON.

    Returns:
        HotspotResult with scored files and summary.

    Raises:
        FileNotFoundError: If input files do not exist.
        json.JSONDecodeError: If input files are not valid JSON.
    """
    # Load input data
    complexity_data = load_json_file(Path(complexity_file))
    churn_data = load_json_file(Path(churn_file))

    # Extract metrics by file
    file_cc = extract_complexity_by_file(complexity_data)
    file_churn = extract_churn_by_file(churn_data)
    file_coupling = extract_coupling_by_file(complexity_data)

    # Get union of all files
    all_files = set(file_cc.keys()) | set(file_churn.keys())

    # Calculate hotspot scores
    hotspots: list[HotspotEntry] = []
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for file_path in all_files:
        # Get raw values (default to 0 if not present)
        cc = file_cc.get(file_path, 0)
        churn = file_churn.get(file_path, 0)
        coupling = file_coupling.get(file_path, 0)

        # Normalize values
        cc_norm = normalize_value(cc, CC_NORMALIZATION_DIVISOR)
        churn_norm = normalize_value(churn, CHURN_NORMALIZATION_DIVISOR)
        coupling_norm = normalize_value(coupling, COUPLING_NORMALIZATION_DIVISOR)

        # Calculate weighted score
        score = (
            (cc_norm * WEIGHT_CC)
            + (churn_norm * WEIGHT_CHURN)
            + (coupling_norm * WEIGHT_COUPLING)
        )

        # Classify risk level
        level = classify_hotspot(score)
        counts[level] += 1

        hotspots.append(
            HotspotEntry(
                file=file_path,
                score=round(score, 4),
                level=level,
                cc_norm=round(cc_norm, 4),
                churn_norm=round(churn_norm, 4),
                coupling_norm=round(coupling_norm, 4),
            )
        )

    # Sort by score descending
    hotspots.sort(key=lambda h: h.score, reverse=True)

    result = HotspotResult(
        hotspots=hotspots,
        summary=HotspotSummary(
            critical_count=counts["CRITICAL"],
            high_count=counts["HIGH"],
            medium_count=counts["MEDIUM"],
            low_count=counts["LOW"],
            total_files=len(hotspots),
        ),
    )

    # Write output if path provided
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_to_dict(result), f, indent=2)

    return result


def result_to_dict(result: HotspotResult) -> dict[str, Any]:
    """Convert HotspotResult to JSON-serializable dictionary."""
    return {
        "hotspots": [asdict(h) for h in result.hotspots],
        "summary": asdict(result.summary),
    }


def main() -> int:
    """CLI entry point for hotspot calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate weighted hotspot scores from complexity and churn data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python calculate_hotspots.py --complexity-file complexity.json --churn-file churn.json --output-file hotspots.json

Formula:
    hotspot_score = (CC_norm x 0.4) + (churn_norm x 0.3) + (coupling_norm x 0.3)

Classification:
    CRITICAL: >= 0.7
    HIGH:     0.5 - 0.7
    MEDIUM:   0.3 - 0.5
    LOW:      < 0.3
        """,
    )
    parser.add_argument(
        "--complexity-file",
        type=str,
        required=True,
        help="Path to complexity JSON from OBSERVE phase",
    )
    parser.add_argument(
        "--churn-file",
        type=str,
        required=True,
        help="Path to churn JSON from git_churn.py",
    )

    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Path for output JSON file",
    )

    args = parser.parse_args()

    try:
        result = calculate_hotspots(
            complexity_file=args.complexity_file,
            churn_file=args.churn_file,
            output_file=args.output_file,
        )

        print(f"Hotspot analysis written to: {args.output_file}")
        print(f"  Total files: {result.summary.total_files}")
        print(f"  CRITICAL: {result.summary.critical_count}")
        print(f"  HIGH: {result.summary.high_count}")
        print(f"  MEDIUM: {result.summary.medium_count}")
        print(f"  LOW: {result.summary.low_count}")

        if result.hotspots:
            print("\nTop 5 hotspots:")
            for entry in result.hotspots[:5]:
                print(f"  {entry.level}: {entry.file} (score: {entry.score})")

        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
