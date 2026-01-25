# Example 1: Research on Async Validation

**Scenario**: User asks "Research async validation patterns in Pydantic v2"

## Agent Findings

```yaml
researcher-external:
  - 'Use async validators with @field_validator decorator'
  - 'Implement async model validation with validate() method'
  - 'Pydantic v2 recommends async validators for I/O operations'
  - 'Use model_validator for complex async validation'

researcher-codebase:
  - 'Current codebase uses sync validators - need migration'
  - 'Refactor validators to async for DB lookups'
```

## Without Synthesis (Current Behavior)

```markdown
Findings from 3 agents:

researcher-external suggests:

- Use async validators with @field_validator
- Implement async validation with validate()
- Use async validators for I/O
- Use model_validator for complex cases

researcher-codebase suggests:

- Current codebase needs migration
- Refactor validators to async

→ User sees 6 overlapping suggestions, unclear which to implement
```

## With Synthesis Framework

```markdown
## Problem: Async Validation Implementation Strategy

**Identified By**: researcher-external, researcher-codebase
**Problem Domain**: Architecture + Performance
**Location**: packages/core/validators.py

---

### Solutions Analysis

#### Solution 1: Incremental Migration with @field_validator ⭐ RECOMMENDED

**Proposed By**: researcher-external
**Score**: 1.33

**Approach**: Start with @field_validator for individual fields with I/O, migrate to model_validator for complex cases later.

**Trade-offs**:

- **Impact**: 4/5 - Enables async DB lookups, improves performance
- **Effort**: 2/5 - Incremental migration, 2-3 days
- **Risk**: Low - Proven pattern, gradual rollout
- **Change Scope**: Localized - Individual validators

**Pros**:

- Incremental migration (low risk)
- Official Pydantic v2 pattern
- Backward compatible (sync validators still work)
- Clear upgrade path

**Cons**:

- Partial async (not all validators migrated immediately)
- Mixed sync/async during transition

---

#### Solution 2: Full Refactor with model_validator

**Proposed By**: researcher-codebase
**Score**: 0.50

**Approach**: Refactor all validators to use async model_validator for centralized validation logic.

**Trade-offs**:

- **Impact**: 3/5 - Centralized validation, but complex migration
- **Effort**: 4/5 - Full refactor, 1-2 weeks
- **Risk**: Medium - Big bang migration, testing burden
- **Change Scope**: Module - All validators

**Pros**:

- Centralized validation logic
- Complex validation patterns supported
- Complete async solution

**Cons**:

- Higher risk (big bang migration)
- Significant effort (2 weeks+)
- All-or-nothing approach
- Blocks other development

**Why Not Recommended**: Much higher effort for marginal benefit over incremental approach. Increases risk with big bang migration.

---

### Recommendation: ✅ Solution 1 (Incremental @field_validator)

**Rationale**:
Score 1.33 vs 0.50 due to lower risk and effort while achieving similar impact. Incremental approach allows validation during migration and provides clear rollback points. Start with high-value I/O validators (user lookups, external APIs) then expand to complex cases if needed.

**Implementation Priority**: This Sprint

**Discarded Solutions**:

- **Solution 2 (Full Refactor)**: Overengineered for immediate needs, high risk
```
