# Phase 1: OBSERVE - Evidence Collection

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Validate scope, collect raw data from codebase and git history

**Deliverable**: Files in scope, complexity patterns, duplication, comments, git metrics

---

## Pre-Flight Validation

**Before analysis, assess scope size:**

| Check | Command | Thresholds |
|-------|---------|------------|
| File Count | `Glob` scope directories | <500: proceed, 500-2000: chunk warning, >2000: MUST chunk |
| LOC Estimation | Sample 10 files | <50K: full, 50-100K: limit history to 1mo, >100K: chunk by directory |
| Git History | `git rev-list --count HEAD` | <100: full, 100-1000: 3mo limit, >1000: 1mo limit |

**Scope Exceeded**: Document coverage gaps, set `analysis_coverage` field, continue with partial results.

---

## Workflow Steps

### Step 1.1: Scope Validation

**Input**: User-defined directories/patterns

**Process**:
1. `Glob`: Identify all files in scope
2. Count files, estimate LOC from sample
3. Check git history depth
4. Determine chunking strategy if needed

**Output**: Validated scope, chunking plan (if needed), coverage limitations

### Step 1.2: Pattern Detection

**Input**: Validated file list

**Process**:
1. `Grep`: Collect complexity patterns (`if|else|while|for|try|catch` nesting depth)
2. `Grep`: Detect duplication patterns (repeated code blocks >10 lines)
3. `Grep`: Find TODO/FIXME/HACK comments with context

**Output**: Raw pattern data with file:line references

### Step 1.3: Git History Collection

**Input**: Scope directories, time window (3mo default)

**Process**:
1. `Bash`: `git log --since="3 months ago" --format="%H" -- {scope}` (commit frequency)
2. `Bash`: `git shortlog -sn --since="3 months ago" -- {scope}` (contributor spread)
3. `Bash`: `git log --oneline --since="3 months ago" -- {scope} | wc -l` (churn count)

**Output**: Commit frequency, contributor distribution, churn metrics

---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Scope validated (file count, LOC estimated)
- [ ] Chunking strategy applied if >500 files
- [ ] Complexity patterns collected with file:line refs
- [ ] Duplication patterns identified
- [ ] TODO/FIXME/HACK comments cataloged
- [ ] Git history collected (commits, contributors, churn)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Scanning without defined scope | Require user-defined directories first |
| Ignoring scope limits | Apply chunking for >500 files |
| Missing evidence format | All findings need `{path}:{line}` format |
| Full history on large repos | Limit to 3mo or 1mo based on commit count |

---

## Exit Criteria

**CQ (Context Quality) >= 0.70 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Scope validated | 0.30 | File count known, LOC estimated |
| Patterns collected | 0.25 | Complexity, duplication, comments |
| Git metrics available | 0.20 | Commits, contributors, churn |
| Evidence formatted | 0.15 | All refs in `{path}:{line}` format |
| Coverage documented | 0.10 | Gaps/limitations noted |

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
