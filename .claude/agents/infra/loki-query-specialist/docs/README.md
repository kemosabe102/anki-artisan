# docs/ Directory

**Purpose**: Externalized domain knowledge for loki-query-specialist

---

## Contents

| File | Purpose | When to Consult |
|------|---------|-----------------|
| `domain-expertise.md` | OTLP format, Gauntlet-Agents specifics | ALL queries against gauntlet-agents namespace |
| `anti-pattern-detection-guide.md` | 9 anti-patterns with detection and remediation | Log quality assessment, performance issues |
| `api-validation-workflow.md` | Loki HTTP API, 5-step validation | Query testing, syntax validation |
| `format-improvement-strategies.md` | Migration approaches, Promtail configs | Format recommendations |
| `high-cardinality-management.md` | Cardinality thresholds, structured_metadata | Stream explosion, cost issues |
| `logql-syntax-reference.md` | LogQL grammar, operators, examples | Query construction |
| `loki-architecture-constraints.md` | Limits, configuration, timeouts | Query failures, performance |
| `parser-selection-guide.md` | Parser hierarchy, decision tree | Parser selection |
| `query-optimization-patterns.md` | Performance frameworks, benchmarks | Query optimization |

---

## Key Concepts

### OTLP Format (Critical)

Gauntlet Agents uses OpenTelemetry OTLP format:
- **Body**: Plain text message
- **Attributes**: Structured data as separate indexed labels
- **Never use `| json`** on OTLP logs - access attributes directly

See `domain-expertise.md` for complete OTLP reference.

### Anti-Pattern Detection

10 categories with detection methods and remediation:
1. JSON-in-String, 2. High-Cardinality Labels, 3. Label Explosion,
4. Mixed Formats, 5. Label vs Field Confusion, 6. Parsing Before Filtering,
7. Regex for Simple Patterns, 8. Unstructured Critical Logs,
9. TSV Without Parsing, 10. JSON Parser on OTLP

See `anti-pattern-detection-guide.md` for complete catalog.

---

## See Also

- **Examples**: `../examples/` for delegation and output patterns
- **Schema**: `../schemas/loki-query-specialist.schema.json`
