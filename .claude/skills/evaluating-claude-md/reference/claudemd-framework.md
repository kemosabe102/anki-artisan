# CloudMD Orchestrator Framework
## Context-Aware Agent Orchestration for Research → Plan → Implementation

**Version**: 2.0  
**Last Updated**: December 2025  
**Aligned with**: Anthropic Best Practices, OODA Loop, HumanLayer Context Engineering

---

## 1. Executive Summary

The **CloudMD Orchestrator** is a read-only coordinator that manages three operational phases mapped to the **OODA Loop**:

| OODA Phase | CloudMD Phase | Purpose | Agent Types |
|-----------|---------------|---------|-------------|
| **Observe** | **Research** | Gather context, understand problem space | Explorer, Platform Engineer, Domain Specialist |
| **Orient** | **Plan** | Analyze data, build decision models | Architect, Planner, Design Reviewer |
| **Decide** | **[Integrated]** | Finalize approach with human approval | Human Review |
| **Act** | **Implementation** | Execute changes, monitor outcomes | Implementer, Builder, Validator |

**Core Mechanism**: Context offloading through domain-appropriate agent delegation. The orchestrator routes to *any available specialist agent*, not rigid roles.

---

## 2. Foundational Principles

### 2.1 The "Read-Only Coordinator" Pattern
- **Role**: Project Coordinator (never a worker)
- **Tool Restriction**: Discovery (glob, ls), limited read (one strategic operation), delegation
- **No Direct Modifications**: Never write code, edit files, or run implementation tasks
- **Context Preservation**: Every token saved on delegation enables higher-level coordination

### 2.2 The "One-Read Rule"
> If you need to read files to understand a request, perform **one** multi-file read operation. If insufficient, **immediately delegate to a specialist agent**.

**Why**: A single well-targeted read tells you *where* the problem is. The specialist agent, with fresh context, discovers the *what* and *how*.

### 2.3 The "Dumb Zone" (40% Context Rule)
> **LLM performance degrades significantly after ~40% context usage**, even if technically within token limits.

**Implication**: 
- A 200k context window has an effective "Smart Zone" of ~80k tokens
- Beyond 40% usage, diminishing returns set in
- **Solution**: Aggressive delegation and "Frequent Intentional Compaction"

### 2.4 Progressive Disclosure via Domain Agents
Instead of loading all knowledge at once, specialist agents carry domain expertise:
- **Research Phase**: Platform engineers, explorers, domain researchers
- **Planning Phase**: Architects, planners, design reviewers, trade-off analysts
- **Implementation Phase**: Implementers, builders, validators, testers

The CloudMD orchestrator knows *which domain* to invoke and *what question* to ask—not the answers themselves.

### 2.5 "Frequent Intentional Compaction"
**The Workflow**:
1. Agent works toward milestone
2. Agent writes `COMPACTED_CONTEXT.md` with *only* what's needed next
3. **Restart**: New context window loads *only* the compaction file
4. Work continues in fresh "Smart Zone"

**When to Compact**:
- Any phase exceeds ~20 conversational turns
- Context usage approaches 40%
- Agent feels "stuck" or starts hallucinating
- Natural phase boundaries (Research → Plan → Implement)

---

## 3. CloudMD Structure (Lean, Persistent Context)

### 3.1 File Size Target
- **Target Size**: < 200 lines
- **Hard Limit**: ≤ 300 lines
- **Principle**: Every line must earn its place; point to external docs rather than embedding

### 3.2 Essential Sections

```markdown
# CloudMD – Project Orchestrator

## Project Identity
- **Name**: [Project Name]
- **Purpose**: [One-sentence mission]
- **Tech Stack**: [Key technologies, versions]

## Orchestration Role
- **You are**: The Project Coordinator (read-only)
- **You delegate**: Research, planning, implementation to domain specialists
- **You preserve**: Context by offloading complexity
- **You never**: Write code, deep-dive files, or perform specialist work

## Core Constraints
- **DO NOT** read >5 files in a single operation
- **DO NOT** attempt any code/config changes yourself
- **DO NOT** run test suites or deployment commands
- **DO** use one strategic read, then delegate immediately
- **DO** stay under 40% context usage (the "Smart Zone")
- **DO** compact and restart threads when approaching limits

## Available Specialist Agents
[List available agents dynamically - examples below]

### Research Phase Specialists
- **Explorer Agent**: Codebase navigation, file discovery
- **Platform Engineer Agent**: Infrastructure, deployment, ops research
- **Domain Researcher Agent**: Business logic, feature understanding
- **[Your Custom Agent]**: [Specific domain]

### Planning Phase Specialists
- **Architect Agent**: System design, technical decisions
- **Planner Agent**: Roadmap creation, task sequencing
- **Design Reviewer Agent**: Architecture validation, trade-off analysis
- **[Your Custom Agent]**: [Specific domain]

### Implementation Phase Specialists
- **Implementer Agent**: Code changes, refactoring
- **Builder Agent**: Feature development, testing
- **Validator Agent**: Quality assurance, verification
- **[Your Custom Agent]**: [Specific domain]

## Agent Selection Guidelines
Select agents based on:
1. **Domain Match**: Which agent has expertise in this area?
2. **Phase Alignment**: Does this agent excel at research/plan/implement?
3. **Availability**: Is this agent configured and accessible?
4. **Context Efficiency**: Will this agent use context wisely?

*Default to the most domain-specific agent available. If uncertain, use general-purpose agents (explorer/architect/implementer).*

## Three-Phase Workflow (OODA Loop)

### Phase 1: Research (Observe)
**Entry**: User asks question or project requires discovery
**Delegate to**: Domain-appropriate research specialist
**Exit Criteria**: Research checklist complete (see Phase Checklists)
**Output**: Compacted context file for planning

### Phase 2: Planning (Orient + Decide)
**Entry**: Research complete + high-level goal
**Delegate to**: Domain-appropriate planning specialist
**Exit Criteria**: Planning checklist complete (see Phase Checklists)
**Output**: Approved roadmap with code snippets

### Phase 3: Implementation (Act)
**Entry**: Approved roadmap from planning
**Delegate to**: Domain-appropriate implementation specialist
**Exit Criteria**: Implementation checklist complete (see Phase Checklists)
**Output**: Verified changes, tests passing

## Compaction Protocol (Avoiding the Dumb Zone)
If any thread exceeds ~20 turns or approaches 40% context:
1. **Compact**: Ask agent to write `phase_checkpoint.md` summary
2. **Restart**: Start new thread with user
3. **Resume**: Load only checkpoint file to continue

## Documentation Map (Progressive Disclosure)
- **Architecture Decisions**: `docs/adr/`
- **Implementation Guides**: `docs/guides/`
- **Agent Specifications**: `.claude/agents/`
- **Domain Skills**: `.claude/skills/`

*Load these only when a specialist recommends them or task requires that domain.*
```

---

## 4. Phase Checklists (Domain-Agnostic)

### 4.1 Research Phase Completion Checklist

**Before moving to Planning, verify:**

- [ ] **Scope Clarity**: Do we understand the problem we're solving?
- [ ] **Current State Mapped**: Can we describe the existing system/architecture?
- [ ] **Code Truth**: Did we read *source code* (not just docs) to verify findings?
- [ ] **Gap Identification**: What's missing, broken, or needs investigation?
- [ ] **Assumptions Documented**: What are we assuming to be true?
- [ ] **Dependency Map**: What systems/components depend on this?
- [ ] **Constraint List**: Budget, timeline, tech, compliance constraints identified?
- [ ] **Success Metrics**: How will we measure success?
- [ ] **Stakeholder Clarity**: Who validates/approves this work?
- [ ] **Context Compacted**: Research output condensed to essential truths

**Handoff Artifact**: `research_summary.md` with:
- Key findings (with line numbers/file references)
- Identified gaps
- Recommended approach for planning
- File paths for deep-dive (not full contents)

---

### 4.2 Planning Phase Completion Checklist

**Before moving to Implementation, verify:**

- [ ] **Approach Justified**: Why this solution vs. alternatives?
- [ ] **Trade-offs Documented**: What are the pros/cons?
- [ ] **Code Snippets Included**: Function signatures, interfaces, data structures for key components
- [ ] **Implementation Stages**: Can we break into clear, independent tasks?
- [ ] **Dependencies Sequenced**: Are dependencies in correct order?
- [ ] **Resource Estimate**: Rough effort/time estimates provided?
- [ ] **Risk Assessment**: What could go wrong? Mitigations identified?
- [ ] **Test Strategy**: How do we validate each phase?
- [ ] **Rollback Plan**: Can we safely undo if needed?
- [ ] **Communication Plan**: Who needs updates at each stage?
- [ ] **Human Approval**: Has plan been reviewed and approved?
- [ ] **Context Compacted**: Plan distilled to actionable roadmap

**Handoff Artifact**: `implementation_plan.md` with:
- Phased roadmap with specific tasks
- Code snippets proving architectural understanding
- Verification criteria for each phase
- Risk mitigation strategies

**Critical**: Plans must include **actual code snippets** (signatures, types, interfaces). Vague plans lead to unreliable implementations.

---

### 4.3 Implementation Phase Completion Checklist

**For EACH implementation phase, verify:**

- [ ] **Code Quality**: Changes align with project standards?
- [ ] **Test Coverage**: All success criteria validated?
- [ ] **Code Snippets Match**: Implementation matches signatures from plan?
- [ ] **Documentation Updated**: Docs reflect new state?
- [ ] **Peer Review**: Code reviewed (human or automated)?
- [ ] **Deployment Safe**: Can deploy? Rollback plan ready?
- [ ] **Performance Impact**: No unexpected degradation?
- [ ] **Security Check**: No new vulnerabilities?
- [ ] **Stakeholder Notification**: Relevant parties updated?
- [ ] **Blocker Resolution**: Critical issues resolved or escalated?
- [ ] **Phase Verification**: Success criteria from plan met?
- [ ] **Context Status**: Still in Smart Zone (<40%)?

**Handoff Artifact**: `phase_N_report.md` per phase with:
- Changes made (with file references)
- Test results (pass/fail with evidence)
- Blockers encountered (and resolution)
- Readiness for next phase

---

## 5. Orchestrator Decision Tree (Domain-Agnostic)

```
User Request
    ↓
1. Do I understand enough context?
    ├─ YES → Go to Step 2
    └─ NO → Perform ONE strategic read (max 5 files)
              If still NO → Delegate to research specialist
              ↓
2. Is this a Research/Discovery question?
    ├─ YES → Select appropriate research specialist
    │        (Explorer? Platform Engineer? Domain Researcher?)
    │        /agents run [specialist] [task]
    └─ NO → Go to Step 3
              ↓
3. Is this a Planning/Design question?
    ├─ YES → Have I completed research first?
    │        ├─ NO → Go back to Step 2
    │        └─ YES → Select planning specialist
    │                 (Architect? Planner? Design Reviewer?)
    │                 /agents run [specialist] [goal + research]
    └─ NO → Go to Step 4
              ↓
4. Is this an Implementation task?
    ├─ YES → Have I completed research + planning?
    │        ├─ NO → Go back to appropriate step
    │        └─ YES → Select implementation specialist
    │                 (Implementer? Builder? Validator?)
    │                 /agents run [specialist] [task from roadmap]
    └─ NO → Coordinate/synthesize from specialist outputs
```

---

## 6. Anti-Patterns (Universal)

| Anti-Pattern | Why Bad | Fix |
|-------------|---------|-----|
| Read 15+ files to "understand" | Context pollution; dumb zone | One read, then delegate |
| "I'll just fix this quickly" | Breaks coordinator discipline | Always delegate to implementation specialist |
| Run full test suite | Not coordinator's job; wastes context | Ask implementer to verify |
| Pass full file contents to agents | Bloats their context | Pass file paths + key excerpts |
| Skip research for "simple" tasks | Plans built on assumptions fail | Always research first |
| Plan without code snippets | Vague plans → unreliable execution | Require signatures/interfaces |
| Plan without approval | Wrong solution gets built | Always get human sign-off |
| Ignore 40% context rule | Work in dumb zone → poor results | Compact and restart aggressively |
| Rely on static docs | Docs are often "slop" (outdated) | Read code; trust source of truth |

---

## 7. Context Window Management

### 7.1 Token Budget (Claude 3.5 Sonnet Example)

| Component | Tokens | Purpose |
|-----------|--------|---------|
| CloudMD Instructions | ~500 | Persistent role definition |
| Available Agents List | ~300 | Routing and delegation |
| Current Phase Context | ~2,000 | Working memory |
| File References (paths) | ~300 | Navigation |
| **Smart Zone Budget** | **~80,000** | **40% of 200k total** |
| Conversation History | Remaining | Task-specific interaction |

### 7.2 Staying in the Smart Zone

**Tactics**:
1. **Offload to files**: Research findings → `research_summary.md`
2. **Offload to specialists**: Deep analysis → fresh agent context
3. **Compress summaries**: Request key points, not full reports
4. **Version snapshots**: Save state at phase boundaries
5. **Restart threads**: When approaching 40%, compact and restart

**Warning Signs** (entering dumb zone):
- Specialist takes >20 turns without completing
- Agent starts repeating itself
- Hallucinations increase
- Context usage >40%

**Fix**: Compact and restart immediately.

---

## 8. Specialist Agent Interface Standards

### 8.1 Research Specialist Input/Output

**Input Format**:
```
Goal: [What do we need to understand?]
Scope: [Which areas/components to investigate?]
Domain: [Technical domain context]
Constraints: [Time, access, complexity limits]
```

**Output Format**:
```markdown
## Research Findings
### Summary (2-3 sentences)
[High-level overview]

### Key Facts (with evidence)
- Fact 1 [File: path/to/file.ts:45-67]
- Fact 2 [File: path/to/config.yml:12]

### Code Truth (actual code references)
- [Not documentation; actual source code findings]

### Gaps & Unknowns
- Gap 1: [What we don't know yet]

### Recommended Next Steps
1. [Action for planning phase]
```

---

### 8.2 Planning Specialist Input/Output

**Input Format**:
```
Goal: [What needs to be designed/planned?]
Research Findings: [Summary from research specialist]
Constraints: [Budget, timeline, tech limits]
Success Metrics: [How will we measure success?]
```

**Output Format**:
```markdown
## Implementation Plan

### Approach Justification
[Why this approach; alternatives considered]

### Trade-Off Analysis
| Option | Pros | Cons | Recommendation |

### Code Snippets (CRITICAL)
```typescript
// Example: Function signatures for key components
interface NotificationService {
  send(userId: string, message: Message): Promise<void>;
  subscribe(userId: string, callback: Handler): void;
}
```

### Implementation Phases
1. Phase 1: [Task] (Effort: X hours)
   - Files: [list]
   - Tests: [how to verify]
2. Phase 2: [Task] (Effort: X hours)

### Risk Assessment
| Risk | Probability | Mitigation |

### Success Criteria (Testable)
- [ ] Criterion 1 (how to verify)
- [ ] Criterion 2 (how to verify)
```

**Critical Requirement**: Plans must include actual code snippets (function signatures, interfaces, data structures). This proves the planner understands the implementation and prevents hallucination.

---

### 8.3 Implementation Specialist Input/Output

**Input Format**:
```
Phase: [Phase number and name from plan]
Task: [Specific implementation task]
Code Snippets: [Signatures/interfaces from plan]
Success Criteria: [How to verify completion]
Test Strategy: [How to validate]
```

**Output Format**:
```markdown
## Phase [N] Implementation Report

### Changes Made
- File 1: [description]
- File 2: [description]

### Code Snippets Match?
- ✓ Signatures match plan
- ✓ Interfaces implemented as designed

### Tests Passed
- Test 1: PASS [evidence]
- Test 2: PASS [evidence]

### Blockers (if any)
- [Description, recommended resolution]

### Verification
All success criteria met: YES / NO [with evidence]

### Ready for Next Phase?
YES / NO [with justification]
```

---

## 9. Dynamic Agent Selection Strategy

### Principle: Domain Over Role

**Don't think**: "I need a 'researcher' agent"
**Think**: "I need a **platform engineering specialist** to research infrastructure"

### Selection Matrix

| Task Type | Domain Examples | Appropriate Specialist |
|-----------|-----------------|------------------------|
| **Understand deployment** | Infrastructure, CI/CD | Platform Engineer (research) |
| **Map API endpoints** | Backend, REST/GraphQL | Backend Explorer (research) |
| **Analyze frontend state** | React, Vue, Angular | Frontend Specialist (research) |
| **Design database schema** | PostgreSQL, MongoDB | Data Architect (planning) |
| **Plan microservice refactor** | Distributed systems | System Architect (planning) |
| **Implement auth flow** | OAuth, JWT, sessions | Security Implementer (implementation) |
| **Build UI component** | React, styling, UX | Frontend Builder (implementation) |

### When to Use General-Purpose Agents

- **Explorer**: When domain is unknown or crosses multiple areas
- **Architect**: When design spans multiple domains
- **Implementer**: When task is straightforward and domain-agnostic

---

## 10. Mental Alignment Through Plans

### Code Review is for Mental Alignment
> "I can't read 1,000 lines of code every week. But I can read the plans and stay aligned on how the system is evolving."
> — Senior Engineer perspective

**Tactic**: Plans become the primary artifact for team coordination.

### The Trade-Off Curve
```
Plan Length
    ↑
    │         ┌─── Sweet Spot
    │        ╱ ╲
Reliability│       ╱   ╲
    │      ╱     ╲
    │     ╱       ╲ ← Readability
    │    ╱         ╲
    │───╱───────────╲─────→
         Plan Detail
```

**Finding Your Sweet Spot**:
- Too vague → Unreliable execution
- Too detailed → Nobody reads it
- **Goal**: Readable by humans + executable by AI

---

## 11. When to Use Each Level of Rigor

| Complexity | Research | Planning | Implementation | Example |
|-----------|----------|----------|----------------|---------|
| **Trivial** | None | None | Direct task | Change button color |
| **Simple** | Quick context | Informal | Standard process | Add form field |
| **Medium** | Focused research | Structured plan | Phase-gated | New API endpoint |
| **Complex** | Deep research | Detailed plan with snippets | Multi-phase with validation | Auth system refactor |
| **Critical** | Multi-domain research | Architecture review + multiple plans | Staged rollout with monitoring | Database migration |

**Rule of Thumb**: The harder the problem, the more context engineering required. The ceiling of what you can solve goes up with rigor.

---

## 12. Evaluation Checklist for Your CloudMD

Use this to validate your orchestrator setup:

### Structure & Format
- [ ] **File Size**: CloudMD is <200 lines (≤300 hard limit)
- [ ] **Role Clear**: "You are a read-only coordinator" stated explicitly
- [ ] **Project Identity**: Name, purpose, tech stack defined
- [ ] **No Code**: Orchestrator never writes code (explicit constraint)

### Agent Configuration
- [ ] **Specialist Agents Listed**: Available agents documented by domain
- [ ] **Selection Guidance**: Criteria for choosing agents provided
- [ ] **Domain Coverage**: Research/Plan/Implement specialists for your domains
- [ ] **Flexibility**: Agents described by capability, not rigid roles

### Phase Structure
- [ ] **Three Phases Defined**: Research → Plan → Implement (OODA aligned)
- [ ] **Exit Checklists**: Each phase has testable completion criteria
- [ ] **Phase Artifacts**: Expected outputs defined (summaries, plans, reports)
- [ ] **Approval Gates**: Human review points identified

### Context Management
- [ ] **One-Read Rule**: Explicitly stated
- [ ] **40% Rule**: Dumb zone concept explained
- [ ] **Compaction Protocol**: Process for restarting threads defined
- [ ] **Token Budget**: Context allocation strategy documented

### Quality Standards
- [ ] **Code Truth**: Research must read source code (not just docs)
- [ ] **Code Snippets**: Plans must include signatures/interfaces
- [ ] **Mental Alignment**: Plans serve as team coordination artifact
- [ ] **Anti-Patterns**: Common mistakes explicitly forbidden

### Process Integration
- [ ] **Decision Tree**: Routing logic for agent selection
- [ ] **Blocker Escalation**: Path for handling implementation blockers
- [ ] **Documentation Map**: Links to additional resources (progressive disclosure)
- [ ] **Success Metrics**: Non-negotiable project criteria defined

### Practical Validation
- [ ] **Tested**: Successfully delegated at least one research task
- [ ] **Readable**: Team member can understand phases in <2 minutes
- [ ] **Findable**: Agent specs accessible in `.claude/agents/`
- [ ] **Iterative**: Framework includes guidance on when to adjust rigor

---

## 13. Common Customization Points

### Adding Domain-Specific Specialists
```markdown
### [Your Domain] Specialists
- **[Agent Name]**: [Capability description]
  - Use for: [Specific tasks]
  - Expertise: [Domain knowledge]
```

### Adjusting Phase Rigor
For **rapid prototyping**:
- Lighter checklists
- Fewer code snippets in plans
- Faster approval gates

For **mission-critical systems**:
- Comprehensive checklists
- Detailed code snippets with types
- Multi-stage approval (architect + security + lead)

### Adding Phase 0 (for compliance-heavy domains)
```markdown
### Phase 0: Security Audit (Pre-Research)
**Delegate to**: Security Specialist
**Exit Criteria**: Risk assessment complete, mitigations defined
```

---

## 14. References & Influences

**Core Concepts**:
- **Anthropic Best Practices**: Read-only coordinator, progressive disclosure
- **OODA Loop**: Observe-Orient-Decide-Act decision framework
- **HumanLayer / Dex Horthy**: Frequent intentional compaction, the dumb zone (40% rule), code truth over docs
- **LangChain Context Engineering**: Write, select, compress, isolate context strategies

**Key Insight**: AI cannot replace thinking—it can only amplify the thinking you've done (or failed to do).

---

**End of CloudMD Orchestrator Framework**

This document provides the complete theory and mental models for context-aware agent orchestration. Use alongside the Quick Reference Guide, Visual Guide, and Evaluation Checklist for comprehensive implementation support.
