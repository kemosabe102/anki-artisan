#!/usr/bin/env python3
"""ROI and NPV calculation for tech debt remediation decisions.

Reads TDR (Tech Debt Ratio) from ORIENT phase and calculates:
- Current/future annual carrying costs
- Annual benefit from remediation
- Break-even period in months
- NPV over 3-year projection

CLI Usage:
    python calculate_roi.py --tdr-file <path> --team-budget <float> \\
        --target-tdr <float> --output-file <path>
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TypedDict


class TDRData(TypedDict):
    """Expected structure from TDR file."""

    current_tdr: float
    remediation_hours: float
    hourly_rate: float


@dataclass
class ROIResult:
    """Result of ROI calculation.

    Attributes:
        current_annual_cost: Annual carrying cost at current TDR
        future_annual_cost: Annual carrying cost at target TDR
        annual_benefit: Difference between current and future costs
        remediation_cost: One-time cost to fix the debt
        break_even_months: Months until remediation pays for itself
        npv_3_year: Net present value over 3 years at 10% discount
        recommendation: APPROVE if break-even < 18 months, else DEFER
    """

    current_annual_cost: float
    future_annual_cost: float
    annual_benefit: float
    remediation_cost: float
    break_even_months: float
    npv_3_year: float
    recommendation: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def load_tdr_file(file_path: Path) -> TDRData:
    """Load TDR data from JSON file.

    Args:
        file_path: Path to TDR JSON file from ORIENT phase

    Returns:
        TDRData with current_tdr, remediation_hours, hourly_rate

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If required fields are missing
    """
    if not file_path.exists():
        raise FileNotFoundError(f"TDR file not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    required_fields = ["current_tdr", "remediation_hours", "hourly_rate"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        raise ValueError(f"TDR file missing required fields: {missing}")

    return TDRData(
        current_tdr=float(data["current_tdr"]),
        remediation_hours=float(data["remediation_hours"]),
        hourly_rate=float(data["hourly_rate"]),
    )


def calculate_npv(
    annual_benefit: float,
    remediation_cost: float,
    years: int = 3,
    discount_rate: float = 0.10,
) -> float:
    """Calculate Net Present Value of remediation investment.

    Formula: NPV = annual_benefit * ((1 - (1 + r)^-n) / r) - remediation_cost

    This is the present value of an annuity formula.

    Args:
        annual_benefit: Annual savings from reduced TDR
        remediation_cost: One-time investment to fix debt
        years: Projection horizon (default: 3)
        discount_rate: Discount rate for NPV (default: 10%)

    Returns:
        Net present value of the investment
    """
    if discount_rate == 0:
        # Edge case: no discount
        pv_factor = float(years)
    else:
        pv_factor = (1 - (1 + discount_rate) ** -years) / discount_rate

    return annual_benefit * pv_factor - remediation_cost


def calculate_roi(
    current_tdr: float,
    target_tdr: float,
    team_budget: float,
    remediation_hours: float,
    hourly_rate: float,
) -> ROIResult:
    """Calculate ROI metrics for tech debt remediation.

    Uses the Annual Cost Model from FORMULAS-DECIDE.md:
    - Annual_Carrying_Cost = Team_Budget * (TDR / 100)
    - Annual_Savings = Current_Cost - Target_Cost
    - Break_Even_Months = Remediation_Cost / Monthly_Savings

    Args:
        current_tdr: Current Tech Debt Ratio (percentage)
        target_tdr: Target TDR after remediation (percentage)
        team_budget: Annual team budget in currency units
        remediation_hours: Hours required to fix the debt
        hourly_rate: Cost per hour for remediation work

    Returns:
        ROIResult with all calculated metrics
    """
    # Calculate annual carrying costs
    current_annual_cost = team_budget * (current_tdr / 100)
    future_annual_cost = team_budget * (target_tdr / 100)
    annual_benefit = current_annual_cost - future_annual_cost

    # Calculate remediation cost
    remediation_cost = remediation_hours * hourly_rate

    # Calculate break-even period
    if annual_benefit <= 0:
        # No benefit or negative benefit - infinite payback
        break_even_months = float("inf")
    else:
        monthly_benefit = annual_benefit / 12
        break_even_months = remediation_cost / monthly_benefit

    # Calculate NPV (3-year, 10% discount)
    npv_3_year = calculate_npv(annual_benefit, remediation_cost)

    # Decision based on break-even threshold
    if break_even_months <= 18:
        recommendation = "APPROVE"
    else:
        recommendation = "DEFER"

    return ROIResult(
        current_annual_cost=round(current_annual_cost, 2),
        future_annual_cost=round(future_annual_cost, 2),
        annual_benefit=round(annual_benefit, 2),
        remediation_cost=round(remediation_cost, 2),
        break_even_months=round(break_even_months, 1),
        npv_3_year=round(npv_3_year, 2),
        recommendation=recommendation,
    )


def main() -> int:
    """CLI entry point for ROI calculation.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Calculate ROI and NPV for tech debt remediation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python calculate_roi.py --tdr-file orient_output.json \\
        --team-budget 1800000 --target-tdr 10 --output-file roi_result.json
        """,
    )
    parser.add_argument(
        "--tdr-file",
        type=Path,
        required=True,
        help="Path to TDR JSON file from ORIENT phase",
    )
    parser.add_argument(
        "--team-budget",
        type=float,
        required=True,
        help="Annual team budget in currency units",
    )

    parser.add_argument(
        "--target-tdr",
        type=float,
        required=True,
        help="Target TDR percentage after remediation",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to write ROI result JSON",
    )

    args = parser.parse_args()

    try:
        # Load TDR data from ORIENT phase
        tdr_data = load_tdr_file(args.tdr_file)

        # Calculate ROI
        result = calculate_roi(
            current_tdr=tdr_data["current_tdr"],
            target_tdr=args.target_tdr,
            team_budget=args.team_budget,
            remediation_hours=tdr_data["remediation_hours"],
            hourly_rate=tdr_data["hourly_rate"],
        )

        # Write output
        output_path = args.output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)

        print(f"ROI analysis written to: {output_path}")
        print(f"Recommendation: {result.recommendation}")
        print(f"Break-even: {result.break_even_months} months")
        print(f"NPV (3-year): ${result.npv_3_year:,.2f}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in TDR file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
