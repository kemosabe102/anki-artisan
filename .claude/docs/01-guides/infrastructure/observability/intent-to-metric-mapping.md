# Intent-to-Metric Mapping Framework

**Domain**: Observability & Monitoring | **Agent**: grafana-dashboard-builder

**Purpose**: Translate natural language monitoring goals into Prometheus metric queries

**Audience**: AI agents creating Grafana dashboards from monitoring requirements

**Version Compatibility**: See [README.md](./README.md#version-compatibility) for Grafana 12.x, Prometheus 3.x, and Jaeger 2.x compatibility details.

---

## Overview

### Problem Statement

Users express monitoring needs in natural language:

- "Show me API latency for the checkout service"

- "I need to track error rates across all microservices"

- "Monitor CPU saturation for production pods"

This framework translates these **intents** into **precise Prometheus PromQL queries** by:

1. Classifying monitoring intent into 4 categories (LATENCY, THROUGHPUT, ERROR, SATURATION)

2. Discovering matching metrics using naming conventions and labels

3. Scoring confidence based on metric name, labels, type, and unit alignment

4. Generating optimal PromQL queries with appropriate aggregations

### Key Principles

**Intent-First Design**: Start with "what to monitor" (user intent) before "how to query" (PromQL syntax)

**Confidence-Scored Matching**: Prefer high-confidence exact matches over regex fallbacks to prevent false positives

**Label-Aware Discovery**: Use service labels (job, namespace, pod) for precise targeting, not just metric names

**Fallback Strategies**: Graceful degradation when no exact match exists (suggest alternatives, regex search, user clarification)

---

## Core Frameworks

### Framework 1: Intent Taxonomy (4 Categories)

**Classification**: All monitoring intents map to one of four categories based on Google SRE "Four Golden Signals"

| Intent Category | Description | Example User Phrases | Metric Patterns |

|----------------|-------------|---------------------|-----------------|

| **LATENCY** | Time to serve requests | "response time", "latency", "duration", "delay" | `*_duration_*`, `*_latency_*`, `*_response_time_*` (type: histogram/summary) |

| **THROUGHPUT** | Rate of operations | "requests per second", "RPS", "QPS", "traffic" | `*_requests_total`, `*_operations_total` (type: counter) |

| **ERROR** | Failure rate | "error rate", "failures", "5xx errors", "failed requests" | `*_errors_total`, `*_failed_*`, `*_status{code=~"5.."}` (type: counter) |

| **SATURATION** | Resource utilization | "CPU usage", "memory usage", "saturation", "utilization" | `*_cpu_*`, `*_memory_*`, `*_usage_*`, `*_utilization_*` (type: gauge) |

**Decision Tree** (Intent Classification):

```

Input: User phrase



1. Check for latency keywords (duration, latency, response time, delay)

   → YES: Intent = LATENCY



2. Check for throughput keywords (requests, RPS, QPS, traffic, rate)

   → YES: Intent = THROUGHPUT



3. Check for error keywords (error, failure, 5xx, failed)

   → YES: Intent = ERROR



4. Check for saturation keywords (CPU, memory, utilization, saturation, usage)

   → YES: Intent = SATURATION



5. Multiple keywords matched?

   → Use priority: LATENCY > ERROR > THROUGHPUT > SATURATION

   → Rationale: User experience impact (latency affects UX most)



6. No keywords matched?

   → Default: THROUGHPUT (most common monitoring intent)

   → Confidence: 0.3 (LOW - request user clarification)

```

**Algorithmic Implementation** (Pseudocode):

```python

def classify_intent(user_phrase: str) -> tuple[IntentCategory, float]:

    """

    Classify monitoring intent from natural language phrase.



    Returns: (intent_category, confidence_score)

    """

    phrase_lower = user_phrase.lower()



    # Keyword matching with weights

    latency_keywords = {"latency", "duration", "response time", "delay", "p95", "p99"}

    throughput_keywords = {"requests", "rps", "qps", "traffic", "rate", "throughput"}

    error_keywords = {"error", "failure", "5xx", "failed", "exception"}

    saturation_keywords = {"cpu", "memory", "utilization", "saturation", "usage", "capacity"}



    # Count matches

    latency_score = sum(1 for kw in latency_keywords if kw in phrase_lower)

    throughput_score = sum(1 for kw in throughput_keywords if kw in phrase_lower)

    error_score = sum(1 for kw in error_keywords if kw in phrase_lower)

    saturation_score = sum(1 for kw in saturation_keywords if kw in phrase_lower)



    # Determine category

    scores = {

        "LATENCY": latency_score,

        "THROUGHPUT": throughput_score,

        "ERROR": error_score,

        "SATURATION": saturation_score

    }



    max_score = max(scores.values())



    if max_score == 0:

        return ("THROUGHPUT", 0.3)  # Default with LOW confidence



    # Priority tiebreaker: LATENCY > ERROR > THROUGHPUT > SATURATION

    priority_order = ["LATENCY", "ERROR", "THROUGHPUT", "SATURATION"]

    for category in priority_order:

        if scores[category] == max_score:

            confidence = min(1.0, max_score / 3.0)  # Normalize to 0.0-1.0

            return (category, confidence)



    return ("THROUGHPUT", 0.5)  # Fallback

```

---

### Framework 2: Prometheus Metric Naming Conventions

**Official Standard** (prometheus.io/docs/practices/naming):

**Pattern**: `<namespace>_<subsystem>_<name>_<unit>`

**Examples**:

- `http_request_duration_seconds` (namespace: http, subsystem: request, name: duration, unit: seconds)

- `process_cpu_usage_ratio` (namespace: process, subsystem: cpu, name: usage, unit: ratio)

- `database_query_errors_total` (namespace: database, subsystem: query, name: errors, unit: total)

**Unit Suffixes** (standardized):

- Time: `_seconds`, `_milliseconds`, `_microseconds`

- Bytes: `_bytes`, `_kilobytes`, `_megabytes`

- Counters: `_total` (monotonically increasing)

- Ratios: `_ratio` (0.0-1.0) or no suffix for percentages (0-100)

- Gauges: No suffix (current value, can go up/down)

**Metric Types** (OpenMetrics):

- **Counter**: Monotonically increasing (requests_total, errors_total)

- **Gauge**: Current value (cpu_usage, memory_bytes)

- **Histogram**: Distributions with buckets (request_duration_seconds_bucket)

- **Summary**: Quantiles (request_duration_seconds{quantile="0.95"})

**Parsing Algorithm** (Extract Components):

```python

def parse_metric_name(metric_name: str) -> dict:

    """

    Parse metric name into components.



    Returns: {

        "namespace": str,

        "subsystem": str,

        "name": str,

        "unit": str,

        "type_hint": str  # Inferred from unit suffix

    }

    """

    parts = metric_name.split('_')



    # Identify unit suffix

    unit_suffixes = {

        "seconds": "TIME", "milliseconds": "TIME", "microseconds": "TIME",

        "bytes": "SIZE", "kilobytes": "SIZE", "megabytes": "SIZE",

        "total": "COUNTER", "ratio": "RATIO"

    }



    unit = None

    type_hint = "GAUGE"  # Default



    for suffix, hint in unit_suffixes.items():

        if metric_name.endswith(f"_{suffix}"):

            unit = suffix

            type_hint = hint

            parts = parts[:-1]  # Remove unit from parts

            break



    # Extract components (heuristic)

    if len(parts) >= 3:

        namespace = parts

        subsystem = parts

        name = '_'.join(parts[2:])

    elif len(parts) == 2:

        namespace = parts

        subsystem = None

        name = parts

    else:

        namespace = None

        subsystem = None

        name = parts



    return {

        "namespace": namespace,

        "subsystem": subsystem,

        "name": name,

        "unit": unit,

        "type_hint": type_hint

    }

```

---

### Framework 3: Label-Based Service Identification

**Standard Labels** (Kubernetes & Prometheus):

| Label | Purpose | Example Values | Discovery Use |

|-------|---------|----------------|---------------|

| `job` | Scrape target | `api-server`, `checkout-service` | Primary service identifier |

| `instance` | Host/pod | `10.0.1.5:8080`, `pod-abc123` | Instance-level filtering |

| `namespace` | K8s namespace | `production`, `staging` | Environment filtering |

| `pod` | Pod name | `api-deployment-7d8f9-xkj2p` | Pod-level filtering |

| `container` | Container name | `app`, `sidecar` | Container-level filtering |

| `service` | K8s service | `checkout`, `payment` | Service-level aggregation |

**Label Resolution Strategy** (Match user input to labels):

```python

def resolve_service_labels(user_input: str, available_labels: dict) -> dict:

    """

    Match user input to Prometheus labels.



    Args:

        user_input: "checkout service in production"

        available_labels: {"job": [...], "namespace": [...], "service": [...]}



    Returns: {"job": "checkout-service", "namespace": "production"}

    """

    input_lower = user_input.lower()

    label_matchers = {}



    # Extract service name (job or service label)

    for label in ["job", "service"]:

        if label in available_labels:

            for value in available_labels[label]:

                if value.lower() in input_lower or input_lower in value.lower():

                    label_matchers[label] = value

                    break



    # Extract namespace (environment)

    env_keywords = {

        "production": ["prod", "production", "prd"],

        "staging": ["staging", "stg", "stage"],

        "development": ["dev", "development"]

    }



    for env, keywords in env_keywords.items():

        if any(kw in input_lower for kw in keywords):

            if env in available_labels.get("namespace", []):

                label_matchers["namespace"] = env

                break



    return label_matchers

```

---

### Framework 4: Confidence Scoring Formula

**Purpose**: Rank metric candidates to select the best match for user intent

**Formula**: `Confidence = (metric_name_match × 0.40) + (label_match × 0.25) + (type_alignment × 0.20) + (unit_correctness × 0.15)`

**Components**:

1. **Metric Name Match** (0.40 weight):
   - Exact keyword match: 1.0 (e.g., "latency" in `http_request_latency_seconds`)

   - Partial match: 0.7 (e.g., "duration" for latency intent)

   - Regex match: 0.5 (e.g., `.*request.*` for throughput)

   - No match: 0.0

2. **Label Match** (0.25 weight):
   - Service label matches: 1.0 (e.g., `job="checkout-service"`)

   - Namespace matches: 0.8 (e.g., `namespace="production"`)

   - No service context: 0.5 (default to all services)

3. **Type Alignment** (0.20 weight):
   - Counter for THROUGHPUT/ERROR: 1.0

   - Histogram/Summary for LATENCY: 1.0

   - Gauge for SATURATION: 1.0

   - Type mismatch: 0.3 (penalty)

4. **Unit Correctness** (0.15 weight):
   - Correct unit for intent: 1.0 (e.g., `_seconds` for LATENCY)

   - Missing unit but correct type: 0.7

   - Incorrect unit: 0.2

**Confidence Thresholds**:

- **High** (≥0.75): Use metric directly

- **Medium** (0.50-0.74): Use metric with user confirmation

- **Low** (<0.50): Suggest alternatives or request clarification

**Algorithmic Implementation**:

```python

def calculate_metric_confidence(

    metric: dict,

    intent: str,

    user_labels: dict

) -> float:

    """

    Calculate confidence score for metric match.



    Args:

        metric: {"name": str, "type": str, "labels": dict, "unit": str}

        intent: "LATENCY" | "THROUGHPUT" | "ERROR" | "SATURATION"

        user_labels: {"job": "checkout-service", "namespace": "production"}



    Returns: confidence_score (0.0-1.0)

    """

    # 1. Metric Name Match (0.40)

    intent_keywords = {

        "LATENCY": ["latency", "duration", "delay", "response_time"],

        "THROUGHPUT": ["requests", "operations", "queries", "rps"],

        "ERROR": ["error", "failure", "failed", "exception"],

        "SATURATION": ["cpu", "memory", "usage", "utilization", "saturation"]

    }



    name_score = 0.0

    metric_name_lower = metric["name"].lower()



    for keyword in intent_keywords[intent]:

        if keyword in metric_name_lower:

            name_score = 1.0  # Exact match

            break

        elif keyword.replace('_', '') in metric_name_lower.replace('_', ''):

            name_score = 0.7  # Partial match



    if name_score == 0.0 and re.search(rf".*{intent.lower()[:4]}.*", metric_name_lower):

        name_score = 0.5  # Regex fallback



    # 2. Label Match (0.25)

    label_score = 0.5  # Default (no service context)



    for label, value in user_labels.items():

        if label in metric["labels"] and metric["labels"][label] == value:

            if label == "job" or label == "service":

                label_score = 1.0  # Service match

                break

            elif label == "namespace":

                label_score = 0.8  # Environment match



    # 3. Type Alignment (0.20)

    type_alignment = {

        "LATENCY": ["histogram", "summary"],

        "THROUGHPUT": ["counter"],

        "ERROR": ["counter"],

        "SATURATION": ["gauge"]

    }



    type_score = 1.0 if metric["type"] in type_alignment[intent] else 0.3



    # 4. Unit Correctness (0.15)

    unit_correctness = {

        "LATENCY": ["seconds", "milliseconds", "microseconds"],

        "THROUGHPUT": ["total"],

        "ERROR": ["total"],

        "SATURATION": ["ratio", "bytes", None]  # Gauges may lack unit

    }



    unit_score = 1.0 if metric["unit"] in unit_correctness[intent] else 0.7



    if metric["unit"] and metric["unit"] not in unit_correctness[intent]:

        unit_score = 0.2  # Penalty for incorrect unit



    # Final confidence

    confidence = (

        name_score * 0.40 +

        label_score * 0.25 +

        type_score * 0.20 +

        unit_score * 0.15

    )



    return round(confidence, 2)

```

---

## Processes & Workflows

### Workflow 1: Intent-to-PromQL Translation (End-to-End)

**Input**: User phrase + Service context

**Output**: PromQL query + Confidence score

**Steps**:

```

1. CLASSIFY INTENT

   Input: "Show me API latency for checkout service"

   Output: Intent = LATENCY, Confidence = 0.9



2. RESOLVE SERVICE LABELS

   Input: "checkout service"

   Output: {"job": "checkout-service"}



3. DISCOVER CANDIDATE METRICS

   Query Prometheus: /api/v1/label/__name__/values

   Filter by intent keywords: metrics with "latency", "duration", "delay"

   Candidates: [

       "http_request_duration_seconds",

       "http_request_latency_milliseconds",

       "grpc_server_handling_seconds"

   ]



4. SCORE CANDIDATES

   For each candidate, calculate_metric_confidence()

   Results:

       - http_request_duration_seconds: 0.85 (HIGH)

       - http_request_latency_milliseconds: 0.78 (HIGH)

       - grpc_server_handling_seconds: 0.45 (LOW - wrong subsystem)



5. SELECT BEST MATCH

   Top candidate: http_request_duration_seconds (0.85)



6. GENERATE PROMQL

   Base query: http_request_duration_seconds{job="checkout-service"}

   Aggregation (histogram): histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="checkout-service"}[5m]))



7. VALIDATE QUERY

   Test against Prometheus: /api/v1/query

   If fails: Use fallback (remove aggregation, try simpler query)



8. RETURN RESULT

   {

       "query": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"checkout-service\"}[5m]))",

       "metric": "http_request_duration_seconds",

       "confidence": 0.85,

       "intent": "LATENCY",

       "description": "95th percentile request duration for checkout service"

   }

```

**Algorithmic Implementation** (Orchestration):

```python

def translate_intent_to_promql(

    user_phrase: str,

    prometheus_client: PrometheusAPI

) -> dict:

    """

    End-to-end translation from user intent to PromQL.



    Returns: {

        "query": str,

        "metric": str,

        "confidence": float,

        "intent": str,

        "description": str

    }

    """

    # Step 1: Classify intent

    intent, intent_confidence = classify_intent(user_phrase)



    # Step 2: Resolve service labels

    available_labels = prometheus_client.get_label_values()

    service_labels = resolve_service_labels(user_phrase, available_labels)



    # Step 3: Discover candidates

    all_metrics = prometheus_client.get_metric_names()

    intent_keywords = get_intent_keywords(intent)



    candidates = [

        m for m in all_metrics

        if any(kw in m.lower() for kw in intent_keywords)

    ]



    if not candidates:

        # Fallback: Regex search

        candidates = [

            m for m in all_metrics

            if re.search(rf".*{intent.lower()[:4]}.*", m.lower())

        ]



    # Step 4: Score candidates

    scored_candidates = []

    for metric_name in candidates:

        metric_metadata = prometheus_client.get_metric_metadata(metric_name)

        confidence = calculate_metric_confidence(

            metric_metadata,

            intent,

            service_labels

        )

        scored_candidates.append((metric_name, confidence, metric_metadata))



    # Step 5: Select best match

    scored_candidates.sort(key=lambda x: x[1], reverse=True)



    if not scored_candidates or scored_candidates[0][1] < 0.50:

        return {

            "query": None,

            "metric": None,

            "confidence": 0.0,

            "intent": intent,

            "description": "No suitable metric found. Please clarify monitoring goal."

        }



    best_metric, best_confidence, best_metadata = scored_candidates



    # Step 6: Generate PromQL

    promql = generate_promql(

        metric_name=best_metric,

        metric_type=best_metadata["type"],

        labels=service_labels,

        intent=intent

    )



    # Step 7: Validate (optional - may query Prometheus)

    # if not prometheus_client.validate_query(promql):

    #     promql = simplify_promql(promql)  # Fallback



    # Step 8: Return result

    return {

        "query": promql,

        "metric": best_metric,

        "confidence": best_confidence,

        "intent": intent,

        "description": generate_description(best_metric, intent, service_labels)

    }

```

---

### Workflow 2: PromQL Query Generation (Type-Specific)

**Purpose**: Generate appropriate PromQL syntax based on metric type and intent

**Rules**:

1. **Counter** (THROUGHPUT, ERROR):
   - Always use `rate()` or `irate()` for per-second rates

   - Window: `[5m]` (5-minute rate, standard)

   - Aggregation: `sum(rate(...))` for totals

2. **Histogram** (LATENCY):
   - Use `histogram_quantile()` for percentiles

   - Common quantiles: 0.50 (median), 0.95 (p95), 0.99 (p99)

   - Requires `_bucket` suffix and `le` label

3. **Summary** (LATENCY):
   - Pre-calculated quantiles available

   - Use `{quantile="0.95"}` label selector

   - No `rate()` needed for quantile values

4. **Gauge** (SATURATION):
   - Use raw value or `avg_over_time()` for smoothing

   - Aggregation: `avg()` for averages, `max()` for peaks

**PromQL Generation Algorithm**:

```python

def generate_promql(

    metric_name: str,

    metric_type: str,

    labels: dict,

    intent: str

) -> str:

    """

    Generate PromQL query based on metric type and intent.



    Args:

        metric_name: "http_request_duration_seconds"

        metric_type: "histogram"

        labels: {"job": "checkout-service"}

        intent: "LATENCY"



    Returns: PromQL query string

    """

    # Build label selector

    label_selector = ','.join([f'{k}="{v}"' for k, v in labels.items()])



    if intent == "LATENCY":

        if metric_type == "histogram":

            # Histogram quantile (p95 by default)

            return (

                f'histogram_quantile(0.95, '

                f'rate({metric_name}_bucket{{{label_selector}}}[5m]))'

            )

        elif metric_type == "summary":

            # Summary with pre-calculated quantile

            label_with_quantile = f'{label_selector},quantile="0.95"' if label_selector else 'quantile="0.95"'

            return f'{metric_name}{{{label_with_quantile}}}'

        else:

            # Gauge fallback (rare for latency)

            return f'{metric_name}{{{label_selector}}}'



    elif intent == "THROUGHPUT":

        if metric_type == "counter":

            # Per-second rate

            return f'sum(rate({metric_name}{{{label_selector}}}[5m]))'

        else:

            # Gauge fallback (instantaneous value)

            return f'{metric_name}{{{label_selector}}}'



    elif intent == "ERROR":

        if metric_type == "counter":

            # Error rate (errors per second)

            return f'sum(rate({metric_name}{{{label_selector}}}[5m]))'

        else:

            # Count of errors

            return f'{metric_name}{{{label_selector}}}'



    elif intent == "SATURATION":

        if metric_type == "gauge":

            # Average over time (smooth out spikes)

            return f'avg_over_time({metric_name}{{{label_selector}}}[5m])'

        else:

            # Raw value

            return f'{metric_name}{{{label_selector}}}'



    # Default fallback

    return f'{metric_name}{{{label_selector}}}'

```

---

## Decision Trees

### Decision Tree 1: No Metric Match Found

**Trigger**: `calculate_metric_confidence()` returns <0.50 for all candidates

**Actions**:

```

1. Check if user provided service context

   → NO: Request service name

      "I couldn't find a latency metric. Which service should I monitor?"



   → YES: Proceed to step 2



2. Expand keyword search (loosen criteria)

   - Remove subsystem requirement (e.g., accept "duration" without "request")

   - Search across ALL metrics (not just intent-filtered)



   → Found match with confidence ≥0.50?

      YES: Return match with warning

           "Using best available metric: <metric_name> (confidence: 0.XX).

            This may not be optimal. Verify metric is correct."



      NO: Proceed to step 3



3. Regex fallback search

   Pattern: `.*{intent_keyword}.*` (e.g., `.*latency.*`)



   → Found matches?

      YES: Return top 3 candidates

           "No exact match found. Did you mean one of these?

            1. http_server_latency_seconds (0.45)

            2. grpc_latency_milliseconds (0.42)

            3. app_response_time_ms (0.38)"



      NO: Proceed to step 4



4. Suggest metric creation

   "No existing metric found for '{intent}' in '{service}'.

    You may need to instrument your service with:

    - Counter: {service}_requests_total

    - Histogram: {service}_request_duration_seconds

    See Prometheus client library docs for instrumentation."



5. Escalate to user

   Return: {

       "query": null,

       "confidence": 0.0,

       "suggestions": [...],

       "action_required": "clarify_intent_or_instrument_service"

   }

```

---

### Decision Tree 2: Multiple High-Confidence Candidates

**Trigger**: 2+ metrics with confidence ≥0.75

**Actions**:

```

1. Check for subsystem differences

   Example:

       - http_request_duration_seconds (HTTP subsystem)

       - grpc_server_handling_seconds (gRPC subsystem)



   → Different subsystems?

      YES: Ask user to specify protocol

           "Found metrics for HTTP and gRPC. Which protocol should I monitor?

            - HTTP: http_request_duration_seconds

            - gRPC: grpc_server_handling_seconds"



      NO: Proceed to step 2



2. Check for unit differences

   Example:

       - request_duration_seconds (seconds)

       - request_duration_milliseconds (milliseconds)



   → Different units?

      YES: Prefer standard unit (seconds for time, bytes for size)

           Select: request_duration_seconds

           Confidence boost: +0.05



      NO: Proceed to step 3



3. Check for type differences

   Example:

       - request_duration_seconds (histogram)

       - request_duration_seconds_summary (summary)



   → Different types?

      YES: Prefer histogram over summary (more flexible aggregation)

           Select: histogram version



      NO: Proceed to step 4



4. Select metric with highest confidence

   If tie: Use alphabetical order (deterministic)



   Return top match with note:

   "Using {metric_name} (confidence: 0.XX).

    Alternative: {alternative_metric} also available."

```

---

### Decision Tree 3: Regex Fallback Strategy

**Trigger**: No exact keyword match in metric names

**Fallback Levels** (progressive relaxation):

```

Level 1: Intent-specific regex

    LATENCY: `.*(?:latency|duration|delay|time).*`

    THROUGHPUT: `.*(?:requests|operations|queries|rate).*`

    ERROR: `.*(?:error|failure|failed|exception).*`

    SATURATION: `.*(?:cpu|memory|usage|utilization).*`



    → Found match? Use it (confidence penalty: -0.20)



Level 2: Unit-based regex

    LATENCY: `.*_seconds$|.*_milliseconds$`

    THROUGHPUT: `.*_total$`

    ERROR: `.*_total$` + filter by name containing "error"

    SATURATION: `.*_ratio$|.*_bytes$`



    → Found match? Use it (confidence penalty: -0.30)



Level 3: Generic pattern search

    Search for ANY metric with service label match

    Filter by metric type alignment (counter for throughput, etc.)



    → Found match? Use it (confidence penalty: -0.40)



Level 4: Failure

    Return null with suggestion to instrument service

```

**Implementation**:

```python

def regex_fallback_search(

    intent: str,

    available_metrics: list,

    service_labels: dict

) -> list:

    """

    Progressive regex search when no exact match found.



    Returns: [(metric_name, confidence_adjusted), ...]

    """

    # Level 1: Intent-specific regex

    intent_patterns = {

        "LATENCY": r".*(?:latency|duration|delay|time).*",

        "THROUGHPUT": r".*(?:requests|operations|queries|rate).*",

        "ERROR": r".*(?:error|failure|failed|exception).*",

        "SATURATION": r".*(?:cpu|memory|usage|utilization).*"

    }



    pattern = intent_patterns[intent]

    matches = [m for m in available_metrics if re.match(pattern, m, re.IGNORECASE)]



    if matches:

        return [(m, 0.50) for m in matches]  # Confidence penalty: -0.20



    # Level 2: Unit-based regex

    unit_patterns = {

        "LATENCY": r".*_(?:seconds|milliseconds|microseconds)$",

        "THROUGHPUT": r".*_total$",

        "ERROR": r".*_total$",

        "SATURATION": r".*_(?:ratio|bytes)$"

    }



    pattern = unit_patterns[intent]

    matches = [m for m in available_metrics if re.match(pattern, m, re.IGNORECASE)]



    if intent == "ERROR":

        # Additional filter for error-related names

        matches = [m for m in matches if "error" in m.lower() or "fail" in m.lower()]



    if matches:

        return [(m, 0.40) for m in matches]  # Confidence penalty: -0.30



    # Level 3: Generic pattern (service label match)

    # (Requires querying Prometheus for label values - not implemented here)



    # Level 4: Failure

    return []

```

---

## Anti-Patterns

### Anti-Pattern 1: High Cardinality Queries

**Problem**: Querying metrics with unbounded label values (e.g., user IDs, request IDs)

**Example** (BAD):

```promql

rate(http_requests_total{user_id=~".*"}[5m])

```

**Why Bad**:

- Prometheus stores time series per unique label combination

- Unbounded labels create millions of series → memory exhaustion

- Query performance degrades exponentially

**Fix**: Aggregate first, then filter

```promql

sum(rate(http_requests_total[5m])) by (job, status_code)

```

**Detection**: Check for labels like `user_id`, `request_id`, `trace_id`, `session_id`

---

### Anti-Pattern 2: Bare Metric Selectors

**Problem**: Using metric name without labels in multi-service environments

**Example** (BAD):

```promql

http_request_duration_seconds

```

**Why Bad**:

- Returns data for ALL services using this metric

- Confusing graphs with mixed service data

- No service-level isolation

**Fix**: Always include service label

```promql

http_request_duration_seconds{job="checkout-service"}

```

**Enforcement**: Require `job` or `service` label in all queries

---

### Anti-Pattern 3: Inefficient Regex Patterns

**Problem**: Using greedy regex that scans all label values

**Example** (BAD):

```promql

http_requests_total{path=~"/api/.*"}

```

**Why Bad**:

- Regex evaluated against every label value (expensive)

- Prometheus index can't optimize regex queries

- Better to use label value equality when possible

**Fix**: Use exact match or prefix match

```promql

http_requests_total{path="/api/users"}  # Best

http_requests_total{path=~"/api/users.*"}  # Better (prefix)

```

**When Regex is Acceptable**:

- Small number of label values (<100)

- Prefix patterns (start with literal string)

- Example: `path=~"/api/v2/.*"` (prefix match on `/api/v2/`)

---

### Anti-Pattern 4: Incorrect Aggregation for Histograms

**Problem**: Using `sum()` instead of `histogram_quantile()` for latency

**Example** (BAD):

```promql

sum(http_request_duration_seconds_bucket{job="api"})

```

**Why Bad**:

- Histogram buckets represent cumulative counts (le="0.1", le="0.5", etc.)

- Summing buckets produces meaningless values

- Loses distribution information

**Fix**: Use `histogram_quantile()` for percentiles

```promql

histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api"}[5m]))

```

**Rule**: Always use `histogram_quantile()` when metric has `_bucket` suffix

---

### Anti-Pattern 5: Missing `rate()` for Counters

**Problem**: Querying counter directly instead of rate of change

**Example** (BAD):

```promql

http_requests_total{job="api"}

```

**Why Bad**:

- Counter is monotonically increasing (cumulative)

- Raw value is meaningless (e.g., 1,234,567 total requests since start)

- Doesn't show current load

**Fix**: Use `rate()` for per-second rate

```promql

sum(rate(http_requests_total{job="api"}[5m]))

```

**Rule**: Always apply `rate()` or `irate()` to counter metrics (suffix `_total`)

---

## Integration Points

### Integration 1: Metric Discovery Capability

**Purpose**: Query Prometheus for available metrics and labels

**API Endpoints**:

1. **List All Metrics**: `GET /api/v1/label/__name__/values`
   - Returns: `["http_request_duration_seconds", "process_cpu_usage", ...]`

   - Use: Candidate discovery

2. **Get Label Values**: `GET /api/v1/label/{label_name}/values`
   - Example: `/api/v1/label/job/values` → `["api-server", "checkout-service"]`

   - Use: Service identification

3. **Metric Metadata**: `GET /api/v1/metadata?metric={metric_name}`
   - Returns: `{"type": "histogram", "help": "Request duration in seconds", "unit": "seconds"}`

   - Use: Type and unit validation

4. **Series Query**: `GET /api/v1/series?match[]={metric_name}`
   - Returns: Label combinations for metric

   - Use: Label discovery

**Caching Strategy**:

- Cache metric list (TTL: 5 minutes)

- Cache label values (TTL: 5 minutes)

- Cache metadata (TTL: 1 hour)

- Invalidate on Prometheus restart

---

### Integration 2: PromQL Query Construction

**Purpose**: Build syntactically correct PromQL from components

**Query Templates** (by intent and type):

```python

QUERY_TEMPLATES = {

    ("LATENCY", "histogram"): 'histogram_quantile({quantile}, rate({metric}_bucket{{{labels}}}[{window}]))',

    ("LATENCY", "summary"): '{metric}{{{labels},quantile="{quantile}"}}',

    ("LATENCY", "gauge"): 'avg_over_time({metric}{{{labels}}}[{window}])',



    ("THROUGHPUT", "counter"): 'sum(rate({metric}{{{labels}}}[{window}]))',

    ("THROUGHPUT", "gauge"): '{metric}{{{labels}}}',



    ("ERROR", "counter"): 'sum(rate({metric}{{{labels}}}[{window}]))',



    ("SATURATION", "gauge"): 'avg_over_time({metric}{{{labels}}}[{window}])',

}



def build_promql(

    metric: str,

    metric_type: str,

    intent: str,

    labels: dict,

    quantile: float = 0.95,

    window: str = "5m"

) -> str:

    """

    Build PromQL query from template.



    Args:

        metric: "http_request_duration_seconds"

        metric_type: "histogram"

        intent: "LATENCY"

        labels: {"job": "api-server", "namespace": "production"}

        quantile: 0.95 (for percentiles)

        window: "5m" (time window)



    Returns: PromQL query string

    """

    template = QUERY_TEMPLATES.get((intent, metric_type))



    if not template:

        # Fallback: Simple selector

        label_str = ','.join([f'{k}="{v}"' for k, v in labels.items()])

        return f'{metric}{{{label_str}}}'



    # Format template

    label_str = ','.join([f'{k}="{v}"' for k, v in labels.items()])



    return template.format(

        metric=metric,

        labels=label_str,

        quantile=quantile,

        window=window

    )

```

---

### Integration 3: RED Method Auto-Detection

**Purpose**: Automatically generate RED metrics (Rate, Error, Duration) for services

**RED Pattern**:

- **Rate**: `sum(rate(http_requests_total{job="service"}[5m]))`

- **Error**: `sum(rate(http_requests_total{job="service",status_code=~"5.."}[5m]))`

- **Duration**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="service"}[5m]))`

**Auto-Detection Algorithm**:

```python

def detect_red_metrics(service_name: str, prometheus_client: PrometheusAPI) -> dict:

    """

    Auto-detect RED metrics for a service.



    Returns: {

        "rate_metric": str,

        "error_metric": str,

        "duration_metric": str,

        "confidence": float

    }

    """

    all_metrics = prometheus_client.get_metric_names()

    service_labels = {"job": service_name}



    # Detect Rate metric (counter with "requests" or "operations")

    rate_candidates = [

        m for m in all_metrics

        if any(kw in m.lower() for kw in ["requests_total", "operations_total"])

    ]



    rate_metric = None

    for candidate in rate_candidates:

        # Check if metric has service label

        series = prometheus_client.get_series(candidate, service_labels)

        if series:

            rate_metric = candidate

            break



    # Detect Error metric (same as rate, but filter by status code)

    error_metric = rate_metric  # Same metric, different label filter



    # Detect Duration metric (histogram with "duration" or "latency")

    duration_candidates = [

        m for m in all_metrics

        if any(kw in m.lower() for kw in ["duration", "latency"])

        and m.endswith("_seconds")  # Standard unit

    ]



    duration_metric = None

    for candidate in duration_candidates:

        metadata = prometheus_client.get_metadata(candidate)

        if metadata.get("type") == "histogram":

            series = prometheus_client.get_series(candidate, service_labels)

            if series:

                duration_metric = candidate

                break



    # Calculate confidence

    confidence = 0.0

    if rate_metric:

        confidence += 0.40

    if error_metric:

        confidence += 0.30

    if duration_metric:

        confidence += 0.30



    return {

        "rate_metric": rate_metric,

        "error_metric": error_metric,

        "duration_metric": duration_metric,

        "confidence": confidence

    }

```

**Dashboard Generation**: Use RED metrics to auto-generate standard service dashboard:

- Panel 1: Request Rate (time series)

- Panel 2: Error Rate (time series)

- Panel 3: p95 Latency (time series)

- Panel 4: Error Rate % (gauge)

---

### Integration 4: Multi-Dimensional Queries

**Purpose**: Build queries that aggregate across multiple dimensions

**Example Use Case**: "Show me latency by HTTP status code and endpoint"

**Query Construction**:

```python

def build_multi_dimensional_query(

    metric: str,

    metric_type: str,

    intent: str,

    base_labels: dict,

    group_by_labels: list

) -> str:

    """

    Build PromQL with multi-dimensional aggregation.



    Args:

        metric: "http_request_duration_seconds"

        metric_type: "histogram"

        intent: "LATENCY"

        base_labels: {"job": "api-server"}

        group_by_labels: ["status_code", "endpoint"]



    Returns: PromQL with group-by clause

    """

    # Generate base query

    base_query = build_promql(metric, metric_type, intent, base_labels)



    # Add group-by aggregation

    if group_by_labels:

        group_by_clause = f'by ({", ".join(group_by_labels)})'



        # Insert group-by before closing parenthesis

        if "histogram_quantile" in base_query:

            # histogram_quantile(0.95, sum(rate(...)) by (status_code, endpoint))

            base_query = base_query.replace(

                "rate(",

                f"sum(rate("

            ).replace(

                "[5m]))",

                f"[5m])) {group_by_clause})"

            )

        elif "sum(" in base_query:

            # sum(rate(...)) by (status_code, endpoint)

            base_query = base_query.replace(

                "sum(rate(",

                f"sum(rate("

            ).replace(

                "))",

                f")) {group_by_clause}"

            )

        else:

            # Wrap in sum() with group-by

            base_query = f"sum({base_query}) {group_by_clause}"



    return base_query

```

**Example Output**:

```promql

histogram_quantile(0.95,

    sum(rate(http_request_duration_seconds_bucket{job="api-server"}[5m]))

    by (status_code, endpoint)

)

```

---

## Sources & References

1. **Prometheus Official Documentation**:
   - Naming conventions: https://prometheus.io/docs/practices/naming/

   - Query examples: https://prometheus.io/docs/prometheus/latest/querying/examples/

   - Best practices: https://prometheus.io/docs/practices/histograms/

2. **Google SRE Book**:
   - Four Golden Signals: https://sre.google/sre-book/monitoring-distributed-systems/

   - Chapter 6: Monitoring Distributed Systems

3. **OpenMetrics Specification**:
   - Metric types: https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md

   - Unit standardization: https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md#units

4. **PromAssistant Research** (Academic):
   - Natural language to PromQL: arxiv.org/abs/2108.05047

   - Intent classification for monitoring: "Learning to Generate Prometheus Queries"

5. **Industry Best Practices**:
   - Grafana query patterns: https://grafana.com/docs/grafana/latest/datasources/prometheus/

   - Robust Perception blog: https://www.robustperception.io/blog

---

**Document Status**: READY FOR USE

**Last Updated**: 2025-10-30

**Agent**: grafana-dashboard-builder

**Maintainer**: documentation (for structure), grafana-dashboard-builder (for content)
