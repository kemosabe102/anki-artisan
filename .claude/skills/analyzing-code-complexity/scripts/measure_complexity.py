#!/usr/bin/env python3
"""
Cyclomatic complexity analysis using Radon.

Analyzes Python files for cyclomatic complexity and classifies risk levels.
Outputs JSON with per-function complexity and summary statistics.
"""

import sys


def _check_radon_installed() -> None:
    """Check if radon is installed, exit with helpful message if not."""
    try:
        import radon  # noqa: F401
    except ImportError:
        print("=" * 60, file=sys.stderr)
        print("ERROR: Missing required dependency: radon", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print("Install with:", file=sys.stderr)
        print("  pip install radon>=6.0", file=sys.stderr)
        print(file=sys.stderr)
        print("Or install all tech debt dependencies:", file=sys.stderr)
        print("  pip install radon>=6.0 gitpython>=3.1 pylint>=3.0", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        sys.exit(1)


_check_radon_installed()

import argparse  # noqa: E402
import json  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from enum import Enum  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import TypedDict  # noqa: E402


class RiskLevel(str, Enum):
    """Risk classification based on cyclomatic complexity."""

    LOW = "LOW"  # CC 1-5: Simple, easy to test
    MODERATE = "MODERATE"  # CC 6-10: Manageable complexity
    HIGH = "HIGH"  # CC 11-15: Difficult to test
    VERY_HIGH = "VERY_HIGH"  # CC 16-20: Error-prone
    CRITICAL = "CRITICAL"  # CC >20: Unmaintainable


def get_risk_level(cc: int) -> RiskLevel:
    """
    Classify cyclomatic complexity into risk levels.

    Thresholds from FORMULAS-OBSERVE.md:
    - LOW: 1-5 (simple to test)
    - MODERATE: 6-10 (manageable)
    - HIGH: 11-15 (difficult to test)
    - VERY_HIGH: 16-20 (error-prone)
    - CRITICAL: >20 (unmaintainable)

    Args:
        cc: Cyclomatic complexity value

    Returns:
        Risk level classification
    """
    if cc <= 5:
        return RiskLevel.LOW
    elif cc <= 10:
        return RiskLevel.MODERATE
    elif cc <= 15:
        return RiskLevel.HIGH
    elif cc <= 20:
        return RiskLevel.VERY_HIGH
    else:
        return RiskLevel.CRITICAL


@dataclass
class FunctionComplexity:
    """Complexity data for a single function."""

    name: str
    cc: int
    risk: str
    line: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "cc": self.cc,
            "risk": self.risk,
            "line": self.line,
        }


@dataclass
class FileComplexity:
    """Complexity data for a single file."""

    path: str
    functions: list[FunctionComplexity]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "functions": [f.to_dict() for f in self.functions],
        }


class ComplexitySummary(TypedDict):
    """Summary statistics for complexity analysis."""

    total_functions: int
    high_risk_count: int
    avg_cc: float
    files_analyzed: int


@dataclass
class ComplexityResult:
    """Complete complexity analysis result."""

    files: list[FileComplexity]
    summary: ComplexitySummary

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "files": [f.to_dict() for f in self.files],
            "summary": dict(self.summary),
        }


def analyze_file(file_path: Path) -> FileComplexity | None:
    """
    Analyze cyclomatic complexity of a single Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        FileComplexity object or None if analysis fails
    """
    try:
        from radon.complexity import cc_visit
    except ImportError:
        print("Error: radon library not installed. Run: uv add radon", file=sys.stderr)
        sys.exit(1)

    try:
        source = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return None

    try:
        results = cc_visit(source)
    except SyntaxError as e:
        print(f"Warning: Syntax error in {file_path}: {e}", file=sys.stderr)
        return None

    functions = []
    for result in results:
        # Radon returns objects with complexity, name, lineno attributes
        cc = result.complexity
        risk = get_risk_level(cc)
        functions.append(
            FunctionComplexity(
                name=result.name,
                cc=cc,
                risk=risk.value,
                line=result.lineno,
            )
        )

    return FileComplexity(
        path=str(file_path),
        functions=functions,
    )


def find_python_files(repo_path: Path) -> list[Path]:
    """
    Find all Python files in a directory recursively.

    Args:
        repo_path: Root directory to search

    Returns:
        List of Python file paths
    """
    if repo_path.is_file():
        return [repo_path] if repo_path.suffix == ".py" else []

    return list(repo_path.rglob("*.py"))


def analyze_complexity(
    repo_path: Path,
    language: str = "python",
) -> ComplexityResult:
    """
    Analyze cyclomatic complexity for all files in a repository.

    Args:
        repo_path: Path to repository or file
        language: Programming language (currently only 'python' supported)

    Returns:
        ComplexityResult with per-file findings and summary

    Raises:
        ValueError: If unsupported language specified
    """
    if language != "python":
        raise ValueError(
            f"Unsupported language: {language}. Only 'python' is supported."
        )

    python_files = find_python_files(repo_path)

    if not python_files:
        return ComplexityResult(
            files=[],
            summary={
                "total_functions": 0,
                "high_risk_count": 0,
                "avg_cc": 0.0,
                "files_analyzed": 0,
            },
        )

    file_results: list[FileComplexity] = []
    total_cc = 0
    total_functions = 0
    high_risk_count = 0

    for py_file in python_files:
        file_complexity = analyze_file(py_file)
        if file_complexity is None:
            continue

        file_results.append(file_complexity)

        for func in file_complexity.functions:
            total_functions += 1
            total_cc += func.cc
            # Count HIGH, VERY_HIGH, and CRITICAL as high risk
            if func.risk in (
                RiskLevel.HIGH.value,
                RiskLevel.VERY_HIGH.value,
                RiskLevel.CRITICAL.value,
            ):
                high_risk_count += 1

    avg_cc = total_cc / total_functions if total_functions > 0 else 0.0

    return ComplexityResult(
        files=file_results,
        summary={
            "total_functions": total_functions,
            "high_risk_count": high_risk_count,
            "avg_cc": round(avg_cc, 2),
            "files_analyzed": len(file_results),
        },
    )


def main() -> None:
    """CLI entry point for complexity analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze cyclomatic complexity of Python files using Radon.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Risk Levels:
  LOW (1-5)       Simple, easy to test
  MODERATE (6-10) Manageable complexity
  HIGH (11-15)    Difficult to test
  VERY_HIGH (16-20) Error-prone
  CRITICAL (>20)  Unmaintainable
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
        "--language",
        default="python",
        choices=["python"],
        help="Programming language to analyze (default: python)",
    )

    args = parser.parse_args()

    # Validate repo path exists
    if not args.repo_path.exists():
        print(f"Error: Path does not exist: {args.repo_path}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    try:
        result = analyze_complexity(args.repo_path, args.language)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

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
