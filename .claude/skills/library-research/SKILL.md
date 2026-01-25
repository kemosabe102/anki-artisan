---
name: library-research
description: >
  Use this skill when fetching official library/framework documentation,
  API references, or version-specific information. Uses Context7 as primary
  source with 15:1 compression. Falls back to web-research skill when coverage insufficient.
  Keywords: library docs, API reference, official documentation, Context7, version-specific, type signatures.
---

# Library Research

*Fetch official library documentation via Context7 with 3-round search strategy and 15:1 compression.*

---

## Contents

1. [Context7 Three-Round Strategy](#context7-three-round-strategy)
2. [Mode Detection](#mode-detection)
3. [Quality Thresholds](#quality-thresholds)
4. [Compression Guidelines](#compression-guidelines)
5. [Good Use Cases](#good-use-cases)
6. [Fallback Patterns](#fallback-patterns)
7. [Error Recovery](#error-recovery)
8. [Anti-Patterns](#anti-patterns)
9. [Thinking Frameworks](#thinking-frameworks)
10. [Quick Reference](#quick-reference)

---

## Context7 Three-Round Strategy

Execute library documentation research in three distinct rounds.

### Round 1: Resolve Library ID (Target: 3 seconds)


**Goal**: Resolve library name to Context7-compatible ID and validate quality

**Tool**: `mcp__context7__resolve-library-id`

**Process**:
1. Call `resolve-library-id("library-name")`
2. Check returned metadata: trust score, snippet count
3. Validate against quality thresholds

**CRITICAL**: Never assume library ID format. Always resolve first.

**Example**:
```
resolve-library-id("Pydantic") 
-> "/pydantic/pydantic" (trust: 9, snippets: 542)
-> quality_pass = true
```

### Round 2: Quality Check & Retrieve Docs (Target: 8 seconds)

**Goal**: Validate quality thresholds and retrieve focused documentation

**Tool**: `mcp__context7__get-library-docs`

**Process**:
1. Check quality thresholds (see [Quality Thresholds](#quality-thresholds))
2. If quality fails -> Return FAILURE immediately
3. If quality passes -> Retrieve docs with specific topic

**Token Allocation Strategy**:

| Scenario | Tokens | Use Case |
|----------|--------|----------|
| Quick | 2000 | Single API lookup, simple syntax question |
| Standard | 5000 | Topic exploration, pattern understanding |
| Deep | 8000 | Complex patterns, multiple related APIs |

**Topic Specificity**: Use 2-4 word phrases for focused results
- Good: "async validation", "model serialization", "field validators"
- Bad: "documentation", "everything", "how to use"

**Example**:
```
get-library-docs("/pydantic/pydantic", topic="async validation", tokens=5000)
-> Extract: API signatures, patterns, 1-2 code examples
```

### Round 3: Validation (Target: 4 seconds)

**Conditions**: ONLY execute if confidence < 0.90 OR version ambiguity detected

**Options**:
1. Additional Context7 query with deeper topic focus
2. Return partial findings with gaps noted

**Termination**: confidence >= 0.90 OR 3 rounds exhausted

---

## Mode Detection

| User Says | Mode | Start With |
|-----------|------|------------|
| "official docs", "library API", "version-specific" | primary | Context7 resolve-library-id |
| "migration guide", "breaking changes" | version_specific | Context7 with version topic |
| "type signatures", "API reference" | api_focused | Context7 with specific API topic |

**Do not announce the mode. Execute the appropriate strategy directly.**

---

## Quality Thresholds

Context7 sources must meet quality gates before use.

### Primary Threshold
```
trust_score >= 7 AND snippet_count >= 100
```

### Exception Threshold
```
trust_score >= 9 AND snippet_count >= 80
```
(Highly authoritative sources with fewer examples)

### Confidence Requirements
- **0.90+**: Sufficient from Context7 alone - proceed with findings
- **0.70-0.89**: Partial coverage - note gaps, consider Round 3
- **<0.70**: Insufficient - return FAILURE, recommend web-research skill

---

## Compression Guidelines

Compress findings before returning. Target 15:1 minimum ratio.

| Content Type | Priority | Keep | Discard |
|--------------|----------|------|---------|
| API signatures | Highest | Full signatures with type hints | Verbose explanations |
| Code examples | High | 1-2 minimal examples (5-10 lines) | Exhaustive variations |
| Patterns | Medium | Core pattern description | Edge case details |
| Prose | Low | Key concepts only | Tutorial-style content |

### Compression Techniques
- **API to Signature**: Full docstring -> function signature with types only
- **Example to Minimal**: 30-line example -> 5-10 line essential version
- **Pattern to Summary**: "All validators use @field_validator decorator"

**Target**: 15,000 tokens retrieved -> 1,000 tokens returned (15:1)

---

## Good Use Cases

| Request | Use This Skill? | Why / Alternative |
|---------|-----------------|-------------------|
| "How does Pydantic validation work?" | YES | Library API reference |
| "What's new in FastAPI 0.100?" | YES | Version-specific features |
| "Migration guide for SQLAlchemy 2.0" | YES | Official migration docs |
| "Type signatures for httpx client" | YES | Authoritative API types |
| "Breaking changes in Django 5.0" | YES | Version-specific changes |
| "Best practices for async Python" | NO | Community patterns -> web-research |
| "How does our auth module work?" | NO | Local code -> codebase-research |
| "Compare SQLAlchemy vs Tortoise" | NO | Trade-off analysis -> web-research |
| "Common FastAPI deployment patterns" | NO | Community patterns -> web-research |

---

## Fallback Patterns

### Library Not Found
- Context7 returns no matches for library name
- **Action**: Return FAILURE with delegation hint to web-research skill
- **Do NOT**: Attempt alternative spellings or guessing

### Trust/Snippets Below Threshold
- Quality check fails (trust<7 OR snippets<100)
- **Action**: Return FAILURE immediately
- **Do NOT**: Proceed with low-quality sources

### Partial Coverage
- Confidence 0.70-0.89 after Round 2
- **Action**: Execute Round 3 OR return partial findings with `iteration_support` populated
- **iteration_support**: Note specific gaps for follow-up queries

---

## Error Recovery

| Issue | Recovery Action | Max Retries |
|-------|-----------------|-------------|
| Rate limit (HTTP 429) | Exponential backoff: 2s, 4s, 8s | 3 |
| MCP timeout (>10s) | Retry with smaller topic scope | 2 |
| Library not found | Return FAILURE (permanent) | 0 |
| Invalid library ID | Return FAILURE (malformed) | 0 |

### Backoff Strategy
```
attempt_1: Execute immediately
attempt_2: Wait 2s + random(0-1s)
attempt_3: Wait 4s + random(0-2s)
```

---

## Anti-Patterns

### NEVER DO
- Fall back to web search directly (delegate to web-research skill instead)
- Ignore quality thresholds (trust<7 or snippets<100 = FAILURE)
- Use over-broad topics ("documentation" vs "async validation")
- Fabricate documentation not from Context7
- Assume library ID format without resolving first
- Return raw Context7 output (compress first)

### Error Recovery Anti-Patterns
- Retrying on "library not found" (permanent failure)
- Continuing after quality threshold failure
- Multiple Context7 queries with same topic (diminishing returns)

---

## Thinking Frameworks

When facing complex library research challenges, apply these frameworks.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

### Most Relevant for Library Research

| Framework | When to Use |
|-----------|-------------|
| ReACT | Quality validation, iterative refinement |
| OODA | Search strategy selection, termination decisions |

### ReACT for Quality Validation
```
REASON: Does this source meet quality thresholds?
ACT: Check trust score and snippet count
OBSERVE: trust=8, snippets=150 -> passes primary threshold
REFINE: Proceed to doc retrieval with specific topic
```

### OODA for Search Strategy
```
OBSERVE: User asks for "Pydantic async validation"
ORIENT: Library docs request, specific topic identified
DECIDE: Use api_focused mode with topic="async validation"
ACT: Execute 3-round strategy
```

> **Selection Tip**: quality validation -> ReACT, search strategy -> OODA

---

## Quick Reference

```
THREE-ROUND STRATEGY:
  Round 1 (3s): resolve-library-id -> validate quality
  Round 2 (8s): get-library-docs with specific topic
  Round 3 (4s): ONLY IF confidence < 0.90

QUALITY THRESHOLDS:
  Primary: trust >= 7 AND snippets >= 100
  Exception: trust >= 9 AND snippets >= 80

COMPRESSION:
  Target: 15:1 minimum
  Priority: API signatures > code examples > patterns > prose

TERMINATION:
  SUCCESS: confidence >= 0.90 AND api_signatures found
  FAILURE: library not found OR quality below threshold

FALLBACK:
  Library not found -> FAILURE + recommend web-research
  Low quality -> FAILURE immediately
  Partial coverage -> populate iteration_support
```

---

## Validation Checklist

Before completing research:

- [ ] Library ID resolved (not assumed)
- [ ] Quality thresholds checked (trust>=7, snippets>=100)
- [ ] Compression ratio 15:1 minimum achieved
- [ ] API signatures include type hints
- [ ] Code examples minimal (5-10 lines each)
- [ ] Confidence score calculated
- [ ] Gaps noted in iteration_support if partial coverage

---

## Cross-References

### Skill-Specific Documentation

| Document | Purpose |
|----------|---------|
| [Tool Patterns](./reference/tool-patterns.md) | Context7 resolve, get-docs, pagination, modes |
| [Common Docs](./reference/common-docs.md) | Links to shared documentation |
| [Simple Example](./examples/example-simple.md) | "React useState docs" - single library |
| [Complex Example](./examples/example-complex.md) | "FastAPI vs Flask routing" - comparison |
| [Findings Template](./templates/findings-template.md) | Output format for library research |

### Shared Documentation

| Document | Purpose |
|----------|---------|
| [Context7 Usage Guide](/docs/shared/mcp/context7-usage-guide.md) | Complete Context7 MCP reference |
| [Research Skill Escalation](/.claude/docs/01-guides/research/research-skill-escalation.md) | When to escalate to web-research |
| [Orchestrator Thresholds](/.claude/docs/00-core/orchestrator-thresholds.md) | CQ formulas and confidence scoring |
| [Research Patterns](/.claude/docs/00-core/research-patterns.md) | General research methodology |

### Related Skills

| Skill | Escalate When |
|-------|---------------|
| [codebase-research](../codebase-research/SKILL.md) | Need to check existing library usage in project |
| [web-research](../web-research/SKILL.md) | Library not in Context7, community patterns needed |
