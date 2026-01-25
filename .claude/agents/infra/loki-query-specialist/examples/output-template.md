# Output Templates

**Purpose**: Standard SUCCESS/FAILURE output structures

---

## SUCCESS Response

### Query Construction Result

```json
{
  "status": "SUCCESS",
  "agent": "loki-query-specialist",
  "task_id": "lqs-20251110-001",
  "operation_type": "construct_query",
  "summary": "Constructed LogQL query for 5xx error extraction with json parser.",
  "confidence": 0.92,
  "execution_timestamp": "2025-11-10T10:30:00Z",
  "agent_specific_output": {
    "query_construction_result": {
      "constructed_query": "{service_name=\"api\"} |= \"error\" | json | status >= 500",
      "parser_used": "json",
      "parser_selection_rationale": "Log format is JSON; json parser is 100x faster than regexp (Grafana benchmark)",
      "extraction_strategy": "Filter for 'error' first (2-5x speedup), then parse JSON, filter by status code",
      "test_results": {
        "query_valid": true,
        "sample_results": ["status=503 endpoint=/api/users", "status=500 endpoint=/api/auth"],
        "result_count": 42
      },
      "anti_patterns_detected": []
    }
  }
}
```

### Format Analysis Result

```json
{
  "status": "SUCCESS",
  "agent": "loki-query-specialist",
  "operation_type": "analyze_format",
  "confidence": 0.88,
  "agent_specific_output": {
    "format_analysis": {
      "current_format": "logfmt",
      "parsing_difficulty": "easy",
      "recommended_parser": "logfmt",
      "parser_performance_impact": "100x faster than regexp (Grafana benchmark)",
      "anti_patterns_detected": [],
      "format_improvements": []
    }
  }
}
```

### Log Quality Assessment Result

```json
{
  "status": "SUCCESS",
  "agent": "loki-query-specialist",
  "operation_type": "assess_log_quality",
  "confidence": 0.85,
  "agent_specific_output": {
    "log_quality_assessment": {
      "anti_patterns_detected": [
        {
          "category": "json_in_string",
          "severity": "high",
          "impact": "10x query slowdown (forces regexp instead of json parser)",
          "fix": "Emit proper JSON logs, use native json parser"
        }
      ],
      "cardinality_analysis": {
        "high_cardinality_labels": ["request_id"],
        "cardinality_ratios": {"request_id": 0.85}
      },
      "recommendations": [
        {
          "priority": "high",
          "issue": "JSON-in-String pattern",
          "fix": "Extract JSON fields at ingestion",
          "expected_improvement": "10x query speedup",
          "promtail_config": "..."
        }
      ]
    }
  }
}
```

---

## FAILURE Response

```json
{
  "status": "FAILURE",
  "agent": "loki-query-specialist",
  "task_id": "lqs-20251110-002",
  "operation_type": "construct_query",
  "summary": "Unable to construct query: Loki API connectivity failed.",
  "confidence": 0.95,
  "execution_timestamp": "2025-11-10T10:35:00Z",
  "failure_details": {
    "failure_type": "loki_connectivity_error",
    "reasons": [
      "Connection refused to http://loki-service:3100",
      "Timeout after 30 seconds"
    ],
    "recovery_suggestions": [
      "Verify Loki service is running: kubectl get pods -l app=loki",
      "Check network connectivity from query location",
      "Verify Loki endpoint URL is correct"
    ],
    "partial_results": {
      "format_classified": true,
      "parser_identified": "json",
      "query_partially_constructed": "{service_name=\"api\"} | json"
    },
    "endpoint_tested": "http://loki-service:3100"
  }
}
```

---

## Failure Types

| Type | Description | Recovery |
|------|-------------|----------|
| `loki_connectivity_error` | Cannot reach Loki API | Verify endpoint, check service |
| `invalid_input` | Missing required fields | Provide extraction_goal or query |
| `unsupported_log_format` | Cannot determine parser | Provide more samples, describe format |
| `query_execution_error` | Query failed at runtime | Check syntax, reduce time range |
| `parser_selection_error` | Cannot select parser | Provide clearer log sample |
| `validation_error` | Syntax validation failed | Fix indicated syntax errors |

---

## Required Fields (All Responses)

- `status`: "SUCCESS" or "FAILURE"
- `agent`: "loki-query-specialist"
- `task_id`: Unique identifier
- `operation_type`: One of 6 types
- `summary`: 1-3 sentence description
- `confidence`: 0-1 score
- `execution_timestamp`: ISO 8601 UTC
