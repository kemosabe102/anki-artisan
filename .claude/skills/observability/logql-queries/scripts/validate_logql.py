#!/usr/bin/env python3
"""
LogQL Query Validator

Validates LogQL query syntax and best practices.

Usage:
    python validate_logql.py '{app="api"} |= "error"'
    python validate_logql.py --file queries.txt
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field


@dataclass
class LogQLValidationResult:
    """Result of LogQL validation."""

    query: str
    valid_syntax: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    anti_patterns: list[str] = field(default_factory=list)
    recommended_parser: str | None = None

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "valid_syntax": self.valid_syntax,
            "warnings": self.warnings,
            "errors": self.errors,
            "suggestions": self.suggestions,
            "anti_patterns": self.anti_patterns,
            "recommended_parser": self.recommended_parser,
            "verdict": "PASS" if self.valid_syntax and not self.errors else "FAIL",
        }


class LogQLValidator:
    """Validates LogQL queries for syntax and best practices."""

    # Parser types in preference order
    PARSERS = ["json", "logfmt", "pattern", "regexp", "unpack"]

    # Stream selector pattern
    STREAM_SELECTOR = re.compile(r"^\{[^}]+\}")

    # Label matcher pattern
    LABEL_MATCHER = re.compile(r'(\w+)\s*([=!~]+)\s*["`]([^"`]*)["`]')

    # Line filter patterns
    LINE_FILTERS = {
        "|=": "contains",
        "!=": "not contains",
        "|~": "regex match",
        "!~": "regex not match",
    }

    # Parser patterns
    PARSER_PATTERN = re.compile(r"\|\s*(json|logfmt|pattern|regexp|unpack)(?:\s|$|\|)")

    # High cardinality label patterns
    HIGH_CARD_LABELS = [
        "request_id",
        "trace_id",
        "user_id",
        "session_id",
        "correlation_id",
        "transaction_id",
        "order_id",
        "message_id",
    ]

    def validate(self, query: str) -> LogQLValidationResult:
        """Validate a LogQL query."""
        result = LogQLValidationResult(query=query)

        # Basic syntax checks
        self._check_stream_selector(query, result)
        self._check_brackets(query, result)
        self._check_quotes(query, result)

        if result.errors:
            result.valid_syntax = False
            return result

        # Anti-pattern checks (10 categories)
        self._check_parser_before_filter(query, result)
        self._check_high_cardinality_labels(query, result)
        self._check_expensive_regex(query, result)
        self._check_missing_stream_selector(query, result)
        self._check_json_on_non_json(query, result)
        self._check_unnecessary_line_format(query, result)
        self._check_multiple_regex_filters(query, result)
        self._check_unbounded_range(query, result)
        self._check_excessive_label_filters(query, result)
        self._check_case_sensitive_search(query, result)

        # Suggest parser based on query patterns
        self._suggest_parser(query, result)

        return result

    def _check_stream_selector(self, query: str, result: LogQLValidationResult) -> None:
        """Verify stream selector exists and is valid."""
        if not query.strip().startswith("{"):
            result.errors.append(
                'Query must start with a stream selector: {label="value"}'
            )
            return

        match = self.STREAM_SELECTOR.match(query.strip())
        if not match:
            result.errors.append("Invalid stream selector syntax")
            return

        selector = match.group(0)

        # Check for at least one label matcher
        if not self.LABEL_MATCHER.search(selector):
            result.warnings.append(
                "Stream selector has no label matchers. "
                'This will scan all streams - add filters like {app="name"}.'
            )

    def _check_brackets(self, query: str, result: LogQLValidationResult) -> None:
        """Check for balanced brackets."""
        for open_b, close_b, name in [
            ("{", "}", "curly braces"),
            ("(", ")", "parentheses"),
            ("[", "]", "square brackets"),
        ]:
            if query.count(open_b) != query.count(close_b):
                result.errors.append(f"Unbalanced {name}")

    def _check_quotes(self, query: str, result: LogQLValidationResult) -> None:
        """Check for balanced quotes."""
        for quote in ['"', "`"]:
            # Simple check - count should be even
            count = query.count(quote)
            if count % 2 != 0:
                result.errors.append(f"Unbalanced {quote} quotes")

    def _check_parser_before_filter(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #1: Parser before line filter (2-5x slowdown)."""
        # Find parser position
        parser_match = self.PARSER_PATTERN.search(query)
        if not parser_match:
            return

        parser_pos = parser_match.start()

        # Find first line filter position
        filter_patterns = [r"\|=", r"!=", r"\|~", r"!~"]
        filter_pos = None

        for pattern in filter_patterns:
            match = re.search(pattern, query)
            if match and (filter_pos is None or match.start() < filter_pos):
                filter_pos = match.start()

        if filter_pos is not None and parser_pos < filter_pos:
            result.anti_patterns.append("AP-01: Parser before line filter")
            result.warnings.append(
                "Parser (json/logfmt/etc) appears before line filter. "
                "Move line filters BEFORE parsers for 2-5x performance improvement. "
                'Example: {app="x"} |= "error" | json'
            )

    def _check_high_cardinality_labels(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #2: High cardinality labels in stream selector."""
        match = self.STREAM_SELECTOR.match(query.strip())
        if not match:
            return

        selector = match.group(0).lower()

        for label in self.HIGH_CARD_LABELS:
            if label in selector:
                result.anti_patterns.append("AP-02: High-cardinality stream label")
                result.errors.append(
                    f"High-cardinality label '{label}' in stream selector. "
                    'Use as filter expression instead: | request_id="abc"'
                )
                break

    def _check_expensive_regex(self, query: str, result: LogQLValidationResult) -> None:
        """Anti-pattern #3: Expensive regex patterns."""
        expensive_patterns = [
            (r'\|~\s*["`]\.+\*', "Leading .* is expensive"),
            (r'\|~\s*["`][^"]*\.\*[^"]*\.\*', "Multiple .* in regex"),
            (r'\|~\s*["`]\(\?i\)', "Case-insensitive regex - use |= with lower()"),
        ]

        for pattern, message in expensive_patterns:
            if re.search(pattern, query):
                result.anti_patterns.append("AP-03: Expensive regex")
                result.warnings.append(f"Expensive regex pattern: {message}")

    def _check_missing_stream_selector(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #4: Missing or empty stream selector."""
        if query.strip() in ["{}", "{  }", "{ }"]:
            result.anti_patterns.append("AP-04: Empty stream selector")
            result.errors.append(
                "Empty stream selector {} scans ALL logs. "
                'Add at least one label filter: {app="name"}'
            )

    def _check_json_on_non_json(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #5: Using json parser when logs aren't JSON."""
        # Check for explicit json parser with non-JSON filters
        if "| json" in query.lower():
            # If there's a line filter for common non-JSON patterns
            non_json_patterns = [
                r'\|=\s*["`]\d{4}-\d{2}-\d{2}',  # Date pattern
                r'\|=\s*["`]\[[A-Z]+\]',  # Log level [INFO]
                r'\|=\s*["`]<\w+>',  # XML-like tags
            ]

            for pattern in non_json_patterns:
                if re.search(pattern, query):
                    result.anti_patterns.append("AP-05: JSON parser on non-JSON logs")
                    result.suggestions.append(
                        "Log format may not be JSON. Consider logfmt or pattern parser."
                    )
                    break

    def _check_unnecessary_line_format(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #6: Using line_format when not needed."""
        if "| line_format" in query and "label_format" not in query:
            # Check if result is used
            if not re.search(r"line_format.*\|\s*(json|logfmt|pattern)", query):
                result.anti_patterns.append("AP-06: Unnecessary line_format")
                result.suggestions.append(
                    "line_format modifies log output but result isn't used. "
                    "Remove if not needed for display."
                )

    def _check_multiple_regex_filters(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #7: Multiple regex filters that could be combined."""
        regex_count = len(re.findall(r"\|~", query))

        if regex_count > 2:
            result.anti_patterns.append("AP-07: Multiple regex filters")
            result.suggestions.append(
                f"Query has {regex_count} regex filters. "
                "Consider combining into single regex with alternation (|) for better performance."
            )

    def _check_unbounded_range(self, query: str, result: LogQLValidationResult) -> None:
        """Anti-pattern #8: Queries without time range (API level)."""
        # This is more of an API-level check, but we can suggest
        if "range" not in query.lower() and "[" not in query:
            result.suggestions.append(
                "Query has no explicit time range. Ensure API call includes "
                "start/end parameters to avoid scanning entire retention period."
            )

    def _check_excessive_label_filters(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #9: Too many label filters in stream selector."""
        match = self.STREAM_SELECTOR.match(query.strip())
        if not match:
            return

        selector = match.group(0)
        label_count = len(self.LABEL_MATCHER.findall(selector))

        if label_count > 5:
            result.anti_patterns.append("AP-09: Excessive label filters")
            result.suggestions.append(
                f"Stream selector has {label_count} label filters. "
                "Consider reducing or moving some to line filter expressions."
            )

    def _check_case_sensitive_search(
        self, query: str, result: LogQLValidationResult
    ) -> None:
        """Anti-pattern #10: Case-sensitive search when case-insensitive needed."""
        # Check for common patterns that might need case-insensitivity
        error_patterns = ["error", "Error", "ERROR"]

        found_patterns = []
        for pattern in error_patterns:
            if f'|= "{pattern}"' in query or f"|= `{pattern}`" in query:
                found_patterns.append(pattern)

        if len(found_patterns) > 1:
            result.anti_patterns.append("AP-10: Multiple case variants")
            result.suggestions.append(
                "Multiple case variants in filters. Use regex for case-insensitive: "
                '|~ "(?i)error" or use |= "error" | __error__!=""`'
            )

    def _suggest_parser(self, query: str, result: LogQLValidationResult) -> None:
        """Suggest appropriate parser based on query patterns."""
        # Check what parser is currently used
        parser_match = self.PARSER_PATTERN.search(query)
        current_parser = parser_match.group(1) if parser_match else None

        # Analyze query for clues about log format
        if (
            "| json" in query.lower() or "{" in query[query.find("|=") :]
            if "|=" in query
            else False
        ):
            result.recommended_parser = "json"
        elif "=" in query and not re.search(r'["\']', query[query.find("}") :]):
            result.recommended_parser = "logfmt"
        elif re.search(r"\|=.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", query):
            result.recommended_parser = "pattern"  # IP addresses suggest access logs
        else:
            result.recommended_parser = "json"  # Default recommendation

        if current_parser and current_parser != result.recommended_parser:
            result.suggestions.append(
                f"Consider {result.recommended_parser} parser based on query patterns "
                f"(currently using {current_parser})."
            )


def main():
    parser = argparse.ArgumentParser(description="Validate LogQL queries")
    parser.add_argument("query", nargs="?", help="LogQL query to validate")
    parser.add_argument("--file", "-f", help="File containing queries (one per line)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.query and not args.file:
        parser.print_help()
        sys.exit(1)

    validator = LogQLValidator()
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

            if result.anti_patterns:
                print(f"Anti-patterns: {', '.join(result.anti_patterns)}")

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

            if result.recommended_parser:
                print(f"Recommended parser: {result.recommended_parser}")


if __name__ == "__main__":
    main()
