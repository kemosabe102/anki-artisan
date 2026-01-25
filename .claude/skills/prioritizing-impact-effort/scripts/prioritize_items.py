#!/usr/bin/env python3
"""Impact/Effort prioritization for tech debt items.

Reads hotspots from ORIENT phase and assigns:
- Impact score (1-10) based on hotspot level
- Effort score (1-10) based on cyclomatic complexity
- Priority score using formula: (impact * 2) - effort
- Quadrant assignment (P1-P4)

CLI Usage:
    python prioritize_items.py --hotspots-file <path> --output-file <path>
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TypedDict


class HotspotItem(TypedDict):
    """Expected structure for a hotspot item."""

    file: str
    level: str  # CRITICAL, HIGH, MEDIUM, LOW
    cc: float  # Cyclomatic complexity


@dataclass
class PrioritizedItem:
    """A tech debt item with priority scores assigned.

    Attributes:
        file: File path of the hotspot
        impact: Impact score (1-10)
        effort: Effort score (1-10)
        priority_score: Calculated priority = (impact * 2) - effort
        quadrant: P1 (quick wins), P2 (strategic), P3 (defer), P4 (opportunistic)
    """

    file: str
    impact: int
    effort: int
    priority_score: int
    quadrant: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PrioritizationResult:
    """Result of prioritization with summary statistics.

    Attributes:
        items: List of prioritized items
        summary: Count of items in each quadrant
    """

    items: list[PrioritizedItem]
    summary: dict[str, int]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "items": [item.to_dict() for item in self.items],
            "summary": self.summary,
        }


# Impact score mapping based on hotspot level
IMPACT_BY_LEVEL: dict[str, int] = {
    "CRITICAL": 10,
    "HIGH": 7,
    "MEDIUM": 4,
    "LOW": 1,
}

# Effort score thresholds based on cyclomatic complexity
# Higher CC = more effort to refactor
EFFORT_THRESHOLDS: list[tuple[float, int]] = [
    (50, 10),  # CC >= 50: extreme effort
    (40, 9),  # CC >= 40
    (30, 8),  # CC >= 30
    (25, 7),  # CC >= 25
    (20, 6),  # CC >= 20
    (15, 5),  # CC >= 15
    (10, 4),  # CC >= 10
    (7, 3),  # CC >= 7
    (4, 2),  # CC >= 4
    (0, 1),  # CC < 4: minimal effort
]


def get_impact_score(level: str) -> int:
    """Get impact score from hotspot level.

    Args:
        level: Hotspot level (CRITICAL, HIGH, MEDIUM, LOW)

    Returns:
        Impact score (1-10)
    """
    return IMPACT_BY_LEVEL.get(level.upper(), 1)


def get_effort_score(cc: float) -> int:
    """Get effort score from cyclomatic complexity.

    Args:
        cc: Cyclomatic complexity value

    Returns:
        Effort score (1-10)
    """
    for threshold, score in EFFORT_THRESHOLDS:
        if cc >= threshold:
            return score
    return 1


def assign_quadrant(impact: int, effort: int) -> str:
    """Assign priority quadrant based on impact and effort.

    Quadrant definitions from FORMULAS-DECIDE.md:
    - P1 Quick Wins: High impact (>=6), Low effort (<=4)
    - P2 Strategic: High impact (>=6), High effort (>4)
    - P3 Defer: Low impact (<6), High effort (>4)
    - P4 Opportunistic: Low impact (<6), Low effort (<=4)

    Args:
        impact: Impact score (1-10)
        effort: Effort score (1-10)

    Returns:
        Quadrant identifier (P1, P2, P3, or P4)
    """
    high_impact = impact >= 6
    low_effort = effort <= 4

    if high_impact and low_effort:
        return "P1"
    elif high_impact and not low_effort:
        return "P2"
    elif not high_impact and not low_effort:
        return "P3"
    else:  # low impact and low effort
        return "P4"


def load_hotspots_file(file_path: Path) -> list[HotspotItem]:
    """Load hotspots data from JSON file.

    Args:
        file_path: Path to hotspots JSON file from ORIENT phase

    Returns:
        List of hotspot items

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If required fields are missing
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Hotspots file not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    # Handle both direct list and wrapped format
    if isinstance(data, list):
        hotspots = data
    elif isinstance(data, dict) and "hotspots" in data:
        hotspots = data["hotspots"]
    else:
        raise ValueError("Expected list or dict with 'hotspots' key")

    # Validate each hotspot has required fields
    validated: list[HotspotItem] = []
    for i, item in enumerate(hotspots):
        if not isinstance(item, dict):
            raise ValueError(f"Hotspot {i} is not a dict")

        missing = []
        if "file" not in item:
            missing.append("file")
        if "level" not in item:
            missing.append("level")
        if "cc" not in item:
            missing.append("cc")

        if missing:
            raise ValueError(f"Hotspot {i} missing fields: {missing}")

        validated.append(
            HotspotItem(
                file=str(item["file"]),
                level=str(item["level"]),
                cc=float(item["cc"]),
            )
        )

    return validated


def prioritize_items(hotspots: list[HotspotItem]) -> PrioritizationResult:
    """Prioritize hotspots based on impact and effort.

    Args:
        hotspots: List of hotspot items from ORIENT phase

    Returns:
        PrioritizationResult with scored items and summary
    """
    items: list[PrioritizedItem] = []
    summary = {"p1_count": 0, "p2_count": 0, "p3_count": 0, "p4_count": 0}

    for hotspot in hotspots:
        impact = get_impact_score(hotspot["level"])
        effort = get_effort_score(hotspot["cc"])
        priority_score = (impact * 2) - effort
        quadrant = assign_quadrant(impact, effort)

        item = PrioritizedItem(
            file=hotspot["file"],
            impact=impact,
            effort=effort,
            priority_score=priority_score,
            quadrant=quadrant,
        )
        items.append(item)

        # Update summary counts
        summary[f"{quadrant.lower()}_count"] += 1

    # Sort by priority score descending
    items.sort(key=lambda x: x.priority_score, reverse=True)

    return PrioritizationResult(items=items, summary=summary)


def main() -> int:
    """CLI entry point for impact/effort prioritization.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Prioritize tech debt items by impact and effort",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python prioritize_items.py --hotspots-file hotspots.json \\
        --output-file prioritized.json
        """,
    )
    parser.add_argument(
        "--hotspots-file",
        type=Path,
        required=True,
        help="Path to hotspots JSON file from ORIENT phase",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to write prioritized items JSON",
    )

    args = parser.parse_args()

    try:
        # Load hotspots from ORIENT phase
        hotspots = load_hotspots_file(args.hotspots_file)

        # Prioritize items
        result = prioritize_items(hotspots)

        # Write output
        output_path = args.output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)

        print(f"Prioritization written to: {output_path}")
        print(f"Total items: {len(result.items)}")
        print(f"P1 (Quick Wins): {result.summary['p1_count']}")
        print(f"P2 (Strategic): {result.summary['p2_count']}")
        print(f"P3 (Defer): {result.summary['p3_count']}")
        print(f"P4 (Opportunistic): {result.summary['p4_count']}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in hotspots file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
