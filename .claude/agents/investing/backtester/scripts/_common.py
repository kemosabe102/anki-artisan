"""Shared utilities for backtester scripts.

This module provides common functionality used across multiple backtester scripts
to reduce code duplication and improve maintainability.
"""

import os
import sys
from pathlib import Path
from typing import Any

# Constants
MAX_JSON_DISPLAY_LENGTH = 2000


class Colors:
    """Terminal color codes for output formatting."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def get_trendy_trader_path() -> Path:
    """Get TRENDY_TRADER_PATH from environment.

    Returns:
        Path to trendy-trader repository.

    Raises:
        SystemExit: If environment variable not set.
    """
    path = os.environ.get("TRENDY_TRADER_PATH", "")
    if not path:
        print(
            f"{Colors.RED}ERROR: TRENDY_TRADER_PATH environment variable not set.{Colors.RESET}",
            file=sys.stderr,
        )
        print("\nSet it with:", file=sys.stderr)
        print('  export TRENDY_TRADER_PATH="/path/to/trendy-trader"', file=sys.stderr)
        sys.exit(1)
    return Path(path)


def get_gate_value(gates: dict, gate_name: str, default: Any = 0) -> Any:
    """Extract gate threshold value from gates configuration.

    Gates can be specified as either a direct value or a dict with a 'value' key.
    This helper normalizes access to handle both cases.

    Args:
        gates: Gates configuration dictionary.
        gate_name: Name of the gate to retrieve.
        default: Default value if gate not found.

    Returns:
        The gate threshold value.
    """
    gate = gates.get(gate_name, {})
    if isinstance(gate, dict):
        return gate.get("value", default)
    return gate if gate else default
