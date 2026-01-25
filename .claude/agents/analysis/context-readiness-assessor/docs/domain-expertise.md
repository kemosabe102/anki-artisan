# Context Readiness Assessor - Domain Expertise

## Context_Quality Component Scoring Rubrics

### Domain_Familiarity (40% weight)

**Definition**: Understanding of technology domain, business context, and project patterns

| Score | Level | Indicators |
|-------|-------|------------|
| 1.0 | Expert | Deep expertise, complete understanding, prior successful work |
| 0.7-0.9 | Strong | Solid experience, patterns clear, some prior exposure |
| 0.4-0.6 | Basic | Some experience, patterns partially understood |
| 0.0-0.3 | Unfamiliar | No prior experience, unclear patterns, novel domain |

**Research Triggers**:
- Score < 0.85 → researcher-codebase (domain patterns)
- Novel technology → researcher-external (official docs)
- Business context unclear → technical-pm (alignment)

---

### Pattern_Clarity (30% weight)

**Definition**: Recognition of existing patterns in codebase and architectural approaches

| Score | Level | Indicators |
|-------|-------|------------|
| 1.0 | Complete | All patterns documented, clear examples, consistent |
| 0.7-0.9 | Good | Most patterns clear, some examples, mostly consistent |
| 0.4-0.6 | Partial | Some patterns documented, few examples |
| 0.0-0.3 | Unclear | Patterns undocumented, no examples, inconsistent |

**Research Triggers**:
- Score < 0.85 → researcher-codebase (pattern discovery)
- Architecture unclear → architecture-review (patterns)
- Quality patterns needed → python-code-reviewer (standards)

---

### Dependency_Understanding (20% weight)

**Definition**: Knowledge of component interactions, integration points, external dependencies

| Score | Level | Indicators |
|-------|-------|------------|
| 1.0 | Complete | All dependencies mapped, interfaces clear |
| 0.7-0.9 | Good | Most dependencies known, key integrations understood |
| 0.4-0.6 | Partial | Some dependencies identified, critical integrations unclear |
| 0.0-0.3 | Minimal | Dependencies unknown, integration points unmapped |

**Research Triggers**:
- Score < 0.85 → researcher-codebase (dependency mapping)
- Tech debt concerns → tech-debt-investigator (coupling)
- External integrations → researcher-external (library docs)

---

### Risk_Awareness (10% weight)

**Definition**: Identification of failure modes, security concerns, edge cases

| Score | Level | Indicators |
|-------|-------|------------|
| 1.0 | Comprehensive | All risks identified, mitigations planned |
| 0.7-0.9 | Good | Major risks identified, basic mitigations |
| 0.4-0.6 | Partial | Some risks identified, critical modes unclear |
| 0.0-0.3 | Minimal | Risks unknown, failure modes unidentified |

**Research Triggers**:
- Score < 0.85 → tech-debt-investigator (risk analysis)
- Security-critical → researcher-external (OWASP best practices)
- Specification validation → spec-reviewer (requirements)

---

## Gap-to-Agent Mapping (10 Available Agents)

| Gap Type | Primary Agent | When to Use |
|----------|---------------|-------------|
| Domain patterns unclear | researcher-codebase | Domain_Familiarity < 0.85, Pattern_Clarity < 0.85 |
| Best practices unknown | researcher-external | Novel approach, security-critical, Domain < 0.3 |
| Library/framework usage | researcher-external | External dependencies, API usage, novel library |
| Multi-source research | researcher-lead | Complex research, multiple gaps, strategic planning |
| Technical debt risks | tech-debt-investigator | Risk_Awareness < 0.85, coupling concerns |
| Quality patterns | python-code-reviewer | Pattern_Clarity < 0.85, quality standards unclear |
| Specification validation | spec-reviewer | Requirements unclear, SPEC.md analysis needed |
| Architectural patterns | architecture-review | Pattern_Clarity < 0.3, architecture redesign |
| Business context | technical-pm | Domain_Familiarity < 0.4, business alignment |
| Recent changes | git-github | Change analysis, recent patterns, git history |

---

## Research Coordination Strategy

### Parallel Research (max 5 agents simultaneously)
- Use when: Independent gaps across different domains
- Example: researcher-codebase + researcher-external + tech-debt-investigator

### Sequential Research (wait for dependencies)
- Use when: Findings from one agent inform next research
- Example: researcher-codebase findings → architecture-review for deeper analysis

### Hard Caps (Prevent Over-Coordination)
- Max 10 agent invocations total across all iterations
- Max 5 agents in parallel (orchestrator limit)
- 5-minute timeout per iteration
- Stop if delta < 0.1 (diminishing returns)

---

## Research Synthesis & Compression

**Target**: 10:1 compression ratio (10K+ input → <1K output)

**Process**:
1. Collect findings from all coordinated agents
2. Extract common themes and patterns
3. Rank by impact on Context_Quality components
4. Compress to essential insights only
5. Track attribution (which agent provided what)

**Output Structure**:
```json
{
  "research_completed": [
    {
      "agent": "researcher-codebase",
      "findings_summary": "3 similar caching implementations in packages/core/",
      "confidence": 0.85,
      "impact_on_components": {
        "domain_familiarity": "+0.2",
        "pattern_clarity": "+0.3"
      }
    }
  ]
}
```

---

## Related Documentation

- [Frameworks & Iteration Management](frameworks.md) - Hermeneutic assessment, iteration logic
- [Assessment Examples](../examples/assessment-examples.md) - 3 worked scenarios
- [Schema Contract](../schemas/context-readiness-assessor.schema.json) - Input/output validation
- [Main Agent Definition](../context-readiness-assessor.md) - Core behavior and workflow
