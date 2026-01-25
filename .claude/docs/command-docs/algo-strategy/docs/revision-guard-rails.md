# Revision Guard Rails

**Purpose**: Enforce HDD discipline, prevent parameter p-hacking during strategy revision.

**When to Reference**: After backtest fails | Parameter changes proposed | Routing to revision path | Archiving hypotheses

---

## Core Principle

> **Parameters are LOCKED once a hypothesis is formed.** Changing parameters after seeing results is p-hacking.

Legitimate parameter changes require: NEW hypothesis + NEW rationale = reset trial counter

---

## Revision Taxonomy (4 Paths)

| Path | Condition | Action | Hypothesis ID |
|------|-----------|--------|---------------|
| **1. Code Bug** | Implementation error detected | Fix code, retry | SAME (no reset) |
| **2. Regime Failure** | Failed only in specific period | Add regime filter | NEW (reset counter) |
| **3. Invalid Theory** | Failed randomly across periods | Archive to graveyard | NEW (reset counter) |
| **4. Insufficient Sample** | <100 trades generated | Extend timeframe | SAME (no reset) |

### Detection Signals

| Path | Signal |
|------|--------|
| Code Bug | Exception traces, NaN values, logic errors |
| Regime Failure | >60% drawdown in crisis (2008, COVID, dot-com) |
| Invalid Theory | No regime correlation, consistent negative expectancy |
| Insufficient Sample | `trade_count < 100` |


---

## Parameter Lock Enforcement

```python
def validate_revision_request(
    original_hypothesis: HypothesisBundle,
    proposed_revision: HypothesisBundle
) -> RevisionValidation:
    # Detect parameter changes
    param_changes = []
    for param_name in original_hypothesis.params_locked:
        old_val = original_hypothesis.params_locked[param_name]["value"]
        new_val = proposed_revision.params_locked.get(param_name, {}).get("value")
        if old_val != new_val:
            param_changes.append({"param": param_name, "old": old_val, "new": new_val})
    
    # BLOCK: Parameters changed without new hypothesis_id
    if param_changes and proposed_revision.hypothesis_id == original_hypothesis.hypothesis_id:
        return RevisionValidation(
            valid=False,
            error="PARAM_CHANGE_BLOCKED",
            message=f"Parameters {[p['param'] for p in param_changes]} are LOCKED.",
            blocked_changes=param_changes
        )
    
    # ALLOW: New hypothesis_id (archives old, resets counter)
    if proposed_revision.hypothesis_id != original_hypothesis.hypothesis_id:
        return RevisionValidation(valid=True, previous_hypothesis_archived=True)
    
    # ALLOW: Same ID, no param changes (code fix or sample extension)
    return RevisionValidation(valid=True, trial_counter_unchanged=True)
```

---

## User-Facing Block Messages

### Parameter Modification Blocked

```
PARAMETER MODIFICATION BLOCKED

You attempted to change RSI(14) -> RSI(13).

RSI period is LOCKED under hypothesis HYP-001. The HDD methodology
prohibits parameter changes after seeing backtest results.

YOUR OPTIONS:
1. CONTINUE with RSI(14) - extend timeframe or add regime filter
   Command: /algo-strategy --continue HYP-001

2. CREATE NEW HYPOTHESIS - explain WHY RSI(13) has different rationale
   This archives HYP-001 and creates HYP-002 (trial counter resets)
   Command: /algo-strategy --revise "RSI(13) because [NEW RATIONALE]..."
```

### Regime Failure Detected

```
REGIME FAILURE DETECTED

Hypothesis HYP-001 failed primarily during: 2008 Financial Crisis

Performance: Overall Sharpe 0.45 (FAIL) | Excluding 2008: 1.85 (PASS)
Drawdown concentration: 78% in Q3-Q4 2008

RECOMMENDED: Add regime filter (requires NEW hypothesis)
Command: /algo-strategy --regime-filter "Exclude VIX > 40 periods"
         Creates: HYP-002 (archives HYP-001)
```

---

## Hypothesis Graveyard


**Purpose**: Archive rejected hypotheses to prevent re-testing, document learning, provide audit trail.

### What Gets Archived

| Trigger | Example |
|---------|---------|
| Path 3 (Invalid Theory) | "EMA crossover on SPY has no edge" |
| New hypothesis created | "RSI(14) replaced by RSI(13) with new rationale" |
| Trial limit exceeded (30) | "Exhausted optimization budget" |
| User explicit abandon | "Abandoning due to changed conditions" |

### Entry Format

```
HYPOTHESIS GRAVEYARD ENTRY
--------------------------
ID: HYP-001 | Created: 2024-01-15 | Archived: 2024-01-22 | Trials: 12

HYPOTHESIS: "RSI(14) crossing above 30 on SPY indicates oversold bounce"

REJECTION: Path 3 - Invalid Theory
Failed randomly across all market regimes (2010-2023)
Final Sharpe: 0.23 | Win Rate: 48% | Expectancy: -0.02%

LEARNINGS:
- RSI(14) on daily SPY lacks predictive power
- Signal frequency too low for statistical significance
```

### Storage

```
.claude/data/hypothesis-graveyard/
  ├── HYP-001.json
  ├── HYP-002.json
  └── index.json
```

---

## Integration with /algo-strategy


### P6 Routing Logic

When P6 receives a failed backtest, it routes based on the taxonomy:

| Path | Route Action | Hypothesis ID | Counter |
|------|--------------|---------------|---------|
| Code Bug | `FIX_CODE` | Same | Unchanged |
| Regime Failure | `ADD_REGIME_FILTER` | New (generated) | Reset |
| Invalid Theory | `ARCHIVE` | Archived | N/A |
| Insufficient Sample | `EXTEND_TIMEFRAME` | Same | Unchanged |

### User Request Interception

Guard rails intercept BEFORE processing any revision request:

```python
def intercept_revision_request(hypothesis: HypothesisBundle, user_input: str) -> InterceptionResult:
    proposed_changes = parse_parameter_changes(user_input)
    if proposed_changes:
        return InterceptionResult(
            blocked=True,
            reason="PARAM_CHANGE_DETECTED",
            display_message=generate_block_message(hypothesis, proposed_changes),
            options=["Continue with current parameters", "Create new hypothesis"]
        )
    return InterceptionResult(blocked=False)
```

---

## Summary

| Scenario | Allowed? | Hypothesis ID | Trial Counter |
|----------|----------|---------------|---------------|
| Fix code bug | YES | Same | Unchanged |
| Extend timeframe | YES | Same | Unchanged |
| Change parameter (same ID) | **NO** | Blocked | N/A |
| Change parameter (new ID + rationale) | YES | New | Reset to 0 |
| Add regime filter | YES | New | Reset to 0 |
| Archive failed theory | YES | Archived | N/A |

---

**Related**: [HDD Methodology](./hdd-methodology.md) | [Anti-Overfit Gates](./anti-overfit-gates.md) | [Workflow Phases](./workflow-phases.md)
