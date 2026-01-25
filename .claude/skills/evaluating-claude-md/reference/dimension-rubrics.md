# Dimension Scoring Rubrics

Detailed criteria and evidence requirements for each dimension.

---

## D1: Structure (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 1.1 | File size <200 lines | 2 | Binary | Line count from file metadata |
| 1.2 | "Read-only coordinator" explicitly stated | 2 | Binary | Exact quote containing read-only + coordinator concept |
| 1.3 | Project identity clear | 2 | Binary | Name, purpose, stack all present in header |
| 1.4 | Three phases defined | 2 | Binary | OODA or Research/Plan/Implement phases |
| 1.5 | Available agents listed | 2 | Binary | Agent registry or selection guidance section |

### Scoring Rules

**1.1 File Size**:
- <200 lines: 2 pts
- >=200 lines: 0 pts
- Search: Count lines via `wc -l` or file metadata

**1.2 Read-Only Coordinator**:
- Explicit statement: 2 pts
- Search for: "read-only", "coordinator", "orchestrator", "never execute", "delegate"

**1.3 Project Identity**:
- All three (name, purpose, stack): 2 pts
- Missing any: 0 pts

**1.4 Three Phases**:
- Clear phase structure: 2 pts
- Search for: OODA labels, Research/Plan/Implement, numbered phases

**1.5 Agents Listed**:
- Dedicated section with agent names/purposes: 2 pts
- Search for: "Available Agents", "Agent Selection", delegation tables

---

## D2: Context Management (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 2.1 | One-Read Rule stated | 4 | Binary | Explicit rule limiting reads before delegation |
| 2.2 | Token budget strategy | 3 | Binary | Token management approach documented |
| 2.3 | Anti-patterns listed | 3 | Binary | BANNED, DO NOT, or negative constraints |

### Scoring Rules

**2.1 One-Read Rule** (4 pts):
- Search for: "one read", "single read", "one strategic read", file count limits
- High weight: Core orchestrator efficiency principle

**2.2 Token Budget Strategy** (3 pts):
- Search for: "token", "context", "budget", allocation strategy

**2.3 Anti-Patterns** (3 pts):
- Search for: "BANNED", "DO NOT", "NEVER", "Anti-Pattern"

---

## D3: Agent Configuration (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 3.1 | Research specialists listed | 2 | Binary | researcher-* or exploration agents identified |
| 3.2 | Planning specialists listed | 2 | Binary | planning/workflow/architect agents identified |
| 3.3 | Implementation specialists listed | 2 | Binary | development/domain/builder agents identified |
| 3.4 | Selection guidance provided | 2 | Binary | ASC formula, decision matrix, or routing guidance |
| 3.5 | Agents described by capability | 2 | Binary | Agent purposes/domains documented |

### Scoring Rules

**3.1-3.3 Specialist Categories**:
- Research: researcher-*, explorer, platform engineer, domain researcher
- Planning: architect, planner, planning, design reviewer, workflow
- Implementation: implementer, builder, development, code-quality

**3.4 Selection Guidance**:
- ASC scores, decision matrix, domain-to-agent mapping, or routing rules

**3.5 Capability Descriptions**:
- Agents have purpose statements (not just names): 2 pts

---

## D4: Phase Quality (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 4.1 | Research/OBSERVE checklist | 2 | Binary | Phase 1 guidance with items |
| 4.2 | Planning/ORIENT checklist | 2 | Binary | Phase 2 guidance with items |
| 4.3 | Implementation/ACT checklist | 2 | Binary | Phase 3 guidance with items |
| 4.4 | Exit criteria testable | 2 | Binary | CQ thresholds, gates, measurable conditions |
| 4.5 | Handoff artifacts defined | 2 | Binary | Goal/Map/Constraints or equivalent |

### Scoring Rules

**4.1-4.3 Phase Checklists**:
- Structured checklist or bullet list: 2 pts
- Prose without structure: 0 pts
- Search for: checkboxes, numbered steps, "verify:", phase-specific guidance

**4.4 Exit Criteria**:
- Measurable conditions: 2 pts
- Search for: CQ >= X, gates, "when X, proceed to Y", thresholds

**4.5 Handoff Artifacts**:
- Defined delegation format: 2 pts
- Search for: Goal/Map/Constraints, input format, handoff protocol

---

## D5: Quality Standards (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 5.1 | "Code Truth" requirement | 3 | Binary | Code as source of truth emphasized |
| 5.2 | "Code Snippets" requirement | 3 | Binary | Plans must include code examples |
| 5.3 | Human approval gates | 2 | Binary | User confirmation checkpoints |
| 5.4 | Blocker escalation path | 2 | Binary | How to handle blockers defined |

### Scoring Rules

**5.1 Code Truth** (3 pts):
- Search for: "code truth", "read code", "source of truth", "trust code not docs"

**5.2 Code Snippets** (3 pts):
- Search for: "code snippets", "signatures", "interfaces", evidence requirement

**5.3 Human Approval Gates** (2 pts):
- Search for: "approval", "confirm", "review", phase gates requiring human input

**5.4 Blocker Escalation** (2 pts):
- Search for: "escalate", "blocker", "stuck", user notification process

---

## D6: Practical Validation (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 6.1 | Successfully tested | 3 | Contextual | Evidence of practical use |
| 6.2 | Readable in <2 minutes | 2 | Judgment | Concise, scannable, well-structured |
| 6.3 | Agent specs path accessible | 2 | Binary | `.claude/agents/` path referenced |
| 6.4 | Documentation map provided | 2 | Binary | Key docs listed with purposes |
| 6.5 | Rigor adjustment guidance | 1 | Binary | Verbosity/detail level control |

### Scoring Rules

**6.1 Successfully Tested** (3 pts):
- Evidence of practical validation or version history showing iteration
- May be inferred from operational CLAUDE.md

**6.2 Readable** (2 pts):
- Judgment based on: scannable headers, bullet points, progressive disclosure
- Fail if: dense prose blocks, no structure, >300 lines

**6.3 Agent Specs Path** (2 pts):
- `.claude/agents/` must be referenced

**6.4 Documentation Map** (2 pts):
- Search for: "Documentation Index", file paths with descriptions

**6.5 Rigor Adjustment** (1 pt):
- Search for: "Level 1-5", "verbosity", "detail level", rigor settings

---

## D7: Agent Architecture (10 pts)

### Criteria

| # | Criterion | Points | Type | Evidence Required |
|---|-----------|--------|------|-------------------|
| 7.1 | Agent inheritance model | 2 | Binary | How agents inherit from root CLAUDE.md |
| 7.2 | Tool lane enforcement | 2 | Binary | Orchestrator tool restrictions |
| 7.3 | Handoff protocol | 2 | Binary | Goal/Map/Constraints delegation pattern |
| 7.4 | Parallelization rules | 2 | Binary | MAX limits for concurrent agents |
| 7.5 | Context budget & recovery | 2 | Binary | Token management and failure handling |

### Scoring Rules

**7.1 Inheritance Model** (2 pts):
- Search for: "inherit", "project context", "agent-specific prompts extend"

**7.2 Tool Lane Enforcement** (2 pts):
- Search for: "read-only", tool permissions, "allowed-tools", delegation-only

**7.3 Handoff Protocol** (2 pts):
- Context-rich delegation pattern documented

**7.4 Parallelization Rules** (2 pts):
- Search for: "MAX 5", parallel vs sequential rules, batching guidance

**7.5 Context Budget & Recovery** (2 pts):
- Search for: error recovery, restart protocol, context preservation strategy

---

## Summary: All 35 Criteria

| Dimension | Criteria Count | Total Points |
|-----------|----------------|--------------|
| D1: Structure | 5 | 10 |
| D2: Context Management | 3 | 10 |
| D3: Agent Configuration | 5 | 10 |
| D4: Phase Quality | 5 | 10 |
| D5: Quality Standards | 4 | 10 |
| D6: Practical Validation | 5 | 10 |
| D7: Agent Architecture | 5 | 10 |
| **TOTAL** | **32** | **70** |

Note: D5 and D6 have variable-weight criteria (3+3+2+2=10 and 3+2+2+2+1=10).
