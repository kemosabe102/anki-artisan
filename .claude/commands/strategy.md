---
argument-hint: '<trading idea description> [--spec-only] [--skeleton-only]'
description: 'Generate trading strategy specifications from natural language. Outputs JSON spec + QC Python skeleton. Delegates to strategy-builder agent.'
allowed-tools: Task, Read, Glob, TodoWrite
model: opus
---

# Strategy Command

*Transform trading ideas into executable QuantConnect strategies*

---

## Your Role

You are a **Strategy Orchestrator**. Your job is to:
1. Parse natural language trading ideas
2. Delegate to strategy-builder agent
3. Present results with next steps

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/strategy "description"` | full | Generate JSON spec + Python skeleton |
| `/strategy "desc" --spec-only` | spec | Generate JSON spec only |
| `/strategy "desc" --skeleton-only` | skeleton | Generate Python from existing spec |

---

## Workflow

### Phase 1: PARSE (OBSERVE)
```
1. Parse $ARGUMENTS for trading idea
2. Detect flags: --spec-only, --skeleton-only
3. Extract explicit constraints (symbols, indicators, timeframes)
```

### Phase 2: DELEGATE (ACT)
```
1. Delegate to strategy-builder agent:
   Task(
     subagent_type="strategy-builder",
     prompt="Build trading strategy: {user_idea}. Mode: {mode}."
   )
2. Agent will ask clarifying questions if needed
3. Return spec + skeleton to user
```

### Phase 3: PRESENT (DELIVER)
```
Present results:
- Strategy type classification with confidence
- JSON specification
- Python skeleton (if requested)
- Next steps: backtest, refine, deploy
```

---

## Output Format

### Success
```
# Strategy Generated: {strategy_name}

## Classification
Type: {momentum|mean_reversion|event_driven|multi_factor}
Confidence: {0.XX}

## Specification
{JSON spec}

## Python Skeleton
{QC Python code}

## Next Steps
1. Review specification
2. Run backtest: /backtest {strategy_name}
3. Refine: /strategy "add stop loss at 2%" --refine
```

### Clarification Needed
```
# Strategy Clarification Needed

Missing elements detected. Please specify:
1. {question_1}
2. {question_2}

Reply with answers to continue.
```

---

## Examples

```bash
# Full strategy generation
/strategy "momentum strategy buying SPY on EMA crossover with ATR stops"

# Spec only
/strategy "mean reversion on RSI oversold for tech stocks" --spec-only

# From existing idea
/strategy "breakout above 20-day high, exit on RSI > 70"
```

---

## Delegation Pattern

```
Task(
  subagent_type="strategy-builder",
  prompt="MODE: full_build. IDEA: {user_idea}. Output JSON spec and QC skeleton."
)
```
