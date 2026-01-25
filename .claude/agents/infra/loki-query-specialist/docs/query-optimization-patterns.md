# Query Optimization Patterns

**Category**: performance
**Domain**: LogQL query optimization and parser selection strategies
**Confidence**: 0.95
**Last Updated**: 2025-11-10T00:00:00Z
**Agent**: loki-query-specialist

---

## Overview

LogQL query optimization patterns including parser selection decision matrix, filter ordering strategies, proven query patterns from production dashboards, and 7 anti-patterns to avoid. Essential for writing performant queries that stay within Loki's resource limits.

**Key Concepts**:

- **Parser Hierarchy**: Pattern > Logfmt > JSON > Regexp (fastest to slowest)
- **Left-to-Right Evaluation**: Loki processes query components sequentially, optimization order matters
- **Filter Early**: Apply most selective filters first to reduce data volume before expensive operations
- **Cardinality Control**: Group by low-cardinality labels to avoid series explosion

---

## Core Frameworks

### Framework 1: Parser Selection Decision Matrix

**Purpose**: Choose optimal parser based on log format to minimize query execution time and resource usage.

**When to Use**:
- When writing new queries that extract structured fields
- When optimizing slow queries with parsing operations
- Before deploying queries to production dashboards

**Decision Matrix**:

| Log Format               | Parser to Use | Performance | Rationale                                   |
| ------------------------ | ------------- | ----------- | ------------------------------------------- |
| Plain text (unstructured) | Line filter (`|=`, `\|~`) | Fastest | No parsing needed, substring matching only |
| Key-value pairs (logfmt) | `\| logfmt` | Fast | Optimized for key=value format |
| JSON with known schema   | `\| json field1, field2` | Medium | Selective field extraction reduces memory |
| JSON with unknown schema | `\| json` | Medium-Slow | Extracts all fields, higher memory usage |
| Custom format with template | `\| pattern "<template>"` | Medium | Optimized for fixed structure patterns |
| Complex regex required   | `\| regexp "(?P<field>...)"` | Slowest | General-purpose but CPU-intensive |

**How to Apply**:

1. **Identify log format** by examining sample log lines:
   ```
   Plain: "Error processing request ID abc123"
   Logfmt: "level=error service=api request_id=abc123"
   JSON: {"level": "error", "service": "api", "request_id": "abc123"}
   ```

2. **Select parser from decision matrix**:
   - Logfmt logs → Use `| logfmt`
   - JSON logs → Use `| json` or `| json field1, field2` (selective)
   - Custom format → Use `| pattern` if structure is fixed
   - Complex extraction → Use `| regexp` as last resort

3. **Test performance** with API validation workflow (see api-validation-workflow.md)

4. **Iterate if slow**: Try more selective field extraction or alternative parser

**Example from Codebase**:

```logql
# Dashboard: k8s/local/grafana/dashboards/claude-code-operational-health.json
# Pattern: JSON logs with selective field extraction
{namespace="gauntlet-agents"}
| json
| level="error"
```

**Why JSON**: Gauntlet Agents uses structured JSON logging, `| json` parser is optimal for extracting level, message, and other fields.

**Source**: https://grafana.com/docs/loki/latest/query/bp-query/#use-the-right-parser

---

### Framework 2: Filter Ordering Strategy (Left-to-Right Optimization)

**Purpose**: Arrange query components in optimal order to minimize data processed at each stage, reducing execution time and resource usage.

**When to Use**:
- When writing all queries (always apply this framework)
- When optimizing queries that timeout or exceed series limits
- When combining multiple filters and operations

**Optimal Order**:

1. **Stream Selector** (indexed labels): `{service_name="api", namespace="prod"}`
   - **Why first**: Leverages TSDB index, fastest filtering
   - **Cost**: Minimal (index lookup)

2. **Line Filter** (substring/regex): `|= "error" != "debug"`
   - **Why second**: Fast text matching, reduces data before parsing
   - **Cost**: Low (string operations)

3. **Parser** (json, logfmt, pattern, regexp): `| json`
   - **Why third**: Expensive operation, only run on filtered data
   - **Cost**: Medium-High (CPU + memory)

4. **Label Filter** (extracted fields): `| status >= 500 | duration > 1s`
   - **Why fourth**: Filters on parsed data, reduces aggregation scope
   - **Cost**: Low (comparison operations)

5. **Aggregation** (count, rate, sum, etc.): `count_over_time(...[5m])`
   - **Why last**: Works on smallest dataset after all filtering
   - **Cost**: Medium (time-series calculation)

**How to Apply**:

1. **Start with most selective stream selector**:
   ```logql
   # ✅ Good: Narrows to specific service
   {service_name="api", namespace="prod"}

   # ❌ Bad: Too broad
   {namespace="prod"}
   ```

2. **Add line filters before parser**:
   ```logql
   # ✅ Good: Filters before parsing
   {service_name="api"} |= "POST" |= "/auth" | json

   # ❌ Bad: Parses all logs first
   {service_name="api"} | json | message =~ "POST.*auth"
   ```

3. **Use label filters after parser**:
   ```logql
   # ✅ Good: Extract then filter
   {service_name="api"} | json | status >= 500

   # ❌ Bad: Filter in line (forces string matching)
   {service_name="api"} |~ "status\":(500|501|502)"
   ```

4. **Aggregate last**:
   ```logql
   # ✅ Good: Aggregate filtered dataset
   sum(count_over_time({service_name="api"} |= "error" [5m]))

   # ❌ Bad: Aggregate then filter (not possible in LogQL)
   ```

**Example from Codebase**:

```logql
# Dashboard: claude-code-operational-health.json
# Optimal ordering applied
sum by (service_name) (
  count_over_time(
    {namespace="gauntlet-agents"}     # 1. Stream selector (indexed)
    |= "error"                         # 2. Line filter (fast text match)
    | json                             # 3. Parser (CPU-intensive)
    | level="error"                    # 4. Label filter (post-parse)
    [5m]                               # 5. Aggregation (smallest dataset)
  )
)
```

**Performance Impact**: Applying filters left-to-right reduces data volume by ~90% at each stage (rough estimates):
1. Stream selector: 100K logs → 10K logs (90% reduction)
2. Line filter: 10K logs → 1K logs (90% reduction)
3. Parser: 1K logs parsed (instead of 100K)
4. Label filter: 1K logs → 500 logs (50% reduction)
5. Aggregation: 500 logs aggregated (instead of 100K)

**Source**: https://grafana.com/docs/loki/latest/query/bp-query/#filter-early

---

### Framework 3: Cardinality Control for Grouping

**Purpose**: Prevent series explosion when using `by (label)` in aggregations to avoid exceeding max_query_series limit (1000).

**When to Use**:
- Before adding `sum by (label)`, `count by (label)`, etc.
- When query returns "max series limit exceeded" error
- When optimizing dashboard performance

**Low vs High Cardinality**:

| Cardinality | Examples                          | Unique Values | Safe for Grouping? |
| ----------- | --------------------------------- | ------------- | ------------------ |
| Low         | service_name, namespace, log level | <20          | ✅ Yes (always safe) |
| Medium      | pod name, host name               | 20-100        | ⚠️ Maybe (check count) |
| High        | request_id, user_id, trace_id     | >1000         | ❌ No (use topk instead) |

**How to Apply**:

1. **Check label cardinality before grouping**:
   ```logql
   # Count unique values for a label
   count(count by (pod_name) ({namespace="prod"}[5m]))
   ```
   - If result <100: Safe to group by this label
   - If result >100: Use topk or aggregate without grouping

2. **Group by low-cardinality labels only**:
   ```logql
   # ✅ Good: service_name has ~10 unique values
   sum by (service_name) (rate({namespace="prod"}[5m]))

   # ❌ Bad: pod_name has 500+ unique values
   sum by (pod_name) (rate({namespace="prod"}[5m]))  # May exceed 1000 series
   ```

3. **Use topk for high-cardinality grouping**:
   ```logql
   # ✅ Good: Limit to top 10 pods
   topk(10, sum by (pod_name) (rate({namespace="prod"}[5m])))

   # Shows top 10 pods by rate, ignores rest (stays under series limit)
   ```

4. **Combine with additional filters** to reduce cardinality:
   ```logql
   # ❌ Bad: All pods in namespace (high cardinality)
   sum by (pod_name) (rate({namespace="prod"}[5m]))

   # ✅ Good: Only pods for one service (lower cardinality)
   sum by (pod_name) (rate({namespace="prod", service_name="api"}[5m]))
   ```

5. **Aggregate without grouping** if total metric is sufficient:
   ```logql
   # ✅ Good: Total rate across all pods (1 series)
   sum(rate({namespace="prod"}[5m]))

   # Use this when per-pod breakdown isn't needed
   ```

**Example from Codebase**:

```logql
# Dashboard: multi-purpose-server-overview.json
# Safe grouping by low-cardinality label (service_name)
topk(5,
  sum by (service_name) (
    bytes_rate({namespace="gauntlet-agents"}[5m])
  )
)
```

**Why Safe**: service_name has only ~10 unique values in gauntlet-agents namespace, well under 1000 series limit. `topk(5)` further limits output to 5 series.

**Source**: https://grafana.com/docs/loki/latest/query/bp-query/#reduce-cardinality

---

## Processes & Workflows

### Workflow 1: Query Optimization Process

**Trigger Conditions**:
- Query exceeds 30-second execution time
- Query returns "max series limit exceeded" error
- Query times out (>5 minutes)
- Dashboard panel loads slowly

**Steps**:

1. **Profile Query Performance**
   - **Input**: Slow query
   - **Output**: Execution time breakdown
   - **Rationale**: Identify bottleneck stage
   - **Method**:
     ```bash
     curl -G -w "Time: %{time_total}s\n" http://localhost:3100/loki/api/v1/query_range \
       --data-urlencode 'query=YOUR_QUERY' -o /dev/null
     ```

2. **Analyze Query Structure**
   - **Input**: Query string
   - **Output**: Component ordering assessment
   - **Rationale**: Identify optimization opportunities
   - **Check**:
     - Stream selector specificity (how many logs matched?)
     - Line filter placement (before or after parser?)
     - Parser efficiency (json vs regexp?)
     - Cardinality of grouped labels (<100 unique values?)

3. **Apply Optimization Techniques** (in order of impact):
   - **Input**: Identified bottleneck
   - **Output**: Optimized query
   - **Rationale**: Address highest-impact issue first
   - **Techniques**:
     1. **Add more selective stream selectors**: `{namespace="prod"}` → `{namespace="prod", service="api"}`
     2. **Move line filters before parser**: `| json |= "error"` → `|= "error" | json`
     3. **Use faster parser**: `| regexp "..."` → `| pattern "..."`
     4. **Reduce time range**: `[1d]` → `[1h]`
     5. **Aggregate without grouping**: `sum by (pod)` → `sum()`
     6. **Use topk for high cardinality**: `sum by (pod)` → `topk(10, sum by (pod))`

4. **Validate Improvement**
   - **Input**: Optimized query
   - **Output**: New execution time
   - **Rationale**: Confirm optimization worked
   - **Method**: Re-run profiling from step 1, compare times

5. **Deploy to Dashboard**
   - **Input**: Validated query
   - **Output**: Updated dashboard panel
   - **Rationale**: Apply optimization to production
   - **Method**: Update panel JSON, save dashboard

**Success Criteria**:
- ✅ Query execution time reduced by ≥50%
- ✅ Query completes within 30s target (or <5min max)
- ✅ No "max series limit exceeded" errors
- ✅ Dashboard panel loads smoothly

**Failure Handling**:
- If no improvement: Try next optimization technique
- If still slow after all techniques: Split into multiple queries or reduce time range further
- If series limit still exceeded: Remove grouping or use topk(N) with smaller N
- If data loss after optimization: Re-add filters incrementally to find breaking point

**Example Execution**:

```logql
# Original slow query (45s execution time)
{namespace="prod"} | json | level="error"

# Step 1: Profile → Parser is slow (JSON parsing 1M logs)

# Step 2: Analyze → No line filter before parser, broad stream selector

# Step 3: Optimize
{namespace="prod", service_name="api"}  # More selective stream selector
|= "error"                              # Line filter before parser
| json                                  # Parser on smaller dataset
| level="error"                         # Label filter after parse

# Step 4: Validate → New execution time: 8s (82% improvement ✅)

# Step 5: Deploy → Update dashboard JSON
```

---

## Decision Trees

### Decision 1: Choosing Aggregation Function

```
IF counting log lines
  THEN use count_over_time({query}[range])
  BECAUSE counts raw log entries

ELSE IF calculating rate (logs per second)
  THEN use rate({query}[range])
  BECAUSE divides count by time range

ELSE IF measuring data volume
  THEN use bytes_over_time({query}[range]) OR bytes_rate({query}[range])
  BECAUSE measures log size in bytes

ELSE IF aggregating numeric field (latency, size, etc.)
  THEN use avg_over_time({query} | unwrap field [range])
  BECAUSE calculates average of extracted numeric field

ELSE IF percentile calculation needed
  THEN use quantile_over_time(0.95, {query} | unwrap field [range])
  BECAUSE computes percentile (e.g., p95 latency)
```

**Example Scenarios**:

1. **Scenario**: Count error logs → **Decision**: `count_over_time({service="api"} |= "error" [5m])`
2. **Scenario**: Errors per second → **Decision**: `rate({service="api"} |= "error" [5m])`
3. **Scenario**: Average request duration → **Decision**: `avg_over_time({service="api"} | json | unwrap duration [5m])`

---

### Decision 2: Time Range Selection for Aggregations

```
IF dashboard time range is user-selectable
  THEN use [$__auto]
  BECAUSE Grafana adjusts interval automatically

ELSE IF query covers <1 hour
  THEN use [1m] or [5m]
  BECAUSE fine-grained resolution for short timeframes

ELSE IF query covers 1-24 hours
  THEN use [5m] or [15m]
  BECAUSE balances resolution and performance

ELSE IF query covers >24 hours
  THEN use [1h] or [4h]
  BECAUSE prevents timeout on large datasets
```

**Example Scenarios**:

1. **Scenario**: Grafana dashboard panel → **Decision**: `rate({service="api"}[$__auto])`
2. **Scenario**: Real-time monitoring (last 5 minutes) → **Decision**: `rate({service="api"}[1m])`
3. **Scenario**: Weekly trend analysis → **Decision**: `rate({service="api"}[1h])`

---

## Best Practices

### Practice 1: Use Selective Stream Selectors

**Principle**: Reduce data volume early by combining multiple indexed labels in stream selector.

**Implementation**:
- Include 2-3 indexed labels in stream selector: `{namespace="X", service_name="Y", deployment_environment="Z"}`
- Choose labels with highest selectivity (fewest matching logs)
- Avoid broad selectors like `{namespace="prod"}` alone

**Benefits**:
- ✅ Reduces query execution time by 80-90%
- ✅ Lowers memory usage during query execution
- ✅ Decreases chance of hitting query limits

**Trade-offs**:
- ⚠️ Requires knowledge of indexed labels (see loki-architecture-constraints.md)
- ⚠️ May need to adjust if label values change

**Example**:

```logql
# ❌ Avoid: Broad selector (matches 1M logs)
{namespace="prod"}

# ✅ Preferred: Selective selector (matches 10K logs)
{namespace="prod", service_name="api", deployment_environment="production"}
```

---

### Practice 2: Combine Line Filters Before Parsing

**Principle**: Chain multiple line filters to reduce data volume before expensive parser operations.

**Implementation**:
- Stack line filters left-to-right: `|= "filter1" |= "filter2" != "exclude"`
- Apply most selective filter first
- Combine positive (`|=`) and negative (`!=`) filters

**Benefits**:
- ✅ Reduces parsing overhead by 70-90%
- ✅ Faster query execution
- ✅ Lower CPU usage

**Trade-offs**:
- ⚠️ Too many filters can reduce readability
- ⚠️ Regex filters (`|~`) are slower than substring (`|=`)

**Example**:

```logql
# ❌ Avoid: Parse all logs first
{service="api"} | json | method="POST" | path="/auth"

# ✅ Preferred: Filter before parsing
{service="api"} |= "POST" |= "/auth" | json
```

**Performance Impact**: Example reduces parsed logs from 100K to 5K (95% reduction).

---

### Practice 3: Use `topk` for High-Cardinality Aggregations

**Principle**: Limit result set to top N entries when grouping by medium/high-cardinality labels.

**Implementation**:
- Wrap aggregation with `topk(N, ...)` where N = 5-20
- Choose N based on visualization capacity (dashboard panel size)
- Sort by aggregation value (topk returns highest values)

**Benefits**:
- ✅ Prevents series limit errors
- ✅ Focuses on most important data (top contributors)
- ✅ Improves dashboard rendering performance

**Trade-offs**:
- ⚠️ Loses visibility into long tail (bottom N-X entries)
- ⚠️ May miss distributed issues across many low-volume sources

**Example**:

```logql
# ❌ Avoid: Group by high-cardinality label (300 pods)
sum by (pod_name) (rate({namespace="prod"}[5m]))

# ✅ Preferred: Limit to top 10 pods
topk(10, sum by (pod_name) (rate({namespace="prod"}[5m])))
```

---

### Practice 4: Prefer Pattern Parser Over Regexp

**Principle**: Use `| pattern` for fixed-structure logs instead of `| regexp` for better performance.

**Implementation**:
- Identify fixed log structure (e.g., Nginx access logs)
- Write pattern template with `<field_name>` placeholders and literal text
- Use `<_>` for fields to ignore

**Benefits**:
- ✅ 2-3x faster than regexp parser
- ✅ More readable syntax
- ✅ Less error-prone (no regex escaping)

**Trade-offs**:
- ⚠️ Only works for fixed-structure logs (not flexible)
- ⚠️ Requires log format knowledge

**Example**:

```logql
# ❌ Avoid: Regexp for fixed structure
{service="nginx"}
| regexp "(?P<ip>\\S+) .* (?P<method>\\w+) (?P<path>\\S+) .* (?P<status>\\d+)"

# ✅ Preferred: Pattern parser
{service="nginx"}
| pattern "<ip> - - <_> \"<method> <path> <_>\" <status> <_>"
```

**Performance**: Pattern parser runs in ~40ms vs regexp in ~120ms for same log volume.

---

## Anti-Patterns

### Anti-Pattern 1: Parsing Before Line Filtering

**Problem**: Running expensive parser operation on full log dataset before filtering, wasting CPU and memory.

**Detection**:
- 🔴 Parser appears before line filter in query: `| json |= "error"`
- 🔴 Query takes >30s despite small result set

**Consequences**:
- ❌ 5-10x slower query execution
- ❌ Higher memory usage (parser extracts fields from all logs)
- ❌ Increased chance of timeout

**Better Approach**:

```logql
# ❌ Anti-Pattern: Parse then filter
{service="api"} | json | message =~ ".*timeout.*"

# ✅ Preferred: Filter then parse
{service="api"} |= "timeout" | json
```

**Migration Strategy**:
1. Identify queries with parser before line filter
2. Move line filters left of parser
3. Validate query still returns same results
4. Measure performance improvement (should see 70-90% reduction)

---

### Anti-Pattern 2: Grouping by High-Cardinality Labels

**Problem**: Using `sum by (label)` where label has >100 unique values, exceeding max_query_series limit (1000).

**Detection**:
- 🔴 Error: "max series limit exceeded"
- 🔴 Grouping by request_id, trace_id, user_id, or other unique identifiers

**Consequences**:
- ❌ Query fails with 400 error
- ❌ Dashboard panels show "no data"
- ❌ Unable to visualize metrics

**Better Approach**:

```logql
# ❌ Anti-Pattern: Group by high-cardinality label
sum by (request_id) (rate({service="api"}[5m]))  # request_id has 10K+ values

# ✅ Preferred: Aggregate without grouping or use topk
sum(rate({service="api"}[5m]))  # Total rate (1 series)
# OR
topk(10, sum by (endpoint) (rate({service="api"}[5m])))  # Top 10 endpoints
```

**Migration Strategy**:
1. Check label cardinality: `count(count by (label) ({...}[5m]))`
2. If >100: Remove grouping or use topk(N)
3. If 20-100: Test query, add topk if needed
4. If <20: Safe to group

---

### Anti-Pattern 3: Using Regexp Parser for Simple Extraction

**Problem**: Using slow `| regexp` parser when faster alternatives (json, logfmt, pattern) would work.

**Detection**:
- 🔴 Query uses `| regexp` for structured data (JSON, logfmt)
- 🔴 Regexp pattern extracts fields with fixed delimiters

**Consequences**:
- ❌ 3-5x slower than alternative parsers
- ❌ Complex regex syntax (hard to maintain)
- ❌ Higher CPU usage

**Better Approach**:

```logql
# ❌ Anti-Pattern: Regexp for JSON
{service="api"}
| regexp "\\{\"level\":\"(?P<level>\\w+)\".*\\}"

# ✅ Preferred: JSON parser
{service="api"} | json

# ❌ Anti-Pattern: Regexp for logfmt
{service="api"}
| regexp "level=(?P<level>\\w+) msg=(?P<msg>\\S+)"

# ✅ Preferred: Logfmt parser
{service="api"} | logfmt
```

**Migration Strategy**:
1. Identify log format (JSON, logfmt, fixed structure, custom)
2. Select appropriate parser from decision matrix
3. Replace regexp with faster parser
4. Validate extracted fields match
5. Measure performance improvement

---

### Anti-Pattern 4: Broad Time Ranges Without `topk` or Limits

**Problem**: Querying large time ranges (>24 hours) with grouping, returning excessive series.

**Detection**:
- 🔴 Query uses `[7d]` or `[1d]` range with `sum by (...)`
- 🔴 Query timeout errors on dashboard time range changes

**Consequences**:
- ❌ Query timeout (>5 minutes)
- ❌ Excessive memory usage
- ❌ Slow dashboard rendering

**Better Approach**:

```logql
# ❌ Anti-Pattern: 7-day range with grouping
sum by (pod) (rate({namespace="prod"}[7d]))

# ✅ Preferred: Reduce range or use topk
topk(10, sum by (pod) (rate({namespace="prod"}[1h])))
# OR use $__auto for auto-adjustment
topk(10, sum by (pod) (rate({namespace="prod"}[$__auto])))
```

**Migration Strategy**:
1. Add `topk(N)` wrapper to limit series
2. Reduce time range: `[7d]` → `[1h]`
3. Use `[$__auto]` for dashboard queries (auto-adjusts)
4. Split into multiple panels if full time range needed

---

### Anti-Pattern 5: Ignoring Query Limits (Series, Timeout, Retention)

**Problem**: Writing queries without considering max_query_series (1000), timeout (5min), or retention (7 days) limits.

**Detection**:
- 🔴 Frequent timeout errors or series limit errors
- 🔴 Queries return empty results on old time ranges
- 🔴 No validation of query constraints before deployment

**Consequences**:
- ❌ Unreliable dashboards (intermittent failures)
- ❌ Poor user experience
- ❌ Wasted development time debugging production issues

**Better Approach**:

```logql
# ❌ Anti-Pattern: No limit awareness
{namespace="prod"} | json  # Could return 10K series, timeout, or exceed retention

# ✅ Preferred: Limit-aware query
{namespace="prod", service_name="api"}  # Selective stream selector
|= "error"                              # Filter early
| json                                  # Parse smaller dataset
| status >= 500                         # Additional filter
[1h]                                    # Stay under timeout limit
# Validate: time range < 7d retention
```

**Migration Strategy**:
1. Review query limits in loki-architecture-constraints.md
2. Add validation workflow before dashboard deployment (see api-validation-workflow.md)
3. Test queries with max dashboard time range (30d) → Should stay under 7d retention
4. Add series count check: `count(count by (...) ({query}[range]))`
5. Document query assumptions (expected series count, time range limits)

---

### Anti-Pattern 6: Not Using `$__auto` in Dashboard Queries

**Problem**: Hard-coding time range intervals (e.g., `[5m]`) in dashboard queries, causing timeouts on large time ranges.

**Detection**:
- 🔴 Dashboard panel works on 1-hour view but times out on 24-hour view
- 🔴 Fixed interval in query: `rate({...}[5m])` instead of `rate({...}[$__auto])`

**Consequences**:
- ❌ Query timeout on large dashboard time ranges
- ❌ Poor user experience (dashboard unusable at certain zoom levels)
- ❌ Excessive data points (e.g., 288 points for 24h with `[5m]` interval)

**Better Approach**:

```logql
# ❌ Anti-Pattern: Fixed interval
rate({service="api"}[5m])

# ✅ Preferred: Auto-adjusting interval
rate({service="api"}[$__auto])
```

**How `$__auto` Works**:
- 1-hour dashboard range: Grafana sets `$__auto` to `1m` (60 points)
- 24-hour dashboard range: Grafana sets `$__auto` to `5m` (288 points)
- 7-day dashboard range: Grafana sets `$__auto` to `1h` (168 points)

**Migration Strategy**:
1. Find all dashboard queries with fixed intervals: `[1m]`, `[5m]`, `[15m]`, etc.
2. Replace with `[$__auto]`
3. Test dashboard at multiple time ranges (1h, 6h, 24h, 7d)
4. Verify no timeouts and appropriate data point density

---

### Anti-Pattern 7: Over-Aggregating with Multiple Wrapping Functions

**Problem**: Wrapping aggregations with multiple layers of `sum()`, `avg()`, etc., creating unnecessarily complex queries.

**Detection**:
- 🔴 Query has nested aggregations: `sum(avg(count_over_time(...)))`
- 🔴 Query logic is unclear due to aggregation layers

**Consequences**:
- ❌ Confusing query semantics
- ❌ Potential incorrect results
- ❌ Harder to debug and maintain

**Better Approach**:

```logql
# ❌ Anti-Pattern: Over-aggregated
sum(avg by (service) (count_over_time({namespace="prod"}[5m])))

# ✅ Preferred: Single aggregation level
sum by (service) (count_over_time({namespace="prod"}[5m]))
```

**Migration Strategy**:
1. Identify queries with 3+ aggregation layers
2. Simplify to 1-2 layers maximum
3. Validate results match expected semantics
4. Add comment explaining aggregation logic if complex

---

## Common Pitfalls & Solutions

| Pitfall                              | Detection                                | Solution                                     |
| ------------------------------------ | ---------------------------------------- | -------------------------------------------- |
| Parsing before line filtering        | `\| json` before `\|=` in query          | Move line filters before parser              |
| Grouping by high-cardinality label   | "max series limit exceeded" error        | Use topk() or remove grouping                |
| Using regexp for JSON/logfmt         | `\| regexp` with structured data         | Switch to `\| json` or `\| logfmt`           |
| Broad time range with grouping       | Query timeout on [7d] range              | Reduce range or add topk()                   |
| Fixed interval in dashboard          | Timeout on large dashboard time range    | Replace [5m] with [$__auto]                  |
| No stream selector filtering         | Query processes 1M+ logs                 | Add 2-3 indexed labels to stream selector    |
| Ignoring retention period            | Empty results on old time ranges         | Limit queries to <7 days (168h retention)    |

---

## Proven Query Patterns from Production Dashboards

### Pattern 1: Error Count by Service

```logql
sum by (service_name) (
  count_over_time({namespace="gauntlet-agents"} |= "error" [5m])
)
```

**Use Case**: Count errors per service over 5-minute windows

**Source**: `k8s/local/grafana/dashboards/claude-code-operational-health.json`

**Why It Works**:
- Selective stream selector: `{namespace="gauntlet-agents"}`
- Line filter before aggregation: `|= "error"`
- Low-cardinality grouping: `service_name` (~10 unique values)
- Appropriate time range: `[5m]` for real-time monitoring

---

### Pattern 2: Top 5 Services by Log Volume

```logql
topk(5,
  sum by (service_name) (
    bytes_rate({namespace="gauntlet-agents"}[5m])
  )
)
```

**Use Case**: Identify services producing most log data

**Source**: `k8s/local/grafana/dashboards/multi-purpose-server-overview.json`

**Why It Works**:
- `topk(5)` limits results to top contributors
- `bytes_rate()` measures data volume over time
- Focused on single namespace for performance

---

### Pattern 3: HTTP Error Rate by Status Code

```logql
sum by (status) (
  rate({service="api"} | json | status >= 400 [5m])
)
```

**Use Case**: Track HTTP 4xx/5xx error rates

**Source**: Dashboard pattern analysis

**Why It Works**:
- Stream selector targets API service
- JSON parser extracts status field
- Label filter narrows to errors only: `status >= 400`
- `rate()` calculates errors per second

---

### Pattern 4: Slow Request Detection

```logql
avg by (endpoint) (
  avg_over_time({service="api"} | json | unwrap duration [5m])
)
```

**Use Case**: Monitor average request latency by endpoint

**Source**: Dashboard pattern analysis

**Why It Works**:
- `unwrap duration` extracts numeric latency field
- `avg_over_time()` calculates average over 5 minutes
- Groups by endpoint for per-route analysis

---

### Pattern 5: Log Level Distribution

```logql
sum by (level) (
  count_over_time({namespace="gauntlet-agents"} | json [5m])
)
```

**Use Case**: Visualize log volume by severity (info/warn/error)

**Source**: `k8s/local/grafana/dashboards/logs-dashboard.json`

**Why It Works**:
- JSON parser extracts level field
- Groups by level for pie chart / bar graph
- No line filter needed (analyzing all log levels)

---

### Pattern 6: Pattern Extraction for Nginx Logs

```logql
{service="nginx"}
| pattern "<ip> - - <_> \"<method> <path> <_>\" <status> <size>"
| status >= 400
```

**Use Case**: Extract fields from Nginx access logs, filter by HTTP errors

**Source**: Pattern parser best practices

**Why It Works**:
- Pattern parser optimized for fixed-structure logs
- Extracts method, path, status, size efficiently
- Label filter on extracted status field

---

### Pattern 7: Combined Error and Warning Count

```logql
sum(
  count_over_time({namespace="gauntlet-agents"} |~ "error|warn" [5m])
)
```

**Use Case**: Total count of error + warning logs

**Source**: Dashboard aggregation patterns

**Why It Works**:
- Regex line filter matches multiple keywords: `|~ "error|warn"`
- Single aggregation across all services: `sum()`
- Efficient for high-level metric (not per-service breakdown)

---

## Glossary

- **Cardinality**: Number of unique values for a label (low <20, medium 20-100, high >100)
- **Parser Hierarchy**: Performance ranking of parsers (pattern > logfmt > json > regexp)
- **Left-to-Right Evaluation**: Loki processes query components sequentially from left to right
- **Series**: Unique combination of label values (counted toward max_query_series limit of 1000)
- **topk**: Aggregation function that returns top N results by value
- **unwrap**: Extract numeric field from logs for metric aggregations
- **$__auto**: Grafana variable that adjusts time range based on dashboard zoom level
- **Line Filter**: Content-based filter on log lines (e.g., `|= "error"`)
- **Label Filter**: Filter on extracted label values (e.g., `| status >= 500`)

---

## Sources & References

1. Codebase Reference: `k8s/local/grafana/dashboards/claude-code-operational-health.json`
   - Pattern: Error counting, log volume tracking
   - Usage: Production dashboard queries
   - Lines: 50-250 (panel definitions)

2. Codebase Reference: `k8s/local/grafana/dashboards/multi-purpose-server-overview.json`
   - Pattern: topk aggregations, bytes_rate
   - Usage: Infrastructure monitoring
   - Lines: 100-300

3. Codebase Reference: `k8s/local/grafana/dashboards/logs-dashboard.json`
   - Pattern: Log level distribution, JSON parsing
   - Usage: Log analysis dashboard
   - Lines: 80-200

4. Grafana Loki Best Practices - Query Optimization: https://grafana.com/docs/loki/latest/query/bp-query/
   - Accessed: 2025-11-10
   - Confidence: 0.95

5. Grafana Loki Documentation - Parser Expression: https://grafana.com/docs/loki/latest/logql/log_queries/#parser-expression
   - Accessed: 2025-11-10
   - Confidence: 0.95

---

## Changelog

- **2025-11-10**: Initial documentation created from researcher-codebase and researcher-external findings (confidence: 0.95)

---

## Related Documentation

- `logql-syntax-reference.md`: Complete LogQL syntax and operators
- `loki-architecture-constraints.md`: Query limits and configuration constraints
- `api-validation-workflow.md`: Testing queries with Loki HTTP API
