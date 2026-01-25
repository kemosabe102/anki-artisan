# 8-Step Scientific Debugging Process

## Overview

A systematic approach to debugging that treats each investigation as a scientific experiment.

---

## Step 1: Reproduce & Baseline

**Goal**: Make the bug fail reliably

- Create minimal reproduction case
- Document exact steps to trigger
- Capture baseline evidence (logs, stack trace, screenshots)
- Verify reproduction is consistent (run 3+ times)

**Output**: Reproducible test case with documented steps

---

## Step 2: Formulate Hypothesis

**Goal**: Create specific, testable statement about the cause

Requirements for valid hypothesis:
- **Specific**: Points to exact location/component
- **Testable**: Can design experiment to verify
- **Falsifiable**: Can be proven wrong

**Bad**: "Something is wrong with the database"
**Good**: "Connection pool exhaustion occurs when concurrent requests exceed 10"

---

## Step 3: Design Experiment

**Goal**: Create non-invasive test to verify hypothesis

Experiment types:
- **Test harness**: Isolated reproduction script
- **Instrumentation**: Temporary logging/tracing
- **Log analysis**: Pattern search in existing logs
- **Debugger**: Step-through execution

**Rule**: No production code changes during experimentation

---

## Step 4: Execute & Observe

**Goal**: Run experiment and capture objective results

- Execute experiment exactly as designed
- Record all observations without interpretation
- Note unexpected behaviors
- Run multiple times for consistency

**Output**: Raw evidence log

---

## Step 5: 5 Whys Analysis

**Goal**: Find root cause, not just symptom

Ask "Why?" iteratively (typically 5 times) until reaching actionable root cause:

1. Why did [symptom] happen? → [cause 1]
2. Why did [cause 1] happen? → [cause 2]
3. Why did [cause 2] happen? → [cause 3]
4. Why did [cause 3] happen? → [cause 4]
5. Why did [cause 4] happen? → [root cause]

**Evidence requirement**: Each "why" must be backed by evidence from Step 4.

---

## Step 6: SCAMPER Solution Generation

**Goal**: Generate multiple fix candidates

Use SCAMPER framework to brainstorm solutions:
- **S**ubstitute: Replace problematic component
- **C**ombine: Merge with existing solution
- **A**dapt: Modify existing code
- **M**odify: Change parameters/configuration
- **P**ut to other use: Repurpose existing functionality
- **E**liminate: Remove the cause entirely
- **R**everse: Opposite approach

Generate 2-3 candidate solutions, rank by:
- Minimality (40%): Smallest change
- Risk (35%): Lowest side effects
- Maintainability (25%): Easiest to understand

---

## Step 7: Minimal Fix

**Goal**: Implement smallest change that resolves issue

- One change at a time
- Only modify after hypothesis confirmed
- Prefer simplest solution from Step 6
- Document the change and reasoning

---

## Step 8: Verify & Guard

**Goal**: Confirm fix and prevent regression

1. Run original failing test → must pass
2. Run full test suite → no regressions
3. Add guard test if none exists
4. Document RCA for future reference
