#!/usr/bin/env python3
"""
Technical Debt Report Generator.

Aggregates OODA phase outputs into a final technical debt report with
executive summary, detailed metrics, prioritized action items, and ROI analysis.

Input files expected:
    OBSERVE phase: complexity.json, duplication.json, churn.json
    ORIENT phase: hotspots.json, tdr.json, sig.json
    DECIDE phase: roi.json, priorities.json
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class Priority(str, Enum):
    """Priority levels for action items."""

    P1 = "P1"  # Quick wins - high impact, low effort
    P2 = "P2"  # Strategic - high impact, high effort
    P3 = "P3"  # Defer - low impact, high effort
    P4 = "P4"  # Opportunistic - low impact, low effort


class SQALEGrade(str, Enum):
    """SQALE maintainability grades based on TDR."""

    A = "A"  # TDR < 5%
    B = "B"  # TDR 5-10%
    C = "C"  # TDR 10-20%
    D = "D"  # TDR 20-50%
    E = "E"  # TDR > 50%


def get_sqale_grade(tdr_percent: float) -> SQALEGrade:
    """
    Map TDR percentage to SQALE grade.

    Args:
        tdr_percent: Technical Debt Ratio as percentage

    Returns:
        SQALE grade (A-E)
    """
    if tdr_percent < 5:
        return SQALEGrade.A
    elif tdr_percent < 10:
        return SQALEGrade.B
    elif tdr_percent < 20:
        return SQALEGrade.C
    elif tdr_percent < 50:
        return SQALEGrade.D
    else:
        return SQALEGrade.E


def get_sig_display(stars: int) -> str:
    """
    Create visual star display for SIG rating.

    Args:
        stars: Number of stars (1-5)

    Returns:
        Unicode star display string
    """
    stars = max(1, min(5, stars))
    return "\u2605" * stars + "\u2606" * (5 - stars)


def get_recommendation(sqale_grade: SQALEGrade, critical_hotspots: int) -> str:
    """
    Generate recommendation based on grade and hotspots.

    Args:
        sqale_grade: SQALE maintainability grade
        critical_hotspots: Number of critical hotspots

    Returns:
        Plain-language recommendation string
    """
    if sqale_grade in (SQALEGrade.A, SQALEGrade.B) and critical_hotspots == 0:
        return "Healthy codebase, continue current practices"
    elif sqale_grade == SQALEGrade.B and critical_hotspots <= 2:
        return "Monitor, minor fixes needed"
    elif sqale_grade == SQALEGrade.C:
        return "Plan targeted remediation for hotspots"
    elif sqale_grade == SQALEGrade.D:
        return "Significant debt, prioritize P1 actions"
    else:
        return "Critical state, immediate intervention required"


@dataclass
class ActionItem:
    """A prioritized remediation action."""

    priority: str
    file: str
    action: str
    effort_hours: float
    impact_score: float = 0.0
    debt_item_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "priority": self.priority,
            "file": self.file,
            "action": self.action,
            "effort_hours": self.effort_hours,
            "impact_score": self.impact_score,
            "debt_item_id": self.debt_item_id,
        }


@dataclass
class ExecutiveSummary:
    """Executive summary section of the report."""

    sqale_grade: str
    sig_stars: int
    sig_display: str
    tdr_percent: float
    critical_hotspots: int
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "sqale_grade": self.sqale_grade,
            "sig_stars": self.sig_stars,
            "sig_display": self.sig_display,
            "tdr_percent": self.tdr_percent,
            "critical_hotspots": self.critical_hotspots,
            "recommendation": self.recommendation,
        }


@dataclass
class ROIAnalysis:
    """ROI analysis for debt remediation."""

    investment_hours: float
    monthly_savings_hours: float
    break_even_months: float
    annual_savings_hours: float
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "investment_hours": self.investment_hours,
            "monthly_savings_hours": self.monthly_savings_hours,
            "break_even_months": round(self.break_even_months, 1),
            "annual_savings_hours": self.annual_savings_hours,
            "recommendation": self.recommendation,
        }


@dataclass
class TechDebtReport:
    """Complete technical debt report."""

    repo_name: str
    analysis_date: str
    executive_summary: ExecutiveSummary
    metrics: dict[str, Any]
    hotspots: list[dict[str, Any]]
    action_items: list[ActionItem]
    roi_analysis: ROIAnalysis

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "repo_name": self.repo_name,
            "analysis_date": self.analysis_date,
            "executive_summary": self.executive_summary.to_dict(),
            "metrics": self.metrics,
            "hotspots": self.hotspots,
            "action_items": [item.to_dict() for item in self.action_items],
            "roi_analysis": self.roi_analysis.to_dict(),
        }


@dataclass
class ReportConfig:
    """Configuration for report generation."""

    input_dir: Path
    output_file: Path
    repo_name: str
    generate_markdown: bool = False

    # Expected input files
    OBSERVE_FILES: list[str] = field(
        default_factory=lambda: ["complexity.json", "duplication.json", "churn.json"]
    )
    ORIENT_FILES: list[str] = field(
        default_factory=lambda: ["hotspots.json", "tdr.json", "sig.json"]
    )
    DECIDE_FILES: list[str] = field(
        default_factory=lambda: ["roi.json", "priorities.json"]
    )


def load_json_file(file_path: Path) -> dict[str, Any] | None:
    """
    Load and parse a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON as dict, or None if file doesn't exist or is invalid
    """
    if not file_path.exists():
        return None

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
        return None


def validate_inputs(config: ReportConfig) -> tuple[bool, list[str]]:
    """
    Validate that required input files exist.

    Args:
        config: Report configuration

    Returns:
        Tuple of (is_valid, list of missing files)
    """
    missing: list[str] = []

    all_expected = config.OBSERVE_FILES + config.ORIENT_FILES + config.DECIDE_FILES

    for filename in all_expected:
        file_path = config.input_dir / filename
        if not file_path.exists():
            missing.append(filename)

    is_valid = len(missing) == 0
    return is_valid, missing


def load_observe_data(config: ReportConfig) -> dict[str, Any]:
    """
    Load OBSERVE phase outputs: complexity, duplication, churn.

    Args:
        config: Report configuration

    Returns:
        Dictionary with observe phase data
    """
    complexity = load_json_file(config.input_dir / "complexity.json") or {}
    duplication = load_json_file(config.input_dir / "duplication.json") or {}
    churn = load_json_file(config.input_dir / "churn.json") or {}

    return {
        "complexity": complexity,
        "duplication": duplication,
        "churn": churn,
    }


def load_orient_data(config: ReportConfig) -> dict[str, Any]:
    """
    Load ORIENT phase outputs: hotspots, TDR, SIG ratings.

    Args:
        config: Report configuration

    Returns:
        Dictionary with orient phase data
    """
    hotspots = load_json_file(config.input_dir / "hotspots.json") or {}
    tdr = load_json_file(config.input_dir / "tdr.json") or {}
    sig = load_json_file(config.input_dir / "sig.json") or {}

    return {
        "hotspots": hotspots,
        "tdr": tdr,
        "sig": sig,
    }


def load_decide_data(config: ReportConfig) -> dict[str, Any]:
    """
    Load DECIDE phase outputs: ROI analysis, priorities.

    Args:
        config: Report configuration

    Returns:
        Dictionary with decide phase data
    """
    roi = load_json_file(config.input_dir / "roi.json") or {}
    priorities = load_json_file(config.input_dir / "priorities.json") or {}

    return {
        "roi": roi,
        "priorities": priorities,
    }


def build_executive_summary(
    orient_data: dict[str, Any],
    hotspots_list: list[dict[str, Any]],
) -> ExecutiveSummary:
    """
    Build executive summary from orient phase data.

    Args:
        orient_data: ORIENT phase outputs
        hotspots_list: List of hotspot dictionaries

    Returns:
        ExecutiveSummary object
    """
    # Extract TDR
    tdr_data = orient_data.get("tdr", {})
    tdr_percent = tdr_data.get("tdr_percent", 0.0)

    # Extract SIG stars
    sig_data = orient_data.get("sig", {})
    sig_stars = sig_data.get("overall_stars", 3)

    # Count critical hotspots (score > 7.0)
    critical_count = sum(1 for h in hotspots_list if h.get("hotspot_score", 0) > 7.0)

    # Calculate derived values
    sqale_grade = get_sqale_grade(tdr_percent)
    sig_display = get_sig_display(sig_stars)
    recommendation = get_recommendation(sqale_grade, critical_count)

    return ExecutiveSummary(
        sqale_grade=sqale_grade.value,
        sig_stars=sig_stars,
        sig_display=sig_display,
        tdr_percent=round(tdr_percent, 1),
        critical_hotspots=critical_count,
        recommendation=recommendation,
    )


def build_action_items(decide_data: dict[str, Any]) -> list[ActionItem]:
    """
    Build prioritized action items from decide phase data.

    Args:
        decide_data: DECIDE phase outputs

    Returns:
        List of ActionItem objects sorted by priority
    """
    priorities_data = decide_data.get("priorities", {})
    items_list = priorities_data.get("items", [])

    action_items: list[ActionItem] = []

    for item in items_list:
        action_items.append(
            ActionItem(
                priority=item.get("priority", "P4"),
                file=item.get("file", ""),
                action=item.get("action", "Review"),
                effort_hours=item.get("effort_hours", 0.0),
                impact_score=item.get("impact_score", 0.0),
                debt_item_id=item.get("debt_item_id", ""),
            )
        )

    # Sort by priority (P1 first)
    priority_order = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
    action_items.sort(key=lambda x: priority_order.get(x.priority, 4))

    return action_items


def build_roi_analysis(decide_data: dict[str, Any]) -> ROIAnalysis:
    """
    Build ROI analysis from decide phase data.

    Args:
        decide_data: DECIDE phase outputs

    Returns:
        ROIAnalysis object
    """
    roi_data = decide_data.get("roi", {})

    investment = roi_data.get("investment_hours", 0.0)
    monthly_savings = roi_data.get("monthly_savings_hours", 0.0)

    # Calculate break-even (avoid division by zero)
    if monthly_savings > 0:
        break_even = investment / monthly_savings
    else:
        break_even = float("inf")

    annual_savings = monthly_savings * 12

    # Determine recommendation based on break-even
    if break_even <= 3:
        recommendation = "APPROVE - Quick payback, high ROI"
    elif break_even <= 6:
        recommendation = "APPROVE - Reasonable payback period"
    elif break_even <= 12:
        recommendation = "DEFER - Consider for next quarter"
    else:
        recommendation = "REJECT - Payback too long, reassess scope"

    return ROIAnalysis(
        investment_hours=investment,
        monthly_savings_hours=monthly_savings,
        break_even_months=break_even,
        annual_savings_hours=annual_savings,
        recommendation=recommendation,
    )


def extract_hotspots(orient_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Extract and format hotspots from orient phase data.

    Args:
        orient_data: ORIENT phase outputs

    Returns:
        List of hotspot dictionaries sorted by score (descending)
    """
    hotspots_data = orient_data.get("hotspots", {})
    items = hotspots_data.get("items", [])

    # Sort by hotspot_score descending
    sorted_items = sorted(
        items,
        key=lambda x: x.get("hotspot_score", 0),
        reverse=True,
    )

    return sorted_items


def build_metrics(observe_data: dict[str, Any]) -> dict[str, Any]:
    """
    Build metrics section from observe phase data.

    Args:
        observe_data: OBSERVE phase outputs

    Returns:
        Dictionary with complexity, duplication, and churn metrics
    """
    return {
        "complexity": observe_data.get("complexity", {}),
        "duplication": observe_data.get("duplication", {}),
        "churn": observe_data.get("churn", {}),
    }


def generate_report(config: ReportConfig) -> TechDebtReport:
    """
    Generate complete technical debt report from OODA phase outputs.

    Args:
        config: Report configuration

    Returns:
        TechDebtReport object with all sections populated
    """
    # Load all phase data
    observe_data = load_observe_data(config)
    orient_data = load_orient_data(config)
    decide_data = load_decide_data(config)

    # Extract and process hotspots
    hotspots_list = extract_hotspots(orient_data)

    # Build report sections
    executive_summary = build_executive_summary(orient_data, hotspots_list)
    metrics = build_metrics(observe_data)
    action_items = build_action_items(decide_data)
    roi_analysis = build_roi_analysis(decide_data)

    # Get current timestamp
    analysis_date = datetime.now().isoformat(timespec="seconds")

    return TechDebtReport(
        repo_name=config.repo_name,
        analysis_date=analysis_date,
        executive_summary=executive_summary,
        metrics=metrics,
        hotspots=hotspots_list,
        action_items=action_items,
        roi_analysis=roi_analysis,
    )


def generate_markdown(report: TechDebtReport) -> str:
    """
    Generate markdown summary from report.

    Args:
        report: TechDebtReport object

    Returns:
        Markdown formatted string
    """
    summary = report.executive_summary
    lines: list[str] = []

    # Header
    lines.append(f"# Tech Debt Report: {report.repo_name}")
    lines.append("")
    lines.append(f"**Assessment Date**: {report.analysis_date}")
    lines.append(f"**TDR**: {summary.tdr_percent}% (Grade: {summary.sqale_grade})")
    lines.append(f"**SIG Rating**: {summary.sig_display}")
    lines.append(f"**Recommendation**: {summary.recommendation}")
    lines.append("")

    # Top Hotspots
    lines.append("## Top Hotspots")
    lines.append("")

    top_hotspots = report.hotspots[:3]
    if top_hotspots:
        for i, hotspot in enumerate(top_hotspots, 1):
            score = hotspot.get("hotspot_score", 0)
            severity = "CRITICAL" if score > 7 else "HIGH" if score > 5 else "MEDIUM"
            file_path = hotspot.get("file_path", "unknown")
            lines.append(f"{i}. `{file_path}` - Score: {score:.2f} - {severity}")
    else:
        lines.append("No hotspots identified.")
    lines.append("")

    return "\n".join(lines)


def append_action_items_markdown(report: TechDebtReport) -> str:
    """
    Generate markdown for action items section.

    Args:
        report: TechDebtReport object

    Returns:
        Markdown formatted string for action items
    """
    lines: list[str] = []

    lines.append("## Priority Action Items")
    lines.append("")

    if report.action_items:
        lines.append("| Priority | File | Action | Effort (hrs) |")
        lines.append("|----------|------|--------|--------------|")

        for item in report.action_items:
            lines.append(
                f"| {item.priority} | `{item.file}` | {item.action} | {item.effort_hours} |"
            )
    else:
        lines.append("No action items identified.")
    lines.append("")

    return "\n".join(lines)


def append_roi_markdown(report: TechDebtReport) -> str:
    """
    Generate markdown for ROI analysis section.

    Args:
        report: TechDebtReport object

    Returns:
        Markdown formatted string for ROI section
    """
    lines: list[str] = []
    roi = report.roi_analysis

    lines.append("## ROI Analysis")
    lines.append("")
    lines.append(f"- **Investment Required**: {roi.investment_hours} hours")
    lines.append(f"- **Monthly Savings**: {roi.monthly_savings_hours} hours")
    lines.append(f"- **Break-even**: {roi.break_even_months} months")
    lines.append(f"- **Annual Savings**: {roi.annual_savings_hours} hours")
    lines.append("")
    lines.append(f"**Recommendation**: {roi.recommendation}")
    lines.append("")

    return "\n".join(lines)


def generate_full_markdown(report: TechDebtReport) -> str:
    """
    Generate complete markdown report.

    Args:
        report: TechDebtReport object

    Returns:
        Complete markdown formatted report
    """
    parts = [
        generate_markdown(report),
        append_action_items_markdown(report),
        append_roi_markdown(report),
    ]

    return "\n".join(parts)


def main() -> None:
    """CLI entry point for report generation."""
    parser = argparse.ArgumentParser(
        description="Generate technical debt report from OODA phase outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Expected input files:
  OBSERVE phase: complexity.json, duplication.json, churn.json
  ORIENT phase:  hotspots.json, tdr.json, sig.json
  DECIDE phase:  roi.json, priorities.json

Example usage:
  python generate_report.py --input-dir ./analysis --output-file report.json --repo-name myproject
  python generate_report.py --input-dir ./analysis --output-file report.json --repo-name myproject --markdown
        """,
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing OODA phase output files",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Output file path for JSON report",
    )
    parser.add_argument(
        "--repo-name",
        type=str,
        required=True,
        help="Repository name for the report",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Also generate markdown summary (same path with .md extension)",
    )

    args = parser.parse_args()

    # Validate input directory exists
    if not args.input_dir.exists():
        print(
            f"Error: Input directory does not exist: {args.input_dir}", file=sys.stderr
        )
        sys.exit(1)

    if not args.input_dir.is_dir():
        print(
            f"Error: Input path is not a directory: {args.input_dir}", file=sys.stderr
        )
        sys.exit(1)

    # Create configuration
    config = ReportConfig(
        input_dir=args.input_dir,
        output_file=args.output_file,
        repo_name=args.repo_name,
        generate_markdown=args.markdown,
    )

    # Validate required input files exist
    is_valid, missing_files = validate_inputs(config)
    if not is_valid:
        print("Warning: Missing input files:", file=sys.stderr)
        for f in missing_files:
            print(f"  - {f}", file=sys.stderr)
        print("Proceeding with available data...", file=sys.stderr)

    # Generate report
    try:
        report = generate_report(config)
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)

    # Write JSON output
    try:
        output_json = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_text(output_json, encoding="utf-8")
        print(f"Report written to {args.output_file}")
    except OSError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate markdown if requested
    if config.generate_markdown:
        md_path = args.output_file.with_suffix(".md")
        try:
            markdown_content = generate_full_markdown(report)
            md_path.write_text(markdown_content, encoding="utf-8")
            print(f"Markdown summary written to {md_path}")
        except OSError as e:
            print(f"Error writing markdown file: {e}", file=sys.stderr)
            sys.exit(1)

    # Print summary to stdout
    summary = report.executive_summary
    print("\n--- Report Summary ---")
    print(f"Repository: {report.repo_name}")
    print(f"Grade: {summary.sqale_grade} | TDR: {summary.tdr_percent}%")
    print(f"SIG Rating: {summary.sig_display}")
    print(f"Critical Hotspots: {summary.critical_hotspots}")
    print(f"Action Items: {len(report.action_items)}")
    print(f"Recommendation: {summary.recommendation}")


if __name__ == "__main__":
    main()
