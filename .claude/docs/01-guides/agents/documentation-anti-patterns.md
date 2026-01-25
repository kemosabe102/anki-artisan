---
title: "Agent Documentation Anti-Patterns"
date: 2025-11-18
status: ACTIVE
tags: [agents, documentation, anti-patterns, progressive-disclosure]
---

# Agent Documentation Anti-Patterns

**Purpose**: Identify and fix common documentation mistakes in Claude Code agent definitions

**Audience**: claude-code-ecosystem, documentation, claude-code-ecosystem, agent creators

**Scope**: Documentation quality issues specific to `.claude/agents/*.md` files

---

## Quick Reference

| **Anti-Pattern** | **Symptom** | **Impact** | **Fix** |
|------------------|-------------|------------|---------|
| Buried Essentials | Critical info in L2+ sections | <80% task completion from L0 | Move formulas/workflows to Quick Reference |
| Vague Labels | Headings don't predict content | <80% first-click accuracy | Use specific, predictive headings with action verbs |
| Excessive Depth | 4+ disclosure levels | Users lose context, unpredictable navigation | Externalize L3+ to separate docs, use links |
| Content Duplication | Same content across agents | ~1,150 tokens wasted/agent | Extract to base-agent-pattern.md, use extension |
| Inline Verbose Examples | 50+ line examples inline | 250-400 tokens per section | Externalize to methodology guides, 2-3 line summary + link |
| Missing Quick Reference | No TOC in >300 line docs | Users scan entire document | Add Quick Reference table at top (L0 layer) |

---

## The 6 Anti-Patterns

### Anti-Pattern 1: Buried Essentials (Visibility Failure)

**Symptom**: Critical formulas, workflows, or patterns hidden deep in document structure (L2+ levels) requiring multiple disclosure actions.

**Example**:
```markdown
❌ BAD STRUCTURE:
# Agent Name

## Overview
General description...

## Advanced Topics
### Deep Concepts
#### Specialized Scenarios
##### **Confidence Scoring Formula**  ← BURIED AT L5!
confidence = (domain × 0.6) + (work_type × 0.3) + (track_record × 0.1)
```

**Impact**:
- Users can't complete common tasks (>30% frequency) without excessive navigation
- Essential information requires 3+ disclosure actions to reach
- Violates progressive disclosure principle: essential info should be immediately visible

**Fix**:
```markdown
✅ GOOD STRUCTURE:
# Agent Name

## Quick Reference (L0 - Always Visible)

| **Formula** | **Application** | **Threshold** |
|-------------|-----------------|---------------|
| Confidence Score | (domain × 0.6) + (work_type × 0.3) + (track_record × 0.1) | ≥0.5 delegate \| <0.5 escalate |
| Context Quality | (domain × 0.4) + (pattern × 0.3) + (dependency × 0.2) + (risk × 0.1) | ≥0.5 implement \| <0.5 research |

**Core Workflow**: Parse → Analyze → Research (if needed) → Generate → Validate

**See**: [Advanced Topics](#advanced-topics) for detailed methodology
```

**Detection**:
- Search for formulas below h3 headings (###)
- Check if >30% frequency tasks require expanding sections
- Verify Quick Reference section exists and contains critical patterns

**Token Impact**: Moving essentials to L0 saves ~50-100 tokens per usage (users navigate faster, agent needs less context)

---

### Anti-Pattern 2: Vague Labels (Information Scent Failure)

**Symptom**: Section headings that don't predict content, using generic labels like "Miscellaneous", "Other", "Additional Information", "Details".

**Example**:
```markdown
❌ BAD HEADINGS:
## Miscellaneous
Contains error recovery patterns, validation checklists, and edge case handling.

## Additional
Tool usage guidelines, API references, command examples.

## Other Considerations
Performance optimization, security checks, logging.
```

**Impact**:
- <80% first-click accuracy (users guess incorrectly)
- Wasted time scanning "wrong" sections
- Violates Nielsen Norman 2-level depth guidelines (unpredictable navigation)

**Fix**:
```markdown
✅ GOOD HEADINGS:
## Error Recovery Patterns
Standard recovery workflows, retry logic, escalation paths.

## Tool Usage Guidelines
API reference, command examples, parameter documentation.

## Performance & Security
Optimization patterns, security validation, logging best practices.
```

**Detection**:
- Grep for headings: "Miscellaneous", "Other", "Additional", "Details", "More"
- Check if heading predicts >80% of section content
- Verify action verbs or domain terms in headings

**Token Impact**: Clear headings reduce navigation overhead ~20-30 tokens per section (users find content faster)

---

### Anti-Pattern 3: Excessive Depth (Level Failure)

**Symptom**: Document structure with 4+ disclosure levels (h4, h5, h6 headings), requiring 3+ clicks to reach essential information.

**Example**:
```markdown
❌ BAD DEPTH:
# Agent Name (L0)
## Overview (L1)
### Core Concepts (L2)
#### Advanced Patterns (L3)
##### Specialized Scenarios (L4)
###### Edge Case Handling (L5)  ← TOO DEEP!
Implementation details for rare edge cases...
```

**Impact**:
- Users lose context navigating deep hierarchies
- Unpredictable navigation (Nielsen Norman 2-level limit violated)
- Difficult to maintain (complex structure)

**Fix**:
```markdown
✅ GOOD DEPTH (MAX 2 LEVELS VISIBLE):
# Agent Name (L0)

## Quick Reference (L1)
Formulas, workflows, common patterns (80%+ tasks)

## Core Workflow (L1)
Standard operation process

## Advanced Patterns (L1)
**See**: .claude/docs/01-guides/[domain]/advanced-patterns.md for:
- Specialized scenarios
- Edge case handling
- Performance optimization
```

**Detection**:
- Count heading levels: h1 (1 level) through h6 (6 levels)
- Flag documents with h4+ headings (4+ levels)
- Check if >2 clicks needed to reach essential info

**Token Impact**: Externalizing L3+ content saves 250-500 tokens per document, improves maintainability

---

### Anti-Pattern 4: Content Duplication (Redundancy Failure)

**Symptom**: Same content repeated across multiple agents without using base-agent-pattern.md inheritance.

**Example**:
```markdown
❌ BAD (DUPLICATED ACROSS 22 AGENTS):
## Knowledge Base Integration
When researching library/framework specifics:
1. Check Context7 first (authoritative, version-specific)
2. Use WebFetch for supplementary cross-reference
3. WebSearch for community patterns/tutorials
[... 45 lines of identical content ...]

## Pre-Flight Checklist
Before implementation:
- [ ] Requirements clear
- [ ] Existing patterns identified
[... 30 lines of identical content ...]
```

**Impact**:
- ~1,150 tokens wasted per agent (proven across 22 agents)
- Maintenance burden: update 22+ places for single change
- Increased risk of inconsistency (agents diverge over time)

**Fix**:
```markdown
✅ GOOD (INHERITED):
**Extends**: .claude/docs/01-guides/agents/base-agent-pattern.md

**Inherited Sections**:
- Knowledge Base Integration
- Pre-Flight Checklist
- Core Workflow
- Error Recovery
- Parallel Execution
- Validation Checklist

## [Agent-Specific Unique Content]
Domain-specific workflows, specialized capabilities, unique patterns.
```

**Detection**:
- Compare agents for identical sections (>80% text similarity)
- Check for base-agent-pattern extension declaration
- Verify agents have <20% content duplication

**Token Impact**: ~1,150 tokens saved per agent through inheritance (26,000 tokens across 22 agents)

---

### Anti-Pattern 5: Inline Verbose Examples (Token Density Failure)

**Symptom**: 50+ line examples, complete methodology walkthroughs, or verbose explanations embedded inline instead of externalized to guides.

**Example**:
```markdown
❌ BAD (INLINE VERBOSE):
## Documentation Optimization Methodology

**Overlap Calculation**:
The overlap score combines three dimensions using weighted formula:

overlap_score = (jaccard_similarity × 0.4) + (structural_overlap × 0.3) + (semantic_similarity × 0.3)

**Jaccard Similarity Calculation**:
1. Extract keywords from agent prompt using TF-IDF
2. Extract keywords from guide using same methodology
3. Calculate intersection and union of keyword sets
4. Compute J(A,G) = |A ∩ G| / |A ∪ G|

[... 50+ more lines of detailed calculation methodology ...]

**Structural Overlap Analysis**:
[... 40+ lines of structural matching algorithm ...]

**Semantic Similarity Computation**:
[... 45+ lines of embedding comparison methodology ...]
```

**Impact**:
- 250-400 tokens per verbose section
- Bloats agent definition beyond <500 line target
- Repeated reading for users (methodology doesn't change)

**Fix**:
```markdown
✅ GOOD (EXTERNALIZED):
## Documentation Optimization Methodology

**Overlap Score Formula**:
```
overlap_score = (jaccard × 0.4) + (structural × 0.3) + (semantic × 0.3)
```

**Thresholds**: ≥0.80 strong | ≥0.70 recommend | <0.70 insufficient

**Detailed Calculation**: See `.claude/docs/01-guides/documentation/doc-optimization-methodology.md` for:
- Jaccard similarity computation (keyword TF-IDF extraction, intersection/union)
- Structural overlap analysis (heading matching, section similarity)
- Semantic similarity (embedding comparison, cosine distance)
```

**Detection**:
- Flag sections >50 lines with methodology/example content
- Check for external guide references
- Verify agent definition <500 lines (or has justification)

**Token Impact**: 250-400 tokens saved per section externalized

---

### Anti-Pattern 6: Missing Quick Reference (Navigation Failure)

**Symptom**: Documents >300 lines without Quick Reference or Table of Contents at the top, forcing users to scan entire document to find formulas/workflows.

**Example**:
```markdown
❌ BAD (NO QUICK REFERENCE):
# Agent Name

## Role & Boundaries
You are a specialist...

[... 200 lines of detailed description ...]

## Workflow Details
The process involves...

[... 150 lines of methodology ...]

## Confidence Scoring  ← User has to scroll 350+ lines to find this!
confidence = (domain × 0.6) + (work_type × 0.3)
```

**Impact**:
- Users scan entire document to find formulas (wasted time, tokens)
- Can't predict where content lives (information scent failure)
- Common tasks (>30% frequency) require full document read

**Fix**:
```markdown
✅ GOOD (QUICK REFERENCE FIRST):
# Agent Name

## Quick Reference

| **Formula** | **Application** | **Threshold** |
|-------------|-----------------|---------------|
| Confidence | (domain × 0.6) + (work_type × 0.3) + (track_record × 0.1) | ≥0.5 |
| Complexity | (components × 0.4) + (dependencies × 0.3) + (unknowns × 0.3) | <0.3 low, >0.7 high |

**Workflow**: Observe → Orient → Decide → Act (OODA Loop)

**See**: [Detailed Methodology](#detailed-methodology) for complete process

---

## Role & Boundaries
[Detailed content below Quick Reference...]
```

**Detection**:
- Check for "Quick Reference" section in first 50 lines
- Flag documents >300 lines without TOC
- Verify formulas/workflows accessible from L0

**Token Impact**: Quick Reference enables 80%+ task completion from L0 (reduces disclosure overhead ~100-200 tokens)

---

## Detection Checklist

Use this checklist when reviewing agent documentation:

- [ ] **Buried Essentials**: All critical formulas/workflows in Quick Reference (L0)?
- [ ] **Vague Labels**: All headings predictive (>80% accuracy) with action verbs or domain terms?
- [ ] **Excessive Depth**: Maximum 2 disclosure levels visible (h1, h2), L3+ externalized?
- [ ] **Content Duplication**: <20% duplication, base-agent-pattern extension declared?
- [ ] **Inline Verbose**: No sections >50 lines with methodology (externalized to guides)?
- [ ] **Missing Quick Reference**: Quick Reference present in first 50 lines for >300 line docs?

---

## Integration with Agent Analysis

**documentation.md** should detect these anti-patterns during token optimization analysis.

**claude-code-ecosystem.md** validates progressive disclosure compliance (anti-patterns 1, 3, 6).

**tech-debt-investigator.md** identifies duplication (anti-pattern 4) and verbosity (anti-pattern 5) as documentation debt.

**claude-code-ecosystem.md** prevents anti-patterns during agent creation by enforcing Quick Reference, base-pattern extension, and external guide references.

**See Also**:
- `.claude/docs/01-guides/documentation/progressive-disclosure-validation-framework.md` - Layering strategies
- `.claude/docs/01-guides/agents/base-agent-pattern.md` - Inheritance model
- `.claude/docs/01-guides/documentation/doc-optimization-methodology.md` - Optimization formulas

---

**Version**: 1.0
**Source**: Worker 2 research findings + Nielsen Norman Group progressive disclosure principles
