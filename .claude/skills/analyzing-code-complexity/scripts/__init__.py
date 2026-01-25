"""
Code Complexity Analysis Scripts.

This package provides tools for measuring code complexity and detecting duplication.

Modules:
    measure_complexity: Cyclomatic complexity analysis using Radon
    detect_duplication: Code duplication detection using Pylint
"""

from .detect_duplication import (
    DuplicateBlock,
    DuplicationResult,
    detect_duplication,
)
from .measure_complexity import (
    ComplexityResult,
    FunctionComplexity,
    RiskLevel,
    analyze_complexity,
)

__all__ = [
    "analyze_complexity",
    "ComplexityResult",
    "FunctionComplexity",
    "RiskLevel",
    "detect_duplication",
    "DuplicationResult",
    "DuplicateBlock",
]
