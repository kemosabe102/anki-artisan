---
title: "Session Phase Model & Agent Guide"
date: 2025-11-26
status: ACTIVE
tags: [orchestrator, phases, agents, claude-docs]
---

# Session Phase Model & Agent Guide

**Purpose**: Detailed explanation of the 4-phase session model and agent recommendations per phase.

**Quick Reference**: See `pre-response-checklist.md` for compact checklist version.

---

## Session Phase Overview

Sessions progress through phases based on user intent and task clarity:

```
ANALYSIS --> DECISION --> IMPLEMENT --> VALIDATE
(Explore)    (Plan)       (Execute)    (Verify)
```

Each phase has:
- **Primary OODA Loop**: Which phases cycle
- **User Behaviors**: Signals indicating this phase
- **Orchestrator Role**: What to focus on
- **Recommended Agents**: Specialists for this phase
- **Exit Criteria**: When to transition

**Key Insight**: Phases are NOT rigid stages. Users may jump phases, revisit earlier phases, or operate in multiple phases simultaneously. The orchestrator adapts fluidly.

---

## Phase 1: ANALYSIS (Explore)

### Primary Loop: OBSERVE <-> ORIENT

The orchestrator gathers information and builds understanding. Cycle between observing user needs and orienting on context until clarity emerges.

**OODA Emphasis**: OBSERVE (60%) + ORIENT (40%)

### User Behaviors

- Asking questions: "What does X do?", "How does Y work?"
- Exploring options: "Can we do Z?", "I'm thinking about..."
- Seeking understanding: "Help me understand...", "Explain..."
- Comparing alternatives: "What's the difference between..."
- Expressing uncertainty: "I'm not sure if...", "Would it be possible to..."

### Orchestrator Role

- Gather context through research delegation
- Ask clarifying questions (prefer structured options over open-ended)
- Research unknowns proactively before proposing solutions
- Build shared understanding with user
- **Avoid premature solutioning** - understand before recommending

### Recommended Agents

| Agent | When to Use | Rationale |
|-------|-------------|-----------|
| **researcher-codebase** | User asks about existing code, patterns, or implementations | Fast local pattern discovery; understands project conventions |
| **researcher-external** | API/framework questions, best practices, industry standards | Authoritative docs (Context7) + community patterns (Perplexity) |
| **context-readiness-assessor** | Evaluating if ready to proceed; multi-component scope | CQ scoring; gap identification; research coordination |
| **intent-analyzer** | Complex multi-part request; ambiguous scope | Decompose into task graph; identify dependencies |
| **feature-analyzer** | Comparing 2+ feature approaches | Overlap analysis; helps decide direction |

### Why These Agents?

**Research-First Philosophy**: ANALYSIS phase prioritizes understanding over action. Research agents (researcher-*) excel at information gathering without side effects. They return findings, not changes.

**Context Quality Focus**: context-readiness-assessor helps quantify "Do we know enough?" - critical for deciding when to exit ANALYSIS.

**Decomposition Tools**: intent-analyzer breaks complex requests into understandable components, reducing cognitive load before planning.

### Exit Criteria

- User signals readiness: "Let's do X", "I want to...", "Go ahead with..."
- Context_Quality >= 0.85 on proposed approach
- Requirements are concrete and understood
- No major unknowns remaining (or unknowns are bounded)
- User approves direction (explicit or implicit)

---

## Phase 2: DECISION (Plan)

### Primary Loop: ORIENT <-> DECIDE

The orchestrator refines understanding and makes delegation decisions. Cycle between orienting on approach and deciding on execution strategy.

**OODA Emphasis**: ORIENT (40%) + DECIDE (60%)

### User Behaviors

- Choosing direction: "Let's go with option A", "Use the second approach"
- Requesting plans: "How should we approach this?", "What's the plan?"
- Seeking breakdown: "Break this down for me", "What are the steps?"
- Reviewing/approving: "That looks good", "Make these changes..."
- Setting constraints: "Keep it simple", "Focus on X first"

### Orchestrator Role

- Propose concrete approach with rationale
- Create task breakdown (TodoWrite for tracking)
- Assign agents to tasks based on domain expertise
- Identify dependencies and execution order
- Get user approval before execution begins
- **Present trade-offs explicitly** when multiple valid approaches exist

### Recommended Agents

| Agent | When to Use | Rationale |
|-------|-------------|-----------|
| **`/spec` command** | Need to formalize requirements | Creates structured SPEC.md; lean ICE scoring |
| **planning** | Adding business context to plans | FR-ID mapping; success metrics; user value focus |
| **architecture** | Technical architecture decisions | Component design; tech stack choices; NFRs |
| **planning** | Ready to break into executable tasks | Generates TASKS.json; estimates complexity |
| **feature-analyzer** | Comparing 2+ feature approaches | Overlap analysis; merge opportunities |
| **planning** | Planning across releases | Sprint capacity; release sequencing |
| **contingency-planner** | High-risk implementations | Failure modes; rollback strategies |
| **planning** | Business alignment validation | ROI assessment; stakeholder concerns |

### Why These Agents?

**Planning Specialists**: DECISION phase requires structured thinking. /spec command, planning, and architecture produce formal artifacts that capture decisions.

**Task Decomposition**: planning converts plans into actionable units. Each task becomes a delegation target for IMPLEMENT phase.

**Risk Awareness**: contingency-planner ensures we consider "what if it fails?" before committing to execution.

### Exit Criteria

- User approves plan/approach (explicit confirmation)
- Tasks are defined and sequenced
- Agent assignments are clear (which agent handles what)
- Dependencies mapped (what must complete before what)
- Risk mitigations identified for high-impact tasks
- Ready to execute

---

## Phase 3: IMPLEMENT (Execute)

### Primary Loop: DECIDE <-> ACT

The orchestrator delegates execution and handles results. Cycle between deciding next action and executing through agents.

**OODA Emphasis**: DECIDE (30%) + ACT (70%)

### User Behaviors

- Authorizing execution: "Go ahead", "Implement it", "Do it"
- Directing changes: "Make the changes", "Update the file"
- Providing feedback: "That's not quite right...", "Also change..."
- Monitoring progress: "How's it going?", "What's the status?"
- Iterating: "Try again with...", "Adjust the approach"

### Orchestrator Role

- Delegate to execution agents (domain-first selection)
- Track progress with TodoWrite (mandatory for multi-step)
- Handle failures with retry or alternative agent selection
- Synthesize multi-agent outputs when parallel execution
- Report progress to user at meaningful intervals
- **Never execute directly** - always delegate to domain specialists

### Recommended Agents

| Agent | When to Use | Rationale |
|-------|-------------|-----------|
| **development** | Writing/modifying Python code | Primary implementation; patterns + testing |
| **code-quality** | Need tests for new code | AAA pattern; coverage focus |
| **test-dataset-creator** | Need test fixtures/data | Validation datasets; edge cases |
| **debugger** | Fixing bugs, investigating failures | Hypothesis-driven debugging |
| **claude-code-ecosystem** | Modifying agent definitions | `.claude/agents/**` domain specialist |
| **workflow** | Modifying .claude/ infrastructure | Commands, hooks, skills, schemas |
| **documentation** | Documentation updates | `docs/**` domain; link health |
| **source-control** | Git operations, PRs, CI | Commit workflow; PR creation |
| **deployment-release** | Kubernetes manifests | Infrastructure domain |

### Why These Agents?

**Domain Specialists**: IMPLEMENT phase requires hands-on expertise. Each agent owns a domain (packages/**, docs/**, .claude/**) and applies domain-specific patterns.

**Separation of Concerns**: development writes code; code-quality writes tests; documentation writes docs. Each focuses on their strength.

**Version Control Integration**: source-control handles the mechanics of committing and PR creation, ensuring consistent commit message format and proper workflow.

### Batch Delegation Principle

When task requires >5 file changes:
- **1-5 files**: Single agent
- **6-10 files**: 2 agents (parallel batches)
- **11-20 files**: 4 agents
- **21+ files**: 5+ agents (max 5 files each)

**Why**: Prevents bottlenecks, enables parallelization, improves failure isolation.

### Exit Criteria

- All tasks completed (TodoWrite shows done)
- No blocking errors
- User accepts output (explicit or implicit)
- Ready for validation

---

## Phase 4: VALIDATE (Verify)

### Primary Loop: ACT <-> OBSERVE

The orchestrator verifies results and gathers feedback. Cycle between running validation and observing results.

**OODA Emphasis**: ACT (40%) + OBSERVE (60%)

### User Behaviors

- Requesting verification: "Does it work?", "Run the tests", "Check it"
- Reviewing output: "Show me the changes", "What did you modify?"
- Accepting: "Looks good", "Ship it", "Merge it"
- Rejecting: "That's wrong", "Try again", "Revert that"
- Requesting refinement: "Almost, but change X", "Good, now also..."

### Orchestrator Role

- Run automated validations (tests, linting, type checks)
- Delegate quality reviews to appropriate specialists
- Identify remaining gaps or issues
- Loop back to earlier phases if issues found
- Prepare for completion (commit, PR, merge)
- **Present validation results clearly** with pass/fail status

### Recommended Agents

| Agent | When to Use | Rationale |
|-------|-------------|-----------|
| **code-quality** | Code quality check | Confidence-driven review; pattern compliance |
| **code-quality** | Run test suites | Execute and categorize failures |
| **sast-scanner** | Security validation | SAST before commit; vulnerability detection |
| **tech-debt-investigator** | Assess debt impact | SQALE/SIG analysis; quantified metrics |
| **planning** | Validate against requirements | WHAT/WHY boundary check; FR compliance |
| **architecture** | Technical architecture validation | Production readiness; NFR compliance |
| **documentation** | Documentation quality | Token efficiency; broken links |

### Why These Agents?

**Review Specialists**: VALIDATE phase requires critical assessment. Reviewers (code-quality, planning, architecture) provide independent validation.

**Automated Verification**: code-quality and sast-scanner run automated checks that catch issues humans might miss.

**Quality Metrics**: tech-debt-investigator and documentation provide quantified assessments (debt score, token savings) for objective decision-making.

### Exit Criteria

- All automated checks pass (tests, linting, SAST)
- Review agents report acceptable quality
- User satisfied with results
- Ready for commit/merge
- **OR**: Issues identified -> return to appropriate phase

---

## Phase Transitions

### Forward Transitions

| Transition | Trigger | Action |
|------------|---------|--------|
| ANALYSIS -> DECISION | User signals intent; CQ >= 0.85 | Propose approach; begin planning |
| DECISION -> IMPLEMENT | User approves plan | Begin execution; track with TodoWrite |
| IMPLEMENT -> VALIDATE | Tasks complete | Run reviews; execute tests |
| VALIDATE -> Complete | All checks pass; user satisfied | Offer commit; create PR |

### Backward Transitions

| Transition | Trigger | Action |
|------------|---------|--------|
| Any -> ANALYSIS | New questions; "Wait..."; scope change | Return to exploration; gather context |
| IMPLEMENT -> DECISION | Plan inadequate; blocking issues | Revise approach; re-plan |
| VALIDATE -> IMPLEMENT | Fixes needed; review failures | Execute fixes; iterate |
| VALIDATE -> DECISION | Fundamental issues; wrong approach | Re-plan with new understanding |

### Transition Signals

**Forward signals** (progressing):
- "Let's do it", "Go ahead", "Looks good"
- Explicit approval of plans or outputs
- No remaining questions or concerns

**Backward signals** (regressing):
- "Wait", "Actually...", "I'm not sure anymore"
- New requirements or scope changes
- Validation failures or quality issues
- User dissatisfaction with direction

### Transition Behavior

The orchestrator transitions **silently** - adapting behavior without announcing "Now entering DECISION phase." Users experience smooth progression, not mechanical state changes.

**Signs of good transitions**:
- User feels guided, not lectured
- Appropriate agents used automatically
- Progress feels natural
- Questions surface at right moments
- No jarring context switches

---

## Anti-Patterns

### 1. Premature Implementation

**Symptom**: Starting to code before plan approval; jumping to development immediately.

**Why It Fails**: Missing requirements discovered mid-implementation; rework required; user expectations misaligned.

**Fix**: Ensure DECISION phase exit criteria met. User approval before execution agents.

**Detection**: Ask "Has the user approved this approach?" If uncertain, you're still in ANALYSIS or DECISION.

---

### 2. Skipped Validation

**Symptom**: Completing IMPLEMENT without VALIDATE; no review, no tests, straight to commit.

**Why It Fails**: Bugs ship; quality degrades; technical debt accumulates silently.

**Fix**: Always run at least one validation agent (code-quality, code-quality, or sast-scanner).

**Detection**: Ask "What validated this change?" If no answer, VALIDATE phase was skipped.

---

### 3. Stuck in Analysis

**Symptom**: Endless OBSERVE <-> ORIENT loop; researching forever; never deciding.

**Why It Fails**: Analysis paralysis; user frustration; no value delivered.

**Fix**: Check CQ threshold. If CQ >= 0.85, prompt for decision. Set iteration limits (max 3 research rounds).

**Detection**: Count research delegations. If >5 without concrete proposal, you're stuck.

---

### 4. Phase Mismatch

**Symptom**: Using IMPLEMENT agents during ANALYSIS; using VALIDATE agents during DECISION.

**Why It Fails**: Wrong tools for the job; inefficient; confusing outputs.

**Fix**: Match agent selection to current phase. Reference phase tables above.

**Detection**: Ask "Is this agent appropriate for what the user is asking right now?"

---

### 5. Rigid Phase Enforcement

**Symptom**: Refusing to help because "we're in ANALYSIS phase"; forcing linear progression.

**Why It Fails**: Users don't think in phases; feels bureaucratic; slows progress.

**Fix**: Phases are guidance, not gates. Adapt fluidly to user needs. Allow phase jumps.

**Detection**: If you're explaining phases to the user, you're being too rigid.

---

### 6. Missing Backward Transitions

**Symptom**: Pressing forward despite user signals to revisit; ignoring "Wait, actually..."

**Why It Fails**: User loses control; changes made against their intent; trust erodes.

**Fix**: Actively listen for backward transition signals. Acknowledge scope changes immediately.

**Detection**: User repeating concerns or questions is a backward signal being ignored.

---

## Integration with OODA Framework

The session phases map to OODA emphasis:

| Phase | Primary OODA | Secondary OODA | Emphasis |
|-------|--------------|----------------|----------|
| ANALYSIS | OBSERVE | ORIENT | Gathering (60/40) |
| DECISION | ORIENT | DECIDE | Planning (40/60) |
| IMPLEMENT | DECIDE | ACT | Executing (30/70) |
| VALIDATE | ACT | OBSERVE | Verifying (40/60) |

### How They Interact

**OODA is per-task**: Each delegation goes through OBSERVE -> ORIENT -> DECIDE -> ACT.

**Phases are per-session**: The session progresses through ANALYSIS -> DECISION -> IMPLEMENT -> VALIDATE.

**Nesting**: Within IMPLEMENT phase, each task delegation still applies OODA. The phase determines which OODA stages are emphasized.

### Example: IMPLEMENT Phase with OODA

```
Session Phase: IMPLEMENT

Task: "Add validation to user input"

OODA for this task:
- OBSERVE: Task is Python implementation in packages/core/
- ORIENT: CQ = 0.92 (existing patterns, clear requirements)
- DECIDE: development (domain match, creation work type)
- ACT: Delegate, track with TodoWrite, verify output

The IMPLEMENT phase context means:
- Less research needed (ANALYSIS already done)
- Plan already approved (DECISION already done)
- Focus on execution quality
```

---

## Agent Selection by Phase (Quick Reference)

### ANALYSIS Phase Agents
```
researcher-codebase    # Local patterns
researcher-external    # External knowledge (library docs + best practices)
context-readiness-assessor  # CQ scoring
intent-analyzer        # Request decomposition
feature-analyzer       # Approach comparison
```

### DECISION Phase Agents
```
/spec command           # Requirements formalization
planning          # Business context
architecture  # Technical design
planning           # Task breakdown
planning        # Release planning
contingency-planner    # Risk mitigation
planning           # Business alignment
```

### IMPLEMENT Phase Agents
```
development  # Python code
code-quality            # Test generation
test-dataset-creator    # Test data
debugger                # Bug investigation
claude-code-ecosystem         # Agent definitions
workflow                # .claude/ infrastructure
documentation           # Documentation
source-control              # Version control
deployment-release          # Kubernetes
```

### VALIDATE Phase Agents
```
code-quality    # Code quality
code-quality           # Test execution
sast-scanner            # Security scanning
tech-debt-investigator  # Debt analysis
planning           # Requirements validation
architecture     # Architecture validation
documentation # Doc quality
```

---

## Related Documentation

- **OODA Framework**: `ooda-loop-framework.md` - Complete OODA methodology
- **Agent Selection**: `agent-selection-guide.md` - 7 frameworks for agent selection
- **Delegation Patterns**: `delegation-patterns.md` - Best practices for delegation
- **Signal-Response Library**: `orchestrator-signal-response-library.md` - Adaptive communication
- **Orchestrator Workflow**: `orchestrator-workflow.md` - Complete coordination patterns

---

**Session phases provide context for agent selection. OODA provides the decision framework. Together, they enable fluid, user-responsive orchestration.**
