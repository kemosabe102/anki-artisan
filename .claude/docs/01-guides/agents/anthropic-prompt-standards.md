---
title: "Anthropic Prompt Engineering Standards for Claude Code Agents"
date: 2025-11-18
status: ACTIVE
tags: [agents, prompt-engineering, standards]
---

# Anthropic Prompt Engineering Standards for Claude Code Agents

**Purpose**: Official Anthropic prompt engineering best practices adapted for Claude Code sub-agent design

**Audience**: claude-code-ecosystem, claude-code-ecosystem, agent creators

**Scope**: Prompt quality validation specific to Claude Code Task tool agents

---

## Quick Reference

| **Principle** | **Application** | **Validation Check** |
|---------------|-----------------|---------------------|
| Be Clear & Direct | Explicit instructions > implicit assumptions | Agent definition states exact responsibilities |
| XML Structure | Use tags for sections, examples, context | Sections use XML tags (`<role>`, `<workflow>`, etc.) |
| Chain-of-Thought | Give Claude time to think | Agent prompts include reasoning guidance |
| Prefill Responses | Reduce chattiness, control format | Output schemas include structure hints |
| Acknowledge Uncertainty | Let Claude say "I don't know" | Agent includes confidence scoring, escalation paths |
| Context Management | Progressive disclosure, external references | Agent references guides vs inline verbosity |

---

## Core Principles (Anthropic Official)

### 1. Be Clear and Direct

**Standard**: Explicit, detailed instructions outperform implicit assumptions or examples alone.

**For Claude Code Agents**:
- State exact role and boundaries in Role & Boundaries section
- List explicit responsibilities (not "help with X" but "perform Y when Z")
- Define what the agent should NOT do (scope discipline)
- Specify output format expectations (schemas, structure)

**Validation Criteria**:
- ✅ Role section starts with "You are [specific role]" (not vague "assistant")
- ✅ Boundaries section lists 3+ explicit exclusions
- ✅ Responsibilities use action verbs (analyze, validate, generate, optimize)
- ✅ Output schema referenced explicitly

**Examples**:
```markdown
✅ GOOD:
**Role**: You are a Python code implementation specialist for packages/**, tests/**, scripts/**.
You execute features with standards compliance and pre-flight validation.

**Boundaries**:
- NOT for: .claude/** (claude-code-ecosystem), docs/** (/spec command), k8s/** (deployment-release)
- NO direct file operations (delegate to orchestrator if file ops needed)
- NO assumption-based implementation (research via Context7 when uncertain)

❌ BAD:
**Role**: You help implement Python code and make it better.
```

---

### 2. Use XML Tags for Structure

**Standard**: XML tags help Claude parse complex prompts, separate instructions from data, and maintain context.

**For Claude Code Agents**:
- Use XML tags for examples: `<example>...</example>`
- Use XML for workflows: `<workflow>...</workflow>`
- Use XML for metadata: `<context>...</context>`, `<constraints>...</constraints>`
- Separate instructions from data clearly

**Validation Criteria**:
- ✅ Examples wrapped in `<example>` tags (not just markdown code blocks)
- ✅ Multi-step workflows use `<workflow>` or numbered XML steps
- ✅ Context/constraints separated from instructions
- ✅ Nested tags used for complex structures

**Examples**:
```markdown
✅ GOOD:
<example>
User request: "Fix auth bug in packages/auth/jwt.py"
Agent actions:
1. Read file to understand context
2. Form hypothesis about failure mode
3. Design minimal test case
</example>

❌ BAD:
Example: User says "fix bug", agent fixes it.
```

---

### 3. Give Claude Time to Think (Chain-of-Thought)

**Standard**: Complex tasks benefit from explicit reasoning steps before answers.

**For Claude Code Agents**:
- Include "Analysis Phase" or "Assessment Phase" in workflows
- Prompt for reasoning: "Before [action], analyze [context]"
- Multi-step decision-making with intermediate outputs
- Encourage hypothesis formation before execution

**Validation Criteria**:
- ✅ Workflow includes analysis/assessment phase before action
- ✅ Complex decisions prompted with "Consider...", "Analyze...", "Evaluate..."
- ✅ Agent encouraged to document reasoning (not just final answer)
- ✅ Hypothesis-driven approaches for debugging/research

**Examples**:
```markdown
✅ GOOD:
**Workflow**:
1. **ANALYZE**: Read existing implementation, identify patterns, assess complexity
2. **PLAN**: Design solution approach, identify dependencies, estimate risk
3. **EXECUTE**: Implement with validation, verify output, document changes

❌ BAD:
**Workflow**: Read file, write code, done.
```

---

### 4. Prefill Responses for Control

**Standard**: Start Claude's response with desired structure to reduce chattiness and ensure format compliance.

**For Claude Code Agents**:
- Schema definitions act as "prefill" guidance
- Output format examples show expected structure
- Two-state model (SUCCESS/FAILURE) acts as format constraint
- agent_specific_output structure guides response format

**Validation Criteria**:
- ✅ Schema includes example outputs
- ✅ Agent definition shows expected response structure
- ✅ Output format specified (JSON, markdown table, structured report)
- ✅ Two-state model clearly documented

**Examples**:
```markdown
✅ GOOD:
**Output Schema**: .claude/docs/schemas/debugger.schema.json

**Example Output**:
{
  "status": "SUCCESS",
  "agent": "debugger",
  "confidence": 0.88,
  "agent_specific_output": {
    "hypothesis": "JWT expiration not checked",
    "evidence": ["Line 42: token.exp not validated"],
    "fix_applied": "packages/auth/jwt.py:42-45"
  }
}

❌ BAD:
**Output**: Returns analysis results.
```

---

### 5. Let Claude Say "I Don't Know"

**Standard**: Prevent hallucinations by explicitly allowing uncertainty acknowledgment.

**For Claude Code Agents**:
- Include confidence scoring (0.0-1.0) in outputs
- Define escalation paths for low confidence (<0.5)
- Encourage research over guessing (Context7, web search)
- iteration_support for open questions

**Validation Criteria**:
- ✅ Output schema includes confidence field
- ✅ Agent definition includes escalation protocol
- ✅ Research tools mentioned for uncertainty resolution
- ✅ iteration_support or open_questions field in schema

**Examples**:
```markdown
✅ GOOD:
**When Uncertain**:
- Return confidence <0.5
- Populate iteration_support.open_questions
- Recommend follow-up research (Context7, web search)
- DO NOT guess implementation details

**Confidence Scoring**:
- ≥0.85: High confidence, proceed
- 0.50-0.84: Medium confidence, note assumptions
- <0.50: Low confidence, escalate to orchestrator

❌ BAD:
Agent always returns answers with confidence 1.0.
```

---

### 6. Context Management (Progressive Disclosure)

**Standard**: Use long context windows strategically - progressive disclosure, external references, just-in-time loading.

**For Claude Code Agents**:
- Reference external guides instead of inline verbosity
- Extend base-agent-pattern.md (don't duplicate)
- Use Quick Reference for 80% tasks
- Just-in-time methodology loading

**Validation Criteria**:
- ✅ Agent declares base-agent-pattern extension
- ✅ Quick Reference section for common tasks
- ✅ External guides referenced: "See .claude/docs/..."
- ✅ Agent <500 lines (or has justification for verbosity)

**Examples**:
```markdown
✅ GOOD:
**Extends**: .claude/docs/01-guides/agents/base-agent-pattern.md

**Quick Reference**: [Table with formulas, workflows, key patterns]

**Detailed Methodology**: See .claude/docs/01-guides/debugging/hypothesis-driven-debugging.md

❌ BAD:
[500 lines of inline methodology documentation repeated from other agents]
```

---

## Validation Checklist

Use this checklist when evaluating agent prompt quality:

- [ ] **Clarity**: Role explicitly stated, responsibilities action-verb focused, boundaries listed
- [ ] **XML Structure**: Examples/workflows use XML tags, instructions separated from data
- [ ] **Chain-of-Thought**: Analysis phase before action, reasoning prompted, hypothesis-driven
- [ ] **Prefill Guidance**: Schema with examples, output format specified, two-state model documented
- [ ] **Uncertainty Handling**: Confidence scoring, escalation paths, research tools mentioned
- [ ] **Context Management**: Base-pattern extension, Quick Reference present, external guide references
- [ ] **Anti-Patterns Avoided**: No vague roles, no implicit assumptions, no inline verbosity, no forced confidence

---

## Integration with Existing Frameworks

**claude-code-ecosystem.md** should validate against these 6 principles as part of "Anthropic Prompt Engineering" framework.

**claude-code-ecosystem.md** should check compliance during agent creation (Quality Matrix criterion: Prompt Engineering Standards).

**See Also**:
- `.claude/docs/01-guides/agents/agent-standards-extended.md` - Universal agent requirements
- `.claude/docs/01-guides/agents/base-agent-pattern.md` - Inheritance model
- `.claude/docs/01-guides/documentation/progressive-disclosure-validation-framework.md` - Context management

---

**Version**: 1.0
**Source**: Anthropic Official Prompt Engineering Docs (https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/)
**Adapted for**: Claude Code Task tool sub-agents
