# Prompt Anti-Patterns Detection

**Purpose**: Comprehensive catalog of agent prompt anti-patterns with detection methods and fixes

**Reference**: Used by `.claude/agents/dev-tools/prompt-evaluator/prompt-evaluator.md`

**Version**: 1.0

---

## Overview

This document catalogs the top 10+ anti-patterns in agent prompt design, organized by category with severity classification, detection methods, and fix guidance.

---

## Performance Anti-Patterns

### Anti-Pattern 1: Tool Initialization Bloat

**Description**: Agent declares multiple heavy tools (Bash + WebSearch + Context7 + Write) without justification

**Severity**: Major (increases initialization time ~5-10s, wastes context window)

**Detection**:
```bash
grep "^tools:" .claude/agents/agent-name.md
# Heavy tools: Write, Bash, WebSearch, Context7, WebFetch
# Count >3 heavy tools = bloat
```

**Indicators**:
- Agent declares 4+ heavy tools
- No justification for tool combination
- Tools not used in workflows
- Read-only agent with Write tool

**Fix**: Remove unused tools, use lighter alternatives, justify heavy combinations.

---

### Anti-Pattern 2: Scope Creep

**Description**: Agent tries to handle multiple responsibilities instead of single purpose
**Severity**: Critical (violates single responsibility principle)
**Detection**: Look for "and", "or", multiple verbs in Role & Boundaries
**Fix**: Split into multiple single-purpose agents, define clear boundaries.

---

### Anti-Pattern 3: Missing Base Pattern

**Description**: Agent does not extend base-agent-pattern.md, duplicating ~1,150 tokens
**Severity**: Major (wastes tokens, increases maintenance burden)
**Detection**: `grep -i "base.agent.pattern" .claude/agents/agent-name.md`
**Fix**: Add "Base Agent Pattern Extension" section, list inherited sections.

---

## Schema & Compliance Anti-Patterns

### Anti-Pattern 4: Schema Non-Compliance

**Description**: Agent does not extend base-agent.schema.json or lacks schema reference
**Severity**: Critical (breaks validation, inconsistent output structure)
**Detection**: Check for schema reference and SUCCESS/FAILURE structures
**Fix**: Add Schema Reference section, ensure base schema inheritance.

---

### Anti-Pattern 5: Vague Tool Descriptions

**Description**: Tool usage not explained clearly for new team members
**Severity**: Major (reduces agent usability)
**Detection**: Tool descriptions <1 sentence, no examples
**Fix**: Apply "new team member" standard, add specific usage examples.

---

## Operational Anti-Patterns

### Anti-Pattern 6: No Termination Rules

**Description**: Missing <20s per task completion guidance or explicit termination criteria
**Severity**: Major (leads to long-running operations)
**Detection**: `grep -i "terminat\|<20s\|completion\|timeout" .claude/agents/agent-name.md`
**Fix**: Add time targets, "good enough" criteria, iteration limits.

---

### Anti-Pattern 7: MultiEdit on Large Files

**Description**: Using MultiEdit for files >22.5K tokens (breaks Claude's editing capability)
**Severity**: Critical (operation will fail)
**Detection**: Check for MultiEdit usage guidance and size warnings
**Fix**: Document MultiEdit size limit, add decision tree for Edit vs MultiEdit vs Write.

---

### Anti-Pattern 8: Parallel Write Operations

**Description**: Concurrent edits on same file or directory without coordination
**Severity**: Critical (race conditions, data loss)
**Detection**: Check Write/Edit tools + parallel execution awareness
**Fix**: Document serialization requirements, add coordination protocol.

---

## Security & Error Handling Anti-Patterns

### Anti-Pattern 9: Missing Error Recovery

**Description**: No FAILURE mode documentation or recovery guidance
**Severity**: Critical (integration failures, poor error messages)
**Detection**: `grep -i "failure\|error.recovery" .claude/agents/agent-name.md`
**Fix**: Document FAILURE response structure, add recovery strategies.

---

### Anti-Pattern 10: No Security Validation

**Description**: Security-critical operations without validation or safety checks
**Severity**: Critical (security vulnerabilities, data exposure)
**Detection**: Check for Bash without command whitelisting, URLs without domain whitelist
**Fix**: Add input validation, document security boundaries, include validation checkpoints.

---

## Prompt Engineering Anti-Patterns

### Anti-Pattern 11: Kitchen-Sink Prompts

**Description**: Including guidance for failures that haven't occurred (hypothetical scenarios)
**Severity**: Major (wastes 200-500+ tokens on unlikely edge cases)
**Detection**: `grep -i "if.*fails\|in case\|might.*happen" .claude/agents/agent-name.md`
**Fix**: Apply MVP methodology, remove guidance for undocumented failures, add guidance ONLY after failure observed.

**Pruning Decision Tree**:
1. Has this failure occurred? NO → Remove section
2. Is failure documented? NO → Remove or add evidence
3. Is guidance actionable? NO → Remove or clarify
4. Is section >50 tokens? YES → Externalize to guide

---

### Anti-Pattern 12: Full Path Doc References

**Description**: Using full directory paths like `.claude/docs/01-guides/file.md` or `docs/04-guides/code-review/file.md` instead of filename-only references like `file.md`

**Severity**: Major (breaks when files move during reorganization, increases maintenance burden)

**Detection**:
```bash
grep -E "\.claude/docs/|docs/[0-9]+-" .claude/agents/agent-name.md
# Matches: .claude/docs/01-guides/agents/base-agent-pattern.md
# Should be: base-agent-pattern.md
```

**Indicators**:
- References contain `.claude/` prefix
- References contain numbered directory patterns like `01-guides/`, `04-guides/`
- Full paths to docs instead of just filenames

**Why This Matters**:
- Files move during documentation reorganization
- AI can search for filename, cannot predict new paths
- Maintenance burden: every reorg requires updating all paths

**Fix**: 
1. Replace full paths with filename only
2. Agent should use `Glob("**/{filename}")` to locate file
3. Exception: Glob patterns for directory scanning (e.g., `Glob(".claude/docs/**/*.md")`) are acceptable

**Examples**:
```markdown
# ❌ WRONG
**Extends**: `.claude/docs/01-guides/agents/base-agent-pattern.md`
See `docs/04-guides/documentation/creating-ai-readable-documentation-framework.md`

# ✅ CORRECT
**Extends**: `base-agent-pattern.md`
See `creating-ai-readable-documentation-framework.md`
```

---

## Detection Workflow

1. **Read agent definition** (full file)
2. **Scan for anti-patterns** (Grep patterns for each)
3. **Classify severity** (Critical/Major/Minor)
4. **Collect evidence** (file:line citations)
5. **Generate fix guidance** (specific, actionable steps)
6. **Priority score** using formula: `(Impact × 0.4) + (Effort⁻¹ × 0.3) + (Risk × 0.3)`

---

## Future Anti-Patterns

Candidates for future addition:
- Anti-Pattern 13: Inconsistent XML tag usage
- Anti-Pattern 14: Missing confidence scoring
- Anti-Pattern 15: Duplicate documentation across agents
- Anti-Pattern 16: No batch operation support

---

## Cross-References

**AI-Readability Anti-Patterns**: See `docs/04-guides/documentation/creating-ai-readable-documentation-framework.md` for additional anti-patterns related to AI-readable documentation (buried keywords, implicit relationships, prose-heavy formatting, missing structural markers).
