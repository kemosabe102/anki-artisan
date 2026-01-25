#!/usr/bin/env python3
"""
Code duplication detection using Pylint.

Analyzes Python files for duplicate code blocks and calculates duplication metrics.
Outputs JSON with duplicate blocks and summary statistics.
"""

import shutil
import sys


def _check_pylint_installed() -> None:
    """Check if pylint is installed, exit with helpful message if not."""
    # Check both import and CLI availability
    try:
        import pylint  # noqa: F401
    except ImportError:
        pass  # Will check CLI below

    if shutil.which("pylint") is None:
        print("=" * 60, file=sys.stderr)
        print("ERROR: Missing required dependency: pylint", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print("Install with:", file=sys.stderr)
        print("  pip install pylint>=3.0", file=sys.stderr)
        print(file=sys.stderr)
        print("Or install all tech debt dependencies:", file=sys.stderr)
        print("  pip install radon>=6.0 gitpython>=3.1 pylint>=3.0", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        sys.exit(1)


_check_pylint_installed()

import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import TypedDict  # noqa: E402

# Remediation effort estimate: 30 minutes per duplicate block
REMEDIATION_MINUTES_PER_BLOCK = 30


@dataclass
class DuplicateBlock:
    """A detected duplicate code block."""

    files: list[str]  # Format: "file.py:line_number"
    lines: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "files": self.files,
            "lines": self.lines,
        }


class DuplicationSummary(TypedDict):
    """Summary statistics for duplication analysis."""

    total_blocks: int
    duplication_percent: float
    remediation_minutes: int


@dataclass
class DuplicationResult:
    """Complete duplication analysis result."""

    duplicate_blocks: list[DuplicateBlock]
    summary: DuplicationSummary

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "duplicate_blocks": [b.to_dict() for b in self.duplicate_blocks],
            "summary": dict(self.summary),
        }


def count_total_lines(repo_path: Path) -> int:
    """
    Count total lines of Python code in the repository.

    Args:
        repo_path: Path to repository or file

    Returns:
        Total number of lines
    """
    total_lines = 0

    if repo_path.is_file():
        python_files = [repo_path] if repo_path.suffix == ".py" else []
    else:
        python_files = list(repo_path.rglob("*.py"))

    for py_file in python_files:
        try:
            content = py_file.read_text(encoding="utf-8")
            total_lines += len(content.splitlines())
        except (OSError, UnicodeDecodeError):
            # Skip files that can't be read
            continue

    return total_lines


def run_pylint_duplication(repo_path: Path, min_lines: int) -> str | None:
    """
    Run Pylint duplicate-code checker and return JSON output.

    Args:
        repo_path: Path to repository or file
        min_lines: Minimum lines for duplication detection

    Returns:
        Pylint JSON output or None if error
    """
    cmd = [
        sys.executable,
        "-m",
        "pylint",
        "--disable=all",
        "--enable=duplicate-code",
        f"--min-similarity-lines={min_lines}",
        "--output-format=json",
        str(repo_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        # Pylint returns non-zero exit codes for issues found, which is expected
        return result.stdout
    except subprocess.TimeoutExpired:
        print("Error: Pylint timed out after 5 minutes", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: Pylint not found. Run: uv add pylint", file=sys.stderr)
        return None


def parse_pylint_output(pylint_json: str) -> list[DuplicateBlock]:
    """
    Parse Pylint JSON output to extract duplicate blocks.

    Pylint duplicate-code format:
    {
        "type": "convention",
        "module": "module_name",
        "obj": "",
        "line": 10,
        "column": 0,
        "path": "path/to/file.py",
        "symbol": "duplicate-code",
        "message": "Similar lines in 2 files..."
    }

    Args:
        pylint_json: Raw JSON string from Pylint

    Returns:
        List of DuplicateBlock objects
    """
    if not pylint_json or not pylint_json.strip():
        return []

    try:
        messages = json.loads(pylint_json)
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse Pylint JSON output: {e}", file=sys.stderr)
        return []

    duplicate_blocks: list[DuplicateBlock] = []

    for msg in messages:
        if msg.get("symbol") != "duplicate-code":
            continue

        message_text = msg.get("message", "")
        path = msg.get("path", "")
        line = msg.get("line", 0)

        # Parse the message to extract line count and file references
        # Format: "Similar lines in N files" or "Duplicate code found..."
        files: list[str] = []
        lines_count = 0

        # Add the current file location
        if path and line:
            files.append(f"{path}:{line}")

        # Try to extract line count from message
        # Message format varies but often contains "N lines"
        lines_match = re.search(r"(\d+)\s+lines?", message_text)
        if lines_match:
            lines_count = int(lines_match.group(1))

        # Look for other file references in the message
        file_matches = re.findall(r"([^\s:]+\.py):(\d+)", message_text)
        for file_path, file_line in file_matches:
            loc = f"{file_path}:{file_line}"
            if loc not in files:
                files.append(loc)

        if files and lines_count > 0:
            duplicate_blocks.append(
                DuplicateBlock(
                    files=files,
                    lines=lines_count,
                )
            )

    return duplicate_blocks


def detect_duplication(
    repo_path: Path,
    min_lines: int = 4,
) -> DuplicationResult:
    """
    Detect code duplication in a repository.

    Args:
        repo_path: Path to repository or file
        min_lines: Minimum lines to consider as duplication (default: 4)

    Returns:
        DuplicationResult with duplicate blocks and summary
    """
    # Run Pylint duplication check
    pylint_output = run_pylint_duplication(repo_path, min_lines)

    if pylint_output is None:
        # Error already reported, return empty result
        return DuplicationResult(
            duplicate_blocks=[],
            summary={
                "total_blocks": 0,
                "duplication_percent": 0.0,
                "remediation_minutes": 0,
            },
        )

    # Parse results
    duplicate_blocks = parse_pylint_output(pylint_output)

    # Calculate summary statistics
    total_blocks = len(duplicate_blocks)
    total_duplicate_lines = sum(block.lines for block in duplicate_blocks)
    total_lines = count_total_lines(repo_path)

    # Calculate duplication percentage
    if total_lines > 0:
        duplication_percent = round((total_duplicate_lines / total_lines) * 100, 1)
    else:
        duplication_percent = 0.0

    # Calculate remediation effort (30 minutes per block)
    remediation_minutes = total_blocks * REMEDIATION_MINUTES_PER_BLOCK

    return DuplicationResult(
        duplicate_blocks=duplicate_blocks,
        summary={
            "total_blocks": total_blocks,
            "duplication_percent": duplication_percent,
            "remediation_minutes": remediation_minutes,
        },
    )


def main() -> None:
    """CLI entry point for duplication detection."""
    parser = argparse.ArgumentParser(
        description="Detect code duplication in Python files using Pylint.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Duplication Thresholds (from FORMULAS-OBSERVE.md):
  0-3%   Acceptable - Normal code reuse
  3-5%   Monitor - Review for extraction opportunities
  5-10%  Technical Debt - Plan refactoring
  >10%   Critical - Immediate refactoring required

Remediation estimate: 30 minutes per duplicate block
        """,
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        required=True,
        help="Path to repository or file to analyze",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        help="Output file path for JSON results (default: stdout)",
    )
    parser.add_argument(
        "--min-lines",
        type=int,
        default=4,
        help="Minimum lines to consider as duplication (default: 4)",
    )

    args = parser.parse_args()

    # Validate repo path exists
    if not args.repo_path.exists():
        print(f"Error: Path does not exist: {args.repo_path}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    result = detect_duplication(args.repo_path, args.min_lines)

    # Output results
    output_json = json.dumps(result.to_dict(), indent=2)

    if args.output_file:
        try:
            args.output_file.write_text(output_json, encoding="utf-8")
            print(f"Results written to {args.output_file}")
        except OSError as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
