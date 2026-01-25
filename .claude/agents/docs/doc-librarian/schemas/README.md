# schemas/ Directory

**Purpose**: JSON Schema definitions for doc-librarian input/output contracts

---

## Contents

| File | Description |
|------|-------------|
| `doc-librarian.schema.json` | Input/output contract for all operations |

---

## Schema Overview

**Extends**: `base-agent.schema.json` (two-state SUCCESS/FAILURE model)

**Operations** (via `operation_type`):
- `check_health` - Full documentation health assessment
- `fix_links` - Validate and repair broken links
- `rename_files` - Kebab-case naming compliance
- `audit_organization` - DOCS-MANAGEMENT.md rule checking

**Key Output Fields**:
- `health_report` - Scores and violation details
- `recommendations` - Prioritized action items
- `fixes_applied` - Tier 2 automated fix results

---

## Validation

All agent outputs validate against this schema. See schema file for:
- Required fields per operation type
- Severity enum values (critical/high/medium/low)
- Health score ranges (0-100)
- Confidence ranges (0.0-1.0)
