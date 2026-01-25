# Agent Phase Files

This directory contains OODA-aligned phase workflows for agents with multi-step processes.

## When to Include Phases

Include a `phases/` directory when the agent has:
- Multi-step workflows with distinct OBSERVE → ORIENT → DECIDE → ACT phases
- Different delegation patterns per phase
- Complex decision gates between phases
- Exit criteria that must be met before advancing

## Phase Files

| File | OODA Stage | Purpose |
|------|------------|---------|
| `phase-1-observe.md` | OBSERVE | Context gathering, pre-flight checks, input validation |
| `phase-2-orient.md` | ORIENT | Analysis, pattern matching, gap detection, options evaluation |
| `phase-3-decide.md` | DECIDE | Planning, risk assessment, approval gates, strategy selection |
| `phase-4-act.md` | ACT | Execution, delegation, validation, completion verification |

## Hybrid Model

**Core agent.md retains**:
- YAML frontmatter (name, description, tools, model, color)
- Core Behavior (identity, tone, anti-patterns, good patterns)
- Role & Boundaries
- Quality Standards
- Knowledge Base references
- Error Recovery patterns
- Technical Details

**Phase files contain**:
- Detailed workflow steps with numbered sub-steps
- Agent delegation tables per phase
- Phase-specific checklists
- Exit criteria with CQ weights
- Common mistakes per phase

## Template Usage

Copy templates to agent's `phases/` directory and customize:
1. Replace `{{agent-name}}` with actual agent name
2. Replace `[Domain-Specific Title]` with phase purpose
3. Fill in delegation tables with relevant agents
4. Define workflow steps for agent's domain
5. Set appropriate exit criteria weights

## Migration

Use `/analyze-agent {{agent-name}} --migrate` to automatically restructure an existing agent into phase-based format.
