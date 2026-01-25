# Repository Analyst Workflows

## 5-Phase Inventory Generation

### Phase 1: Discovery (5-10s)
```
Parallel Glob operations:
- .claude/agents/**/*.md → agent definitions
- .claude/commands/**/*.md → command definitions
- .claude/hooks/**/*.py → lifecycle hooks
- .claude/skills/**/*.md → skill definitions
```

### Phase 2: Extract (10-15s)
```
Parallel Read in batches of 10-15 files:
- Parse YAML frontmatter (lines 1-10)
- Extract: name, description, model, tools, ooda_phase, domain
- Handle errors gracefully (skip + warn)
```

### Phase 3: Categorize (2-3s)
Group components by:
- OODA phase (OBSERVE/ORIENT/DECIDE/ACT)
- Domain (.claude/**/packages/**/docs/**/k8s/**)
- Type (Creator/Reviewer/Enhancer/Runner/Analyzer/Planner)
- Maturity (alpha/beta/stable/GA)

### Phase 4: Validate (3-5s)
- Naming conventions (kebab-case for .md, snake_case for .py)
- Required fields present (name, description, model, tools)
- Tool names valid (against standard tool list)
- References resolvable (no broken links)

### Phase 5: Generate (2-3s)
Output formats:
- **Markdown**: Tables with component lists, capabilities
- **JSON**: Machine-readable inventory for programmatic access
- **Summary**: CLI-friendly statistics and counts

---

## Performance Targets

| Phase | Target Time | Strategy |
|-------|-------------|----------|
| Discovery | <10s | Parallel Glob (4 operations) |
| Extract | <20s | Parallel Read (batches of 15) |
| Categorize | <3s | In-memory grouping |
| Validate | <5s | Parallel Grep for references |
| Generate | <3s | Sequential Write |
| **Total** | **<45s** | Hard timeout with partial results |

---

## Decision Trees

### Output Format Selection
```
IF consumer is agent (agent-architect, doc-librarian, context-optimizer)
  → JSON (machine-readable)
ELSE IF user says "report" or "summary"
  → Markdown (human-readable)
ELSE IF user says "count" or "stats"
  → Summary (CLI statistics)
ELSE
  → All formats (maximum utility)
```

### Parallel vs Sequential Strategy
```
IF component_count <= 15
  → Single parallel batch
ELSE IF component_count <= 50
  → Batched parallel (batch_size=15)
ELSE
  → Batched parallel (batch_size=10, prevent timeout)
```

---

## Termination Rules

### "Good Enough" Criteria
- Component count >0 sufficient (don't block on edge cases)
- 80%+ files validated is acceptable
- Partial results OK if error count <10

### Maximum Limits
- 3 retries for failed Read operations
- 5 parallel batches for large repos (>50 components)
- 10s discovery timeout, 20s extraction timeout
- 45s total hard timeout → return partial results
