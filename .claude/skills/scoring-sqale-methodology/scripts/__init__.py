"""SQALE Methodology Scoring Scripts.

This package provides scripts for calculating technical debt metrics
using the SQALE (Software Quality Assessment based on Lifecycle Expectations)
methodology and SIG (Software Improvement Group) star ratings.

Scripts:
    calculate_tdr: Calculate Technical Debt Ratio and assign SQALE grades
    calculate_sig: Calculate SIG star ratings from TDR scores
"""

from pathlib import Path

__version__ = "1.0.0"
__author__ = "Gauntlet Agents"

# Package directory for reference
SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent
