#!/usr/bin/env python3
"""
Grafana Dashboard Validator

Comprehensive validation of Grafana dashboard JSON against best practices.

Usage:
    python validate_dashboard.py dashboard.json
    python validate_dashboard.py --dir /path/to/dashboards/
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DashboardValidationResult:
    """Result of dashboard validation."""

    file_path: str
    title: str
    uid: str
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    panel_count: int = 0

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "title": self.title,
            "uid": self.uid,
            "valid": self.valid and not self.errors,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "panel_count": self.panel_count,
            "verdict": "PASS" if self.valid and not self.errors else "FAIL",
        }


class DashboardValidator:
    """Validates Grafana dashboard JSON for best practices."""

    # Schema version requirements
    MIN_SCHEMA_VERSION = 38

    # Grid constraints (24-column grid)
    GRID_COLUMNS = 24

    # Standard panel widths
    STANDARD_WIDTHS = [24, 12, 8, 6, 4, 3]

    # Standard panel heights by type
    STANDARD_HEIGHTS = {
        "row": 1,
        "stat": 4,
        "gauge": 6,
        "table": 8,
        "timeseries": 8,
        "graph": 8,
        "heatmap": 8,
        "barchart": 8,
        "piechart": 8,
        "text": 4,
        "logs": 10,
    }

    # WCAG 2.1 AA minimum contrast ratio
    MIN_CONTRAST_RATIO = 4.5

    def __init__(self):
        self.seen_panel_ids: set[int] = set()

    def validate_file(self, file_path: Path) -> DashboardValidationResult:
        """Validate a dashboard JSON file."""
        try:
            with open(file_path) as f:
                content = json.load(f)
        except json.JSONDecodeError as e:
            result = DashboardValidationResult(
                file_path=str(file_path), title="<JSON_ERROR>", uid="", valid=False
            )
            result.errors.append(f"Invalid JSON: {e}")
            return result
        except Exception as e:
            result = DashboardValidationResult(
                file_path=str(file_path), title="<FILE_ERROR>", uid="", valid=False
            )
            result.errors.append(f"Failed to read file: {e}")
            return result

        # Handle wrapped format (dashboard + meta)
        dashboard = content.get("dashboard", content)

        return self.validate(dashboard, str(file_path))

    def validate(
        self, dashboard: dict[str, Any], file_path: str = ""
    ) -> DashboardValidationResult:
        """Validate a dashboard dictionary."""
        result = DashboardValidationResult(
            file_path=file_path,
            title=dashboard.get("title", "<untitled>"),
            uid=dashboard.get("uid", ""),
        )

        self.seen_panel_ids.clear()

        # Structure validation
        self._validate_schema_version(dashboard, result)
        self._validate_uid(dashboard, result)
        self._validate_time_settings(dashboard, result)
        self._validate_templating(dashboard, result)

        # Panel validation
        panels = dashboard.get("panels", [])
        result.panel_count = len(panels)

        for panel in panels:
            self._validate_panel(panel, result)

            # Handle collapsed row panels
            if panel.get("type") == "row" and panel.get("collapsed"):
                for child_panel in panel.get("panels", []):
                    self._validate_panel(child_panel, result)

        # Grid layout validation
        self._validate_grid_layout(panels, result)

        return result

    def _validate_schema_version(
        self, dashboard: dict, result: DashboardValidationResult
    ) -> None:
        """Validate schema version."""
        version = dashboard.get("schemaVersion", 0)

        if version < self.MIN_SCHEMA_VERSION:
            result.warnings.append(
                f"Schema version {version} is outdated. "
                f"Recommend upgrading to {self.MIN_SCHEMA_VERSION}+ for Grafana 10.x/11.x compatibility."
            )

    def _validate_uid(self, dashboard: dict, result: DashboardValidationResult) -> None:
        """Validate dashboard UID."""
        uid = dashboard.get("uid", "")

        if not uid:
            result.errors.append(
                "Dashboard is missing 'uid'. Required for provisioning and API operations."
            )
        elif len(uid) < 8:
            result.warnings.append(
                f"Dashboard UID '{uid}' is short. Recommend 8-40 characters for uniqueness."
            )
        elif len(uid) > 40:
            result.errors.append(f"Dashboard UID '{uid}' exceeds 40 character limit.")

    def _validate_time_settings(
        self, dashboard: dict, result: DashboardValidationResult
    ) -> None:
        """Validate time settings."""
        time = dashboard.get("time", {})

        if not time:
            result.warnings.append(
                'Dashboard has no default time range. Add \'time: {from: "now-6h", to: "now"}\''
            )

        refresh = dashboard.get("refresh", "")
        if not refresh:
            result.suggestions.append(
                "Consider adding a default refresh interval: 'refresh: \"30s\"'"
            )

    def _validate_templating(
        self, dashboard: dict, result: DashboardValidationResult
    ) -> None:
        """Validate templating variables."""
        templating = dashboard.get("templating", {})
        variables = templating.get("list", [])

        # Check for datasource variable
        has_datasource_var = any(v.get("type") == "datasource" for v in variables)

        if not has_datasource_var:
            result.suggestions.append(
                "Consider adding a datasource variable for flexibility across environments."
            )

        # Check variable names
        for var in variables:
            name = var.get("name", "")
            if name and not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
                result.warnings.append(
                    f"Variable '{name}' has invalid characters. Use alphanumeric and underscores."
                )

    def _validate_panel(self, panel: dict, result: DashboardValidationResult) -> None:
        """Validate a single panel."""
        panel_id = panel.get("id")
        panel_type = panel.get("type", "")
        title = panel.get("title", "<untitled>")

        # Check panel ID
        if panel_id is None:
            result.errors.append(f"Panel '{title}' is missing 'id'.")
        elif panel_id in self.seen_panel_ids:
            result.errors.append(f"Duplicate panel ID {panel_id} for panel '{title}'.")
        else:
            self.seen_panel_ids.add(panel_id)

        # Check panel type
        if not panel_type:
            result.errors.append(f"Panel '{title}' is missing 'type'.")

        # Skip row panels for some checks
        if panel_type == "row":
            return

        # Check gridPos
        grid_pos = panel.get("gridPos", {})
        self._validate_grid_pos(grid_pos, panel_type, title, result)

        # Check targets (queries)
        targets = panel.get("targets", [])
        if not targets and panel_type not in ["row", "text"]:
            result.warnings.append(f"Panel '{title}' has no targets (queries).")

        for target in targets:
            self._validate_target(target, title, result)

        # Check description
        if not panel.get("description"):
            result.suggestions.append(
                f"Panel '{title}' has no description. Add one for documentation."
            )

        # Check field configuration
        self._validate_field_config(panel, title, result)

    def _validate_grid_pos(
        self,
        grid_pos: dict,
        panel_type: str,
        title: str,
        result: DashboardValidationResult,
    ) -> None:
        """Validate panel grid position."""
        if not grid_pos:
            result.errors.append(f"Panel '{title}' is missing 'gridPos'.")
            return

        x = grid_pos.get("x", 0)
        y = grid_pos.get("y", 0)
        w = grid_pos.get("w", 0)
        h = grid_pos.get("h", 0)

        # Check bounds
        if x < 0 or x >= self.GRID_COLUMNS:
            result.errors.append(f"Panel '{title}' has invalid x position: {x}")

        if y < 0:
            result.errors.append(f"Panel '{title}' has invalid y position: {y}")

        if w <= 0 or w > self.GRID_COLUMNS:
            result.errors.append(f"Panel '{title}' has invalid width: {w}")

        if x + w > self.GRID_COLUMNS:
            result.errors.append(
                f"Panel '{title}' exceeds grid width: x={x} + w={w} > {self.GRID_COLUMNS}"
            )

        if h <= 0:
            result.errors.append(f"Panel '{title}' has invalid height: {h}")

        # Check standard widths
        if w not in self.STANDARD_WIDTHS:
            result.suggestions.append(
                f"Panel '{title}' width {w} is non-standard. "
                f"Recommend: {self.STANDARD_WIDTHS}"
            )

        # Check standard heights
        standard_h = self.STANDARD_HEIGHTS.get(panel_type)
        if standard_h and h != standard_h and abs(h - standard_h) > 2:
            result.suggestions.append(
                f"Panel '{title}' ({panel_type}) height {h} differs from standard {standard_h}."
            )

    def _validate_target(
        self, target: dict, panel_title: str, result: DashboardValidationResult
    ) -> None:
        """Validate a panel target (query)."""
        expr = target.get("expr", "")

        if not expr:
            return

        # Check for PromQL best practices
        if "irate" in expr.lower():
            result.warnings.append(
                f"Panel '{panel_title}' uses irate() which is volatile. "
                "Consider rate() for more stable visualizations."
            )

        # Check for $__rate_interval usage
        if "rate(" in expr.lower() or "increase(" in expr.lower():
            if "$__rate_interval" not in expr:
                result.suggestions.append(
                    f"Panel '{panel_title}' uses rate/increase without $__rate_interval. "
                    "Consider using $__rate_interval for proper interval handling."
                )

        # Check legendFormat
        legend = target.get("legendFormat", "")
        if not legend:
            result.suggestions.append(
                f"Panel '{panel_title}' target has no legendFormat. "
                "Add one for readable legends: {{label_name}}"
            )

    def _validate_field_config(
        self, panel: dict, title: str, result: DashboardValidationResult
    ) -> None:
        """Validate panel field configuration."""
        field_config = panel.get("fieldConfig", {})
        defaults = field_config.get("defaults", {})

        # Check unit
        unit = defaults.get("unit")
        panel_type = panel.get("type", "")

        if not unit and panel_type in ["timeseries", "stat", "gauge"]:
            result.suggestions.append(
                f"Panel '{title}' has no unit configured. Add one for clarity."
            )

        # Check thresholds for stat/gauge
        if panel_type in ["stat", "gauge"]:
            thresholds = defaults.get("thresholds", {})
            steps = thresholds.get("steps", [])

            if len(steps) < 2:
                result.suggestions.append(
                    f"Panel '{title}' ({panel_type}) has few threshold steps. "
                    "Add thresholds for visual feedback."
                )

    def _validate_grid_layout(
        self, panels: list[dict], result: DashboardValidationResult
    ) -> None:
        """Validate overall grid layout for overlaps."""
        # Build grid occupation map
        grid = {}  # (x, y) -> panel_title

        for panel in panels:
            if panel.get("type") == "row" and panel.get("collapsed"):
                continue

            grid_pos = panel.get("gridPos", {})
            x = grid_pos.get("x", 0)
            y = grid_pos.get("y", 0)
            w = grid_pos.get("w", 1)
            h = grid_pos.get("h", 1)
            title = panel.get("title", "<untitled>")

            for dx in range(w):
                for dy in range(h):
                    pos = (x + dx, y + dy)
                    if pos in grid:
                        result.errors.append(
                            f"Panel '{title}' overlaps with '{grid[pos]}' at position {pos}"
                        )
                    else:
                        grid[pos] = title

    def generate_panel_id(
        self, row_title: str, panel_title: str, panel_type: str
    ) -> str:
        """Generate deterministic panel ID using SHA256."""
        seed = f"{row_title}|{panel_title}|{panel_type}"
        hash_hex = hashlib.sha256(seed.encode()).hexdigest()[:8]
        return hash_hex


def main():
    parser = argparse.ArgumentParser(description="Validate Grafana dashboards")
    parser.add_argument("path", nargs="?", help="Path to dashboard JSON file")
    parser.add_argument("--dir", "-d", help="Directory containing dashboard files")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--strict", "-s", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    if not args.path and not args.dir:
        parser.print_help()
        sys.exit(1)

    validator = DashboardValidator()
    all_results = []

    files_to_check = []
    if args.path:
        files_to_check.append(Path(args.path))
    if args.dir:
        dir_path = Path(args.dir)
        files_to_check.extend(dir_path.glob("**/*.json"))

    for file_path in files_to_check:
        result = validator.validate_file(file_path)
        all_results.append(result)

    # Calculate summary
    total = len(all_results)
    passed = sum(1 for r in all_results if not r.errors)
    if args.strict:
        passed = sum(1 for r in all_results if not r.errors and not r.warnings)

    if args.json:
        output = {
            "summary": {"total": total, "passed": passed, "failed": total - passed},
            "results": [r.to_dict() for r in all_results],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'=' * 60}")
        print("Grafana Dashboard Validation Report")
        print(f"{'=' * 60}")

        for result in all_results:
            status = "✅ PASS" if not result.errors else "❌ FAIL"
            if args.strict and result.warnings:
                status = "❌ FAIL"

            print(f"\n{status} {result.title}")
            print(f"   File: {result.file_path}")
            print(f"   UID: {result.uid}")
            print(f"   Panels: {result.panel_count}")

            for e in result.errors:
                print(f"   ❌ ERROR: {e}")

            for w in result.warnings:
                print(f"   ⚠️  WARNING: {w}")

            for s in result.suggestions:
                print(f"   💡 {s}")

        print(f"\n{'=' * 60}")
        print(f"Summary: {passed}/{total} dashboards passed validation")
        print(f"{'=' * 60}")

    # Exit with error if any failures
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
