#!/usr/bin/env python3
"""
Test Failure Categorization Script

Analyzes pytest output and categorizes failures into:
- APPLICATION_BUG: Bug in application code
- TEST_BUG: Bug in test code
- ENVIRONMENT: Environment/dependency issue
- FLAKY: Non-deterministic failure

Usage:
    python categorize_failure.py <pytest_output_file>
    python categorize_failure.py --stdin  # Read from stdin
"""

import json
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class FailureCategory(Enum):
    APPLICATION_BUG = "APPLICATION_BUG"
    TEST_BUG = "TEST_BUG"
    ENVIRONMENT = "ENVIRONMENT"
    FLAKY = "FLAKY"
    UNKNOWN = "UNKNOWN"


@dataclass
class CategorizationResult:
    category: FailureCategory
    confidence: float
    pattern_matched: str
    adjustments: list[str]
    recommendation: str


# Pattern catalog with base confidence scores
PATTERNS = {
    # ENVIRONMENT patterns (check first - highest certainty)
    "ModuleNotFoundError": (FailureCategory.ENVIRONMENT, 0.90, "Missing dependency"),
    "ImportError": (FailureCategory.ENVIRONMENT, 0.85, "Import failure"),
    "ConnectionRefusedError": (
        FailureCategory.ENVIRONMENT,
        0.85,
        "Resource unavailable",
    ),
    "ConnectionError": (FailureCategory.ENVIRONMENT, 0.80, "Network issue"),
    "FileNotFoundError": (FailureCategory.ENVIRONMENT, 0.75, "Missing file"),
    "PermissionError": (FailureCategory.ENVIRONMENT, 0.80, "Permission denied"),
    # TEST_BUG patterns
    "fixture.*not found": (FailureCategory.TEST_BUG, 0.85, "Fixture misuse"),
    "MagicMock": (FailureCategory.TEST_BUG, 0.80, "Mock configuration error"),
    "@pytest.fixture": (FailureCategory.TEST_BUG, 0.75, "Fixture decorator issue"),
    "setup_method.*failed": (FailureCategory.TEST_BUG, 0.70, "Setup failure"),
    "teardown.*failed": (FailureCategory.TEST_BUG, 0.70, "Teardown failure"),
    # APPLICATION_BUG patterns
    "AssertionError": (FailureCategory.APPLICATION_BUG, 0.75, "Assertion mismatch"),
    "TypeError": (FailureCategory.APPLICATION_BUG, 0.70, "Type error"),
    "ValueError": (FailureCategory.APPLICATION_BUG, 0.70, "Value error"),
    "AttributeError": (FailureCategory.APPLICATION_BUG, 0.70, "Attribute error"),
    "KeyError": (FailureCategory.APPLICATION_BUG, 0.70, "Key error"),
    "IndexError": (FailureCategory.APPLICATION_BUG, 0.70, "Index error"),
    # FLAKY patterns (need N-run validation)
    "TimeoutError": (FailureCategory.FLAKY, 0.65, "Timeout - possible flaky"),
    "asyncio.*timeout": (FailureCategory.FLAKY, 0.60, "Async timeout"),
    "random": (FailureCategory.FLAKY, 0.55, "Randomness detected"),
}


def apply_adjustments(
    base_confidence: float, error_output: str, category: FailureCategory
) -> tuple[float, list[str]]:
    """Apply confidence adjustments based on context."""
    adjustments = []
    confidence = base_confidence

    # Positive adjustments
    if "assert" in error_output.lower() and "==" in error_output:
        confidence += 0.10
        adjustments.append("+0.10: Clear expected vs actual")

    if error_output.count("File") == 1:
        confidence += 0.05
        adjustments.append("+0.05: Single location")

    # Negative adjustments
    if (
        "multiple" in error_output.lower()
        or len(re.findall(r"File.*line", error_output)) > 3
    ):
        confidence -= 0.10
        adjustments.append("-0.10: Multiple locations")

    if category == FailureCategory.APPLICATION_BUG and "test_" in error_output:
        confidence -= 0.05
        adjustments.append("-0.05: Error in test file")

    # Cap confidence
    confidence = max(0.30, min(0.95, confidence))

    return confidence, adjustments


def get_recommendation(category: FailureCategory, confidence: float) -> str:
    """Get action recommendation based on category."""
    recommendations = {
        FailureCategory.APPLICATION_BUG: "Delegate to development agent for debugging",
        FailureCategory.TEST_BUG: "Fix test code directly - check fixtures/mocks",
        FailureCategory.ENVIRONMENT: "Report to user - check dependencies/resources",
        FailureCategory.FLAKY: "Run N-run validation before proceeding",
        FailureCategory.UNKNOWN: "Manual investigation required",
    }

    base = recommendations[category]
    if confidence < 0.70:
        base += " (low confidence - verify manually)"

    return base


def categorize_failure(error_output: str) -> CategorizationResult:
    """Categorize a test failure based on error output."""

    # Try each pattern in order
    for pattern, (category, base_confidence, description) in PATTERNS.items():
        if re.search(pattern, error_output, re.IGNORECASE):
            confidence, adjustments = apply_adjustments(
                base_confidence, error_output, category
            )
            return CategorizationResult(
                category=category,
                confidence=confidence,
                pattern_matched=description,
                adjustments=adjustments,
                recommendation=get_recommendation(category, confidence),
            )

    # No pattern matched
    return CategorizationResult(
        category=FailureCategory.UNKNOWN,
        confidence=0.50,
        pattern_matched="No pattern matched",
        adjustments=[],
        recommendation=get_recommendation(FailureCategory.UNKNOWN, 0.50),
    )


def format_output(result: CategorizationResult) -> str:
    """Format result as JSON."""
    return json.dumps(
        {
            "category": result.category.value,
            "confidence": round(result.confidence, 2),
            "pattern_matched": result.pattern_matched,
            "adjustments": result.adjustments,
            "recommendation": result.recommendation,
        },
        indent=2,
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python categorize_failure.py <pytest_output_file>")
        print("       python categorize_failure.py --stdin")
        sys.exit(1)

    if sys.argv[1] == "--stdin":
        error_output = sys.stdin.read()
    else:
        error_output = Path(sys.argv[1]).read_text()

    result = categorize_failure(error_output)
    print(format_output(result))


if __name__ == "__main__":
    main()
