#!/usr/bin/env python3
"""Calculate Technical Debt Ratio (TDR) using SQALE methodology.

Reads complexity and duplication analysis outputs from OBSERVE phase,
calculates remediation effort, and assigns SQALE grades A-E.

Usage:
    python calculate_tdr.py --complexity-file complexity.json \
                            --duplication-file duplication.json \
                            --loc 10000 \
                            --output-file tdr_results.json

Effort Estimates (per FORMULAS-ORIENT.md):
    - Complexity (CC>15): 45 min/function
    - Duplication: 30 min/block
    - Missing tests: 20 min/uncovered branch (optional)

Formula:
    TDR = (remediation_hours / development_hours) x 100
    development_hours = LOC / 10 (industry standard)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

# Effort estimates in minutes (from FORMULAS-ORIENT.md)
EFFORT_COMPLEXITY_MINUTES = 45  # per function with CC > 15
EFFORT_DUPLICATION_MINUTES = 30  # per duplication block
EFFORT_MISSING_TESTS_MINUTES = 20  # per uncovered branch

# Development productivity constant
LOC_PER_HOUR = 10  # Industry standard: 10 LOC per hour

# SQALE grade thresholds (TDR percentages)
GRADE_THRESHOLDS = {
    "A": 5.0,  # TDR < 5%
    "B": 10.0,  # TDR < 10%
    "C": 20.0,  # TDR < 20%
    "D": 50.0,  # TDR < 50%
    "E": float("inf"),  # TDR >= 50%
}


class BreakdownResult(TypedDict):
    """Breakdown of remediation minutes by category."""

    complexity_minutes: int
    duplication_minutes: int
    missing_tests_minutes: int
    total_minutes: int


class TDRResult(TypedDict):
    """Complete TDR calculation result."""

    tdr_percent: float
    grade: str
    remediation_hours: float
    development_hours: float
    breakdown: BreakdownResult


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON content as dictionary.

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If file is not valid JSON.
    """
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def count_complex_functions(complexity_data: dict) -> int:
    """Count functions with cyclomatic complexity > 15.

    Args:
        complexity_data: Parsed complexity.json from OBSERVE phase.
            Expected format: {"functions": [{"name": str, "complexity": int}, ...]}
            or {"files": [{"functions": [...]}]}

    Returns:
        Number of functions exceeding complexity threshold.
    """
    count = 0
    threshold = 15

    # Handle flat function list format
    if "functions" in complexity_data:
        for func in complexity_data["functions"]:
            if func.get("complexity", 0) > threshold:
                count += 1

    # Handle nested file->functions format
    elif "files" in complexity_data:
        for file_entry in complexity_data["files"]:
            for func in file_entry.get("functions", []):
                if func.get("complexity", 0) > threshold:
                    count += 1

    return count


def count_duplication_blocks(duplication_data: dict) -> int:
    """Count duplication blocks from OBSERVE phase output.

    Args:
        duplication_data: Parsed duplication.json from OBSERVE phase.
            Expected format: {"blocks": [...]} or {"duplications": [...]}

    Returns:
        Number of duplication blocks found.
    """
    if "blocks" in duplication_data:
        return len(duplication_data["blocks"])
    if "duplications" in duplication_data:
        return len(duplication_data["duplications"])
    if "total_blocks" in duplication_data:
        return duplication_data["total_blocks"]
    return 0


def count_uncovered_branches(coverage_data: dict | None) -> int:
    """Count uncovered branches from optional coverage data.

    Args:
        coverage_data: Optional coverage.json from OBSERVE phase.
            Expected format: {"uncovered_branches": int} or {"branches": {"missed": int}}

    Returns:
        Number of uncovered branches, or 0 if no data.
    """
    if coverage_data is None:
        return 0

    if "uncovered_branches" in coverage_data:
        return coverage_data["uncovered_branches"]
    if "branches" in coverage_data:
        return coverage_data["branches"].get("missed", 0)
    return 0


def assign_grade(tdr_percent: float) -> str:
    """Assign SQALE grade based on TDR percentage.

    Args:
        tdr_percent: Technical Debt Ratio as percentage.

    Returns:
        Grade letter A-E.
    """
    if tdr_percent < GRADE_THRESHOLDS["A"]:
        return "A"
    if tdr_percent < GRADE_THRESHOLDS["B"]:
        return "B"
    if tdr_percent < GRADE_THRESHOLDS["C"]:
        return "C"
    if tdr_percent < GRADE_THRESHOLDS["D"]:
        return "D"
    return "E"


def calculate_tdr(
    complexity_file: Path | None,
    duplication_file: Path | None,
    loc: int,
    coverage_file: Path | None = None,
) -> TDRResult:
    """Calculate Technical Debt Ratio and assign SQALE grade.

    Args:
        complexity_file: Path to complexity.json from OBSERVE phase.
        duplication_file: Path to duplication.json from OBSERVE phase.
        loc: Lines of code in the codebase.
        coverage_file: Optional path to coverage.json for test coverage data.

    Returns:
        TDRResult with TDR percentage, grade, and breakdown.
    """
    # Load input files
    complexity_data = load_json_file(complexity_file) if complexity_file else {}
    duplication_data = load_json_file(duplication_file) if duplication_file else {}
    coverage_data = load_json_file(coverage_file) if coverage_file else None

    # Count issues
    complex_functions = count_complex_functions(complexity_data)
    duplication_blocks = count_duplication_blocks(duplication_data)
    uncovered_branches = count_uncovered_branches(coverage_data)

    # Calculate remediation minutes
    complexity_minutes = complex_functions * EFFORT_COMPLEXITY_MINUTES
    duplication_minutes = duplication_blocks * EFFORT_DUPLICATION_MINUTES
    missing_tests_minutes = uncovered_branches * EFFORT_MISSING_TESTS_MINUTES
    total_minutes = complexity_minutes + duplication_minutes + missing_tests_minutes

    # Convert to hours
    remediation_hours = total_minutes / 60.0
    development_hours = loc / LOC_PER_HOUR

    # Calculate TDR
    if development_hours > 0:
        tdr_percent = (remediation_hours / development_hours) * 100
    else:
        tdr_percent = 0.0

    # Assign grade
    grade = assign_grade(tdr_percent)

    return TDRResult(
        tdr_percent=round(tdr_percent, 2),
        grade=grade,
        remediation_hours=round(remediation_hours, 2),
        development_hours=round(development_hours, 2),
        breakdown=BreakdownResult(
            complexity_minutes=complexity_minutes,
            duplication_minutes=duplication_minutes,
            missing_tests_minutes=missing_tests_minutes,
            total_minutes=total_minutes,
        ),
    )


def write_output(result: TDRResult, output_file: Path) -> None:
    """Write TDR result to JSON file.

    Args:
        result: TDR calculation result.
        output_file: Path to output JSON file.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dict(result), f, indent=2)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Calculate Technical Debt Ratio using SQALE methodology.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--complexity-file",
        type=Path,
        help="Path to complexity.json from OBSERVE phase",
    )
    parser.add_argument(
        "--duplication-file",
        type=Path,
        help="Path to duplication.json from OBSERVE phase",
    )
    parser.add_argument(
        "--coverage-file",
        type=Path,
        help="Optional path to coverage.json for test coverage data",
    )
    parser.add_argument(
        "--loc",
        type=int,
        required=True,
        help="Lines of code in the codebase",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to output JSON file for TDR results",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for TDR calculation.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args()

    try:
        result = calculate_tdr(
            complexity_file=args.complexity_file,
            duplication_file=args.duplication_file,
            loc=args.loc,
            coverage_file=args.coverage_file,
        )
        write_output(result, args.output_file)

        # Print summary to stdout
        print(f"TDR: {result['tdr_percent']}%")
        print(f"Grade: {result['grade']}")
        print(f"Remediation: {result['remediation_hours']} hours")
        print(f"Output written to: {args.output_file}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
