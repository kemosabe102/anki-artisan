"""
Technical Debt Report Generation Scripts.

This package provides tools for aggregating OODA phase outputs into
final technical debt reports with executive summaries and action items.

Modules:
    generate_report: Final report aggregation from OODA phase outputs
"""

from .generate_report import (
    ActionItem,
    ExecutiveSummary,
    ReportConfig,
    TechDebtReport,
    generate_report,
)

__all__ = [
    "generate_report",
    "ReportConfig",
    "TechDebtReport",
    "ExecutiveSummary",
    "ActionItem",
]
