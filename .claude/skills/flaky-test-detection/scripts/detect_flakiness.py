#!/usr/bin/env python3
"""
Flaky Test Detection Script

Detects flakiness indicators in test code and runs N-run validation.

Usage:
    python detect_flakiness.py <test_file>           # Analyze test file for indicators
    python detect_flakiness.py --run <test_path> -n 5  # Run test N times
    python detect_flakiness.py --report <results_json>  # Generate flakiness report
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FlakinessIndicator:
    pattern: str
    category: str
    risk_level: str  # HIGH, MEDIUM, LOW
    line_number: int
    fix_suggestion: str


# Flakiness indicator patterns
INDICATOR_PATTERNS = {
    # Timing-related (HIGH risk)
    r"time\.sleep": ("timing", "HIGH", "Replace with explicit wait conditions"),
    r"asyncio\.sleep": ("timing", "HIGH", "Use asyncio.wait_for with proper timeout"),
    r"datetime\.now\(\)": (
        "timing",
        "HIGH",
        "Use time freezing or ranges for comparison",
    ),
    r"\.timeout\s*=": ("timing", "MEDIUM", "Use generous timeouts or mock time"),
    # State-related (HIGH risk)
    r"global\s+\w+": ("state", "HIGH", "Avoid global state in tests"),
    r"class\s+\w+.*:\s*\n\s+\w+\s*=\s*\[\]": (
        "state",
        "HIGH",
        "Use fixtures instead of class variables",
    ),
    r"os\.environ\[": ("state", "MEDIUM", "Set environment in fixtures with cleanup"),
    # External dependencies (HIGH risk)
    r"requests\.(get|post|put|delete)": ("network", "HIGH", "Mock external HTTP calls"),
    r"urllib\.request": ("network", "HIGH", "Mock external HTTP calls"),
    r"socket\.": ("network", "HIGH", "Mock network operations"),
    # Randomness (HIGH risk)
    r"random\.(random|randint|choice|shuffle)": (
        "randomness",
        "HIGH",
        "Seed random or mock",
    ),
    r"uuid\.uuid[14]": ("randomness", "MEDIUM", "Mock UUID generation in tests"),
    # Concurrency (MEDIUM-HIGH risk)
    r"threading\.Thread": ("concurrency", "HIGH", "Use synchronization primitives"),
    r"asyncio\.create_task": ("concurrency", "MEDIUM", "Await tasks explicitly"),
    r"multiprocessing\.": (
        "concurrency",
        "HIGH",
        "Avoid multiprocessing in unit tests",
    ),
    # File system (MEDIUM risk)
    r"open\(['\"]\/tmp": ("filesystem", "MEDIUM", "Use pytest tmp_path fixture"),
    r"Path\(['\"]\/": ("filesystem", "MEDIUM", "Use relative paths or fixtures"),
}


def analyze_test_file(file_path: Path) -> list[FlakinessIndicator]:
    """Analyze a test file for flakiness indicators."""
    content = file_path.read_text()
    lines = content.split("\n")
    indicators = []

    for i, line in enumerate(lines, 1):
        for pattern, (category, risk, fix) in INDICATOR_PATTERNS.items():
            if re.search(pattern, line):
                indicators.append(
                    FlakinessIndicator(
                        pattern=pattern,
                        category=category,
                        risk_level=risk,
                        line_number=i,
                        fix_suggestion=fix,
                    )
                )

    return indicators


def calculate_flakiness_score(indicators: list[FlakinessIndicator]) -> float:
    """Calculate flakiness risk score (0-10)."""
    risk_weights = {"HIGH": 1.0, "MEDIUM": 0.5, "LOW": 0.25}

    total = sum(risk_weights[ind.risk_level] for ind in indicators)

    # Normalize to 0-10 scale (cap at 10)
    return min(10.0, total)


def run_n_times(test_path: str, n: int = 5) -> dict:
    """Run a test N times and collect results."""
    results = {"passed": 0, "failed": 0, "errors": []}

    for i in range(n):
        try:
            result = subprocess.run(
                ["uv", "run", "pytest", test_path, "-x", "-q"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Run {i + 1}: {result.stdout[-500:]}")
        except subprocess.TimeoutExpired:
            results["failed"] += 1
            results["errors"].append(f"Run {i + 1}: Timeout")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Run {i + 1}: {str(e)}")

    # Calculate failure rate
    results["failure_rate"] = results["failed"] / n
    results["is_flaky"] = 0 < results["failure_rate"] < 1.0
    results["verdict"] = classify_failure_rate(results["failure_rate"])

    return results


def classify_failure_rate(rate: float) -> str:
    """Classify failure rate into verdict."""
    if rate == 0:
        return "STABLE - No failures detected"
    elif rate < 0.15:
        return "LIKELY_FLAKY - Rare failures (< 15%)"
    elif rate < 1.0:
        return "FLAKY - Intermittent failures"
    else:
        return "BROKEN - Consistent failure (not flaky)"


def generate_report(
    indicators: list[FlakinessIndicator], n_run_results: dict | None = None
) -> dict:
    """Generate comprehensive flakiness report."""
    score = calculate_flakiness_score(indicators)

    report = {
        "flakiness_score": round(score, 2),
        "risk_level": "HIGH" if score >= 3 else "MEDIUM" if score >= 1 else "LOW",
        "indicator_count": len(indicators),
        "indicators_by_category": {},
        "indicators": [
            {
                "line": ind.line_number,
                "pattern": ind.pattern,
                "category": ind.category,
                "risk": ind.risk_level,
                "fix": ind.fix_suggestion,
            }
            for ind in indicators
        ],
    }

    # Group by category
    for ind in indicators:
        if ind.category not in report["indicators_by_category"]:
            report["indicators_by_category"][ind.category] = 0
        report["indicators_by_category"][ind.category] += 1

    # Add N-run results if available
    if n_run_results:
        report["n_run_validation"] = n_run_results

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python detect_flakiness.py <test_file>")
        print("  python detect_flakiness.py --run <test_path> -n 5")
        sys.exit(1)

    if sys.argv[1] == "--run":
        test_path = sys.argv[2]
        n = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "-n" else 5
        results = run_n_times(test_path, n)
        print(json.dumps(results, indent=2))
    else:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        indicators = analyze_test_file(file_path)
        report = generate_report(indicators)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
