# SCAMPER Optimization

Phase 8 workflow optimization for `/analyze-command`.

**Version**: 1.0.0 | **Last Updated**: 2025-12-21

---

## Purpose

Apply the SCAMPER creative thinking framework to optimize command workflows. SCAMPER provides a structured approach to identifying improvement opportunities.

---

## Trigger Conditions

Phase 8 executes when:

| Condition | Trigger |
|-----------|---------|
| Explicit flag | `--optimize` passed |
| Low score | `overall_score < 70` |
| High debt | `debt_classification == "Critical"` |
| User request | "optimize this command" in prompt |

---

## The 7 SCAMPER Techniques

### S - Substitute

**Question**: What can be replaced with something better?

**Apply to Commands**:
- Replace inefficient delegation patterns
- Substitute deprecated agents with newer alternatives
- Swap verbose error handling with reference patterns
- Replace inline documentation with external references

**Examples**:
| Current State | Substitution | Benefit |
|---------------|--------------|---------|
| Inline error codes | Reference to error-codes.md | 200+ token savings |
| Custom validation | Shared validation skill | Consistency, reuse |
| Manual timeout handling | Timeout wrapper pattern | Reliability |

**Scoring Weight**: Minimality 50%, Risk 25%, Maintainability 25%

---

### C - Combine

**Question**: What can be merged for efficiency?

**Apply to Commands**:
- Merge redundant workflow phases
- Batch sequential agent delegations
- Consolidate similar error codes
- Combine overlapping validation checks

**Examples**:
| Current State | Combination | Benefit |
|---------------|-------------|---------|
| P2a, P2b, P2c validations | Single P2 validation phase | Reduced complexity |
| 5 similar error handlers | Generic handler + specific cases | DRY principle |
| Sequential similar agents | Parallel batch delegation | 40% time reduction |

**Scoring Weight**: Minimality 45%, Risk 30%, Maintainability 25%

---

### A - Adapt

**Question**: What patterns from elsewhere can be applied?

**Apply to Commands**:
- Adopt patterns from high-scoring commands
- Apply industry best practices
- Adapt OODA patterns from framework docs
- Import successful error handling from similar commands

**Examples**:
| Pattern Source | Adaptation | Benefit |
|----------------|------------|---------|
| /implement pre-flight | Add validation phase | Fewer runtime errors |
| /git delegation batching | Parallel agent launch | Performance |
| OODA from frameworks.md | Phase structure alignment | Consistency |

**Scoring Weight**: Minimality 35%, Risk 35%, Maintainability 30%

---

### M - Modify

**Question**: What can be changed in scale or structure?

**Apply to Commands**:
- Adjust phase granularity (more/fewer phases)
- Change delegation depth (more/less nesting)
- Modify timeout values for reliability
- Scale error handling coverage up/down

**Examples**:
| Current State | Modification | Benefit |
|---------------|--------------|---------|
| 12 fine-grained phases | 6 consolidated phases | Simpler flow |
| 30s timeout | 60s timeout | Reliability for slow agents |
| Minimal error handling | Comprehensive coverage | Production-ready |

**Scoring Weight**: Minimality 40%, Risk 40%, Maintainability 20%

---

### P - Put to Other Uses

**Question**: What can be extracted for reuse?

**Apply to Commands**:
- Extract reusable components to skills
- Create shared templates from patterns
- Build reusable validation modules
- Generalize specific logic for other commands

**Examples**:
| Specific Component | Reusable Form | Consumers |
|--------------------|---------------|-----------|
| Input validation logic | `validate-command-input` skill | All commands |
| Report generation | Report template | /analyze-*, /review-* |
| Agent health check | Pre-flight skill | Multi-agent commands |

**Scoring Weight**: Minimality 30%, Risk 35%, Maintainability 35%

---

### E - Eliminate

**Question**: What can be removed without loss?

**Apply to Commands**:
- Remove redundant validation steps
- Eliminate unused error codes
- Delete deprecated delegation patterns
- Remove over-documentation

**Examples**:
| Elimination Target | Rationale | Token Savings |
|--------------------|-----------|---------------|
| Duplicate validation in P0 and P1 | Redundant | 150 tokens |
| Unused error codes | Dead code | 100 tokens |
| Verbose explanatory comments | Not needed at runtime | 300 tokens |
| Legacy fallback paths | No longer triggered | 200 tokens |

**Scoring Weight**: Minimality 50%, Risk 30%, Maintainability 20%

---

### R - Reverse/Rearrange

**Question**: What order or structure can be changed?

**Apply to Commands**:
- Reorder phases for earlier failure detection
- Parallelize sequential operations
- Reverse dependency direction
- Restructure delegation hierarchy

**Examples**:
| Current Order | Rearrangement | Benefit |
|---------------|---------------|---------|
| Validate after process | Validate before process | Fail fast |
| Sequential agents | Parallel agents | 60% faster |
| Top-down delegation | Bottom-up aggregation | Better synthesis |

**Scoring Weight**: Minimality 35%, Risk 40%, Maintainability 25%

---

## Scoring Formula

Each SCAMPER recommendation is scored:

```
composite_score = (minimality x 0.40) + (risk x 0.35) + (maintainability x 0.25)
```

### Component Definitions

| Component | Description | Scoring |
|-----------|-------------|---------|
| **Minimality** | Does it reduce complexity? | 1.0 = significant reduction, 0.0 = adds complexity |
| **Risk** | What's the implementation risk? | 1.0 = low risk, 0.0 = high risk (inverted) |
| **Maintainability** | Does it improve long-term maintenance? | 1.0 = major improvement, 0.0 = harder to maintain |

### Priority Assignment

| Composite Score | Priority | Action |
|-----------------|----------|--------|
| >= 0.75 | P1 (High Value) | Implement immediately |
| 0.50 - 0.74 | P2 (Medium Value) | Plan for next iteration |
| 0.25 - 0.49 | P3 (Low Value) | Consider when convenient |
| < 0.25 | Skip | Not worth the effort |

---

## Quick Reference: Technique Selection

| Symptom | Best Technique |
|---------|----------------|
| Token bloat | E (Eliminate), C (Combine) |
| Slow execution | C (Combine), R (Reverse) |
| Duplicate logic | C (Combine), P (Put to other uses) |
| Outdated patterns | S (Substitute), A (Adapt) |
| Over-complexity | E (Eliminate), M (Modify) |
| Poor reusability | P (Put to other uses) |
| Suboptimal flow | R (Reverse), M (Modify) |

---

## Execution Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Expected Duration | 3-5 minutes | After P6 report generation |
| Timeout | 300 seconds | Hard limit |
| Retry on Timeout | None | Optional phase, skip if fails |
| Minimum Recommendations | 0 | Empty = already optimized |
| Maximum Recommendations | 15 | Prioritize, don't overwhelm |

---

## Related Documentation

- `workflow-phases.md` - Phase 8 overview
- `.claude/docs/00-core/frameworks/README.md` - SCAMPER framework details
- `delegation-patterns.md` - Task() syntax for P8
