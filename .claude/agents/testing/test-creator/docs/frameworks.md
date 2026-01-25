# Frameworks & Methodologies for test-creator

**Purpose**: Research protocols, decision frameworks, and escalation paths

---

## Research Tool Selection Protocol

### Cost-Optimized Research (Context7 FIRST → Perplexity SECOND)

**Principle**: Context7 is free and authoritative. Only escalate to Perplexity when necessary.

### Step 1: Context7 First (Free)

**Use Context7 for**:
- Testing framework docs (pytest, unittest, hypothesis)
- Fixture patterns, parametrization, mocking strategies
- Test library best practices (pytest-asyncio, pytest-mock, faker)
- Version-specific testing features

**Process**:
1. `resolve_library_id("pytest")` → Get library metadata
2. `get_library_docs(library_id, topic="fixtures", tokens=5000)` → Fetch docs
3. IF trust ≥7 AND snippets ≥100 → **STOP, use Context7 solution**
4. IF insufficient → Escalate to Perplexity

### Step 2: Perplexity Escalation (Paid)

**Use Perplexity ONLY when**:
- Confidence < 0.8 (unclear test strategy)
- Context7 insufficient (library not covered)
- Test design failed 2+ times
- General testing patterns not in specific library docs

**Tool Selection**:
| Tool | Use Case | Cost |
|------|----------|------|
| `perplexity_search` | Quick pattern lookups | ~$0.003 |
| `perplexity_ask` | General test design questions | ~$0.003 |
| `perplexity_research` | Comprehensive strategy investigation | ~$0.005-0.010 |

---

## Decision Matrix

| Scenario | Confidence | Tool | Cost |
|----------|-----------|------|------|
| Testing framework question | Any | **Context7 FIRST** | Free |
| Context7 quality docs | ≥0.9 | **Context7 ONLY** | Free |
| Context7 insufficient | <0.9 | Perplexity | $0.003-0.010 |
| Test strategy unclear | <0.8 | Perplexity | $0.003-0.010 |
| Failed 2+ times | Any | Perplexity | $0.003-0.010 |

---

## Information Hierarchy

### 1. Essential Source (Always Trusted)
- **What**: Code under test and existing test patterns
- **Location**: `packages/**/*.py`, `tests/**/*.py`
- **Usage**: Function signatures, dependencies, edge cases, AAA consistency

### 2. Progressive Source (Project Standards)
- **What**: Configuration and coding standards
- **Location**: `pyproject.toml` (lines 88-126), `coding-guidelines.md`
- **Usage**: Coverage targets (80%), markers, timeout settings, style

### 3. External Source (Library Docs)
- **What**: Testing framework documentation via Context7
- **Location**: pytest, pytest-mock, pytest-asyncio library IDs
- **Usage**: Fixture patterns, parametrization, mocking best practices

### 4. Escalation Source (When Blocked)
- **What**: User clarification and orchestrator guidance
- **Usage**: Resolve ambiguous behavior, clarify strategy preferences

---

## Escalation Path (3-Step)

**Attempt Definition**: One attempt = analysis + research + design (15-30 min)

### Step 1: Research Existing Patterns
- Operations: `Grep` similar tests, `Read` test files, identify patterns
- Success: Found comparable pattern OR confirmed novel scenario

### Step 2: Query Context7
- Operations: `resolve-library-id`, `get-library-docs` for relevant topics
- Success: Found framework guidance OR confirmed custom design needed

### Step 3: Escalate to Orchestrator
- Required: Specific gap description, attempted paths, recommended action
- Output: Request user specification, example test, or expected output

---

## Escalation Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Unclear expected behavior | 2 attempts (30-60 min) | Escalate for specification |
| Ambiguous strategy | Multiple valid approaches | Report options, request decision |
| Coverage vs. design conflict | 100% requires internals | Recommend public API focus |

---

## Framework Integration

### OODA Loop for Test Creation
1. **Observe**: Code under test, dependencies, existing patterns
2. **Orient**: Coverage gaps, edge cases, mock requirements
3. **Decide**: Strategy (scenarios, fixtures, parametrization)
4. **Act**: Generate files, verify AAA, delegate to test-executor

### Combining Frameworks
- **AAA + Mock Decision Tree**: Apply mock tree during Arrange phase
- **OODA + Research Protocol**: Research during Orient phase

---

## Quick Reference

### Decision Tree Summary

```
Test creation task
    │
    ├─ Simple function? → Unit test with AAA
    │
    ├─ External dependencies? → Mock + document rationale
    │
    ├─ Complex logic? → Parametrized tests
    │
    └─ Integration needed? → tests/integration/ + fixtures
```
