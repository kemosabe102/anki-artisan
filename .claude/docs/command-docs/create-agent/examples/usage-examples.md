# Usage Examples

Complete workflow examples for the `/create-agent` command.

---

## Example 1: Standard Template-Based Workflow

Basic end-to-end workflow using an existing definition file.

```bash
User: /create-agent .claude/definitions/security-scanner.md

# Phase 0-1: Parse & Validate
Claude: [Parses definition, validates preconditions, checks duplicates]

Output:
Definition parsed successfully
- Name: security-scanner
- Domain: packages/**
- Capabilities: 5 identified
- No duplicates found

Proceeding to Phase 2...

# Phase 2: Requirements Assessment
Claude: [Delegates to context-readiness-assessor]

Output:
Information requirements identified:

High-Confidence (Essential):
- OWASP security patterns (0.95)
- Static analysis techniques (0.92)
- Vulnerability classification (0.88)

Medium-Confidence (Important):
- Security testing frameworks (0.72)
- Code injection patterns (0.68)

Proceed with high + medium topics? [Y/n/modify]

User: Y

# Phase 3-7: Research, Documentation, Schema, Agent
Claude: [Executes research, generates documentation, creates schema and agent]

Output:
Phase 4: 4 research workers completed (avg confidence: 0.84)
Phase 5: 3 documentation files generated
Phase 6: Schema created (12 fields defined)
Phase 7: Agent definition generated (4,200 tokens)

# Phase 8: Quality Validation
Claude: [Runs 5 parallel validators]

Output:
Quality Validation: PASSED

- Template Compliance: 100%
- Documentation Health: 88/100
- Prompt Quality: No high-severity anti-patterns
- Context Optimization: 4,200 tokens (within target)
- Quality Matrix: 78/100

Proceeding to Phase 9...

# Phase 9: Review
Claude: [Presents summary]

Output:
# security-scanner - Ready for Review

Type: Analyzer
Domain: packages/**

Orchestrator Description:
"Scan Python code for security vulnerabilities including injection
flaws, authentication issues, and sensitive data exposure. Call
when reviewing code before deployment or after security-related changes."

Core Capabilities:
- Detect OWASP Top 10 vulnerabilities (0.95)
- Identify hardcoded secrets (0.92)
- Analyze authentication patterns (0.88)
- Generate remediation recommendations (0.85)
- Track vulnerability severity (0.82)

Quality Score: 78/100

Options:
1. Approve and finalize
2. Refine specific sections
3. Cancel creation

User: 1

# Phase 10: Finalization
Claude: [Writes files, updates integrations]

Output:
# Agent Creation Complete: security-scanner

## Files Created
- .claude/agents/dev-tools/security-scanner/security-scanner.md
- .claude/agents/dev-tools/security-scanner/schemas/security-scanner.schema.json
- .claude/agents/dev-tools/security-scanner/docs/security-patterns.md
- .claude/agents/dev-tools/security-scanner/docs/vulnerability-detection.md
- .claude/agents/dev-tools/security-scanner/examples/delegation-examples.md

## Integrations Updated
- CLAUDE.md (delegation table)
- orchestrator-workflow.md (agent legend)
- agent-categorization.md

## Next Steps
1. RESTART Claude Code session
2. Test with: Task(subagent_type="security-scanner", prompt="Scan packages/auth/ for vulnerabilities")
```

---

## Example 2: Interactive Mode

Creating an agent from scratch using guided Q&A.

```bash
User: /create-agent --create-definition api-optimizer.md

# Phase I-1: Capture Idea
Claude: Describe your agent idea in 2-3 sentences...

User: "An agent that analyzes REST API endpoints for performance issues.
       It should identify slow queries, inefficient serialization, and
       suggest caching strategies. Call it when API response times degrade."

# Phase I-2: Analyze & Propose
Claude: [Delegates to claude-code-ecosystem]

Output:
Analysis complete. Proposed structure:

Name Options:
1. api-performance-optimizer (confidence: 0.91)
2. rest-api-analyzer (confidence: 0.82)
3. endpoint-profiler (confidence: 0.75)

Domain: packages/** (confidence: 0.93)
Type: Analyzer (confidence: 0.89)

Purpose: "Analyze REST API endpoints for performance bottlenecks
including slow database queries, inefficient serialization, and
missing cache opportunities. Call when API response times exceed
acceptable thresholds."

Capabilities (confidence):
1. Profile endpoint response times (0.95)
2. Identify slow database queries (0.92)
3. Analyze serialization overhead (0.88)
4. Recommend caching strategies (0.85)
5. Generate optimization roadmap (0.82)

# Phase I-3: Interactive Refinement
Claude: Choose name [1/2/3] or custom:
User: 1

Claude: Accept domain packages/**? [Y/n]
User: Y

Claude: Accept type Analyzer? [Y/n]
User: Y

Claude: Accept purpose statement? [Y/n/edit]
User: Y

Claude: Capabilities - Accept all? [A/R/E/+]
User: + "Compare before/after metrics"

Claude: Added capability. Final list:
1. Profile endpoint response times (0.95)
2. Identify slow database queries (0.92)
3. Analyze serialization overhead (0.88)
4. Recommend caching strategies (0.85)
5. Generate optimization roadmap (0.82)
6. Compare before/after metrics (user-added)

Confirm? [Y/n]
User: Y

# Phase I-4: Generate Definition
Claude: [Generates definition file]

Output:
Definition file created: api-optimizer.md

Preview:
---
# Agent Definition Input
name: api-performance-optimizer
domain: packages/**
type: Analyzer
purpose: "Analyze REST API endpoints for performance bottlenecks..."
...
---

# Phase I-5: Present Options
Claude: Choose [P]roceed / [R]eview first / [G]enerate:
User: P

[Continues to standard 10-phase workflow...]
```

---

## Example 3: With Context Directory

Providing additional domain knowledge via `--context-dir`.

```bash
User: /create-agent security-analyzer.md --context-dir=docs/security-patterns/

# Phase 1: Parse & Validate
Claude: [Standard parsing]

# Phase 2: Requirements
Claude: [Identifies 6 high-confidence topics]

# Phase 3: Context Analysis
Claude: [Analyzes user-provided context]

Output:
Context Analysis Complete

Files analyzed: 5
- security-patterns/owasp-top-10.md
- security-patterns/injection-prevention.md
- security-patterns/auth-best-practices.md
- security-patterns/data-protection.md
- security-patterns/logging-security.md

Coverage Analysis:
- OWASP patterns: 95% covered (from owasp-top-10.md)
- Injection prevention: 88% covered (from injection-prevention.md)
- Authentication patterns: 82% covered (from auth-best-practices.md)
- Logging security: 75% covered (from logging-security.md)

Gaps requiring research:
- Cryptographic best practices: 0% coverage
- Security testing frameworks: 0% coverage

Proceeding to Phase 4 with reduced research scope...

# Phase 4: Research (Reduced)
Claude: [Only researches gaps - 2 topics instead of 6]

Output:
Research completed for 2 gap topics (avg confidence: 0.81)
Skipped 4 topics (covered by user context)

Time saved: ~3 minutes
```

---

## Example 4: Dry Run Mode

Preview what would be created without writing files.

```bash
User: /create-agent definition.md --dry-run

# Phases 1-9 execute normally...

# Phase 10: Dry Run Output
Claude: [Does NOT write files]

Output:
# DRY RUN COMPLETE - No files written

## Files That WOULD Be Created

### Agent Definition
Path: .claude/agents/dev-tools/my-agent/my-agent.md
Size: 4,200 tokens
Preview (first 50 lines):
```markdown
---
name: my-agent
description: "..."
tools: Read, Write, Grep, Task
...
```

### Schema
Path: .claude/agents/dev-tools/my-agent/schemas/my-agent.schema.json
Preview:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "allOf": [{"$ref": "base-agent.schema.json"}],
  ...
}
```

### Documentation (3 files)
- docs/domain-knowledge.md (1,200 tokens)
- docs/workflows.md (800 tokens)
- docs/frameworks.md (950 tokens)

## Integrations That WOULD Be Updated
- CLAUDE.md: Add row to delegation table
- orchestrator-workflow.md: Add to agent legend
- agent-categorization.md: Add to Analyzer category

## Quality Summary
- Quality Score: 76/100
- Template Compliance: PASS
- Documentation Health: 82/100

To create these files, run without --dry-run:
/create-agent definition.md
```

---

## Example 5: Skip Validation (High Risk)

Fast prototyping mode - skips Phase 8 quality gates.

```bash
User: /create-agent experimental-agent.md --skip-validation

Output:
WARNING: --skip-validation flag detected
Quality gates will be SKIPPED. Agent may have issues.
Use only for rapid prototyping, NOT production agents.

Proceed? [Y/n]

User: Y

# Phases 1-7 execute...
# Phase 8 SKIPPED

Output:
Phase 8: SKIPPED (--skip-validation flag)

Proceeding directly to Phase 9...

# Phase 9-10 execute...

Output:
# Agent Creation Complete: experimental-agent

WARNING: This agent was created without quality validation.
Before production use:
1. Run /analyze-agent experimental-agent.md
2. Fix any issues identified
3. Re-validate manually
```

---

## Example 6: Quality Gate Failure Recovery

Handling validation failures during Phase 8.

```bash
User: /create-agent complex-agent.md

# Phases 1-7 complete...

# Phase 8: Validation FAILS
Output:
Quality Validation: FAILED (2 of 5 validators)

FAILED: Template Compliance
- Missing section: "Error Recovery"
- Tools field formatted as YAML list (should be string)

FAILED: Quality Matrix (Score: 58/100)
- Error recovery: 2/5
- Validation coverage: 2/5

Options:
1. AUTO-FIX (recommended)
2. Manual fix
3. Skip validation (high risk)

User: 1

Claude: [Delegates fixes to claude-code-ecosystem]

Output:
Auto-fix attempt 1 of 3...
- Added Error Recovery section
- Converted Tools to comma-separated string
- Enhanced validation coverage

Re-validating...

Quality Validation: PASSED
- Template Compliance: 100%
- Quality Matrix: 72/100

Proceeding to Phase 9...
```

---

## Example 7: Duplicate Agent Detection

Handling overlap with existing agents.

```bash
User: /create-agent code-reviewer.md

# Phase 1: Duplicate Check
Output:
Duplicate Detection: CONFLICT FOUND

Proposed: code-reviewer
Existing: code-quality (similarity: 0.89)

Overlap Analysis:
- 5 of 6 capabilities overlap
- Same domain: packages/**
- Similar purpose

Options:
1. RENAME to distinct name
2. MERGE capabilities into existing agent
3. PROCEED anyway (document distinction)
4. CANCEL

User: 1

Claude: Suggest a distinct name:
User: typescript-code-reviewer

Claude: [Updates definition, re-validates]

Output:
Name updated to: typescript-code-reviewer
No duplicates found.
Proceeding to Phase 2...
```

---

## Example 8: Template Variants

Using different output sizes.

```bash
# Minimal (token-optimized)
User: /create-agent definition.md --template=minimal

Output:
Template: minimal
- Agent definition: ~2,000 tokens (vs 4,000 standard)
- Documentation: Essential only (1-2 files)
- Examples: Minimal
- Trade-off: Less comprehensive, faster loading

# Standard (default)
User: /create-agent definition.md --template=standard

Output:
Template: standard
- Agent definition: ~4,000 tokens
- Documentation: Full coverage (3-5 files)
- Examples: Complete delegation patterns

# Comprehensive (maximum detail)
User: /create-agent definition.md --template=comprehensive

Output:
Template: comprehensive
- Agent definition: ~6,000 tokens
- Documentation: Extensive (5-8 files)
- Examples: Multiple scenarios with edge cases
- Trade-off: Higher token usage, slower loading
```
