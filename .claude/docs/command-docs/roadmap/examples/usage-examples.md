# Usage Examples

Complete workflow examples for the `/roadmap` command.

---

## Example 1: Basic Health Check

```bash
User: /roadmap

Claude: [Phase 1: Discovers 8 roadmap files]
        [Phase 2: 3 agents analyze in parallel (~40s)]
        [Phase 3: Synthesizes results, ranks recommendations]
        [Phase 4: Presents health dashboard]

## Roadmap Ecosystem Health Report

**Overall**: 0.82 (B) | **Date**: 2025-11-03 | **Files**: 8 (6 active, 2 archive)

**Dimensions**:
- Progressive Disclosure: 0.88 (B+)
- Token Density: 0.75 (C+)
- Cross-Ref Integrity: 0.92 (A)
- Sprint Compliance: 0.95 (A)
- Freshness: 0.68 (D+)
- Completeness: 0.85 (B)

**Top 5 Actions** (ranked by ROI):
1. Token Density (HIGH impact, LOW effort) -> /roadmap optimize
2. Freshness (MED impact, LOW effort) -> /roadmap update
3. Broken Links (MED impact, MED effort) -> Manual fix
4. Progressive Disclosure (MED impact, HIGH effort) -> Restructure
5. Date Consistency (LOW impact, LOW effort) -> /roadmap update

**Next Check**: Run `/roadmap check` after fixes
```


---

## Example 2: Update + Optimize Workflow

```bash
User: /roadmap update

Claude: [Discovers files needing status updates]
        [planning updates status fields]
        
Status updates applied: 3 files
- Q1-2026.md: PLANNING -> IN PROGRESS
- Q4-2025.md: IN PROGRESS -> COMPLETE
- Timestamps refreshed: LIVING_SPRINT.md

User: /roadmap optimize

Claude: [Analyzes token density]
        [context-optimizer applies best practices]
        
Token reduction: 745 tokens (25.5%)
Files optimized: 4
Techniques applied:
- Filler word removal: 312 tokens saved
- Passive voice conversion: 198 tokens saved
- Structure improvements: 235 tokens saved
```

---

## Example 3: Explicit Check Mode

```bash
User: /roadmap check

Claude: [Same as Example 1 - explicit check mode]
        [Full multi-agent analysis with dashboard output]
```


---

## Example 4: Partial Agent Failure

```bash
User: /roadmap check

Claude: [Phase 1: Discovers 8 files]
        [Phase 2: 2 of 3 agents succeed, documentation times out]
        [Phase 3: Synthesizes partial results]
        [Phase 4: Dashboard with N/A for failed dimensions]

## Roadmap Ecosystem Health Report

**Overall**: 0.78 (C+) | **Date**: 2025-11-03 | **Files**: 8

**Dimensions**:
- Progressive Disclosure: N/A (agent timeout)
- Token Density: 0.75 (C+)
- Cross-Ref Integrity: N/A (agent timeout)
- Sprint Compliance: 0.95 (A)
- Freshness: 0.68 (D+)
- Completeness: 0.85 (B)

**Note**: documentation timed out. Cross-reference validation incomplete.
Retry with `/roadmap check` or run manual validation.
```

---

## Example 5: No Files Found

```bash
User: /roadmap check

Claude: ROADMAP CHECK BLOCKED

Error: No roadmap files found
Phase: 1 (Discovery)
Recovery attempted: Checked all expected paths

Paths searched:
- docs/00-project/roadmaps/active/*.md (0 files)
- docs/00-project/roadmaps/archive/*.md (0 files)
- docs/00-project/operations/LIVING_SPRINT.md (not found)
- docs/00-project/SPRINT-ROADMAP.md (not found)

Recommended action: Create initial roadmap file before running health check.
```


---

## Performance Comparison

### Parallel Execution (Correct)

```text
Phase 1 (Discovery):     5s
Phase 2 (Analysis):     40s  <- 3 agents in parallel
Phase 3 (Synthesis):    10s
Phase 4 (Present):       5s
------------------------
Total:                  60s
```

### Sequential Execution (Anti-Pattern)

```text
Phase 1 (Discovery):     5s
Phase 2a (roadmap-mgr): 30s
Phase 2b (doc-lib):     35s
Phase 2c (ctx-opt):     25s
Phase 3 (Synthesis):    10s
Phase 4 (Present):       5s
------------------------
Total:                 110s  <- 50s wasted!
```

**Key Insight**: Parallel launch saves ~50 seconds per health check.

---

## Mode Summary

| Command | Duration | Output |
|---------|----------|--------|
| `/roadmap` | ~60s | Health dashboard |
| `/roadmap check` | ~60s | Health dashboard |
| `/roadmap update` | ~25s | Status update summary |
| `/roadmap optimize` | ~40s | Token savings report |
