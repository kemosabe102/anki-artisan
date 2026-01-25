---
name: prompt-structural-analysis
description: >
  16-criterion structural validation for agent prompts. Use when reviewing prompt
  structure, detecting anti-patterns, or auditing agent definitions.
  Trigger keywords: prompt structure, structural analysis, anti-patterns, prompt audit.
---

# Prompt Structural Analysis

> **Systematic 16-criterion structural validation for Claude Code agent prompts with anti-pattern detection.**

---

## When to Use This Skill

**Trigger Keywords**: "prompt structure", "structural analysis", "anti-patterns", "prompt audit", "agent review", "structural validation"

**Use For**:
- Structural validation of agent prompts (16 criteria)
- Anti-pattern detection and classification (12 patterns)
- Agent definition auditing
- Pre-deployment prompt review

**NOT For**:
- Full 7-framework evaluation (use claude-code-ecosystem agent)
- Token optimization analysis (use claude-code-ecosystem agent)
- Creating/modifying agents (use claude-code-ecosystem)

---

## Core Methodology

### Evidence-Based Findings

**Every finding MUST include**:
- File:line citation (e.g., `agent.md:41`)
- Pass/Fail determination
- Specific evidence from the file
- Confidence score (0.0-1.0)

**Citation Format**:
```
agent.md:41 - PASS: Single responsibility found "Analyzes code quality"
agent.md:15-20 - FAIL: No boundaries section documented
```

### Scoring Model

**Pass** = 1 point | **Fail** = 0 point | **N/A** = Not counted

**Final Score**: X/16 (or X/N if criteria marked N/A)

---

## 16-Criterion Structural Checklist

### Category 1: Single Responsibility & Boundaries (3 criteria)

| # | Criterion | PASS | FAIL |
|---|-----------|------|------|
| 1 | Single Responsibility | One clear purpose in Role & Boundaries | Multiple responsibilities or unclear |
| 2 | Scope Discipline | Explicit "NOT for" boundaries | No boundaries documented |
| 3 | Domain Scope Limits | Restricted to specific paths/types | Unlimited or cross-domain |

### Category 2: Schema & Pattern Compliance (4 criteria)

| # | Criterion | PASS | FAIL |
|---|-----------|------|------|
| 4 | Frontmatter Compliance | Valid Claude Code fields only | Invalid/undocumented fields |
| 5 | Schema Compliance | Extends base-agent.schema.json | No schema reference |
| 6 | Base Pattern Extension | Extends base-agent-pattern.md | Duplicates base content |
| 7 | Two-State Model | SUCCESS/FAILURE documented | Missing state model |

### Category 3: Tool & Workflow Architecture (3 criteria)

| # | Criterion | PASS | FAIL |
|---|-----------|------|------|
| 8 | Performance-First Tools | Tool tier matches task complexity | Heavy tools for simple tasks |
| 9 | Workflow Structure | Complete phase documentation | Missing workflow phases |
| 10 | File Operation Protocol | References protocol, follows standards | No protocol reference |

### Category 4: Communication Quality (3 criteria)

| # | Criterion | PASS | FAIL |
|---|-----------|------|------|
| 11 | Tool Descriptions | Clear for unfamiliar users | Vague or assumes knowledge |
| 12 | Explicit Context | All decisions documented | Relies on implicit knowledge |
| 13 | High-Signal Information | Actionable outputs specified | Generic outputs |

### Category 5: Integration Patterns (3 criteria)

| # | Criterion | PASS | FAIL | N/A Condition |
|---|-----------|------|------|---------------|
| 14 | Four-Component Delegation | Complete delegation context | Missing components | Not orchestrator |
| 15 | Query Classification | Query types with strategies | Single strategy | Not research agent |
| 16 | Parallel Execution Awareness | Concurrency documented | No guidance | - |

**Full criteria definitions**: [references/structural-criteria.md](references/structural-criteria.md)

---

## Anti-Pattern Detection

### Severity Levels

| Level | Action | Examples |
|-------|--------|----------|
| **CRITICAL** | Immediate fix | Schema non-compliance, missing error recovery, security gaps |
| **MAJOR** | Fix before deploy | Tool bloat, missing base pattern, kitchen-sink prompts |
| **MINOR** | Fix when convenient | Suboptimal wording, minor structure issues |

### Quick Detection Patterns

```bash
# AP-1: Tool Initialization Bloat
Grep("^tools:", agent_path)  # Count heavy tools (>3 = bloat)

# AP-3: Missing Base Pattern
Grep("base.agent.pattern", agent_path, "-i")  # No match = missing

# AP-9: Missing Error Recovery
Grep("failure|error.recovery", agent_path, "-i")  # No match = missing

# AP-12: Full Path Doc References
Grep("\\.claude/docs/|docs/[0-9]+-", agent_path)  # Any match = violation
```

### Anti-Pattern Summary

| ID | Name | Severity |
|----|------|----------|
| AP-1 | Tool Initialization Bloat | MAJOR |
| AP-2 | Scope Creep | CRITICAL |
| AP-3 | Missing Base Pattern | MAJOR |
| AP-4 | Schema Non-Compliance | CRITICAL |
| AP-5 | Vague Tool Descriptions | MAJOR |
| AP-6 | No Termination Rules | MAJOR |
| AP-7 | MultiEdit on Large Files | CRITICAL |
| AP-8 | Parallel Write Operations | CRITICAL |
| AP-9 | Missing Error Recovery | CRITICAL |
| AP-10 | No Security Validation | CRITICAL |
| AP-11 | Kitchen-Sink Prompts | MAJOR |
| AP-12 | Full Path Doc References | MAJOR |

**Full anti-pattern catalog**: [references/anti-pattern-catalog.md](references/anti-pattern-catalog.md)

---

## Analysis Workflow

### Phase 1: Load & Baseline
1. Read target agent file completely
2. Extract frontmatter fields
3. Count total lines for size compliance

### Phase 2: Structural Validation
1. Apply 16 criteria sequentially
2. Collect file:line evidence for each
3. Mark PASS/FAIL/N/A per criterion
4. Calculate structural score (X/16)

### Phase 3: Anti-Pattern Scan
1. Run detection patterns for each anti-pattern
2. Classify severity (Critical/Major/Minor)
3. Collect evidence with file:line citations
4. Generate fix recommendations

### Phase 4: Report Generation
Output structured findings:
```json
{
  "agent_path": "path/to/agent.md",
  "structural_score": "14/16",
  "criteria": [
    {"id": 1, "name": "Single Responsibility", "status": "PASS", "evidence": "agent.md:12", "confidence": 0.95}
  ],
  "anti_patterns": [
    {"id": "AP-3", "severity": "MAJOR", "evidence": "agent.md:1-150", "fix": "Add base pattern extension"}
  ]
}
```

---

## Output Format

### Structural Analysis Report

```markdown
## Structural Analysis: {agent_name}

**Score**: {X}/16 ({percentage}%)
**Anti-Patterns Found**: {count} ({critical} critical, {major} major)

### Criteria Results

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Single Responsibility | PASS | agent.md:12 - "Analyzes code quality" |
| 2 | Scope Discipline | FAIL | No boundaries section found |
...

### Anti-Patterns Detected

| ID | Name | Severity | Evidence | Fix |
|----|------|----------|----------|-----|
| AP-3 | Missing Base Pattern | MAJOR | Lines 1-150 | Add base-agent-pattern.md extension |
...

### Recommendations (Priority Order)
1. [CRITICAL] Add error recovery documentation
2. [MAJOR] Extend base-agent-pattern.md to save ~1,150 tokens
3. [MAJOR] Add explicit boundaries section
```

---

## References

- **Structural Criteria**: [references/structural-criteria.md](references/structural-criteria.md)
- **Anti-Pattern Catalog**: [references/anti-pattern-catalog.md](references/anti-pattern-catalog.md)
