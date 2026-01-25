# Phase 1: OBSERVE - HDD Enforcement and Input Validation

**OODA Stage**: OBSERVE | **Time Allocation**: 10-15%

**Purpose**: Enforce Hypothesis-Driven Development protocol, validate hypothesis_id, check trial budget

**Deliverable**: Validated request with HDD compliance status

---

## HDD Enforcement Protocol (MANDATORY)

### Step 1.1: Require hypothesis_id

**Input**: Backtest request from orchestrator or user

**Process**:
```
1. REQUIRE hypothesis_id
   - IF missing: HALT "Cannot backtest without hypothesis_id"
   - IF malformed: REJECT with format requirements
```

**Validation**:
- hypothesis_id must match pattern: `HYP-[0-9]{3,5}`
- Must exist in hypothesis-tracking registry

**Output**: Validated hypothesis_id or HALT

---

### Step 1.2: Check Trial Budget

**Input**: hypothesis_id from Step 1.1

**Process**:
```
2. CHECK trial_number
   - IF trial_number > 5: HALT "Maximum trials exceeded"
   - IF trial_number > 3: WARN "Trial budget low (remaining: {5 - trial_number})"
   - IF trial_number <= 3: PROCEED
```

**Trial Budget Table**:

| trial_number | Status | Action |
|--------------|--------|--------|
| 1-3 | GREEN | Proceed normally |
| 4 | YELLOW | Warn: 1 trial remaining after this |
| 5 | ORANGE | Final trial - no retries possible |
| >5 | RED | HALT - hypothesis exhausted |

**Output**: Trial status with remaining budget

---

### Step 1.3: Validate Input Parameters

**Input**: Backtest request parameters

**Required Fields**:
- `hypothesis_id` (validated in 1.1)
- `strategy_spec` (from strategy-builder)
- `backtest_params`:
  - `start_date` (ISO 8601)
  - `end_date` (ISO 8601)
  - `initial_capital` (positive number)

**Optional Fields**:
- `regime_config` (for regime-stratified testing)
- `tier` (1-4, for tier_test mode)
- `algorithm_path` (path to algorithm folder)

**Validation Checks**:
- `start_date` < `end_date`
- `initial_capital` > 0
- `strategy_spec` validates against strategy-specification schema
- Date range >= 252 trading days (1 year minimum)

**Output**: Validation status (PASS/FAIL with specific issues)

---

## Exit Criteria

**All criteria must pass to proceed to ORIENT**:

| Criterion | Check | On Failure |
|-----------|-------|------------|
| hypothesis_id present | Non-empty, valid format | HALT immediately |
| Trial budget available | trial_number <= 5 | HALT with exhaustion message |
| Required params present | All fields validated | REJECT with missing fields |
| Date range valid | start < end, >= 252 days | REJECT with requirements |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Proceeding without hypothesis_id | ALWAYS halt - no exceptions |
| Ignoring trial count | Check BEFORE any execution |
| Accepting invalid date ranges | Enforce 252-day minimum |

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
