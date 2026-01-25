# Integration Checklist

**Purpose**: Per-pair review criteria for integration boundaries.

---

## Checklist Categories

| Category | Description | Severity if Failed |
|----------|-------------|-------------------|
| Contract Alignment | Type compatibility | CRITICAL |
| Schema Compatibility | Field matching | HIGH |
| Null/Optional Handling | None handling | HIGH |
| Error Propagation | Exception flow | MEDIUM |
| Edge Cases | Boundary conditions | MEDIUM |
| Performance | Efficiency at boundary | LOW |

---

## 1. Contract Alignment (CRITICAL)

### What to Check
- Output type of upstream == Input type of downstream
- Required fields are present
- No implicit type coercion that could fail

### Evidence to Collect
```python
# Upstream return type
def fetch(self) -> list[Document]:  # Returns list[Document]

# Downstream parameter type
def process(self, docs: list[Document]):  # Expects list[Document]
```

### Pass Criteria
- Types match exactly OR
- Types are compatible (subclass, Protocol implementation)

### Fail Indicators
- Type mismatch (e.g., `str` vs `int`)
- Missing required field in dataclass
- Incompatible generic types (e.g., `list` vs `dict`)

---

## 2. Schema Compatibility (HIGH)

### What to Check
- Field names match between shared models
- Field types are compatible
- Optional vs required alignment

### Evidence to Collect
```python
# Upstream produces
@dataclass
class Document:
    id: str
    content: str
    timestamp: datetime

# Downstream expects
@dataclass
class Document:
    id: str
    content: str
    timestamp: datetime  # Must match
    metadata: dict = field(default_factory=dict)  # Optional OK
```

### Pass Criteria
- All required fields present
- Types compatible for each field
- Defaults provided for new optional fields

### Fail Indicators
- Missing required field
- Field type mismatch
- Field name typo (case sensitivity)

---

## 3. Null/Optional Handling (HIGH)

### What to Check
- Upstream can return None → Downstream handles None
- Optional fields → Downstream doesn't assume present
- Empty collections → Downstream handles empty case

### Evidence to Collect
```python
# Upstream
def fetch(self) -> Document | None:  # Can return None
    if not data:
        return None

# Downstream
def process(self, doc: Document | None):
    if doc is None:  # Must check
        return default_result
```

### Pass Criteria
- All None returns handled
- Optional unwrapping with defaults
- Empty collection guards present

### Fail Indicators
- No None check before attribute access
- Assuming list has elements without check
- Missing `or default` patterns

---

## 4. Error Propagation (MEDIUM)

### What to Check
- Upstream exceptions documented
- Downstream catches OR propagates appropriately
- Error context preserved

### Evidence to Collect
```python
# Upstream raises
class Provider:
    def fetch(self):
        raise RateLimitError("API quota exceeded")  # Custom exception

# Downstream should handle
class Normalizer:
    def process(self):
        try:
            data = provider.fetch()
        except RateLimitError:
            logger.warning("Rate limited, using cache")
            return cached_data
```

### Pass Criteria
- Known exceptions caught or documented as propagated
- Error context logged/preserved
- Recovery path exists for transient errors

### Fail Indicators
- Bare `except:` clauses swallowing errors
- No logging of caught exceptions
- Critical exceptions not handled

---

## 5. Edge Cases (MEDIUM)

### What to Check
- Empty input handling
- Boundary values (0, max, min)
- Unicode/special characters
- Concurrent access patterns

### Common Edge Cases
| Case | Upstream Output | Downstream Should Handle |
|------|-----------------|-------------------------|
| Empty | `[]` | Return empty, not error |
| Single | `[item]` | Process normally |
| Large | `[10000 items]` | Batch or stream |
| Zero | `count=0` | Valid, not error |
| Negative | `-1` (if possible) | Validate or reject |

### Pass Criteria
- Empty collections handled gracefully
- Zero values don't cause division errors
- Large inputs don't cause OOM

### Fail Indicators
- Index access without length check
- Division without zero check
- Unbounded memory allocation

---

## 6. Performance (LOW)

### What to Check
- N+1 query patterns at boundary
- Unnecessary data copying
- Blocking calls in async context
- Memory allocation patterns

### Evidence to Collect
```python
# BAD: N+1 pattern
for doc in documents:
    details = db.fetch_details(doc.id)  # Query per item

# GOOD: Batch query
doc_ids = [d.id for d in documents]
details_map = db.fetch_details_batch(doc_ids)  # Single query
```

### Pass Criteria
- Batch operations where possible
- Streaming for large data
- Async preserved across boundary

### Fail Indicators
- Loop with database call inside
- Full collection copy when slice would work
- Sync call blocking async context

---

## Scoring

### Per-Category Scores
- **PASS**: All criteria met
- **PARTIAL**: Some criteria met, minor gaps
- **FAIL**: Critical criteria not met

### Overall Pair Status
```
if any category == FAIL and category.severity in [CRITICAL, HIGH]:
    pair_status = "FAIL"
elif any category == FAIL:
    pair_status = "PASS_WITH_CONDITIONS"
elif any category == PARTIAL:
    pair_status = "PASS_WITH_CONDITIONS"
else:
    pair_status = "PASS"
```

---

## 7. Reliability (Four Hats)

**Delegate to**: `reliability-reviewer` agent

The reliability-reviewer applies Four Hats analysis at integration boundaries:

### Graph Theorist (Edge Reliability)
- Timeout budgets on cross-component calls
- Race condition guards (mutex, semaphores)
- Backpressure mechanism (queue limits, flow control)
- Idempotency for retries

**Skills**: `edge-reliability` → `system-edge-checklist.md`, `monolith-edge-checklist.md`

### Lawyer (Node Reliability)
- Precondition validation at entry points (fail fast)
- Postcondition guarantees on outputs
- Resource bound enforcement (bounded allocations)
- Class invariants enforced

**Skills**: `node-reliability` → `invariant-checklist.md`, `resource-bound-checklist.md`

### Operator (Observability)
- "Why" logs at failure points (not just "what")
- Metrics for new queues/APIs
- Kill switch / feature flag capability

**Skills**: `operational-reliability` → `observability-checklist.md`

### Historian (Maintainability)
- Cognitive load assessment (readable in one pass)
- Dependency hygiene (minimal coupling)

**Skills**: `operational-reliability` → `maintainability-checklist.md`

### Severity Mapping
| Check | Severity |
|-------|----------|
| Timeout < upstream timeout | HIGH |
| Race condition guards | CRITICAL |
| Precondition validation | HIGH |
| Bounded allocations | CRITICAL |
| "Why" logs | MEDIUM |
| Cognitive load | LOW |

---

## Scoring

### Per-Category Scores
- **PASS**: All criteria met
- **PARTIAL**: Some criteria met, minor gaps
- **FAIL**: Critical criteria not met

### Overall Pair Status
```
if any category == FAIL and category.severity in [CRITICAL, HIGH]:
    pair_status = "FAIL"
elif any category == FAIL:
    pair_status = "PASS_WITH_CONDITIONS"
elif any category == PARTIAL:
    pair_status = "PASS_WITH_CONDITIONS"
else:
    pair_status = "PASS"
```

---

## Output Format

```json
{
  "checklist_scores": {
    "contract_alignment": "PASS",
    "schema_compatibility": "PASS",
    "null_handling": "PARTIAL",
    "error_propagation": "FAIL",
    "edge_cases": "PASS",
    "performance": "PASS",
    "reliability": "PASS"
  },
  "failed_checks": [
    {
      "category": "error_propagation",
      "issue": "RateLimitError not caught",
      "evidence": "normalizer.py:45 calls provider.fetch() without try/except",
      "severity": "MEDIUM"
    }
  ]
}
```
