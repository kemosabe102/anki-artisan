# Prometheus API & PromQL Optimization Patterns

**Purpose**: Actionable patterns for Prometheus HTTP API interaction and PromQL query optimization for metric discovery and signal detection

**Referenced by**: grafana-dashboard-builder

**Version Compatibility**: See README.md for Grafana 12.x, Prometheus 3.x, and Jaeger 2.x compatibility details.

## Overview

This guide provides production-ready patterns for interacting with the Prometheus HTTP API v1 and constructing optimized PromQL queries. Focus areas: metric discovery workflows, query validation strategies, error handling with retry logic, and PromQL optimization for signal detection and noise reduction.

**Key Capabilities**:

- Metric discovery via Prometheus API endpoints

- PromQL query construction for counters, gauges, histograms

- Request/response validation with error categorization

- Retry strategies with exponential backoff

- Cardinality management and aggregation optimization

**Sources**:

- Prometheus HTTP API v1 Documentation: https://prometheus.io/docs/prometheus/latest/querying/api/

- PromQL Query Language: https://prometheus.io/docs/prometheus/latest/querying/basics/

- Best Practices: https://prometheus.io/docs/practices/naming/

- SRE Monitoring Patterns: Google SRE Workbook

---

## Core Frameworks

### Framework 1: Metric Discovery via Prometheus API

**Purpose**: Query Prometheus to discover available metrics matching user intent

**When to Use**:

- User describes monitoring goal without specifying exact metric names

- Validating metric availability before dashboard generation

- Exploring available metrics in a new Prometheus instance

**How to Apply**:

1. Query all metric names: `GET /api/v1/label/__name__/values`

2. Filter by pattern using grep or regex (client-side filtering)

3. Validate metric availability: `GET /api/v1/query?query={metric_name}`

4. Discover label names for a metric: `GET /api/v1/label/<name>/values`

5. Check metric type from metadata endpoint (counter/gauge/histogram)

**Example**:

```bash

# Discover all metrics containing "duration"

curl -s http://localhost:9090/api/v1/label/__name__/values | jq -r '.data[]' | grep duration



# Example response (partial):

# http_server_duration_seconds

# http_client_duration_seconds

# grpc_server_handling_seconds



# Validate metric exists and has data

curl -s "http://localhost:9090/api/v1/query?query=http_server_duration_seconds" | jq '.status'

# Returns: "success" if metric exists



# Discover labels for a metric

curl -s http://localhost:9090/api/v1/label/http_server_duration_seconds/values | jq '.data'

# Returns: ["method", "status", "route", "le"]

```

**Decision Tree**:

- User intent contains "latency" OR "duration" → Search for `*duration*` OR `*latency*` metrics

- User intent contains "error" OR "failure" → Search for `*error*` OR `*failed*` OR metrics with status label

- User intent contains "throughput" OR "rate" → Search for `*count*` OR `*total*` counter metrics

- User intent contains "utilization" → Search for `*usage*` OR `*utilization*` gauge metrics

---

### Framework 2: PromQL Query Construction by Metric Type

**Purpose**: Build appropriate PromQL queries based on metric type (counter, gauge, histogram)

**When to Use**: Constructing queries for dashboard panels, ensuring signal detection with noise reduction

**How to Apply**:

**Counter Metrics** (monotonically increasing):

- Use `rate()` for per-second rate of change

- Use `increase()` for absolute increase over time range

- Apply aggregation AFTER rate() for accuracy

- Choose interval based on scrape frequency (typically 2-5x scrape interval)

**Gauge Metrics** (point-in-time values):

- Use raw value for current state

- Use `delta()` for change over time

- Apply aggregation functions directly (avg, sum, max, min)

- No rate() needed (not monotonic)

**Histogram Metrics** (distribution data):

- Use `histogram_quantile()` for percentile calculations

- Apply `rate()` to `_bucket` suffix before quantile

- Aggregate by `le` label (histogram bucket boundaries)

- Common percentiles: 0.50 (p50), 0.95 (p95), 0.99 (p99)

**Example - Counter (Request Count)**:

```promql

# Bad: No rate() - shows cumulative total (not useful for trends)

http_server_request_count{service="user-service"}



# Good: Rate per second (5m window for smoothing)

rate(http_server_request_count{service="user-service"}[5m])



# Best: Aggregated rate by status code

sum by (status) (rate(http_server_request_count{service="user-service"}[5m]))

```

**Example - Gauge (CPU Usage)**:

```promql

# Current CPU usage (no rate needed)

cpu_usage_percent{instance="web-01"}



# Average CPU across instances

avg(cpu_usage_percent{service="web"})



# Change in CPU over last hour

delta(cpu_usage_percent{instance="web-01"}[1h])

```

**Example - Histogram (Request Duration)**:

```promql

# P95 latency (5m rate window)

histogram_quantile(0.95,

  sum by (le) (rate(http_server_duration_seconds_bucket{service="user-service"}[5m]))

)



# P50, P95, P99 comparison

histogram_quantile(0.50, sum by (le) (rate(http_server_duration_seconds_bucket[5m]))) # P50

histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m]))) # P95

histogram_quantile(0.99, sum by (le) (rate(http_server_duration_seconds_bucket[5m]))) # P99

```

**Decision Tree**:

- Metric ends with `_total` OR `_count` → Counter → Use `rate()` or `increase()`

- Metric has `_bucket` suffix → Histogram → Use `histogram_quantile()` with `rate()`

- Metric represents current state (no suffix) → Gauge → Use raw value or `delta()`

---

### Framework 3: Signal Detection & Noise Reduction

**Purpose**: Optimize PromQL queries to highlight meaningful signals and reduce noise

**When to Use**: Configuring dashboard panels, setting alert thresholds, analyzing time-series trends

**How to Apply**:

**1. Rate Interval Selection** (5m rule):

- Use 5m interval for most rate() queries (balances responsiveness vs noise)

- Increase to 15m for smoother trends (reduces spikes)

- Decrease to 1m for real-time monitoring (more noise but faster detection)

- Never use interval < scrape frequency (causes gaps)

**2. Aggregation Order** (rate before sum):

- Apply `rate()` BEFORE aggregation for accuracy

- Bad: `rate(sum(...)[5m])` - aggregates then rates (incorrect)

- Good: `sum(rate(...[5m]))` - rates then aggregates (correct)

**3. Percentiles Over Averages**:

- Use p95/p99 for latency (captures tail latency)

- Avoid avg() for latency (hides outliers)

- Use avg() for throughput/CPU (meaningful for capacity)

**4. Cardinality Management**:

- Limit high-cardinality labels (customer_id, request_id)

- Aggregate by low-cardinality labels (service, environment, status)

- Use `topk()` or `bottomk()` to limit series (e.g., top 10 endpoints)

**Example - High Signal-to-Noise Query**:

```promql

# Bad: Noisy, high cardinality, no smoothing

http_server_duration_seconds{route!=""}



# Better: Rate for smoothing, aggregated by route

sum by (route) (rate(http_server_duration_seconds_count{route!=""}[5m]))



# Best: P95 latency, top 10 routes only, 15m smoothing

topk(10,

  histogram_quantile(0.95,

    sum by (route, le) (rate(http_server_duration_seconds_bucket{route!=""}[15m]))

  )

)

```

**Decision Tree**:

- Metric shows extreme spikes → Increase rate() interval (5m → 15m)

- Too many time series (>100) → Add aggregation by low-cardinality label OR use topk()

- Need fast detection → Decrease interval (5m → 1m) but expect more noise

- Latency monitoring → Use histogram_quantile() for p95/p99, not avg()

---

### Framework 4: Time-Based Comparisons

**Purpose**: Compare current metrics to historical baselines (hour-over-hour, day-over-day, week-over-week)

**When to Use**: Identifying anomalies, detecting trends, comparing traffic patterns

**How to Apply**:

**1. Offset Operator**:

- `offset 1h` - Compare to 1 hour ago

- `offset 1d` - Compare to 1 day ago (same time yesterday)

- `offset 1w` - Compare to 1 week ago (same day last week)

**2. Vector Arithmetic**:

- Subtract: `metric - metric offset 1h` (absolute difference)

- Ratio: `metric / metric offset 1h` (percentage change)

- Use `or vector(0)` to handle missing historical data

**3. Multiple Baselines**:

- Compare to multiple periods: current vs 1h ago vs 1d ago vs 1w ago

- Use separate panel queries for each baseline

- Color-code baselines for readability (current=blue, 1h=yellow, 1d=orange, 1w=red)

**Example - Hour-over-Hour Comparison**:

```promql

# Current request rate

sum(rate(http_server_request_count{service="api"}[5m]))



# Request rate 1 hour ago

sum(rate(http_server_request_count{service="api"}[5m] offset 1h))



# Percentage change (current vs 1h ago)

(

  sum(rate(http_server_request_count{service="api"}[5m]))

  /

  sum(rate(http_server_request_count{service="api"}[5m] offset 1h))

) * 100 - 100

```

**Example - Week-over-Week Latency Comparison**:

```promql

# Current week p95 latency

histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m])))



# Same time last week

histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m] offset 1w)))

```

**Decision Tree**:

- Detecting recent changes → Use `offset 1h` (hour-over-hour)

- Daily traffic patterns → Use `offset 1d` (day-over-day)

- Weekly seasonality → Use `offset 1w` (week-over-week)

- Need % change → Use `(current / historical) * 100 - 100`

---

### Framework 5: Error Handling & Retry Strategy

**Purpose**: Robust Prometheus API interaction with graceful degradation

**When to Use**: All Prometheus API calls (metric discovery, query validation, dashboard generation)

**How to Apply**:

**HTTP Status Code Handling**:

- `200 OK` - Success, parse response data

- `400 Bad Request` - Invalid PromQL query syntax (return error to user, suggest correction)

- `422 Unprocessable Entity` - Query timeout or resource limits (simplify query, reduce time range)

- `503 Service Unavailable` - Prometheus overloaded or down (retry with exponential backoff)

**Retry Strategy** (Exponential Backoff):

- Initial retry delay: 1 second

- Max retries: 3

- Backoff multiplier: 2x (1s → 2s → 4s)

- Only retry on 503 or network errors (NOT 400/422)

**Validation Strategy**:

- **Client-side**: Check PromQL syntax before API call (basic regex validation)

- **Server-side**: Test query via `/api/v1/query` instant query endpoint

- **Fallback**: If query fails, simplify (remove aggregations, reduce time range)

**Example - Retry with Exponential Backoff (Python)**:

```python

import time

import requests



def query_prometheus(url, query, max_retries=3):

    """Query Prometheus with exponential backoff retry."""

    for attempt in range(max_retries):

        try:

            response = requests.get(

                f"{url}/api/v1/query",

                params={"query": query},

                timeout=10

            )



            if response.status_code == 200:

                return response.json()

            elif response.status_code == 400:

                # Bad request - don't retry (syntax error)

                raise ValueError(f"Invalid PromQL query: {response.json()['error']}")

            elif response.status_code == 422:

                # Timeout - don't retry (query too complex)

                raise ValueError(f"Query timeout: simplify query or reduce time range")

            elif response.status_code == 503:

                # Service unavailable - retry with backoff

                if attempt < max_retries - 1:

                    delay = 2 ** attempt  # 1s, 2s, 4s

                    time.sleep(delay)

                    continue

                else:

                    raise RuntimeError("Prometheus unavailable after 3 retries")

        except requests.exceptions.RequestException as e:

            # Network error - retry

            if attempt < max_retries - 1:

                time.sleep(2 ** attempt)

                continue

            else:

                raise RuntimeError(f"Network error: {e}")



    raise RuntimeError("Max retries exceeded")



# Usage

result = query_prometheus(

    "http://localhost:9090",

    "rate(http_server_request_count[5m])"

)

```

**Example - Bash Implementation**:

```bash

#!/bin/bash

# Query Prometheus with retry logic



query_prometheus() {

    local url="$1"

    local query="$2"

    local max_retries=3

    local attempt=0



    while [ $attempt -lt $max_retries ]; do

        response=$(curl -s -w "\n%{http_code}" "$url/api/v1/query?query=$query")

        http_code=$(echo "$response" | tail -n 1)

        body=$(echo "$response" | head -n -1)



        case $http_code in

            200)

                echo "$body"

                return 0

                ;;

            400|422)

                echo "Error: Invalid query (HTTP $http_code)" >&2

                echo "$body" | jq '.error' >&2

                return 1

                ;;

            503)

                if [ $attempt -lt $((max_retries - 1)) ]; then

                    delay=$((2 ** attempt))

                    echo "Prometheus unavailable, retrying in ${delay}s..." >&2

                    sleep $delay

                    attempt=$((attempt + 1))

                else

                    echo "Error: Prometheus unavailable after 3 retries" >&2

                    return 1

                fi

                ;;

            *)

                echo "Error: Unexpected HTTP $http_code" >&2

                return 1

                ;;

        esac

    done

}



# Usage

query_prometheus "http://localhost:9090" "rate(http_server_request_count[5m])"

```

**Decision Tree**:

- HTTP 200 → Parse response, extract data

- HTTP 400 → Parse error message, suggest query correction, FAIL (don't retry)

- HTTP 422 → Timeout, simplify query (remove aggregations OR reduce time range), FAIL (don't retry)

- HTTP 503 → Retry with exponential backoff (max 3 attempts)

- Network error → Retry with exponential backoff (max 3 attempts)

---

## Processes & Workflows

### Workflow 1: Metric Discovery for User Intent

**Goal**: Translate user's monitoring goal (e.g., "monitor API latency") to concrete Prometheus metrics

**Steps**:

1. **Parse Intent**: Extract monitoring signals from user description
   - Keywords: latency → duration, error → status/error, throughput → count/total

2. **Generate Search Pattern**: Create metric name pattern
   - "API latency" → `*http*duration*` OR `*api*latency*`

3. **Query Prometheus API**: Fetch all metric names

   ```bash

   curl -s http://localhost:9090/api/v1/label/__name__/values | jq -r '.data[]'

   ```

4. **Filter Matches**: Client-side filtering by pattern

   ```bash

   jq -r '.data[]' | grep -E '(http|api).*(duration|latency)'

   ```

5. **Validate Availability**: Check each metric has data

   ```bash

   curl -s "http://localhost:9090/api/v1/query?query=http_server_duration_seconds"

   ```

6. **Discover Labels**: Get label names for context

   ```bash

   curl -s http://localhost:9090/api/v1/label/http_server_duration_seconds/values

   ```

7. **Rank by Relevance**: Score metrics by:
   - Metric name similarity to intent (Levenshtein distance)

   - Label availability (more labels = more flexibility)

   - Data freshness (has recent data points)

8. **Return Top Matches**: Provide top 3-5 metrics with:
   - Metric name

   - Metric type (counter/gauge/histogram)

   - Available labels

   - Sample query

**Rationale**: Start broad (all metrics) → narrow progressively (pattern match) → validate (has data) → rank (best match). Prevents false negatives from overly narrow initial search.

**Example Output**:

```json
{
  "discovered_metrics": [
    {
      "name": "http_server_duration_seconds",

      "type": "histogram",

      "labels": ["method", "status", "route", "le"],

      "sample_query": "histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m])))",

      "relevance_score": 0.95
    },

    {
      "name": "http_request_latency_ms",

      "type": "gauge",

      "labels": ["endpoint", "status"],

      "sample_query": "avg(http_request_latency_ms)",

      "relevance_score": 0.87
    }
  ]
}
```

---

### Workflow 2: PromQL Query Validation

**Goal**: Ensure generated PromQL queries are syntactically valid and return data

**Steps**:

1. **Client-Side Syntax Check**: Basic validation before API call
   - Check matching parentheses: `()`, `[]`, `{}`

   - Verify function names exist: `rate`, `sum`, `histogram_quantile`

   - Validate time range format: `[5m]`, `[1h]`, `[7d]`

2. **Test Query via Instant Query API**:

   ```bash

   curl -s "http://localhost:9090/api/v1/query?query=YOUR_QUERY_HERE"

   ```

3. **Parse Response**:
   - `status: "success"` → Query valid

   - `status: "error"` → Parse error message, extract issue

4. **Check Data Availability**:

   ```json
   {
     "status": "success",

     "data": {
       "resultType": "vector",

       "result": [] // Empty = no data (warn user)
     }
   }
   ```

5. **Handle Errors**:
   - **Syntax error**: Parse error message, suggest fix
     - Example: `"parse error at char 45: unexpected )"` → Missing opening parenthesis

   - **Unknown function**: Suggest alternatives
     - Example: `"unknown function: rates"` → Did you mean `rate`?

   - **Timeout (422)**: Simplify query
     - Remove complex aggregations, reduce time range

6. **Return Validation Result**:

   ```json
   {
     "valid": true,

     "query": "rate(http_server_request_count[5m])",

     "has_data": true,

     "sample_result": {
       "metric": { "service": "api" },

       "value": [1698765432, "42.5"]
     }
   }
   ```

**Rationale**: Two-phase validation (client + server) catches obvious errors early (saves API calls) while ensuring final query executes correctly.

**Error Recovery**:

- Syntax error → Parse error location, suggest correction

- No data → Return query as valid but warn user (metric might be new)

- Timeout → Simplify query (remove `topk`, reduce aggregations)

---

### Workflow 3: Production Client Pattern

**Goal**: Reliable Prometheus API client with error handling, retries, and connection pooling

**Implementation** (Python):

```python

import requests

from typing import Dict, Any, Optional, List

from urllib.parse import urljoin

import time

import logging



logger = logging.getLogger(__name__)



class PrometheusClient:

    """Production-ready Prometheus API client with retries and error handling."""



    def __init__(

        self,

        base_url: str = "http://localhost:9090",

        timeout: int = 10,

        max_retries: int = 3

    ):

        self.base_url = base_url

        self.timeout = timeout

        self.max_retries = max_retries

        self.session = requests.Session()  # Connection pooling



    def _request(

        self,

        endpoint: str,

        params: Optional[Dict[str, str]] = None

    ) -> Dict[str, Any]:

        """Make request with retry logic."""

        url = urljoin(self.base_url, endpoint)



        for attempt in range(self.max_retries):

            try:

                response = self.session.get(

                    url,

                    params=params,

                    timeout=self.timeout

                )



                if response.status_code == 200:

                    return response.json()

                elif response.status_code in (400, 422):

                    # Client error - don't retry

                    error_data = response.json()

                    raise ValueError(f"API error: {error_data.get('error', 'Unknown error')}")

                elif response.status_code == 503:

                    # Service unavailable - retry

                    if attempt < self.max_retries - 1:

                        delay = 2 ** attempt

                        logger.warning(f"Prometheus unavailable, retrying in {delay}s...")

                        time.sleep(delay)

                        continue

                    else:

                        raise RuntimeError("Prometheus unavailable after retries")

                else:

                    raise RuntimeError(f"Unexpected status code: {response.status_code}")



            except requests.exceptions.RequestException as e:

                if attempt < self.max_retries - 1:

                    delay = 2 ** attempt

                    logger.warning(f"Request failed: {e}, retrying in {delay}s...")

                    time.sleep(delay)

                    continue

                else:

                    raise RuntimeError(f"Request failed after retries: {e}")



        raise RuntimeError("Max retries exceeded")



    def query(self, query: str, time: Optional[str] = None) -> Dict[str, Any]:

        """Execute instant query."""

        params = {"query": query}

        if time:

            params["time"] = time



        response = self._request("/api/v1/query", params)



        if response["status"] != "success":

            raise ValueError(f"Query failed: {response.get('error', 'Unknown error')}")



        return response["data"]



    def query_range(

        self,

        query: str,

        start: str,

        end: str,

        step: str

    ) -> Dict[str, Any]:

        """Execute range query."""

        params = {

            "query": query,

            "start": start,

            "end": end,

            "step": step

        }



        response = self._request("/api/v1/query_range", params)



        if response["status"] != "success":

            raise ValueError(f"Query failed: {response.get('error', 'Unknown error')}")



        return response["data"]



    def get_metric_names(self) -> List[str]:

        """Get all available metric names."""

        response = self._request("/api/v1/label/__name__/values")



        if response["status"] != "success":

            raise ValueError("Failed to fetch metric names")



        return response["data"]



    def get_label_values(self, label: str) -> List[str]:

        """Get all values for a label."""

        response = self._request(f"/api/v1/label/{label}/values")



        if response["status"] != "success":

            raise ValueError(f"Failed to fetch values for label: {label}")



        return response["data"]



    def health_check(self) -> bool:

        """Check if Prometheus is healthy."""

        try:

            response = self.session.get(

                urljoin(self.base_url, "/-/healthy"),

                timeout=5

            )

            return response.status_code == 200

        except requests.exceptions.RequestException:

            return False



# Usage example

client = PrometheusClient(base_url="http://localhost:9090")



# Health check

if not client.health_check():

    print("Prometheus is not healthy")



# Discover metrics

metrics = client.get_metric_names()

duration_metrics = [m for m in metrics if "duration" in m]



# Execute query

result = client.query("rate(http_server_request_count[5m])")

print(f"Result: {result}")



# Range query

range_result = client.query_range(

    query="rate(http_server_request_count[5m])",

    start="2024-01-01T00:00:00Z",

    end="2024-01-01T01:00:00Z",

    step="1m"

)

```

**Key Features**:

- Connection pooling via `requests.Session()`

- Exponential backoff retry (1s → 2s → 4s)

- Timeout protection (10s default)

- Error categorization (client vs server errors)

- Health check endpoint support

---

## Decision Trees

### Decision Tree 1: Query Type Selection

```

START: User monitoring goal

│

├─ Need CURRENT value (single point in time)?

│  └─ YES → Use instant query (/api/v1/query)

│         Example: "What is current error rate?"

│

└─ Need TIME SERIES (trend over time)?

   └─ YES → Use range query (/api/v1/query_range)

          Example: "Show error rate for last 24 hours"



Query constructed → Choose metric type:

│

├─ Metric ends with _total or _count?

│  └─ YES → COUNTER → Use rate() or increase()

│         Example: rate(http_requests_total[5m])

│

├─ Metric has _bucket suffix?

│  └─ YES → HISTOGRAM → Use histogram_quantile() with rate()

│         Example: histogram_quantile(0.95, sum by (le) (rate(metric_bucket[5m])))

│

└─ Metric is current state (no suffix)?

   └─ YES → GAUGE → Use raw value or delta()

          Example: memory_usage_bytes OR delta(memory_usage_bytes[1h])

```

### Decision Tree 2: Rate Interval Selection

```

START: Choose rate() interval

│

├─ Scrape interval known?

│  ├─ YES → Use 4x scrape interval (minimum)

│  │      Example: 15s scrape → 60s (1m) rate interval

│  │

│  └─ NO → Default to 5m (safe for most deployments)

│

├─ Real-time alerting needed?

│  └─ YES → Use 1-2m interval (more noise, faster detection)

│

├─ Trend analysis (reduce noise)?

│  └─ YES → Use 15m or 1h interval (smoother, slower detection)

│

└─ Production dashboard (balanced)?

   └─ YES → Use 5m interval (industry standard)

```

### Decision Tree 3: Error Recovery

```

START: Prometheus API call

│

├─ HTTP 200 OK?

│  └─ YES → Parse response, check data.result

│         ├─ result not empty → SUCCESS (use data)

│         └─ result empty → WARNING (metric exists but no data)

│

├─ HTTP 400 Bad Request?

│  └─ YES → Parse error message

│         ├─ "parse error" → Syntax error (suggest fix)

│         ├─ "unknown function" → Suggest alternatives

│         └─ Other → Return error to user (don't retry)

│

├─ HTTP 422 Unprocessable Entity?

│  └─ YES → Query timeout or resource limit

│         ├─ Simplify query (remove aggregations)

│         ├─ Reduce time range (24h → 6h)

│         └─ Return partial results if available

│

├─ HTTP 503 Service Unavailable?

│  └─ YES → Retry with exponential backoff

│         ├─ Attempt 1: Wait 1s

│         ├─ Attempt 2: Wait 2s

│         ├─ Attempt 3: Wait 4s

│         └─ Max retries exceeded → FAIL (Prometheus down)

│

└─ Network error (timeout, connection refused)?

   └─ YES → Retry with exponential backoff (same as 503)

```

---

## Anti-Patterns

### Anti-Pattern 1: Aggregating Before Rating

**Problem**: Applying `rate()` to already-aggregated data produces incorrect results

**Bad Example**:

```promql

# WRONG: Aggregates THEN rates (mathematically incorrect)

rate(sum(http_server_request_count)[5m])

```

**Why It Fails**: `rate()` expects raw counter values. Aggregating first loses per-instance reset information, causing incorrect rate calculations.

**Correct Alternative**:

```promql

# RIGHT: Rates THEN aggregates

sum(rate(http_server_request_count[5m]))

```

**Rule**: Always apply `rate()` or `increase()` BEFORE aggregation functions (`sum`, `avg`, etc.)

---

### Anti-Pattern 2: Using Average for Latency

**Problem**: `avg()` hides tail latency, making p95/p99 outliers invisible

**Bad Example**:

```promql

# WRONG: Average latency (hides slow requests)

avg(http_server_duration_seconds)

```

**Why It Fails**: Average is dominated by the majority of fast requests. Slow requests (p99) that impact user experience are invisible.

**Correct Alternative**:

```promql

# RIGHT: P95 latency (captures tail behavior)

histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m])))

```

**Rule**: For latency monitoring, use percentiles (p50, p95, p99) from histograms, not averages.

---

### Anti-Pattern 3: No Rate Window for Counters

**Problem**: Querying raw counter values shows cumulative total, not rate of change

**Bad Example**:

```promql

# WRONG: Raw counter (shows total requests since start)

http_server_request_count

```

**Why It Fails**: Counter resets on restart create misleading drops. Cumulative total is not useful for trend analysis.

**Correct Alternative**:

```promql

# RIGHT: Rate per second (meaningful trend)

rate(http_server_request_count[5m])

```

**Rule**: Always use `rate()` or `increase()` for counter metrics in dashboards and alerts.

---

### Anti-Pattern 4: High-Cardinality Label Aggregation

**Problem**: Aggregating by high-cardinality labels (user_id, request_id) creates excessive time series

**Bad Example**:

```promql

# WRONG: Aggregates by customer_id (thousands of series)

sum by (customer_id) (rate(http_server_request_count[5m]))

```

**Why It Fails**: Creates one time series per customer. With 10,000 customers, this generates 10,000 series, causing:

- High memory usage in Prometheus

- Slow query execution

- Overwhelming dashboard (too many lines to visualize)

**Correct Alternative**:

```promql

# RIGHT: Aggregate by low-cardinality label (service, status)

sum by (service, status) (rate(http_server_request_count[5m]))



# OR: Limit to top N using topk()

topk(10, sum by (customer_id) (rate(http_server_request_count[5m])))

```

**Rule**: Aggregate by low-cardinality labels (<100 unique values). Use `topk()` or `bottomk()` to limit series count.

---

### Anti-Pattern 5: Missing Offset for Time Comparisons

**Problem**: Attempting to compare metrics without using `offset` operator

**Bad Example**:

```promql

# WRONG: Cannot compare current to historical without offset

rate(http_server_request_count[5m])  # Where's the comparison?

```

**Why It Fails**: Without `offset`, there's no way to reference historical data for comparison.

**Correct Alternative**:

```promql

# RIGHT: Hour-over-hour comparison

rate(http_server_request_count[5m]) / rate(http_server_request_count[5m] offset 1h)

```

**Rule**: Use `offset` operator for time-based comparisons (offset 1h, offset 1d, offset 1w).

---

## Integration Points

### Integration 1: Grafana Dashboard Generation

**How Prometheus API Integrates with grafana-dashboard-builder**:

1. **Metric Discovery Phase**:
   - grafana-dashboard-builder receives user intent (e.g., "monitor API latency")

   - Calls Prometheus API: `/api/v1/label/__name__/values`

   - Filters metrics by pattern (e.g., `*duration*`)

   - Validates metric availability via instant query

2. **Panel Configuration Phase**:
   - For each metric, determine type (counter/gauge/histogram)

   - Apply Framework 2 (PromQL Query Construction by Metric Type)

   - Generate appropriate query (rate() for counters, histogram_quantile() for histograms)

   - Apply Framework 3 (Signal Detection & Noise Reduction)

3. **Query Validation Phase**:
   - Test each PromQL query via `/api/v1/query`

   - Apply Framework 5 (Error Handling & Retry Strategy)

   - Validate response status, check for data availability

   - Retry on failures (503), fail fast on client errors (400, 422)

4. **Dashboard JSON Generation**:
   - Embed validated queries into Grafana panel definitions

   - Configure time range, refresh interval

   - Set panel type based on metric characteristics

   - Generate ConfigMap with dashboard JSON

**Dependencies**:

- Prometheus must be accessible (http://localhost:9090)

- Metrics must be actively scraped (not just defined)

- PromQL queries must complete within timeout (10s default)

---

### Integration 2: SRE Framework Mapping

**How PromQL patterns map to SRE monitoring frameworks**:

**Four Golden Signals**:

- **Latency**: `histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m])))`

- **Traffic**: `sum(rate(http_server_request_count[5m]))`

- **Errors**: `sum(rate(http_server_request_count{status=~"5.."}[5m])) / sum(rate(http_server_request_count[5m]))`

- **Saturation**: `avg(cpu_usage_percent)` OR `avg(memory_usage_percent)`

**USE Method** (resources):

- **Utilization**: `avg(cpu_usage_percent)`

- **Saturation**: `avg(cpu_queue_length)` OR `rate(cpu_throttle_seconds_total[5m])`

- **Errors**: `rate(disk_errors_total[5m])`

**RED Method** (services):

- **Rate**: `sum(rate(http_server_request_count[5m]))`

- **Errors**: `sum(rate(http_server_request_count{status=~"5.."}[5m]))`

- **Duration**: `histogram_quantile(0.95, sum by (le) (rate(http_server_duration_seconds_bucket[5m])))`

**Implementation**:

- grafana-dashboard-builder receives SRE framework in input (e.g., `"sre_framework": "four_golden_signals"`)

- Maps framework to required signal types (latency, traffic, errors, saturation)

- Discovers appropriate metrics for each signal type

- Generates panel for each signal with framework-specific PromQL

---

### Integration 3: Metric Type Detection

**How to determine metric type from Prometheus API**:

**Option 1: Naming Convention** (fast, heuristic):

- Ends with `_total` OR `_count` → Counter

- Has `_bucket` suffix → Histogram (part of histogram metric)

- Has `_sum` suffix → Histogram (part of histogram metric)

- No suffix → Gauge (assumption)

**Option 2: Metadata Endpoint** (accurate, requires Prometheus 2.0+):

```bash

# Query metric metadata

curl -s "http://localhost:9090/api/v1/metadata?metric=http_server_request_count"



# Response:

{

  "status": "success",

  "data": {

    "http_server_request_count": [

      {

        "type": "counter",

        "help": "Total number of HTTP requests",

        "unit": ""

      }

    ]

  }

}

```

**Recommended Approach**: Use naming convention as primary (fast), fall back to metadata endpoint if ambiguous.

**Example Implementation**:

```python

def detect_metric_type(client: PrometheusClient, metric_name: str) -> str:

    """Detect metric type (counter, gauge, histogram)."""

    # Heuristic based on naming

    if metric_name.endswith(("_total", "_count")):

        return "counter"

    elif metric_name.endswith("_bucket"):

        return "histogram"

    elif metric_name.endswith(("_sum", "_count")):

        # Part of histogram or summary

        base_name = metric_name.rsplit("_", 1)

        return "histogram"



    # Fallback: Query metadata API

    try:

        metadata = client._request(f"/api/v1/metadata", params={"metric": metric_name})

        if metadata["status"] == "success" and metric_name in metadata["data"]:

            return metadata["data"][metric_name][0]["type"]

    except Exception:

        pass



    # Default to gauge if unknown

    return "gauge"

```

---

## Appendix: Complete Examples

### Example 1: Health Check Implementation

**Goal**: Validate Prometheus API connectivity before dashboard generation

```python

import requests



def check_prometheus_health(base_url: str = "http://localhost:9090") -> dict:

    """Check Prometheus health and return status."""

    result = {

        "healthy": False,

        "version": None,

        "metric_count": 0,

        "error": None

    }



    try:

        # Health check endpoint

        health_response = requests.get(f"{base_url}/-/healthy", timeout=5)

        result["healthy"] = health_response.status_code == 200



        if not result["healthy"]:

            result["error"] = f"Health check failed: HTTP {health_response.status_code}"

            return result



        # Get version

        status_response = requests.get(f"{base_url}/api/v1/status/config", timeout=5)

        if status_response.status_code == 200:

            # Version is in build info, not config (simplified)

            result["version"] = "unknown"  # Would parse from /api/v1/status/buildinfo



        # Count metrics

        metrics_response = requests.get(f"{base_url}/api/v1/label/__name__/values", timeout=10)

        if metrics_response.status_code == 200:

            data = metrics_response.json()

            if data["status"] == "success":

                result["metric_count"] = len(data["data"])



        return result



    except requests.exceptions.RequestException as e:

        result["error"] = f"Connection failed: {e}"

        return result



# Usage

health = check_prometheus_health()

if health["healthy"]:

    print(f"✓ Prometheus healthy ({health['metric_count']} metrics)")

else:

    print(f"✗ Prometheus unhealthy: {health['error']}")

```

---

### Example 2: Metric Discovery with Ranking

**Goal**: Find best-matching metrics for user intent with relevance scoring

```python

from typing import List, Dict

import re



def discover_metrics(

    client: PrometheusClient,

    intent: str,

    pattern: str = None

) -> List[Dict[str, any]]:

    """Discover metrics matching user intent with relevance scoring."""



    # Keyword mapping for intent parsing

    keyword_patterns = {

        "latency": ["duration", "latency", "time"],

        "error": ["error", "failed", "failure", "exception"],

        "throughput": ["count", "total", "requests"],

        "utilization": ["usage", "utilization", "percent"],

    }



    # Extract keywords from intent

    intent_lower = intent.lower()

    search_terms = []

    for category, terms in keyword_patterns.items():

        if category in intent_lower:

            search_terms.extend(terms)



    # Get all metrics

    all_metrics = client.get_metric_names()



    # Filter by pattern if provided

    if pattern:

        pattern_regex = re.compile(pattern.replace("*", ".*"))

        all_metrics = [m for m in all_metrics if pattern_regex.match(m)]



    # Score and rank metrics

    scored_metrics = []

    for metric_name in all_metrics:

        score = 0.0



        # Score by keyword matches

        metric_lower = metric_name.lower()

        for term in search_terms:

            if term in metric_lower:

                score += 1.0



        # Normalize by metric name length (prefer concise names)

        score = score / (len(metric_name) / 30.0)



        # Boost http/api metrics for service monitoring

        if "http" in metric_lower or "api" in metric_lower:

            score *= 1.2



        if score > 0:

            # Get labels for this metric

            try:

                # Query metric to get labels

                result = client.query(f"{metric_name}")

                labels = []

                if result.get("result"):

                    labels = list(result["result"][0].get("metric", {}).keys())



                # Detect metric type

                metric_type = detect_metric_type(client, metric_name)



                # Generate sample query

                sample_query = generate_sample_query(metric_name, metric_type)



                scored_metrics.append({

                    "name": metric_name,

                    "type": metric_type,

                    "labels": labels,

                    "sample_query": sample_query,

                    "relevance_score": score

                })

            except Exception:

                # Skip metrics that can't be queried

                continue



    # Sort by relevance score (descending)

    scored_metrics.sort(key=lambda x: x["relevance_score"], reverse=True)



    # Return top 5

    return scored_metrics[:5]



def generate_sample_query(metric_name: str, metric_type: str) -> str:

    """Generate sample PromQL query based on metric type."""

    if metric_type == "counter":

        return f"rate({metric_name}[5m])"

    elif metric_type == "histogram":

        base_name = metric_name.replace("_bucket", "")

        return f"histogram_quantile(0.95, sum by (le) (rate({base_name}_bucket[5m])))"

    else:  # gauge

        return f"avg({metric_name})"



# Usage

metrics = discover_metrics(

    client,

    intent="Monitor API latency trends",

    pattern="http*"

)



for metric in metrics:

    print(f"{metric['name']} (score: {metric['relevance_score']:.2f})")

    print(f"  Type: {metric['type']}")

    print(f"  Labels: {', '.join(metric['labels'])}")

    print(f"  Sample: {metric['sample_query']}")

```

---

### Example 3: PromQL Query Validator

**Goal**: Validate PromQL query syntax and data availability

```python

def validate_promql_query(

    client: PrometheusClient,

    query: str

) -> Dict[str, any]:

    """Validate PromQL query and check data availability."""



    result = {

        "valid": False,

        "has_data": False,

        "error": None,

        "suggestion": None,

        "sample_result": None

    }



    # Client-side syntax checks

    if not query.strip():

        result["error"] = "Empty query"

        return result



    # Check balanced parentheses

    if query.count("(") != query.count(")"):

        result["error"] = "Unbalanced parentheses"

        result["suggestion"] = "Add missing closing parenthesis ')'"

        return result



    if query.count("[") != query.count("]"):

        result["error"] = "Unbalanced square brackets"

        result["suggestion"] = "Add missing closing bracket ']'"

        return result



    # Server-side validation via instant query

    try:

        response = client.query(query)



        result["valid"] = True

        result["has_data"] = len(response.get("result", [])) > 0



        if result["has_data"]:

            # Extract sample result

            sample = response["result"]

            result["sample_result"] = {

                "metric": sample.get("metric", {}),

                "value": sample.get("value", [None, None])

            }

        else:

            result["suggestion"] = "Query is valid but returned no data. Check if metric exists and has recent data points."



        return result



    except ValueError as e:

        # API returned error

        error_msg = str(e)

        result["error"] = error_msg



        # Parse error and suggest fixes

        if "parse error" in error_msg.lower():

            result["suggestion"] = "Check PromQL syntax: https://prometheus.io/docs/prometheus/latest/querying/basics/"

        elif "unknown function" in error_msg.lower():

            # Extract function name and suggest alternatives

            result["suggestion"] = "Unknown function. Did you mean: rate(), increase(), sum(), avg()?"

        elif "timeout" in error_msg.lower() or "422" in error_msg:

            result["suggestion"] = "Query timeout. Simplify query: reduce time range, remove complex aggregations"



        return result



    except RuntimeError as e:

        # Prometheus unavailable

        result["error"] = str(e)

        result["suggestion"] = "Check Prometheus connectivity: kubectl port-forward prometheus-server 9090:9090"

        return result



# Usage

validation = validate_promql_query(

    client,

    "rate(http_server_request_count[5m])"

)



if validation["valid"]:

    if validation["has_data"]:

        print(f"✓ Query valid with data: {validation['sample_result']}")

    else:

        print(f"⚠ Query valid but no data: {validation['suggestion']}")

else:

    print(f"✗ Query invalid: {validation['error']}")

    print(f"  Suggestion: {validation['suggestion']}")

```

---

## Sources & References

**Primary Sources**:

1. **Prometheus HTTP API v1 Documentation**: https://prometheus.io/docs/prometheus/latest/querying/api/
   - API endpoints, request/response formats, error codes

2. **PromQL Query Language**: https://prometheus.io/docs/prometheus/latest/querying/basics/
   - Functions, operators, aggregations, metric types

3. **Prometheus Best Practices**: https://prometheus.io/docs/practices/naming/
   - Metric naming conventions, label usage, cardinality management

4. **Google SRE Workbook**: https://sre.google/workbook/monitoring/
   - Four Golden Signals, USE method, RED method, SLI/SLO patterns

**Additional References**:

- Grafana Dashboard JSON Model: https://grafana.com/docs/grafana/latest/dashboards/json-model/

- OpenTelemetry Semantic Conventions: https://opentelemetry.io/docs/specs/semconv/

- Prometheus Alerting Best Practices: https://prometheus.io/docs/practices/alerting/

---

**Document Version**: 1.0.0

**Last Updated**: 2025-10-30

**Maintained by**: grafana-dashboard-builder

**Review Cycle**: Quarterly (or when Prometheus/Grafana major version updates)
