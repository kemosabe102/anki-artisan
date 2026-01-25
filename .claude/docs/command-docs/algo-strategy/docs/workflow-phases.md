# Workflow Phases Reference

**Purpose**: Detailed reference for the 6-phase workflow in `/algo-strategy` command.

---

## Overview

| Phase | Name | OODA | Function | Gates |
|-------|------|------|----------|-------|
| P1 | PARSE | Observe | Input handling, mode detection | GATE 1: INPUT |
| P2 | HYPOTHESIS | Orient | HDD core, anti-overfit | GATE 2a/2b/2c |
| P3 | DATA_CHECK | Orient | Data validation | GATE 3: DATA |
| P4 | DELEGATE | Decide/Act | Strategy generation | - |
| P5 | VALIDATE | Act | Quality checks | GATE 5: CONSISTENCY |
| P6 | PRESENT/REVISE | Act | Output or revision routing | - |

**Critical Path**: P1 -> P2 -> P3 -> P4 -> P5 -> P6
**Blocking Gates**: P1, P2 (all), P5 | **Non-Blocking**: P3

---

## P1: PARSE - Input Handling

### Mode Detection
| User Input | Mode | Output |
|------------|------|--------|
| `/algo-strategy "description"` | `freeform` | spec + skeleton |
| `/algo-strategy --from-doc <path>` | `doc_first` | extract from docs |
| `--spec-only` | `spec_only` | JSON spec only |
| `--skeleton-only` | `skeleton_only` | QC Python only |
| `--hypothesis-only` | `hypothesis_only` | hypothesis bundle only |


### GATE 1: INPUT
**Type**: BLOCKING | **Error**: `ALGO_ERR_001`

Requires 7 strategy elements OR asks clarifying questions:

| Element | Example |
|---------|---------|
| Universe | SPY, QQQ, tech stocks |
| Entry Signal | EMA crossover, RSI oversold |
| Exit Signal | Trailing stop, profit target |
| Timeframe | 4-hour, daily |
| Position Sizing | 2% per trade |
| Risk Management | Stop loss at 2 ATR |
| Regime Filters | Price > 200DMA, volatility LOW/NORMAL |

```
IF elements_found < 7: ASK clarifying_questions, BLOCK
ELSE: PASS to P2
```

---

## P2: HYPOTHESIS - HDD Core + Anti-Overfit

### Hypothesis Formulation (Cause -> Effect -> Why)
**Template**: "I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]"

| Component | Good | Bad |
|-----------|------|-----|
| CAUSE | "EMA(20) crossing above EMA(50)" | "Market feels bullish" |
| EFFECT | "2-5% gains within 10 days" | "Stock goes up" |
| WHY | "Institutional entry levels" | "It worked before" |

### Parameter Locking
All parameters locked BEFORE first backtest with rationale:
```json
{"ema_fast": {"value": 20, "rationale": "Industry standard"}}
```


### GATE 2a: PARAM_COUNT
**Type**: BLOCKING | **Error**: `ALGO_ERR_004`
- **Threshold**: < 10 parameters
- **On Fail**: "OVERFIT RISK: Too many parameters. Reduce degrees of freedom."

### GATE 2b: PARAM_RANGES
**Type**: BLOCKING | **Error**: `ALGO_ERR_004`
- **Threshold**: No parameter range > 3x span (`(max-min)/min < 3`)
- **Violations**: `ema: 5-50` (10x) BLOCKED | `ema: 18-22` (0.22x) PASS

### GATE 2c: HYPOTHESIS
**Type**: BLOCKING | **Error**: `ALGO_ERR_002`
- Schema valid (`hypothesis-bundle.schema.json`)
- All parameters locked with rationale
- Testability score >= 0.7

**Testability Score**: cause_measurable(0.3) + effect_quantifiable(0.3) + timeframe_defined(0.2) + why_has_mechanism(0.2)

---

## P3: DATA_CHECK - Validation

### OHLCV Requirements
- **Symbols**: From universe (SPY, QQQ)
- **Date Range**: Backtest period
- **Resolution**: Bar size (1min, daily)
- **Adjustments**: Split/dividend adjusted

### Indicator Dependencies
| Indicator | Warmup Bars |
|-----------|-------------|
| EMA(200) | 200+ |
| ATR(14), RSI(14) | 14+ |
| MACD(12,26,9) | 35+ |


### Market-Data-Specialist Delegation
```
Task(market-data-specialist, "Validate OHLCV for {symbols} {start}-{end}")
```

### GATE 3: DATA
**Type**: NON-BLOCKING | **Error**: `ALGO_ERR_003` (if score < 0.5)

**Score Impact**:
| Condition | Impact |
|-----------|--------|
| OHLCV gaps < 5% | -0.05 |
| OHLCV gaps 5-20% | -0.15 |
| Missing indicator data | -0.10 |
| Insufficient history | -0.20 |

**If data_confidence < 0.8**: Show warnings, require user acknowledgment

---

## P4: DELEGATE - Strategy Generation

### Task Delegation
```
Task(strategy-builder, "MODE: {mode}. HYPOTHESIS_BUNDLE: {json}. Generate spec + skeleton.")
```

### Expected Output
- **JSON Specification**: Parameters, signals, risk rules
- **QC Python Skeleton**: Initialize/OnData methods

**Note**: Anti-overfit already enforced in P2 (not duplicated here).
**Error**: `ALGO_ERR_005` - Strategy generation failed

---

## P5: VALIDATE - Quality Checks

### Schema Validation
Validate spec against `strategy-spec.schema.json`. **Error**: `ALGO_ERR_006`


### Syntax Check (QC Skeleton)
- Python syntax valid (ast.parse)
- QC imports present (`from AlgorithmImports import *`)
- Required methods exist (Initialize, OnData)
**Error**: `ALGO_ERR_007`

### GATE 5: CONSISTENCY
**Type**: BLOCKING | **Error**: `ALGO_ERR_008`

| Rule | Check | Type |
|------|-------|------|
| TIMEFRAME_ALIGNMENT | hypothesis.timeframe == spec.timeframe | BLOCKING |
| SIGNAL_LOGIC | Entry uses stated indicators | BLOCKING |
| PARAMETER_BINDING | Locked params unchanged in spec | BLOCKING |
| MECHANISM_SOUNDNESS | Strategy type matches hypothesis | WARNING |

**On Blocking Violation**: Show mismatch, route to P6 revision, do NOT present to user.

---

## P6: PRESENT/REVISE - Output or Routing

### Success Path
Present: Hypothesis bundle, JSON spec, QC skeleton (if requested), next steps.

### Failure Path: Revision Taxonomy (4 Paths)

| Path | Condition | Action | Hypothesis ID |
|------|-----------|--------|---------------|
| 1. Code Bug | Implementation error | Fix code, retry | SAME |
| 2. Regime Failure | Failed specific period | Add regime filter | NEW |
| 3. Invalid Theory | Failed randomly | Archive to graveyard | NEW |
| 4. Insufficient Sample | <100 trades | Extend timeframe | SAME |

**Detection Signals**:
- Code Bug: Exception traces, NaN values, logic errors
- Regime Failure: >60% drawdown in crisis periods (2008, COVID)
- Invalid Theory: No regime correlation, consistent negative expectancy
- Insufficient Sample: `trade_count < 100`

See [Revision Guard Rails](./revision-guard-rails.md) for detailed rules.


---

## Gate Summary Table

| Gate | Phase | Check | Type | Action on Fail |
|------|-------|-------|------|----------------|
| GATE 1: INPUT | P1 | 7 elements present | BLOCKING | Clarifying questions |
| GATE 2a: PARAM_COUNT | P2 | Count < 10 | BLOCKING | Reduction guidance |
| GATE 2b: PARAM_RANGES | P2 | No range > 3x | BLOCKING | Narrow ranges |
| GATE 2c: HYPOTHESIS | P2 | Schema, locked, testability >= 0.7 | BLOCKING | Reformulate |
| GATE 3: DATA | P3 | Confidence score | NON-BLOCKING | Warn if < 0.8 |
| GATE 5: CONSISTENCY | P5 | 4 alignment rules | BLOCKING | Route to revision |

### Gate Flow
```
P1 ─[G1]─> P2 ─[G2a]─> [G2b] ─> [G2c]─> P3 ─[G3]─> P4 ───> P5 ─[G5]─> P6
   BLOCK      BLOCK     BLOCK    BLOCK     warn              BLOCK
```

---

## Error Codes

| Code | Phase | Description |
|------|-------|-------------|
| ALGO_ERR_001 | P1 | Insufficient input (< 7 elements) |
| ALGO_ERR_002 | P2 | Untestable hypothesis |
| ALGO_ERR_003 | P3 | Critical data unavailable |
| ALGO_ERR_004 | P2 | Overfit risk (hard constraint) |
| ALGO_ERR_005 | P4 | Strategy generation failed |
| ALGO_ERR_006 | P5 | Spec schema validation failed |
| ALGO_ERR_007 | P5 | Skeleton syntax error |
| ALGO_ERR_008 | P5 | Hypothesis-spec mismatch |

---

**Related**: [Revision Guard Rails](./revision-guard-rails.md) | [HDD Methodology](./hdd-methodology.md) | [Anti-Overfit Gates](./anti-overfit-gates.md)
