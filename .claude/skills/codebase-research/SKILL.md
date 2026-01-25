---
name: codebase-research
description: >
  Use this skill when analyzing local code patterns, discovering implementations,
  or mapping dependencies. Provides 3-phase search strategy (Discovery->Mapping->Validation),
  progressive narrowing, and 10:1 compression methodology.
  Keywords: code analysis, pattern discovery, dependency mapping, codebase search, find code, architecture.
---

# Codebase Research

*Execute focused codebase research with three-phase search strategy and compression methodology.*

---

## Contents

1. [Three-Phase Search Strategy](#three-phase-search-strategy)
2. [Mode Detection](#mode-detection)
3. [Progressive Narrowing](#progressive-narrowing)
4. [Tool Patterns](#tool-patterns)
5. [BlastRadius Pattern](#blastradius-pattern)
6. [Compression Guidelines](#compression-guidelines)
7. [Termination Rules](#termination-rules)
8. [Good Enough Criteria](#good-enough-criteria)
9. [Anti-Patterns](#anti-patterns)
10. [Thinking Frameworks](#thinking-frameworks)
11. [Quick Reference](#quick-reference)

---

## Three-Phase Search Strategy

Execute research in three distinct phases with strict time budgets.

### Phase 1: Discovery (Target: 5 seconds)

**Goal**: Find starting points quickly

1. Get project structure with `Glob("**/*.py")`
2. Find initial matches with `Grep(pattern, output_mode="files_with_matches", head_limit=20)`
3. Count references with `Grep(pattern, output_mode="count")`

**Track internally**:
- `visited_files`: List of files examined
- `match_counts`: Dictionary of {file: count}

### Phase 2: Mapping (Target: 10 seconds)

**Goal**: Understand connections and structure

1. **Find imports**:
   ```
   Grep("^import |^from ", output_mode="content", type="py", -n=true)
   ```

2. **Read top files** (MAX 3-5):
   - Sort by match_counts (highest first)
   - Extract: imports, exports, function/class definitions

3. **Build dependency map**:
   - `imports`: {file: [modules]}
   - `exports`: {file: [symbols]}
   - `references`: {symbol: [files]}

### Phase 3: Validation (Target: 5 seconds)

**Goal**: Verify findings and assess confidence

1. **Find tests**:
   ```
   Grep(pattern, glob="**/test_*.py", output_mode="files_with_matches")
   ```

2. **Find usage examples**:
   ```
   Grep(pattern, output_mode="content", -B=2, -A=2, head_limit=5)
   ```

3. **Calculate confidence score** based on:
   - Has definition + tests + 10+ refs = 0.9
   - Has refs only = 0.7

**STOP if**: confidence > 0.85 AND found > 10 files

---

## Mode Detection

| User Says | Mode | Start With |
|-----------|------|------------|
| "find code", "locate function" | Discovery | Glob + Grep patterns |
| "analyze patterns", "how does X work" | Pattern Analysis | Structure + dependencies |
| "map dependencies", "architecture" | Architecture | Import/export mapping |

**Do not announce the mode. Execute the appropriate search strategy directly.**

---

## Progressive Narrowing

Apply progressive narrowing when results are too broad or too narrow.

| Stage | Pattern | Purpose |
|-------|---------|---------|
| Broad | `**/*.py` | Get full project scope |
| Narrow | `src/**` | Focus on source code |
| Precise | `\bpattern\b` | Word boundary match |
| Deep | Read top 3-5 files | Detailed analysis |

### Tool Budget

- **MAX 15 tool calls** total (track: increment counter after each Glob/Grep/Read)
- **MAX 30 seconds** estimated (approximate: 2s per tool call)
- **Parallel Glob/Grep** batching when searching multiple patterns

---

## Tool Patterns

### Finding Definitions

```
# Class definition
Grep("^class ClassName", output_mode="content", -n=true)

# Function definition
Grep("^def function_name", output_mode="content", -n=true)
```

### Finding Usage

```
# Word boundary (precise)
Grep("\bClassName\b", output_mode="files_with_matches")

# With context
Grep("ClassName", output_mode="content", -A=2, -B=2, head_limit=5)

# Count references
Grep("ClassName", output_mode="count")
```

### Finding Dependencies

```
# Find all imports
Grep("^import |^from ", output_mode="content", type="py", -n=true)

# Find imports of specific module
Grep("from.*module_name import", output_mode="files_with_matches")
```

### Finding Tests

```
Grep(pattern, glob="**/test_*.py", output_mode="files_with_matches")
Grep(pattern, glob="**/*_test.py", output_mode="files_with_matches")
```

---

## BlastRadius Pattern

**Purpose**: Map the full scope of changes by tracing dependencies outward from a focal point.

**When to Use**:
- Investigating impact of a proposed change
- Understanding how a component is used across the codebase
- Risk assessment for refactoring
- Finding all consumers of an API/function/class

### The Pattern

```
1. IDENTIFY Focal Point:
   - File, function, class, or pattern being changed
   - Example: "packages/core/auth/validator.py::validate_token()"

2. TRACE Direct Dependencies (Layer 1):
   Grep("from.*auth.*import|import.*auth", output_mode="files_with_matches")
   → Files that directly import the focal point

3. TRACE Indirect Dependencies (Layer 2):
   For each Layer 1 file:
     Grep("from.*{layer1_module}.*import", output_mode="files_with_matches")
   → Files that import Layer 1 files (transitive dependencies)

4. MAP Test Coverage:
   Grep(focal_point, glob="**/test_*.py", output_mode="files_with_matches")
   → Tests that exercise the focal point

5. CALCULATE Blast Radius:
   blast_radius = {
     direct_consumers: len(layer1_files),
     transitive_consumers: len(layer2_files),
     test_coverage: len(test_files),
     risk_score: (direct × 1.0) + (transitive × 0.5)
   }
```

### Risk Score Interpretation

| Risk Score | Level | Action |
|------------|-------|--------|
| <5 | Low | Proceed with standard review |
| 5-15 | Medium | Require test coverage verification |
| >15 | High | Require architecture review |

---

## Compression Guidelines

Compress findings before returning. Target ratios:

| Content Type | Compression Ratio | Keep | Discard |
|--------------|------------------|------|---------|
| Definition | 5:1 | Signatures, key patterns | Implementation details |
| Patterns | 10:1 | Pattern name, 2-3 examples | Exhaustive lists |
| Architecture | 15:1 | Structure, layers | Full dependency graphs |

### Compression Techniques

- **Pattern to Summary**: "All 15 services use BaseConnector pattern"
- **Code to Insight**: "Authentication handled via @requires_auth decorator"
- **Architecture to Structure**: "3-tier: API -> Service -> Repository"
- **Examples to Sample**: 1-2 examples, not all occurrences

**Target**: 10:1 minimum (200k research -> 20k findings)

---

## Termination Rules

### Stop When ANY Condition is True

1. Found 20+ files AND confidence > 0.85
2. Search iterations > 5
3. Estimated time > 30 seconds
4. Last iteration found < 2 new items
5. Memory approaching 10k tokens

### Stagnation Detection

Track file sets returned by each search iteration:
- **Stagnation**: Same file set returned 2 consecutive iterations
- **Action**: Force termination, return current findings
- **Rationale**: Continuing will not yield new information

---

## Good Enough Criteria

ALL must be true to terminate with SUCCESS:

1. Found definition OR clear entry point for the search target
2. Found 3+ distinct usages (in different files)
3. At least 1 finding directly answers the objective
4. Confidence > 0.85 based on RELEVANCE (not just file count)

**If criteria not met after 15 tool calls**: Return partial findings with gaps noted.

---

## Anti-Patterns

### NEVER DO

- Return raw tool output (compress first)
- List all files (summarize patterns instead)
- Exceed 20 seconds research time
- Fabricate missing information
- Execute code modifications
- Delegate to other agents (research only)

### Error Recovery

| Issue | Fallback Sequence |
|-------|-------------------|
| Nothing found | Case-insensitive -> Partial match -> Semantic variants -> Broaden scope |
| Too many results | Add type filter -> Exclude tests -> Limit results -> Focus on src/ |
| Vague input | Extract objective -> Plan strategy -> Start Discovery phase |
| Tool failure | Retry once -> If 2nd failure: return partial with error noted |

---

## Thinking Frameworks

When facing complex research challenges, apply these frameworks.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

### Most Relevant for Codebase Research

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Iterative search refinement, progressive narrowing |
| [CAGEERF](../../docs/00-core/frameworks/analysis.md) | Complex multi-component analysis |

### ReACT for Search

```
REASON: What am I looking for? What's the best search pattern?
ACT: Execute Glob/Grep/Read
OBSERVE: What did I find? Is it sufficient?
REFINE: Narrow or broaden based on results
REPEAT: Until confidence >= 0.85 or limits reached
```

> **Selection Tip**: iterative search -> ReACT, complex analysis -> CAGEERF

---

## Quick Reference

```
PHASES:
  Discovery (5s) -> Mapping (10s) -> Validation (5s)

LIMITS:
  Tool calls: 15 max
  Time: 30 seconds max
  Read files: 5 per phase (15 total)

COMPRESSION:
  Definition: 5:1
  Patterns: 10:1
  Architecture: 15:1

GOOD ENOUGH:
  - Definition OR entry point found
  - 3+ distinct usages
  - 1+ finding answers objective
  - Confidence > 0.85

PROGRESSIVE NARROWING:
  Broad (**/*.py) -> Narrow (src/**) -> Precise (\bpattern\b) -> Deep (Read)
```

---

## Validation Checklist

Before completing research:

- [ ] Three-phase search executed (Discovery -> Mapping -> Validation)
- [ ] Compression ratio 10:1 minimum achieved
- [ ] File:line references included for key findings
- [ ] Confidence score calculated with breakdown
- [ ] Termination rules checked before returning
- [ ] Patterns summarized, not exhaustively listed

---

## Cross-References

### Skill-Specific Documentation

| Document | Purpose |
|----------|---------|
| [Tool Patterns](./reference/tool-patterns.md) | Glob, Grep, Read patterns and examples |
| [Common Docs](./reference/common-docs.md) | Links to shared documentation |
| [Simple Example](./examples/example-simple.md) | "Find ConfigLoader" - needle query |
| [Complex Example](./examples/example-complex.md) | "How does auth work?" - investigation |
| [Findings Template](./templates/findings-template.md) | Output format for research results |

### Shared Documentation

| Document | Purpose |
|----------|---------|
| [Research Skill Escalation](/.claude/docs/01-guides/research/research-skill-escalation.md) | When to escalate to library-research or web-research |
| [Orchestrator Thresholds](/.claude/docs/00-core/orchestrator-thresholds.md) | CQ formulas and confidence scoring |
| [Research Patterns](/.claude/docs/00-core/research-patterns.md) | General research methodology |
| [Tool Parallelization](/.claude/docs/01-guides/performance/tool-parallelization-patterns.md) | Parallel vs sequential tool execution |

### Related Skills

| Skill | Escalate When |
|-------|---------------|
| [library-research](../library-research/SKILL.md) | Need official API docs for external library |
| [web-research](../web-research/SKILL.md) | Need community patterns, production deployment |
