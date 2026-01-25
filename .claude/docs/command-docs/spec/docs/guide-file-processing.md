# Guide File Processing

Extraction patterns for `file:path` inputs in the `/spec` workflow.

---

## Overview

When users provide `file:docs/04-guides/some-guide.md`, the `/spec` command:
1. Reads the complete guide file
2. Extracts business goals, scenarios, and technical patterns
3. Structures context for specification generation
4. Preserves technical patterns for planning phase propagation

---

## Pattern Recognition

**Input Format**: `file:[path-to-guide.md]`

**Examples**:
- `file:docs/04-guides/auth.md`
- `file:docs/04-guides/claude-code/codebase-navigation-guide.md`
- `file:docs/04-guides/domain-specific/Multi-Agent-System.md`

**Validation**:
- File must exist and be readable
- Only `.md` files currently supported
- Path can be relative or absolute

---

## Extraction Strategy

### 1. Read Complete Guide File

- Load full content for comprehensive analysis
- Preserve structure (sections, code blocks, examples)
- Identify document type (technical guide, API reference, pattern catalog)

### 2. Extract Business Goals & User Value

**Source Sections**:
- Overview/Introduction
- Purpose/Goals
- Use Cases
- Core Concepts

**Extract**:
- Primary business goals → SPEC: Business Case
- User value propositions → SPEC: User Scenarios
- Performance targets → SPEC: Success Criteria
- Use cases → SPEC: Acceptance Criteria

### 3. Extract Technical Approaches & Patterns

**Source Sections**:
- Workflow descriptions
- Algorithm explanations
- Tool listings
- Code examples
- Decision trees

**Extract**:
- Implementation workflows → SPEC: Technical Expectations
- Required tools → SPEC: Dependencies
- Algorithm patterns → SPEC: Technical Constraints
- Code examples → Reference for planning phase
- Decision logic → SPEC: Business Logic Patterns

### 4. Extract Constraints & Requirements

**Source Elements**:
- Performance targets (time limits, accuracy thresholds)
- Quality requirements (coverage, reliability)
- Resource constraints (memory, CPU, API limits)
- Integration requirements (systems, protocols)

**Map To**:
- Time limits → NFR: Performance
- Quality thresholds → NFR: Quality
- Resource limits → NFR: Scalability
- Integrations → SPEC: Dependencies

---

## Context Structure

### Reference Guide Context Block

```json
{
  "referenceGuideContext": {
    "guidePath": "[absolute path to guide file]",
    "guideType": "technical_implementation_guide",
    "guideTitle": "[extracted from guide header]",
    "extractedGoals": [
      "Goal 1 from guide overview",
      "Goal 2 from guide purpose"
    ],
    "extractedScenarios": [
      "Scenario 1 from use cases",
      "Scenario 2 from examples"
    ],
    "technicalPatterns": {
      "primaryApproach": "[main technical approach]",
      "tools": ["tool1", "tool2", "tool3"],
      "workflows": ["workflow1", "workflow2"],
      "algorithms": ["algorithm1", "algorithm2"]
    },
    "performanceTargets": {
      "target_name": "< threshold",
      "another_target": "< threshold"
    },
    "qualityTargets": {
      "accuracy": "95%+",
      "other": "value"
    },
    "preserveForPlanning": true
  }
}
```

---

## Example Extraction

### Input: `file:docs/04-guides/codebase-navigation-guide.md`

**Guide Content Summary**:
- Purpose: Enable efficient codebase exploration
- Tools: ripgrep, tree-sitter, ctags
- Approach: Three-layer search strategy
- Performance: <1s initial, <5s dependency mapping

### Extracted Business Goals

```markdown
1. Enable developers to efficiently navigate and understand codebases
2. Support impact analysis for code changes
3. Provide fast and accurate dependency mapping
4. Deliver search results within strict performance budgets
```

### Extracted User Scenarios

```markdown
1. Initial Discovery: Find all code mentioning a specific function/class
2. Dependency Mapping: Understand what code depends on a module
3. Impact Analysis: Determine what will break if code changes
4. Semantic Search: Find similar code patterns across codebase
```

### Extracted Technical Approaches

```markdown
- Three-Layer Search Strategy: Quick (ripgrep) → Smart (tree-sitter) → Deep (custom)
- Tools: ripgrep, grep, find, ctags, tree-sitter, language servers
- Memory Structure: Per-file cache + global dependency graph
- Optimization: Bloom filters, parallel search, early termination
```

### Extracted Constraints

```markdown
- Initial search: < 1 second
- Dependency mapping: < 5 seconds
- Full impact analysis: < 30 seconds
- Accuracy: 95%+ for most operations
- Philosophy: "95% quickly beats 100% slowly"
```

### Feature Name Derivation

From guide: "codebase-navigation-guide.md"
Derived: "Codebase Navigation Agent" or "003-codebase-navigation"

---

## Preservation for Planning

**Key Principle**: Technical patterns extracted from guides MUST be preserved for `/plan` phase.

**Why**: Guide files often contain domain-specific implementation approaches that should inform architecture decisions.

**How**:
1. Include `referenceGuideContext` in specification generation
2. Set `preserveForPlanning: true`
3. Store guide path in SPEC.md metadata
4. `/plan` command reads this context for architecture phase

---

## Common Guide Types

| Type | Extraction Focus | Example |
|------|------------------|---------|
| Technical Implementation | Workflows, tools, algorithms | codebase-navigation-guide.md |
| API Reference | Endpoints, data models, errors | api-patterns.md |
| Pattern Catalog | Design patterns, anti-patterns | best-practices.md |
| Domain Guide | Business rules, constraints | trading-rules.md |

---

## Error Cases

### File Not Found
```
❌ Guide file not found: docs/04-guides/missing.md

Verify path and try again.
```

### Unsupported Format
```
❌ Unsupported file format: .pdf

Currently only .md files supported.
```

### Empty or Minimal Content
```
⚠️ Guide file has minimal extractable content.

Proceeding with limited context. Consider providing more detailed guide.
```

### No Clear Goals/Patterns
```
⚠️ Could not extract clear business goals from guide.

Manual input may be required. Extracted patterns:
- [list what was found]
```
