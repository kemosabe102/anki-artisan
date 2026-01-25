---
name: logql-queries
description: >
  Use this skill when constructing LogQL queries, selecting parsers, or
  optimizing log queries. Covers parser decision tree, filter ordering,
  anti-patterns, and performance optimization.
  Keywords: logql, loki, parser, json, logfmt, pattern, regexp, logs.
---

# LogQL Query Construction

*Parser selection, filter optimization, and anti-pattern avoidance for Loki queries*

## Reference Documentation

**Detailed Guides** (read when relevant):
- **Parser Selection** → [reference/parser-selection.md](reference/parser-selection.md)

## Scripts

**Validation Tools**:
- **Validate LogQL** → `python scripts/validate_logql.py '{app="api"} |= "error"'`
- **Detect Log Format** → `python scripts/detect_log_format.py --file sample.log`

---

## Parser Performance Hierarchy

| Parser | Relative Speed | Use Case |
|--------|----------------|----------|
| `json` | 100x (baseline) | JSON-formatted logs |
| `logfmt` | 100x | Key=value formatted logs |
| `pattern` | 10x | Consistent structure, custom delimiter |
| `regexp` | 1x (slowest) | Complex/irregular patterns |

**Rule**: Always prefer higher-speed parsers when log format permits.

---

## Parser Selection Decision Tree

```
START
  │
  ├─ Is log JSON formatted?
  │   YES → Use `| json`
  │   NO ↓
  │
  ├─ Is log key=value (logfmt)?
  │   YES → Use `| logfmt`
  │   NO ↓
  │
  ├─ Does log have consistent structure?
  │   YES → Use `| pattern`
  │   NO ↓
  │
  └─ Complex/irregular format
      → Use `| regexp` (last resort)

ALWAYS: Apply filter BEFORE parser (2-5x speedup)
```

---

## Filter BEFORE Parser Rule

**Critical Performance Optimization**: 2-5x speedup

```logql
# BAD - Parses all lines, then filters
{job="app"} | json | status >= 500

# GOOD - Filters first, parses fewer lines
{job="app"} |= "error" | json | status >= 500
```

**Why**: Line filters (`|=`, `!=`, `|~`, `!~`) are applied BEFORE parsing. Reducing the number of lines to parse dramatically improves performance.

---

## Parser Examples

### JSON Parser

```logql
# Extract fields from JSON logs
{job="api"} | json | level="error" | line_format "{{.message}}"

# With label extraction
{job="api"} | json status_code="status", err="error.message"
```

### Logfmt Parser

```logql
# Parse key=value logs
{job="nginx"} | logfmt | status >= 400

# Example log: level=info msg="request completed" status=200 duration=1.5s
```

### Pattern Parser

```logql
# Parse structured logs with custom format
{job="access"} | pattern `<ip> - - [<timestamp>] "<method> <path> <_>" <status>`

# Example log: 192.168.1.1 - - [10/Oct/2023:13:55:36] "GET /api/users HTTP/1.1" 200
```

### Regexp Parser

```logql
# Complex/irregular patterns (last resort)
{job="legacy"} | regexp `(?P<timestamp>\d{4}-\d{2}-\d{2}) (?P<level>\w+): (?P<message>.*)`

# Use named capture groups for field extraction
```

---

## 10 Anti-Pattern Categories

| # | Anti-Pattern | Impact | Fix |
|---|--------------|--------|-----|
| 1 | **JSON-in-String** | 10x slowdown | Emit proper JSON directly |
| 2 | **High-Cardinality Labels** | 73% cost increase | Move to structured_metadata |
| 3 | **Label Explosion** | Stream count explosion | Reduce label dimensions |
| 4 | **Mixed Log Formats** | Complex parsing required | Standardize on single format |
| 5 | **Label vs Field Confusion** | Index bloat | Use labels for filtering only |
| 6 | **Parsing Before Filtering** | 2-5x slowdown | Filter first with `|=`, `!=` |
| 7 | **Regex for Simple Patterns** | 100x slower | Use json/logfmt instead |
| 8 | **Unstructured Critical Logs** | Query complexity | Adopt structured logging |
| 9 | **TSV Without Explicit Parsing** | Inconsistent extraction | Use regexp with named groups |
| 10 | **JSON Parser on OTLP Logs** | JSONParserErr | Access OTLP attributes directly |

---

## Common Mistakes

### Mistake 1: Wrong Parser for Format

```logql
# WRONG - Using regexp for JSON
{job="api"} | regexp `"status":(?P<status>\d+)`

# CORRECT - Use json parser
{job="api"} | json | status >= 400
```

### Mistake 2: Not Filtering First

```logql
# WRONG - Parses everything
{job="api"} | json | level="error"

# CORRECT - Filter narrows before parse
{job="api"} |= "error" | json | level="error"
```

### Mistake 3: High-Cardinality Labels

```logql
# WRONG - user_id as label (millions of streams)
{job="api", user_id="12345"}

# CORRECT - user_id extracted post-parse
{job="api"} | json | user_id="12345"
```

### Mistake 4: Overly Broad Queries

```logql
# WRONG - Scans all logs
{job=~".+"} | json | status >= 500

# CORRECT - Narrow stream selector
{job="api", environment="production"} |= "error" | json | status >= 500
```

---

## Trade-Off Analysis

| Factor | json/logfmt | pattern | regexp |
|--------|-------------|---------|--------|
| **Speed** | Fastest (100x) | Fast (10x) | Slowest (1x) |
| **Flexibility** | Low (format-specific) | Medium | High (any pattern) |
| **Maintainability** | High | Medium | Low |
| **Setup Effort** | None | Define pattern | Write regex |
| **Error Tolerance** | Strict | Moderate | Flexible |

**Decision Matrix**:
- Speed critical? → json/logfmt
- Custom format? → pattern
- Legacy/irregular? → regexp (with caching)

---

## Aggregation Patterns

### Count by Level

```logql
sum by (level) (count_over_time({job="api"} | json [5m]))
```

### Error Rate

```logql
sum(count_over_time({job="api"} |= "error" [5m]))
/
sum(count_over_time({job="api"} [5m]))
* 100
```

### Bytes per Service

```logql
sum by (service) (bytes_over_time({namespace="prod"} [1h]))
```

### Log Volume Trend

```logql
sum(rate({job="api"} [5m])) by (level)
```

---

## Line Format Templates

### Extract Specific Fields

```logql
{job="api"} | json | line_format "{{.level}}: {{.message}}"
```

### Conditional Formatting

```logql
{job="api"} | json | line_format `{{ if eq .level "error" }}🔴{{ else }}🟢{{ end }} {{.message}}`
```

### Timestamp Reformatting

```logql
{job="api"} | json | line_format "{{.timestamp | date \"15:04:05\"}} {{.message}}"
```

---

## Quick Reference Checklist

Before writing a LogQL query, verify:

- [ ] **Stream selector is narrow** (specific job, namespace, environment)
- [ ] **Line filters applied FIRST** (`|=`, `!=` before parsers)
- [ ] **Correct parser selected** (json > logfmt > pattern > regexp)
- [ ] **No high-cardinality labels** (user_id, request_id as fields, not labels)
- [ ] **Time range is bounded** (avoid open-ended queries)

### Query Template

```logql
{job="<service>", namespace="<ns>"}   # 1. Narrow stream selector
  |= "<filter_term>"                   # 2. Line filter FIRST
  | <parser>                           # 3. Parser (json/logfmt/pattern/regexp)
  | <field_filter>                     # 4. Field-based filtering
  | line_format "{{.field}}"           # 5. Optional: format output
```

---

## OODA Loop for Query Construction

1. **Observe**: User's extraction goal, log sample, existing queries
2. **Orient**: Best parser strategy, performance implications, anti-pattern detection
3. **Decide**: Select parser, prioritize recommendations, construct filters
4. **Act**: Build query, test via API, document rationale with evidence

---

## Quality Standards

When constructing queries, ensure:

1. Parser selection includes performance rationale (cite benchmarks)
2. All queries apply filter BEFORE parser (2-5x speedup)
3. Anti-pattern detection performed (10 categories)
4. Recommendations cite evidence sources (Grafana blog, case studies)
5. OTLP logs never use `| json` parser (check service_namespace)
