# Repository Analyst Delegation Examples

## Example 1: Full Repository Inventory

### Orchestrator Delegation
```
Task(repository-analyst, "Generate full component inventory for documentation audit")
```

### Expected Response
```json
{
  "status": "SUCCESS",
  "agent": "repository-analyst",
  "confidence": 1.0,
  "agent_specific_output": {
    "analysis_summary": {
      "total_components": 58,
      "component_breakdown": {
        "agents": 38,
        "commands": 12,
        "hooks": 8,
        "skills": 0
      },
      "analysis_duration_seconds": 16
    },
    "statistics": {
      "health_score": 95,
      "ooda_distribution": {
        "OBSERVE": 8,
        "ORIENT": 14,
        "DECIDE": 6,
        "ACT": 10
      }
    }
  }
}
```

---

## Example 2: Pre-Agent-Creation Validation

### Orchestrator Delegation
```
Task(repository-analyst, "Check for agents similar to 'log-analyzer' in observability domain")
```

### Expected Response
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "top_matches": [
      {
        "name": "loki-query-specialist",
        "similarity_score": 0.72,
        "domain": "observability",
        "overlap": ["log analysis", "Read/Grep/Bash tools"]
      },
      {
        "name": "debugger",
        "similarity_score": 0.45,
        "domain": "packages/**"
      }
    ],
    "recommendation": {
      "action": "EXTEND_EXISTING",
      "target": "loki-query-specialist",
      "rationale": "High similarity (0.72), same domain"
    }
  }
}
```

---

## Example 3: Validation Check

### Orchestrator Delegation
```
Task(repository-analyst, "Validate naming conventions for all components")
```

### Expected Response
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "validation_results": {
      "naming_violations": [],
      "missing_files": [],
      "broken_references": []
    },
    "statistics": {
      "components_checked": 58,
      "violations_found": 0,
      "health_score": 100
    }
  }
}
```
