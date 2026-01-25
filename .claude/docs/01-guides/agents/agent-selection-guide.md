---
title: "Agent Selection Guide"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Selection Guide

## Purpose

**Framework-based reasoning** for selecting the right agent for any task. Seven conceptual frameworks guide understanding of domain, work type, and expertise matching—not keyword matching or algorithmic rules.

**Core Problem**: planning overweighted python-code-implementer using keyword-only matching ("create" → python-code-implementer) without domain context. Result: "create intent-analyzer in `.claude/agents/`" → python-code-implementer (wrong), not agent-architect (correct domain specialist).

**Solution**: Seven frameworks that connect file location → domain → specialist agent.

---

**For researcher-lead Agent**:

Use frameworks below for agent→domain mappings when creating research plans.

**Domain Specialists in Read-Only Mode** (ANY agent can research within their domain):

| Domain                    | Read-Only Specialists                                                 | Use Case                                                      |
| ------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| `.claude/agents/**`       | agent-architect, prompt-evaluator                                     | Agent design analysis, prompt evaluation                      |
| `packages/**`, `tests/**` | debugger, python-code-implementer, python-code-reviewer, test-executor | Failure patterns, implementation patterns, quality assessment |
| `docs/**`                 | spec-reviewer, architecture-reviewer, plan-enhancer, doc-librarian                  | Spec quality, business alignment, architecture validation, doc health |
| `.claude/**`              | workflow, agent-architect, doc-librarian                                  | Workflow patterns, config analysis, doc health                |
| Any domain                | tech-debt-investigator, architecture-reviewer, intent-analyzer                 | Debt detection, dependency analysis, complexity assessment    |

**Selection Principle**: Domain specialist > generic researcher-\* when expertise aligns

**Examples**: "Analyze auth patterns" → debugger (domain expert) | "Analyze agent duplication" → agent-architect (domain expert)

**Reference**: See Framework 1 + Framework 3 for comprehensive domain mappings.

---

## Framework 1: Domain-First Thinking

**Core Principle**: File location reveals domain → Domain determines specialist agent.

### Domain Boundaries

#### Claude Code Ecosystem (`.claude/**`)

**Agent Lifecycle** (`.claude/agents/**`) → **agent-architect**

- Prompt engineering patterns, agent evaluation (9-criteria matrix), simulation-driven development
- Recognition: `.claude/agents/**` path → agent lifecycle work

**Claude Code Configuration** (`.claude/**` excluding agents) → **workflow**

- System architecture, slash commands, hooks, schemas, integration patterns
- Recognition: `.claude/**` path (non-agents) → Claude Code config work

**Example**: "Create intent-analyzer in `.claude/agents/intent-analyzer.md`"

- Keyword: "create" (suggests python-code-implementer) | Domain: `.claude/agents/**` → **agent-architect** (domain wins)

---

#### Main Codebase (`packages/**`, `tests/**`, `scripts/**`)

**Multiple specialists, distinguished by WORK TYPE**:

| Work Type           | Agent                   | Recognition Pattern                                   |
| ------------------- | ----------------------- | ----------------------------------------------------- |
| **Creation**        | python-code-implementer | "implement", "build", "add new", emphasis on newness  |
| **Investigation**   | debugger                | "debug", "why failing", "troubleshoot", unknown cause |
| **Test Generation** | test-creator            | "create tests", "test coverage", "design tests"       |
| **Test Execution**  | test-executor           | "run tests", "execute", "validate test results"       |
| **Test Data**       | test-dataset-creator    | "test data", "fixtures", "validation datasets"        |
| **Quality Review**  | python-code-reviewer    | "review", "validate", "assess quality", "audit"       |
| **Improvement**     | python-code-implementer | "refactor", "restructure", "optimize" (existing code) |

**Key Point**: Domain alone (packages/\*\*) doesn't determine specialist—work type does.

---

#### Documentation Domain (`docs/**`)

| Doc Type                | Agent                                            | Recognition Pattern                              | NEVER Use |
| ----------------------- | ------------------------------------------------ | ------------------------------------------------ | --------- |
| **SPEC.md**             | `/spec` command (create), spec-reviewer (validate)    | New specs vs review                              | python-code-implementer, debugger, python-code-reviewer |
| **PLAN.md** (business)  | plan-enhancer, technical-pm                                         | Business requirements, FR-IDs, user value        | python-code-implementer, debugger, python-code-reviewer |
| **PLAN.md** (technical) | architecture-enhancer, architecture-reviewer                                     | Architecture, NFRs, patterns, tech stack         | python-code-implementer, debugger, python-code-reviewer |
| **Tasks**               | task-creator, roadmap-manager                                         | `/tasks/` directories, converting plans to tasks | python-code-implementer |
| **Review (business)**   | spec-reviewer, plan-enhancer                                         | Business alignment, ROI, strategic fit           | python-code-reviewer |
| **Review (technical)**  | architecture-reviewer                                     | Feasibility, NFRs, production readiness          | python-code-reviewer |
| **Doc Health**          | doc-librarian                                    | Link validation, orphan detection, staleness, health scoring | python-code-implementer |
| **Doc Optimization**    | doc-reference-optimizer                                    | Token reduction, deduplication, consolidation    | python-code-implementer |
| **Doc Organization**    | doc-librarian                                    | Directory structure, naming, tier safety         | python-code-implementer |
| **Doc Standards**       | doc-librarian                                    | Style, tone, formatting consistency              | python-code-implementer |
| **Doc Synthesis**       | doc-librarian                                    | README creation, index generation, diagrams      | python-code-implementer |
| **Doc Maintenance**     | doc-librarian                                    | Scheduled checks, deprecation tracking, version sync | python-code-implementer |
| **Doc Governance**      | doc-librarian                                    | Review workflows, approval gates, access control | python-code-implementer |

**CRITICAL DOMAIN BOUNDARY**: Python agents (python-code-implementer, debugger, python-code-reviewer, test-creator) should NEVER be used for `docs/**` domain. These agents specialize in Python code patterns, not documentation structure, planning methodologies (SDD), or architectural thinking.

**Documentation Agent**: Use `doc-librarian` for documentation lifecycle tasks and `doc-reference-optimizer` for token optimization.

---

### File Type Boundaries (Override Directory Domain)

**Critical Principle**: File type domain expertise > Directory location when conflict exists.

**Universal File Type Routing** (applies regardless of directory):

| File Type | Correct Agent(s) | NEVER Use | Reasoning |
|-----------|------------------|-----------|-----------|
| `**/*.md` | doc-librarian, spec-reviewer, architecture-reviewer | python-code-implementer, debugger, python-code-reviewer | Documentation requires writing expertise, not coding expertise |
| `**/*.py` | python-code-implementer, debugger, python-code-reviewer, test-creator | doc-librarian | Python code requires coding expertise, not documentation expertise |
| `**/*.yaml`, `**/*.yml` | k8s-deployment (k8s/**), workflow (.claude/**), context-dependent | python-code-implementer | Config files require domain context (K8s vs Claude Code ecosystem) |
| `.claude/agents/**/*.md` | agent-architect | python-code-implementer, doc-librarian | Agent definitions require prompt engineering expertise |
| `docs/01-planning/specifications/**/SPEC.md` | `/spec` command (create/update), spec-reviewer (validate) | python-code-implementer, debugger, ANY Python agent | SPEC files require SDD methodology, not Python coding patterns |
| `docs/01-planning/specifications/**/PLAN.md` | plan-enhancer (business), architecture-enhancer (technical) | python-code-implementer, debugger, ANY Python agent | PLAN files require planning expertise, not Python coding patterns |

**Anti-Pattern Examples**:
- ❌ **WRONG**: "Task says 'implement feature.md' → keyword 'implement' → python-code-implementer"
- ✅ **CORRECT**: "File is `feature.md` → file type `.md` → domain: documentation → `/spec` command/spec-reviewer"

- ❌ **WRONG**: "Update SPEC.md with changes → keyword 'update' → python-code-implementer"
- ✅ **CORRECT**: "File is `SPEC.md` → domain: specifications → `/spec` command"

- ❌ **WRONG**: "Implement PLAN.md for feature → keyword 'implement' → python-code-implementer"
- ✅ **CORRECT**: "File is `PLAN.md` → domain: planning → plan-enhancer/architecture-enhancer"

**Decision Hierarchy**:
1. Check file type (.md, .py, .yaml)
2. If file type has universal routing → use file type agent
3. If file type is context-dependent → check directory domain
4. Apply domain-first thinking from Framework 1

**Why This Matters**: python-code-implementer is a Python coding specialist, not a documentation specialist. Even if the task verb is "implement", Markdown files require documentation domain expertise (structure, clarity, formatting) rather than coding expertise (syntax, testing, refactoring).

---

#### Cross-Domain Work

| Agent                          | Domain Scope | Recognition Pattern                                                  |
| ------------------------------ | ------------ | -------------------------------------------------------------------- |
| **researcher-external**              | Any          | Information gathering, pattern discovery ("research", "investigate") |
| **tech-debt-investigator**     | Any          | Debt identification, duplication, hotspots                           |
| **git-github**                 | Any          | Git operations ("commit", "PR", "CI")                                |
| **sast-scanner**               | Any          | Security scanning ("vulnerability", "OWASP")                         |
| **intent-analyzer**            | Any          | Request decomposition, task graphs, dependencies                     |
| **context-readiness-assessor** | Any          | Context quality gating, research coordination                        |
| **contingency-planner**        | Any          | Failure modes, risk scoring, fallback strategies                     |
| **context-optimizer**          | Any          | Token budget optimization, context pruning                           |
| **terminal-bench**             | Terminal-Bench | Task creation, validation, review, submission workflow              |

---

### Terminal-Bench Tasks

For any Terminal-Bench task work, route to the `terminal-bench` domain agent:
- Task creation, brainstorming, ideation
- Task package building (task.yaml, solution, tests, Dockerfile)
- Difficulty validation (11-factor scoring)
- Quality review (12 quality checks)
- Submission workflow

The domain agent uses these skills (gerund-form naming):
- `navigating-terminal-bench-workflow` - 5-phase workflow guidance
- `brainstorming-terminal-bench-tasks` - HARD task ideation
- `implementing-terminal-bench-tasks` - Task package building
- `validating-terminal-bench-difficulty` - Difficulty scoring
- `reviewing-terminal-bench-tasks` - Quality review

**Do NOT use** the deprecated individual agents (designer, builder, evaluator).

---

### Documentation Domain

**Agents**: `doc-librarian`, `doc-reference-optimizer`

**Coordinator for**: All documentation lifecycle tasks

**doc-librarian Skills**:
- Documentation health - Link validation, orphan detection, staleness, health scoring
- Documentation organization - Directory structure, naming, tier safety
- Documentation standards - Style, tone, formatting consistency
- Documentation synthesis - README creation, index generation, diagrams
- Documentation maintenance - Scheduled checks, deprecation tracking, version sync
- Documentation governance - Review workflows, approval gates, access control

**doc-reference-optimizer Skills**:
- Token reduction, deduplication, consolidation

**Route when user says**: "doc health", "fix docs", "optimize docs", "generate README", "lint docs", "track deprecations", "set doc governance", "validate links", "find orphaned docs", "check doc staleness", "reduce doc tokens", "consolidate docs", "organize docs", "standardize docs"

**Use Cases**:
- Health checks: Link validation, orphan detection, staleness tracking → `doc-librarian`
- Optimization: Token reduction, deduplication, reference replacement → `doc-reference-optimizer`
- Organization: Directory restructuring, naming conventions, tier management → `doc-librarian`
- Standards: Style guides, tone consistency, formatting rules → `doc-librarian`
- Synthesis: README generation, index creation, diagram generation → `doc-librarian`
- Maintenance: Scheduled audits, deprecation tracking, version synchronization → `doc-librarian`
- Governance: Review workflows, approval processes, access control → `doc-librarian`

---

### Domain-First Decision Flow

1. **Identify file paths** in task description
2. **Match to domain** (`.claude/agents/**`, `.claude/**`, `packages/**`, `docs/**`)
3. **If single domain + clear specialist** (`.claude/agents/**` → agent-architect) → DONE
4. **If main codebase** → Proceed to Framework 2 (Work Type Recognition)
5. **If cross-domain** → Recognize nature of work (research, debt, git, security)

**Key Insight**: Domain is the strongest signal. Start there, always.

**Detailed Examples**: See `agent-selection-examples.md` for 30+ scenarios with full analysis.

---

## Framework 2: Work Type Recognition

**Core Principle**: Within same domain (especially main codebase), work type determines specialist.

### Primary Work Types

| Work Type         | Characteristics                                | Language Signals                              | Agent (Main Codebase)         |
| ----------------- | ---------------------------------------------- | --------------------------------------------- | ----------------------------- |
| **Creation**      | Building new features, implementing from specs | "create", "implement", "build", "add new"     | python-code-implementer       |
| **Investigation** | Root cause discovery, failure analysis         | "debug", "investigate", "why", "troubleshoot" | debugger                      |
| **Improvement**   | Refactoring, optimization, restructuring       | "refactor", "optimize", "improve structure"   | python-code-implementer       |
| **Analysis**      | Read-only assessment, pattern discovery        | "analyze", "assess", "review", "evaluate"     | Domain specialist (read-only) |

### Work Type Disambiguation

**The "Fix" Ambiguity**:

- "Fix failing tests" (unknown cause) → **debugger** (investigation)
- "Fix failing tests" (known: missing null check) → **python-code-implementer** (implementation)

**Test Work Disambiguation**:

- "Create tests" → **test-creator** (generation)
- "Run tests" → **test-executor** (execution)
- "Fix failing tests" (unknown) → **debugger** (root cause discovery)
- "Fix failing tests" (known impl issue) → **python-code-implementer** (fix code)

### Read-Only Analysis Mode

**Key Distinction**: Implementation mode (Write/Edit) vs Analysis mode (Read/Grep only)

**Language Signals**: "analyze", "investigate", "assess", "review" → Read-only mode

**Selection**:

- Analysis within domain → Domain specialist (read-only)
- Analysis across domains → researcher-\* or tech-debt-investigator

**Examples**: See `agent-selection-examples.md` (Examples 2.4-2.6) for security assessment, agent duplication, plan quality scenarios.

---

## Framework 3: Agent Expertise Mapping

**Core Principle**: Match task to agent whose expertise best fits—not just technical capability.

### The Specialist Principle

**Specialists have developed**:

- Deep patterns specific to their domain
- Templates and structures ensuring quality
- Knowledge of domain pitfalls
- Understanding of best practices

**Anti-Pattern**: "python-code-implementer can edit any Python file" → Use for everything in packages/\*\*

**Why Wrong**: python-code-implementer (creation) ≠ debugger (investigation). Both edit Python, but expertise differs.

### Technical Capability vs Domain Expertise

**Anti-Pattern**: "Anyone can edit Markdown in `.claude/agents/`" → Use python-code-implementer

**Why Wrong**: Technical capability (edit .md) ≠ Domain expertise (agent prompt engineering)

**Better**: Match domain expertise, not file type capability.

### Domain Expertise Examples

| Agent                       | Expertise                                                   | Does NOT Transfer To                         |
| --------------------------- | ----------------------------------------------------------- | -------------------------------------------- |
| **agent-architect**         | Prompt engineering, agent evaluation, simulation-driven dev | Python implementation, specification writing |
| **python-code-implementer** | Python patterns, code organization, testing strategies      | Agent prompt design, spec structure          |
| **`/spec` command**         | Spec structure, requirements clarity, component breakdown   | Code implementation, agent design            |

### Read-Only Research Workers (by Domain)

See table in Purpose section above for complete domain → specialist mapping.

**When to Use Domain Specialist vs researcher-\***:

- **Domain specialist**: Targeted analysis within single domain, deeper expertise
- **researcher-codebase**: Cross-domain pattern discovery, broad investigation
- **researcher-external**: External research (library docs, best practices, trade-off analysis)

**Detailed Examples**: See `agent-selection-examples.md` (Framework 3 section) for expertise matching scenarios.

---

## Framework 4: Multi-Agent Decision Framework

**Core Principle**: Recognize when multiple perspectives or sequential expertise is needed.

### Complexity Signals

**Single-Agent Indicators**:

- Clear scope within one domain
- One expertise type suffices
- Low risk (not security-critical)

**Multi-Agent Indicators**:

- Spans multiple domains ("implement + test + document")
- High criticality (security, payments, auth, data privacy)
- Multiple perspectives valuable (business + technical validation)
- Validation checkpoints needed (implement → review → verify)
- Unfamiliar domain requiring research first

### Common Patterns

#### Sequential Pipeline

**When**: Later steps depend on earlier steps (dependencies)
**Example**: Secure payment feature

1. researcher-external (OWASP patterns, Stripe SDK docs) → 2. python-code-implementer → 3. test-creator → 4. test-executor → 5. python-code-reviewer

#### Parallel Validation

**When**: Multiple independent perspectives on same artifact
**Example**: Implementation plan review

- spec-reviewer, plan-enhancer (business alignment) | architecture-reviewer (technical feasibility) | tech-debt-investigator (debt detection)
- All review in parallel → Orchestrator synthesizes

#### Research-Then-Act

**When**: Context missing, need to discover patterns before acting
**Example**: "Add caching" (unfamiliar with existing patterns)

1. researcher-codebase (discover patterns) → 2. python-code-implementer (implement with context)

### Single Agent Sufficiency

**Use single agent when**:

- Domain clear, matches expertise perfectly
- Well-defined task, no ambiguity
- Low risk (not security-critical)
- No cross-domain work
- Context is sufficient

**Detailed Examples**: See `agent-selection-examples.md` (Framework 4 section) for sequential pipeline, parallel validation, and research-then-act scenarios.

---

## Framework 5: Context-Aware Selection

**Core Principle**: Visible task description may not contain all context needed. Sometimes gathering context IS the first task.

### The "What Don't I Know?" Check

**Before assigning implementation agent, check**:

- How many related files might this touch?
- Are there existing patterns to follow?
- What dependencies exist?
- Is this duplicating existing functionality?
- Do I understand full scope?

**If answers are "I Don't Know"**: Start with researcher-codebase → then implementation agent

### Single-File Assumption Trap

**Anti-Pattern**: One file mentioned → assume simple → direct to implementation

**Reality**: One file might affect 10+ dependents, tests, configs, other modules.

**Decision Framework**:

- **1 file, truly isolated** → Direct to implementation agent
- **1 file + 5-10 related files** → researcher-codebase first
- **2-4 files mentioned** → researcher-codebase for synthesis
- **5+ files mentioned** → researcher-codebase for pattern discovery

**Why**: Implementation without context → breaks functionality, inconsistent patterns, duplicates utilities, misses edge cases.

### Security Context Trigger (AUTOMATIC)

**High-Risk Domains** (require research before implementation):

- Authentication/Authorization
- Payment processing
- External API integration
- Data privacy/PII handling
- Cryptography
- Input validation/sanitization

**Required Pattern**: researcher-external (OWASP) → python-code-implementer → python-code-reviewer (security lens)

**Why Automatic**: Security mistakes are expensive. Research establishes patterns before writing vulnerable code.

### Context Quality Assessment

**High Quality** (proceed directly):

- Detailed requirements
- Patterns specified
- Dependencies listed
- Examples provided
- Clear acceptance criteria

**Low Quality** (gather context first):

- Vague task ("improve auth")
- No patterns specified
- Unknown dependencies
- No examples
- Ambiguous success criteria

**Detailed Examples**: See `agent-selection-examples.md` (Framework 5 section) for single-file trap, security triggers, context quality scenarios.

---

## Framework 6: Disambiguation Principles

**Core Principle**: When multiple agents fit equally well, use these principles to distinguish.

### The Hierarchy

1. **Domain Ownership** (strongest signal) → Domain boundaries deliberately designed
2. **Closest Expertise** → Match work type to specialization
3. **Least Assumptions** → Prefer feedback over changes when ambiguous
4. **Workload Balance** → Tie-breaker only (don't sacrifice expertise)

### Principle 1: Domain Ownership Trumps All

**Example**: "Update agent list in CLAUDE.md"

- Technical capability: Many can edit Markdown
- Domain ownership: CLAUDE.md = Claude Code config
- Domain owner: **workflow**
- **Decision**: workflow (domain ownership wins)

**Why**: Domain owners understand structure, conventions, implications, integration patterns.

### Principle 2: Closest Expertise Match

**Example**: "Fix bug in auth.py where login fails with 500 error"

- Candidates: debugger (investigation) vs python-code-implementer (implementation)
- Root cause known? NO
- Investigation work? YES
- **Decision**: debugger (closest expertise)

**Alternative**: "Fix known bug (missing null check) causing 500 error"

- Root cause known? YES
- Implementation work? YES
- **Decision**: python-code-implementer

### Principle 3: Least Assumptions

**Example**: "Improve code quality in payment.py"

- What "improve" means: comments? restructure? fix bugs? optimize? all?
- python-code-reviewer: Provides feedback (no changes)
- python-code-implementer: Assumes specific improvement + makes changes
- debugger: Assumes bugs exist
- **Decision**: python-code-reviewer (least invasive, clarifies needs)

**Pattern**: Ambiguous request → python-code-reviewer (clarify) → specific agent (implement)

### Principle 4: Workload Balance

**When to Apply**: Only as tie-breaker when expertise is equal.

**Why**: Prevents systematic overuse of one agent, ensures agents stay within expertise zones.

**Detailed Examples**: See `agent-selection-examples.md` (Framework 6 section) for CLAUDE.md update, bug fix disambiguation, quality improvement scenarios.

---

## Framework 7: Anti-Patterns to Avoid

**Core Principle**: Learn from common mistakes to develop better selection intuition.

> **Note**: This framework documents orchestrator delegation anti-patterns. For agent definition quality anti-patterns, see [claude-code-ecosystem anti-patterns](../../../../docs/04-guides/claude-code-ecosystem/anti-patterns.md).

### Eight Anti-Patterns

| Anti-Pattern                             | Mistake                                                          | Better Approach                                   | Self-Check                          |
| ---------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------- | ----------------------------------- |
| **1. Default to Familiar**               | Always choose python-code-implementer (most used)                | Let domain + work type guide selection            | "Right expertise or first thought?" |
| **2. Ignore Domain Boundaries**          | Use python-code-implementer for `.claude/agents/` (can edit .md) | Domain expertise > technical capability           | "File type or domain expertise?"    |
| **3. Single Agent for Cross-Domain**     | Assign python-code-implementer for impl + tests + docs           | Decompose into specialist sequences               | "Spans multiple domains?"           |
| **4. Keyword Matching**                  | "create" → python-code-implementer (ignoring domain/work type)   | Domain first → Work type → Keywords confirm       | "Words or task nature?"             |
| **5. Ignore Security Context**           | Treat auth/payments like any implementation                      | Recognize security → trigger research-then-review | "Security-sensitive?"               |
| **6. Assume Simple (File Count)**        | One file → simple → skip context gathering                       | Assess impact radius, not file count              | "File count or complexity?"         |
| **7. Default When Ambiguous**            | "Don't know → python-code-implementer (versatile)"               | Mark for manual review, force clarification       | "Certain or hiding 'I don't know'?" |
| **8. Orchestrator Direct Execution**     | Execute tasks directly instead of delegating to specialists      | Interpret "please do X" as "delegate to agents"   | "Am I orchestrating or executing?"  |

**Detailed Examples**: See `agent-selection-examples.md` (Framework 7 section) for each anti-pattern with real scenarios, rationale, and self-checks.

---

## Quick Reference Summary

### Decision Flow

1. **Apply Domain-First Thinking** (Framework 1)
   - Check file paths → Identify domain(s) → If single domain + clear specialist → DONE

2. **Recognize Work Type** (Framework 2)
   - If main codebase, what work type? Creation | Investigation | Improvement | Analysis

3. **Check Agent Expertise** (Framework 3)
   - Does expertise align with this work? Domain expertise match?

4. **Consider Multi-Agent** (Framework 4)
   - Complexity/criticality suggest multiple agents? Cross-domain? Security-critical?

5. **Assess Context Needs** (Framework 5)
   - Context sufficient? Gather context first?

6. **Apply Disambiguation** (Framework 6)
   - Still ambiguous? Use principles: Domain ownership > Closest expertise > Least assumptions > Workload balance

7. **Avoid Anti-Patterns** (Framework 7)
   - Not defaulting to familiar? Respecting domain boundaries? Not keyword matching? Considering security?

---

## Integration with Other Frameworks

**This guide complements**:

- **Delegation Confidence Scoring (DCS)** (`docs/01-planning/custom/confidence-based-delegation-framework.md`) - Use this guide for common patterns (80%), DCS for novel/complex scenarios (20%)
- **Orchestrator Workflow** (`.claude/docs/03-workflows/orchestrator-workflow.md`) - Informs agent selection within coordination patterns
- **Research Patterns** (`.claude/docs/00-core/research-patterns.md`) - Research-then-act pattern integration

**When to Use This Guide vs DCS**:

- **This guide**: Common patterns, known domains, standard work types
- **DCS calculation**: Novel scenarios, unclear confidence, complex multi-factor decisions

Both enforce domain boundaries and avoid keyword-only matching.

---

## Detailed Examples Reference

**For 30+ scenario walkthroughs with full analysis**:

- See `.claude/docs/04-examples/agent-selection-examples.md`
- Organized by framework (1-7)
- Each example includes: scenario, framework application, decision rationale, alternatives

**Practice Examples** (from agent-selection-examples.md):

1. "Fix the failing login tests" → debugger (unknown cause) vs python-code-implementer (known cause)
2. "Create payment processing feature" → Multi-agent sequential pipeline (security-critical)
3. "Update CLAUDE.md with new agent list" → workflow (domain ownership)
4. "Analyze patterns in authentication code" → researcher-codebase (pattern discovery)

---

## Conclusion

**Core Takeaway**: Agent selection = understanding domain + work type + expertise alignment (NOT keyword matching or defaults).

**The Seven Frameworks** provide different lenses:

1. Where is the work? (Domain)
2. What kind of work? (Work Type)
3. Who specializes? (Expertise)
4. Multiple agents needed? (Multi-Agent)
5. Enough context? (Context-Aware)
6. How to choose when ambiguous? (Disambiguation)
7. What mistakes to avoid? (Anti-Patterns)

**Application**: 80% of cases clear with these frameworks. Remaining 20% (novel/complex) → use DCS calculation.

**Remember**: Respecting domain boundaries + matching expertise = better work than defaulting to familiar agent.