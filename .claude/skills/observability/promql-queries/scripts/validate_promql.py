#!/usr/bin/env python3
"""
PromQL Query Validator

Validates PromQL query syntax and best practices.

Usage:
    python validate_promql.py "rate(http_requests_total[5m])"
    python validate_promql.py --file queries.txt
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of PromQL validation."""

    query: str
    valid_syntax: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    cardinality_estimate: int | None = None
    recording_rule_candidate: bool = False

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "valid_syntax": self.valid_syntax,
            "warnings": self.warnings,
            "errors": self.errors,
            "suggestions": self.suggestions,
            "cardinality_estimate": self.cardinality_estimate,
            "recording_rule_candidate": self.recording_rule_candidate,
            "verdict": "PASS" if self.valid_syntax and not self.errors else "FAIL",
        }


class PromQLValidator:
    """Validates PromQL queries for syntax and best practices."""

    # Common PromQL functions
    AGGREGATION_OPS = {
        "sum",
        "min",
        "max",
        "avg",
        "group",
        "stddev",
        "stdvar",
        "count",
        "count_values",
        "bottomk",
        "topk",
        "quantile",
    }

    RANGE_FUNCTIONS = {
        "rate",
        "irate",
        "increase",
        "delta",
        "idelta",
        "deriv",
        "predict_linear",
        "holt_winters",
        "changes",
        "resets",
        "avg_over_time",
        "min_over_time",
        "max_over_time",
        "sum_over_time",
        "count_over_time",
        "quantile_over_time",
        "stddev_over_time",
        "stdvar_over_time",
        "last_over_time",
        "present_over_time",
        "absent_over_time",
    }

    INSTANT_FUNCTIONS = {
        "abs",
        "absent",
        "ceil",
        "clamp",
        "clamp_max",
        "clamp_min",
        "day_of_month",
        "day_of_week",
        "day_of_year",
        "days_in_month",
        "exp",
        "floor",
        "histogram_quantile",
        "hour",
        "label_join",
        "label_replace",
        "ln",
        "log2",
        "log10",
        "minute",
        "month",
        "round",
        "scalar",
        "sgn",
        "sort",
        "sort_desc",
        "sqrt",
        "time",
        "timestamp",
        "vector",
        "year",
    }

    # Patterns
    DURATION_PATTERN = re.compile(r"\[(\d+)(ms|s|m|h|d|w|y)\]")
    LABEL_PATTERN = re.compile(r"\{([^}]*)\}")
    RATE_PATTERN = re.compile(r"\b(rate|irate|increase)\s*\(")
    OFFSET_PATTERN = re.compile(r"offset\s+(\d+)(ms|s|m|h|d|w|y)")
    SUBQUERY_PATTERN = re.compile(r"\[(\d+)(ms|s|m|h|d|w|y):(\d+)?(ms|s|m|h|d|w|y)?\]")

    # Duration in seconds
    DURATION_MULTIPLIERS = {
        "ms": 0.001,
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "y": 31536000,
    }

    def __init__(self, scrape_interval: int = 15):
        """Initialize validator with scrape interval in seconds."""
        self.scrape_interval = scrape_interval
        self.min_rate_interval = scrape_interval * 4  # 4x rule

    def validate(self, query: str) -> ValidationResult:
        """Validate a PromQL query."""
        result = ValidationResult(query=query)

        # Basic syntax checks
        self._check_brackets(query, result)
        self._check_parentheses(query, result)
        self._check_quotes(query, result)

        if result.errors:
            result.valid_syntax = False
            return result

        # Best practice checks
        self._check_rate_interval(query, result)
        self._check_irate_usage(query, result)
        self._check_label_matchers(query, result)
        self._check_aggregation_without_by(query, result)
        self._check_histogram_quantile(query, result)

        # Cardinality and recording rule analysis
        self._estimate_cardinality(query, result)
        self._check_recording_rule_candidate(query, result)

        return result

    def _check_brackets(self, query: str, result: ValidationResult) -> None:
        """Check for balanced square brackets."""
        count = 0
        for char in query:
            if char == "[":
                count += 1
            elif char == "]":
                count -= 1
            if count < 0:
                result.errors.append("Unbalanced square brackets: extra ']'")
                return
        if count > 0:
            result.errors.append("Unbalanced square brackets: missing ']'")

    def _check_parentheses(self, query: str, result: ValidationResult) -> None:
        """Check for balanced parentheses."""
        count = 0
        for char in query:
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1
            if count < 0:
                result.errors.append("Unbalanced parentheses: extra ')'")
                return
        if count > 0:
            result.errors.append("Unbalanced parentheses: missing ')'")

    def _check_quotes(self, query: str, result: ValidationResult) -> None:
        """Check for balanced quotes in label matchers."""
        in_string = False
        escape = False
        quote_char = None

        for char in query:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char in "\"'`":
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None

        if in_string:
            result.errors.append(f"Unclosed string literal (started with {quote_char})")

    def _check_rate_interval(self, query: str, result: ValidationResult) -> None:
        """Check rate/irate/increase interval follows 4x scrape_interval rule."""
        for match in self.RATE_PATTERN.finditer(query):
            func_name = match.group(1)
            # Find the duration after this function
            rest = query[match.end() :]
            duration_match = self.DURATION_PATTERN.search(rest)

            if duration_match:
                value = int(duration_match.group(1))
                unit = duration_match.group(2)
                interval_seconds = value * self.DURATION_MULTIPLIERS[unit]

                if interval_seconds < self.min_rate_interval:
                    result.warnings.append(
                        f"{func_name}() interval [{value}{unit}] is less than 4x "
                        f"scrape_interval ({self.scrape_interval}s). "
                        f"Recommend at least [{self.min_rate_interval}s] or use $__rate_interval."
                    )

    def _check_irate_usage(self, query: str, result: ValidationResult) -> None:
        """Warn about irate() usage in alerts or recording rules."""
        if re.search(r"\birate\s*\(", query):
            result.warnings.append(
                "irate() is volatile and not recommended for alerts or recording rules. "
                "Consider using rate() instead for more stable results."
            )

    def _check_label_matchers(self, query: str, result: ValidationResult) -> None:
        """Check label matcher syntax and patterns."""
        for match in self.LABEL_PATTERN.finditer(query):
            labels = match.group(1)

            # Check for empty regex matchers
            if '=~""' in labels or "=~''" in labels:
                result.warnings.append(
                    'Empty regex matcher (=~"") matches everything. '
                    "Consider removing or using a specific pattern."
                )

            # Check for .* without anchors
            if '=~".*"' in labels or "=~'.*'" in labels:
                result.warnings.append(
                    "Regex '.*' matches everything. Consider using a more specific pattern "
                    "or remove the label matcher entirely."
                )

            # Check for high-cardinality label patterns
            high_card_labels = [
                "request_id",
                "trace_id",
                "user_id",
                "session_id",
                "correlation_id",
            ]
            for label in high_card_labels:
                if label in labels and "!=" not in labels and "!~" not in labels:
                    result.warnings.append(
                        f"Label '{label}' is typically high-cardinality. "
                        f"Ensure this doesn't cause cardinality explosion."
                    )

    def _check_aggregation_without_by(
        self, query: str, result: ValidationResult
    ) -> None:
        """Warn about aggregations without by/without clause."""
        for op in self.AGGREGATION_OPS:
            pattern = rf"\b{op}\s*\("
            if re.search(pattern, query, re.IGNORECASE):
                # Check if followed by 'by' or 'without'
                agg_pattern = rf"\b{op}\s*(?:by|without)?\s*\("
                match = re.search(agg_pattern, query, re.IGNORECASE)
                if (
                    match
                    and "by" not in match.group().lower()
                    and "without" not in match.group().lower()
                ):
                    result.suggestions.append(
                        f"{op}() without explicit 'by' or 'without' clause aggregates across all labels. "
                        f"Consider adding 'by (label1, label2)' for clarity."
                    )

    def _check_histogram_quantile(self, query: str, result: ValidationResult) -> None:
        """Check histogram_quantile usage."""
        if "histogram_quantile" in query.lower():
            if "_bucket" not in query:
                result.errors.append(
                    "histogram_quantile() requires a metric with '_bucket' suffix. "
                    "Ensure you're using a histogram metric."
                )

            # Check for le label in by clause
            if "by" in query.lower() and "le" not in query.lower():
                result.warnings.append(
                    "histogram_quantile() aggregation should include 'le' label in by clause."
                )

    def _estimate_cardinality(self, query: str, result: ValidationResult) -> None:
        """Estimate query cardinality based on label matchers."""
        label_matches = self.LABEL_PATTERN.findall(query)

        if not label_matches:
            result.cardinality_estimate = None
            return

        # Count unique label constraints
        total_labels = 0
        constrained_labels = 0

        for labels_str in label_matches:
            # Count label matchers
            matchers = re.findall(r"(\w+)\s*[=!~]+", labels_str)
            total_labels += len(matchers)

            # Count equality matchers (more constrained)
            equality = re.findall(r'(\w+)\s*=\s*"[^"]*"', labels_str)
            constrained_labels += len(equality)

        # Rough estimate: fewer constraints = higher cardinality
        if constrained_labels >= 3:
            result.cardinality_estimate = 100  # Well constrained
        elif constrained_labels >= 2:
            result.cardinality_estimate = 1000
        elif constrained_labels >= 1:
            result.cardinality_estimate = 10000
        else:
            result.cardinality_estimate = 100000  # Poorly constrained

    def _check_recording_rule_candidate(
        self, query: str, result: ValidationResult
    ) -> None:
        """Determine if query is a good candidate for recording rule."""
        reasons = []

        # Complex aggregations
        agg_count = sum(1 for op in self.AGGREGATION_OPS if op in query.lower())
        if agg_count >= 2:
            reasons.append("Multiple aggregations")

        # Subqueries
        if self.SUBQUERY_PATTERN.search(query):
            reasons.append("Contains subquery")

        # Long range vectors
        for match in self.DURATION_PATTERN.finditer(query):
            value = int(match.group(1))
            unit = match.group(2)
            seconds = value * self.DURATION_MULTIPLIERS[unit]
            if seconds >= 3600:  # 1 hour or more
                reasons.append(f"Long range vector ({value}{unit})")

        # histogram_quantile is expensive
        if "histogram_quantile" in query.lower():
            reasons.append("Uses histogram_quantile()")

        if reasons:
            result.recording_rule_candidate = True
            result.suggestions.append(
                f"Recording rule candidate: {', '.join(reasons)}. "
                f"Consider creating a recording rule for better performance."
            )


def main():
    parser = argparse.ArgumentParser(description="Validate PromQL queries")
    parser.add_argument("query", nargs="?", help="PromQL query to validate")
    parser.add_argument("--file", "-f", help="File containing queries (one per line)")
    parser.add_argument(
        "--scrape-interval",
        "-s",
        type=int,
        default=15,
        help="Scrape interval in seconds (default: 15)",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.query and not args.file:
        parser.print_help()
        sys.exit(1)

    validator = PromQLValidator(scrape_interval=args.scrape_interval)
    results = []

    if args.query:
        results.append(validator.validate(args.query))

    if args.file:
        with open(args.file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    results.append(validator.validate(line))

    if args.json:
        output = [r.to_dict() for r in results]
        print(json.dumps(output, indent=2))
    else:
        for result in results:
            print(f"\nQuery: {result.query}")
            print(f"Valid: {result.valid_syntax}")
            print(
                f"Verdict: {'PASS' if result.valid_syntax and not result.errors else 'FAIL'}"
            )

            if result.errors:
                print("Errors:")
                for e in result.errors:
                    print(f"  ❌ {e}")

            if result.warnings:
                print("Warnings:")
                for w in result.warnings:
                    print(f"  ⚠️  {w}")

            if result.suggestions:
                print("Suggestions:")
                for s in result.suggestions:
                    print(f"  💡 {s}")

            if result.cardinality_estimate:
                print(f"Cardinality estimate: ~{result.cardinality_estimate} series")

            if result.recording_rule_candidate:
                print("Recording rule: Recommended")


if __name__ == "__main__":
    main()
