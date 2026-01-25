# Documentation Health Skill

**Status**: ✅ Complete  
**Version**: 1.0.0  
**Created**: 2025-12-13

---

## Overview

Validates documentation ecosystem health through link checking, orphan detection, staleness analysis, and health scoring (0-100).

## Files

- `SKILL.md` (402 lines) - Main skill specification
- `references/link-validation-patterns.md` - Regex patterns, HTTP validation
- `references/health-score-formula.md` - Calculation methodology
- `references/staleness-detection.md` - Age thresholds, freshness rules

## Key Features

### Three-Tier Safety Model
- **Tier 1**: Read-only analysis (always safe)
- **Tier 2**: Automated safe fixes (auto-approved)
- **Tier 3**: Supervised restructuring (user approval)

### Health Scoring
- **Range**: 0-100
- **Grades**: A (90+), B (75-89), C (60-74), D (40-59), F (<40)
- **Formula**: `100 - (critical×10 + high×5 + medium×2 + low×1)`

### Validations
- Link validation (internal/external)
- Orphan detection (zero incoming references)
- Staleness analysis (file age + reference freshness)
- Naming convention (kebab-case)

## Usage

**Trigger keywords**: "audit docs", "doc health", "broken links", "find orphans", "staleness report"

**Scope**: `docs/**` and `.claude/docs/**` only

## Integration

**Used by**: `documentation` agent  
**Coordinates with**: `documentation-synthesis`, `documentation-optimization`

---

**Template for**: Documentation domain skills
