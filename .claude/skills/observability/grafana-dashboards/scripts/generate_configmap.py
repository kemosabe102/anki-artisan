#!/usr/bin/env python3
"""
Grafana Dashboard ConfigMap Generator

Generates Kubernetes ConfigMap YAML from Grafana dashboard JSON.

Usage:
    python generate_configmap.py dashboard.json
    python generate_configmap.py dashboard.json --namespace monitoring --name my-dashboard
"""

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to DNS-1123 compliant name."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    # Replace multiple hyphens with single
    text = re.sub(r"-+", "-", text)
    # Truncate to 63 characters (DNS-1123 limit)
    return text[:63]


def validate_dashboard(dashboard: dict) -> list[str]:
    """Validate dashboard before ConfigMap generation."""
    errors = []

    # Check required fields
    if not dashboard.get("uid"):
        errors.append("Dashboard missing 'uid' field")

    if not dashboard.get("title"):
        errors.append("Dashboard missing 'title' field")

    # Check schema version
    schema_version = dashboard.get("schemaVersion", 0)
    if schema_version < 38:
        errors.append(f"Schema version {schema_version} is outdated (recommend 38+)")

    # Check for panels
    panels = dashboard.get("panels", [])
    if not panels:
        errors.append("Dashboard has no panels")

    return errors


def generate_configmap(
    dashboard: dict,
    name: str | None = None,
    namespace: str = "monitoring",
    folder: str = "",
    labels: dict | None = None,
) -> str:
    """Generate Kubernetes ConfigMap YAML from dashboard JSON."""

    # Derive name from dashboard title if not provided
    if not name:
        title = dashboard.get("title", "dashboard")
        name = slugify(title)
        if not name.endswith("-dashboard"):
            name = f"{name}-dashboard"

    # Ensure name is valid
    name = slugify(name)

    # Build labels
    default_labels = {"grafana_dashboard": "1"}
    if labels:
        default_labels.update(labels)

    # Add folder annotation if specified
    annotations = {}
    if folder:
        annotations["grafana_folder"] = folder

    # Format labels as YAML
    labels_yaml = "\n".join(f'    {k}: "{v}"' for k, v in default_labels.items())

    # Format annotations as YAML
    annotations_yaml = ""
    if annotations:
        annotations_yaml = "  annotations:\n" + "\n".join(
            f'    {k}: "{v}"' for k, v in annotations.items()
        )

    # JSON encode the dashboard with proper indentation
    dashboard_json = json.dumps(dashboard, indent=2, ensure_ascii=False)

    # Indent JSON for YAML embedding (4 spaces)
    indented_json = "\n".join(
        "    " + line if line else line for line in dashboard_json.split("\n")
    )

    # Generate ConfigMap YAML
    configmap = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {name}
  namespace: {namespace}
  labels:
{labels_yaml}
{annotations_yaml}
data:
  {name}.json: |
{indented_json}
"""

    return configmap.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate Kubernetes ConfigMap from Grafana dashboard JSON"
    )
    parser.add_argument("dashboard", help="Path to dashboard JSON file")
    parser.add_argument(
        "--name", "-n", help="ConfigMap name (default: derived from title)"
    )
    parser.add_argument(
        "--namespace",
        "-ns",
        default="monitoring",
        help="Kubernetes namespace (default: monitoring)",
    )
    parser.add_argument("--folder", "-f", help="Grafana folder name")
    parser.add_argument(
        "--label",
        "-l",
        action="append",
        default=[],
        help="Additional labels (key=value format)",
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--validate",
        "-v",
        action="store_true",
        help="Validate dashboard before generation",
    )
    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        help="Output metadata as JSON instead of ConfigMap",
    )

    args = parser.parse_args()

    # Load dashboard
    dashboard_path = Path(args.dashboard)

    try:
        with open(dashboard_path) as f:
            content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {dashboard_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: File not found: {dashboard_path}", file=sys.stderr)
        sys.exit(1)

    # Handle wrapped format (dashboard + meta)
    dashboard = content.get("dashboard", content)

    # Validate if requested
    if args.validate:
        errors = validate_dashboard(dashboard)
        if errors:
            print("Validation errors:", file=sys.stderr)
            for error in errors:
                print(f"  ❌ {error}", file=sys.stderr)
            sys.exit(1)
        print("✅ Dashboard validation passed", file=sys.stderr)

    # Parse additional labels
    labels = {}
    for label in args.label:
        if "=" not in label:
            print(
                f"ERROR: Invalid label format '{label}'. Use key=value", file=sys.stderr
            )
            sys.exit(1)
        key, value = label.split("=", 1)
        labels[key] = value

    # Generate ConfigMap
    configmap = generate_configmap(
        dashboard=dashboard,
        name=args.name,
        namespace=args.namespace,
        folder=args.folder,
        labels=labels if labels else None,
    )

    if args.json_output:
        # Output metadata as JSON
        output = {
            "configmap_name": args.name or slugify(dashboard.get("title", "dashboard")),
            "namespace": args.namespace,
            "dashboard_uid": dashboard.get("uid"),
            "dashboard_title": dashboard.get("title"),
            "panel_count": len(dashboard.get("panels", [])),
            "schema_version": dashboard.get("schemaVersion"),
        }
        result = json.dumps(output, indent=2)
    else:
        result = configmap

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result)
        print(f"✅ ConfigMap written to {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
