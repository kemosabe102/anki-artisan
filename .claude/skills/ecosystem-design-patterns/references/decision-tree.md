# Agent vs Skill Decision Tree

Decision flowchart for choosing between agent and skill when extending the ecosystem.

---

## Primary Decision Flow

```
START: "I need to add new capability to the ecosystem"
         │
         ▼
    ┌────────────────────────────────────────┐
    │ Does this capability need to OWN       │
    │ a domain (files, lifecycle, state)?    │
    └────────────────────────────────────────┘
         │                    │
        YES                  NO
         │                    │
         ▼                    ▼
    ┌─────────┐         ┌────────────────────────────────────────┐
    │  AGENT  │         │ Is this reusable methodology or        │
    └─────────┘         │ decision framework used by many agents?│
                        └────────────────────────────────────────┘
                             │                    │
                            YES                  NO
                             │                    │
                             ▼                    ▼
                        ┌─────────┐         ┌─────────────────────┐
                        │  SKILL  │         │ Consider embedding  │
                        └─────────┘         │ in existing agent   │
                                            └─────────────────────┘
```

---

## Secondary Criteria (When Primary Is Ambiguous)

### Complexity Assessment

| Factor | Points for Agent | Points for Skill |
|--------|------------------|------------------|
| Multi-phase workflow | +2 | 0 |
| File modification needed | +2 | 0 |
| Cross-domain applicability | 0 | +2 |
| Reusable by multiple agents | 0 | +2 |
| Needs persistent state | +2 | 0 |
| Pure decision logic | 0 | +2 |
| Domain ownership required | +2 | 0 |
| Guidance/methodology focus | 0 | +2 |

**Scoring**: Sum points. Higher score wins. Tie = default to skill (lower maintenance).

---

## Decision Examples

### Example 1: "Add Python code review capability"

**Analysis**:
- Domain ownership? YES (owns review workflow)
- File modification? YES (adds review comments, suggests fixes)
- Multi-phase? YES (analyze -> critique -> suggest)

**Decision**: AGENT (code-quality)

### Example 2: "Add debugging methodology"

**Analysis**:
- Domain ownership? NO (doesn't own files)
- Reusable? YES (any agent debugging uses this)
- Cross-domain? YES (applies to any code)
- Pure methodology? YES (8-step process)

**Decision**: SKILL (debugging-methodology)

### Example 3: "Add Git workflow patterns"

**Analysis**:
- Domain ownership? YES (owns commit/PR workflow)
- File modification? YES (commits, branches)
- BUT: Core patterns are reusable guidance

**Decision**: HYBRID
- Agent: source-control (executes git operations)
- Skill: git-workflow (methodology for when to commit, branch naming)

---

## Edge Cases

### When to Split Agent + Skill

Create BOTH when:
1. Execution requires agent (file ops, state)
2. Methodology is independently valuable
3. Other agents could use the methodology

**Pattern**: Agent USES skill for guidance, skill provides methodology.

### When to Embed in Existing Agent

Embed (don't create new) when:
1. Capability is narrow extension of existing agent
2. Would create <100 lines if standalone
3. Only one agent would ever use it

### When to Create Reference Document (Not Skill)

Create reference doc when:
1. Pure data/lookup table
2. No decision framework
3. Static information (schemas, API refs)

---

## Quick Decision Matrix

| Scenario | Create |
|----------|--------|
| "I want agents to follow X methodology" | Skill |
| "I need to modify files in X domain" | Agent |
| "Multiple agents need this decision framework" | Skill |
| "This capability needs its own lifecycle" | Agent |
| "This is just reference data" | Reference doc |
| "This extends an existing agent's job" | Embed in agent |
