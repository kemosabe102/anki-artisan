---
argument-hint: '<hypothesis-statement> [--symbols SPY,QQQ] [--timeframe 2Y] [--alpha 0.05] [--resume <hypothesis_id>] [--output json|markdown|both]'
description: 'Rapid hypothesis validation via QuantConnect research node before full backtest'
allowed-tools: [Task, Read, Glob, Grep, Write]
model: opus
---

# Algo Hypothesis Test

*Fast statistical validation of trading hypotheses using QuantConnect research nodes*

---

## Purpose

Validate trading hypotheses statistically BEFORE building full backtest algorithms. Generates ready-to-execute QuantConnect Research.ipynb cells that:
1. Structure natural language into Cause→Effect→Why format
2. Fetch historical data via QuantBook API
3. Run correlation and stationarity tests (p < 0.05 threshold)
4. Output GO/NO-GO recommendation with statistical confidence

**Time savings**: ~5 minutes vs ~2 hours for full backtest cycle.

---

## Modes

| User Input | Mode | Action |
|------------|------|--------|
| `/algo-hypothesis-test "RSI crosses below 30 leads to reversal"` | validate | Structure hypothesis, generate QC notebook cells |
| `/algo-hypothesis-test --from-file docs/hypotheses/H001.md` | file | Load existing hypothesis, generate QC cells |
| `/algo-hypothesis-test --check-graveyard "momentum"` | graveyard | Search hypothesis graveyard for similar failed ideas |
| `/algo-hypothesis-test --resume H001` | resume | Resume from checkpoint after P2 |

**Note**: Semantic pre-validation (P0.5) runs automatically in `validate` and `file` modes before hypothesis structuring. Output format (`--output`) defaults to `both` (markdown + JSON).

---

## Workflow

```text
/algo-hypothesis-test <hypothesis-statement> [flags]
|
+-- P0: PARSE & VALIDATE
|   +-- Extract hypothesis statement from args
|   +-- Parse flags: --symbols, --timeframe, --alpha, --from-file, --resume
|   +-- IF --resume specified:
|   |   +-- Load checkpoint from temp/algo-hypothesis-test/{hypothesis_id}_checkpoint.json
|   |   +-- Validate checksum
|   |   +-- IF valid: Skip to phase after checkpoint (typically P3)
|   |   +-- IF invalid: ALGO_HYP_008, prompt user to restart
|   +-- [GATE 0] Hypothesis statement present or --from-file or --resume specified
|
+-- P0.5: SEMANTIC PRE-VALIDATION
|   +-- LLM confidence scoring of raw hypothesis statement
|   +-- Evaluate: Is the statement parseable into Cause→Effect→Why?
|   +-- Score dimensions:
|   |   +-- indicator_clarity (0-1): Can a specific indicator be identified?
|   |   +-- threshold_presence (0-1): Is there a numerical threshold?
|   |   +-- effect_measurability (0-1): Is the effect quantifiable?
|   |   +-- mechanism_plausibility (0-1): Does the WHY make sense?
|   +-- semantic_confidence = avg(all dimensions)
|   +-- [GATE 0.5] semantic_confidence >= 0.6 OR suggest improvements
|   +-- IF confidence < 0.6: ALGO_HYP_006 with suggestions
|
+-- P1: STRUCTURE HYPOTHESIS (if natural language input)
|   +-- Apply Cause→Effect→Why template (hypothesis-formulation skill)
|   +-- Extract: indicator, threshold, expected_effect, timeframe, mechanism
|   +-- Validate: cause is measurable, effect is testable, why is grounded
|   +-- [GATE 1] Structured hypothesis passes quality checklist
|
+-- P1.5: ECONOMIC THEORY VALIDATION
|   +-- Task(researcher-external,
|   |     "Search for economic/finance theory supporting:
|   |      CAUSE: {cause}
|   |      EFFECT: {effect}
|   |      WHY: {why}
|   |      Return: theory_name, academic_support (high/medium/low/none),
|   |      key_citations (max 3), contradicting_evidence")
|   +-- Parse research response:
|   |   +-- theory_support score (0.0-1.0):
|   |   |   +-- high academic support = 0.9
|   |   |   +-- medium academic support = 0.7
|   |   |   +-- low academic support = 0.4
|   |   |   +-- no academic support = 0.1
|   +-- [GATE 1.5] theory_support >= 0.3 OR user override with acknowledgment
|   +-- IF research timeout (>30s): ALGO_HYP_011, soft fail with skip option
|   +-- IF no theory found: ALGO_HYP_007 (WARNING, not blocking)
|
+-- P2: GRAVEYARD CHECK
|   +-- Search hypothesis graveyard for similar failed hypotheses
|   +-- Calculate similarity score (semantic match on cause/effect/why)
|   +-- IF similarity > 0.7: WARN user, show epitaph
|   +-- [GATE 2] User acknowledges or hypothesis is novel
|   +-- [CHECKPOINT] Save state to temp/algo-hypothesis-test/{hypothesis_id}_checkpoint.json
|
+-- P3: GENERATE QC NOTEBOOK CELLS
|   +-- Load templates from .claude/commands/templates/qc-hypothesis-cells.md
|   +-- IF template not found: ALGO_HYP_009
|   +-- Generate cells with variable substitution:
|   |   +-- Cell 1: Setup (QuantBook, imports)
|   |   +-- Cell 2: Data fetch (symbols, resolution, timeframe)
|   |   +-- Cell 3: Indicator calculation (from CAUSE)
|   |   +-- Cell 4: Statistical tests (correlation, ADF stationarity)
|   |   +-- Cell 5: Visualization (signal vs returns scatter, time series)
|   |   +-- Cell 6: GO/NO-GO decision logic
|   +-- [VALIDATE] For each generated cell:
|   |   +-- Run ast.parse(cell_code) to validate Python syntax
|   |   +-- IF ast.parse fails:
|   |   |   +-- Attempt self-healing: LLM fix of syntax error
|   |   |   +-- Retry ast.parse() once
|   |   |   +-- IF still fails: ALGO_HYP_010
|   +-- [GATE 3] All 6 cells generated AND pass ast.parse()
|
+-- P4: OUTPUT & NEXT STEPS
    +-- Determine output format (--output flag, default: both)
    +-- IF output includes markdown:
    |   +-- Display structured hypothesis
    |   +-- Output QC notebook cells (copy-paste ready)
    |   +-- Provide interpretation guide for results
    +-- IF output includes json:
    |   +-- Generate JSON per schema
    |   +-- Validate against JSON schema
    |   +-- IF validation fails: ALGO_HYP_012
    |   +-- Write to temp/algo-hypothesis-test/{hypothesis_id}_output.json
    +-- Suggest: If GO → /algo-strategy --from-hypothesis {hypothesis_id}
    +-- [GATE 4] User has actionable output in requested format(s)
```

---

## Agent Delegation

| Phase | Agent | Task | Timeout |
|-------|-------|------|---------|
| P0.5 | (orchestrator) | LLM confidence scoring of hypothesis statement | 15s |
| P1 | (orchestrator) | Apply hypothesis-formulation skill patterns | 30s |
| P1.5 | researcher-external | Search economic/finance theory for hypothesis support | 30s |
| P2 | Explore | Search graveyard for similar hypotheses | 60s |
| P3 | (orchestrator) | Generate QC Python cells from templates | 30s |
| P4 | (orchestrator) | Format output with interpretation guide | 15s |

### Delegation Examples

**P1.5 Economic Theory Search:**
```
Task(researcher-external, 
  "Search for economic/finance theory supporting this trading hypothesis:
   CAUSE: '{cause}'
   EFFECT: '{effect}'
   WHY: '{why}'
   
   Return structured response:
   - theory_name: Name of supporting theory (e.g., 'Mean Reversion', 'Momentum Effect')
   - academic_support: high|medium|low|none
   - key_citations: Up to 3 academic papers or authoritative sources
   - contradicting_evidence: Any conflicting research or conditions where theory fails
   
   BOUNDARIES: Research only. Focus on established finance/economics literature.")
```

**P2 Graveyard Search:**
```
Task(Explore, 
  "Search .claude/skills/hypothesis-tracking/ and docs/hypotheses/ for failed 
   hypotheses similar to: '{cause}' → '{effect}' because '{why}'.
   Return: hypothesis_id, similarity_score, failure_mode, epitaph
   BOUNDARIES: Read-only. Do not modify graveyard entries.")
```

---

## Checkpoint Support

Checkpoints allow resuming hypothesis validation after P2 (graveyard check), avoiding re-running semantic validation and theory research.

### Checkpoint File Location
```
temp/algo-hypothesis-test/{hypothesis_id}_checkpoint.json
```

### Checkpoint Schema
```json
{
  "hypothesis_id": "H001",
  "phase_completed": "P2",
  "timestamp": "2025-01-19T10:30:00Z",
  "checksum": "sha256 of structured_hypothesis JSON",
  "data": {
    "structured_hypothesis": {
      "cause": "RSI(14) crosses below 30",
      "effect": "Price reverses upward within 5 bars",
      "why": "Oversold conditions trigger value buyers",
      "indicator": "RSI",
      "threshold": 30,
      "direction": "below",
      "effect_bars": 5
    },
    "semantic_validation": {
      "confidence": 0.85,
      "scores": {
        "indicator_clarity": 0.9,
        "threshold_presence": 1.0,
        "effect_measurability": 0.8,
        "mechanism_plausibility": 0.7
      }
    },
    "theory_validation": {
      "theory_support": 0.7,
      "theory_name": "Mean Reversion",
      "academic_support": "medium",
      "citations": ["Poterba & Summers (1988)", "DeBondt & Thaler (1985)"]
    },
    "graveyard_check": {
      "similar_found": false,
      "max_similarity": 0.32
    }
  },
  "parameters": {
    "symbols": ["SPY"],
    "timeframe": "2Y",
    "alpha": 0.05
  }
}
```

### Resume Flag
```bash
/algo-hypothesis-test --resume H001
```

### Checkpoint Validation
- Checksum verification prevents tampering
- Expired checkpoints (>24h) trigger ALGO_HYP_008 warning
- Missing checkpoint file triggers ALGO_HYP_008 error

---

## Statistical Tests

### Test Suite (p < 0.05 threshold)

| Test | Purpose | Pass Condition |
|------|---------|----------------|
| Pearson Correlation | Linear relationship | \|r\| > 0.1, p < 0.05 |
| Spearman Correlation | Monotonic relationship | \|ρ\| > 0.1, p < 0.05 |
| ADF Stationarity | Signal mean-reverts | p < 0.05 (reject unit root) |

### Decision Matrix

| Correlation | Stationarity | Recommendation |
|-------------|--------------|----------------|
| Significant (p<0.05) | Stationary | **GO** - Proceed to backtest |
| Significant (p<0.05) | Non-stationary | **CAUTION** - May work in trends only |
| Not significant | Stationary | **NO-GO** - Signal lacks predictive power |
| Not significant | Non-stationary | **NO-GO** - No edge detected |

---

## Code Validation

### ast.parse() Gate
All generated Python cells are validated with Python's `ast.parse()` before output.

**Why**: Prevents users from copying invalid Python into QuantConnect notebooks.

**Process**:
1. Generate cell code from template
2. Strip markdown fencing (```python ... ```)
3. Run `ast.parse(code)` to check syntax
4. If SyntaxError:
   - Log error location and message
   - Attempt LLM self-healing (one retry)
   - If still failing: ALGO_HYP_010

**Known Exceptions**:
QuantConnect-specific imports that may not be installed locally are allowed:
- `from QuantConnect import *`
- `from QuantConnect.Research import *`
- `qb = QuantBook()`

These pass ast.parse() even without QuantConnect installed because they're syntactically valid.

**Self-Healing Example**:
```python
# Error: ast.parse() failed
# Line 5: invalid syntax
#   signal_df = df.rolling(14).apply(lambda x: ...)  # missing closing paren

# LLM attempts fix:
signal_df = df.rolling(14).apply(lambda x: x.mean())  # fixed
```

---

## QC Notebook Templates

Templates are externalized to `.claude/commands/templates/qc-hypothesis-cells.md` for maintainability.

**Loading**: The command reads templates via:
```
Read(.claude/commands/templates/qc-hypothesis-cells.md)
```

**Variables**: Templates use placeholder variables that get substituted:
- `{symbols}` - Target symbols (e.g., ["SPY"])
- `{timeframe}` - Data lookback (e.g., "2Y")
- `{cause}` - Hypothesis cause statement
- `{indicator_code}` - Generated indicator Python code
- `{alpha}` - Statistical significance threshold
- `{effect_bars}` - Forward return calculation period

**Error handling**: If template file not found -> ALGO_HYP_009

---

## Error Codes

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ALGO_HYP_001 | P0 | No hypothesis statement provided | Provide statement or use --from-file |
| ALGO_HYP_002 | P1 | Cannot parse Cause→Effect→Why structure | Rephrase hypothesis more explicitly |
| ALGO_HYP_003 | P1 | CAUSE is not measurable | Add specific indicator and threshold |
| ALGO_HYP_004 | P2 | Similar hypothesis failed in graveyard | Review epitaph, modify approach |
| ALGO_HYP_005 | P3 | Unknown indicator in CAUSE | Use standard indicators (RSI, SMA, BB, etc.) |
| ALGO_HYP_006 | P0.5 | Semantic confidence < 0.6 - hypothesis statement too vague or ambiguous | Rephrase with specific indicator, threshold, and timeframe |
| ALGO_HYP_007 | P1.5 | No economic theory support found - hypothesis lacks theoretical grounding | Consider academic literature or reformulate based on established market principles |
| ALGO_HYP_008 | P2 | Checkpoint resume failed - corrupt or missing checkpoint file | Delete checkpoint and restart from P0 |
| ALGO_HYP_009 | P3 | Template file not found | Verify `.claude/commands/templates/qc-hypothesis-cells.md` exists |
| ALGO_HYP_010 | P3 | ast.parse() validation failed - generated Python code has syntax errors | Review indicator specification, use standard indicator names |
| ALGO_HYP_011 | P1.5 | Perplexity research timeout - economic theory search took > 30s | Retry with simpler query or skip theory validation with user override |
| ALGO_HYP_012 | P4 | JSON schema validation failed - output structure doesn't match schema | Internal error - report to maintainer |

---

## Output Format

### Success Output
```
Hypothesis Structured:
━━━━━━━━━━━━━━━━━━━━━
CAUSE:  RSI(14) crosses below 30
EFFECT: Price reverses upward within 5 bars
WHY:    Oversold conditions trigger value buyers

Parameters:
  Symbols: SPY, QQQ
  Timeframe: 2Y (504 bars)
  Alpha: 0.05

Graveyard Check: ✓ No similar failed hypotheses found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QuantConnect Research Notebook Cells (copy to Research.ipynb)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Cell 1: Setup]
<code block>

[Cell 2: Data Fetch]
<code block>

... (all 6 cells)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretation Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- If GO: Run /algo-strategy "RSI oversold reversal" to build backtest
- If CAUTION: Add regime filter (e.g., price > SMA200) to hypothesis
- If NO-GO: Archive hypothesis, formulate new one with different mechanism
```

### Failure Output
```
Hypothesis Test Failed

Error: ALGO_HYP_002
Phase: P1 - STRUCTURE HYPOTHESIS
Description: Cannot parse Cause→Effect→Why structure

Input: "momentum is good for trading"

Issue: Statement lacks:
  - Specific indicator (CAUSE missing threshold)
  - Measurable effect (no price target or timeframe)
  - Testable mechanism (WHY not explicit)

Suggestion: Rephrase as:
  "When [INDICATOR] crosses [THRESHOLD], price [MOVES HOW] within [TIMEFRAME]
   because [MECHANISM]"

Example:
  "When RSI(14) crosses below 30, price reverses upward within 5 bars
   because oversold conditions trigger value buyers"
```

---

## JSON Output Schema

When `--output json` or `--output both` is specified, a structured JSON output is generated.

### Output File Location
```
temp/algo-hypothesis-test/{hypothesis_id}_output.json
```

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AlgoHypothesisTestOutput",
  "type": "object",
  "required": ["hypothesis_id", "structured", "validation", "recommendation", "qc_cells_path", "next_command"],
  "properties": {
    "hypothesis_id": {
      "type": "string",
      "description": "Unique identifier (e.g., H001)"
    },
    "structured": {
      "type": "object",
      "required": ["cause", "effect", "why"],
      "properties": {
        "cause": { "type": "string" },
        "effect": { "type": "string" },
        "why": { "type": "string" },
        "indicator": { "type": "string" },
        "threshold": { "type": "number" },
        "direction": { "enum": ["above", "below", "crosses"] },
        "effect_bars": { "type": "integer" }
      }
    },
    "validation": {
      "type": "object",
      "properties": {
        "semantic_confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "theory_support": { "type": "number", "minimum": 0, "maximum": 1 },
        "theory_name": { "type": "string" },
        "theory_citations": { 
          "type": "array", 
          "items": { "type": "string" },
          "maxItems": 3 
        },
        "graveyard_similar": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "hypothesis_id": { "type": "string" },
              "similarity": { "type": "number" },
              "failure_mode": { "type": "string" }
            }
          }
        }
      }
    },
    "recommendation": {
      "enum": ["GO", "CAUTION", "NO-GO"],
      "description": "Overall recommendation based on validation gates"
    },
    "qc_cells_path": {
      "type": "string",
      "description": "Path to generated QC notebook cells file"
    },
    "next_command": {
      "type": "string",
      "description": "Suggested next command (e.g., '/algo-strategy --from-hypothesis H001')"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "version": { "type": "string" },
        "parameters": {
          "type": "object",
          "properties": {
            "symbols": { "type": "array", "items": { "type": "string" } },
            "timeframe": { "type": "string" },
            "alpha": { "type": "number" }
          }
        }
      }
    }
  }
}
```

### Example Output

```json
{
  "hypothesis_id": "H001",
  "structured": {
    "cause": "RSI(14) crosses below 30",
    "effect": "Price reverses upward within 5 bars",
    "why": "Oversold conditions trigger value buyers",
    "indicator": "RSI",
    "threshold": 30,
    "direction": "below",
    "effect_bars": 5
  },
  "validation": {
    "semantic_confidence": 0.85,
    "theory_support": 0.7,
    "theory_name": "Mean Reversion",
    "theory_citations": [
      "Poterba & Summers (1988)",
      "DeBondt & Thaler (1985)"
    ],
    "graveyard_similar": []
  },
  "recommendation": "GO",
  "qc_cells_path": "temp/algo-hypothesis-test/H001_cells.py",
  "next_command": "/algo-strategy --from-hypothesis H001",
  "metadata": {
    "timestamp": "2025-01-19T10:30:00Z",
    "version": "2.0",
    "parameters": {
      "symbols": ["SPY"],
      "timeframe": "2Y",
      "alpha": 0.05
    }
  }
}
```

### Output Flag Options

| Flag | Description |
|------|-------------|
| `--output markdown` | Human-readable markdown only (default behavior) |
| `--output json` | JSON file only |
| `--output both` | Both markdown display AND JSON file (default) |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Skip graveyard check | Repeat failed experiments | Always P2 before P3 |
| Test multiple hypotheses at once | Confounded results | One hypothesis per run |
| Ignore NO-GO result | Overfitting risk | Archive and pivot |
| Modify alpha post-hoc | P-hacking | Set alpha before running |
| Run without structured hypothesis | Untestable | Require Cause→Effect→Why |

---

## Good Patterns

| Pattern | Why Good | Example |
|---------|----------|---------|
| Specific indicators | Reproducible tests | "RSI(14) < 30" not "oversold" |
| Define effect timeframe | Testable outcome | "within 5 bars" |
| Check graveyard first | Avoid wasted effort | Similar H003 failed 2024-12 |
| Archive NO-GO results | Build knowledge | Prevents zombie resurrection |
| Use standard alpha | Consistent standards | p < 0.05 default |

---

## Integration with HDD Workflow

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Hypothesis-Driven Development                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. FORMULATE (hypothesis-formulation skill)                    │
│     └─> Cause→Effect→Why structure                              │
│                                                                  │
│  2. PRE-VALIDATE (/algo-hypothesis-test) ◄── YOU ARE HERE       │
│     └─> Statistical tests on research node                      │
│     └─> GO/NO-GO decision before backtest                       │
│                                                                  │
│  3. BUILD (/algo-strategy)                                      │
│     └─> Full backtest algorithm (only if GO)                    │
│                                                                  │
│  4. VALIDATE (/backtest)                                        │
│     └─> Walk-forward, robustness checks                         │
│                                                                  │
│  5. TRACK (hypothesis-tracking skill)                           │
│     └─> Trial count, graveyard management                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Knowledge Base

| Resource | Purpose |
|----------|---------|
| `.claude/commands/templates/qc-hypothesis-cells.md` | QC notebook cell templates |
| `.claude/skills/hypothesis-formulation/SKILL.md` | Cause→Effect→Why structure |
| `.claude/skills/hypothesis-tracking/SKILL.md` | Trial limits, graveyard |
| `docs/00-project/SPEC.md` | System architecture |
| QuantConnect Research Docs | QuantBook API reference |

---

## Boundaries

**IN SCOPE:**
- Structure natural language hypotheses
- Generate QC research notebook cells
- Check hypothesis graveyard
- Statistical test templates (correlation, stationarity)

**OUT OF SCOPE:**
- Execute code on QuantConnect (user does this)
- Build full backtest algorithms (use /algo-strategy)
- Modify hypothesis graveyard (use hypothesis-tracking)
- Run actual backtests (use /backtest)

---

**Version**: 1.0
**Author**: Created via /create-command wizard
**Dependencies**: hypothesis-formulation skill, hypothesis-tracking skill
