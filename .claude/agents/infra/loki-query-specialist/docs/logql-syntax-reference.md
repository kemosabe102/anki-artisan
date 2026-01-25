# LogQL Syntax Reference

**Category**: domain-specific
**Domain**: Loki query language fundamentals and operators
**Confidence**: 0.95
**Last Updated**: 2025-11-10T00:00:00Z
**Agent**: loki-query-specialist

---

## Overview

LogQL v3.5.7 syntax fundamentals including stream selectors, line filters, parsers, label operations, and aggregation functions. This reference provides the core building blocks for constructing efficient Loki queries.

**Key Concepts**:

- **Stream Selector**: Label-based log stream filtering using equality/regex operators
- **Line Filter**: Content-based filtering of log lines within selected streams
- **Parser**: Structured extraction of fields from log content (json, logfmt, regexp, pattern)
- **Aggregation**: Time-based calculations over log data (count, rate, bytes, etc.)

---

## Core Frameworks

### Framework 1: Stream Selectors

**Purpose**: Filter log streams by labels before processing log content, reducing data volume early in query execution.

**When to Use**:
- Always as the first query component (leftmost)
- When filtering by indexed labels (service, namespace, pod, etc.)
- To narrow scope before expensive operations (parsing, aggregation)

**Components**:

1. **Equality Operator (=)**: Exact label match - `{service="auth"}`
2. **Inequality Operator (!=)**: Exclude exact match - `{service!="debug"}`
3. **Regex Match (=~)**: Pattern matching - `{pod=~"app-.*"}`
4. **Regex Not Match (!~)**: Pattern exclusion - `{namespace!~"test-.*"}`

**How to Apply**:

1. Identify indexed labels (see loki-architecture-constraints.md for 14 OTLP attributes)
2. Choose most selective label first (fewest matching streams)
3. Combine multiple selectors with commas: `{service="api", namespace="prod"}`
4. Use regex only when necessary (slower than equality)

**Example from Codebase**:

```logql
{namespace="gauntlet-agents", service_name="orchestrator"}
```

**Source**: https://grafana.com/docs/loki/latest/logql/log_queries/#log-stream-selector

---

### Framework 2: Line Filters

**Purpose**: Filter log content within selected streams before parsing, reducing data processed by expensive parser operations.

**When to Use**:
- After stream selector, before parser
- When filtering by log message content (not labels)
- To eliminate irrelevant logs early

**Components**:

1. **Contains (|=)**: Line contains substring - `|= "error"`
2. **Not Contains (!=)**: Line excludes substring - `!= "debug"`
3. **Regex Match (|~)**: Line matches pattern - `|~ "error|warn"`
4. **Regex Not Match (!~)**: Line excludes pattern - `!~ "info|debug"`
5. **IP Filter (ip())**: IP address/CIDR matching - `| ip("192.168.1.0/24")`
6. **Pattern Match**: Structured pattern - `| pattern "<_> level=<level>"`

**How to Apply**:

1. Place immediately after stream selector
2. Use fastest filter first: contains > regex > pattern
3. Chain multiple filters left-to-right: `|= "error" |= "database"`
4. Combine positive and negative filters: `|= "auth" != "success"`

**Example from Codebase**:

```logql
{service="api"} |= "POST" |= "/auth" != "200"
```

**Source**: https://grafana.com/docs/loki/latest/logql/log_queries/#line-filter-expression

---

### Framework 3: Parsers

**Purpose**: Extract structured fields from unstructured log content, enabling label operations and aggregations on log data.

**When to Use**:
- After stream selector and line filters
- When log format is known (JSON, logfmt, etc.)
- Before label filtering or aggregation

**Components**:

1. **JSON Parser**: Extract fields from JSON logs
   ```logql
   | json
   | json field1="json.path", field2="other.path"
   ```

2. **Logfmt Parser**: Parse key=value format
   ```logql
   | logfmt
   | logfmt level, msg
   ```

3. **Regexp Parser**: Custom extraction with named groups
   ```logql
   | regexp "(?P<method>\\w+) (?P<path>/\\S+) (?P<status>\\d+)"
   ```

4. **Pattern Parser**: Template-based extraction
   ```logql
   | pattern "<method> <path> HTTP/<version> <status>"
   ```

**How to Apply**:

1. Determine log format (see query-optimization-patterns.md for decision matrix)
2. Select appropriate parser (json > logfmt > pattern > regexp for performance)
3. Extract only needed fields (reduces memory usage)
4. Validate extraction with label filter: `| label_format extracted_field`

**Example from Codebase**:

```logql
{service="api"} | json | level="error"
```

**Source**: https://grafana.com/docs/loki/latest/logql/log_queries/#parser-expression

---

### Framework 4: Label Operations

**Purpose**: Manipulate extracted labels for filtering, formatting, and retention control.

**When to Use**:
- After parser to filter on extracted fields
- To format labels for display
- To control which labels are kept

**Components**:

1. **Label Filter**: Filter by extracted label values
   ```logql
   | level="error"
   | status >= 400
   | duration > 1s
   ```

2. **Label Format**: Rename or transform labels
   ```logql
   | label_format new_name=old_name
   | label_format message="{{ .msg }}: {{ .error }}"
   ```

3. **Keep/Drop Labels**: Control label retention
   ```logql
   | keep pod, namespace
   | drop internal_field
   ```

4. **Line Format**: Create formatted output line
   ```logql
   | line_format "{{.level}} - {{.message}}"
   ```

**How to Apply**:

1. Filter on extracted labels immediately after parsing
2. Format labels before aggregation for cleaner output
3. Drop unnecessary labels to reduce cardinality
4. Use line_format for custom log output

**Example from Codebase**:

```logql
{service="api"} | json | status >= 500 | line_format "Error: {{.message}}"
```

**Source**: https://grafana.com/docs/loki/latest/logql/log_queries/#labels-format-expression

---

### Framework 5: Aggregation Functions

**Purpose**: Calculate metrics and statistics over log data within time ranges.

**When to Use**:
- For metric queries (counts, rates, percentiles)
- With range vectors: `[5m]`, `[$__auto]`
- At end of query pipeline

**Components**:

1. **count_over_time**: Count log lines
   ```logql
   count_over_time({service="api"}[5m])
   ```

2. **rate**: Lines per second
   ```logql
   rate({service="api"}[5m])
   ```

3. **bytes_over_time**: Total bytes
   ```logql
   bytes_over_time({service="api"}[5m])
   ```

4. **bytes_rate**: Bytes per second
   ```logql
   bytes_rate({service="api"}[5m])
   ```

5. **avg_over_time**: Average of extracted numeric field
   ```logql
   avg_over_time({service="api"} | json | unwrap duration [5m])
   ```

6. **sum**: Sum values across streams
   ```logql
   sum(rate({service="api"}[5m]))
   ```

7. **topk**: Top N results
   ```logql
   topk(5, sum by (pod) (rate({service="api"}[5m])))
   ```

8. **count**: Count unique label combinations
   ```logql
   count by (status) (count_over_time({service="api"} | json [5m]))
   ```

**How to Apply**:

1. Select appropriate aggregation for metric type (count vs rate vs bytes)
2. Choose time range based on query timeframe: `[5m]` for short, `[$__auto]` for Grafana
3. Use `by (label)` to group results
4. Combine aggregations: `sum(rate(...))` for total rate across pods

**Example from Codebase**:

```logql
sum by (service_name) (count_over_time({namespace="gauntlet-agents"} |= "error" [5m]))
```

**Source**: https://grafana.com/docs/loki/latest/logql/metric_queries/#aggregation-operators

---

## Decision Trees

### Decision 1: Choosing Line Filter vs Parser

```
IF log format is unknown OR need substring search
  THEN use line filter (|= or |~)
  BECAUSE faster than parsing when format unknown

ELSE IF need to filter on structured field value
  THEN use parser + label filter
  BECAUSE enables typed comparisons (status >= 500)

ELSE IF both substring AND field filtering needed
  THEN use line filter FIRST, then parser
  BECAUSE reduces data volume before expensive parse operation
```

**Example Scenarios**:

1. **Scenario**: Find logs containing "timeout" → **Decision**: `|= "timeout"` (line filter)
2. **Scenario**: Find logs where status >= 500 → **Decision**: `| json | status >= 500` (parser + label filter)
3. **Scenario**: Find error-level logs in JSON format → **Decision**: `|= "error" | json | level="error"` (both)

---

### Decision 2: Range Vector Duration Selection

```
IF query covers <1 hour
  THEN use [1m] or [5m]
  BECAUSE fine-grained resolution for short timeframes

ELSE IF query covers 1-24 hours
  THEN use [5m] or [15m]
  BECAUSE balances resolution and query performance

ELSE IF query in Grafana dashboard
  THEN use [$__auto]
  BECAUSE automatically adjusts to dashboard time range

ELSE IF query covers >24 hours
  THEN use [1h] or [4h]
  BECAUSE prevents query timeout on large datasets
```

**Example Scenarios**:

1. **Scenario**: Dashboard with 15-minute view → **Decision**: `[$__auto]` (auto-adjusts)
2. **Scenario**: Ad-hoc query for last 5 minutes → **Decision**: `[1m]` (fine resolution)
3. **Scenario**: Weekly trend analysis → **Decision**: `[1h]` (coarse resolution)

---

## Complete Query Examples

### Example 1: Count Errors by Service

```logql
sum by (service_name) (
  count_over_time({namespace="gauntlet-agents"} |= "error" [5m])
)
```

**Explanation**:
1. Stream selector: `{namespace="gauntlet-agents"}` (filter by namespace)
2. Line filter: `|= "error"` (only lines containing "error")
3. Aggregation: `count_over_time(...[5m])` (count lines in 5-minute windows)
4. Group: `sum by (service_name)` (total per service)

---

### Example 2: HTTP Error Rate

```logql
sum by (status) (
  rate({service="api"} | json | status >= 400 [5m])
)
```

**Explanation**:
1. Stream selector: `{service="api"}` (filter by service)
2. Parser: `| json` (extract JSON fields)
3. Label filter: `| status >= 400` (HTTP errors only)
4. Aggregation: `rate(...[5m])` (errors per second)
5. Group: `sum by (status)` (total per status code)

---

### Example 3: Top 5 Pods by Log Volume

```logql
topk(5,
  sum by (pod) (
    bytes_rate({namespace="prod"}[5m])
  )
)
```

**Explanation**:
1. Stream selector: `{namespace="prod"}` (production namespace)
2. Aggregation: `bytes_rate(...[5m])` (bytes per second)
3. Group: `sum by (pod)` (total per pod)
4. Limit: `topk(5, ...)` (top 5 results)

---

### Example 4: Slow Requests (Unwrap Metric)

```logql
avg by (endpoint) (
  avg_over_time({service="api"} | json | unwrap duration [5m])
)
```

**Explanation**:
1. Stream selector: `{service="api"}` (API service)
2. Parser: `| json` (extract JSON fields)
3. Unwrap: `unwrap duration` (extract numeric duration field)
4. Aggregation: `avg_over_time(...[5m])` (average duration over 5 minutes)
5. Group: `avg by (endpoint)` (average per endpoint)

---

### Example 5: Pattern Extraction

```logql
{service="nginx"}
| pattern "<ip> - - <_> \"<method> <path> <_>\" <status> <size>"
| status >= 400
```

**Explanation**:
1. Stream selector: `{service="nginx"}` (Nginx logs)
2. Parser: `| pattern "..."` (extract fields from common log format)
3. Label filter: `| status >= 400` (filter by extracted status)

---

### Example 6: Regex Extraction

```logql
{service="auth"}
| regexp "user=(?P<user>\\w+) action=(?P<action>\\w+)"
| action="login"
```

**Explanation**:
1. Stream selector: `{service="auth"}` (auth service)
2. Parser: `| regexp "..."` (extract user and action fields)
3. Label filter: `| action="login"` (login events only)

---

### Example 7: Combined Aggregations

```logql
sum(
  count_over_time({namespace="gauntlet-agents"} [5m])
)
/
sum(
  count_over_time({namespace="gauntlet-agents"} |= "error" [5m])
)
```

**Explanation**:
1. Numerator: Total log lines in 5 minutes
2. Denominator: Error log lines in 5 minutes
3. Result: Error rate percentage

---

## Glossary

- **Stream Selector**: Label-based filter to select log streams (e.g., `{service="api"}`)
- **Line Filter**: Content-based filter on log lines (e.g., `|= "error"`)
- **Parser**: Extracts structured fields from log content (json, logfmt, regexp, pattern)
- **Label Filter**: Filter on extracted label values (e.g., `| status >= 500`)
- **Range Vector**: Time window for aggregation (e.g., `[5m]`, `[$__auto]`)
- **Aggregation**: Metric calculation over logs (count_over_time, rate, etc.)
- **Unwrap**: Extract numeric field for metric aggregations (e.g., `unwrap duration`)
- **Cardinality**: Number of unique label combinations (high cardinality = performance impact)

---

## Sources & References

1. Grafana Loki Documentation - LogQL Log Queries: https://grafana.com/docs/loki/latest/logql/log_queries/
   - Accessed: 2025-11-10
   - Confidence: 0.95

2. Grafana Loki Documentation - LogQL Metric Queries: https://grafana.com/docs/loki/latest/logql/metric_queries/
   - Accessed: 2025-11-10
   - Confidence: 0.95

3. Grafana Loki Documentation - Query Language: https://grafana.com/docs/loki/latest/query/
   - Accessed: 2025-11-10
   - Confidence: 0.95

---

## Changelog

- **2025-11-10**: Initial documentation created from researcher-external findings (confidence: 0.95)

---

## Related Documentation

- `loki-architecture-constraints.md`: Local Loki configuration and indexed labels
- `query-optimization-patterns.md`: Parser selection and query performance optimization
- `api-validation-workflow.md`: Loki HTTP API for query testing
