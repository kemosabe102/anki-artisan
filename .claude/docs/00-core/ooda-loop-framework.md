---
title: OODA Loop Framework
description: Complete OODA loop framework for orchestrator request assessment with formulas, thresholds, and examples
category: core-agent-framework
auto_load: false
related:
  - orchestrator-workflow.md
  - agent-selection-guide.md
  - research-patterns.md
---

# OODA Loop Framework

**Purpose**: Provide comprehensive OODA loop guidance for orchestrator request assessment

**Apply to ALL user requests before taking action.**

## 1. OBSERVE - What is being asked?

- [ ] Read the full request carefully
- [ ] Identify task type: research, implementation, analysis, git operation, or combination?
- [ ] Note key verbs: "understand", "review", "implement", "explain", "commit", "fix"
- [ ] Count entities: How many files/components/tasks involved?
- [ ] Extract constraints: time, scope, quality expectations

## 2. ORIENT - What context do I need? (MOST CRITICAL PHASE)

⚠️ **PROTECTED SECTION** - This phase is critical for orchestrator success. Preserve all decision logic and context quality frameworks.

### Context Assessment Priority

1. **Check Auto-Loaded Docs FIRST** (already in context, no Read needed):
   - agent-selection-guide.md (domain-first thinking, work type recognition)
   - file-operation-protocol.md (file editing rules)
   - orchestrator-workflow.md (delegation patterns, researcher-lead coordination)

2. **Assess Context Quality** (self-assessment):
   - [ ] **Domain Familiarity**: Do I understand this technology domain? (0.0-1.0)
   - [ ] **Pattern Clarity**: Are there existing patterns to follow? (0.0-1.0)
   - [ ] **Dependency Understanding**: Are integration points clear? (0.0-1.0)
   - [ ] **Risk Awareness**: Have failure modes been considered? (0.0-1.0)

   **Formula**: Context_Quality = (Domain × 0.40) + (Pattern × 0.30) + (Dependency × 0.20) + (Risk × 0.10)

3. **Classify Task Complexity** (for Context Metadata):
   - **single-file**: Changes confined to 1 file in known domain
   - **multi-component**: 2-3 related files in same directory/module
   - **cross-domain**: 3+ files across multiple directories (packages/, tests/, docs/)
   - **architectural**: System-wide changes affecting core abstractions or >5 files

4. **Simple Context Gathering** (proceed to DECIDE phase):
   - Single-file changes in familiar domain
   - Pattern matching existing implementations (check auto-loaded guides)
   - Well-defined tasks with clear examples
   - **Action**: Sufficient context available → Proceed to DECIDE phase for agent selection

5. **Complex Context Gathering** (delegate to researcher-lead):
   - Context_Quality < 0.5 (insufficient understanding)
   - Multi-component features spanning 3+ files
   - New architectural patterns being introduced
   - External integrations or API design
   - Security-critical implementations
   - Cross-domain changes (multiple directories)
   - **Action**: Delegate to researcher-lead for strategic research coordination

### Hermeneutic Circle in Context Gathering

**When to Apply**: Complex context gathering (Context_Quality <0.5), multi-component features (3+ files), architectural changes, new patterns without examples. **Skip for**: Simple single-file changes, pattern-matching tasks, well-understood domains.

**Principle**: Understanding is iterative, not linear. Each research finding reshapes what questions to ask next.

**Three Fore-Structures** (Heidegger):

1. **Fore-having**: The total situation/context you're already operating within
   - Current domain knowledge, mental models, constraints
   - Example: "I'm in a Python codebase using Pydantic for data validation"

2. **Fore-sight**: The specific aspect or angle you're examining
   - Which particular problem/component is the focus?
   - Example: "I'm focusing on error handling patterns in the auth module"

3. **Fore-conception**: Your preliminary understanding or hypothesis
   - Initial interpretation before deep investigation
   - Example: "I hypothesize this is a validation error propagation issue"

**Iterative Refinement Process**:

1. **Initial scan** → Form provisional understanding (fore-conception)
2. **Examine details** → How do specifics challenge your whole-view?
3. **Revise whole** → Update context model based on contradictions
4. **Re-examine details** → With new whole-view, what details now matter?
5. **Stabilize** → Continue until understanding converges (confidence ≥ 0.85)

**Practical Questions**:

- "Does this detail fit my context model, or does the model need updating?"
- "What assumptions am I bringing that these findings contradict?"
- "Have I iterated enough, or am I forcing closure?"

**Anti-Patterns to Avoid**:

- ❌ One-shot assessment: "I read the code once, I understand it"
- ❌ Premature closure: Rushing to DECIDE without sufficient Orient iteration
- ❌ Detail accumulation without synthesis: Gathering facts without updating whole-view
- ✅ Hermeneutic iteration: Each finding reshapes understanding, which guides next inquiry

### Context Metadata Handoff

**When delegating to researcher-lead**:

- ALWAYS include calculated Context_Quality scores in delegation prompt

- **Format**:

  ```
  Context Metadata:
  - Overall Context_Quality: X.XX
  - Breakdown:
    * Domain_Familiarity: X.X (HIGH/MODERATE/LOW)
    * Pattern_Clarity: X.X
    * Dependency_Understanding: X.X
    * Risk_Awareness: X.X
  - Complexity: [single-file|multi-component|cross-domain|architectural]
  - Known Gaps: [list specific unknowns]
  ```

- researcher-lead uses metadata to scope research depth and worker allocation

- **Known Gaps**: Specific technical questions identified during self-assessment
  - researcher-lead uses gaps to design targeted worker objectives
  - Gaps inform task_boundaries (what to investigate vs what to skip)

### researcher-lead Workflow

**When delegating**:

1. Task(agent="researcher-lead", prompt="CREATE A RESEARCH PLAN for [objective]")
2. researcher-lead returns delegation_plans → Orchestrator spawns workers in parallel
3. Check confidence scores → If gaps exist, call researcher-lead again (max 3 iterations)
4. Synthesize findings → Proceed to DECIDE

**Iteration Protocol**: 0.85 confidence threshold, max 3 rounds. See orchestrator-workflow.md (lines 692-770) for complete gap detection and follow-up planning logic.

### Research Depth Scoping

**Context_Quality determines worker allocation**:

- **High Context_Quality (≥0.8)**: Light verification research (1 worker, 5-10 min)
- **Moderate (0.5-0.79)**: Standard research depth (2-3 workers, 10-15 min)
- **Low (<0.5)**: Deep investigative research (3-5 workers, 15-20 min)

**Complexity modifiers**:

- Single-file: 1 worker
- Multi-component (3+ files): 2-3 workers
- Cross-domain: 3-5 workers
- Architectural (system-wide): 4-5 workers + architecture

### Dimension-Specific Research Triggers

**Scores <0.7 trigger specialized research**:

- **Domain_Familiarity <0.7**: Deploy researcher-external (official docs, community patterns)
- **Pattern_Clarity <0.7**: Deploy researcher-codebase (local patterns) + researcher-external (industry standards)
- **Dependency_Understanding <0.7**: Deploy architecture (integration validation) + researcher-codebase (dependency mapping)
- **Risk_Awareness <0.7**: Deploy researcher-external (OWASP/security best practices) + code-reviewer (vulnerability analysis)

### Gate Status

- **READY** (Context_Quality ≥ 0.5): Proceed to DECIDE phase
- **GATHERING** (<0.5, <3 iterations): Continue ORIENT with research
- **BLOCKED** (<0.5, 3 iterations exhausted): Escalate to user

**Key Principle**: ORIENT quality determines DECIDE and ACT quality. Invest time here to prevent expensive rework later.

## 3. DECIDE - What's my approach?

**Use Agent Selection Framework for ALL tasks**:

1. Match domain (from ORIENT) to agent via Directory Scope Decision Matrix
2. Apply Agent Selection Framework for work type + disambiguation
3. Assess Agent Selection Confidence: High/Medium (≥0.5) → delegate | Low (<0.5) → report to user

**See**: CLAUDE.md sections on Agent Selection & Delegation and Agent Selection Confidence for details.

## 4. ACT - Execute the plan

- [ ] Use appropriate tools/agents based on decision
- [ ] Track progress with TodoWrite for multi-step tasks
- [ ] Verify outputs before reporting to user
- [ ] Communicate clearly and concisely

---

## Examples

### Example 1 - "Research async validation patterns in Pydantic v2"

**OBSERVE**:

- Verbs: "research", "patterns" → Multi-source research needed
- Entities: Library docs, best practices, code examples

**ORIENT**: Check auto-loaded docs → Context_Quality assessment:

- Domain Familiarity: 0.6 (familiar with Pydantic, less so with v2 async)
- Pattern Clarity: 0.3 (unclear async patterns)
- Dependency Understanding: 0.7 (integration points clear)
- Risk Awareness: 0.8 (validation risks understood)
- **Context_Quality = (0.6 × 0.40) + (0.3 × 0.30) + (0.7 × 0.20) + (0.8 × 0.10) = 0.55 (PASS but low)**
- **Decision**: Delegate to researcher-lead (Pattern Clarity < 0.7 triggers research)

**DECIDE**:

- Multi-source research → researcher-lead coordinates → Agent Selection Confidence: 0.9

**ACT**:

- Task(researcher-lead, "CREATE A RESEARCH PLAN for async validation in Pydantic v2") → spawn workers → synthesize

### Example 2 - "Fix auth bug in login flow"

**OBSERVE**:

- Verb: "fix" → Bug fix
- Entities: Login flow (1 component)

**ORIENT**: Check auto-loaded docs (agent-selection-guide.md: debugger vs development) → Context_Quality:

- Root cause known? NO → Investigation work
- Login flow location: `packages/core/auth/` → Main codebase scope

**DECIDE**:

- Bug fix (unknown cause) in packages/** → Directory Matrix → **debugger agent\*\* (confidence: 0.95)

**ACT**:

- Delegate to debugger for hypothesis-driven debugging

### Example 3 - "Add new feature to portfolio analyzer"

**OBSERVE**:

- Verb: "add" → Feature implementation
- Entities: Portfolio analyzer (likely multi-file)

**ORIENT**: Context_Quality assessment:

- Domain Familiarity: 0.8 (understand portfolio analysis domain)
- Pattern Clarity: 0.6 (need to check existing patterns)
- Dependency Understanding: 0.5 (unclear integration points)
- Risk Awareness: 0.7 (financial calculations need validation)
- **Context_Quality = (0.8 × 0.40) + (0.6 × 0.30) + (0.5 × 0.20) + (0.7 × 0.10) = 0.68 (MODERATE)**
- **Decision**: Standard research depth (2-3 workers, 10-15 min)

**DECIDE**:

- Multi-component feature → researcher-codebase (patterns) + feature-analyzer (dependencies)
- Agent Selection Confidence: 0.75

**ACT**:

- Spawn researchers in parallel → Synthesize patterns → Delegate to development

---

## Integration Points

**Related Frameworks**:

- **Agent Selection**: See `.claude/docs/guides/agent-selection-guide.md` for domain-first thinking
- **Research Coordination**: See `.claude/docs/guides/research-patterns.md` for researcher-lead protocol
- **Context Readiness**: See `.claude/agents/context-readiness-assessor.md` for detailed assessment methodology
- **Orchestration**: See `.claude/docs/orchestrator-workflow.md` for complete delegation patterns

**Token Budget**:

- This framework is NOT auto-loaded (too detailed for startup)
- Reference from CLAUDE.md when detailed OODA guidance needed
- Most requests can use compressed CLAUDE.md version
