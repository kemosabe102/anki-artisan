#!/usr/bin/env python3
"""Fetch comprehensive backtest reports from QuantConnect cloud.

This script retrieves complete backtest reporting data including statistics,
orders, and aggregated summaries from the QuantConnect API.

Usage Examples:
    # Single backtest comprehensive report
    python fetch_backtest_report.py --project-id 27218459 --backtest-id abc123 --output-dir ./reports/

    # Multiple backtests (comma-separated)
    python fetch_backtest_report.py --project-id 27218459 --backtest-ids abc123,def456 --output-dir ./reports/

    # All completed backtests for a project
    python fetch_backtest_report.py --project-id 27218459 --all --output-dir ./reports/

    # Generate summary comparison CSV only
    python fetch_backtest_report.py --project-id 27218459 --all --summary

Environment Variables:
    QC_API_USER_ID: QuantConnect API User ID (required)
    QC_API_TOKEN: QuantConnect API Token (required)

Exit Codes:
    0: Success
    1: Missing credentials
    2: API request failed
    3: Invalid arguments
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print(
        "ERROR: requests library not installed. Run: uv add requests", file=sys.stderr
    )
    sys.exit(1)

from _common import Colors

# API Base URL
BASE_URL = "https://www.quantconnect.com/api/v2"

# Statistics keys to extract for summary CSV
SUMMARY_STATISTICS_KEYS = [
    "Sharpe Ratio",
    "Total Return",
    "Drawdown",
    "Win Rate",
    "Total Trades",
]


def get_credentials() -> tuple[str, str]:
    """Load QC credentials from environment variables.

    Returns:
        Tuple of (user_id, api_token).

    Raises:
        SystemExit: If credentials are not set.
    """
    user_id = os.environ.get("QC_API_USER_ID", "")
    api_token = os.environ.get("QC_API_TOKEN", "")

    if not user_id or not api_token:
        print(
            f"{Colors.RED}ERROR: QC_API_USER_ID and QC_API_TOKEN environment variables must be set.{Colors.RESET}",
            file=sys.stderr,
        )
        print("\nSet them with:", file=sys.stderr)
        print('  export QC_API_USER_ID="your-user-id"', file=sys.stderr)
        print('  export QC_API_TOKEN="your-api-token"', file=sys.stderr)
        sys.exit(1)

    return user_id, api_token


def get_auth(user_id: str, api_token: str) -> tuple[tuple[str, str], dict[str, str]]:
    """Get timestamp-based hash authentication for QC API.

    QuantConnect API requires a timestamp and SHA256 hash of (api_token:timestamp).

    Args:
        user_id: API user ID.
        api_token: API token.

    Returns:
        Tuple of (auth_tuple, headers_dict) for use with requests.
    """
    timestamp = str(int(time.time()))
    hash_string = f"{api_token}:{timestamp}"
    api_hash = hashlib.sha256(hash_string.encode("utf-8")).hexdigest()
    return (user_id, api_hash), {"Timestamp": timestamp}


def list_backtests(project_id: str, user_id: str, api_token: str) -> list[dict]:
    """List all backtests for a project.

    Args:
        project_id: QuantConnect project ID.
        user_id: API user ID.
        api_token: API token.

    Returns:
        List of backtest dictionaries.

    Raises:
        SystemExit: If API request fails.
    """
    url = f"{BASE_URL}/backtests/list"
    params = {"projectId": project_id}

    print(
        f"{Colors.BLUE}Fetching backtest list for project {project_id}...{Colors.RESET}"
    )

    try:
        auth, headers = get_auth(user_id, api_token)
        response = requests.get(
            url, params=params, auth=auth, headers=headers, timeout=30
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(
            f"{Colors.RED}ERROR: API request failed: {e}{Colors.RESET}", file=sys.stderr
        )
        sys.exit(2)

    if not data.get("success"):
        print(
            f"{Colors.RED}ERROR: API returned error: {data}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)

    backtests = data.get("backtests", [])
    print(f"{Colors.GREEN}Found {len(backtests)} backtests{Colors.RESET}")
    return backtests


def fetch_backtest(
    project_id: str, backtest_id: str, user_id: str, api_token: str
) -> dict:
    """Fetch backtest data from QC API.

    Args:
        project_id: QuantConnect project ID.
        backtest_id: Specific backtest ID to fetch.
        user_id: API user ID.
        api_token: API token.

    Returns:
        Backtest result dictionary.

    Raises:
        SystemExit: If API request fails.
    """
    url = f"{BASE_URL}/backtests/read"
    params = {"projectId": project_id, "backtestId": backtest_id}

    print(f"{Colors.BLUE}Fetching backtest: {backtest_id}{Colors.RESET}")

    try:
        auth, headers = get_auth(user_id, api_token)
        response = requests.get(
            url, params=params, auth=auth, headers=headers, timeout=30
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(
            f"{Colors.RED}ERROR: API request failed: {e}{Colors.RESET}", file=sys.stderr
        )
        sys.exit(2)

    if not data.get("success"):
        print(
            f"{Colors.RED}ERROR: API returned error: {data}{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(2)

    print(f"{Colors.GREEN}Successfully fetched backtest{Colors.RESET}")
    return data


def extract_statistics(backtest_data: dict) -> dict[str, Any]:
    """Extract key statistics from backtest result.

    Args:
        backtest_data: Full backtest API response.

    Returns:
        Dictionary of extracted statistics.
    """
    result = backtest_data.get("result", {})
    statistics = result.get("Statistics", {})
    runtime_statistics = result.get("RuntimeStatistics", {})

    extracted = {
        "backtest_id": backtest_data.get("backtestId", ""),
        "name": backtest_data.get("name", ""),
        "created": backtest_data.get("created", ""),
        "completed": backtest_data.get("completed", ""),
        "progress": backtest_data.get("progress", 0),
    }

    # Add all statistics
    for key, value in statistics.items():
        extracted[f"stat_{key}"] = value

    # Add runtime statistics
    for key, value in runtime_statistics.items():
        extracted[f"runtime_{key}"] = value

    return extracted


def extract_orders(backtest_data: dict) -> list[dict[str, Any]]:
    """Extract orders from backtest result.

    Args:
        backtest_data: Full backtest API response.

    Returns:
        List of order dictionaries.
    """
    result = backtest_data.get("result", {})
    orders = result.get("Orders", {})

    order_list = []
    for order_id, order_data in orders.items():
        order_list.append(
            {
                "order_id": order_id,
                "symbol": order_data.get("Symbol", {}).get("Value", ""),
                "type": order_data.get("Type", ""),
                "quantity": order_data.get("Quantity", 0),
                "time": order_data.get("Time", ""),
                "price": order_data.get("Price", 0),
                "value": order_data.get("Value", 0),
                "status": order_data.get("Status", ""),
                "direction": order_data.get("Direction", ""),
                "tag": order_data.get("Tag", ""),
            }
        )

    return order_list


def save_report(
    backtest_data: dict,
    output_dir: Path,
    project_id: str,
) -> Path:
    """Save comprehensive backtest report to files.

    Creates the following files:
    - metadata.json: Download timestamp, IDs, name
    - results.json: Full API response
    - statistics.csv: Key metrics
    - orders.csv: Trade orders
    - runtime_statistics.csv: Memory, execution time

    Args:
        backtest_data: Full backtest API response.
        output_dir: Base output directory.
        project_id: Project ID for directory structure.

    Returns:
        Path to the created report directory.
    """
    backtest_id = backtest_data.get("backtestId", "unknown")
    backtest_name = backtest_data.get("name", "unnamed")
    # Sanitize name for filesystem
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in backtest_name)

    report_dir = output_dir / f"project_{project_id}" / f"{safe_name}_{backtest_id}"
    report_dir.mkdir(parents=True, exist_ok=True)

    print(f"{Colors.CYAN}Saving report to: {report_dir}{Colors.RESET}")

    # Save metadata
    metadata = {
        "download_timestamp": datetime.now().isoformat(),
        "project_id": project_id,
        "backtest_id": backtest_id,
        "backtest_name": backtest_name,
        "created": backtest_data.get("created", ""),
        "completed": backtest_data.get("completed", ""),
    }
    with open(report_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Save full results
    with open(report_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(backtest_data, f, indent=2)

    # Save statistics CSV
    statistics = extract_statistics(backtest_data)
    with open(report_dir / "statistics.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in statistics.items():
            writer.writerow([key, value])

    # Save orders CSV
    orders = extract_orders(backtest_data)
    if orders:
        with open(report_dir / "orders.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=orders[0].keys())
            writer.writeheader()
            writer.writerows(orders)
    else:
        # Create empty orders file with headers
        with open(report_dir / "orders.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "order_id",
                    "symbol",
                    "type",
                    "quantity",
                    "time",
                    "price",
                    "value",
                    "status",
                    "direction",
                    "tag",
                ]
            )

    # Save runtime statistics CSV
    result = backtest_data.get("result", {})
    runtime_stats = result.get("RuntimeStatistics", {})
    with open(
        report_dir / "runtime_statistics.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in runtime_stats.items():
            writer.writerow([key, value])

    print(f"{Colors.GREEN}Report saved successfully{Colors.RESET}")
    return report_dir


def generate_summary(
    backtest_results: list[dict],
    output_dir: Path,
    project_id: str,
) -> Path:
    """Generate summary CSV comparing multiple backtests.

    Args:
        backtest_results: List of backtest API responses.
        output_dir: Base output directory.
        project_id: Project ID for directory structure.

    Returns:
        Path to the generated summary CSV.
    """
    project_dir = output_dir / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)
    summary_path = project_dir / "summary.csv"

    print(f"{Colors.CYAN}Generating summary CSV...{Colors.RESET}")

    rows = []
    for backtest_data in backtest_results:
        result = backtest_data.get("result", {})
        statistics = result.get("Statistics", {})

        row = {
            "backtest_id": backtest_data.get("backtestId", ""),
            "name": backtest_data.get("name", ""),
            "created": backtest_data.get("created", ""),
            "sharpe_ratio": statistics.get("Sharpe Ratio", ""),
            "total_return": statistics.get(
                "Total Net Profit", statistics.get("Total Return", "")
            ),
            "drawdown": statistics.get("Drawdown", ""),
            "win_rate": statistics.get("Win Rate", ""),
            "total_trades": statistics.get(
                "Total Trades", statistics.get("Total Orders", "")
            ),
        }
        rows.append(row)

    if rows:
        fieldnames = [
            "backtest_id",
            "name",
            "created",
            "sharpe_ratio",
            "total_return",
            "drawdown",
            "win_rate",
            "total_trades",
        ]
        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    print(f"{Colors.GREEN}Summary saved to: {summary_path}{Colors.RESET}")
    return summary_path


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch comprehensive backtest reports from QuantConnect cloud.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single backtest report:
    %(prog)s --project-id 27218459 --backtest-id abc123 --output-dir ./reports/

  Multiple backtests:
    %(prog)s --project-id 27218459 --backtest-ids abc123,def456 --output-dir ./reports/

  All backtests with summary:
    %(prog)s --project-id 27218459 --all --output-dir ./reports/

  Summary only:
    %(prog)s --project-id 27218459 --all --summary
        """,
    )

    parser.add_argument(
        "--project-id",
        required=True,
        help="QuantConnect project ID",
    )
    parser.add_argument(
        "--backtest-id",
        help="Single backtest ID to fetch",
    )
    parser.add_argument(
        "--backtest-ids",
        help="Comma-separated list of backtest IDs to fetch",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch all completed backtests for the project",
    )
    parser.add_argument(
        "--output-dir",
        default="./reports",
        help="Directory to save reports (default: ./reports)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Generate summary comparison CSV only (no individual reports)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success).
    """
    args = parse_args()

    # Validate arguments
    if not args.backtest_id and not args.backtest_ids and not args.all:
        print(
            f"{Colors.RED}ERROR: One of --backtest-id, --backtest-ids, or --all must be specified{Colors.RESET}",
            file=sys.stderr,
        )
        return 3

    # Get credentials
    user_id, api_token = get_credentials()

    output_dir = Path(args.output_dir)

    # Determine which backtests to fetch
    backtest_ids_to_fetch: list[str] = []

    if args.backtest_id:
        backtest_ids_to_fetch = [args.backtest_id]
    elif args.backtest_ids:
        backtest_ids_to_fetch = [bid.strip() for bid in args.backtest_ids.split(",")]
    elif args.all:
        backtests = list_backtests(args.project_id, user_id, api_token)
        backtest_ids_to_fetch = [
            bt.get("backtestId", "") for bt in backtests if bt.get("backtestId")
        ]

    if not backtest_ids_to_fetch:
        print(
            f"{Colors.YELLOW}No backtests found to process{Colors.RESET}",
            file=sys.stderr,
        )
        return 0

    print(
        f"\n{Colors.BOLD}Processing {len(backtest_ids_to_fetch)} backtest(s)...{Colors.RESET}\n"
    )

    # Fetch all backtest data
    backtest_results: list[dict] = []
    for backtest_id in backtest_ids_to_fetch:
        try:
            result = fetch_backtest(args.project_id, backtest_id, user_id, api_token)
            backtest_results.append(result)
        except SystemExit:
            print(
                f"{Colors.YELLOW}Skipping backtest {backtest_id} due to error{Colors.RESET}"
            )
            continue

    if not backtest_results:
        print(
            f"{Colors.RED}ERROR: No backtests were successfully fetched{Colors.RESET}",
            file=sys.stderr,
        )
        return 2

    # Save individual reports (unless summary-only mode)
    if not args.summary:
        for result in backtest_results:
            save_report(result, output_dir, args.project_id)

    # Generate summary CSV (when multiple backtests or summary flag)
    if len(backtest_results) > 1 or args.summary:
        generate_summary(backtest_results, output_dir, args.project_id)

    print(
        f"\n{Colors.GREEN}{Colors.BOLD}Done! Processed {len(backtest_results)} backtest(s){Colors.RESET}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
