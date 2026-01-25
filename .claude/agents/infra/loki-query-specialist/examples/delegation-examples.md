# Delegation Examples

**Purpose**: How orchestrator delegates to loki-query-specialist

---

## Operation Types

### 1. construct_query

```markdown
Task(loki-query-specialist,
  "Construct a LogQL query to extract error logs from the API service.
   
   Operation: construct_query
   Extraction goal: Count 5xx errors by endpoint over last hour
   Log sample: 
   ```
   {"level":"error","msg":"Request failed","status":503,"endpoint":"/api/users"}
   ```
   Loki endpoint: http://loki-service.gauntlet-agents.svc.cluster.local:3100")
```

**Expected Response**: Constructed query, parser selection rationale, test results

---

### 2. analyze_format

```markdown
Task(loki-query-specialist,
  "Analyze this log format and recommend parsing strategy.
   
   Operation: analyze_format
   Log sample:
   ```
   2025-11-10T10:30:00Z level=error msg=\"Connection failed\" host=db-01 retries=3
   ```
   Extraction goal: Extract error counts by host")
```

**Expected Response**: Format classification, recommended parser, anti-pattern detection

---

### 3. validate_syntax

```markdown
Task(loki-query-specialist,
  "Validate this LogQL query syntax.
   
   Operation: validate_syntax
   Query: {service_name=\"api\"} | json | status >= 500
   Loki endpoint: http://localhost:3100")
```

**Expected Response**: Syntax validity, errors (if any), suggested corrections

---

### 4. optimize_query

```markdown
Task(loki-query-specialist,
  "Optimize this slow query.
   
   Operation: optimize_query
   Query: {namespace=\"prod\"} | json | level=\"error\"
   Performance context: Query times out on 24h range")
```

**Expected Response**: Anti-patterns detected, prioritized recommendations, expected improvements

---

### 5. assess_log_quality

```markdown
Task(loki-query-specialist,
  "Assess log quality for our API service.
   
   Operation: assess_log_quality
   Log sample:
   ```
   msg=\"User action: {\\\"user_id\\\":\\\"123\\\",\\\"action\\\":\\\"login\\\"}\"
   ```
   Assessment depth: comprehensive")
```

**Expected Response**: Anti-pattern detection (10 categories), cardinality analysis, migration recommendations

---

## Context Metadata

Always include when delegating:

| Field | Required | Description |
|-------|----------|-------------|
| `operation_type` | YES | One of 6 operation types |
| `extraction_goal` | For construct_query | What data to extract |
| `log_sample` | For analyze/assess | Sample log lines |
| `logql_query` | For validate/optimize | Query string |
| `loki_endpoint` | Optional | Loki API URL (has default) |
| `assessment_depth` | For assess | "quick" or "comprehensive" |

---

## Multi-Agent Coordination

### Upstream
- User provides extraction goal and log sample
- Orchestrator coordinates request

### Downstream
- Returns structured JSON to orchestrator
- Orchestrator synthesizes with other agent outputs

**Note**: No sub-agent delegation - returns directly to orchestrator.
