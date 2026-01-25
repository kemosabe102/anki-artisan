#!/usr/bin/env python3
"""Fetch backtest logs and results from QuantConnect cloud.

This script retrieves backtest results from the QuantConnect API using
environment variables for authentication (QC_API_USER_ID, QC_API_TOKEN).

Usage Examples:
    # List recent backtests for a project
    uv run python fetch_backtest_logs.py --project-id 27218459 --list

    # Fetch specific backtest results
    uv run python fetch_backtest_logs.py --project-id 27218459 --backtest-id abc123

    # Save results to a directory
    uv run python fetch_backtest_logs.py --project-id 27218459 --backtest-id abc123 --output-dir ./results/

    # Fetch logs for a backtest
    uv run python fetch_backtest_logs.py --project-id 27218459 --backtest-id abc123 --logs

    # Fetch logs with a search filter
    uv run python fetch_backtest_logs.py --project-id 27218459 --backtest-id abc123 --logs --query "ERROR"

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
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print(
        "ERROR: requests library not installed. Run: uv add requests", file=sys.stderr
    )
    sys.exit(1)

from _common import MAX_JSON_DISPLAY_LENGTH, Colors


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


def list_backtests(
    project_id: str, user_id: str, api_token: str, limit: int = 10
) -> list[dict]:
    """List available backtests for a project.

    Args:
        project_id: QuantConnect project ID.
        user_id: API user ID.
        api_token: API token.
        limit: Maximum number of backtests to return.

    Returns:
        List of backtest dictionaries.
    """
    base_url = "https://www.quantconnect.com/api/v2"
    url = f"{base_url}/backtests/list"
    params = {"projectId": project_id}

    print(f"{Colors.BLUE}Fetching backtests for project {project_id}...{Colors.RESET}")

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
    print(f"{Colors.GREEN}Found {len(backtests)} backtests{Colors.RESET}\n")

    # Display limited results
    for bt in backtests[:limit]:
        backtest_id = bt.get("backtestId", "N/A")
        name = bt.get("name", "Unnamed")
        created = bt.get("created", "Unknown")
        print(f"  {Colors.BOLD}{backtest_id}{Colors.RESET}: {name}")
        print(f"    Created: {created}\n")

    return backtests[:limit]


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
    """
    base_url = "https://www.quantconnect.com/api/v2"
    url = f"{base_url}/backtests/read"
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


def fetch_logs(
    project_id: str, backtest_id: str, user_id: str, api_token: str, query: str = ""
) -> list[str]:
    """Fetch all logs from a backtest with pagination.

    Uses the /api/v2/backtests/read/log endpoint with POST requests.
    Paginates through results 200 records at a time with rate limiting.

    Args:
        project_id: QuantConnect project ID.
        backtest_id: Specific backtest ID to fetch logs for.
        user_id: API user ID.
        api_token: API token.
        query: Optional search filter string for logs.

    Returns:
        List of log strings from the backtest.
    """
    url = "https://www.quantconnect.com/api/v2/backtests/read/log"
    all_logs: list[str] = []
    start = 0
    page_size = 200

    query_info = f" (query='{query}')" if query else ""
    print(
        f"{Colors.BLUE}Fetching logs for backtest {backtest_id}{query_info}...{Colors.RESET}"
    )

    while True:
        body = {
            "projectId": int(project_id),
            "backtestId": backtest_id,
            "start": start,
            "end": start + page_size,
            "query": query,
        }

        try:
            auth, headers = get_auth(user_id, api_token)
            response = requests.post(
                url, json=body, auth=auth, headers=headers, timeout=30
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(
                f"{Colors.RED}ERROR: API request failed: {e}{Colors.RESET}",
                file=sys.stderr,
            )
            break

        if not data.get("success"):
            if start == 0:
                errors = data.get("errors", [])
                print(
                    f"{Colors.RED}ERROR: Failed to fetch logs: {errors}{Colors.RESET}",
                    file=sys.stderr,
                )
            break

        logs = data.get("logs", [])
        if not logs:
            break

        all_logs.extend(logs)

        # Check if we've received all logs (less than page_size means last page)
        if len(logs) < page_size:
            break

        start += page_size
        time.sleep(0.3)  # Rate limiting

    print(f"{Colors.GREEN}Fetched {len(all_logs)} log entries{Colors.RESET}")
    return all_logs


def save_logs(
    logs: list[str], output_dir: str, backtest_id: str, query: str = ""
) -> Path:
    """Save backtest logs to a JSON file.

    Args:
        logs: List of log strings.
        output_dir: Directory to save logs.
        backtest_id: Backtest ID for filename.
        query: Optional query string used to filter logs.

    Returns:
        Path to saved file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{backtest_id}_logs.json"
    filepath = output_path / filename

    result = {
        "backtest_id": backtest_id,
        "query": query,
        "total_logs": len(logs),
        "logs": logs,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"{Colors.GREEN}Logs saved to: {filepath}{Colors.RESET}")
    return filepath


def display_log_sample(logs: list[str]) -> None:
    """Display a sample of logs (first 10 and last 5).

    Args:
        logs: List of log strings to display.
    """
    if not logs:
        print(f"{Colors.YELLOW}No logs found{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}Total logs: {len(logs)}{Colors.RESET}")

    # Show first 10 logs
    first_count = min(10, len(logs))
    print(f"\n{Colors.CYAN}First {first_count} logs:{Colors.RESET}")
    for log in logs[:first_count]:
        # Truncate long log lines for display
        display_log = log[:150] + "..." if len(log) > 150 else log
        print(f"  {display_log}")

    # Show last 5 logs (if there are more than 15 total)
    if len(logs) > 15:
        print(f"\n{Colors.CYAN}Last 5 logs:{Colors.RESET}")
        for log in logs[-5:]:
            display_log = log[:150] + "..." if len(log) > 150 else log
            print(f"  {display_log}")

    print(f"\n{Colors.YELLOW}Use --output-dir to save all logs to a file{Colors.RESET}")


def save_results(data: dict, output_dir: str, backtest_id: str) -> Path:
    """Save backtest results to a JSON file.

    Args:
        data: Backtest result data.
        output_dir: Directory to save results.
        backtest_id: Backtest ID for filename.

    Returns:
        Path to saved file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backtest_{backtest_id}_{timestamp}.json"
    filepath = output_path / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"{Colors.GREEN}Results saved to: {filepath}{Colors.RESET}")
    return filepath


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch backtest logs and results from QuantConnect cloud.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List backtests:
    %(prog)s --project-id 27218459 --list

  Fetch specific backtest metadata:
    %(prog)s --project-id 27218459 --backtest-id abc123def456

  Save metadata to directory:
    %(prog)s --project-id 27218459 --backtest-id abc123 --output-dir ./results/

  Fetch logs for a backtest:
    %(prog)s --project-id 27218459 --backtest-id abc123 --logs

  Fetch logs with search filter:
    %(prog)s --project-id 27218459 --backtest-id abc123 --logs --query "Signal"

  Save logs to directory:
    %(prog)s --project-id 27218459 --backtest-id abc123 --logs --output-dir ./results/
        """,
    )

    parser.add_argument(
        "--project-id",
        required=True,
        help="QuantConnect project ID",
    )
    parser.add_argument(
        "--backtest-id",
        help="Specific backtest ID to fetch",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List recent backtests for the project",
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Fetch logs for the specified backtest (requires --backtest-id)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Optional search filter for logs (e.g., 'ERROR', 'Signal')",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save results (creates if not exists)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of backtests to list (default: 10)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success).
    """
    args = parse_args()

    # Validate arguments
    if not args.list and not args.backtest_id:
        print(
            f"{Colors.RED}ERROR: Either --list or --backtest-id must be specified{Colors.RESET}",
            file=sys.stderr,
        )
        return 3

    # Validate --logs requires --backtest-id
    if args.logs and not args.backtest_id:
        print(
            f"{Colors.RED}ERROR: --logs requires --backtest-id to be specified{Colors.RESET}",
            file=sys.stderr,
        )
        return 3

    # Validate --query requires --logs
    if args.query and not args.logs:
        print(
            f"{Colors.YELLOW}WARNING: --query has no effect without --logs flag{Colors.RESET}",
            file=sys.stderr,
        )

    # Get credentials
    user_id, api_token = get_credentials()

    if args.list:
        list_backtests(args.project_id, user_id, api_token, args.limit)
        return 0

    # Handle --logs mode
    if args.logs:
        logs = fetch_logs(
            args.project_id, args.backtest_id, user_id, api_token, args.query
        )

        if args.output_dir:
            save_logs(logs, args.output_dir, args.backtest_id, args.query)
        else:
            display_log_sample(logs)

        return 0

    # Fetch specific backtest metadata (default behavior)
    result = fetch_backtest(args.project_id, args.backtest_id, user_id, api_token)

    # Save or print results
    if args.output_dir:
        save_results(result, args.output_dir, args.backtest_id)
    else:
        print(f"\n{Colors.BOLD}API Response:{Colors.RESET}")
        result_json = json.dumps(result, indent=2)
        print(result_json[:MAX_JSON_DISPLAY_LENGTH])
        if len(result_json) > MAX_JSON_DISPLAY_LENGTH:
            print(
                f"\n{Colors.YELLOW}... (truncated, use --output-dir to save full results){Colors.RESET}"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
