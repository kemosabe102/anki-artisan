---
name: debugging-methodology
description: >
  Use this skill when debugging issues using systematic hypothesis-driven methods.
  Provides the 8-step scientific debugging process, 5 Whys root cause analysis,
  and SCAMPER solution generation. Trigger keywords: debug, hypothesis, root cause,
  5 whys, RCA, experiment, reproduce, SCAMPER, scientific method.
---

# Debugging Methodology Skill

Systematic hypothesis-driven debugging with evidence-before-edits principle.

## Core Principle

**Never edit code until you have evidence.** Work systematically:
1. Reproduce → 2. Hypothesize → 3. Experiment → 4. Observe → 5. RCA → 6. Solution → 7. Fix → 8. Verify

---

## Zero-Step: State Recovery

Before starting any debugging session:
1. Check for in-progress debugging state (hypothesis log, experiment results)
2. If resuming: Continue from last hypothesis
3. If new: Initialize fresh debugging session

After each significant action:
- Log hypothesis, evidence, and result
- Preserve state for session continuity

## Reference Documentation

- **8-Step Process** -> [reference/eight-step-process.md](reference/eight-step-process.md)
- **5 Whys RCA** -> [reference/five-whys-rca.md](reference/five-whys-rca.md)
- **SCAMPER Solutions** -> [reference/scamper-solutions.md](reference/scamper-solutions.md)

---

## Templates

**RCA Report Template**: [templates/rca-report.md](templates/rca-report.md)

Use this template for documenting root cause analysis with:
- 5 Whys chain with evidence
- Hypothesis testing log
- SCAMPER solution analysis
- Verification checklist

---

## Quick Reference: 8-Step Scientific Method

| Step | Action | Output |
|------|--------|--------|
| 1. Reproduce | Make bug fail reliably | Reproducible test case |
| 2. Hypothesize | Form specific, testable statement | Hypothesis document |
| 3. Experiment | Design non-invasive test | Test harness/instrumentation |
| 4. Observe | Run experiment, capture results | Evidence log |
| 5. 5 Whys | Find root cause, not symptom | RCA chain |
| 6. SCAMPER | Generate 2-3 fix candidates | Ranked solutions |
| 7. Minimal Fix | One change at a time | Code change |
| 8. Verify | Original test passes, no regressions | Green test suite |

---

## Hypothesis Requirements

A valid hypothesis must be:
- **Testable**: Can design an experiment to prove/disprove
- **Specific**: Points to exact location/cause
- **Falsifiable**: Can be proven wrong

**Bad**: "Something is wrong with authentication"
**Good**: "JWT token expiry check in auth.py:45 uses UTC but server returns local time"

---

## Experiment Toolkit

| Method | When to Use | Example |
|--------|-------------|---------|
| Test Harness | Isolate component | Create minimal reproduction script |
| Instrumentation | Track execution flow | Add temporary logging |
| Log Analysis | Pattern detection | `grep -C5 "ERROR" logs/` |
| Debugger | Step through code | `pdb.set_trace()` |

**Rule**: Experiments must be non-invasive. No production code changes during hypothesis testing.

---

## Anti-Patterns (NEVER DO)

- Edit code before confirming hypothesis
- Skip reproduction step
- Accept "it works now" without understanding why
- Stop at symptom instead of root cause
- Make multiple changes simultaneously
