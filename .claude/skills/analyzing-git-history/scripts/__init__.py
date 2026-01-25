"""Git history analysis scripts for the analyzing-git-history skill.

This package provides CLI tools for:
- git_churn: Analyze git commit history and extract churn metrics
- calculate_hotspots: Calculate weighted hotspot scores from complexity and churn data

Usage:
    uv run python -m scripts.git_churn --repo-path . --output-file churn.json --days 90
    uv run python -m scripts.calculate_hotspots --complexity-file complexity.json --churn-file churn.json --output-file hotspots.json
"""

from .calculate_hotspots import HotspotEntry, HotspotResult, calculate_hotspots
from .git_churn import ChurnResult, FileStat, analyze_churn

__all__ = [
    "analyze_churn",
    "ChurnResult",
    "FileStat",
    "calculate_hotspots",
    "HotspotResult",
    "HotspotEntry",
]
