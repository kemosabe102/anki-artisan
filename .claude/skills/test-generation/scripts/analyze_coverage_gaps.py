#!/usr/bin/env python3
"""
Coverage Gap Analyzer

Analyzes test coverage gaps for a module or package by:
1. Finding all public interfaces (functions, classes, methods)
2. Checking which ones have corresponding tests
3. Identifying missing test cases by category

Usage:
    python analyze_coverage_gaps.py <module_path>
    python analyze_coverage_gaps.py packages/core/

Output: JSON with coverage analysis and recommended test cases
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any


def extract_interfaces(file_path: Path) -> list[dict[str, Any]]:
    """Extract public interfaces from a Python file."""
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        return []

    interfaces = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            interfaces.append(
                {
                    "name": node.name,
                    "type": "function",
                    "file": str(file_path),
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "has_return": any(
                        isinstance(n, ast.Return) for n in ast.walk(node)
                    ),
                }
            )

        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            class_info = {
                "name": node.name,
                "type": "class",
                "file": str(file_path),
                "line": node.lineno,
                "methods": [],
            }
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    class_info["methods"].append(item.name)
            interfaces.append(class_info)

    return interfaces


def find_existing_tests(module_path: Path) -> dict[str, list[str]]:
    """Find existing test files and what they test."""
    project_root = Path.cwd()
    tests_dir = project_root / "tests"

    if not tests_dir.exists():
        return {}

    tested = {}
    for test_file in tests_dir.rglob("test_*.py"):
        try:
            with open(test_file) as f:
                content = f.read()
        except Exception:
            continue

        # Extract test function names and what they reference
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                # Parse test name: test_<target>_<condition>_<outcome>
                parts = node.name.split("_")
                if len(parts) >= 2:
                    target = parts[1]
                    if target not in tested:
                        tested[target] = []
                    tested[target].append(node.name)

    return tested


def suggest_test_cases(interface: dict[str, Any]) -> list[dict[str, str]]:
    """Generate suggested test cases for an interface."""
    suggestions = []
    name = interface["name"]
    itype = interface["type"]

    if itype == "function":
        # Happy path
        suggestions.append(
            {
                "name": f"test_{name}_returns_expected_output",
                "category": "happy_path",
                "description": f"Verify {name} returns expected output with valid input",
            }
        )

        # Edge cases based on args
        if interface.get("args"):
            suggestions.append(
                {
                    "name": f"test_{name}_handles_empty_input",
                    "category": "edge_case",
                    "description": f"Verify {name} handles empty/None inputs",
                }
            )

        # Error handling
        suggestions.append(
            {
                "name": f"test_{name}_raises_on_invalid_input",
                "category": "error_handling",
                "description": f"Verify {name} raises appropriate exceptions",
            }
        )

    elif itype == "class":
        suggestions.append(
            {
                "name": f"test_{name}_initialization",
                "category": "happy_path",
                "description": f"Verify {name} initializes correctly",
            }
        )
        for method in interface.get("methods", []):
            suggestions.append(
                {
                    "name": f"test_{name}_{method}_works",
                    "category": "method_test",
                    "description": f"Verify {name}.{method} works correctly",
                }
            )

    return suggestions


def analyze_coverage_gaps(module_path: str) -> dict[str, Any]:
    """
    Main analysis function.

    Returns JSON with:
    - total_interfaces: int
    - tested_interfaces: int
    - untested_interfaces: list[dict]
    - coverage_percentage: float
    - suggested_tests: list[dict]
    """
    path = Path(module_path)

    if not path.exists():
        return {"error": "path_not_found", "path": str(path)}

    # Collect all interfaces
    all_interfaces = []
    if path.is_file():
        all_interfaces = extract_interfaces(path)
    else:
        for py_file in path.rglob("*.py"):
            if "__pycache__" not in str(py_file):
                all_interfaces.extend(extract_interfaces(py_file))

    # Find existing tests
    existing_tests = find_existing_tests(path)

    # Categorize interfaces
    tested = []
    untested = []

    for iface in all_interfaces:
        name = iface["name"].lower()
        if name in existing_tests or any(name in t.lower() for t in existing_tests):
            tested.append(iface)
        else:
            untested.append(iface)

    # Generate suggestions for untested
    suggestions = []
    for iface in untested[:10]:  # Limit to top 10
        suggestions.extend(suggest_test_cases(iface))

    total = len(all_interfaces)
    return {
        "module_path": str(path),
        "total_interfaces": total,
        "tested_count": len(tested),
        "untested_count": len(untested),
        "coverage_percentage": (len(tested) / total * 100) if total else 100.0,
        "untested_interfaces": untested[:20],  # Limit output
        "suggested_tests": suggestions[:15],
        "meets_80_threshold": (len(tested) / total >= 0.8) if total else True,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_coverage_gaps.py <module_path>")
        sys.exit(1)

    result = analyze_coverage_gaps(sys.argv[1])
    print(json.dumps(result, indent=2))
