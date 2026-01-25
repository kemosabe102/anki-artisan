# Documentation Context Loading Guide

**Purpose**: Define how agents load documentation and capture new knowledge
**Last Updated**: 2025-10-03

## Documentation Loading Pattern

### Always Loaded at Startup

Every agent automatically loads:

1. **Agent's own definition** (`.claude/agents/[agent-name].md`)
2. **CLAUDE.md** - Project context and quick reference
3. **Relevant workflow guides** from `.claude/docs/guides/` based on agent type

### Context Gathering Hierarchy

When an agent needs additional context or is uncertain about something:

#### Level 1: Internal Agent Documentation

- Check `.claude/docs/guides/` for agent-specific guidance
- Look for workflow patterns, best practices, templates
- Review agent categorization and naming conventions

#### Level 2: User Documentation

- Check `docs/04-guides/` for user-facing documentation
- Review feature specifications in `docs/01-planning/specifications/`
- Consult `docs/00-project/` for project-wide context

#### Level 3: MCP Servers

Use available MCP servers for external knowledge:

- **Context7** (`mcp__context7__*`) - Library documentation and code examples
- **Microsoft Docs** (`mcp__microsoft_docs_*`) - Azure and Microsoft technologies
- **Hugging Face** (`mcp__hugging-face__*`) - ML models and datasets

#### Level 4: Web Search

Only use web search when:

- Information not found in Levels 1-3
- Need latest updates (post knowledge cutoff)
- Researching external tools or services

#### Level 5: Documentation Learning

**If knowledge gap identified, capture it:**

## Documentation Learning Process

### 1. Identify Knowledge Gap

When encountering undocumented knowledge:

- Is this a recurring question?
- Would other agents benefit from this information?
- Is this project-specific or general Claude Code knowledge?

### 2. Check Existing Guides

Before creating new documentation:

```bash
# Search for related content
grep -r "keyword" .claude/docs/guides/
grep -r "keyword" docs/04-guides/
```

### 3. Update Existing Guide (Preferred)

If a related guide exists:

- Add new section with clear heading
- Include practical examples
- Update table of contents if present
- Add cross-references to related guides

Example update:

```markdown
## Newly Discovered Pattern

**Context**: Discovered while implementing [feature]
**Problem**: [What gap this fills]
**Solution**: [The pattern or knowledge]

### Example

[Practical example of usage]

### Related

- See also: [related-guide.md]
```

### 4. Create New Guide (If Truly New Area)

Only create new guide if:

- Completely new domain not covered elsewhere
- Would be 100+ lines of new content
- Multiple agents would reference it

New guide structure:

```markdown
# [Topic] Guide

**Purpose**: [Why this guide exists]
**Audience**: [Which agents/users need this]
**Last Updated**: [Date]

## Overview

[Brief introduction]

## Core Concepts

[Key information]

## Examples

[Practical usage]

## References

[Links to related guides]
```

### 5. Update Indices

After adding documentation:

- Update README.md in guide directory
- Add to relevant agent definitions if applicable
- Consider adding to CLAUDE.md if frequently needed

## Agent-Specific Loading

### Planning Agents (planning, architecture)

Always load:

- `.claude/docs/guides/planning/`
- Pain point validation guides
- Cost analysis frameworks

### Implementation Agents (development, test-runner)

Always load:

- `.claude/docs/guides/development/`
- Component almanac references
- Testing patterns

### Review Agents (code-quality, planning)

Always load:

- `.claude/docs/guides/validation/`
- Review checklists
- Quality metrics

## Documentation Maintenance

### Weekly Review

- Check for duplicate information across guides
- Identify frequently accessed sections
- Remove outdated content

### Monthly Consolidation

- Merge related small guides
- Update cross-references
- Archive obsolete guides

### Continuous Improvement

- Track which guides are most useful
- Identify gaps from agent queries
- Refactor based on usage patterns

## Quick Reference

```python
# Documentation loading priority
def get_context(query):
    # 1. Internal guides
    if found_in(".claude/docs/guides/"):
        return internal_guide

    # 2. User docs
    elif found_in("docs/04-guides/"):
        return user_doc

    # 3. MCP servers
    elif available_in_mcp():
        return mcp_result

    # 4. Web search
    elif web_search_needed():
        result = web_search(query)

    # 5. Capture learning
    if knowledge_gap_identified():
        update_or_create_guide(result)

    return result
```

## Best Practices

### DO ✅

- Check existing guides first
- Update rather than duplicate
- Include practical examples
- Cross-reference related content
- Keep guides focused and concise

### DON'T ❌

- Create guides for trivial knowledge
- Duplicate existing content
- Create deeply nested structures
- Mix agent and user documentation
- Forget to update indices

## Guide Templates

### For Patterns

- `.claude/docs/templates/pattern-guide-template.md`

### For Workflows

- `.claude/docs/templates/workflow-guide-template.md`

### For Troubleshooting

- `.claude/docs/templates/troubleshooting-guide-template.md`

---

**Remember**: Documentation should be living - update it when you learn something new!
