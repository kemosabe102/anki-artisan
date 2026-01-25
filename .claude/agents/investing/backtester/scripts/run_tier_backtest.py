#!/usr/bin/env python3
"""Run tier-based progressive backtests.

This script executes backtests across all periods defined for a specific tier
in tier-config.json. It supports checkpoint recovery for interrupted runs
and aggregates results at the end for gate validation.

Usage Examples:
    # Run Tier 1 backtest (sanity check)
    uv run python run_tier_backtest.py --algorithm StageAnalysisTrendMomentum --tier 1 \\
        --hypothesis-id HYP-20260115-STAGE2-001

    # Run with checkpoint resume
    uv run python run_tier_backtest.py --algorithm StageAnalysisTrendMomentum --tier 2 \\
        --hypothesis-id HYP-20260115-STAGE2-001 --resume

    # Save results to specific directory
    uv run python run_tier_backtest.py --algorithm StageAnalysisTrendMomentum --tier 3 \\
        --hypothesis-id HYP-20260115-STAGE2-001 --output-dir ./backtest-history/runs/

Environment Variables:
    TRENDY_TRADER_PATH: Path to trendy-trader repository (required)

Exit Codes:
    0: Success (all gates passed)
    1: TRENDY_TRADER_PATH not set
    2: Configuration error
    3: Backtest execution failed
    4: Gate validation failed
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import Colors, get_gate_value, get_trendy_trader_path


def load_tier_config(trendy_trader_path: Path) -> dict:
    """Load tier configuration from tier-config.json.

    Args:
        trendy_trader_path: Path to trendy-trader repository.

    Returns:
        Tier configuration dictionary.
    """
    config_path = trendy_trader_path / "quantconnect" / "tier-config.json"
    try:
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            f"{Colors.RED}ERROR: tier-config.json not found at {config_path}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(
            f"{Colors.RED}ERROR: Invalid JSON in tier-config.json: {e}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)


def load_backtest_periods(trendy_trader_path: Path) -> dict:
    """Load backtest periods from backtest-periods.json.

    Args:
        trendy_trader_path: Path to trendy-trader repository.

    Returns:
        Backtest periods dictionary.
    """
    periods_path = trendy_trader_path / "quantconnect" / "backtest-periods.json"
    try:
        with open(periods_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            f"{Colors.RED}ERROR: backtest-periods.json not found at {periods_path}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(
            f"{Colors.RED}ERROR: Invalid JSON in backtest-periods.json: {e}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)


def get_tier_periods(tier: int, tier_config: dict, periods_data: dict) -> list[dict]:
    """Get the list of periods for a specific tier.

    Args:
        tier: Tier number (1-4).
        tier_config: Tier configuration dictionary.
        periods_data: Backtest periods dictionary.

    Returns:
        List of period dictionaries with start_date, end_date, name, regime.
    """
    tier_key = f"tier_{tier}"
    tier_info = tier_config.get("tiers", {}).get(tier_key, {})

    if not tier_info:
        print(
            f"{Colors.RED}ERROR: Tier {tier} not found in tier-config.json{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)

    # For tiers 1-2, periods are explicitly listed
    if "periods" in tier_info and isinstance(tier_info["periods"], list):
        period_ids = []
        for p in tier_info["periods"]:
            if isinstance(p, dict):
                period_ids.append(p.get("id", ""))
            else:
                period_ids.append(p)

        # Resolve period IDs to full period data
        return resolve_period_ids(period_ids, periods_data)

    # For tiers 3-4, use development/validation groups
    if tier <= 3:
        group = "development"
    else:
        group = "validation"

    return get_periods_by_group(periods_data, group)


def resolve_period_ids(period_ids: list[str], periods_data: dict) -> list[dict]:
    """Resolve period IDs to full period data using exact matching.

    Args:
        period_ids: List of period identifiers.
        periods_data: Full periods data dictionary.

    Returns:
        List of resolved period dictionaries.
    """
    resolved = []
    all_periods = []

    # Collect all periods from all regime categories
    for category in periods_data.get("regime_categories", {}).values():
        if isinstance(category, dict) and "backtest_periods" in category:
            all_periods.extend(category["backtest_periods"])

    # Create lookup by normalized name (exact match only)
    period_lookup = {}
    for p in all_periods:
        name = p.get("name", "").lower().replace(" ", "_").replace("-", "_")
        period_lookup[name] = p

    for pid in period_ids:
        pid_normalized = pid.lower().replace("-", "_").replace(" ", "_")
        if pid_normalized in period_lookup:
            resolved.append(period_lookup[pid_normalized])
        else:
            print(
                f"{Colors.YELLOW}WARNING: Could not resolve period ID: {pid}{Colors.RESET}"
            )

    return resolved


def get_periods_by_group(periods_data: dict, group: str) -> list[dict]:
    """Get all periods belonging to a specific group.

    Args:
        periods_data: Full periods data dictionary.
        group: Group name ('development' or 'validation').

    Returns:
        List of period dictionaries in the specified group.
    """
    result = []
    for category in periods_data.get("regime_categories", {}).values():
        if isinstance(category, dict) and "backtest_periods" in category:
            for period in category["backtest_periods"]:
                if period.get("group") == group:
                    # Only include periods with available data
                    algo_config = period.get("algorithm_config", {})
                    if algo_config.get("data_available", False):
                        result.append(period)
    return result


class CheckpointManager:
    """Manage checkpoint files for resumable backtest runs."""

    def __init__(self, output_dir: Path, hypothesis_id: str, tier: int):
        """Initialize checkpoint manager.

        Args:
            output_dir: Directory for checkpoint files.
            hypothesis_id: Hypothesis identifier.
            tier: Tier number.
        """
        self.output_dir = output_dir
        self.hypothesis_id = hypothesis_id
        self.tier = tier
        self.checkpoint_file = (
            output_dir / f"checkpoint_{hypothesis_id}_tier{tier}.json"
        )
        self._cache: dict | None = None

    def load(self) -> dict:
        """Load checkpoint data with caching.

        Returns:
            Checkpoint dictionary with completed periods and results.
        """
        if self._cache is not None:
            return self._cache

        if not self.checkpoint_file.exists():
            self._cache = {"completed_periods": [], "results": [], "started_at": None}
            return self._cache

        try:
            with open(self.checkpoint_file, encoding="utf-8") as f:
                self._cache = json.load(f)
                return self._cache
        except json.JSONDecodeError:
            self._cache = {"completed_periods": [], "results": [], "started_at": None}
            return self._cache

    def save(self, checkpoint_data: dict) -> None:
        """Save checkpoint data and update cache.

        Args:
            checkpoint_data: Checkpoint dictionary to save.
        """
        self._cache = checkpoint_data
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2)

    def is_completed(self, period_name: str) -> bool:
        """Check if a period has been completed.

        Args:
            period_name: Name of the period.

        Returns:
            True if period is already completed.
        """
        checkpoint = self.load()
        return period_name in checkpoint.get("completed_periods", [])

    def add_result(self, period_name: str, result: dict) -> None:
        """Add a completed period result.

        Args:
            period_name: Name of the period.
            result: Result dictionary.
        """
        checkpoint = self.load()
        if checkpoint["started_at"] is None:
            checkpoint["started_at"] = datetime.now().isoformat()
        checkpoint["completed_periods"].append(period_name)
        checkpoint["results"].append(result)
        checkpoint["updated_at"] = datetime.now().isoformat()
        self.save(checkpoint)


def run_backtest(
    algorithm: str, start_date: str, end_date: str, qc_dir: Path, timeout: int = 600
) -> dict[str, Any]:
    """Run a single backtest for a period.

    Args:
        algorithm: Algorithm name.
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        qc_dir: QuantConnect directory path.
        timeout: Timeout in seconds.

    Returns:
        Dictionary with backtest results or error info.
    """
    print(f"  Running: {start_date} to {end_date}")

    try:
        # Run lean backtest command
        result = subprocess.run(
            [
                "lean",
                "backtest",
                f"Algorithms/{algorithm}",
                "--parameter",
                f"start_date={start_date}",
                "--parameter",
                f"end_date={end_date}",
            ],
            cwd=qc_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr or "Backtest failed",
                "stdout": result.stdout,
            }

        # Parse results from output or summary file
        return {
            "success": True,
            "stdout": result.stdout,
            "metrics": parse_backtest_output(result.stdout, qc_dir, algorithm),
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Backtest timed out after {timeout} seconds",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def parse_backtest_output(stdout: str, qc_dir: Path, algorithm: str) -> dict:
    """Parse backtest output to extract metrics.

    Args:
        stdout: Standard output from backtest command.
        qc_dir: QuantConnect directory path.
        algorithm: Algorithm name.

    Returns:
        Dictionary with parsed metrics.
    """
    metrics = {
        "sharpe_ratio": None,
        "max_drawdown": None,
        "total_trades": None,
        "win_rate": None,
        "total_return": None,
    }

    # Try to find and parse summary JSON file
    algo_dir = qc_dir / "Algorithms" / algorithm
    summary_files = list(algo_dir.glob("*-summary.json"))

    if summary_files:
        # Use most recent summary file
        latest_summary = max(summary_files, key=lambda p: p.stat().st_mtime)
        try:
            with open(latest_summary, encoding="utf-8") as f:
                summary = json.load(f)
                stats = summary.get("Statistics", {})
                metrics["sharpe_ratio"] = float(stats.get("Sharpe Ratio", 0))
                metrics["max_drawdown"] = float(
                    stats.get("Drawdown", "0").replace("%", "")
                )
                metrics["total_trades"] = int(stats.get("Total Trades", 0))
                metrics["win_rate"] = float(stats.get("Win Rate", "0").replace("%", ""))
                metrics["total_return"] = float(
                    stats.get("Net Profit", "0").replace("%", "")
                )
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(
                f"{Colors.YELLOW}    Warning: Could not parse summary: {e}{Colors.RESET}"
            )

    return metrics


def aggregate_results(results: list[dict]) -> dict:
    """Aggregate metrics from multiple period results.

    Args:
        results: List of result dictionaries from each period.

    Returns:
        Aggregated metrics dictionary.
    """
    successful_results = [r for r in results if r.get("success") and r.get("metrics")]

    if not successful_results:
        return {
            "avg_sharpe": None,
            "worst_drawdown": None,
            "total_trades": 0,
            "avg_win_rate": None,
            "periods_completed": 0,
            "periods_failed": len(results),
        }

    sharpe_values = [
        r["metrics"]["sharpe_ratio"]
        for r in successful_results
        if r["metrics"]["sharpe_ratio"] is not None
    ]
    drawdown_values = [
        r["metrics"]["max_drawdown"]
        for r in successful_results
        if r["metrics"]["max_drawdown"] is not None
    ]
    trade_counts = [
        r["metrics"]["total_trades"]
        for r in successful_results
        if r["metrics"]["total_trades"] is not None
    ]
    win_rates = [
        r["metrics"]["win_rate"]
        for r in successful_results
        if r["metrics"]["win_rate"] is not None
    ]

    return {
        "avg_sharpe": sum(sharpe_values) / len(sharpe_values)
        if sharpe_values
        else None,
        "worst_drawdown": min(drawdown_values) if drawdown_values else None,
        "total_trades": sum(trade_counts) if trade_counts else 0,
        "avg_win_rate": sum(win_rates) / len(win_rates) if win_rates else None,
        "periods_completed": len(successful_results),
        "periods_failed": len(results) - len(successful_results),
    }


def evaluate_gates(
    aggregated: dict, tier: int, tier_config: dict
) -> tuple[bool, list[str]]:
    """Evaluate tier-specific gates against aggregated results.

    Args:
        aggregated: Aggregated metrics dictionary.
        tier: Tier number.
        tier_config: Tier configuration dictionary.

    Returns:
        Tuple of (all_passed, list of failure reasons).
    """
    tier_key = f"tier_{tier}"
    gates = tier_config.get("tiers", {}).get(tier_key, {}).get("gates", {})
    failures = []

    # Check Sharpe minimum
    threshold = get_gate_value(gates, "sharpe_minimum", 0)
    if aggregated["avg_sharpe"] is not None and aggregated["avg_sharpe"] < threshold:
        failures.append(f"Sharpe {aggregated['avg_sharpe']:.2f} < {threshold} minimum")

    # Check max drawdown (try max_drawdown_absolute first, then max_drawdown)
    dd_threshold = get_gate_value(gates, "max_drawdown_absolute", None)
    if dd_threshold is None:
        dd_threshold = get_gate_value(gates, "max_drawdown", -50)
    if (
        aggregated["worst_drawdown"] is not None
        and aggregated["worst_drawdown"] < dd_threshold
    ):
        failures.append(
            f"Drawdown {aggregated['worst_drawdown']:.1f}% exceeds {dd_threshold}% limit"
        )

    # Check trade count
    trade_threshold = get_gate_value(gates, "trade_count_minimum", 0)
    if aggregated["total_trades"] < trade_threshold:
        failures.append(
            f"Trade count {aggregated['total_trades']} < {trade_threshold} minimum"
        )

    # Check win rate (tiers 2+)
    if tier >= 2:
        win_threshold = get_gate_value(gates, "win_rate_minimum", 0)
        if (
            aggregated["avg_win_rate"] is not None
            and aggregated["avg_win_rate"] < win_threshold
        ):
            failures.append(
                f"Win rate {aggregated['avg_win_rate']:.1f}% < {win_threshold}% minimum"
            )

    return len(failures) == 0, failures


def print_summary(
    aggregated: dict, passed: bool, failures: list[str], tier: int
) -> None:
    """Print a summary of backtest results.

    Args:
        aggregated: Aggregated metrics dictionary.
        passed: Whether all gates passed.
        failures: List of failure reasons.
        tier: Tier number.
    """
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}Tier {tier} Backtest Summary{Colors.RESET}")
    print(f"{'=' * 60}")

    print(f"\n{Colors.CYAN}Aggregated Metrics:{Colors.RESET}")
    print(
        f"  Average Sharpe:    {aggregated['avg_sharpe']:.3f}"
        if aggregated["avg_sharpe"]
        else "  Average Sharpe:    N/A"
    )
    print(
        f"  Worst Drawdown:    {aggregated['worst_drawdown']:.1f}%"
        if aggregated["worst_drawdown"]
        else "  Worst Drawdown:    N/A"
    )
    print(f"  Total Trades:      {aggregated['total_trades']}")
    print(
        f"  Average Win Rate:  {aggregated['avg_win_rate']:.1f}%"
        if aggregated["avg_win_rate"]
        else "  Average Win Rate:  N/A"
    )
    print(f"  Periods Completed: {aggregated['periods_completed']}")
    print(f"  Periods Failed:    {aggregated['periods_failed']}")

    print(f"\n{Colors.CYAN}Gate Evaluation:{Colors.RESET}")
    if passed:
        print(f"  {Colors.GREEN}ALL GATES PASSED{Colors.RESET}")
        print(
            f"\n  {Colors.GREEN}Tier {tier} PASS - Ready for Tier {tier + 1}{Colors.RESET}"
        )
    else:
        print(f"  {Colors.RED}GATES FAILED:{Colors.RESET}")
        for failure in failures:
            print(f"    - {failure}")
        print(f"\n  {Colors.RED}Tier {tier} FAIL - See failure analysis{Colors.RESET}")

    print(f"\n{'=' * 60}\n")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run tier-based progressive backtests.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Run Tier 1:
    %(prog)s --algorithm StageAnalysis --tier 1 --hypothesis-id HYP-001

  Resume interrupted run:
    %(prog)s --algorithm StageAnalysis --tier 2 --hypothesis-id HYP-001 --resume

  Save results:
    %(prog)s --algorithm StageAnalysis --tier 3 --hypothesis-id HYP-001 --output-dir ./results/
        """,
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        help="Name of the algorithm directory",
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        required=True,
        help="Tier level (1-4)",
    )
    parser.add_argument(
        "--hypothesis-id",
        required=True,
        help="Hypothesis identifier (e.g., HYP-20260115-STAGE2-001)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint if available",
    )
    parser.add_argument(
        "--output-dir",
        default="./backtest-history/runs/",
        help="Directory for output and checkpoint files",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout per backtest in seconds (default: 600)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code based on backtest results.
    """
    args = parse_args()

    print(f"\n{Colors.BOLD}Tier {args.tier} Backtest Execution{Colors.RESET}")
    print(f"Algorithm:    {args.algorithm}")
    print(f"Hypothesis:   {args.hypothesis_id}")
    print(f"Resume mode:  {args.resume}\n")

    # Setup paths
    trendy_trader_path = get_trendy_trader_path()
    qc_dir = trendy_trader_path / "quantconnect"
    output_dir = Path(args.output_dir)

    # Load configurations
    print(f"{Colors.BLUE}Loading configurations...{Colors.RESET}")
    tier_config = load_tier_config(trendy_trader_path)
    periods_data = load_backtest_periods(trendy_trader_path)

    # Get periods for this tier
    periods = get_tier_periods(args.tier, tier_config, periods_data)
    print(f"Found {len(periods)} periods for Tier {args.tier}")

    if not periods:
        print(
            f"{Colors.RED}ERROR: No periods found for Tier {args.tier}{Colors.RESET}",
            file=sys.stderr,
        )
        return 2

    # Initialize checkpoint manager
    checkpoint = CheckpointManager(output_dir, args.hypothesis_id, args.tier)

    # Load existing results if resuming
    results = []
    if args.resume:
        checkpoint_data = checkpoint.load()
        results = checkpoint_data.get("results", [])
        if results:
            print(
                f"{Colors.YELLOW}Resuming from checkpoint: {len(results)} periods already completed{Colors.RESET}"
            )

    # Execute backtests
    print(f"\n{Colors.BLUE}Executing backtests...{Colors.RESET}")
    for i, period in enumerate(periods, 1):
        period_name = period.get("name", f"Period_{i}")
        algo_config = period.get("algorithm_config", {})
        start_date = algo_config.get("start_date", period.get("start_date"))
        end_date = algo_config.get("end_date", period.get("end_date"))

        # Skip if already completed
        if args.resume and checkpoint.is_completed(period_name):
            print(
                f"\n[{i}/{len(periods)}] {Colors.YELLOW}Skipping (already completed):{Colors.RESET} {period_name}"
            )
            continue

        print(f"\n[{i}/{len(periods)}] {Colors.CYAN}{period_name}{Colors.RESET}")
        print(f"  Regime: {period.get('regime', 'unknown')}")

        # Check data availability
        if not algo_config.get("data_available", True):
            print(f"  {Colors.YELLOW}Skipping: Data not available{Colors.RESET}")
            continue

        # Run backtest
        result = run_backtest(
            args.algorithm, start_date, end_date, qc_dir, args.timeout
        )
        result["period_name"] = period_name
        result["regime"] = period.get("regime", "unknown")
        result["start_date"] = start_date
        result["end_date"] = end_date

        if result["success"]:
            print(f"  {Colors.GREEN}SUCCESS{Colors.RESET}")
            if result.get("metrics"):
                m = result["metrics"]
                if m.get("sharpe_ratio") is not None:
                    print(f"    Sharpe: {m['sharpe_ratio']:.3f}")
                if m.get("max_drawdown") is not None:
                    print(f"    Drawdown: {m['max_drawdown']:.1f}%")
                if m.get("total_trades") is not None:
                    print(f"    Trades: {m['total_trades']}")
        else:
            print(
                f"  {Colors.RED}FAILED: {result.get('error', 'Unknown error')}{Colors.RESET}"
            )

        results.append(result)
        checkpoint.add_result(period_name, result)

    # Aggregate results
    print(f"\n{Colors.BLUE}Aggregating results...{Colors.RESET}")
    aggregated = aggregate_results(results)

    # Evaluate gates
    print(f"{Colors.BLUE}Evaluating gates...{Colors.RESET}")
    passed, failures = evaluate_gates(aggregated, args.tier, tier_config)

    # Print summary
    print_summary(aggregated, passed, failures, args.tier)

    # Save final results
    final_results = {
        "hypothesis_id": args.hypothesis_id,
        "tier": args.tier,
        "algorithm": args.algorithm,
        "completed_at": datetime.now().isoformat(),
        "aggregated_metrics": aggregated,
        "gates_passed": passed,
        "gate_failures": failures,
        "period_results": results,
    }

    results_file = (
        output_dir
        / f"tier{args.tier}_{args.hypothesis_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2)
    print(f"Results saved to: {results_file}")

    return 0 if passed else 4


if __name__ == "__main__":
    sys.exit(main())
