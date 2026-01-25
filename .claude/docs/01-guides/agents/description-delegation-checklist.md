---
title: "Description Delegation Checklist"
date: 2025-11-21
status: ACTIVE
tags: [agents, descriptions, delegation]
---
# Description Delegation Checklist

**Purpose**: Evaluation framework for agent descriptions to ensure effective orchestrator delegation.

**Primary User**: claude-code-ecosystem (during agent creation and review)

**Focus**: Will Claude Code select this agent correctly based on its description?

**Scope**: Orchestrator-facing description quality (delegation effectiveness, semantic matching, trigger clarity)

**Not Covered**: Token efficiency (see description-alignment-checklist.md), internal prompt quality (see claude-code-ecosystem frameworks)

---

## Overview

Agent descriptions are the **first-line trigger** for orchestrator delegation. A well-crafted description ensures Claude Code:

1. **Recognizes when to use the agent** (clear trigger conditions)
2. **Proactively suggests the agent** (explicit delegation signals)
3. **Matches semantic intent** (domain keywords present)
4. **Understands capabilities** (action-oriented language)
5. **Assigns appropriate tasks** (role/expertise declaration)

**Critical Insight**: Orchestrator sees ONLY the description (not full prompt) during initial agent selection. Description quality directly impacts Agent Selection Confidence (ASC) scoring.

---

## The 6 Delegation Criteria

### ✅ Criterion 1: Clear Trigger Condition

**Question Answered**: "When should I use this agent?"

**Requirements**:
- [ ] Explicit trigger phrase (e.g., "Use when...", "Proactively use for...", "Specialist for...")
- [ ] Specific conditions listed (file types, task types, problem domains)
- [ ] No ambiguous language ("may help", "can assist", "sometimes useful")
- [ ] First 1-2 sentences establish primary use case

**Evidence Format** (for claude-code-ecosystem):
```markdown
**Trigger Clarity Score**: X/5
- ✅/❌ Explicit trigger phrase present
- ✅/❌ Specific conditions listed
- ✅/❌ No ambiguous qualifiers
- ✅/❌ Primary use case in first sentence
```

**Examples**:

✅ **GOOD**:
```
"Debugging specialist for errors, test failures, and unexpected behavior.
Use proactively when encountering any issues."
```
- Clear trigger: "errors, test failures, unexpected behavior"
- Proactive signal: "Use proactively"
- No ambiguity

✅ **GOOD**:
```
"Data analysis expert for SQL queries, BigQuery operations, and data insights.
Use proactively for data analysis tasks and queries."
```
- Clear domain: "SQL queries, BigQuery operations, data insights"
- Explicit action: "Use proactively for..."

❌ **BAD**:
```
"Helps with code quality and might assist in reviewing implementations."
```
- Vague trigger: "helps with" (when?)
- Conditional: "might assist" (not definitive)
- No specific conditions

❌ **BAD**:
```
"General-purpose agent for various tasks."
```
- No specific trigger
- No domain boundaries
- No use case clarity

---

### ✅ Criterion 2: Proactive Delegation Signal

**Question Answered**: "Should I suggest this agent without being asked?"

**Requirements**:
- [ ] Contains "proactively" OR equivalent signal ("automatically", "immediately", "always use for")
- [ ] Encourages orchestrator to delegate early (not wait for failure)
- [ ] Signals low-friction delegation (not "only when absolutely necessary")
- [ ] Positioned within first 2 sentences

**Evidence Format**:
```markdown
**Proactive Signal Score**: X/5
- ✅/❌ "Proactively" keyword present OR equivalent
- ✅/❌ Encourages early delegation
- ✅/❌ Low-friction language
- ✅/❌ Signal in first 2 sentences
```

**Examples**:

✅ **GOOD**:
```
"Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Use immediately after writing or modifying code."
```
- "Proactively reviews" - clear signal
- "Use immediately after" - early delegation
- "writing or modifying code" - low friction

✅ **GOOD**:
```
"Git workflow automation specialist. Automatically handles commit preparation,
branch management, and PR creation."
```
- "Automatically handles" - proactive equivalent
- Implies orchestrator should delegate without asking

❌ **BAD**:
```
"Code review agent for final quality checks before production deployment."
```
- No proactive signal
- "Final quality checks" implies late delegation
- High friction (production deployment)

❌ **BAD**:
```
"Can be used to review code when requested."
```
- "Can be used" - passive, not proactive
- "When requested" - reactive signal

---

### ✅ Criterion 3: Domain Keywords for Semantic Matching

**Question Answered**: "What technical domains does this agent cover?"

**Requirements**:
- [ ] 3-5 domain-specific keywords present (technologies, file types, problem categories)
- [ ] Keywords match orchestrator's agent selection frameworks (see agent-selection-guide.md)
- [ ] No generic terms only ("code", "files", "tasks")
- [ ] Keywords appear in first paragraph

**Evidence Format**:
```markdown
**Domain Keywords Score**: X/5
- ✅/❌ 3+ domain-specific keywords
- ✅/❌ Keywords match selection frameworks
- ✅/❌ Beyond generic terms
- ✅/❌ Keywords in first paragraph

**Keywords Identified**: [list]
```

**Examples**:

✅ **GOOD**:
```
"Observability specialist for Prometheus, Grafana, Loki, and OpenTelemetry.
Proactively builds dashboards, queries metrics, and analyzes logs."
```
- **Keywords**: Prometheus, Grafana, Loki, OpenTelemetry, dashboards, metrics, logs (7 total)
- All domain-specific (observability stack)

✅ **GOOD**:
```
"Python implementation specialist for packages/**, tests/**, and core modules.
Handles FastAPI, SQLAlchemy, and async patterns."
```
- **Keywords**: Python, packages, tests, FastAPI, SQLAlchemy, async (6 total)
- Matches directory structure + technology stack

❌ **BAD**:
```
"Works with code files and performs various operations."
```
- **Keywords**: code, files, operations (generic only)
- No domain specificity

❌ **BAD**:
```
"Agent for improving quality."
```
- **Keywords**: quality (1, too generic)
- No technical domain

---

### ✅ Criterion 4: Action-Oriented Language

**Question Answered**: "What does this agent DO?"

**Requirements**:
- [ ] 3+ action verbs present (builds, analyzes, fixes, generates, validates, optimizes, etc.)
- [ ] Verbs describe concrete actions (not abstract concepts)
- [ ] Verbs match agent's actual capabilities in prompt
- [ ] Active voice (not passive: "can be used to...")

**Evidence Format**:
```markdown
**Action Verbs Score**: X/5
- ✅/❌ 3+ action verbs
- ✅/❌ Concrete actions (not abstract)
- ✅/❌ Match prompt capabilities
- ✅/❌ Active voice

**Action Verbs Identified**: [list]
```

**Examples**:

✅ **GOOD**:
```
"Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Validates standards compliance, detects anti-patterns,
and generates improvement recommendations."
```
- **Verbs**: reviews, validates, detects, generates (4 total)
- All concrete actions

✅ **GOOD**:
```
"Debugging specialist. Analyzes errors, formulates hypotheses, executes tests,
and iterates until resolution."
```
- **Verbs**: analyzes, formulates, executes, iterates (4 total)
- Describes complete workflow

❌ **BAD**:
```
"Responsible for code quality and can help with reviews."
```
- **Verbs**: help (1, vague)
- "Responsible for" - no action
- "Can help" - passive

❌ **BAD**:
```
"Supports development activities and provides assistance."
```
- **Verbs**: supports, provides (2, abstract)
- No concrete actions

---

### ✅ Criterion 5: Role/Expertise Declaration

**Question Answered**: "What is this agent's primary expertise?"

**Requirements**:
- [ ] Clear role statement (Specialist, Expert, Architect, etc.)
- [ ] Expertise level implied (not beginner/general)
- [ ] Domain authority established (first sentence)
- [ ] Differentiates from other agents (unique value proposition)

**Evidence Format**:
```markdown
**Role Clarity Score**: X/5
- ✅/❌ Clear role statement
- ✅/❌ Expertise level established
- ✅/❌ Domain authority (first sentence)
- ✅/❌ Unique differentiation

**Role Identified**: [role name]
**Expertise Domain**: [domain]
```

**Examples**:

✅ **GOOD**:
```
"Expert code review specialist. Proactively reviews code for quality,
security, and maintainability."
```
- **Role**: Expert code review specialist
- **Expertise**: Code quality, security, maintainability
- **Authority**: "Expert" establishes level
- First sentence

✅ **GOOD**:
```
"Debugging specialist for errors, test failures, and unexpected behavior."
```
- **Role**: Debugging specialist
- **Expertise**: Errors, test failures, unexpected behavior
- **Authority**: "Specialist" implies deep knowledge
- First sentence

❌ **BAD**:
```
"General-purpose agent that can handle various tasks."
```
- **Role**: General-purpose (not specialized)
- **Expertise**: None specified
- **Authority**: None established

❌ **BAD**:
```
"Helps with code when needed."
```
- **Role**: Not stated
- **Expertise**: Vague ("code")
- **Authority**: None

---

### ✅ Criterion 6: YAML Syntax Compliance

**Question Answered**: "Is the description field properly formatted for parsing?"

**Requirement**: Description field must use single-quoted string format, NOT YAML multi-line blocks.

### Valid Format
```yaml
description: 'Single line description with all content here. Use for: X. NOT for: Y.'
```

### Invalid Formats (REJECTED)
```yaml
# BROKEN - pipe literal block
description: |
  Multi-line content here
  Will truncate to ~14 tokens

# BROKEN - folded block  
description: >
  Multi-line content here
  Will truncate to ~11 tokens
```

### Why This Matters
Claude Code's agent loader does NOT properly parse YAML multi-line syntax. Using `|` or `>` causes descriptions to truncate, breaking agent selection and discoverability.

### Checklist
- [ ] Description on single line after `description: '`
- [ ] No pipe (`|`) or folded (`>`) syntax used
- [ ] Content enclosed in single quotes
- [ ] Internal single quotes escaped with double single-quotes (`''`)

**Evidence Format**:
```markdown
**YAML Syntax Score**: X/5
- ✅/❌ Single-line format used
- ✅/❌ No pipe or folded syntax
- ✅/❌ Single quotes enclosing content
- ✅/❌ Internal quotes properly escaped
```

**Examples**:

✅ **GOOD**:
```yaml
description: 'Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.'
```
- Single line after `description: '`
- Content enclosed in single quotes
- No multi-line syntax

✅ **GOOD** (with escaped quotes):
```yaml
description: 'Handles edge cases like ''quoted values'' within the description text.'
```
- Internal single quotes escaped with `''`

❌ **BAD**:
```yaml
description: |
  Expert code review specialist.
  Proactively reviews code for quality.
```
- Uses pipe literal block (`|`)
- Will truncate to ~14 tokens

❌ **BAD**:
```yaml
description: >
  Expert code review specialist.
  Proactively reviews code for quality.
```
- Uses folded block (`>`)
- Will truncate to ~11 tokens

---

## Scoring Rubric

**Overall Delegation Quality** = Sum of individual criterion scores

| **Total Score** | **Grade** | **Interpretation** | **Action** |
|----------------|-----------|-------------------|------------|
| **6/6** | A+ | All criteria met - Excellent delegation quality | PASS - No changes needed |
| **5/6** | A | 5/6 criteria met - Strong delegation quality | PASS - Minor improvements optional |
| **4/6** | B+ | 4/6 criteria met - Good delegation quality | CONSIDER - Improvement recommended |
| **3/6** | B | 3/6 criteria met - Adequate delegation quality | CONSIDER - Improvement recommended |
| **2/6** | C | 2/6 criteria met - Weak delegation quality | FAIL - Revisions required |
| **1/6** | D | 1/6 criteria met - Poor delegation quality | FAIL - Major rewrite required |
| **0/6** | F | No criteria met - Ineffective description | FAIL - Complete rewrite required |

**Confidence Threshold**: ≥5/6 recommended for production agents (83%+ delegation quality)

**Note**: Criterion 6 (YAML Syntax Compliance) is a HARD REQUIREMENT. If Criterion 6 fails, the description is non-functional regardless of other scores.

---

## Validation Workflow (claude-code-ecosystem)

### Manual Analysis Checklist

When evaluating agent descriptions, work through each criterion:

```markdown
## Description Delegation Analysis

**Agent**: [agent-name]
**Date**: [YYYY-MM-DD]
**Reviewer**: claude-code-ecosystem

### Criterion 1: Clear Trigger Condition
- [ ] Explicit trigger phrase present
- [ ] Specific conditions listed
- [ ] No ambiguous language
- [ ] Primary use case in first sentence
**Score**: X/5
**Evidence**: [quote relevant text]

### Criterion 2: Proactive Delegation Signal
- [ ] "Proactively" or equivalent present
- [ ] Encourages early delegation
- [ ] Low-friction language
- [ ] Signal in first 2 sentences
**Score**: X/5
**Evidence**: [quote relevant text]

### Criterion 3: Domain Keywords
- [ ] 3+ domain-specific keywords
- [ ] Keywords match selection frameworks
- [ ] Beyond generic terms
- [ ] Keywords in first paragraph
**Score**: X/5
**Keywords**: [list]

### Criterion 4: Action-Oriented Language
- [ ] 3+ action verbs
- [ ] Concrete actions
- [ ] Match prompt capabilities
- [ ] Active voice
**Score**: X/5
**Verbs**: [list]

### Criterion 5: Role/Expertise Declaration
- [ ] Clear role statement
- [ ] Expertise level established
- [ ] Domain authority (first sentence)
- [ ] Unique differentiation
**Score**: X/5
**Role**: [name]
**Domain**: [name]

---

**Total Score**: X/5
**Grade**: [A+/A/B/C/D/F]
**Decision**: PASS/FAIL
**Recommendations**: [if score <4/5]
```

### Automated Grep Checks (Optional)

Quick validation commands for common patterns:

```bash
# Check for proactive signal
grep -i "proactive\|immediately\|automatically\|always use" .claude/agents/[agent-name].md | head -5

# Check for trigger phrases
grep -i "use when\|use for\|specialist for\|expert for" .claude/agents/[agent-name].md | head -5

# Check for action verbs (common patterns)
grep -iE "builds|analyzes|fixes|generates|validates|optimizes|detects|executes|reviews|handles" .claude/agents/[agent-name].md | head -10

# Check for role declarations
grep -iE "specialist|expert|architect|analyst|builder" .claude/agents/[agent-name].md | head -5
```

**Note**: Grep checks are NOT comprehensive - use as quick screening only. Full manual analysis required for scoring.

---

## Official Claude Code Examples

**Source**: Claude Code official agent descriptions (validated for delegation effectiveness)

### Example 1: Code Review Specialist

```
"Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Use immediately after writing or modifying code."
```

**Analysis**:
- ✅ Criterion 1: "Use immediately after writing or modifying code" (trigger)
- ✅ Criterion 2: "Proactively reviews" (proactive signal)
- ✅ Criterion 3: quality, security, maintainability, code (keywords)
- ✅ Criterion 4: reviews (action verb)
- ✅ Criterion 5: "Expert code review specialist" (role)
- **Score**: 5/5 (A+)

### Example 2: Debugging Specialist

```
"Debugging specialist for errors, test failures, and unexpected behavior.
Use proactively when encountering any issues."
```

**Analysis**:
- ✅ Criterion 1: "errors, test failures, unexpected behavior" (specific triggers)
- ✅ Criterion 2: "Use proactively when encountering any issues" (proactive signal)
- ✅ Criterion 3: errors, test failures, unexpected behavior, debugging (keywords)
- ✅ Criterion 4: encountering (implicit action context)
- ✅ Criterion 5: "Debugging specialist" (role)
- **Score**: 5/5 (A+)

### Example 3: Data Analysis Expert

```
"Data analysis expert for SQL queries, BigQuery operations, and data insights.
Use proactively for data analysis tasks and queries."
```

**Analysis**:
- ✅ Criterion 1: "SQL queries, BigQuery operations, data insights" (specific triggers)
- ✅ Criterion 2: "Use proactively for..." (proactive signal)
- ✅ Criterion 3: SQL, BigQuery, data insights, queries (keywords)
- ✅ Criterion 4: analysis (action context)
- ✅ Criterion 5: "Data analysis expert" (role)
- **Score**: 5/5 (A+)

---

## Key Reminders

1. **This checklist focuses ONLY on delegation quality** - NOT token efficiency (see description-alignment-checklist.md)

2. **claude-code-ecosystem does NOT run token counting** - claude-code-ecosystem handles token analysis (no duplication)

3. **Descriptions are orchestrator-facing** - They must work for Claude Code's agent selection, not end users

4. **First 1-2 sentences are critical** - Orchestrator likely uses truncated preview for initial matching

5. **Keywords must match agent-selection-guide.md frameworks** - Use established domain vocabulary

6. **Proactive signals reduce delegation friction** - Encourage orchestrator to delegate early and often

---

## See Also

- **description-alignment-checklist.md** - Token efficiency and capability accuracy (claude-code-ecosystem)
- **agent-selection-guide.md** - Orchestrator's agent selection frameworks (domain keywords, decision trees)
- **golden-agent-standards.md** - Reference examples of excellent agent design
- **agent-standards-extended.md** - Complete agent design standards and patterns

---

**Version**: 1.0
**Last Updated**: 2025-11-21
**Maintained By**: claude-code-ecosystem
