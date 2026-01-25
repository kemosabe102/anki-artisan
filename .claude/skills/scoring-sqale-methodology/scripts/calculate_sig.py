#!/usr/bin/env python3
"""Calculate SIG Star Rating from Technical Debt Ratio.

Reads TDR results and maps to SIG (Software Improvement Group)
star ratings using TDR-based thresholds.

Usage:
    python calculate_sig.py --tdr-file tdr_results.json \
                            --output-file sig_rating.json

SIG Star Mapping (from FORMULAS-ORIENT.md):
    5 stars: TDR <= 5%  (Excellent)
    4 stars: TDR <= 10% (Good)
    3 stars: TDR <= 20% (Average - market benchmark)
    2 stars: TDR <= 50% (Poor)
    1 star:  TDR > 50%  (Critical)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

# SIG star thresholds (TDR-based, from FORMULAS-ORIENT.md)
SIG_THRESHOLDS = [
    (5.0, 5, "Excellent"),
    (10.0, 4, "Good"),
    (20.0, 3, "Average"),
    (50.0, 2, "Poor"),
    (float("inf"), 1, "Critical"),
]

# Star display characters
STAR_FILLED = "\u2605"  # Black star
STAR_EMPTY = "\u2606"  # White star


class SIGResult(TypedDict):
    """SIG star rating result."""

    sig_stars: int
    sig_display: str
    tdr_percent: float
    interpretation: str


def load_tdr_file(file_path: Path) -> dict:
    """Load TDR results from JSON file.

    Args:
        file_path: Path to TDR results JSON file.

    Returns:
        Parsed TDR results.

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If file is not valid JSON.
        KeyError: If tdr_percent is missing from file.
    """
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    if "tdr_percent" not in data:
        raise KeyError("tdr_percent not found in TDR file")

    return data


def calculate_sig_rating(tdr_percent: float) -> tuple[int, str]:
    """Calculate SIG star rating from TDR percentage.

    Args:
        tdr_percent: Technical Debt Ratio as percentage.

    Returns:
        Tuple of (star count, interpretation label).
    """
    for threshold, stars, label in SIG_THRESHOLDS:
        if tdr_percent <= threshold:
            return stars, label

    # Fallback (should not reach here)
    return 1, "Critical"


def format_star_display(stars: int, max_stars: int = 5) -> str:
    """Format star rating as visual display.

    Args:
        stars: Number of filled stars (1-5).
        max_stars: Maximum number of stars to display.

    Returns:
        String with filled and empty star characters.
    """
    filled = STAR_FILLED * stars
    empty = STAR_EMPTY * (max_stars - stars)
    return filled + empty


def get_interpretation(stars: int) -> str:
    """Get detailed interpretation for star rating.

    Args:
        stars: SIG star rating (1-5).

    Returns:
        Interpretation string describing maintainability level.
    """
    interpretations = {
        5: "Exceptional maintainability - top 5% of industry",
        4: "Above average maintainability - top 30% of industry",
        3: "Average maintainability - industry median",
        2: "Below average maintainability - needs improvement",
        1: "Critical maintainability concerns - urgent action required",
    }
    return interpretations.get(stars, "Unknown rating")


def calculate_sig(tdr_file: Path) -> SIGResult:
    """Calculate SIG star rating from TDR results.

    Args:
        tdr_file: Path to TDR results JSON file.

    Returns:
        SIGResult with star rating and interpretation.
    """
    tdr_data = load_tdr_file(tdr_file)
    tdr_percent = tdr_data["tdr_percent"]

    stars, _ = calculate_sig_rating(tdr_percent)
    display = format_star_display(stars)
    interpretation = get_interpretation(stars)

    return SIGResult(
        sig_stars=stars,
        sig_display=display,
        tdr_percent=tdr_percent,
        interpretation=interpretation,
    )


def write_output(result: SIGResult, output_file: Path) -> None:
    """Write SIG result to JSON file.

    Args:
        result: SIG rating result.
        output_file: Path to output JSON file.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dict(result), f, indent=2)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Calculate SIG star rating from TDR results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--tdr-file",
        type=Path,
        required=True,
        help="Path to TDR results JSON file from calculate_tdr.py",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to output JSON file for SIG rating",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for SIG rating calculation.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args()

    try:
        result = calculate_sig(args.tdr_file)
        write_output(result, args.output_file)

        # Print summary to stdout
        print(f"SIG Rating: {result['sig_stars']} stars")
        print(f"Display: {result['sig_display']}")
        print(f"TDR: {result['tdr_percent']}%")
        print(f"Interpretation: {result['interpretation']}")
        print(f"Output written to: {args.output_file}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"Error: Missing required field - {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
