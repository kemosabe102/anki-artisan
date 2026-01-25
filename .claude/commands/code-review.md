---
argument-hint: '<source> [--focus=security|performance|quality|design|all] [--mode=quick|comprehensive] [--output=path] [--resume] [--force-restart]'
description: 'Multi-agent code review with confidence-driven investigation. Use for quality assessment, pre-commit validation, security scans. Severity-prioritized findings with research validation.'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__plugin_perplexity_perplexity__perplexity_search, mcp__plugin_perplexity_perplexity__perplexity_research]
model: opus
---

# Code Review Command

*Multi-agent review with confidence-driven investigation*

---

## Core Behavior

YOU ARE A CODE REVIEW ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> Discover files -> Route to agents -> Investigate findings -> Generate report

### The Flow
User: /code-review <source> -> File Discovery -> Agent Routing -> Parallel Review -> Confidence Investigation -> Consolidation -> Report

### Anti-Patterns (NEVER DO)
- Report low-confidence findings as facts (<0.75 confidence)
- Skip investigation for Critical/High severity findings
- Hard-code language-to-agent routing (delegate to orchestrator)
- Run review on binary/generated files

### Good Patterns (ALWAYS DO)
- Investigate findings until confidence >= 0.75 or escalate
- Use Context7 first (free), Perplexity second (paid) - target 4:1 ratio
- Deduplicate findings (hash + semantic)
- Include verification commands with every finding

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/code-review --all` | All Changes | Review uncommitted changes |
| `/code-review --files <paths>` | Specific | Review specified files |
| `/code-review --branch <name>` | Branch | Compare branch vs main |
| `/code-review --commit <hash>` | Commit | Review specific commit |
| `--focus=security` | Focus | Prioritize security agents |
| `--mode=quick` | Quick | 3 core agents, minimal investigation |
| `--mode=comprehensive` | Full | 3 core + 0-2 dynamic, full investigation |

---

## Resume Support

| Flag | Behavior |
|------|----------|
| (default) | Check for checkpoint, offer resume if found |
| `--resume` | Require checkpoint, fail if not found |
| `--force-restart` | Ignore checkpoint, start fresh |

### Checkpoint Location
`temp/code-review/{session_id}/checkpoint.json`

### Checkpoint Recovery
On command start:
1. Check for existing checkpoint in temp/code-review/
2. If found AND < 24h old: Prompt "Resume from Phase {N}? [Y/n]"
3. If stale (> 24h): Delete and start fresh
4. Write checkpoint after each phase (P0-P6)
5. Delete checkpoint on successful completion

---

## Workflow Overview

```text
PHASE 0: PRE-FLIGHT VALIDATION [HYBRID]
  |-- Critical-path tool check (direct - blocks entire review):
  |     - git: Bash("git --version") - REQUIRED, abort if missing
  |-- Optional tool check (delegated):
  |     - Task(git-github, "Check semgrep availability")
  |     - IF semgrep missing: Continue with reduced agent set (no sast-scanner)
  |-- Checkpoint write: temp/code-review/{session}/checkpoint.json
  |-- Output: {tools_available: [git, semgrep?], warnings: []}

PHASE 1: FILE DISCOVERY -> Task(git-github)
  |-- Task(git-github, "Discover files for code review:
  |       Source: {source_flag} {source_value}
  |       Exclusions: .claude/**, docs/**, node_modules/**
  |       Return: {files: [{path, language}], warnings: []}")
  |-- Validate output, write checkpoint
  |-- Output: [(file, language), ...]

PHASE 2: AGENT ROUTING -> Task(git-github) for batching
  |-- Group by language -> Batch (max 5 files) -> Select reviewers
  |-- Output: commit_batches[] with assigned agents

PHASE 3: MULTI-AGENT REVIEW -> 3 core + 0-2 dynamic (parallel)
  |-- Core: python-code-reviewer, tech-debt-investigator, sast-scanner
  |-- Dynamic: Select via Agent Selection Framework (confidence > 0.8)
  |-- Output: raw_findings[]

PHASE 4: CONFIDENCE INVESTIGATION [CRITICAL - INLINE PROTOCOL]
  |-- For EACH finding, execute this decision tree:
  |
  |-- IF confidence >= 0.90:
  |     Action: Report as-is, no investigation
  |     Output: finding unchanged
  |
  |-- IF confidence 0.75-0.89:
  |     Action: Optional Context7 validation
  |     Steps:
  |       1. Task(researcher-external, "Validate finding: {finding}")
  |       2. IF docs confirm: confidence += 0.10 (cap 0.95)
  |       3. IF docs contradict: downgrade to "Open Question"
  |       4. Add source citation to finding
  |
  |-- IF confidence < 0.75:
  |     Action: MANDATORY investigation
  |     Steps:
  |       1. Task(researcher-external, "Validate finding: {finding}")
  |       2. IF confidence boosted to >= 0.75: DONE
  |       3. IF still < 0.75: Task(researcher-external, "Research: {finding as question}")
  |       4. Cross-reference with OWASP/PEP/RFC standards
  |       5. IF strong consensus: confidence = 0.80-0.90
  |       6. IF no consensus: confidence stays < 0.70
  |
  |-- IF confidence < 0.50 after ALL research:
  |     Action: ESCALATE - do NOT report as fact
  |     Move to "Open Questions" section with:
  |       - Research attempts documented
  |       - Why confidence couldn't be raised
  |       - Recommendation for manual review
  |
  |-- Output: validated_findings[] with investigation_trail
  |
  |-- SPECIAL RULE FOR CRITICAL SEVERITY:
  |     Critical findings ALWAYS get Context7 + Perplexity research
  |     regardless of initial confidence (even if >= 0.90)

PHASE 5: CONSOLIDATION -> Dedupe + Synthesis + Conflict Resolution
  |-- Hash dedup (exact) -> Semantic dedup (>0.8 similarity)
  |-- SEVERITY CONFLICT RESOLUTION:
  |     - IF same finding, different severities from multiple agents:
  |       - Precedence: sast-scanner > python-code-reviewer > tech-debt-investigator
  |       - IF gap > 1 level (e.g., Critical vs Medium): Flag for user review
  |       - Record resolution in finding.conflict_resolution
  |-- If 3+ findings overlap > 0.7: Apply synthesis framework
  |-- Output: consolidated_findings[]

PHASE 6: REPORT GENERATION
  |-- Severity-ordered sections (Critical -> Nit)
  |-- Verification commands per finding
  |-- Investigation summary + Open Questions
```

**Detailed Phase Documentation**: `.claude/docs/command-docs/code-review/docs/workflow-phases.md`

---

## Agent Delegation

| Phase | Agent | Operation |
|-------|-------|-----------|
| 0 | git-github | Semgrep availability check (git check remains direct) |
| 1 | git-github | File discovery and language detection |
| 2 | git-github | File batching (max 5 per batch) |
| 3 | python-code-reviewer | Language-specific review |
| 3 | tech-debt-investigator | Debt analysis (debt_score, TDR) |
| 3 | sast-scanner | Security scan (OWASP, secrets) |
| 3 | Dynamic (0-2) | Agent Selection Framework, confidence > 0.8 |
| 4 | researcher-external | External research (Context7 library docs, Perplexity web) |
| 5 | (orchestrator) | Deduplication + synthesis + conflict resolution |
| 6 | (orchestrator) | Report generation |

**Exact Task() syntax**: `.claude/docs/command-docs/code-review/docs/delegation-patterns.md`

---

## Confidence-Severity Matrix

| Severity | Min Confidence | Investigation Required |
|----------|---------------|------------------------|
| Critical | 0.90 | ALWAYS Context7 + Perplexity (regardless of initial confidence) |
| High | 0.80 | Context7 if < 0.90 |
| Medium | 0.75 | Context7 if < 0.85 |
| Low | 0.70 | Context7 if security-relevant OR user requested --focus=security |
| Nit | 0.60 | Skip (low impact, not worth research cost) |

**Critical Finding Rule**: Even if a Critical finding starts at 0.95 confidence, it MUST be investigated. Security issues require validation regardless of initial confidence.

**Rule**: If confidence < minimum after research -> Downgrade severity OR escalate to "Open Questions"

---

## Error Recovery (Quick Reference)

| Error Type | Recovery |
|------------|----------|
| No files to review | Check git status, verify source flag |
| Invalid source flag | Show correct usage, require ONE source |
| Language not supported | Report gap, continue with available |
| Agent fails | Partial review, report which agent failed |
| Context7 rate limit | Fallback to Perplexity |
| Both APIs offline | Degrade to agent confidence only (cap 0.50) |
| Confidence < 0.50 after research | Move to "Open Questions", DO NOT report as fact |

**Detailed recovery patterns**: `.claude/docs/command-docs/code-review/docs/error-handling.md`

---

## Output Format

### Review Success
```text
Code Review Report
==================
Status: APPROVED | APPROVED_WITH_CONDITIONS | CHANGES_REQUIRED

Summary:
- Files: N (X Python, Y TypeScript)
- Findings: N (Critical: X, High: Y, Medium: Z)
- Investigation: N findings researched (Context7: X, Perplexity: Y)

CRITICAL (must fix):
[CRIT-001] SQL Injection (src/api.py:42)
  Confidence: 0.92 | Verified: Context7 + OWASP A01
  Fix: Use parameterized queries
  Verify: rg -n 'f"SELECT.*{' src/

HIGH (should fix):
...

Open Questions (needs manual review):
[OQ-001] Potential race condition (confidence: 0.45)
  Research inconclusive - manual review required
```

---

## Quick Examples (Inline)

### Example A: Review Uncommitted Changes
```
User: /code-review --all

Phase 1: git status --porcelain -> 5 Python files discovered
Phase 2: git-github groups into 1 batch (5 files, python-code-reviewer)
Phase 3: Launch 3 agents parallel:
  - python-code-reviewer: 4 findings (1 High, 2 Medium, 1 Low)
  - tech-debt-investigator: debt_score=34, TDR=0.15
  - sast-scanner: 1 finding (Medium - hardcoded timeout)
Phase 4: 2 findings at 0.72 confidence -> Context7 boost to 0.85
Phase 5: 1 duplicate removed (same issue, 2 agents)
Phase 6: Output APPROVED_WITH_CONDITIONS

Report: 4 unique findings (0 Critical, 1 High, 2 Medium, 1 Low)
```

### Example B: Security-Focused Review
```
User: /code-review --all --focus=security

Phase 1: 3 Python files in packages/auth/
Phase 3: sast-scanner gets priority weighting
  - sast-scanner: 2 Critical (SQL injection, hardcoded secret)
  - python-code-reviewer: 1 High (input not sanitized)
Phase 4: Critical findings -> ALWAYS investigate
  - SQL injection: Context7 (SQLAlchemy docs) + Perplexity (OWASP A03)
  - Confidence: 0.88 -> 0.94 (confirmed)
Phase 6: Output CHANGES_REQUIRED

Report: CRITICAL issues block merge
  [CRIT-001] SQL Injection (packages/auth/queries.py:42)
    Confidence: 0.94 | Verified: Context7 + OWASP A03:2021
    Fix: Use parameterized queries
    Verify: rg -n 'f"SELECT.*{' packages/auth/
```

### Example C: Branch Comparison
```
User: /code-review --branch feature/new-api

Phase 1: git diff --name-only main...feature/new-api -> 12 files
Phase 2: git-github groups into 3 batches (4+4+4 files)
Phase 3: 3 parallel batches, each with 3 core agents (9 agent calls total)
Phase 5: Synthesis triggered (5 overlapping findings > 0.7 similarity)
Phase 6: Output APPROVED_WITH_CONDITIONS

Report: Consolidated recommendations with trade-off analysis
```

---

## Knowledge Base

- `.claude/docs/command-docs/code-review/docs/workflow-phases.md` - Detailed 7-phase documentation (Phase 0-6)
- `.claude/docs/command-docs/code-review/docs/delegation-patterns.md` - Exact Task() call syntax
- `.claude/docs/command-docs/code-review/docs/error-handling.md` - Error scenarios and recovery
- `.claude/docs/command-docs/code-review/docs/confidence-investigation.md` - Phase 4 confidence-driven research
- `.claude/docs/command-docs/code-review/docs/finding-schema.md` - Complete finding structure
- `.claude/docs/command-docs/code-review/examples/usage-examples.md` - Complete workflow examples
- `.claude/docs/command-docs/code-review/schemas/code-review.schema.json` - Finding JSON schema

---

## Orchestrator Integration

**Trigger Keywords**: review code, code review, analyze code, check code quality, validate code

**Delegation Pattern**:
```
User: "Review the authentication module"
Claude Code (OBSERVE): Parse request -> Identify /code-review trigger + scope
Claude Code (ORIENT): packages/auth/ exists with 8 Python files
Claude Code (DECIDE): ASC = 0.97 -> Delegate to /code-review
Claude Code (ACT): SlashCommand(command="/code-review --files packages/auth/")
```

**Integration Points**:
- **Upstream**: /implement, code modifications
- **Downstream**: /git prepare (Phase 3 quality gates), bug fixes
- **Parallel**: 3-5 agents simultaneously

**Anti-Patterns** (do NOT use /code-review for):
- Automated fixes (use debugger after review)
- Specification validation (use /spec review)
- Linting only (use ruff/black directly)
