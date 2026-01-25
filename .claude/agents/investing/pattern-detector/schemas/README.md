# Pattern Detector Schemas

JSON Schema definitions for pattern-detector agent input/output contracts.

| Schema | Purpose |
|--------|---------|
| `pattern-detector.schema.json` | SUCCESS/FAILURE response schema with pattern detections and evidence bundles |

## Schema Structure

Extends `base-agent.schema.json` with:
- `agent_specific_output`: Pattern detections, Fact objects, metadata
- `failure_details`: Data quality issues, missing indicators, recovery suggestions

## Output Format

**SUCCESS**: patterns_detected[], facts[], metadata (regime, context_quality, patterns_evaluated)

**FAILURE**: failure_type, reasons[], partial_results, recovery_suggestions[], next_steps
