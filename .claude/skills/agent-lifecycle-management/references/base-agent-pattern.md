# Base Agent Pattern Reference

This document provides a quick reference to the Base Agent Pattern. For the complete pattern, see the canonical source.

## Canonical Source

**Location**: `.claude/docs/01-guides/agents/base-agent-pattern.md`

## Overview

The Base Agent Pattern establishes the universal baseline for all Claude Code agents. It contains 6 core patterns that appear in 15+ agents.

## Core Patterns Inherited

| Pattern | Purpose |
|---------|---------|
| Knowledge Base Integration | Context gathering hierarchy, path rules |
| Pre-Flight Checklist | Task assessment, ambiguity detection |
| Core Workflow Structure | 6-phase lifecycle (Analysis → Validation) |
| Error Recovery Patterns | Retry logic, graceful degradation |
| Parallel Execution Awareness | When to parallelize/serialize |
| Validation Checklist | Lifecycle, core requirements, QA |

## Extension Mechanism

Agents extend the base pattern:

```markdown
## Base Agent Pattern Extension

**This agent EXTENDS**: `.claude/docs/01-guides/agents/base-agent-pattern.md`

**Specialized Focus**: [Agent's unique capability]

**Inherited from Base Pattern**:
- Knowledge Base Integration
- Pre-Flight Checklist
- Core Workflow Structure
- Error Recovery Patterns
- Parallel Execution Awareness
- Validation Checklist
```

## Override Pattern

To override specific sections:

```markdown
**Extends**: base-agent-pattern.md ([Section Name])

**Agent-Specific Additions:**
- [Specialized content]
```

## Token Savings

~1,140 tokens saved per agent through inheritance.

---

**Full Documentation**: `.claude/docs/01-guides/agents/base-agent-pattern.md`
