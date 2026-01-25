#!/usr/bin/env python3
"""
Component Selector - Random weighted component selection for reviews

This script implements the weighted random selection algorithm for choosing
components to review. Used by the component-reviewer Skill and CI workflows.

Usage:
    python component_selector.py [--count 3] [--category <category>]

Examples:
    # Select 3 random components (default)
    python component_selector.py

    # Select 5 random components
    python component_selector.py --count 5

    # Select all components in a specific category
    python component_selector.py --category agents
"""

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path

# Component weights (higher = more frequent reviews)
COMPONENT_WEIGHTS = {
    "agents": 1.5,  # Higher priority - core to system
    "commands": 1.2,  # Medium-high - user-facing
    "hooks": 1.0,  # Medium - security-critical
    "claude_docs": 0.9,  # Medium - documentation
    "core_infrastructure": 1.5,  # High - business logic
    "data_connectors": 1.3,  # Medium-high - reliability critical
    "api_layer": 1.4,  # High - security surface
    "tests": 1.0,  # Medium - quality foundation
    "specifications": 0.8,  # Medium-low - less frequently changed
    "plans": 0.7,  # Lower - stable after completion
    "guides": 0.7,  # Lower - documentation
    "scripts": 1.0,  # Medium - automation
    "ci_workflows": 1.1,  # Medium - cost/reliability
    "dependencies": 0.8,  # Medium-low - stable
}

# Component to directory mapping
COMPONENT_PATHS = {
    "agents": ".claude/agents",
    "commands": ".claude/commands",
    "hooks": ".claude/hooks",
    "claude_docs": ".claude/docs",
    "core_infrastructure": "packages/core",
    "data_connectors": "packages/connectors",
    "api_layer": "packages/api",
    "tests": "tests",
    "specifications": "docs/01-planning/specifications",
    "plans": "docs/02-planning",
    "guides": "docs/04-guides",
    "scripts": "scripts",
    "ci_workflows": ".github/workflows",
    "dependencies": ".",  # Root level files
}

# File patterns for each component
COMPONENT_PATTERNS = {
    "agents": ["*.md"],
    "commands": ["*.md"],
    "hooks": ["*.py"],
    "claude_docs": ["**/*.md", "**/*.json"],
    "core_infrastructure": ["**/*.py"],
    "data_connectors": ["**/*.py"],
    "api_layer": ["**/*.py"],
    "tests": ["**/*.py"],
    "specifications": ["**/*.md"],
    "plans": ["**/*.md"],
    "guides": ["**/*.md"],
    "scripts": ["**/*.py"],
    "ci_workflows": ["*.yml", "*.yaml"],
    "dependencies": ["pyproject.toml", "uv.lock"],
}


@dataclass
class Component:
    """Represents a reviewable component"""

    category: str
    path: str
    relative_path: str
    weight: float


class ComponentSelector:
    """Selects components for review using weighted random algorithm"""

    def __init__(self, repo_root: Path | None = None):
        """
        Initialize component selector

        Args:
            repo_root: Repository root directory (defaults to current directory)
        """
        self.repo_root = repo_root or Path.cwd()

    def discover_components(self, category: str | None = None) -> list[Component]:
        """
        Discover all components in repository

        Args:
            category: Optional category to filter (e.g., "agents", "tests")

        Returns:
            List of discovered components
        """
        components = []
        categories = [category] if category else COMPONENT_PATHS.keys()

        for cat in categories:
            if cat not in COMPONENT_PATHS:
                print(f"Warning: Unknown category '{cat}', skipping")
                continue

            base_path = self.repo_root / COMPONENT_PATHS[cat]
            if not base_path.exists():
                print(f"Warning: Path '{base_path}' does not exist, skipping")
                continue

            patterns = COMPONENT_PATTERNS[cat]
            weight = COMPONENT_WEIGHTS[cat]

            for pattern in patterns:
                if "**" in pattern:
                    # Recursive glob
                    for file_path in base_path.glob(pattern):
                        if file_path.is_file():
                            components.append(
                                Component(
                                    category=cat,
                                    path=str(file_path),
                                    relative_path=str(
                                        file_path.relative_to(self.repo_root)
                                    ),
                                    weight=weight,
                                )
                            )
                else:
                    # Non-recursive glob
                    for file_path in base_path.glob(pattern):
                        if file_path.is_file():
                            components.append(
                                Component(
                                    category=cat,
                                    path=str(file_path),
                                    relative_path=str(
                                        file_path.relative_to(self.repo_root)
                                    ),
                                    weight=weight,
                                )
                            )

        return components

    def select_random(
        self, components: list[Component], count: int = 3
    ) -> list[Component]:
        """
        Select random components using weighted algorithm

        Args:
            components: List of components to select from
            count: Number of components to select

        Returns:
            Selected components
        """
        if not components:
            return []

        # Ensure we don't try to select more than available
        count = min(count, len(components))

        # Extract weights for random.choices
        weights = [c.weight for c in components]

        # Select components (with replacement to honor weights)
        selected = random.choices(components, weights=weights, k=count)

        # Remove duplicates while preserving order and weight-based selection
        seen = set()
        unique_selected = []
        for comp in selected:
            if comp.relative_path not in seen:
                seen.add(comp.relative_path)
                unique_selected.append(comp)

        return unique_selected

    def select_by_category(self, category: str) -> list[Component]:
        """
        Select all components in a specific category

        Args:
            category: Component category

        Returns:
            All components in category
        """
        return self.discover_components(category=category)

    def get_component_info(self, component: Component) -> dict:
        """
        Get detailed information about a component

        Args:
            component: Component to get info for

        Returns:
            Component information dictionary
        """
        file_path = Path(component.path)

        return {
            "category": component.category,
            "path": component.relative_path,
            "size_bytes": file_path.stat().st_size,
            "weight": component.weight,
            "last_modified": file_path.stat().st_mtime,
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Select components for automated review",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Select 3 random components (default)
  python component_selector.py

  # Select 5 random components
  python component_selector.py --count 5

  # Select all components in a specific category
  python component_selector.py --category agents

  # Output as JSON
  python component_selector.py --count 3 --format json
        """,
    )

    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of components to select (default: 3)",
    )

    parser.add_argument(
        "--category",
        type=str,
        choices=list(COMPONENT_PATHS.keys()),
        help="Select all components in specific category",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root directory (default: current directory)",
    )

    args = parser.parse_args()

    # Initialize selector
    selector = ComponentSelector(repo_root=args.repo_root)

    # Select components
    if args.category:
        components = selector.select_by_category(args.category)
        selected = components  # All components in category
    else:
        all_components = selector.discover_components()
        selected = selector.select_random(all_components, count=args.count)

    # Output results
    if args.format == "json":
        output = {
            "selection_method": "category" if args.category else "random",
            "count": len(selected),
            "components": [selector.get_component_info(c) for c in selected],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'=' * 60}")
        print("Component Selection Results")
        print(f"{'=' * 60}")
        print(
            f"Method: {'All in category' if args.category else f'Weighted random (n={args.count})'}"
        )
        print(f"Total selected: {len(selected)}\n")

        for i, comp in enumerate(selected, 1):
            info = selector.get_component_info(comp)
            print(f"{i}. {comp.relative_path}")
            print(f"   Category: {comp.category}")
            print(f"   Weight: {comp.weight}")
            print(f"   Size: {info['size_bytes']:,} bytes")
            print()

        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
