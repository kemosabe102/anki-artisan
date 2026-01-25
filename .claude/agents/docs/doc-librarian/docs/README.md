# docs/ Directory

**Purpose**: Externalized domain knowledge for the doc-librarian agent

---

## Contents

| File | Description |
|------|-------------|
| `domain-expertise.md` | Health assessment patterns, validation strategies, naming conventions |
| `frameworks.md` | Three-tier safety model, workflow operations, coordination protocols |

---

## Quick Reference

**Agent Scope**: `docs/**` and `.claude/docs/**` only

**Key Operations**:
- `check_health` - Full documentation health scan
- `fix_links` - Validate and repair broken links
- `rename_files` - Kebab-case naming compliance
- `audit_organization` - DOCS-MANAGEMENT.md rule checking

**External Dependencies**:
- `DOCS-MANAGEMENT.md` - Organization rules
- `file-operation-protocol.md` - File modification guidelines
- `progressive-disclosure-validation-framework.md` - Quality scoring
