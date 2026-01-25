---
title: "Grafana Dashboard Validation & ConfigMap Management"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Grafana Dashboard Validation & ConfigMap Management

**Category**: observability

**Domain**: Grafana dashboard validation, PromQL linting, ConfigMap chunking, quality assurance

**Confidence**: 0.95

**Last Updated**: 2025-10-30T00:00:00Z

**Agent**: grafana-dashboard-builder

**Version Compatibility**: See [README.md](./README.md#version-compatibility) for Grafana 12.x, Prometheus 3.x, and Jaeger 2.x compatibility details.

---

## Overview

Automated dashboard validation ensures production-ready Grafana dashboards through 4-stage validation (schema → PromQL → datasource → quality), official tooling integration (dashboard-linter, promtool, pint), quality scoring algorithms, and intelligent ConfigMap chunking strategies for Kubernetes deployment.

**Key Concepts**:

- **4-Stage Validation Pipeline**: Schema validation → PromQL linting → Datasource testing → Quality scoring

- **Quality Scoring Formula**: `(signal × 0.6) + (usability × 0.3) + (performance × 0.1)`

- **ConfigMap Chunking**: 4 strategies to handle 1MB Kubernetes ConfigMap size limit

- **CI/CD Integration**: GitHub Actions workflow for automated validation and deployment

---

## Core Frameworks

### Framework 1: 4-Stage Dashboard Validation Pipeline

**Purpose**: Provide systematic validation workflow ensuring dashboards meet schema, PromQL, datasource, and quality standards before deployment.

**When to Use**:

- Before committing dashboard changes to version control

- During CI/CD pipeline validation phase

- When generating dashboards programmatically

- After manual dashboard edits for quality assurance

**Components**:

1. **Stage 1: Schema Validation** - Validate JSON structure against Grafana dashboard schema

2. **Stage 2: PromQL Linting** - Check Prometheus query syntax and anti-patterns

3. **Stage 3: Datasource Testing** - Verify datasource connectivity and query execution

4. **Stage 4: Quality Scoring** - Assess dashboard usability, signal clarity, and performance

**How to Apply**:

1. Parse dashboard JSON and extract metadata

2. Execute validation stages sequentially (fail-fast on critical errors)

3. Collect warnings and recommendations from each stage

4. Generate comprehensive validation report with actionable fixes

5. Block deployment if quality score < threshold (default: 70/100)

**Example from Research**:

```python

from typing import Dict, List, Tuple

from enum import Enum



class ValidationStage(str, Enum):

    """Dashboard validation stages."""

    SCHEMA = "SCHEMA"

    PROMQL = "PROMQL"

    DATASOURCE = "DATASOURCE"

    QUALITY = "QUALITY"



class ValidationSeverity(str, Enum):

    """Issue severity levels."""

    CRITICAL = "CRITICAL"  # Blocks deployment

    WARNING = "WARNING"    # Deployment allowed, fix recommended

    INFO = "INFO"          # Best practice suggestion



class ValidationResult:

    """Result from single validation stage."""

    def __init__(self, stage: ValidationStage, passed: bool,

                 issues: List[Dict], execution_time_ms: int):

        self.stage = stage

        self.passed = passed

        self.issues = issues  # [{"severity": str, "message": str, "location": str}]

        self.execution_time_ms = execution_time_ms



def validate_dashboard_pipeline(dashboard_json: Dict) -> Tuple[bool, List[ValidationResult]]:

    """

    Execute 4-stage validation pipeline.



    Returns:

        (overall_passed, stage_results)

    """

    results = []



    # Stage 1: Schema Validation

    schema_result = validate_schema(dashboard_json)

    results.append(schema_result)

    if not schema_result.passed:

        return (False, results)  # Fail-fast on schema errors



    # Stage 2: PromQL Linting

    promql_result = validate_promql(dashboard_json)

    results.append(promql_result)



    # Stage 3: Datasource Testing

    datasource_result = validate_datasources(dashboard_json)

    results.append(datasource_result)



    # Stage 4: Quality Scoring

    quality_result = calculate_quality_score(dashboard_json)

    results.append(quality_result)



    # Overall pass = no critical issues across all stages

    overall_passed = all(r.passed for r in results)

    return (overall_passed, results)

```

**Source**: Grafana dashboard-linter design patterns, O'Reilly Practical Monitoring Chapter 7

---

### Framework 2: Schema Validation with dashboard-linter

**Purpose**: Validate dashboard JSON structure against official Grafana schema using dashboard-linter CLI tool.

**When to Use**:

- First stage in validation pipeline (foundational check)

- After programmatic dashboard generation

- When migrating dashboards between Grafana versions

- To detect breaking changes in schema updates

**Components**:

1. **dashboard-linter CLI**: Official Grafana validation tool

2. **JSON Schema Rules**: Grafana dashboard schema definition (v9.0+)

3. **Required Fields**: title, panels, schemaVersion, uid

4. **Panel Validation**: Targets, queries, visualization options

5. **Template Variables**: Syntax, scoping, default values

**How to Apply**:

1. Install dashboard-linter: `npm install -g @grafana/dashboard-linter`

2. Run validation: `dashboard-linter lint <dashboard.json>`

3. Parse output for error/warning categorization

4. Generate fixes for common schema violations

5. Re-validate after fixes applied

**Example from Research**:

```bash

# Install dashboard-linter globally

npm install -g @grafana/dashboard-linter



# Validate single dashboard

dashboard-linter lint dashboards/monitoring-overview.json



# Validate all dashboards in directory with strict mode

dashboard-linter lint dashboards/*.json --strict



# Output JSON report for CI/CD integration

dashboard-linter lint dashboards/*.json --format json > validation-report.json



# Fix common issues automatically

dashboard-linter fix dashboards/monitoring-overview.json

```

**Python Integration**:

```python

import json

import subprocess

from typing import Dict, List



def validate_schema_with_linter(dashboard_path: str) -> ValidationResult:

    """

    Validate dashboard schema using dashboard-linter.



    Returns:

        ValidationResult with issues categorized by severity

    """

    try:

        # Run dashboard-linter with JSON output

        result = subprocess.run(

            ["dashboard-linter", "lint", dashboard_path, "--format", "json"],

            capture_output=True,

            text=True,

            timeout=30

        )



        # Parse JSON output

        lint_output = json.loads(result.stdout)

        issues = []



        for error in lint_output.get("errors", []):

            issues.append({

                "severity": ValidationSeverity.CRITICAL,

                "message": error["message"],

                "location": error.get("path", "unknown"),

                "rule": error.get("rule", "schema")

            })



        for warning in lint_output.get("warnings", []):

            issues.append({

                "severity": ValidationSeverity.WARNING,

                "message": warning["message"],

                "location": warning.get("path", "unknown"),

                "rule": warning.get("rule", "schema")

            })



        passed = len([i for i in issues if i["severity"] == ValidationSeverity.CRITICAL]) == 0



        return ValidationResult(

            stage=ValidationStage.SCHEMA,

            passed=passed,

            issues=issues,

            execution_time_ms=int(result.returncode * 1000)  # Approximate

        )



    except subprocess.TimeoutExpired:

        return ValidationResult(

            stage=ValidationStage.SCHEMA,

            passed=False,

            issues=[{"severity": ValidationSeverity.CRITICAL,

                    "message": "Schema validation timed out (>30s)",

                    "location": "pipeline"}],

            execution_time_ms=30000

        )

    except Exception as e:

        return ValidationResult(

            stage=ValidationStage.SCHEMA,

            passed=False,

            issues=[{"severity": ValidationSeverity.CRITICAL,

                    "message": f"Schema validation failed: {str(e)}",

                    "location": "pipeline"}],

            execution_time_ms=0

        )

```

**Common Schema Violations**:

- Missing required fields: `title`, `uid`, `schemaVersion`

- Invalid panel types: Unsupported visualization types

- Malformed targets: Missing `expr` (PromQL) or `datasource`

- Template variable errors: Invalid scoping or default values

- Deprecated fields: Old Grafana version syntax

**Source**:

- Grafana dashboard-linter documentation (https://github.com/grafana/dashboard-linter)

- Grafana JSON Dashboard Schema (https://grafana.com/docs/grafana/latest/dashboards/json-model/)

---

### Framework 3: PromQL Validation with promtool & pint

**Purpose**: Validate Prometheus query syntax, detect anti-patterns, and ensure query performance using official Prometheus tooling.

**When to Use**:

- Stage 2 in validation pipeline (after schema validation)

- When adding new dashboard panels with PromQL queries

- To detect high-cardinality queries before production

- For query performance optimization and best practice enforcement

**Components**:

1. **promtool**: Official Prometheus CLI for query validation

2. **pint**: Cloudflare's PromQL linter with advanced rules

3. **Syntax Validation**: PromQL grammar and function checks

4. **Anti-Pattern Detection**: Regex abuse, unbounded range queries, high cardinality

5. **Performance Linting**: Query complexity, label filtering, aggregation efficiency

**How to Apply**:

1. Extract PromQL queries from dashboard JSON (panels → targets → expr)

2. Validate syntax with promtool: `promtool query analyze <expr>`

3. Lint for anti-patterns with pint: `pint lint <query>`

4. Check query performance against Prometheus API (optional)

5. Generate recommendations for query optimization

**Example from Research**:

```python

import json

import subprocess

from typing import List, Dict



def extract_promql_queries(dashboard_json: Dict) -> List[Dict]:

    """

    Extract all PromQL queries from dashboard panels.



    Returns:

        [{"panel_id": int, "panel_title": str, "expr": str, "datasource": str}]

    """

    queries = []

    for panel in dashboard_json.get("panels", []):

        panel_id = panel.get("id")

        panel_title = panel.get("title", "Untitled")



        for target in panel.get("targets", []):

            expr = target.get("expr")

            datasource = target.get("datasource")



            if expr:  # Only PromQL queries

                queries.append({

                    "panel_id": panel_id,

                    "panel_title": panel_title,

                    "expr": expr,

                    "datasource": datasource

                })



    return queries



def validate_promql_with_promtool(expr: str) -> Dict:

    """

    Validate PromQL syntax using promtool.



    Returns:

        {"valid": bool, "error": str|None}

    """

    try:

        # promtool expects query on stdin

        result = subprocess.run(

            ["promtool", "query", "analyze"],

            input=expr,

            capture_output=True,

            text=True,

            timeout=10

        )



        if result.returncode == 0:

            return {"valid": True, "error": None}

        else:

            return {"valid": False, "error": result.stderr.strip()}



    except subprocess.TimeoutExpired:

        return {"valid": False, "error": "Query validation timed out (>10s)"}

    except FileNotFoundError:

        return {"valid": False, "error": "promtool not installed"}



def lint_promql_with_pint(expr: str) -> List[Dict]:

    """

    Lint PromQL for anti-patterns using Cloudflare pint.



    Returns:

        [{"severity": str, "message": str, "rule": str}]

    """

    # pint requires query in temporary file with Prometheus rules format

    rule_content = f"""

groups:

  - name: temp

    rules:

      - record: temp_query

        expr: {expr}

"""



    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:

        f.write(rule_content)

        temp_file = f.name



    try:

        result = subprocess.run(

            ["pint", "lint", temp_file],

            capture_output=True,

            text=True,

            timeout=15

        )



        issues = []

        # Parse pint output (format: "file:line:col: [severity] message (rule)")

        for line in result.stdout.splitlines():

            if ":" in line:

                parts = line.split(":", 3)

                if len(parts) >= 4:

                    severity_msg = parts[3].strip()

                    # Extract severity (WARNING/ERROR), message, rule

                    if "[WARNING]" in severity_msg:

                        severity = ValidationSeverity.WARNING

                        msg = severity_msg.split("[WARNING]", 1)[1].strip()

                    elif "[ERROR]" in severity_msg:

                        severity = ValidationSeverity.CRITICAL

                        msg = severity_msg.split("[ERROR]", 1)[1].strip()

                    else:

                        continue



                    # Extract rule name from (rule_name)

                    rule = "unknown"

                    if "(" in msg and ")" in msg:

                        rule = msg.split("(")[-1].split(")")



                    issues.append({

                        "severity": severity,

                        "message": msg,

                        "rule": rule

                    })



        return issues



    finally:

        os.unlink(temp_file)  # Clean up temp file



def validate_promql(dashboard_json: Dict) -> ValidationResult:

    """

    Execute Stage 2: PromQL validation using promtool and pint.



    Returns:

        ValidationResult with all PromQL issues across dashboard

    """

    import time

    start_time = time.time()



    queries = extract_promql_queries(dashboard_json)

    issues = []



    for query in queries:

        expr = query["expr"]

        panel_title = query["panel_title"]



        # Syntax validation with promtool

        syntax_result = validate_promql_with_promtool(expr)

        if not syntax_result["valid"]:

            issues.append({

                "severity": ValidationSeverity.CRITICAL,

                "message": f"PromQL syntax error: {syntax_result['error']}",

                "location": f"panel '{panel_title}'",

                "query": expr

            })

            continue  # Skip linting if syntax invalid



        # Anti-pattern linting with pint

        lint_issues = lint_promql_with_pint(expr)

        for issue in lint_issues:

            issue["location"] = f"panel '{panel_title}'"

            issue["query"] = expr

            issues.append(issue)



    passed = len([i for i in issues if i["severity"] == ValidationSeverity.CRITICAL]) == 0



    return ValidationResult(

        stage=ValidationStage.PROMQL,

        passed=passed,

        issues=issues,

        execution_time_ms=int((time.time() - start_time) * 1000)

    )

```

**Common PromQL Anti-Patterns Detected by pint**:

1. **Unbounded Range Queries**: `rate(metric[5m])` without time bounds (queries entire history)

2. **High Cardinality Labels**: `sum(metric) by (instance, pod, container)` (excessive grouping)

3. **Regex Abuse**: `metric{label=~".*"}` (matches everything, slow)

4. **Missing Rate/Increase**: Counter without `rate()` or `increase()` (incorrect metric type)

5. **Redundant Aggregations**: `sum(sum(metric))` (inefficient double aggregation)

6. **Inefficient Joins**: `metric1 * on(label) metric2` without proper label filtering

**Source**:

- Prometheus promtool documentation (https://prometheus.io/docs/prometheus/latest/command-line/promtool/)

- Cloudflare pint GitHub (https://github.com/cloudflare/pint)

- PromQL best practices (https://prometheus.io/docs/practices/rules/)

---

### Framework 4: Quality Scoring Algorithm

**Purpose**: Calculate objective dashboard quality score based on signal clarity, usability, and performance metrics.

**When to Use**:

- Stage 4 in validation pipeline (final quality gate)

- When comparing multiple dashboard implementations

- To enforce quality standards before production deployment

- For automated dashboard improvement recommendations

**Components**:

1. **Signal Clarity (60%)**: Metric relevance, panel naming, legend quality

2. **Usability (30%)**: Layout organization, color usage, interactivity

3. **Performance (10%)**: Query efficiency, rendering speed, data density

**How to Apply**:

1. Calculate individual component scores (0-100 each)

2. Apply weighted formula: `(signal × 0.6) + (usability × 0.3) + (performance × 0.1)`

3. Generate detailed score breakdown for each component

4. Provide actionable recommendations for score improvement

5. Set quality gate threshold (default: 70/100 for production)

**Example from Research**:

```python

from typing import Dict, List, Tuple



class QualityScoreComponents:

    """Dashboard quality score components."""

    def __init__(self):

        self.signal_score = 0  # 0-100

        self.usability_score = 0  # 0-100

        self.performance_score = 0  # 0-100

        self.total_score = 0  # Weighted average

        self.recommendations = []  # List of improvement suggestions



def calculate_signal_clarity_score(dashboard_json: Dict) -> Tuple[int, List[str]]:

    """

    Calculate signal clarity score (60% weight).



    Components:

    - Panel titles descriptive (not "Panel 1", "Graph", etc.)

    - Legends enabled and informative

    - Units specified for all metrics

    - Thresholds configured for alerting context

    - Y-axis labels clear and bounded



    Returns:

        (score_0_to_100, recommendations)

    """

    score = 100

    recommendations = []

    panels = dashboard_json.get("panels", [])



    if not panels:

        return (0, ["Dashboard has no panels"])



    # Check panel titles (deduct 10 points per generic title)

    generic_titles = ["Panel", "Graph", "Chart", "Visualization", "Untitled"]

    for panel in panels:

        title = panel.get("title", "").strip()

        if not title or any(generic in title for generic in generic_titles):

            score -= 10

            recommendations.append(f"Panel {panel.get('id')} has generic/missing title")



    # Check legend configuration (deduct 5 points per missing legend)

    for panel in panels:

        legend = panel.get("options", {}).get("legend", {})

        if not legend.get("show", True):

            score -= 5

            recommendations.append(f"Panel '{panel.get('title')}' has legend disabled")



    # Check unit specifications (deduct 10 points per missing unit)

    for panel in panels:

        field_config = panel.get("fieldConfig", {}).get("defaults", {})

        if not field_config.get("unit"):

            score -= 10

            recommendations.append(f"Panel '{panel.get('title')}' missing unit specification")



    # Check thresholds (bonus 10 points if configured)

    threshold_count = sum(1 for p in panels if p.get("fieldConfig", {}).get("defaults", {}).get("thresholds"))

    if threshold_count > 0:

        score += min(20, threshold_count * 10)  # Max +20 bonus



    return (max(0, min(100, score)), recommendations)



def calculate_usability_score(dashboard_json: Dict) -> Tuple[int, List[str]]:

    """

    Calculate usability score (30% weight).



    Components:

    - Logical panel layout (rows, alignment)

    - Appropriate color usage (not excessive)

    - Template variables for filtering

    - Time range picker enabled

    - Refresh intervals configured

    - Panel descriptions/documentation



    Returns:

        (score_0_to_100, recommendations)

    """

    score = 100

    recommendations = []



    # Check template variables (deduct 20 if none defined)

    templating = dashboard_json.get("templating", {})

    if not templating.get("list"):

        score -= 20

        recommendations.append("No template variables defined (limits filtering capability)")



    # Check time range picker

    time_options = dashboard_json.get("time", {})

    if not time_options:

        score -= 10

        recommendations.append("Time range picker not configured")



    # Check refresh intervals

    refresh = dashboard_json.get("refresh")

    if not refresh:

        score -= 5

        recommendations.append("Auto-refresh not configured (may show stale data)")



    # Check panel descriptions

    panels = dashboard_json.get("panels", [])

    panels_with_descriptions = sum(1 for p in panels if p.get("description"))

    if panels_with_descriptions < len(panels) * 0.5:  # Less than 50% documented

        score -= 15

        recommendations.append("Less than 50% of panels have descriptions")



    # Check color usage (deduct if >5 colors used)

    color_count = 0

    unique_colors = set()



    for panel in panels:

        # Extract colors from fieldConfig overrides

        field_config = panel.get("fieldConfig", {})

        overrides = field_config.get("overrides", [])



        for override in overrides:

            for prop in override.get("properties", []):

                if prop.get("id") == "color":

                    color = prop.get("value", {}).get("fixedColor")

                    if color:

                        unique_colors.add(color)



        # Extract colors from threshold steps

        thresholds = field_config.get("defaults", {}).get("thresholds", {})

        for step in thresholds.get("steps", []):

            color = step.get("color")

            if color:

                unique_colors.add(color)



    color_count = len(unique_colors)

    if color_count > 5:

        score -= 10

        recommendations.append(f"Dashboard uses {color_count} unique colors (>5 may cause visual confusion)")



    return (max(0, min(100, score)), recommendations)



def calculate_performance_score(dashboard_json: Dict) -> Tuple[int, List[str]]:

    """

    Calculate performance score (10% weight).



    Components:

    - Query efficiency (promql complexity)

    - Data point limits (avoid excessive resolution)

    - Panel count (not overloaded)

    - Caching headers configured



    Returns:

        (score_0_to_100, recommendations)

    """

    score = 100

    recommendations = []

    panels = dashboard_json.get("panels", [])



    # Check panel count (deduct if >20 panels)

    if len(panels) > 20:

        score -= 20

        recommendations.append(f"Dashboard has {len(panels)} panels (>20 may cause slow rendering)")

    elif len(panels) > 15:

        score -= 10

        recommendations.append(f"Dashboard has {len(panels)} panels (consider splitting)")



    # Check query complexity (count aggregations, functions)

    complex_query_count = 0

    for panel in panels:

        for target in panel.get("targets", []):

            expr = target.get("expr", "")

            # Count PromQL complexity indicators

            if expr.count("(") > 5:  # More than 5 nested functions

                complex_query_count += 1



    if complex_query_count > 0:

        score -= min(30, complex_query_count * 10)  # Max -30

        recommendations.append(f"{complex_query_count} panels have complex queries (>5 function calls)")



    # Check data point limits

    for panel in panels:

        max_data_points = panel.get("maxDataPoints")

        if max_data_points and max_data_points > 1000:

            score -= 10

            recommendations.append(f"Panel '{panel.get('title')}' has high maxDataPoints ({max_data_points})")



    return (max(0, min(100, score)), recommendations)



def calculate_quality_score(dashboard_json: Dict) -> ValidationResult:

    """

    Execute Stage 4: Calculate overall quality score.



    Formula: (signal × 0.6) + (usability × 0.3) + (performance × 0.1)



    Returns:

        ValidationResult with quality score and improvement recommendations

    """

    components = QualityScoreComponents()



    # Calculate component scores

    signal_score, signal_recs = calculate_signal_clarity_score(dashboard_json)

    usability_score, usability_recs = calculate_usability_score(dashboard_json)

    performance_score, performance_recs = calculate_performance_score(dashboard_json)



    # Apply weighted formula

    total_score = int(

        (signal_score * 0.6) +

        (usability_score * 0.3) +

        (performance_score * 0.1)

    )



    # Aggregate recommendations

    all_recommendations = []

    if signal_recs:

        all_recommendations.append(f"Signal Clarity ({signal_score}/100): " + "; ".join(signal_recs))

    if usability_recs:

        all_recommendations.append(f"Usability ({usability_score}/100): " + "; ".join(usability_recs))

    if performance_recs:

        all_recommendations.append(f"Performance ({performance_score}/100): " + "; ".join(performance_recs))



    # Quality gate: Pass if score >= 70

    quality_threshold = 70

    passed = total_score >= quality_threshold



    issues = []

    if not passed:

        issues.append({

            "severity": ValidationSeverity.WARNING,

            "message": f"Quality score {total_score}/100 below threshold ({quality_threshold})",

            "location": "dashboard",

            "recommendations": all_recommendations

        })

    else:

        # Even if passing, include recommendations as INFO

        if all_recommendations:

            issues.append({

                "severity": ValidationSeverity.INFO,

                "message": f"Quality score {total_score}/100 (PASS)",

                "location": "dashboard",

                "recommendations": all_recommendations

            })



    return ValidationResult(

        stage=ValidationStage.QUALITY,

        passed=passed,

        issues=issues,

        execution_time_ms=0

    )

```

**Quality Score Interpretation**:

- **90-100**: Excellent - Production-ready with best practices

- **70-89**: Good - Acceptable for production with minor improvements

- **50-69**: Fair - Requires improvements before production

- **< 50**: Poor - Major rework needed

**Source**: O'Reilly Practical Monitoring Chapter 7 (Dashboard Design Principles)

---

## Processes & Workflows

### Workflow 1: Complete CI/CD Validation Pipeline

**Purpose**: Automate dashboard validation in GitHub Actions workflow from commit to deployment.

**When to Use**:

- On pull requests modifying dashboard files

- Before merging to main branch (quality gate)

- In scheduled dashboard audit workflows

- As pre-deployment validation step

**Workflow Steps**:

1. **Trigger**: PR with changes to `dashboards/**/*.json` or `k8s/**/dashboards-*.yaml`

2. **Checkout**: Retrieve repository code and dashboard files

3. **Setup**: Install validation tools (dashboard-linter, promtool, pint)

4. **Execute**: Run 4-stage validation pipeline

5. **Report**: Generate validation report artifact

6. **Gate**: Fail workflow if critical issues or quality score < 70

7. **Deploy**: If validation passes, update ConfigMaps and apply to cluster

**Example GitHub Actions Workflow**:

```yaml
# .github/workflows/dashboard-validation.yml

name: Grafana Dashboard Validation

on:
  pull_request:
    paths:
      - 'dashboards/**/*.json'

      - 'k8s/**/dashboards-*.yaml'

  push:
    branches:
      - main

    paths:
      - 'dashboards/**/*.json'

jobs:
  validate-dashboards:
    name: Validate Grafana Dashboards

    runs-on: ubuntu-latest

    timeout-minutes: 10

    steps:
      # Step 1: Checkout repository

      - name: Checkout code

        uses: actions/checkout@v4

        with:
          fetch-depth: 0 # Full history for diff analysis

      # Step 2: Setup Node.js for dashboard-linter

      - name: Setup Node.js

        uses: actions/setup-node@v4

        with:
          node-version: '20'

      # Step 3: Install validation tools

      - name: Install validation tools

        run: |

          # Install dashboard-linter

          npm install -g @grafana/dashboard-linter



          # Install Prometheus promtool

          wget https://github.com/prometheus/prometheus/releases/download/v3.7.3/prometheus-3.7.3.linux-amd64.tar.gz

          tar xzf prometheus-3.7.3.linux-amd64.tar.gz

          sudo mv prometheus-3.7.3.linux-amd64/promtool /usr/local/bin/



          # Install Cloudflare pint

          wget https://github.com/cloudflare/pint/releases/download/v0.45.0/pint-0.45.0-linux-amd64.tar.gz

          tar xzf pint-0.45.0-linux-amd64.tar.gz

          sudo mv pint /usr/local/bin/

      # Step 4: Setup Python for validation scripts

      - name: Setup Python

        uses: actions/setup-python@v5

        with:
          python-version: '3.11'

      - name: Install Python dependencies

        run: |

          pip install -r scripts/requirements-dashboard-validation.txt

          # Expected: pydantic, requests, pyyaml

      # Step 5: Run 4-stage validation pipeline

      - name: Validate dashboard schemas

        id: schema-validation

        run: |

          echo "::group::Schema Validation"

          dashboard-linter lint dashboards/*.json --format json > schema-report.json

          python scripts/validate_dashboards.py --stage schema --report schema-report.json

          echo "::endgroup::"

      - name: Validate PromQL queries

        id: promql-validation

        run: |

          echo "::group::PromQL Validation"

          python scripts/validate_dashboards.py --stage promql --dashboards dashboards/*.json

          echo "::endgroup::"

      - name: Test datasource connectivity

        id: datasource-test

        env:
          PROMETHEUS_URL: ${{ secrets.PROMETHEUS_URL }}

        run: |

          echo "::group::Datasource Testing"

          python scripts/validate_dashboards.py --stage datasource --prometheus-url "$PROMETHEUS_URL"

          echo "::endgroup::"

        continue-on-error: true # Allow failure if Prometheus unreachable

      - name: Calculate quality scores

        id: quality-scoring

        run: |

          echo "::group::Quality Scoring"

          python scripts/validate_dashboards.py --stage quality --threshold 70

          echo "::endgroup::"

      # Step 6: Generate validation report

      - name: Generate validation report

        if: always()

        run: |

          python scripts/generate_validation_report.py \

            --schema schema-report.json \

            --output validation-report.md

      # Step 7: Upload artifacts

      - name: Upload validation report

        if: always()

        uses: actions/upload-artifact@v4

        with:
          name: dashboard-validation-report

          path: |

            validation-report.md

            schema-report.json

          retention-days: 30

      # Step 8: Comment on PR with results

      - name: Comment validation results on PR

        if: github.event_name == 'pull_request'

        uses: actions/github-script@v7

        with:
          script: |

            const fs = require('fs');

            const report = fs.readFileSync('validation-report.md', 'utf8');



            github.rest.issues.createComment({

              issue_number: context.issue.number,

              owner: context.repo.owner,

              repo: context.repo.repo,

              body: `## 📊 Dashboard Validation Results\n\n${report}`

            });

      # Step 9: Quality gate enforcement

      - name: Check quality gate

        run: |

          QUALITY_SCORE=$(python scripts/get_quality_score.py)

          echo "Quality Score: $QUALITY_SCORE"



          if [ "$QUALITY_SCORE" -lt 70 ]; then

            echo "::error::Quality score $QUALITY_SCORE below threshold (70)"

            exit 1

          fi

  deploy-dashboards:
    name: Deploy to Kubernetes

    needs: validate-dashboards

    if: github.ref == 'refs/heads/main'

    runs-on: ubuntu-latest

    steps:
      - name: Checkout code

        uses: actions/checkout@v4

      - name: Setup kubectl

        uses: azure/setup-kubectl@v3

        with:
          version: 'v1.28.0'

      - name: Configure kubectl

        env:
          KUBECONFIG_CONTENT: ${{ secrets.KUBECONFIG }}

        run: |

          mkdir -p $HOME/.kube

          echo "$KUBECONFIG_CONTENT" | base64 -d > $HOME/.kube/config

      - name: Generate ConfigMaps with chunking

        run: |

          python scripts/generate_dashboard_configmaps.py \

            --input dashboards/ \

            --output k8s/base/dashboards/ \

            --strategy one-per-dashboard \

            --max-size 900000  # 900KB to stay under 1MB limit

      - name: Apply ConfigMaps to cluster

        run: |

          kubectl apply -f k8s/base/dashboards/

          kubectl rollout restart deployment/grafana -n monitoring
```

**Python Validation Script Example** (`scripts/validate_dashboards.py`):

```python

#!/usr/bin/env python3

"""

Dashboard validation script for CI/CD pipeline.



Usage:

    python validate_dashboards.py --stage schema --report schema-report.json

    python validate_dashboards.py --stage promql --dashboards dashboards/*.json

    python validate_dashboards.py --stage quality --threshold 70

"""



import argparse

import json

import sys

from pathlib import Path

from typing import List



# Import validation functions from framework examples above

# (validate_schema_with_linter, validate_promql, calculate_quality_score)



def main():

    parser = argparse.ArgumentParser(description="Validate Grafana dashboards")

    parser.add_argument("--stage", choices=["schema", "promql", "datasource", "quality"],

                       required=True, help="Validation stage to execute")

    parser.add_argument("--dashboards", nargs="+", help="Dashboard JSON files to validate")

    parser.add_argument("--report", help="Input report file (for schema stage)")

    parser.add_argument("--threshold", type=int, default=70,

                       help="Quality score threshold (default: 70)")

    parser.add_argument("--prometheus-url", help="Prometheus URL for datasource testing")



    args = parser.parse_args()



    if args.stage == "schema":

        # Parse dashboard-linter JSON report

        with open(args.report) as f:

            report = json.load(f)



        critical_count = len([e for e in report.get("errors", [])

                             if e.get("severity") == "error"])



        if critical_count > 0:

            print(f"❌ Schema validation failed: {critical_count} critical errors")

            sys.exit(1)

        else:

            print("✅ Schema validation passed")



    elif args.stage == "promql":

        # Validate PromQL in all dashboards

        total_issues = 0



        for dashboard_path in args.dashboards:

            with open(dashboard_path) as f:

                dashboard = json.load(f)



            result = validate_promql(dashboard)

            critical_issues = [i for i in result.issues

                              if i["severity"] == ValidationSeverity.CRITICAL]



            if critical_issues:

                print(f"❌ {dashboard_path}: {len(critical_issues)} PromQL errors")

                total_issues += len(critical_issues)



        if total_issues > 0:

            print(f"❌ PromQL validation failed: {total_issues} total errors")

            sys.exit(1)

        else:

            print("✅ PromQL validation passed")



    elif args.stage == "quality":

        # Calculate quality scores

        scores = []



        scores = []

        for dashboard_path in args.dashboards:

            with open(dashboard_path) as f:

                dashboard = json.load(f)



            result = calculate_quality_score(dashboard)



            # Extract score from validation result message

            # Format: "Quality score X/100 (PASS)" or "Quality score X/100 below threshold"

            score = 0

            for issue in result.issues:

                message = issue.get("message", "")

                if "Quality score" in message:

                    # Extract score using regex

                    import re

                    match = re.search(r"Quality score (\d+)/100", message)

                    if match:

                        score = int(match.group(1))

                        break



            scores.append({"dashboard": dashboard_path, "score": score, "passed": result.passed})

            print(f"{dashboard_path}: {score}/100 ({'PASS' if result.passed else 'FAIL'})")



        # Check if all scores meet threshold

        avg_score = sum(s["score"] for s in scores) / len(scores) if scores else 0

        print(f"\n✅ Quality scoring completed: Average {avg_score:.1f}/100")



    else:

        print(f"Stage {args.stage} not implemented yet")

        sys.exit(1)



if __name__ == "__main__":

    main()

```

**Source**: GitHub Actions best practices, Grafana deployment workflows

---

## Decision Trees

### Decision Tree 1: ConfigMap Chunking Strategy Selection

**Purpose**: Select optimal ConfigMap chunking strategy based on dashboard count, size, and deployment requirements.

**When to Use**:

- When dashboard ConfigMaps exceed 1MB Kubernetes limit

- Planning dashboard storage architecture

- Optimizing ConfigMap deployment performance

- Designing dashboard versioning strategy

**Decision Criteria**:

1. **Total dashboard count** - How many dashboards to deploy?

2. **Average dashboard size** - Typical JSON file size (KB)

3. **Grafana sidecar support** - Using grafana-sidecar for auto-loading?

4. **Update frequency** - How often dashboards change?

5. **Cluster constraints** - etcd size limits, ConfigMap count limits

**Decision Flow**:

```

Start: Calculate total_size = dashboard_count × avg_size



├─ total_size < 900KB?

│  └─ YES → **Strategy 1: Single ConfigMap**

│      ├─ All dashboards in one ConfigMap

│      ├─ Simplest approach

│      └─ Best for: <10 dashboards, minimal updates

│

├─ total_size < 5MB AND dashboard_count < 20?

│  └─ YES → **Strategy 2: One ConfigMap Per Dashboard**

│      ├─ Each dashboard = separate ConfigMap

│      ├─ Granular updates (only changed dashboards redeploy)

│      └─ Best for: 10-20 dashboards, frequent updates

│

├─ total_size < 20MB AND using grafana-sidecar?

│  └─ YES → **Strategy 3: Panel-Level Splitting**

│      ├─ Split large dashboards into multiple smaller dashboards

│      ├─ Group related panels together

│      ├─ Use template variables for cross-dashboard navigation

│      └─ Best for: Large dashboards (>1MB each), complex monitoring

│

└─ total_size >= 20MB OR etcd constraints?

   └─ YES → **Strategy 4: External Storage (PV/PVC)**

       ├─ Store dashboards in Persistent Volume

       ├─ Mount volume to Grafana pod

       ├─ Use provisioning directory for auto-loading

       └─ Best for: Enterprise deployments, 50+ dashboards, GitOps workflows

```

**Implementation Examples**:

**Strategy 1: Single ConfigMap** (< 900KB total):

```yaml
# k8s/base/dashboards-all.yaml

apiVersion: v1

kind: ConfigMap

metadata:
  name: grafana-dashboards

  namespace: monitoring

  labels:
    grafana_dashboard: '1'

data:
  monitoring-overview.json: |

    {...}  # Dashboard JSON

  application-metrics.json: |

    {...}

  infrastructure-health.json: |

    {...}
```

**Strategy 2: One ConfigMap Per Dashboard** (10-20 dashboards):

```yaml
# k8s/base/dashboard-monitoring-overview.yaml

apiVersion: v1

kind: ConfigMap

metadata:
  name: grafana-dashboard-monitoring-overview

  namespace: monitoring

  labels:
    grafana_dashboard: '1'

data:
  monitoring-overview.json: |

    {...}

---
# k8s/base/dashboard-application-metrics.yaml

apiVersion: v1

kind: ConfigMap

metadata:
  name: grafana-dashboard-application-metrics

  namespace: monitoring

  labels:
    grafana_dashboard: '1'

data:
  application-metrics.json: |

    {...}
```

**Python Script for Automated Chunking** (`scripts/generate_dashboard_configmaps.py`):

```python

#!/usr/bin/env python3

"""

Generate Kubernetes ConfigMaps for Grafana dashboards with intelligent chunking.



Usage:

    python generate_dashboard_configmaps.py \

        --input dashboards/ \

        --output k8s/base/dashboards/ \

        --strategy one-per-dashboard \

        --max-size 900000

"""



import argparse

import json

import os

import yaml

from pathlib import Path

from typing import List, Dict



MAX_CONFIGMAP_SIZE = 1_000_000  # 1MB Kubernetes limit

SAFE_MAX_SIZE = 900_000  # 900KB to leave headroom



def calculate_dashboard_size(dashboard_json: Dict) -> int:

    """Calculate serialized size of dashboard JSON."""

    return len(json.dumps(dashboard_json))



def generate_single_configmap(dashboards: List[Dict], output_path: Path):

    """Strategy 1: All dashboards in single ConfigMap."""

    configmap = {

        "apiVersion": "v1",

        "kind": "ConfigMap",

        "metadata": {

            "name": "grafana-dashboards",

            "namespace": "monitoring",

            "labels": {"grafana_dashboard": "1"}

        },

        "data": {}

    }



    for dashboard in dashboards:

        filename = dashboard["filename"]

        content = json.dumps(dashboard["content"], indent=2)

        configmap["data"][filename] = content



    with open(output_path / "dashboards-all.yaml", "w") as f:

        yaml.dump(configmap, f, default_flow_style=False, sort_keys=False)



    print(f"✅ Generated single ConfigMap: {output_path / 'dashboards-all.yaml'}")



def generate_per_dashboard_configmaps(dashboards: List[Dict], output_path: Path):

    """Strategy 2: One ConfigMap per dashboard."""

    for dashboard in dashboards:

        filename = dashboard["filename"]

        name = filename.replace(".json", "").replace("_", "-")



        configmap = {

            "apiVersion": "v1",

            "kind": "ConfigMap",

            "metadata": {

                "name": f"grafana-dashboard-{name}",

                "namespace": "monitoring",

                "labels": {"grafana_dashboard": "1"}

            },

            "data": {

                filename: json.dumps(dashboard["content"], indent=2)

            }

        }



        output_file = output_path / f"dashboard-{name}.yaml"

        with open(output_file, "w") as f:

            yaml.dump(configmap, f, default_flow_style=False, sort_keys=False)



        print(f"✅ Generated ConfigMap: {output_file}")



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True, help="Input directory with dashboard JSONs")

    parser.add_argument("--output", required=True, help="Output directory for ConfigMaps")

    parser.add_argument("--strategy", choices=["single", "one-per-dashboard"],

                       default="one-per-dashboard")

    parser.add_argument("--max-size", type=int, default=SAFE_MAX_SIZE,

                       help="Max ConfigMap size in bytes")



    args = parser.parse_args()



    input_path = Path(args.input)

    output_path = Path(args.output)

    output_path.mkdir(parents=True, exist_ok=True)



    # Load all dashboards

    dashboards = []

    total_size = 0



    for json_file in input_path.glob("*.json"):

        with open(json_file) as f:

            content = json.load(f)



        size = calculate_dashboard_size(content)

        total_size += size



        dashboards.append({

            "filename": json_file.name,

            "content": content,

            "size": size

        })



        print(f"Loaded {json_file.name} ({size / 1024:.1f} KB)")



    print(f"\nTotal size: {total_size / 1024:.1f} KB across {len(dashboards)} dashboards")



    # Validate strategy feasibility

    if args.strategy == "single" and total_size > args.max_size:

        print(f"❌ ERROR: Total size {total_size / 1024:.1f} KB exceeds max {args.max_size / 1024:.1f} KB")

        print("Consider using --strategy one-per-dashboard")

        return 1



    # Generate ConfigMaps

    if args.strategy == "single":

        generate_single_configmap(dashboards, output_path)

    else:

        generate_per_dashboard_configmaps(dashboards, output_path)



    print(f"\n✅ Successfully generated ConfigMaps in {output_path}")

    return 0



if __name__ == "__main__":

    exit(main())

```

**Strategy 3: Panel-Level Splitting** (for large dashboards):

```python

def split_dashboard_by_panels(dashboard_json: Dict, max_panels: int = 10) -> List[Dict]:

    """

    Split large dashboard into multiple smaller dashboards by panel groups.



    Args:

        dashboard_json: Original dashboard JSON

        max_panels: Maximum panels per split dashboard



    Returns:

        List of dashboard JSONs (one per split)

    """

    panels = dashboard_json.get("panels", [])



    # Group panels by row (if using row panels)

    panel_groups = []

    current_group = []



    for panel in panels:

        if panel.get("type") == "row":

            # Start new group at row boundary

            if current_group:

                panel_groups.append(current_group)

            current_group = [panel]

        else:

            current_group.append(panel)



            # Split if group exceeds max_panels

            if len(current_group) >= max_panels:

                panel_groups.append(current_group)

                current_group = []



    # Add remaining panels

    if current_group:

        panel_groups.append(current_group)



    # Create separate dashboard for each group

    split_dashboards = []

    base_title = dashboard_json.get("title", "Dashboard")



    for i, group in enumerate(panel_groups, 1):

        split_dashboard = dashboard_json.copy()

        split_dashboard["title"] = f"{base_title} - Part {i}"

        split_dashboard["uid"] = f"{dashboard_json.get('uid', 'dash')}-part{i}"

        split_dashboard["panels"] = group



        split_dashboards.append(split_dashboard)



    return split_dashboards

```

**Strategy 4: External Storage (PV/PVC)**:

```yaml
# k8s/base/grafana-dashboards-pvc.yaml

apiVersion: v1

kind: PersistentVolumeClaim

metadata:
  name: grafana-dashboards-storage

  namespace: monitoring

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 10Gi

  storageClassName: standard

---
# k8s/base/grafana-deployment.yaml (excerpt)

apiVersion: apps/v1

kind: Deployment

metadata:
  name: grafana

  namespace: monitoring

spec:
  template:
    spec:
      containers:
        - name: grafana

          image: grafana/grafana:10.0.0

          volumeMounts:
            - name: dashboards-storage

              mountPath: /etc/grafana/provisioning/dashboards

      volumes:
        - name: dashboards-storage

          persistentVolumeClaim:
            claimName: grafana-dashboards-storage
```

**Source**: Kubernetes ConfigMap size limits, Grafana dashboard provisioning documentation

---

## Anti-Patterns

### Anti-Pattern 1: Information Overload Dashboards

**Problem**: Too many panels (>20) on single dashboard causing slow rendering, cognitive overload, and maintenance nightmares.

**Symptoms**:

- Dashboard takes >10 seconds to load

- Users struggle to find relevant metrics

- Frequent "which panel shows X?" questions

- Mobile/laptop viewing unusable

**Example**:

```json
{
  "title": "Everything Dashboard",

  "panels": [
    /* 47 panels covering infrastructure, applications, business metrics, security, etc. */
  ]
}
```

**Why It's Bad**:

- **Performance**: 47 PromQL queries execute simultaneously, overwhelming Prometheus

- **Usability**: Can't see big picture, endless scrolling

- **Maintenance**: Changes require coordination across many teams

**Fix**:

```python

def fix_information_overload(dashboard_json: Dict) -> List[Dict]:

    """

    Split overloaded dashboard into focused sub-dashboards.



    Strategy:

    1. Group panels by domain (infra, app, business)

    2. Create separate dashboard for each domain

    3. Add cross-dashboard links via template variables



    Returns:

        List of focused dashboards

    """

    panels = dashboard_json.get("panels", [])



    # Categorize panels by metric prefix or panel title

    categories = {

        "infrastructure": [],

        "application": [],

        "business": [],

        "security": []

    }



    for panel in panels:

        # Simple heuristic: categorize by first PromQL metric name

        targets = panel.get("targets", [])

        if targets:

            expr = targets[0].get("expr", "")

            if expr.startswith("node_") or expr.startswith("kube_"):

                categories["infrastructure"].append(panel)

            elif expr.startswith("http_") or expr.startswith("app_"):

                categories["application"].append(panel)

            elif expr.startswith("revenue_") or expr.startswith("user_"):

                categories["business"].append(panel)

            else:

                categories["security"].append(panel)



    # Create focused dashboard for each category

    focused_dashboards = []

    for category, category_panels in categories.items():

        if not category_panels:

            continue



        focused_dashboard = dashboard_json.copy()

        focused_dashboard["title"] = f"{category.title()} Monitoring"

        focused_dashboard["uid"] = f"{dashboard_json['uid']}-{category}"

        focused_dashboard["panels"] = category_panels



        focused_dashboards.append(focused_dashboard)



    return focused_dashboards

```

**Best Practice**: 5-15 panels per dashboard, group by domain/purpose

---

### Anti-Pattern 2: Line Graph Pollution

**Problem**: Using line graphs for everything, even when other visualizations are more appropriate.

**Symptoms**:

- Pie chart data displayed as lines

- Boolean states (up/down) as lines

- Status codes as lines

- 50+ lines on single graph (spaghetti)

**Example**:

```json
{
  "type": "graph", // Line graph

  "title": "HTTP Status Codes",

  "targets": [
    { "expr": "http_requests_total{code='200'}" },

    { "expr": "http_requests_total{code='201'}" },

    { "expr": "http_requests_total{code='204'}" }

    /* ... 47 more status codes */
  ]
}
```

**Why It's Bad**:

- **Usability**: Can't distinguish 50 overlapping lines

- **Clarity**: Wrong visualization for categorical data

- **Performance**: Rendering 50 time series is slow

**Fix**:

```json
{
  "type": "bargauge", // Better for categorical comparison

  "title": "HTTP Status Code Distribution",

  "targets": [
    {
      "expr": "sum by (code) (rate(http_requests_total[5m]))",

      "legendFormat": "{{code}}"
    }
  ],

  "options": {
    "orientation": "horizontal",

    "displayMode": "gradient"
  }
}
```

**Visualization Selection Guide**:

- **Line graphs**: Time-series trends (CPU, memory, latency)

- **Bar gauge**: Categorical comparison (status codes, error types)

- **Stat panel**: Single metric with thresholds (uptime %, error rate)

- **Table**: Multi-dimensional data (top N queries, pod resource usage)

- **Heatmap**: Distribution over time (latency percentiles, request sizes)

---

### Anti-Pattern 3: High Cardinality Label Explosions

**Problem**: Using high-cardinality labels (user_id, request_id, IP address) in PromQL queries causing memory exhaustion and slow queries.

**Symptoms**:

- Queries timing out after 30+ seconds

- Prometheus "too many samples" errors

- Dashboard panels never loading

- Prometheus OOM crashes

**Example**:

```promql

# BAD: user_id has millions of unique values

sum by (user_id) (rate(api_requests_total[5m]))



# BAD: ip_address has thousands of unique values

histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{client_ip=~".*"}[5m]))

```

**Why It's Bad**:

- **Cardinality**: Millions of time series generated (one per user_id)

- **Memory**: Prometheus stores every unique label combination

- **Performance**: Aggregating millions of series is prohibitively slow

**Fix**:

```promql

# GOOD: Aggregate to low-cardinality labels

sum by (endpoint, method) (rate(api_requests_total[5m]))



# GOOD: Use recording rules to pre-aggregate

# prometheus-rules.yml

groups:

  - name: api_metrics

    rules:

      - record: api:requests:rate5m

        expr: sum by (endpoint, method, status) (rate(api_requests_total[5m]))



# Then use in dashboard

api:requests:rate5m

```

**Detection Script**:

```python

import re



def detect_high_cardinality_queries(dashboard_json: Dict) -> List[Dict]:

    """

    Detect PromQL queries with high-cardinality label usage.



    Returns:

        [{"panel": str, "expr": str, "issue": str}]

    """

    high_cardinality_labels = [

        "user_id", "request_id", "trace_id", "ip_address", "client_ip",

        "session_id", "transaction_id", "email"

    ]



    issues = []



    for panel in dashboard_json.get("panels", []):

        for target in panel.get("targets", []):

            expr = target.get("expr", "")



            # Check if query uses high-cardinality labels

            for label in high_cardinality_labels:

                if label in expr:

                    issues.append({

                        "panel": panel.get("title"),

                        "expr": expr,

                        "issue": f"High-cardinality label '{label}' detected"

                    })



    return issues

```

**Best Practice**: Use labels with <1000 unique values (ideally <100)

---

### Anti-Pattern 4: Missing Contextual Information

**Problem**: Panels lack units, thresholds, descriptions, or legends making data interpretation impossible.

**Symptoms**:

- "Is 5000 good or bad?" questions

- No units on Y-axis (is it ms, seconds, GB?)

- Missing alert thresholds for context

- Cryptic PromQL expressions without explanation

**Example**:

```json
{
  "title": "Metric 1", // Non-descriptive

  "targets": [
    {
      "expr": "rate(http_requests_total[5m])",

      "legendFormat": "" // Empty legend
    }
  ],

  "fieldConfig": {
    "defaults": {
      // Missing: unit, thresholds, description
    }
  }
}
```

**Why It's Bad**:

- **Usability**: Users can't interpret data without context

- **Debugging**: No way to know if values are normal or anomalous

- **Communication**: Can't share screenshots with stakeholders

**Fix**:

```json
{
  "title": "HTTP Request Rate", // Descriptive

  "description": "Rate of HTTP requests per second across all endpoints. Alert threshold: >1000 req/s indicates traffic spike.",

  "targets": [
    {
      "expr": "sum(rate(http_requests_total[5m]))",

      "legendFormat": "Total Requests" // Clear legend
    }
  ],

  "fieldConfig": {
    "defaults": {
      "unit": "reqps", // Requests per second

      "thresholds": {
        "mode": "absolute",

        "steps": [
          { "value": 0, "color": "green" },

          { "value": 800, "color": "yellow" }, // Warning

          { "value": 1000, "color": "red" } // Critical
        ]
      }
    }
  }
}
```

**Automated Fix**:

```python

def add_contextual_information(panel: Dict) -> Dict:

    """

    Enhance panel with contextual information.



    Adds:

    - Units based on metric name

    - Thresholds for common metrics

    - Descriptions

    """

    # Infer unit from metric name

    unit_map = {

        "bytes": "bytes",

        "seconds": "s",

        "duration": "ms",

        "requests": "reqps",

        "errors": "errors",

        "percent": "percent"

    }



    title = panel.get("title", "").lower()

    for keyword, unit in unit_map.items():

        if keyword in title:

            panel.setdefault("fieldConfig", {}).setdefault("defaults", {})["unit"] = unit

            break



    # Add default thresholds for rate/error metrics

    if "rate" in title or "error" in title:

        panel["fieldConfig"]["defaults"]["thresholds"] = {

            "mode": "absolute",

            "steps": [

                {"value": 0, "color": "green"},

                {"value": 80, "color": "yellow"},

                {"value": 95, "color": "red"}

            ]

        }



    # Add description template if missing

    if not panel.get("description"):

        # Generate contextual description based on panel type and queries

        panel_type = panel.get("type", "graph")

        title = panel.get("title", "Untitled Panel")



        # Extract first query for context

        first_query = ""

        targets = panel.get("targets", [])

        if targets and targets[0].get("expr"):

            first_query = targets[0]["expr"][:100]  # First 100 chars



        # Generate template based on panel type

        if panel_type == "graph":

            panel["description"] = (

                f"**{title}** - Time-series visualization showing metric trends over time.\n\n"

                f"**Query**: \n\n"

                f"**Use this panel to**: Monitor changes and identify patterns in the metric."

            )

        elif panel_type == "stat":

            panel["description"] = (

                f"**{title}** - Single value metric display with threshold indicators.\n\n"

                f"**Query**: \n\n"

                f"**Use this panel to**: Quickly assess current state and compare against thresholds."

            )

        elif panel_type == "table":

            panel["description"] = (

                f"**{title}** - Tabular data view for detailed metric analysis.\n\n"

                f"**Query**: \n\n"

                f"**Use this panel to**: Examine individual metric values and perform comparisons."

            )

        else:

            panel["description"] = (

                f"**{title}** - Dashboard panel showing {panel_type} visualization.\n\n"

                f"**Query**: \n\n"

                f"**Use this panel to**: Review metric data in {panel_type} format."

            )



    return panel

```

**Best Practice**: Every panel must have unit, thresholds, legend, and description

---

### Anti-Pattern 5: Unbounded Time Ranges in Queries

**Problem**: Using PromQL range vectors without time bounds, querying entire metric history.

**Symptoms**:

- Queries take minutes to execute

- Prometheus "query timeout" errors

- Memory spikes during dashboard load

- Different results depending on time range selector

**Example**:

```promql

# BAD: Queries entire history of metric (potentially years of data)

rate(http_requests_total[])



# BAD: Unbounded offset (queries from beginning of time)

rate(http_requests_total[5m] offset 0)

```

**Why It's Bad**:

- **Performance**: Processing years of data for single query

- **Consistency**: Results change based on dashboard time range

- **Resource Usage**: Excessive memory and CPU consumption

**Fix**:

```promql

# GOOD: Explicit time range

rate(http_requests_total[5m])



# GOOD: Bounded offset

rate(http_requests_total[5m] offset 1h)



# GOOD: Use $__range variable in Grafana for dynamic ranges

rate(http_requests_total[$__range])

```

**Detection**:

```python

import re



def detect_unbounded_ranges(dashboard_json: Dict) -> List[Dict]:

    """

    Detect PromQL queries with unbounded time ranges.



    Returns:

        [{"panel": str, "expr": str, "issue": str}]

    """

    issues = []

    unbounded_pattern = re.compile(r'\[[^\]]*\]')  # Empty brackets or no duration



    for panel in dashboard_json.get("panels", []):

        for target in panel.get("targets", []):

            expr = target.get("expr", "")



            # Check for [] or missing range vector

            if "[]" in expr:

                issues.append({

                    "panel": panel.get("title"),

                    "expr": expr,

                    "issue": "Unbounded range vector [] detected"

                })



            # Check for rate/increase without range vector

            if re.search(r'(rate|increase)\([^[]+\)', expr):

                issues.append({

                    "panel": panel.get("title"),

                    "expr": expr,

                    "issue": "Missing range vector on rate/increase function"

                })



    return issues

```

**Best Practice**: Always specify explicit duration in range vectors (5m, 1h, etc.)

---

### Anti-Pattern 6: Regex Label Matching Abuse

**Problem**: Using regex matchers like `label=~".*"` or `label!~".*"` causing inefficient queries.

**Symptoms**:

- Slow query execution (>5 seconds)

- High Prometheus CPU usage

- Queries return too much data

- Unexpected metric matches

**Example**:

```promql

# BAD: Matches everything (equivalent to no filter)

http_requests_total{endpoint=~".*"}



# BAD: Expensive negative regex

http_requests_total{endpoint!~".*admin.*"}



# BAD: Overly broad regex

http_requests_total{status=~"[0-9]+"}

```

**Why It's Bad**:

- **Performance**: Regex evaluation is expensive (CPU-intensive)

- **Correctness**: `.*` matches everything, provides no filtering

- **Cardinality**: Unfiltered queries return all label combinations

**Fix**:

```promql

# GOOD: Exact match

http_requests_total{endpoint="/api/users"}



# GOOD: OR condition for multiple values

http_requests_total{endpoint=~"/api/users|/api/posts"}



# GOOD: Anchored prefix match

http_requests_total{endpoint=~"/api/.*"}



# GOOD: Use label_replace for transformation, not filtering

label_replace(http_requests_total, "status_class", "${1}xx", "status", "([0-9]).*")

```

**Detection**:

```python

def detect_regex_abuse(dashboard_json: Dict) -> List[Dict]:

    """

    Detect inefficient regex label matchers in PromQL.



    Returns:

        [{"panel": str, "expr": str, "issue": str}]

    """

    issues = []

    problematic_patterns = [

        (r'=~"\.\*"', "Match-all regex =~\".*\" provides no filtering"),

        (r'!~"\.\*"', "Expensive negative regex !~\".*\""),

        (r'=~"\[', "Unanchored regex character class (use prefix match)"),

    ]



    for panel in dashboard_json.get("panels", []):

        for target in panel.get("targets", []):

            expr = target.get("expr", "")



            for pattern, message in problematic_patterns:

                if re.search(pattern, expr):

                    issues.append({

                        "panel": panel.get("title"),

                        "expr": expr,

                        "issue": message

                    })



    return issues

```

**Best Practice**: Use exact matches when possible, anchor regex patterns, avoid `.*` matchers

---

### Anti-Pattern 7: Missing Error Handling in Complex Queries

**Problem**: PromQL queries that fail silently when metrics missing, returning empty graphs without explanation.

**Symptoms**:

- Empty panels with no error message

- "No data" without context

- Queries work in PromQL console but not dashboard

- Dashboards break after metric name changes

**Example**:

```promql

# BAD: Returns empty if metric doesn't exist (no indication of problem)

rate(nonexistent_metric[5m])



# BAD: Division by zero if denominator is 0

sum(http_errors_total) / sum(http_requests_total)

```

**Why It's Bad**:

- **Debugging**: No indication whether metric is missing or truly zero

- **Reliability**: Dashboards break silently after schema changes

- **User Experience**: "No data" frustrates users (is it broken or just no traffic?)

**Fix**:

```promql

# GOOD: Use absent() to detect missing metrics

absent(http_requests_total) OR rate(http_requests_total[5m])

# Returns 1 if metric missing, otherwise shows rate



# GOOD: Handle division by zero

sum(http_errors_total) / (sum(http_requests_total) > 0)

# Returns NaN if denominator is 0 (shows as "N/A" in Grafana)



# GOOD: Fallback to default value

rate(http_requests_total[5m]) OR vector(0)

# Shows 0 if metric doesn't exist



# GOOD: Use or with metric fallback

rate(new_metric_name[5m]) OR rate(old_metric_name[5m])

# Supports metric renames gracefully

```

**Panel Configuration for Missing Data**:

```json
{
  "fieldConfig": {
    "defaults": {
      "noValue": "Metric not available", // Show message instead of empty

      "color": {
        "mode": "thresholds"
      },

      "thresholds": {
        "steps": [
          { "value": null, "color": "transparent" } // Gray out if no data
        ]
      }
    }
  }
}
```

**Best Practice**: Use `absent()`, `OR vector()`, and `noValue` configuration for graceful degradation

---

## Integration Points

### Integration 1: CI/CD Pipeline (GitHub Actions)

**Purpose**: Automate dashboard validation on every pull request and deployment.

**Workflow**:

1. **Trigger**: PR modifying `dashboards/**/*.json`

2. **Validation**: Run 4-stage pipeline (schema → PromQL → datasource → quality)

3. **Report**: Comment validation results on PR

4. **Gate**: Block merge if quality score < 70 or critical issues

5. **Deploy**: On merge to main, update ConfigMaps and restart Grafana

**Integration Points**:

- **GitHub Actions**: Workflow orchestration

- **dashboard-linter**: Schema validation

- **promtool**: PromQL syntax checking

- **pint**: Anti-pattern linting

- **Python scripts**: Quality scoring and reporting

- **kubectl**: ConfigMap deployment

**See**: Workflow 1 above for complete GitHub Actions YAML

---

### Integration 2: kubectl Validation

**Purpose**: Validate generated ConfigMaps before applying to Kubernetes cluster.

**Workflow**:

1. Generate ConfigMaps from dashboard JSONs

2. Validate YAML syntax: `kubectl apply --dry-run=client -f configmap.yaml`

3. Check size limits: Ensure each ConfigMap < 1MB

4. Validate label selectors for Grafana sidecar

5. Apply to cluster: `kubectl apply -f configmap.yaml`

6. Verify Grafana dashboard reload: Check Grafana provisioning logs

**Commands**:

```bash

# Dry-run validation (checks syntax and size)

kubectl apply --dry-run=server -f k8s/base/dashboards/ --namespace=monitoring



# Check ConfigMap size before applying

kubectl get configmap grafana-dashboards -n monitoring -o json | jq '.data | length'



# Apply ConfigMaps

kubectl apply -f k8s/base/dashboards/ --namespace=monitoring



# Restart Grafana to reload dashboards

kubectl rollout restart deployment/grafana -n monitoring



# Check Grafana logs for dashboard loading errors

kubectl logs -f deployment/grafana -n monitoring | grep -i dashboard

```

---

### Integration 3: Grafana API for Runtime Validation

**Purpose**: Test dashboards against live Grafana instance to validate datasource connectivity and query execution.

**Workflow**:

1. **Upload**: POST dashboard JSON to Grafana API

2. **Snapshot**: Create dashboard snapshot for testing

3. **Query Test**: Execute panel queries against datasources

4. **Validation**: Check for query errors, timeouts, missing datasources

5. **Cleanup**: Delete test snapshot after validation

**Python Integration**:

```python

import requests

from typing import Dict, Tuple



class GrafanaAPIClient:

    """Client for Grafana API dashboard validation."""



    def __init__(self, base_url: str, api_key: str):

        self.base_url = base_url.rstrip("/")

        self.headers = {"Authorization": f"Bearer {api_key}"}



    def validate_dashboard_runtime(self, dashboard_json: Dict) -> Tuple[bool, List[str]]:

        """

        Validate dashboard by uploading to Grafana and testing queries.



        Returns:

            (success, errors)

        """

        errors = []



        # Step 1: Upload dashboard as snapshot (non-persistent)

        snapshot_url = f"{self.base_url}/api/snapshots"

        response = requests.post(

            snapshot_url,

            json={"dashboard": dashboard_json},

            headers=self.headers

        )



        if response.status_code != 200:

            return (False, [f"Failed to create snapshot: {response.text}"])



        snapshot_id = response.json()["key"]



        try:

            # Step 2: Test datasource connectivity

            for panel in dashboard_json.get("panels", []):

                for target in panel.get("targets", []):

                    datasource_uid = target.get("datasource", {}).get("uid")



                    if datasource_uid:

                        ds_health = self._test_datasource(datasource_uid)

                        if not ds_health["healthy"]:

                            errors.append(

                                f"Panel '{panel.get('title')}': "

                                f"Datasource {datasource_uid} unhealthy"

                            )



            # Step 3: Execute test queries

            for panel in dashboard_json.get("panels", []):

                for target in panel.get("targets", []):

                    expr = target.get("expr")

                    if expr:

                        query_result = self._test_query(target)

                        if not query_result["success"]:

                            errors.append(

                                f"Panel '{panel.get('title')}': "

                                f"Query failed: {query_result['error']}"

                            )



            return (len(errors) == 0, errors)



        finally:

            # Step 4: Cleanup snapshot

            self._delete_snapshot(snapshot_id)



    def _test_datasource(self, uid: str) -> Dict:

        """Test datasource connectivity."""

        url = f"{self.base_url}/api/datasources/uid/{uid}/health"

        response = requests.get(url, headers=self.headers)



        return {

            "healthy": response.status_code == 200,

            "status": response.json() if response.status_code == 200 else {}

        }



    def _test_query(self, target: Dict) -> Dict:

        """Execute PromQL query against datasource."""

        url = f"{self.base_url}/api/ds/query"



        payload = {

            "queries": [target],

            "from": "now-5m",

            "to": "now"

        }



        response = requests.post(url, json=payload, headers=self.headers)



        if response.status_code != 200:

            return {"success": False, "error": response.text}



        # Check for query execution errors in response

        results = response.json()

        if "error" in results:

            return {"success": False, "error": results["error"]}



        return {"success": True, "error": None}



    def _delete_snapshot(self, snapshot_id: str):

        """Delete test snapshot."""

        url = f"{self.base_url}/api/snapshots/{snapshot_id}"

        requests.delete(url, headers=self.headers)



# Usage in validation pipeline

def validate_datasources(dashboard_json: Dict) -> ValidationResult:

    """

    Execute Stage 3: Datasource testing.



    Returns:

        ValidationResult with datasource connectivity issues

    """

    import time

    start_time = time.time()



    grafana_url = os.getenv("GRAFANA_URL", "http://localhost:3000")

    grafana_api_key = os.getenv("GRAFANA_API_KEY")



    if not grafana_api_key:

        execution_time_ms = int((time.time() - start_time) * 1000)

        return ValidationResult(

            stage=ValidationStage.DATASOURCE,

            passed=True,  # Skip if no API key (CI environment)

            issues=[{

                "severity": ValidationSeverity.INFO,

                "message": "Datasource testing skipped (no GRAFANA_API_KEY)"

            }],

            execution_time_ms=execution_time_ms

        )



    client = GrafanaAPIClient(grafana_url, grafana_api_key)

    success, errors = client.validate_dashboard_runtime(dashboard_json)



    issues = []

    for error in errors:

        issues.append({

            "severity": ValidationSeverity.WARNING,  # Non-blocking

            "message": error,

            "location": "datasource"

        })



    execution_time_ms = int((time.time() - start_time) * 1000)



    return ValidationResult(

        stage=ValidationStage.DATASOURCE,

        passed=success,

        issues=issues,

        execution_time_ms=execution_time_ms

    )

```

**Required Environment Variables**:

- `GRAFANA_URL`: Base URL of Grafana instance (e.g., `http://localhost:3000`)

- `GRAFANA_API_KEY`: Service account token with dashboard edit permissions

**Security Considerations**:

- Store API keys in GitHub Secrets (not in code)

- Use service accounts with minimum required permissions (dashboard:write, datasource:read)

- Delete snapshots immediately after testing (no persistent test dashboards)

---

## Summary

This validation workflows guide provides comprehensive automation for Grafana dashboard quality assurance:

1. **4-Stage Validation Pipeline**: Schema → PromQL → Datasource → Quality (sequential fail-fast)

2. **Official Tooling**: dashboard-linter (Grafana), promtool (Prometheus), pint (Cloudflare)

3. **Quality Scoring**: Objective formula `(signal × 0.6) + (usability × 0.3) + (performance × 0.1)`

4. **ConfigMap Chunking**: 4 strategies to handle 1MB Kubernetes limit (single, per-dashboard, panel-splitting, PV/PVC)

5. **CI/CD Integration**: Complete GitHub Actions workflow for automated validation and deployment

6. **Anti-Pattern Detection**: 7 common dashboard mistakes with automated fixes

7. **Multi-Tool Integration**: kubectl validation, Grafana API runtime testing, Python scripting

**Next Steps for grafana-dashboard-builder Agent**:

1. Implement `validate_dashboard_pipeline()` function as primary operation

2. Add `generate_dashboard_configmaps()` for intelligent chunking

3. Integrate quality scoring into output schema (`quality_score` field)

4. Create `fix_anti_patterns()` automated remediation

5. Support CI/CD artifact generation (validation-report.md, schema-report.json)

**Sources**:

- Grafana dashboard-linter: https://github.com/grafana/dashboard-linter

- Prometheus promtool: https://prometheus.io/docs/prometheus/latest/command-line/promtool/

- Cloudflare pint: https://github.com/cloudflare/pint

- O'Reilly Practical Monitoring (Chapter 7: Dashboard Design)

- Kubernetes ConfigMap documentation

- Grafana provisioning docs: https://grafana.com/docs/grafana/latest/administration/provisioning/