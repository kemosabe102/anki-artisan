---
title: "Error Code Reference"
date: 2025-11-30
status: ACTIVE
tags: [analyze-agent, error-handling, claude-docs]
---

# Error Code Reference

Comprehensive error codes for the `/analyze-agent` command with phases, triggers, recovery strategies, and examples.

---

## Error Code Index

| Code | Name | Phase | Retryable |
|------|------|-------|-----------|
| ANALYZE_ERR_001 | Agent Not Found | 0 (VALIDATE) | No |
| ANALYZE_ERR_002 | Dependency Missing | 0 (VALIDATE) | No |
| ANALYZE_ERR_003 | Invalid Mode | 0 (VALIDATE) | No |
| ANALYZE_ERR_004 | Partial Failure | 2 (COLLECT) | Yes (1x) |
| ANALYZE_ERR_005 | Synthesis Failure | 3 (SYNTHESIZE) | Yes (1x) |
| ANALYZE_ERR_006 | Report Validation Failure | 6 (REPORT) | Yes (2x) |

---

## ANALYZE_ERR_001: Agent Not Found

**Phase**: 0 (VALIDATE)
**Severity**: BLOCKING
**Retryable**: No

### Trigger
Target agent path does not exist in the filesystem.

### Message
`Agent not found: {path}`

### Recovery Strategy
1. **Fuzzy match suggestion**: Find similar agent names using Levenshtein distance
2. **List available agents**: Show agents in the target directory
3. **Path correction hints**: Suggest common path mistakes

### Example
```
FAILURE: ANALYZE_ERR_001
Agent not found: researcher-libary

Did you mean: researcher-external?

Available agents in .claude/agents/:
  - researcher-external
  - researcher-codebase
  - researcher-lead

Common fixes:
  - Check spelling
  - Use full path: .claude/agents/research/researcher-external/researcher-external.md
  - List agents: Glob(".claude/agents/**/*.md")
```

---

## ANALYZE_ERR_002: Dependency Missing

**Phase**: 0 (VALIDATE)
**Severity**: BLOCKING
**Retryable**: No

### Trigger
Required dependency not found during pre-flight validation.

### Dependencies Checked
| Dependency | Type | Required By |
|------------|------|-------------|
| claude-code-ecosystem | Agent | Phase 1 analysis |
| claude-code-ecosystem | Agent | Phase 1 analysis |
| documentation | Agent | Phase 1 analysis |
| tech-debt-investigator | Agent | Phase 1 analysis |
| scripts/calculate_tokens.py | Script | claude-code-ecosystem, documentation |
| Knowledge base docs | Files | All agents |

### Message
`Missing dependency: {dependency}`

### Recovery Strategy
1. **List all missing items**: Complete inventory of unavailable dependencies
2. **Suggest installation**: Provide creation/installation commands
3. **Offer fallback**: Use heuristic methods where possible

### Example
```
FAILURE: ANALYZE_ERR_002
Missing dependencies detected:

Agents:
  [OK] claude-code-ecosystem
  [OK] claude-code-ecosystem
  [MISSING] documentation
  [OK] tech-debt-investigator

Scripts:
  [MISSING] scripts/calculate_tokens.py

Recovery options:
  1. Create missing agent: /create-agent documentation
  2. Create token script: See docs/04-guides/scripts/token-counting.md
  3. Continue with fallback: Use --skip-missing flag (partial analysis)
```

---

## ANALYZE_ERR_003: Invalid Mode

**Phase**: 0 (VALIDATE)
**Severity**: BLOCKING
**Retryable**: No

### Trigger
Cannot determine analysis mode from provided arguments.

### Valid Modes
| Mode | Argument Pattern | Example |
|------|------------------|---------|
| by-name | `<agent-name>` | `researcher-external` |
| by-path | `<path/to/agent.md>` | `.claude/agents/debugger.md` |
| CLAUDE.md | `CLAUDE.md` | `CLAUDE.md` |
| --all | `--all` | `--all` |

### Message
`Invalid mode: {argument}`

### Recovery Strategy
1. **Show valid usage**: Display all supported argument patterns
2. **Suggest closest match**: If argument resembles valid mode
3. **Provide examples**: Common usage scenarios

### Example
```
FAILURE: ANALYZE_ERR_003
Invalid mode: --quick

"--quick" is not a supported flag.

Valid usage:
  /analyze-agent researcher-external      # Analyze by name
  /analyze-agent .claude/agents/X.md     # Analyze by path
  /analyze-agent CLAUDE.md               # Analyze orchestrator
  /analyze-agent --all                   # Analyze all agents

Supported flags:
  --all          Analyze entire agent ecosystem
  --skip-missing Continue with available dependencies
  --verbose      Include detailed agent outputs
```

---

## ANALYZE_ERR_004: Partial Failure

**Phase**: 2 (COLLECT)
**Severity**: WARNING
**Retryable**: Yes (1 retry, 30s backoff)

### Trigger
Fewer than 2 agents returned valid results during Phase 1 parallel analysis.

### Threshold
- **PASS**: 4/4 agents return valid results
- **ACCEPTABLE**: 2-3/4 agents return valid results (proceed with partial)
- **FAIL**: 0-1/4 agents return valid results (trigger ERR_004)

### Message
`Partial failure: {returned}/{total} agents`

### Recovery Strategy
1. **Identify failed agents**: List each agent's status and failure reason
2. **Retry once**: After 30s backoff, retry failed agents only
3. **Proceed with partial**: If 2+ agents available after retry
4. **Manual fallback**: Suggest running agents individually

### Example
```
FAILURE: ANALYZE_ERR_004
Partial failure: 1/4 agents returned valid results

Agent Status:
  [TIMEOUT]  claude-code-ecosystem (exceeded 120s limit)
  [ERROR]    claude-code-ecosystem: "calculate_tokens.py not found"
  [SUCCESS]  documentation
  [TIMEOUT]  tech-debt-investigator (exceeded 120s limit)

Attempting retry in 30s for failed agents...

Retry result: 2/3 recovered

Final status: 3/4 agents available (ACCEPTABLE)
Proceeding with partial analysis...

Recovery options if retry fails:
  1. Increase timeout: Set AGENT_TIMEOUT=180
  2. Run individually: Task(claude-code-ecosystem, "...")
  3. Check agent health: /analyze-agent claude-code-ecosystem --self-check
```

---

## ANALYZE_ERR_005: Synthesis Failure

**Phase**: 3 (SYNTHESIZE)
**Severity**: WARNING
**Retryable**: Yes (1 retry, 0s backoff)

### Trigger
Cannot merge findings due to irreconcilable conflicts between agent recommendations.

### Conflict Types
| Type | Description | Resolution |
|------|-------------|------------|
| Contradictory | Agents recommend opposite actions | Present trade-offs |
| Incompatible | Recommendations cannot coexist | Prioritize by domain fit |
| Circular | Dependencies create loops | Break cycle, flag for review |

### Message
`Synthesis failed: {reason}`

### Recovery Strategy
1. **Identify conflicts**: List contradicting recommendations
2. **Present trade-offs**: Show pros/cons of each approach
3. **Skip synthesis**: Present raw findings without merging
4. **Flag for manual review**: Recommend human decision

### Example
```
FAILURE: ANALYZE_ERR_005
Synthesis failed: Irreconcilable conflicts detected

Conflict 1:
  claude-code-ecosystem recommends:
    "Add more usage examples to improve clarity"
    Rationale: Examples reduce ambiguity, improve adoption

  documentation recommends:
    "Remove examples section (redundant with knowledge base)"
    Rationale: Examples duplicate docs/examples/, waste 450 tokens

Trade-off analysis:
  Option A (Add examples): +Clarity, -Token efficiency
  Option B (Remove examples): +Token efficiency, -Standalone clarity

Conflict 2:
  claude-code-ecosystem: "Use CAGEERF methodology"
  tech-debt-investigator: "Simplify to ReACT (lower maintenance)"

Recovery: Presenting raw findings without synthesis.
          Manual review required to resolve conflicts.
          See: .claude/docs/00-core/synthesis-and-recommendation-framework.md
```

---

## ANALYZE_ERR_006: Report Validation Failure

**Phase**: 6 (REPORT)
**Severity**: WARNING
**Retryable**: Yes (2 retries, 0s backoff)

### Trigger
Generated report fails validation against `report.schema.json`.

### Common Schema Errors
| Error | Cause | Fix |
|-------|-------|-----|
| Missing required field | Agent returned incomplete data | Use fallback defaults |
| Invalid type | Type mismatch (e.g., array vs object) | Transform data structure |
| Out of range | Score outside 0-100 bounds | Clamp to valid range |
| Invalid enum | Unknown priority level | Map to closest valid value |

### Message
`Report validation failed: {schema_errors}`

### Recovery Strategy
1. **Show schema errors**: List all validation failures
2. **Attempt auto-fix**: Apply type coercion and defaults
3. **Generate minimal report**: Use only validated fields
4. **Output with warning**: Flag unvalidated sections

### Example
```
FAILURE: ANALYZE_ERR_006
Report validation failed:

Schema errors:
  1. Missing required field: overall_score
     Path: $.summary.overall_score
     Fix: Calculating from dimension averages...

  2. Invalid type at $.findings
     Expected: array
     Received: object
     Fix: Converting object values to array...

  3. Out of range at $.dimensions.prompt_quality
     Value: 105
     Valid range: 0-100
     Fix: Clamping to 100...

Retry 1: Applying auto-fixes...
Retry 1: Validation PASSED

Report generated successfully with 3 auto-corrections applied.
```

---

## Error Handling Strategy

### Retry Logic

| Error Code | Retryable | Max Retries | Backoff | Condition |
|------------|-----------|-------------|---------|-----------|
| ANALYZE_ERR_001 | No | 0 | N/A | Path doesn't exist |
| ANALYZE_ERR_002 | No | 0 | N/A | Dependencies missing |
| ANALYZE_ERR_003 | No | 0 | N/A | Invalid arguments |
| ANALYZE_ERR_004 | Yes | 1 | 30s | <2 agents returned |
| ANALYZE_ERR_005 | Yes | 1 | 0s | Conflicts detected |
| ANALYZE_ERR_006 | Yes | 2 | 0s | Schema validation fails |

### Graceful Degradation

The command implements graceful degradation to maximize useful output:

| Scenario | Degradation Strategy | Output Quality |
|----------|---------------------|----------------|
| ERR_004 with 2-3 agents | Produce partial report | 60-85% |
| ERR_004 with 1 agent | Single-agent report with warning | 30-40% |
| ERR_005 any conflict | Skip synthesis, present raw findings | 80-90% |
| ERR_006 schema errors | Auto-fix + minimal valid report | 70-90% |

### Degradation Decision Tree

```
Agent Results < 2?
  |
  +-- YES --> ERR_004
  |             |
  |             +-- Retry successful? --> Continue with recovered agents
  |             |
  |             +-- Still < 2? --> Produce single-agent report + WARNING
  |
  +-- NO --> Continue to Synthesis
                |
                +-- Conflicts detected?
                      |
                      +-- YES --> ERR_005
                      |             |
                      |             +-- Resolvable? --> Apply resolution
                      |             |
                      |             +-- Irreconcilable? --> Present raw + WARNING
                      |
                      +-- NO --> Generate Report
                                    |
                                    +-- Schema valid?
                                          |
                                          +-- YES --> SUCCESS
                                          |
                                          +-- NO --> ERR_006
                                                       |
                                                       +-- Auto-fix works? --> SUCCESS + NOTE
                                                       |
                                                       +-- Cannot fix? --> Minimal report + WARNING
```

---

## Error Logging

### Log Format

All errors are logged with structured metadata:

```json
{
  "timestamp": "2025-11-30T10:30:45Z",
  "error_code": "ANALYZE_ERR_004",
  "phase": 2,
  "severity": "WARNING",
  "target_agent": "researcher-external",
  "details": {
    "agents_returned": 1,
    "agents_expected": 4,
    "failed_agents": ["claude-code-ecosystem", "claude-code-ecosystem", "tech-debt-investigator"]
  },
  "recovery_attempted": true,
  "recovery_result": "partial_success",
  "final_status": "DEGRADED"
}
```

### Log Location

Errors are written to:
- **Console**: Immediate user feedback
- **Session log**: `.claude/logs/analyze-agent-{timestamp}.log`
- **Metrics**: Aggregated for command health monitoring

---

## Quick Troubleshooting

| Symptom | Likely Error | First Step |
|---------|--------------|------------|
| "Agent not found" | ERR_001 | Check spelling, use `Glob(".claude/agents/**/*.md")` |
| "Missing dependency" | ERR_002 | Run `/analyze-agent --check-deps` |
| "Invalid mode" | ERR_003 | Use one of: name, path, CLAUDE.md, --all |
| "Partial failure" | ERR_004 | Check agent health, increase timeout |
| "Synthesis failed" | ERR_005 | Review conflicts, accept raw findings |
| "Validation failed" | ERR_006 | Usually auto-recovers; check schema if persistent |

---

## Related Documentation

- **Workflow Phases**: `workflow-phases.md` - Phase definitions where errors occur
- **Delegation Patterns**: `delegation-patterns.md` - Agent Task() syntax
- **Report Format**: `report-format.md` - Schema structure for ERR_006
- **Report Schema**: `../schemas/report.schema.json` - Validation schema

---

**Version**: 3.0
**Last Updated**: 2025-11-30
