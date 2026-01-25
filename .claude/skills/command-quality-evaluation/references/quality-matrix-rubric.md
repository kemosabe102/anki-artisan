# Quality Matrix Rubric

Detailed scoring criteria for each criterion in the 11-criterion command quality matrix.

---

## 1. Workflow Correctness (Weight: 0.15)

Steps in correct order, dependencies valid.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Perfect step ordering; all dependencies explicit; no gaps | Complete dependency chain documented |
| 4 | Clear ordering; minor implicit dependencies | >90% dependencies explicit |
| 3 | Mostly correct; some ordering ambiguity | 70-90% clear ordering |
| 2 | Frequent ordering issues; missing steps | 50-70% correct sequence |
| 1 | Steps out of order; broken workflow | <50% correct sequence |

**Assessment Questions**:
- Are all workflow phases/steps numbered or explicitly ordered?
- Does each step's output feed into the next step's input?
- Are there any circular dependencies?

**Good Example**:
```markdown
## Workflow
P0:VALIDATE -> P1:DISCOVER -> P2:COLLECT -> P3:SYNTHESIZE
     |             |              |              |
  fail-fast    parallel       await          merge
```

**Poor Example**:
```markdown
## Steps
- Do analysis
- Validate input (should be first!)
- Generate report
```

---

## 2. Frontmatter Compliance (Weight: 0.12)

Valid YAML, required fields present.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | All required fields; valid YAML; proper formatting | 100% field coverage |
| 4 | All required fields; minor formatting issues | All fields present |
| 3 | Missing 1 optional field; valid syntax | 3/4 required fields |
| 2 | Missing required field; parsing issues | 2/4 required fields |
| 1 | Invalid YAML; multiple missing fields | <2 required fields |

**Required Fields**:
- `argument-hint`: Describes expected arguments
- `description`: <200 chars with trigger keywords
- `allowed-tools`: Comma-separated tool list
- `model`: opus, sonnet, or haiku

**Good Example**:
```yaml
---
argument-hint: '<agent-name | agent-path | --all>'
description: 'Analyze agent quality with 9-phase workflow. Use for audits.'
allowed-tools: Task, Read, Grep, Glob
model: opus
---
```

---

## 3. Subagent Validity (Weight: 0.12)

All Task() targets exist in `.claude/agents/`, have required tools.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | All Task() targets exist; tools verified; prompts clear | 100% agent verification |
| 4 | All agents exist; minor tool mismatches | All agents found |
| 3 | 1 agent missing or misconfigured | 80-99% valid |
| 2 | Multiple agents missing or wrong | 50-80% valid |
| 1 | Most Task() targets invalid | <50% valid |

**Assessment Questions**:
- Does each Task() reference an agent in `.claude/agents/`?
- Does the referenced agent have the tools needed for the delegated task?
- Is the Task() prompt clear and within agent's capabilities?

---

## 4. Gate Coverage (Weight: 0.10)

Critical decision points have gates.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Every phase has exit condition, timeout, failure handling | 100% gate coverage |
| 4 | Most phases gated; minor gaps | >90% coverage |
| 3 | Key phases gated; some missing | 70-90% coverage |
| 2 | Few gates; critical phases ungated | 50-70% coverage |
| 1 | No gates defined | <50% coverage |

**Gate Components**:
- Exit condition: What must be true to proceed
- Timeout: Maximum duration for phase
- Failure handling: What to do if gate fails

**Good Example**:
```markdown
### P2: COLLECT
- **Gate**: >= 3 agents returned valid results
- **Timeout**: 180s total
- **On Failure**: ANALYZE_ERR_004
```

---

## 5. Error Recovery (Weight: 0.10)

Comprehensive error handling, retry policies.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Named error codes; recovery actions; retry policies | Complete error matrix |
| 4 | Error codes defined; most have recovery | >90% errors handled |
| 3 | Basic error handling; some gaps | 70-90% handled |
| 2 | Minimal error handling | 50-70% handled |
| 1 | No error handling defined | <50% handled |

**Assessment Questions**:
- Are error codes defined and documented?
- Does each error have a recovery action?
- Are retry policies specified for transient failures?

**Good Example**:
```markdown
## Error Codes
| Code | Meaning | Recovery |
|------|---------|----------|
| CMD_ERR_001 | Agent not found | List available, suggest match |
| CMD_ERR_002 | Timeout exceeded | Retry with backoff |
```

---

## 6. Parallelization Safety (Weight: 0.10)

Parallel operations are truly independent.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | All parallel ops verified independent; no conflicts | Explicit independence proof |
| 4 | Parallel ops mostly safe; minor shared state | >95% safe |
| 3 | Some parallel ops may conflict | 80-95% safe |
| 2 | Risky parallelization; race conditions possible | 60-80% safe |
| 1 | Parallel ops with clear dependencies | <60% safe |

**Independence Criteria**:
- No shared file writes
- No shared state modification
- No dependency on parallel task output
- No ordering requirements between parallel tasks

**Good Example**:
```markdown
**P1 - Launch ALL in single message (parallel-safe):**
- Agent A: Analyzes structure (READ-ONLY)
- Agent B: Evaluates prompts (READ-ONLY)
- Agent C: Checks efficiency (READ-ONLY)
- Agent D: Assesses debt (READ-ONLY)
```


---

## 7. Skill References (Weight: 0.08)

Referenced skills exist and accessible.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | All Skill() references valid; paths verified | 100% valid references |
| 4 | All skills exist; minor path issues | All skills found |
| 3 | 1 skill missing or path incorrect | 80-99% valid |
| 2 | Multiple skill references invalid | 50-80% valid |
| 1 | Most skill references broken | <50% valid |

**Assessment Questions**:
- Does each Skill() reference point to `.claude/skills/*/SKILL.md`?
- Are referenced skills appropriate for the command's purpose?
- Do skills have required capabilities?

---

## 8. Tool Permissions (Weight: 0.08)

Tools properly scoped (Bash with patterns).

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Minimal tool set; Bash patterns defined; no over-permission | Justified tool list |
| 4 | Tools justified; minor redundancy | Mostly minimal |
| 3 | Some unnecessary tools; Bash unscoped | Acceptable scope |
| 2 | Tool sprawl; broad permissions | Over-permissioned |
| 1 | Excessive tools; security risk | Major scope issues |

**Assessment Questions**:
- Is each tool in `allowed-tools` actually used?
- Are Bash commands scoped with patterns?
- Are dangerous operations (Write, Edit) justified?

---

## 9. Documentation (Weight: 0.08)

Anti-patterns, good patterns, examples.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Anti-patterns, good patterns, examples, references | Complete documentation |
| 4 | Most documentation present; minor gaps | >90% documented |
| 3 | Basic documentation; missing sections | 70-90% documented |
| 2 | Minimal documentation | 50-70% documented |
| 1 | No documentation beyond basic usage | <50% documented |

**Required Documentation Sections**:
- Anti-patterns (NEVER DO)
- Good patterns (ALWAYS DO)
- Examples (usage scenarios)
- References (linked docs)

---

## 10. Orchestrator Integration (Weight: 0.05)

Trigger keywords, integration points.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Clear triggers; integration points; discovery hints | Full integration |
| 4 | Good triggers; minor integration gaps | Strong integration |
| 3 | Basic triggers; limited discoverability | Adequate integration |
| 2 | Weak triggers; hard to discover | Poor integration |
| 1 | No integration support | No integration |

**Integration Components**:
- Trigger keywords in description
- Clear invocation pattern
- Output format compatible with orchestrator
- Next-step suggestions

---

## 11. State Management (Weight: 0.02)

Checkpoint/resume support if multi-phase.

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| 5 | Checkpoint/resume; state persistence; recovery | Full state management |
| 4 | Checkpoints defined; resume possible | Good state handling |
| 3 | Basic state tracking; manual resume | Adequate handling |
| 2 | Minimal state; restart required on failure | Poor handling |
| 1 | No state management; stateless only | No handling |

**Note**: Score 3+ only required for multi-phase commands (>3 phases). Single-phase commands may score N/A (treat as 3).

---

## Scoring Worksheet Template

```markdown
## Command Quality Evaluation: [Command Name]

### Criterion Scores

| Criterion | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Workflow Correctness | 0.15 | _/5 | _ |
| Frontmatter Compliance | 0.12 | _/5 | _ |
| Subagent Validity | 0.12 | _/5 | _ |
| Gate Coverage | 0.10 | _/5 | _ |
| Error Recovery | 0.10 | _/5 | _ |
| Parallelization Safety | 0.10 | _/5 | _ |
| Skill References | 0.08 | _/5 | _ |
| Tool Permissions | 0.08 | _/5 | _ |
| Documentation | 0.08 | _/5 | _ |
| Orchestrator Integration | 0.05 | _/5 | _ |
| State Management | 0.02 | _/5 | _ |
| **TOTAL** | 1.00 | | **_** |


### Grade: [ ] (A/B/C/D/F)

### Evidence Summary
- Workflow Correctness: [evidence]
- Frontmatter Compliance: [evidence]
- Subagent Validity: [evidence]
- Gate Coverage: [evidence]
- Error Recovery: [evidence]
- Parallelization Safety: [evidence]
- Skill References: [evidence]
- Tool Permissions: [evidence]
- Documentation: [evidence]
- Orchestrator Integration: [evidence]
- State Management: [evidence]

### Priority Improvements
1. [Lowest scoring criterion]: [recommendation]
2. [Second lowest]: [recommendation]
3. [Third lowest]: [recommendation]
```

---

## Quick Reference Card

**Weights** (memorize): 15-12-12-10-10-10-08-08-08-05-02

**Grade Thresholds**: A(4.5), B(3.5), C(2.5), D(1.5), F(<1.5)

**Critical Failures**:
- Workflow Correctness < 3: Steps broken
- Subagent Validity < 2: Invalid agents
- Error Recovery < 2: No error handling
