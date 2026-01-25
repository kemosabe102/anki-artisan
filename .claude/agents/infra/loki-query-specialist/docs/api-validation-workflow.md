# Loki API Validation Workflow

**Category**: domain-specific
**Domain**: Loki HTTP API for query validation and testing
**Confidence**: 0.90
**Last Updated**: 2025-11-10T00:00:00Z
**Agent**: loki-query-specialist

---

## Overview

Loki HTTP API reference for query validation, including 4 core endpoints, query parameters, response formats, error handling patterns, and a 5-step validation workflow. Essential for testing queries before deploying to production dashboards.

**Key Concepts**:

- **Query Endpoint**: Execute LogQL queries and return results
- **Query Range Endpoint**: Time-series queries for metric visualization
- **Label Endpoints**: Discover available labels and their values
- **Error Handling**: 400/401/timeout error detection and recovery

---

## Core Frameworks

### Framework 1: Four Core API Endpoints

**Purpose**: Understand which endpoint to use for different query validation scenarios.

**When to Use**:
- Testing queries before adding to Grafana dashboards
- Validating LogQL syntax correctness
- Discovering available labels and values
- Debugging query performance issues

**Components**:

1. **Instant Query** (`/loki/api/v1/query`)
   - **Purpose**: Execute query at single point in time
   - **Returns**: Current log lines matching query
   - **Use case**: Ad-hoc log exploration, syntax validation

2. **Range Query** (`/loki/api/v1/query_range`)
   - **Purpose**: Execute query over time range
   - **Returns**: Time-series data for visualization
   - **Use case**: Dashboard queries, metric aggregations

3. **Label Discovery** (`/loki/api/v1/labels`)
   - **Purpose**: List all indexed labels
   - **Returns**: Array of label names
   - **Use case**: Discover available stream selector labels

4. **Label Values** (`/loki/api/v1/label/<name>/values`)
   - **Purpose**: Get all values for specific label
   - **Returns**: Array of label values
   - **Use case**: Populate dashboard variable dropdowns

**How to Apply**:

1. **Start with label discovery** to understand available filters:
   ```bash
   curl -G http://localhost:3100/loki/api/v1/labels
   ```

2. **Check label values** before writing stream selectors:
   ```bash
   curl -G http://localhost:3100/loki/api/v1/label/service_name/values
   ```

3. **Validate query syntax** with instant query:
   ```bash
   curl -G http://localhost:3100/loki/api/v1/query \
     --data-urlencode 'query={service_name="orchestrator"}'
   ```

4. **Test metric queries** with range query:
   ```bash
   curl -G http://localhost:3100/loki/api/v1/query_range \
     --data-urlencode 'query=rate({service_name="api"}[5m])' \
     --data-urlencode 'start=2025-11-10T00:00:00Z' \
     --data-urlencode 'end=2025-11-10T01:00:00Z' \
     --data-urlencode 'step=60s'
   ```

**Example from Codebase**:

```python
# Example API client usage
import requests

LOKI_URL = "http://localhost:3100"

def validate_query(query: str) -> dict:
    """Validate LogQL query syntax."""
    response = requests.get(
        f"{LOKI_URL}/loki/api/v1/query",
        params={"query": query}
    )
    return response.json()
```

**Source**: https://grafana.com/docs/loki/latest/reference/loki-http-api/

---

### Framework 2: Query Parameters

**Purpose**: Configure query execution behavior (time ranges, limits, directions).

**When to Use**:
- Every API request to /query or /query_range
- To control result size and format
- To optimize query performance

**Components**:

1. **Common Parameters** (all endpoints):
   - `query` (required): LogQL query string (URL-encoded)
   - `limit`: Maximum entries returned (default: 100, max: 5000)
   - `time`: Timestamp for instant queries (default: now)

2. **Range Query Parameters**:
   - `start` (required): Start time (RFC3339 or Unix timestamp)
   - `end` (required): End time (RFC3339 or Unix timestamp)
   - `step`: Query resolution (e.g., "60s", "5m", "1h")
   - `direction`: "forward" or "backward" (default: backward)

3. **Label Query Parameters**:
   - `start`: Filter labels by time range start
   - `end`: Filter labels by time range end

**How to Apply**:

1. **Always URL-encode query parameter**:
   ```bash
   # ❌ Incorrect (spaces and special chars not encoded)
   curl "http://localhost:3100/loki/api/v1/query?query={service_name="api"}"

   # ✅ Correct (using --data-urlencode)
   curl -G http://localhost:3100/loki/api/v1/query \
     --data-urlencode 'query={service_name="api"}'
   ```

2. **Use appropriate time formats**:
   ```bash
   # RFC3339 format (recommended)
   --data-urlencode 'start=2025-11-10T00:00:00Z'

   # Unix timestamp (nanoseconds)
   --data-urlencode 'start=1699574400000000000'
   ```

3. **Set step based on time range** (for range queries):
   ```bash
   # 1-hour range: use 60s step (60 data points)
   --data-urlencode 'step=60s'

   # 24-hour range: use 5m step (288 data points)
   --data-urlencode 'step=5m'

   # 7-day range: use 1h step (168 data points)
   --data-urlencode 'step=1h'
   ```

4. **Limit results to prevent timeout**:
   ```bash
   --data-urlencode 'limit=1000'  # Max 1000 entries
   ```

**Example from Codebase**:

```python
def query_range(query: str, start: str, end: str, step: str = "60s") -> dict:
    """Execute range query with parameters."""
    response = requests.get(
        f"{LOKI_URL}/loki/api/v1/query_range",
        params={
            "query": query,
            "start": start,
            "end": end,
            "step": step,
            "limit": 5000
        }
    )
    return response.json()
```

**Source**: https://grafana.com/docs/loki/latest/reference/loki-http-api/#query-loki

---

### Framework 3: Response Format & Error Handling

**Purpose**: Parse API responses correctly and handle errors gracefully.

**When to Use**:
- After every API request
- To detect query syntax errors
- To diagnose query performance issues
- To handle authentication failures

**Components**:

1. **Success Response** (HTTP 200):
   ```json
   {
     "status": "success",
     "data": {
       "resultType": "streams" | "matrix" | "vector",
       "result": [...]
     }
   }
   ```

2. **Error Response** (HTTP 400):
   ```json
   {
     "status": "error",
     "errorType": "bad_data",
     "error": "parse error at line 1, col 5: syntax error: unexpected }"
   }
   ```

3. **Authentication Error** (HTTP 401):
   ```json
   {
     "status": "error",
     "error": "unauthorized"
   }
   ```

4. **Timeout Error** (HTTP 503):
   ```json
   {
     "status": "error",
     "errorType": "timeout",
     "error": "query timeout exceeded"
   }
   ```

**How to Apply**:

1. **Check HTTP status code first**:
   ```python
   response = requests.get(url, params=params)
   if response.status_code != 200:
       handle_error(response)
   ```

2. **Parse status field in JSON**:
   ```python
   data = response.json()
   if data["status"] != "success":
       raise QueryError(data["error"])
   ```

3. **Handle specific error types**:
   ```python
   if response.status_code == 400:
       # Syntax error - fix query
       print(f"Query syntax error: {data['error']}")
   elif response.status_code == 503:
       # Timeout - reduce time range or add filters
       print("Query timeout - try reducing time range")
   elif response.status_code == 401:
       # Auth error - check credentials
       print("Authentication failed")
   ```

4. **Extract result data based on resultType**:
   ```python
   result_type = data["data"]["resultType"]
   if result_type == "streams":
       # Log query results (instant query)
       for stream in data["data"]["result"]:
           print(stream["stream"], stream["values"])
   elif result_type == "matrix":
       # Metric query results (range query)
       for series in data["data"]["result"]:
           print(series["metric"], series["values"])
   ```

**Example from Codebase**:

```python
def handle_query_response(response: requests.Response) -> dict:
    """Parse and validate Loki API response."""
    if response.status_code == 400:
        data = response.json()
        raise ValueError(f"Query syntax error: {data['error']}")
    elif response.status_code == 401:
        raise PermissionError("Loki authentication failed")
    elif response.status_code == 503:
        raise TimeoutError("Query exceeded timeout limit")
    elif response.status_code != 200:
        raise RuntimeError(f"Loki API error: {response.status_code}")

    data = response.json()
    if data["status"] != "success":
        raise RuntimeError(f"Query failed: {data.get('error', 'unknown error')}")

    return data["data"]
```

**Source**: https://grafana.com/docs/loki/latest/reference/loki-http-api/#responses

---

## Processes & Workflows

### Workflow 1: 5-Step Query Validation

**Trigger Conditions**:
- Before adding query to Grafana dashboard
- After modifying existing query syntax
- When debugging query performance
- When query returns unexpected results

**Steps**:

1. **Label Discovery**
   - **Input**: None
   - **Output**: List of available indexed labels
   - **Rationale**: Verify labels exist before using in stream selectors
   - **Command**:
     ```bash
     curl -G http://localhost:3100/loki/api/v1/labels
     ```

2. **Label Value Verification**
   - **Input**: Label name from step 1
   - **Output**: Array of values for that label
   - **Rationale**: Confirm label values exist (avoid empty results)
   - **Command**:
     ```bash
     curl -G http://localhost:3100/loki/api/v1/label/service_name/values
     ```

3. **Syntax Validation** (Instant Query)
   - **Input**: LogQL query string
   - **Output**: Success/error response
   - **Rationale**: Check query syntax without executing over time range
   - **Command**:
     ```bash
     curl -G http://localhost:3100/loki/api/v1/query \
       --data-urlencode 'query={service_name="api"} | json | status >= 500'
     ```

4. **Result Verification** (Range Query)
   - **Input**: Validated query + time range
   - **Output**: Time-series data
   - **Rationale**: Ensure query returns expected data format and volume
   - **Command**:
     ```bash
     curl -G http://localhost:3100/loki/api/v1/query_range \
       --data-urlencode 'query=rate({service_name="api"}[5m])' \
       --data-urlencode 'start=2025-11-10T00:00:00Z' \
       --data-urlencode 'end=2025-11-10T01:00:00Z' \
       --data-urlencode 'step=60s'
     ```

5. **Performance Validation**
   - **Input**: Query execution time from response headers
   - **Output**: Performance metrics
   - **Rationale**: Ensure query completes within timeout limits (<5min)
   - **Check**:
     ```bash
     curl -G -w "Time: %{time_total}s\n" http://localhost:3100/loki/api/v1/query_range \
       --data-urlencode 'query=...'
     ```

**Success Criteria**:
- ✅ All labels exist in label discovery response
- ✅ Label values match expected service/pod names
- ✅ Syntax validation returns HTTP 200 with status="success"
- ✅ Range query returns data in expected format (matrix/streams)
- ✅ Query execution time < 30s (dashboard target) or < 300s (max)

**Failure Handling**:
- If step 1 fails (connection error): Verify Loki is running and accessible
- If step 2 fails (label not found): Check label name spelling or OTLP mapping
- If step 3 fails (400 error): Parse error message, fix syntax, retry
- If step 4 fails (empty results): Verify time range is within retention (7 days)
- If step 5 fails (timeout): Reduce time range, add more selective filters, or aggregate

**Example Execution**:

```bash
# Step 1: Discover labels
$ curl -s http://localhost:3100/loki/api/v1/labels | jq '.data'
["service_name", "service_namespace", "deployment_environment", ...]

# Step 2: Check service_name values
$ curl -s http://localhost:3100/loki/api/v1/label/service_name/values | jq '.data'
["orchestrator", "debugger", "api", "test-executor"]

# Step 3: Validate syntax
$ curl -s -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query={service_name="api"} |= "error"' | jq '.status'
"success"

# Step 4: Test range query
$ curl -s -G http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query=count_over_time({service_name="api"} |= "error" [5m])' \
  --data-urlencode 'start=2025-11-10T00:00:00Z' \
  --data-urlencode 'end=2025-11-10T01:00:00Z' \
  --data-urlencode 'step=60s' | jq '.data.resultType'
"matrix"

# Step 5: Check performance
$ curl -s -G -w "Time: %{time_total}s\n" http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query=count_over_time({service_name="api"} [5m])' \
  --data-urlencode 'start=2025-11-10T00:00:00Z' \
  --data-urlencode 'end=2025-11-10T01:00:00Z' \
  --data-urlencode 'step=60s' -o /dev/null
Time: 0.342s  ✅ Under 30s target
```

---

### Workflow 2: Dashboard Query Migration

**Trigger Conditions**:
- Copying query from Grafana Explore to dashboard panel
- Migrating query from another dashboard
- Converting manual API query to Grafana format

**Steps**:

1. **Extract Query from Grafana**
   - **Input**: Grafana Explore URL or dashboard JSON
   - **Output**: Raw LogQL query string
   - **Rationale**: Get baseline query to validate

2. **Test with API** (validation workflow from above)
   - **Input**: Extracted query
   - **Output**: Validated query with results
   - **Rationale**: Ensure query works outside Grafana

3. **Adapt for Dashboard Variables**
   - **Input**: Validated query + dashboard variables
   - **Output**: Query with `$variable` placeholders
   - **Rationale**: Enable dynamic filtering via dropdowns
   - **Example**:
     ```logql
     # Before: {service_name="api"}
     # After: {service_name="$service"}
     ```

4. **Replace Absolute Time with `$__auto`**
   - **Input**: Query with fixed time range (e.g., `[5m]`)
   - **Output**: Query with auto-adjusting interval
   - **Rationale**: Prevent timeout on large dashboard time ranges
   - **Example**:
     ```logql
     # Before: rate({service="api"}[5m])
     # After: rate({service="api"}[$__auto])
     ```

5. **Test in Dashboard Panel**
   - **Input**: Adapted query in Grafana panel
   - **Output**: Visualization with data
   - **Rationale**: Verify query works with dashboard context

**Success Criteria**:
- ✅ Query executes successfully in API test
- ✅ Dashboard variables populate correctly
- ✅ `$__auto` adjusts based on time range
- ✅ Panel renders data without errors
- ✅ Query completes within timeout across all time ranges

**Failure Handling**:
- If variables don't work: Check variable definition matches label name
- If `$__auto` causes errors: Fall back to fixed interval (e.g., `[5m]`)
- If panel shows "no data": Verify time range is within retention period
- If query times out: Add more selective filters or reduce aggregation complexity

**Example Execution**:

```bash
# Original Grafana Explore query
{service_name="api"} | json | status >= 500

# Step 1: Validate with API
curl -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query={service_name="api"} | json | status >= 500'
# ✅ Returns success

# Step 2: Adapt for dashboard variable ($service)
{service_name="$service"} | json | status >= 500

# Step 3: Add to dashboard panel JSON
{
  "expr": "{service_name=\"$service\"} | json | status >= 500",
  "refId": "A"
}

# Step 4: Test in Grafana UI
# - Select service from dropdown
# - Verify panel shows filtered data
```

---

## Decision Trees

### Decision 1: Choosing Query Endpoint

```
IF testing query syntax only
  THEN use /loki/api/v1/query (instant query)
  BECAUSE faster, returns current state only

ELSE IF need time-series data for visualization
  THEN use /loki/api/v1/query_range
  BECAUSE returns data points over time

ELSE IF discovering available labels
  THEN use /loki/api/v1/labels
  BECAUSE lists all indexed labels

ELSE IF populating dropdown options
  THEN use /loki/api/v1/label/<name>/values
  BECAUSE returns all values for specific label
```

**Example Scenarios**:

1. **Scenario**: Check if query syntax is valid → **Decision**: `/query` (instant)
2. **Scenario**: Get error count over last hour → **Decision**: `/query_range`
3. **Scenario**: List all service names → **Decision**: `/label/service_name/values`

---

### Decision 2: Handling Query Errors

```
IF HTTP 400 error
  THEN parse error message → fix syntax → retry
  BECAUSE syntax error in query

ELSE IF HTTP 401 error
  THEN check authentication credentials
  BECAUSE Loki requires valid auth token

ELSE IF HTTP 503 error with "timeout"
  THEN reduce time range OR add more filters OR increase step interval
  BECAUSE query exceeded 5-minute limit

ELSE IF HTTP 200 but empty results
  THEN verify time range within retention (7 days)
  BECAUSE data may be outside retention window

ELSE IF HTTP 200 but "max series limit exceeded"
  THEN add more selective stream selectors OR aggregate higher
  BECAUSE query returned >1000 unique series
```

**Example Scenarios**:

1. **Scenario**: Error "parse error at line 1, col 5" → **Decision**: Fix query syntax at position 5
2. **Scenario**: Error "query timeout exceeded" → **Decision**: Reduce time range from 7d to 1d
3. **Scenario**: Empty results on 10-day query → **Decision**: Limit to 7-day retention period

---

## Anti-Patterns

### Anti-Pattern 1: Not URL-Encoding Query Parameter

**Problem**: Special characters in query string cause API parsing errors or incorrect queries.

**Detection**:
- 🔴 400 error "parse error" when query looks correct
- 🔴 Query with spaces or special chars passed directly in URL

**Consequences**:
- ❌ Query fails with cryptic error messages
- ❌ Unexpected results due to character interpretation

**Better Approach**:

```bash
# ❌ Anti-Pattern (not encoded)
curl "http://localhost:3100/loki/api/v1/query?query={service_name="api"} |= "error""

# ✅ Preferred Pattern (URL-encoded)
curl -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query={service_name="api"} |= "error"'
```

**Migration Strategy**:
1. Always use `-G --data-urlencode` with curl
2. In Python, use `requests` library (auto-encodes params dict)
3. In JavaScript, use `encodeURIComponent()` before building URL

---

### Anti-Pattern 2: Using Instant Query for Time-Series Data

**Problem**: Instant query returns single point in time, not suitable for dashboard visualizations requiring trends.

**Detection**:
- 🔴 Dashboard panel shows single data point instead of line graph
- 🔴 Using `/query` endpoint when `/query_range` is needed

**Consequences**:
- ❌ No trend visualization (can't see changes over time)
- ❌ Dashboard panels appear empty or show only latest value

**Better Approach**:

```bash
# ❌ Anti-Pattern (instant query for dashboard)
curl -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query=rate({service="api"}[5m])'

# ✅ Preferred Pattern (range query with time window)
curl -G http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query=rate({service="api"}[5m])' \
  --data-urlencode 'start=2025-11-10T00:00:00Z' \
  --data-urlencode 'end=2025-11-10T01:00:00Z' \
  --data-urlencode 'step=60s'
```

**Migration Strategy**:
1. Use `/query` only for ad-hoc testing and syntax validation
2. Use `/query_range` for all dashboard panels and metric queries
3. Set `step` parameter based on time range (see loki-architecture-constraints.md)

---

### Anti-Pattern 3: Not Handling Timeout Errors

**Problem**: Query exceeds 5-minute timeout but code doesn't handle 503 error gracefully.

**Detection**:
- 🔴 Application crashes on query timeout
- 🔴 No retry or mitigation logic for slow queries

**Consequences**:
- ❌ Poor user experience (unhandled errors)
- ❌ No actionable feedback to fix query

**Better Approach**:

```python
# ❌ Anti-Pattern (no timeout handling)
def query_loki(query: str) -> dict:
    response = requests.get(f"{LOKI_URL}/loki/api/v1/query", params={"query": query})
    return response.json()["data"]  # Crashes on timeout

# ✅ Preferred Pattern (handle timeout)
def query_loki(query: str, retry_with_smaller_range: bool = True) -> dict:
    response = requests.get(f"{LOKI_URL}/loki/api/v1/query", params={"query": query})

    if response.status_code == 503:
        data = response.json()
        if "timeout" in data.get("error", "").lower():
            if retry_with_smaller_range:
                # Suggest smaller time range
                raise TimeoutError(
                    "Query timeout. Try reducing time range or adding more filters."
                )
            raise TimeoutError(f"Query timeout: {data['error']}")

    response.raise_for_status()
    return response.json()["data"]
```

**Migration Strategy**:
1. Always check for 503 status code after query execution
2. Provide actionable error messages (suggest smaller time range)
3. Implement automatic retry with reduced time range for idempotent queries
4. Log slow queries for later optimization

---

## Tools & Resources

### Recommended Tools

1. **curl**
   - **Purpose**: Command-line API testing
   - **When to Use**: Quick query validation, CI/CD pipelines
   - **Documentation**: https://curl.se/docs/

2. **jq**
   - **Purpose**: JSON response parsing and formatting
   - **When to Use**: Extracting specific fields from API responses
   - **Documentation**: https://jqlang.github.io/jq/

3. **Grafana Explore**
   - **Purpose**: Interactive query builder with syntax highlighting
   - **When to Use**: Developing queries before API integration
   - **Documentation**: https://grafana.com/docs/grafana/latest/explore/

4. **Postman / Insomnia**
   - **Purpose**: GUI-based API testing with request history
   - **When to Use**: Complex query parameter testing, authentication debugging
   - **Documentation**: https://www.postman.com/docs/

### Learning Resources

1. **Loki HTTP API Reference**: https://grafana.com/docs/loki/latest/reference/loki-http-api/
   - **Topic**: Complete API endpoint documentation
   - **Quality**: High

2. **LogQL Query Examples**: https://grafana.com/docs/loki/latest/query/
   - **Topic**: Example queries with explanations
   - **Quality**: High

3. **Grafana Dashboards with Loki**: https://grafana.com/docs/grafana/latest/datasources/loki/
   - **Topic**: Integrating Loki queries in Grafana
   - **Quality**: High

---

## Glossary

- **Instant Query**: Query executed at single point in time (endpoint: `/query`)
- **Range Query**: Query executed over time range returning time-series data (endpoint: `/query_range`)
- **Label Discovery**: Listing all indexed labels available for filtering (endpoint: `/labels`)
- **Label Values**: Getting all values for specific label (endpoint: `/label/<name>/values`)
- **Step**: Query resolution interval (e.g., "60s" = 1 data point per minute)
- **RFC3339**: Timestamp format (e.g., "2025-11-10T00:00:00Z")
- **URL Encoding**: Converting special characters to %XX format for URLs
- **resultType**: Response data format ("streams" for logs, "matrix" for metrics)

---

## Sources & References

1. Grafana Loki HTTP API Documentation: https://grafana.com/docs/loki/latest/reference/loki-http-api/
   - Accessed: 2025-11-10
   - Confidence: 0.90

2. Grafana Loki Query API: https://grafana.com/docs/loki/latest/reference/loki-http-api/#query-loki
   - Accessed: 2025-11-10
   - Confidence: 0.90

3. LogQL Query Language: https://grafana.com/docs/loki/latest/query/
   - Accessed: 2025-11-10
   - Confidence: 0.90

---

## Changelog

- **2025-11-10**: Initial documentation created from researcher-external findings (confidence: 0.90)

---

## Related Documentation

- `logql-syntax-reference.md`: LogQL syntax and operators
- `loki-architecture-constraints.md`: Query limits and configuration
- `query-optimization-patterns.md`: Query performance best practices
