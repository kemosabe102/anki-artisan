---
title: "Agent Framework Evaluation Workflow"
date: 2025-11-26
status: ACTIVE
tags: [agents, frameworks, evaluation, workflow]
---

# Agent Framework Evaluation Workflow

**Purpose**: Operational guide for evaluating all agents against appropriate thinking frameworks

**Audience**: Orchestrator, claude-code-ecosystem, claude-code-ecosystem

**Prerequisites**: `00-core/frameworks/README.md` (framework definitions and agent mappings)

---

## Quick Reference

**Evaluation Command**: Use `/analyze-agent <agent-name>` to run comprehensive analysis including framework alignment

**Direct Framework Check**:
```
Task(claude-code-ecosystem, "Evaluate framework alignment for .claude/agents/dev-tools/<agent-name>.md 
     using 00-core/frameworks/README.md. Check if agent uses appropriate framework for its domain.")
```

---

## Evaluation Process

### Phase 1: Identify Agent Domain

| Domain Category | File Path Pattern | Example Agents |
|----------------|-------------------|----------------|
| Research | `.claude/agents/research/**` | researcher-lead, researcher-external |
| Implementation | `packages/**` focus | development |
| Analysis/Review | Review-focused agents | code-quality, claude-code-ecosystem |
| Planning/Design | Spec/Plan focus | planning, architecture |
| Debugging | Error/debug focus | debugger |
| Optimization | Token/efficiency focus | context-optimizer, documentation |

### Phase 2: Match to Expected Framework

**From `00-core/frameworks/README.md` Agent-Framework Matching Guide**:

| Agent Category | Primary Framework | Secondary |
|---------------|-------------------|-----------|
| Research | ReACT | CAGEERF |
| Implementation | CAGEERF | ReACT |
| Analysis/Review | 5W1H / DMAIC | SCAMPER |
| Planning/Design | 5W1H / CAGEERF | First Principles |
| Debugging | ReACT | 5 Whys + Systems |
| Optimization | SCAMPER | DMAIC |

### Phase 3: Check Framework Integration

**Evidence Checklist**:

1. [ ] **Declaration**: Agent mentions framework name in Methodology/Reasoning section
2. [ ] **Application**: Framework steps visible in workflow operations
3. [ ] **Consistency**: Framework applied throughout, not just mentioned once
4. [ ] **Appropriateness**: Framework matches agent's actual work type

### Phase 4: Score Assignment

| Grade | Criteria |
|-------|----------|
| **A** | Optimal framework, fully integrated, all steps visible |
| **B** | Good framework choice, minor application gaps |
| **C** | Acceptable framework, loosely applied |
| **D** | Framework mismatch or barely applied |
| **F** | No framework when needed, or completely wrong choice |

---

## Batch Evaluation

### All Agents Evaluation

```bash
# List all agents to evaluate
ls .claude/agents/**/*.md

# Run batch evaluation (orchestrator coordinates)
for agent in .claude/agents/dev-tools/*.md .claude/agents/research/*.md .claude/agents/investing/*.md; do
  echo "Evaluating: $agent"
  # Delegate to claude-code-ecosystem for each
done
```

### Priority Order for Evaluation

1. **Critical Path Agents** (high usage, complex work):
   - development
   - debugger
   - researcher-lead
   - planning

2. **Review/Quality Agents** (evaluation accuracy matters):
   - code-quality
   - claude-code-ecosystem
   - claude-code-ecosystem

3. **Specialist Agents** (domain-specific):
   - postgres-timescale-specialist
   - deployment-release
   - grafana-dashboard-builder

4. **Support Agents** (lower impact):
   - documentation
   - planning

---

## Framework Recommendation Template

When an agent lacks appropriate framework, use this template to recommend integration:

```markdown
## Framework Recommendation for [agent-name]

**Current State**: [No framework / Wrong framework / Partial framework]

**Recommended Framework**: [Framework Name]

**Rationale**: [Agent domain] + [Work type] = [Framework] per 00-core/frameworks/README.md

**Integration Points**:
1. Add to Methodology section: Reference [Framework] with link to catalog
2. Update Reasoning Approach: Apply [Framework] steps explicitly
3. Modify Workflow Operations: Structure around [Framework] phases

**Example Application** (for this agent):
```
[Show how the framework would look applied to this agent's specific workflow]
```

**Priority**: [High/Medium/Low] based on agent usage and impact
```

---

## Evaluation Report Format

```json
{
  "agent_name": "agent-name",
  "domain": "research|implementation|analysis|planning|debugging|optimization",
  "expected_framework": "Framework Name",
  "current_framework": "Framework Name or null",
  "grade": "A|B|C|D|F",
  "evidence": {
    "declaration": "file:line - evidence text or null",
    "application": "file:line-line - evidence text or null",
    "consistency": "pass|partial|fail",
    "appropriateness": "optimal|acceptable|mismatch"
  },
  "recommendation": "null or improvement text",
  "priority": "high|medium|low"
}
```

---

## Integration with /analyze-agent

The `/analyze-agent` command automatically includes framework evaluation as part of its multi-agent analysis. The workflow is:

1. **claude-code-ecosystem** evaluates framework alignment as Dimension 7
2. **claude-code-ecosystem** validates framework integration in quality matrix
3. **tech-debt-investigator** flags framework gaps as documentation debt
4. Results synthesized into 360° assessment

---

## Maintenance Schedule

- **Per Agent Change**: Evaluate framework alignment when agent is modified
- **Quarterly Review**: Batch evaluate all agents for framework currency
- **New Framework Addition**: Update catalog → Re-evaluate affected agents

---

**See Also**:
- `00-core/frameworks/README.md` - Complete framework definitions
- `00-core/frameworks/README.md` - Core 4 methodology details
- `agent-analysis-suite-protocol.md` - Full analysis workflow

---

**Version**: 1.0
**Last Updated**: 2025-11-26
