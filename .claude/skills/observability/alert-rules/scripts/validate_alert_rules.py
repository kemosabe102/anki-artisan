#!/usr/bin/env python3
"""
Prometheus Alert Rules Validator

Validates Prometheus alert rules against 10 anti-patterns.

Usage:
    python validate_alert_rules.py alerts.yaml
    python validate_alert_rules.py --dir /path/to/rules/
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


@dataclass
class AlertValidationResult:
    """Result of alert rule validation."""

    alert_name: str
    file_path: str
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    anti_patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "alert_name": self.alert_name,
            "file_path": self.file_path,
            "valid": self.valid and not self.errors,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "anti_patterns": self.anti_patterns,
            "verdict": "PASS" if self.valid and not self.errors else "FAIL",
        }


class AlertRulesValidator:
    """Validates Prometheus alert rules against best practices."""

    # Severity levels in order of priority
    SEVERITY_LEVELS = ["critical", "warning", "info", "none"]

    # Required annotations
    REQUIRED_ANNOTATIONS = ["summary", "description"]

    # Recommended for clause durations by severity
    RECOMMENDED_FOR_DURATION = {"critical": "5m", "warning": "10m", "info": "15m"}

    # Duration in seconds
    DURATION_PATTERN = re.compile(r"^(\d+)(ms|s|m|h|d)$")
    DURATION_MULTIPLIERS = {"ms": 0.001, "s": 1, "m": 60, "h": 3600, "d": 86400}

    def __init__(self):
        self.seen_alert_names: set[str] = set()

    def validate_file(self, file_path: Path) -> list[AlertValidationResult]:
        """Validate all alert rules in a file."""
        results = []

        try:
            with open(file_path) as f:
                content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            result = AlertValidationResult(
                alert_name="<YAML_ERROR>", file_path=str(file_path), valid=False
            )
            result.errors.append(f"Invalid YAML: {e}")
            return [result]
        except Exception as e:
            result = AlertValidationResult(
                alert_name="<FILE_ERROR>", file_path=str(file_path), valid=False
            )
            result.errors.append(f"Failed to read file: {e}")
            return [result]

        if not content:
            return results

        # Handle both standalone rules and groups format
        groups = content.get("groups", [])
        if not groups and "rules" in content:
            groups = [{"name": "default", "rules": content["rules"]}]

        for group in groups:
            rules = group.get("rules", [])
            for rule in rules:
                if "alert" in rule:  # It's an alert rule, not recording rule
                    result = self.validate_rule(rule, str(file_path))
                    results.append(result)

        return results

    def validate_rule(
        self, rule: dict[str, Any], file_path: str
    ) -> AlertValidationResult:
        """Validate a single alert rule."""
        alert_name = rule.get("alert", "<unnamed>")
        result = AlertValidationResult(alert_name=alert_name, file_path=file_path)

        # Run all anti-pattern checks
        self._check_duplicate_name(rule, result)
        self._check_missing_for_clause(rule, result)
        self._check_irate_in_alert(rule, result)
        self._check_absolute_thresholds(rule, result)
        self._check_missing_severity(rule, result)
        self._check_missing_runbook(rule, result)
        self._check_complex_expression(rule, result)
        self._check_high_cardinality_labels(rule, result)
        self._check_missing_annotations(rule, result)
        self._check_unreachable_thresholds(rule, result)

        # Additional best practice checks
        self._check_for_duration(rule, result)
        self._check_expression_syntax(rule, result)

        return result

    def _check_duplicate_name(self, rule: dict, result: AlertValidationResult) -> None:
        """Anti-pattern #9: Duplicate alert names."""
        alert_name = rule.get("alert", "")

        if alert_name in self.seen_alert_names:
            result.anti_patterns.append("AP-09: Duplicate alert name")
            result.errors.append(
                f"Duplicate alert name '{alert_name}'. "
                "Alert names must be unique across all rules."
            )
        else:
            self.seen_alert_names.add(alert_name)

    def _check_missing_for_clause(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #1: Missing for clause."""
        if "for" not in rule:
            result.anti_patterns.append("AP-01: Missing 'for' clause")
            result.warnings.append(
                "Alert has no 'for' clause. Without it, the alert fires immediately "
                "on first evaluation, causing potential alert spam. "
                "Recommend adding 'for: 5m' or appropriate duration."
            )

    def _check_irate_in_alert(self, rule: dict, result: AlertValidationResult) -> None:
        """Anti-pattern #2: irate() in alert expressions."""
        expr = rule.get("expr", "")

        if re.search(r"\birate\s*\(", expr, re.IGNORECASE):
            result.anti_patterns.append("AP-02: irate() in alert expression")
            result.errors.append(
                "irate() is not recommended in alert expressions. "
                "It's volatile and can cause alerts to flap. Use rate() instead."
            )

    def _check_absolute_thresholds(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #3: Absolute thresholds that don't scale."""
        expr = rule.get("expr", "")

        # Look for patterns like "> 1000" without rate or ratio
        absolute_patterns = [
            r">\s*\d{4,}",  # > large number (1000+)
            r"<\s*\d{4,}",  # < large number
        ]

        has_absolute = any(re.search(p, expr) for p in absolute_patterns)
        has_rate = bool(re.search(r"\b(rate|irate|increase)\s*\(", expr, re.IGNORECASE))
        has_ratio = bool(re.search(r"/", expr))  # Division suggests ratio

        if has_absolute and not has_rate and not has_ratio:
            result.anti_patterns.append("AP-03: Absolute threshold")
            result.suggestions.append(
                "Alert uses absolute threshold that may not scale with traffic. "
                "Consider using rates, ratios, or percentiles instead."
            )

    def _check_missing_severity(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #4: Missing severity labels."""
        labels = rule.get("labels", {})

        if "severity" not in labels:
            result.anti_patterns.append("AP-04: Missing severity label")
            result.errors.append(
                "Alert is missing 'severity' label. "
                "Add 'labels: severity: critical|warning|info' for proper routing."
            )
        else:
            severity = labels.get("severity", "").lower()
            if severity not in self.SEVERITY_LEVELS:
                result.warnings.append(
                    f"Non-standard severity '{severity}'. "
                    f"Recommended values: {', '.join(self.SEVERITY_LEVELS)}"
                )

    def _check_missing_runbook(self, rule: dict, result: AlertValidationResult) -> None:
        """Anti-pattern #5: Missing runbook_url annotation."""
        annotations = rule.get("annotations", {})

        if "runbook_url" not in annotations:
            result.anti_patterns.append("AP-05: Missing runbook_url")
            result.warnings.append(
                "Alert is missing 'runbook_url' annotation. "
                "Runbooks help on-call engineers respond quickly."
            )

    def _check_complex_expression(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #6: Overly complex expressions."""
        expr = rule.get("expr", "")

        # Count complexity indicators
        complexity_score = 0
        complexity_score += expr.count("(") * 0.5  # Nested functions
        complexity_score += expr.count("and") + expr.count("or")  # Boolean ops
        complexity_score += expr.count("unless") * 2  # Set operations
        complexity_score += len(re.findall(r"\bby\s*\(", expr))  # Aggregations

        if complexity_score > 5:
            result.anti_patterns.append("AP-06: Overly complex expression")
            result.suggestions.append(
                f"Complex expression (score: {complexity_score:.1f}). "
                "Consider breaking into recording rules for readability and performance."
            )

    def _check_high_cardinality_labels(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #7: High cardinality label selectors."""
        expr = rule.get("expr", "")

        high_card_patterns = [
            "request_id",
            "trace_id",
            "user_id",
            "session_id",
            "correlation_id",
            "transaction_id",
            "order_id",
        ]

        for pattern in high_card_patterns:
            if pattern in expr.lower():
                result.anti_patterns.append("AP-07: High-cardinality label")
                result.warnings.append(
                    f"Expression references potentially high-cardinality label '{pattern}'. "
                    "This may cause cardinality explosion in ALERTS time series."
                )
                break

    def _check_missing_annotations(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #8: Missing summary/description annotations."""
        annotations = rule.get("annotations", {})

        missing = [a for a in self.REQUIRED_ANNOTATIONS if a not in annotations]

        if missing:
            result.anti_patterns.append("AP-08: Missing annotations")
            result.warnings.append(
                f"Alert is missing annotations: {', '.join(missing)}. "
                "These help understand what the alert means."
            )

    def _check_unreachable_thresholds(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Anti-pattern #10: Unreachable or always-true thresholds."""
        expr = rule.get("expr", "")

        # Check for always-true conditions
        always_true_patterns = [
            r">\s*-\d+",  # > negative number (most metrics are positive)
            r">=\s*0\b",  # >= 0 (always true for counters)
            r"<\s*inf",  # < infinity
        ]

        for pattern in always_true_patterns:
            if re.search(pattern, expr, re.IGNORECASE):
                result.anti_patterns.append("AP-10: Unreachable threshold")
                result.errors.append(
                    "Alert expression may always be true or never fire. "
                    "Check threshold values are realistic."
                )
                break

        # Check for impossible conditions
        impossible_patterns = [
            r"<\s*0\b",  # < 0 (impossible for counters)
            r">\s*1\b.*percent(?:ile)?",  # > 1 for percentages (assuming 0-1)
        ]

        for pattern in impossible_patterns:
            if re.search(pattern, expr, re.IGNORECASE):
                result.warnings.append(
                    "Alert threshold may be impossible to reach. "
                    "Verify the threshold makes sense for the metric type."
                )
                break

    def _check_for_duration(self, rule: dict, result: AlertValidationResult) -> None:
        """Check if 'for' duration is appropriate for severity."""
        for_duration = rule.get("for", "")
        severity = rule.get("labels", {}).get("severity", "").lower()

        if not for_duration or severity not in self.RECOMMENDED_FOR_DURATION:
            return

        # Parse duration
        match = self.DURATION_PATTERN.match(for_duration)
        if not match:
            return

        value = int(match.group(1))
        unit = match.group(2)
        duration_seconds = value * self.DURATION_MULTIPLIERS[unit]

        # Check against recommendations
        recommended = self.RECOMMENDED_FOR_DURATION[severity]
        rec_match = self.DURATION_PATTERN.match(recommended)
        if rec_match:
            rec_value = int(rec_match.group(1))
            rec_unit = rec_match.group(2)
            rec_seconds = rec_value * self.DURATION_MULTIPLIERS[rec_unit]

            if duration_seconds < rec_seconds * 0.5:
                result.suggestions.append(
                    f"'for: {for_duration}' is short for {severity} severity. "
                    f"Consider 'for: {recommended}' to reduce alert noise."
                )

    def _check_expression_syntax(
        self, rule: dict, result: AlertValidationResult
    ) -> None:
        """Basic expression syntax validation."""
        expr = rule.get("expr", "")

        # Check balanced brackets
        if expr.count("(") != expr.count(")"):
            result.errors.append("Unbalanced parentheses in expression")

        if expr.count("[") != expr.count("]"):
            result.errors.append("Unbalanced square brackets in expression")

        if expr.count("{") != expr.count("}"):
            result.errors.append("Unbalanced curly braces in expression")


def main():
    parser = argparse.ArgumentParser(description="Validate Prometheus alert rules")
    parser.add_argument("path", nargs="?", help="Path to alert rules YAML file")
    parser.add_argument("--dir", "-d", help="Directory containing alert rule files")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--strict", "-s", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    if not args.path and not args.dir:
        parser.print_help()
        sys.exit(1)

    validator = AlertRulesValidator()
    all_results = []

    files_to_check = []
    if args.path:
        files_to_check.append(Path(args.path))
    if args.dir:
        dir_path = Path(args.dir)
        files_to_check.extend(dir_path.glob("**/*.yaml"))
        files_to_check.extend(dir_path.glob("**/*.yml"))

    for file_path in files_to_check:
        results = validator.validate_file(file_path)
        all_results.extend(results)

    # Calculate summary
    total = len(all_results)
    passed = sum(1 for r in all_results if not r.errors)
    if args.strict:
        passed = sum(1 for r in all_results if not r.errors and not r.warnings)

    if args.json:
        output = {
            "summary": {"total": total, "passed": passed, "failed": total - passed},
            "results": [r.to_dict() for r in all_results],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'=' * 60}")
        print("Alert Rules Validation Report")
        print(f"{'=' * 60}")

        for result in all_results:
            status = "✅ PASS" if not result.errors else "❌ FAIL"
            if args.strict and result.warnings:
                status = "❌ FAIL"

            print(f"\n{status} {result.alert_name}")
            print(f"   File: {result.file_path}")

            if result.anti_patterns:
                print(f"   Anti-patterns: {', '.join(result.anti_patterns)}")

            for e in result.errors:
                print(f"   ❌ ERROR: {e}")

            for w in result.warnings:
                print(f"   ⚠️  WARNING: {w}")

            for s in result.suggestions:
                print(f"   💡 {s}")

        print(f"\n{'=' * 60}")
        print(f"Summary: {passed}/{total} alerts passed validation")
        print(f"{'=' * 60}")

    # Exit with error if any failures
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
