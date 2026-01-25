# Reliability Reviewer Documentation

## Overview

The reliability-reviewer agent applies the **Four Hats** methodology to evaluate system reliability at integration boundaries between components.

## Four Hats Framework

| Hat | Perspective | Focus Area |
|-----|-------------|------------|
| **Graph Theorist** | Edge reliability | Timeouts, race conditions, failure propagation |
| **Lawyer** | Node contracts | Preconditions, invariants, resource bounds |
| **Operator** | Observability | Logs, metrics, configurability |
| **Historian** | Maintainability | Cognitive load, dependency hygiene |

## Skills Used

This agent references three skills for its checklists:

1. **edge-reliability** - Graph Theorist hat checklists
2. **node-reliability** - Lawyer hat checklists  
3. **operational-reliability** - Operator + Historian hat checklists

## Integration

Called by `integration-boundary-reviewer` agent as 4th parallel delegate during MODE: review.

## Source Documents

The Four Hats methodology is derived from:
- `system-edge-reliability.md`
- `monolith-edge-reliability.md`
- `system-node-reliability.md`
- `operational-edge-reliability.md`
