# Problem Statement & Requirements Report

> **Feature**: [Feature Name]
> **Author**: [Name]
> **Date**: [YYYY-MM-DD]
> **Status**: Draft | Review | Approved

---

## 1. Problem Statement

**One-sentence summary**:
[Clear, concise statement of the core problem being solved]

**Executive Summary**:
[2-3 sentences explaining the business/technical problem, who it affects, and why it matters now]

---

## 2. Inputs, Outputs & Side Effects

| Category | Description | Format/Type | Source/Destination |
|----------|-------------|-------------|-------------------|
| **Input** | [What data comes in] | [JSON, etc.] | [User, API, DB] |
| **Output** | [What is produced] | [Format] | [Where it goes] |
| **Side Effect** | [State changes] | [Type] | [System affected] |


---

## 3. Constraints Matrix

### Performance
| Metric | Target | Notes |
|--------|--------|-------|
| Latency (p95) | [e.g., <200ms] | [Context] |
| Throughput | [e.g., 1000 QPS] | [Peak vs sustained] |
| Availability | [e.g., 99.9%] | [SLA requirement] |

### Reliability
| Requirement | Value | Rationale |
|-------------|-------|-----------|
| Idempotency | [Required/Optional] | [Why] |
| Consistency | [Strong/Eventual] | [Trade-offs] |
| Atomicity | [Full/Partial] | [Failure behavior] |

### Compliance
| Standard | Requirement | Impact |
|----------|-------------|--------|
| [e.g., GDPR] | [Specific need] | [Implementation impact] |

### Resources
| Resource | Limit | Notes |
|----------|-------|-------|
| Memory | [e.g., 512MB] | [Per instance] |
| Timeout | [e.g., 30s] | [Request budget] |


---

## 4. Edge Cases

| # | Scenario | Input Condition | Expected Behavior | Priority |
|---|----------|-----------------|-------------------|----------|
| 1 | Empty input | null/empty array | Return 400 with error message | High |
| 2 | Duplicate request | Same idempotency key | Return cached result | High |
| 3 | Invalid format | Malformed JSON | Return 400 with validation errors | Medium |
| 4 | Out of range | Negative values | Reject with specific error | Medium |
| 5 | Concurrent access | Race condition | Handle via locking strategy | High |
| 6 | [Additional case] | [Condition] | [Behavior] | [Priority] |

---

## 5. Success Criteria

- [ ] [Measurable criterion 1 - e.g., "Error rate drops from 2% to <0.1%"]
- [ ] [Measurable criterion 2 - e.g., "p95 latency remains <200ms"]
- [ ] [Measurable criterion 3 - e.g., "Zero duplicate transactions"]
- [ ] [Measurable criterion 4 - e.g., "All edge cases have test coverage"]

---

## 6. Integration Points

```
[Client/User]
     |
     v
[This Feature] -----> [Dependency 1: e.g., Database]
     |
     +--------------> [Dependency 2: e.g., External API]
     |
     +--------------> [Dependency 3: e.g., Cache]
```

| Dependency | Type | SLA | Failure Mode |
|------------|------|-----|--------------|
| [Service] | [Sync/Async] | [Uptime %] | [Behavior on failure] |

---

## 7. Open Questions

- [ ] [Question 1 that needs stakeholder input]
- [ ] [Question 2 about requirements ambiguity]
- [ ] [Assumption that needs validation]

---

**Phase 1 Checklist**:
- [ ] Problem expressible in one sentence
- [ ] Inputs, outputs, side effects defined
- [ ] All constraints explicit
- [ ] 5+ edge cases documented
- [ ] Success criteria measurable
- [ ] Integration dependencies mapped
