# Analyze Command Documentation

Supporting documentation for the `/analyze-command` slash command.

**Version**: 1.0.0 | **Last Updated**: 2025-12-21

---

## Purpose

The `/analyze-command` command performs comprehensive analysis of slash command workflows, evaluating structure, delegation patterns, error handling, and optimization opportunities.

---

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed P0-P8 phase documentation | Understanding phase behavior, customizing analysis |
| `delegation-patterns.md` | Exact Task() call syntax for all phases | Implementing delegation, debugging agent calls |
| `pre-mortem-phase.md` | P4 failure mode analysis for commands | Predictive failure identification |
| `scamper-optimization.md` | P8 SCAMPER optimization techniques | Command workflow optimization |

---

## Quick Navigation

- **Need exact delegation syntax?** -> `delegation-patterns.md`
- **Understanding analysis phases?** -> `workflow-phases.md`
- **Predictive failure analysis?** -> `pre-mortem-phase.md`
- **Workflow optimization?** -> `scamper-optimization.md`

---

## Relationship to Main Command

The main `/analyze-command` command file provides:
- Concise workflow overview
- Mode/argument reference
- Quick delegation syntax
- Error recovery table

These docs provide the **detailed implementation** referenced from the main file.

---

## Dependencies

- `contingency-planner` agent (P4 pre-mortem)
- `claude-code-ecosystem` agent (P1 analysis)
- `documentation` agent (P1 token analysis)
- `tech-debt-investigator` agent (P1 debt analysis)

---

## Schema Reference

See `../schemas/command-analysis.schema.json` for the complete output schema.
