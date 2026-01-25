# Architecture Reviewer Schemas

## Contents

| File | Purpose |
|------|---------|
| `architecture-reviewer.schema.json` | Input/output contract extending base-agent.schema.json |

## Schema Overview

The architecture-reviewer produces two primary outputs:
1. **Technical Review Report** - Comprehensive analysis with scores
2. **Technical Edit Plan** - Actionable patches for enhancer agents

Both are embedded in the SUCCESS response under `agent_specific_output`.
