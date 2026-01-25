#!/usr/bin/env python3
"""Verify backtest environment prerequisites.

This script validates that all required components are in place before
executing backtests. It checks for Lean CLI installation, environment
variables, and required configuration files.

Usage Examples:
    # Check local backtest environment
    uv run python verify_backtest_env.py --mode local

    # Check cloud backtest environment (includes API credentials)
    uv run python verify_backtest_env.py --mode cloud

    # Verbose output
    uv run python verify_backtest_env.py --mode local --verbose

Exit Codes:
    0: All checks passed
    1: TRENDY_TRADER_PATH not set or invalid
    2: Configuration files missing
    3: Lean CLI not installed
    4: Cloud credentials missing (cloud mode only)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from _common import Colors


def print_check(name: str, passed: bool, message: str = "") -> None:
    """Print a check result with color coding.

    Args:
        name: Name of the check.
        passed: Whether the check passed.
        message: Optional additional message.
    """
    status = (
        f"{Colors.GREEN}PASS{Colors.RESET}"
        if passed
        else f"{Colors.RED}FAIL{Colors.RESET}"
    )
    print(f"  [{status}] {name}")
    if message:
        indent = "         "
        print(f"{indent}{message}")


def check_lean_cli() -> tuple[bool, str]:
    """Check if Lean CLI is installed and accessible.

    Returns:
        Tuple of (passed, message).
    """
    # Check if lean is in PATH
    lean_path = shutil.which("lean")
    if not lean_path:
        return False, "Lean CLI not found in PATH. Install with: pip install lean"

    # Try to get version
    try:
        result = subprocess.run(
            ["lean", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, f"Version: {version}"
        return False, f"lean --version failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Lean CLI timed out"
    except Exception as e:
        return False, f"Error checking Lean CLI: {e}"


def check_trendy_trader_path() -> tuple[bool, str, str]:
    """Check if TRENDY_TRADER_PATH environment variable is set and valid.

    Returns:
        Tuple of (passed, message, path).
    """
    path = os.environ.get("TRENDY_TRADER_PATH", "")

    if not path:
        return False, "TRENDY_TRADER_PATH environment variable not set", ""

    path_obj = Path(path)
    if not path_obj.exists():
        return False, f"Path does not exist: {path}", path

    if not path_obj.is_dir():
        return False, f"Path is not a directory: {path}", path

    return True, f"Path: {path}", path


def check_config_file(trendy_trader_path: str, filename: str) -> tuple[bool, str]:
    """Check if a configuration file exists.

    Args:
        trendy_trader_path: Path to trendy-trader repository.
        filename: Configuration file name.

    Returns:
        Tuple of (passed, message).
    """
    if not trendy_trader_path:
        return False, "TRENDY_TRADER_PATH not set"

    config_path = Path(trendy_trader_path) / "quantconnect" / filename

    if not config_path.exists():
        return False, f"File not found: {config_path}"

    # Validate JSON structure
    try:
        with open(config_path, encoding="utf-8") as f:
            json.load(f)
        return True, f"Found: {config_path}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in {filename}: {e}"


def check_cloud_credentials() -> tuple[bool, str]:
    """Check if QC cloud credentials are set.

    Returns:
        Tuple of (passed, message).
    """
    user_id = os.environ.get("QC_API_USER_ID", "")
    api_token = os.environ.get("QC_API_TOKEN", "")

    if not user_id:
        return False, "QC_API_USER_ID environment variable not set"

    if not api_token:
        return False, "QC_API_TOKEN environment variable not set"

    # Mask token for display
    masked_token = (
        api_token[:4] + "..." + api_token[-4:] if len(api_token) > 8 else "****"
    )
    return True, f"User ID: {user_id}, Token: {masked_token}"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Verify backtest environment prerequisites.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0: All checks passed
  1: TRENDY_TRADER_PATH issue
  2: Configuration files missing
  3: Lean CLI not installed
  4: Cloud credentials missing
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["local", "cloud"],
        default="local",
        help="Verification mode: local (default) or cloud",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code based on verification results.
    """
    args = parse_args()

    print(f"\n{Colors.BOLD}Backtest Environment Verification{Colors.RESET}")
    print(f"Mode: {args.mode}\n")

    all_passed = True
    exit_code = 0

    # Check 1: Lean CLI
    print(f"{Colors.BLUE}Checking Lean CLI...{Colors.RESET}")
    lean_ok, lean_msg = check_lean_cli()
    print_check(
        "Lean CLI installed", lean_ok, lean_msg if args.verbose or not lean_ok else ""
    )
    if not lean_ok:
        all_passed = False
        exit_code = 3

    # Check 2: TRENDY_TRADER_PATH
    print(f"\n{Colors.BLUE}Checking TRENDY_TRADER_PATH...{Colors.RESET}")
    path_ok, path_msg, trendy_trader_path = check_trendy_trader_path()
    print_check(
        "TRENDY_TRADER_PATH set",
        path_ok,
        path_msg if args.verbose or not path_ok else "",
    )
    if not path_ok:
        all_passed = False
        if exit_code == 0:
            exit_code = 1

    # Check 3: tier-config.json
    print(f"\n{Colors.BLUE}Checking configuration files...{Colors.RESET}")
    tier_ok, tier_msg = check_config_file(trendy_trader_path, "tier-config.json")
    print_check(
        "tier-config.json exists",
        tier_ok,
        tier_msg if args.verbose or not tier_ok else "",
    )
    if not tier_ok:
        all_passed = False
        if exit_code == 0:
            exit_code = 2

    # Check 4: backtest-periods.json
    periods_ok, periods_msg = check_config_file(
        trendy_trader_path, "backtest-periods.json"
    )
    print_check(
        "backtest-periods.json exists",
        periods_ok,
        periods_msg if args.verbose or not periods_ok else "",
    )
    if not periods_ok:
        all_passed = False
        if exit_code == 0:
            exit_code = 2

    # Check 5: Cloud credentials (cloud mode only)
    if args.mode == "cloud":
        print(f"\n{Colors.BLUE}Checking cloud credentials...{Colors.RESET}")
        creds_ok, creds_msg = check_cloud_credentials()
        print_check(
            "QC API credentials set",
            creds_ok,
            creds_msg if args.verbose or not creds_ok else "",
        )
        if not creds_ok:
            all_passed = False
            if exit_code == 0:
                exit_code = 4

    # Summary
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    if all_passed:
        print(
            f"{Colors.GREEN}All checks passed! Environment is ready for backtesting.{Colors.RESET}\n"
        )
    else:
        print(
            f"{Colors.RED}Some checks failed. Please fix the issues above.{Colors.RESET}"
        )
        print("\nFix suggestions:")
        if exit_code == 1:
            print(
                "  - Set TRENDY_TRADER_PATH to point to your trendy-trader repository"
            )
            print('    export TRENDY_TRADER_PATH="/path/to/trendy-trader"')
        elif exit_code == 2:
            print("  - Ensure tier-config.json and backtest-periods.json exist in")
            print("    $TRENDY_TRADER_PATH/quantconnect/")
        elif exit_code == 3:
            print("  - Install Lean CLI: pip install lean")
        elif exit_code == 4:
            print("  - Set QC_API_USER_ID and QC_API_TOKEN environment variables")
            print('    export QC_API_USER_ID="your-user-id"')
            print('    export QC_API_TOKEN="your-api-token"')
        print()

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
