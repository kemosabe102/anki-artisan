#!/usr/bin/env python3
"""
Log Format Detector

Detects log format from sample lines and recommends appropriate LogQL parser.

Usage:
    python detect_log_format.py "sample log line"
    python detect_log_format.py --file sample.log
    cat sample.log | python detect_log_format.py --stdin
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass


@dataclass
class FormatDetectionResult:
    """Result of log format detection."""

    detected_format: str
    confidence: float
    recommended_parser: str
    sample_line: str
    details: dict

    def to_dict(self) -> dict:
        return {
            "detected_format": self.detected_format,
            "confidence": self.confidence,
            "recommended_parser": self.recommended_parser,
            "sample_line": self.sample_line[:100] + "..."
            if len(self.sample_line) > 100
            else self.sample_line,
            "details": self.details,
        }


class LogFormatDetector:
    """Detects log format and recommends appropriate parser."""

    # Common timestamp patterns
    TIMESTAMP_PATTERNS = [
        (r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "ISO8601"),
        (r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "datetime"),
        (r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}", "CLF"),
        (r"\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}", "syslog"),
        (r"\d{10,13}", "unix_epoch"),
    ]

    # Log level patterns
    LOG_LEVELS = [
        "DEBUG",
        "INFO",
        "WARN",
        "WARNING",
        "ERROR",
        "FATAL",
        "CRITICAL",
        "TRACE",
    ]

    def detect(self, line: str) -> FormatDetectionResult:
        """Detect format of a single log line."""
        line = line.strip()

        # Try detection methods in order of specificity
        detectors = [
            self._detect_json,
            self._detect_logfmt,
            self._detect_clf,  # Common Log Format (Apache/Nginx)
            self._detect_syslog,
            self._detect_structured,  # Generic structured
            self._detect_unstructured,  # Fallback
        ]

        for detector in detectors:
            result = detector(line)
            if result and result.confidence >= 0.6:
                return result

        # Fallback to unstructured
        return self._detect_unstructured(line)

    def detect_from_samples(self, lines: list[str]) -> FormatDetectionResult:
        """Detect format from multiple sample lines."""
        if not lines:
            return FormatDetectionResult(
                detected_format="unknown",
                confidence=0.0,
                recommended_parser="regexp",
                sample_line="",
                details={"error": "No sample lines provided"},
            )

        # Detect format for each line
        format_counts = {}
        results = []

        for line in lines[:20]:  # Sample up to 20 lines
            if not line.strip():
                continue
            result = self.detect(line)
            results.append(result)
            fmt = result.detected_format
            format_counts[fmt] = format_counts.get(fmt, 0) + 1

        if not results:
            return FormatDetectionResult(
                detected_format="unknown",
                confidence=0.0,
                recommended_parser="regexp",
                sample_line="",
                details={"error": "No valid sample lines"},
            )

        # Find most common format
        most_common = max(format_counts, key=format_counts.get)
        confidence = format_counts[most_common] / len(results)

        # Get representative result
        for result in results:
            if result.detected_format == most_common:
                result.confidence = confidence
                result.details["sample_count"] = len(results)
                result.details["format_distribution"] = format_counts
                return result

        return results[0]

    def _detect_json(self, line: str) -> FormatDetectionResult | None:
        """Detect JSON formatted logs."""
        line = line.strip()

        if not (line.startswith("{") and line.endswith("}")):
            return None

        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                return None

            # Check for common log fields
            common_fields = [
                "level",
                "message",
                "msg",
                "time",
                "timestamp",
                "@timestamp",
                "ts",
            ]
            found_fields = [f for f in common_fields if f in data]

            confidence = 0.9 if found_fields else 0.7

            return FormatDetectionResult(
                detected_format="json",
                confidence=confidence,
                recommended_parser="json",
                sample_line=line,
                details={
                    "fields": list(data.keys())[:10],
                    "common_fields_found": found_fields,
                },
            )
        except json.JSONDecodeError:
            return None

    def _detect_logfmt(self, line: str) -> FormatDetectionResult | None:
        """Detect logfmt formatted logs (key=value pairs)."""
        # Pattern: key=value or key="value with spaces"
        pattern = r'(\w+)=(?:"[^"]*"|[^\s]+)'
        matches = re.findall(pattern, line)

        if len(matches) < 2:
            return None

        # Calculate what percentage of line is key=value pairs
        total_pairs = len(matches)
        line_words = len(line.split())

        # If most of the line is key=value pairs, it's likely logfmt
        if total_pairs >= 3 and total_pairs >= line_words * 0.3:
            return FormatDetectionResult(
                detected_format="logfmt",
                confidence=0.85,
                recommended_parser="logfmt",
                sample_line=line,
                details={"fields": matches[:10], "field_count": total_pairs},
            )

        return None

    def _detect_clf(self, line: str) -> FormatDetectionResult | None:
        """Detect Common Log Format (Apache/Nginx access logs)."""
        # CLF pattern: host ident authuser [date] "request" status bytes
        clf_pattern = r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d+) (\S+)'

        match = re.match(clf_pattern, line)
        if match:
            return FormatDetectionResult(
                detected_format="clf",
                confidence=0.95,
                recommended_parser="pattern",
                sample_line=line,
                details={
                    "pattern": '<ip> <ident> <user> [<timestamp>] "<request>" <status> <bytes>',
                    "host": match.group(1),
                    "status": match.group(6),
                },
            )

        # Combined Log Format (CLF + referrer + user-agent)
        combined_pattern = clf_pattern + r' "([^"]*)" "([^"]*)"'
        match = re.match(combined_pattern, line)
        if match:
            return FormatDetectionResult(
                detected_format="combined",
                confidence=0.95,
                recommended_parser="pattern",
                sample_line=line,
                details={
                    "pattern": '<ip> <ident> <user> [<timestamp>] "<request>" <status> <bytes> "<referer>" "<agent>"',
                    "host": match.group(1),
                    "status": match.group(6),
                },
            )

        return None

    def _detect_syslog(self, line: str) -> FormatDetectionResult | None:
        """Detect syslog formatted logs."""
        # RFC 3164 syslog: <priority>timestamp hostname tag: message
        # Simplified: Mon DD HH:MM:SS hostname process[pid]: message
        syslog_pattern = r"^(?:<\d+>)?(\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}) (\S+) (\S+?)(?:\[(\d+)\])?: (.+)$"

        match = re.match(syslog_pattern, line)
        if match:
            return FormatDetectionResult(
                detected_format="syslog",
                confidence=0.90,
                recommended_parser="pattern",
                sample_line=line,
                details={
                    "pattern": "<timestamp> <host> <process>[<pid>]: <message>",
                    "timestamp": match.group(1),
                    "host": match.group(2),
                    "process": match.group(3),
                },
            )

        return None

    def _detect_structured(self, line: str) -> FormatDetectionResult | None:
        """Detect generic structured logs with timestamp and level."""
        # Look for timestamp
        timestamp_found = None
        for pattern, name in self.TIMESTAMP_PATTERNS:
            if re.search(pattern, line):
                timestamp_found = name
                break

        # Look for log level
        level_found = None
        for level in self.LOG_LEVELS:
            if re.search(rf"\b{level}\b", line, re.IGNORECASE):
                level_found = level
                break

        if timestamp_found and level_found:
            return FormatDetectionResult(
                detected_format="structured",
                confidence=0.75,
                recommended_parser="pattern",
                sample_line=line,
                details={
                    "timestamp_format": timestamp_found,
                    "log_level": level_found,
                    "suggestion": "Use pattern parser with appropriate <placeholders>",
                },
            )

        return None

    def _detect_unstructured(self, line: str) -> FormatDetectionResult:
        """Fallback for unstructured logs."""
        details = {}

        # Try to find any useful patterns
        for pattern, name in self.TIMESTAMP_PATTERNS:
            if re.search(pattern, line):
                details["has_timestamp"] = name
                break

        for level in self.LOG_LEVELS:
            if re.search(rf"\b{level}\b", line, re.IGNORECASE):
                details["has_log_level"] = level
                break

        return FormatDetectionResult(
            detected_format="unstructured",
            confidence=0.5,
            recommended_parser="regexp",
            sample_line=line,
            details={
                **details,
                "suggestion": "Use regexp parser with custom pattern, or line_format for extraction",
            },
        )


def main():
    parser = argparse.ArgumentParser(description="Detect log format")
    parser.add_argument("line", nargs="?", help="Sample log line")
    parser.add_argument("--file", "-f", help="File containing sample logs")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    detector = LogFormatDetector()

    if args.stdin:
        lines = [line.strip() for line in sys.stdin]
        result = detector.detect_from_samples(lines)
    elif args.file:
        with open(args.file) as f:
            lines = [line.strip() for line in f]
        result = detector.detect_from_samples(lines)
    elif args.line:
        result = detector.detect(args.line)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\n{'=' * 50}")
        print("Log Format Detection Results")
        print(f"{'=' * 50}")
        print(f"Detected Format: {result.detected_format}")
        print(f"Confidence: {result.confidence:.0%}")
        print(f"Recommended Parser: {result.recommended_parser}")
        print(
            f"\nSample: {result.sample_line[:80]}{'...' if len(result.sample_line) > 80 else ''}"
        )
        print("\nDetails:")
        for key, value in result.details.items():
            print(f"  {key}: {value}")

        # Print LogQL example
        print(f"\n{'=' * 50}")
        print("Example LogQL Query:")
        print(f"{'=' * 50}")

        if result.recommended_parser == "json":
            print('{app="your-app"} | json | level="error"')
        elif result.recommended_parser == "logfmt":
            print('{app="your-app"} | logfmt | level="error"')
        elif result.recommended_parser == "pattern":
            print('{app="your-app"} | pattern `<timestamp> <level> <message>`')
        else:
            print('{app="your-app"} | regexp `(?P<level>\\w+): (?P<message>.+)`')


if __name__ == "__main__":
    main()
