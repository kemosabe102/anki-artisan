# Delegation Examples

## MODE: detect

### Basic Invocation

```markdown
Task(integration-boundary-reviewer, prompt="MODE: detect
Feature: packages/alpha-phase-01/")
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "agent": "feature-final-review",
  "mode": "detect",
  "feature": "packages/alpha-phase-01",
  "total_pairs": 3,
  "integration_pairs": [
    {
      "id": 1,
      "upstream": "PerplexityProvider",
      "downstream": "Normalizer",
      "upstream_file": "packages/connectors/perplexity_provider.py",
      "downstream_file": "packages/processing/normalizer.py",
      "data_flow_type": "direct",
      "confidence": 0.92,
      "evidence": ["ARCHITECTURE.md line 45", "import in normalizer.py:12"]
    }
  ]
}
```

---

## MODE: review

### Basic Invocation

```markdown
Task(integration-boundary-reviewer, prompt="MODE: review
Pair: {
  \"id\": 1,
  \"upstream\": \"PerplexityProvider\",
  \"downstream\": \"Normalizer\",
  \"upstream_file\": \"packages/connectors/perplexity_provider.py\",
  \"downstream_file\": \"packages/processing/normalizer.py\",
  \"data_flow_type\": \"direct\"
}")
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "agent": "feature-final-review",
  "mode": "review",
  "pair_id": 1,
  "upstream": "PerplexityProvider",
  "downstream": "Normalizer",
  "gate_status": "PASS_WITH_CONDITIONS",
  "confidence": 0.85,
  "pair_findings": [
    {
      "id": "INT-001",
      "category": "error_propagation",
      "severity": "MEDIUM",
      "confidence": 0.85,
      "issue": "RateLimitError not caught in downstream",
      "evidence": "perplexity_provider.py:78 raises, normalizer.py:34 no catch",
      "recommendation": "Add try/except in Normalizer.process()"
    }
  ],
  "checklist_scores": {
    "contract_alignment": "PASS",
    "schema_compatibility": "PASS",
    "null_handling": "PASS",
    "error_propagation": "FAIL",
    "edge_cases": "PARTIAL",
    "performance": "PASS"
  },
  "test_coverage": {
    "status": "PARTIAL",
    "test_file": "tests/integration/test_providers.py",
    "missing_scenarios": ["error_handling", "empty_response"]
  }
}
```

---

## Chained Workflow Example

First detect pairs, then review each:

```markdown
# Step 1: Detect all pairs
Task(integration-boundary-reviewer, prompt="MODE: detect
Feature: packages/alpha-phase-01/")

# Step 2: Review each pair (parallel)
Task(integration-boundary-reviewer, prompt="MODE: review
Pair: {pair_1_json}")

Task(integration-boundary-reviewer, prompt="MODE: review
Pair: {pair_2_json}")

Task(integration-boundary-reviewer, prompt="MODE: review
Pair: {pair_3_json}")
```

## Failure Example

### Input with Missing Feature

```markdown
Task(integration-boundary-reviewer, prompt="MODE: detect
Feature: packages/nonexistent/")
```

### Expected Failure Output

```json
{
  "status": "FAILURE",
  "agent": "feature-final-review",
  "mode": "detect",
  "failure_details": {
    "failure_type": "feature_not_found",
    "error_message": "Directory not found: packages/nonexistent/",
    "recovery_suggestions": [
      "Verify feature path exists",
      "Check for typos in directory name",
      "Use Glob to discover available feature directories"
    ]
  }
}
```
