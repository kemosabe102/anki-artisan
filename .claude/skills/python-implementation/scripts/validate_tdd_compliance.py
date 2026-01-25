#!/usr/bin/env python3
"""
TDD Compliance Validator

Validates that implementation follows TDD-first methodology by checking:
1. Test file exists before/with implementation
2. Test covers public interfaces
3. Defensive programming patterns are applied

Usage:
    python validate_tdd_compliance.py <implementation_file>
    python validate_tdd_compliance.py packages/core/auth.py

Output: JSON with compliance status and violations
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any


def find_test_file(impl_path: Path) -> Path | None:
    """Find corresponding test file for implementation."""
    # Convert impl path to potential test paths
    impl_name = impl_path.stem
    impl_parts = impl_path.parts

    # Try different test file locations
    test_patterns = [
        f"tests/unit/test_{impl_name}.py",
        f"tests/test_{impl_name}.py",
        f"tests/unit/{'/'.join(impl_parts[1:-1])}/test_{impl_name}.py",
    ]

    project_root = Path.cwd()
    for pattern in test_patterns:
        test_path = project_root / pattern
        if test_path.exists():
            return test_path

    return None


def extract_public_interfaces(impl_path: Path) -> list[str]:
    """Extract public function/class names from implementation."""
    try:
        with open(impl_path) as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        return []

    interfaces = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            interfaces.append(node.name)
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            interfaces.append(node.name)

    return interfaces


def extract_tested_names(test_path: Path) -> list[str]:
    """Extract what names are referenced in test file."""
    try:
        with open(test_path) as f:
            content = f.read()
            tree = ast.parse(content)
    except SyntaxError:
        return []

    # Collect all names referenced in tests
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)

    return list(names)


def check_defensive_patterns(impl_path: Path) -> dict[str, Any]:
    """Check for defensive programming pattern violations."""
    try:
        with open(impl_path) as f:
            content = f.read()
            tree = ast.parse(content)
    except SyntaxError:
        return {"error": "syntax_error", "violations": []}

    violations = []

    for node in ast.walk(tree):
        # DP-02: Mutable default arguments
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    violations.append(
                        {
                            "pattern": "DP-02",
                            "description": "Mutable default argument",
                            "line": node.lineno,
                            "function": node.name,
                            "severity": "HIGH",
                        }
                    )

        # DP-03: Bare except clauses
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                violations.append(
                    {
                        "pattern": "DP-03",
                        "description": "Bare except clause",
                        "line": node.lineno,
                        "severity": "HIGH",
                    }
                )

    return {"violations": violations, "count": len(violations)}


def validate_tdd_compliance(impl_path: str) -> dict[str, Any]:
    """
    Main validation function.

    Returns JSON with:
    - test_exists: bool
    - test_path: str | None
    - public_interfaces: list[str]
    - tested_interfaces: list[str]
    - untested_interfaces: list[str]
    - coverage_ratio: float
    - defensive_violations: list[dict]
    - compliant: bool
    """
    impl = Path(impl_path)

    if not impl.exists():
        return {"error": "file_not_found", "path": str(impl)}

    result = {
        "implementation_file": str(impl),
        "test_exists": False,
        "test_path": None,
        "public_interfaces": [],
        "tested_interfaces": [],
        "untested_interfaces": [],
        "coverage_ratio": 0.0,
        "defensive_violations": [],
        "compliant": False,
    }

    # Check for test file
    test_path = find_test_file(impl)
    result["test_exists"] = test_path is not None
    result["test_path"] = str(test_path) if test_path else None

    # Extract public interfaces
    interfaces = extract_public_interfaces(impl)
    result["public_interfaces"] = interfaces

    # Check test coverage of interfaces
    if test_path:
        tested_names = extract_tested_names(test_path)
        tested = [i for i in interfaces if i in tested_names]
        untested = [i for i in interfaces if i not in tested_names]
        result["tested_interfaces"] = tested
        result["untested_interfaces"] = untested
        result["coverage_ratio"] = len(tested) / len(interfaces) if interfaces else 1.0

    # Check defensive patterns
    defensive = check_defensive_patterns(impl)
    result["defensive_violations"] = defensive.get("violations", [])

    # Determine compliance
    result["compliant"] = (
        result["test_exists"]
        and result["coverage_ratio"] >= 0.8
        and len(result["defensive_violations"]) == 0
    )

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_tdd_compliance.py <implementation_file>")
        sys.exit(1)

    result = validate_tdd_compliance(sys.argv[1])
    print(json.dumps(result, indent=2))
