#!/usr/bin/env python3
"""Initialize or sync a QuantConnect project.

This script handles project initialization and cloud synchronization for
QuantConnect algorithms. It validates project structure, creates config.json
if missing, and optionally syncs to the QuantConnect cloud.

Usage Examples:
    # Initialize a new algorithm project
    uv run python init_qc_project.py --algorithm StageAnalysisTrendMomentum

    # Sync existing project to cloud
    uv run python init_qc_project.py --algorithm StageAnalysisTrendMomentum --cloud-sync

    # Validate project structure only
    uv run python init_qc_project.py --algorithm StageAnalysisTrendMomentum --validate-only

Environment Variables:
    TRENDY_TRADER_PATH: Path to trendy-trader repository (required)

Exit Codes:
    0: Success
    1: TRENDY_TRADER_PATH not set
    2: Algorithm directory not found
    3: Project validation failed
    4: Cloud sync failed
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _common import Colors, get_trendy_trader_path


def get_algorithm_path(trendy_trader_path: Path, algorithm_name: str) -> Path:
    """Get path to algorithm directory.

    Args:
        trendy_trader_path: Path to trendy-trader repository.
        algorithm_name: Name of the algorithm.

    Returns:
        Path to algorithm directory.
    """
    return trendy_trader_path / "quantconnect" / "Algorithms" / algorithm_name


def validate_algorithm_directory(algo_path: Path) -> tuple[bool, list[str]]:
    """Validate that algorithm directory has required structure.

    Args:
        algo_path: Path to algorithm directory.

    Returns:
        Tuple of (is_valid, list of issues).
    """
    issues = []

    if not algo_path.exists():
        issues.append(f"Directory does not exist: {algo_path}")
        return False, issues

    if not algo_path.is_dir():
        issues.append(f"Path is not a directory: {algo_path}")
        return False, issues

    # Check for main.py or algorithm file
    py_files = list(algo_path.glob("*.py"))
    if not py_files:
        issues.append("No Python files found in algorithm directory")

    return len(issues) == 0, issues


def create_config_json(algo_path: Path, algorithm_name: str) -> Path:
    """Create config.json for the algorithm if it doesn't exist.

    Args:
        algo_path: Path to algorithm directory.
        algorithm_name: Name of the algorithm.

    Returns:
        Path to config.json file.
    """
    config_path = algo_path / "config.json"

    if config_path.exists():
        print(
            f"{Colors.YELLOW}config.json already exists, skipping creation{Colors.RESET}"
        )
        return config_path

    # Default config structure
    config = {
        "algorithm-language": "Python",
        "parameters": {},
        "description": f"{algorithm_name} algorithm configuration",
        "organization-id": "",
        "python-venv": "",
        "local-id": 0,
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print(f"{Colors.GREEN}Created config.json at {config_path}{Colors.RESET}")
    return config_path


def read_config_json(config_path: Path) -> dict:
    """Read existing config.json.

    Args:
        config_path: Path to config.json file.

    Returns:
        Configuration dictionary.
    """
    try:
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(
            f"{Colors.RED}ERROR reading config.json: {e}{Colors.RESET}", file=sys.stderr
        )
        return {}


def cloud_sync(algo_path: Path, algorithm_name: str) -> bool:
    """Sync project to QuantConnect cloud.

    Args:
        algo_path: Path to algorithm directory.
        algorithm_name: Name of the algorithm.

    Returns:
        True if sync succeeded, False otherwise.
    """
    print(
        f"\n{Colors.BLUE}Syncing {algorithm_name} to QuantConnect cloud...{Colors.RESET}"
    )

    # Change to quantconnect directory for lean commands
    qc_dir = algo_path.parent.parent

    try:
        result = subprocess.run(
            ["lean", "cloud", "push", "--project", f"Algorithms/{algorithm_name}"],
            cwd=qc_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            print(f"{Colors.GREEN}Successfully synced to cloud{Colors.RESET}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"{Colors.RED}Cloud sync failed{Colors.RESET}", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(
            f"{Colors.RED}Cloud sync timed out after 120 seconds{Colors.RESET}",
            file=sys.stderr,
        )
        return False
    except FileNotFoundError:
        print(
            f"{Colors.RED}Lean CLI not found. Install with: pip install lean{Colors.RESET}",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"{Colors.RED}Cloud sync error: {e}{Colors.RESET}", file=sys.stderr)
        return False


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize or sync a QuantConnect project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Initialize project:
    %(prog)s --algorithm StageAnalysisTrendMomentum

  Initialize and sync to cloud:
    %(prog)s --algorithm StageAnalysisTrendMomentum --cloud-sync

  Validate only (no changes):
    %(prog)s --algorithm StageAnalysisTrendMomentum --validate-only
        """,
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        help="Name of the algorithm directory",
    )
    parser.add_argument(
        "--cloud-sync",
        action="store_true",
        help="Sync project to QuantConnect cloud after initialization",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate project structure, make no changes",
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
        Exit code based on operation result.
    """
    args = parse_args()

    print(f"\n{Colors.BOLD}QuantConnect Project Initialization{Colors.RESET}")
    print(f"Algorithm: {args.algorithm}\n")

    # Get paths
    trendy_trader_path = get_trendy_trader_path()
    algo_path = get_algorithm_path(trendy_trader_path, args.algorithm)

    # Validate algorithm directory
    print(f"{Colors.BLUE}Validating project structure...{Colors.RESET}")
    is_valid, issues = validate_algorithm_directory(algo_path)

    if not is_valid:
        print(f"{Colors.RED}Validation failed:{Colors.RESET}")
        for issue in issues:
            print(f"  - {issue}")
        return 2

    print(f"{Colors.GREEN}Project structure valid{Colors.RESET}")

    if args.validate_only:
        print(
            f"\n{Colors.GREEN}Validation complete (--validate-only mode){Colors.RESET}"
        )
        return 0

    # Create config.json if needed
    print(f"\n{Colors.BLUE}Checking config.json...{Colors.RESET}")
    config_path = create_config_json(algo_path, args.algorithm)

    # Read and display config
    if args.verbose:
        config = read_config_json(config_path)
        if config:
            print("\nConfig contents:")
            print(json.dumps(config, indent=2))

    # Cloud sync if requested
    if args.cloud_sync:
        if not cloud_sync(algo_path, args.algorithm):
            return 4

    print(f"\n{Colors.GREEN}Project initialization complete!{Colors.RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
