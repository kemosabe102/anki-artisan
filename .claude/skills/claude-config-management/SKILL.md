---
name: claude-config-management
description: >
  CLAUDE.md and orchestration layer governance. Use when updating agent registry,
  modifying CLAUDE.md structure, managing agent color taxonomy, or retiring agents.
  Trigger keywords: CLAUDE.md, agent registry, config, orchestrator, retire agent.
---

# Claude Config Management Skill

Governance of CLAUDE.md and orchestration layer configuration.

---

## Quick Reference

| Task | Section | Protocol |
|------|---------|----------|
| Add new agent | Agent Registry | Add to selection guide + update README.md |
| Retire agent | Agent Registry | Move to deprecated/ + remove from tables |
| Update CLAUDE.md section | Structure Reference | Preserve version, update timestamp |
| Change agent color | Color Taxonomy | Match domain semantics |
| Add build command | Commands Section | Follow `uv run` pattern |
| Modify thresholds | Thresholds Section | Document rationale |

---

## CLAUDE.md Structure

### Section Order (Mandatory)

Maintain sections in this exact order:

1. **Header** - Version, Last Updated, Project name
2. **Environment** - Python version, package manager, paths
3. **Commands** - Build commands table
4. **Code Style** - Typing, naming, formatting rules
5. **Architecture** - Directory structure diagram
6. **Orchestrator Identity** - Cardinal rule, delegation directives
7. **State Tracking** - Phase identification, CQ status
8. **Phase Transitions** - Exit criteria, user signals
9. **Plan Mode** - Agent assignment requirements
10. **Thresholds** - CQ/ASC gates with actions
11. **Phase-Based Operations** - OODA workflow details
12. **BANNED Operations** - Forbidden commands and patterns
13. **Agent Selection** - Selection paths, inheritance rules
14. **Skill Delegation Model** - Skill vs agent boundaries
15. **Multi-Agent Patterns** - Parallel/sequential rules
16. **Research Strategy** - Cost-optimized research patterns
17. **File Operations** - Tool selection, phase restrictions
18. **Critical Warnings** - Platform-specific gotchas
19. **ALWAYS Directives** - Mandatory behaviors
20. **Communication Style** - Tone, verbosity levels
21. **Documentation Index** - Key file references

### Version Management

Update version using semantic versioning:
- **MAJOR** (X.0.0): Breaking changes to orchestration behavior
- **MINOR** (0.X.0): New sections, agent additions, threshold changes
- **PATCH** (0.0.X): Typo fixes, clarifications, formatting

**Update Protocol**:
```
1. Increment version number
2. Update "Last Updated" date
3. Document change in commit message: "docs(claude): <change summary>"
```

---

## Agent Registry Protocol

### Adding a New Agent

**Prerequisites**:
- Agent definition file created in `.claude/agents/<domain>/<agent-name>.md`
- Agent follows base-agent-pattern.md structure
- Frontmatter includes: name, description, model, color, tools

**Steps**:

1. **Update Agent Selection Guide** (`.claude/docs/01-guides/agents/agent-selection-guide.md`):
   - Add to appropriate Framework 1 domain section
   - Include work type recognition patterns
   - Add to cross-domain table if applicable

2. **Update Agent README** (`.claude/agents/README.md`):
   - Add to appropriate domain coordinator or specialist section
   - Follow table format: `| agent-name | Purpose description |`

3. **Assign Color** (see Color Taxonomy section):
   - Match domain semantics
   - Verify no conflicts with existing agents

4. **Verify Integration**:
   - Check delegation examples work
   - Confirm orchestrator can route to agent

### Retiring an Agent

**Decision Criteria** (retire when ANY apply):
- Functionality absorbed by domain coordinator
- Replaced by skill-based approach
- No delegations in past 30 days
- Superseded by more capable agent

**Steps**:

1. **Move to Deprecated**:
   ```
   .claude/agents/<domain>/<agent>.md
   → .claude/agents/deprecated/<domain>/<agent>/<agent>.md
   ```

2. **Update Agent Selection Guide**:
   - Remove from active agent tables
   - Add deprecation notice with replacement agent

3. **Update Agent README**:
   - Remove from active sections
   - Add to deprecated section with superseding info

4. **Update CLAUDE.md** (if agent was in delegation table):
   - Remove from User Request Type table
   - Update any references to retired agent

5. **Preserve Documentation**:
   - Keep agent definition for reference
   - Move supporting docs to deprecated folder


---

## Agent Color Taxonomy

Colors provide visual domain identification in Claude Code UI.

### Color Assignments by Domain

| Color | Domain | Agents | Semantic Meaning |
|-------|--------|--------|------------------|
| **green** | Coding | development, code-quality, architecture, claude-code-ecosystem | Creation, implementation, growth |
| **blue** | Planning | planning, research | Strategy, analysis, planning |
| **orange** | Workflow | workflow | Configuration, automation |
| **purple** | Infrastructure | observability, deployment-release, platform-infrastructure | Operations, monitoring |
| **yellow** | Analysis | context-readiness-assessor, contingency-planner | Assessment, warning, attention |
| **cyan** | Utility | intent-analyzer, context-optimizer | Support, optimization |
| **red** | Security | sast-scanner | Critical, security-sensitive |
| **gray** | Specialists | Various domain specialists | Neutral, specialized tasks |

### Color Selection Rules

1. **Match Domain First**: Use established color for domain
2. **No Duplicates Within Domain**: Each agent in a domain uses same color
3. **Semantic Consistency**: Color meaning should align with agent purpose
4. **Contrast Requirement**: Avoid similar colors for frequently co-used agents

### Adding New Colors

Reserve new colors for genuinely new domains. Prefer:
- Existing domain colors for related agents
- Gray for specialized one-off agents
- Request team discussion for new color introduction


---

## Build Commands Standards

### Command Table Format

All commands in CLAUDE.md Commands section follow this pattern:

```markdown
| Task | Command |
|------|---------|
| [Task Name] | `[executable] [args]` |
```

### Command Requirements

1. **Use UV Runner**: All Python commands use `uv run`
   - Correct: `uv run pytest`
   - Wrong: `pytest`, `python -m pytest`

2. **No Shell Constructs**: Commands must work without shell interpretation
   - Correct: `uv run ruff check .`
   - Wrong: `uv run ruff check . && echo "Done"`

3. **Absolute Paths**: When paths needed, use project-relative
   - Correct: `pytest tests/unit/`
   - Wrong: `pytest ./tests/unit/`

4. **Task Naming**: Use parenthetical qualifiers for variants
   - Primary: `Test`
   - Variants: `Test (unit)`, `Test (coverage)`, `Test (integration)`

### Adding New Commands

1. Determine task category (Test, Lint, Format, Build, Deploy)
2. Follow UV pattern: `uv run <tool> <args>`
3. Add to Commands table in correct position (alphabetical by Task)
4. Document any requirements inline


---

## Threshold Management

### Current Thresholds

| Metric | Gate | Action |
|--------|------|--------|
| CQ (Context Quality) | >= 0.85 | Proceed to DECIDE |
| CQ | < 0.70 | Spawn exploration agents |
| ASC (Agent Selection Confidence) | >= 0.80 | Use agent |
| ASC | < 0.50 | ESCALATE to user |

### Modifying Thresholds

**When to Adjust**:
- False positive rate > 10% (threshold too low)
- False negative rate > 10% (threshold too high)
- New capability requires different sensitivity

**Change Protocol**:
1. Document current threshold and observed issue
2. Propose new threshold with rationale
3. Update CLAUDE.md Thresholds section
4. Update orchestrator-thresholds.md with formula details
5. Monitor for 1 week, adjust if needed

**Never Change Without**:
- Documented evidence of threshold inadequacy
- Clear rationale for new value
- Rollback plan if degradation observed


---

## Agent Frontmatter Standards

### Required Fields

Every agent `.md` file must include this frontmatter:

```yaml
---
name: agent-name
description: >
  Brief description of agent purpose and capabilities.
  Include: primary use cases, trigger keywords.
  Exclude: what NOT to use agent for.
model: opus | sonnet
color: green | blue | orange | purple | yellow | cyan | red | gray
tools: [comma-separated list of allowed tools]
---
```

### Field Specifications

**name**: Kebab-case, matches filename without .md extension

**description**: 
- First sentence: Core purpose (< 20 words)
- Second part: "Use for:" with 3-5 trigger scenarios
- Third part: "NOT for:" with clear boundaries
- Keep under 200 characters for UI display

**model**:
- `opus`: Complex reasoning, multi-step tasks, research
- `sonnet`: Fast responses, simple tasks, validation

**color**: See Color Taxonomy section

**tools**: Only tools agent actually needs
- Read-only agents: `Read, Glob, Grep`
- Implementation agents: Add `mcp__desktop-commander__*`
- Research agents: Add `mcp__context7__*`, `mcp__perplexity__*`

### Invalid Fields (NEVER Use)

These fields are NOT recognized and will be ignored:
- `version` - Use CLAUDE.md version instead
- `maturity` - Not a valid frontmatter field
- `temperature` - Model parameter, not frontmatter
- `max_tokens` - Model parameter, not frontmatter


---

## Decision Criteria: Add vs Retire

### When to Add a New Agent

**Add agent when ALL apply**:
- [ ] Distinct domain expertise not covered by existing agents
- [ ] Will be delegated to >= 5 times per week (projected)
- [ ] Cannot be achieved by adding skill to existing coordinator
- [ ] Clear boundaries that don't overlap with existing agents

**Prefer skill over agent when**:
- Knowledge/methodology can be reused across agents
- No unique tool requirements
- Read-only reference material
- Domain coordinator already exists

### When to Retire an Agent

**Retire when ANY apply**:
- [ ] Functionality fully absorbed by domain coordinator
- [ ] < 3 delegations in past 30 days
- [ ] Replaced by skill-based approach
- [ ] Superseded by more capable/general agent
- [ ] Maintaining causes more overhead than value

**Retirement Indicators**:
- Orchestrator consistently routes around agent
- Users explicitly request alternative agents
- Agent output quality lower than alternatives
- Domain has been consolidated into coordinator


---

## Metadata Standards

### Agent Definition Metadata

Located in agent frontmatter and README.md:

| Field | Location | Update Frequency |
|-------|----------|------------------|
| name | Frontmatter | Never (immutable) |
| description | Frontmatter | On capability change |
| model | Frontmatter | On performance needs |
| color | Frontmatter | On domain reassignment |
| tools | Frontmatter | On capability change |
| Purpose | README table | On role change |

### CLAUDE.md Metadata

| Field | Location | Format |
|-------|----------|--------|
| Version | Header | X.Y.Z (semver) |
| Last Updated | Header | YYYY-MM-DD |
| Project | Header | Human-readable name |

### Commit Message Format

For CLAUDE.md and agent config changes:

```
docs(claude): <summary of change>

- Detail 1
- Detail 2

Version: X.Y.Z -> X.Y.Z
```


---

## Integration Points

### Files Affected by Config Changes

| Change Type | Files to Update |
|-------------|-----------------|
| Add agent | Agent .md, README.md, agent-selection-guide.md |
| Retire agent | Move to deprecated/, README.md, agent-selection-guide.md |
| Update CLAUDE.md section | CLAUDE.md only |
| Add command | CLAUDE.md Commands section |
| Modify threshold | CLAUDE.md, orchestrator-thresholds.md |
| Change color | Agent frontmatter only |

### Dependency Order

When making changes, update in this order:
1. Agent definition files (source of truth)
2. README.md (registry)
3. agent-selection-guide.md (routing rules)
4. CLAUDE.md (if orchestrator-level impact)

### Session Restart Requirement

Changes to these require Claude Code session restart:
- New `.claude/agents/*.md` files
- New `.claude/hooks/*.py` files
- Modified agent frontmatter (name, tools)

Changes that take effect immediately:
- CLAUDE.md content updates
- Agent body content (not frontmatter)
- Skill file updates


---

## Validation Checklist

Before completing any config management task, verify:

### Adding Agent
- [ ] Agent .md file created in correct domain directory
- [ ] Frontmatter includes all required fields (name, description, model, color, tools)
- [ ] Color matches domain taxonomy
- [ ] README.md updated with new agent entry
- [ ] agent-selection-guide.md updated with routing rules
- [ ] No tool conflicts with existing agents
- [ ] Description includes "Use for" and "NOT for" sections

### Retiring Agent
- [ ] Agent moved to `.claude/agents/deprecated/<domain>/`
- [ ] README.md deprecated section updated
- [ ] agent-selection-guide.md references removed/updated
- [ ] Replacement agent documented
- [ ] No orphaned references in CLAUDE.md

### Updating CLAUDE.md
- [ ] Version incremented appropriately (major/minor/patch)
- [ ] Last Updated date changed
- [ ] Section order preserved
- [ ] No broken internal references
- [ ] Commit message follows format

### Modifying Thresholds
- [ ] Change rationale documented
- [ ] Both CLAUDE.md and orchestrator-thresholds.md updated
- [ ] Rollback plan identified
- [ ] Monitoring plan in place


---

## Anti-Patterns (NEVER DO)

- Edit CLAUDE.md without incrementing version
- Add agent without updating README.md and selection guide
- Use invalid frontmatter fields (version, maturity, temperature)
- Create agents that duplicate existing coordinator functionality
- Retire agents without documenting replacement
- Change thresholds without evidence and rationale
- Bypass color taxonomy conventions
- Create circular references in agent selection routing

---

## References

Detailed reference documentation:
- `references/claude-md-template.md` - Full CLAUDE.md section templates
- `references/color-taxonomy.md` - Complete color assignment rationale

---

## Related Resources

| Resource | Purpose |
|----------|---------|
| `.claude/agents/README.md` | Agent catalog and registry |
| `.claude/docs/01-guides/agents/agent-selection-guide.md` | Routing frameworks |
| `.claude/docs/00-core/orchestrator-thresholds.md` | Threshold formulas |
| `.claude/docs/01-guides/agents/base-agent-pattern.md` | Agent template |

