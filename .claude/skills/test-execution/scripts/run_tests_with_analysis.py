#!/usr/bin/env python3
"""
Test Execution Runner with Analysis

Runs pytest with structured output parsing and provides:
1. Exit code interpretation
2. Failure extraction with categorization hints
3. Test independence validation (isolated reruns)
4. Timing analysis

Usage:
    python run_tests_with_analysis.py [test_path] [--validate-independence]
    python run_tests_with_analysis.py tests/unit/
    python run_tests_with_analysis.py tests/unit/test_auth.py --validate-independence

Output: JSON with execution results and analysis
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

EXIT_CODES = {
    0: {"status": "passed", "description": "All tests passed"},
    1: {"status": "failed", "description": "Some tests failed"},
    2: {"status": "interrupted", "description": "Test interrupted by user"},
    3: {"status": "internal_error", "description": "Internal pytest error"},
    4: {"status": "usage_error", "description": "Command line usage error"},
    5: {"status": "no_tests", "description": "No tests collected"},
}


def run_pytest(test_path: str, extra_args: list[str] = None) -> dict[str, Any]:
    """Run pytest and capture output."""
    cmd = ["uv", "run", "pytest", test_path, "-v", "--tb=short"]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Test execution timed out after 5 minutes",
            "success": False,
            "timeout": True,
        }
    except Exception as e:
        return {"exit_code": -2, "stdout": "", "stderr": str(e), "success": False}


def parse_failures(output: str) -> list[dict[str, Any]]:
    """Extract failure information from pytest output."""
    failures = []

    # Pattern: FAILED tests/path/test_file.py::test_name - reason
    failure_pattern = r"FAILED\s+([\w/\.]+)::(\w+)(?:\s+-\s+(.+))?"

    for match in re.finditer(failure_pattern, output):
        file_path, test_name, reason = match.groups()
        failures.append(
            {
                "file": file_path,
                "test": test_name,
                "reason": reason or "Unknown",
                "full_id": f"{file_path}::{test_name}",
            }
        )

    return failures


def parse_summary(output: str) -> dict[str, int]:
    """Extract test summary counts from output."""
    summary = {"passed": 0, "failed": 0, "skipped": 0, "error": 0}

    # Pattern: 5 passed, 2 failed, 1 skipped in 1.23s
    patterns = {
        "passed": r"(\d+)\s+passed",
        "failed": r"(\d+)\s+failed",
        "skipped": r"(\d+)\s+skipped",
        "error": r"(\d+)\s+error",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            summary[key] = int(match.group(1))

    return summary


def validate_independence(test_path: str, test_ids: list[str]) -> list[dict[str, Any]]:
    """Run tests in isolation to check for interdependencies."""
    results = []

    for test_id in test_ids[:5]:  # Limit to 5 tests
        isolated = run_pytest(test_id)
        results.append(
            {
                "test_id": test_id,
                "isolated_result": "passed" if isolated["success"] else "failed",
                "exit_code": isolated["exit_code"],
            }
        )

    return results


def run_tests_with_analysis(
    test_path: str, validate_ind: bool = False
) -> dict[str, Any]:
    """
    Main execution function.

    Returns JSON with:
    - exit_code: int
    - exit_info: dict (status, description)
    - summary: dict (passed, failed, skipped, error)
    - failures: list[dict]
    - independence_check: list[dict] (if requested)
    """
    path = Path(test_path) if test_path else Path("tests/")

    if not path.exists():
        return {"error": "path_not_found", "path": str(path)}

    # Run main test suite
    result = run_pytest(str(path))

    exit_info = EXIT_CODES.get(
        result["exit_code"],
        {
            "status": "unknown",
            "description": f"Unknown exit code: {result['exit_code']}",
        },
    )

    failures = parse_failures(result["stdout"])
    summary = parse_summary(result["stdout"])

    output = {
        "test_path": str(path),
        "exit_code": result["exit_code"],
        "exit_info": exit_info,
        "summary": summary,
        "failures": failures,
        "total_tests": sum(summary.values()),
        "pass_rate": summary["passed"] / sum(summary.values()) * 100
        if sum(summary.values())
        else 0,
    }

    # Optional independence validation
    if validate_ind and failures:
        failed_ids = [f["full_id"] for f in failures]
        output["independence_check"] = validate_independence(str(path), failed_ids)

    return output


if __name__ == "__main__":
    test_path = sys.argv[1] if len(sys.argv) > 1 else "tests/"
    validate_ind = "--validate-independence" in sys.argv

    result = run_tests_with_analysis(test_path, validate_ind)
    print(json.dumps(result, indent=2))
