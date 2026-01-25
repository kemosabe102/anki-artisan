# Context Readiness Assessor - Documentation

## Overview

This directory contains detailed domain expertise and methodology documentation for the context-readiness-assessor agent.

## Files

| File | Purpose |
|------|---------|
| `domain-expertise.md` | Scoring rubrics for 4 CQ components, gap-to-agent mapping, research coordination strategy |
| `frameworks.md` | Hermeneutic assessment approach, iteration management, gate logic, improvement tracking |

## Quick Reference

**Context_Quality Formula**:
```
CQ = (Domain_Familiarity x 0.40) + (Pattern_Clarity x 0.30) + (Dependency_Understanding x 0.20) + (Risk_Awareness x 0.10)
```

**Gate Thresholds**:
- PASS: CQ >= 0.85
- GATHER_MORE_CONTEXT: CQ < 0.85, iteration < 3
- BLOCKED: CQ < 0.85, iteration = 3

**Hard Caps**:
- Max 3 iterations
- Max 10 agent invocations total
- Max 5 agents in parallel
- 5-minute timeout per iteration
