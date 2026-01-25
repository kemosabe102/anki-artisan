---
title: "Agent Decision Protocol"
date: 2025-11-18
status: ACTIVE
tags: [agents, planning, decision-making, escalation]
---

# Agent Decision Protocol

**Purpose**: Standard decision-making framework for planning agents - information hierarchy, decision paths, limitations handling, and escalation strategies.

**Applies to**: researcher-lead, planning, architecture (planning-focused agents)

---

## Information Hierarchy

**1. Primary Source** (authoritative, always trusted):

- **Source Type**: Task input from orchestrator with metadata (Context_Quality, requirements, constraints)
- **Location**: Task description, delegation requirements, known gaps
- **Usage**: Core input for decision-making, strategy determination, delegation design

**2. Secondary Source** (reliable methodology):

- **Source Type**: Planning frameworks, patterns, and domain-specific guides
- **Location**: `.claude/docs/00-core/` guides, domain-specific methodology files
- **Usage**: Apply proven patterns, scaling rules, structure templates
- **Examples**: research-patterns.md, coordination-patterns.md, worker-allocation.md

**3. Tertiary Source** (contextual validation):

- **Source Type**: Light reconnaissance for validation (minimal tool calls)
- **Location**: Glob results for structure checks, file existence verification
- **Usage**: Validate assumptions, confirm domain existence, assess scope
- **Limits**: ≤3 tool calls (planning scope, not research/execution)

**4. Fallback Source** (when planning blocked):

- **Source Type**: User clarification and orchestrator guidance
- **Location**: Iteration context, gap summaries, follow-up requests
- **Usage**: Resolve ambiguous objectives, unclear boundaries, scope conflicts

---

## Decision Protocol

### Main Decision Path (Standard Planning)

1. **Parse Input** → Extract requirements, classify task type
2. **Apply Metadata** → Use Context_Quality/complexity scores for decision weighting
3. **Assess Scope** → Determine delegation needs (worker count, types)
4. **Design Plan** → Create delegations with appropriate structure
5. **Set Quality Targets** → Define success criteria, compression ratios
6. **Return Plan** → Output to orchestrator

### Iteration/Follow-up Decision Path

1. **Analyze Gaps** → Review orchestrator-provided gap patterns
2. **Group Similar** → Consolidate related gaps for efficient delegation
3. **Design Targeted** → Create focused delegations (1-3 workers, narrow scope)
4. **Link to Context** → Reference original plan, explain gap coverage
5. **Return Follow-up** → Output iteration plan to orchestrator

### Checkpoint Validation (Before Output)

**Quality Gates** (blocking - must pass):
- [ ] All delegations complete? (all required components present)
- [ ] Worker count within limits? (MAX_WORKERS enforced)
- [ ] Boundaries prevent scope creep? (exclusions defined)
- [ ] Tool usage within planning scope? (≤3 calls for structure checks)
- [ ] Plan is executable? (no ambiguous objectives, clear termination)

**Decision Point**: If ANY gate fails, fix before proceeding. If unfixable, escalate to orchestrator with clarification questions.

---

## Limitations Protocol

**Strategy**: Acknowledge limitations explicitly, delegate out-of-scope work, never attempt execution beyond planning domain.

### Out-of-Scope Topic Examples

**Execution Requests**:
- User: "Execute this research"
- Response: "I create plans, orchestrator executes. Returning delegation plan for orchestrator to spawn workers."

**Synthesis Requests**:
- User: "Synthesize worker findings"
- Response: "Synthesis is orchestrator responsibility. I can provide synthesis approach guidance in plan, but orchestrator performs synthesis."

**Implementation Decisions**:
- User: "What should we implement?"
- Response: "Implementation decisions outside planning scope. Recommend delegating to planning or architecture agent."

**Domain Expertise**:
- User: "Is this architecture scalable?"
- Response: "Architecture evaluation outside planning scope. Delegating to architecture agent for assessment."

### Handling Strategy Matrix

| Request Type | Agent Action | Rationale |
|--------------|--------------|-----------|
| **Planning** (delegation design, scaling) | Plan confidently | Core domain |
| **Execution** (research, implementation) | Acknowledge limitation, delegate to workers | Out of scope |
| **Synthesis** (combining results) | Provide guidance, orchestrator handles | Out of scope |
| **Domain Expertise** (technical decisions) | Delegate to domain specialist | Lacks expertise |

---

## Escalation Path

**Attempt Definition**: One "attempt" = analysis cycle (parse → match patterns → validate → decide)

**Typical Duration**: 2-3 minutes per attempt

### 3-Step Escalation (When Planning Blocked)

**1. First Attempt** (Quick Resolution):
- **Action**: Parse input → Match to known patterns from guides → Validate with minimal tools (≤3 calls)
- **Success Criteria**: Task classified AND plan designed OR ambiguity identified
- **Failure Trigger**: Objective unclear after pattern matching

**2. Second Attempt** (Pattern Search):
- **Action**: Review similar scenarios in orchestrator-workflow.md, delegation-examples.md
- **Success Criteria**: Found comparable pattern OR confirmed task is novel
- **Failure Trigger**: No comparable pattern exists AND task still unclear

**3. Final Escalation** (User Clarification):
- **Action**: Report to orchestrator with specific clarification questions (2-5 questions)
- **Required Output**:
  - Ambiguity description (what's unclear)
  - Clarification questions (specific, actionable)
  - Suggested approach if user clarifies
- **Example**: "Research objective unclear. Clarify: (1) Focus on library docs only or include community practices? (2) Compare all 6 frameworks or prioritize top 3?"

### Escalation Triggers (Deterministic)

| Condition | Trigger Point | Action |
|-----------|---------------|--------|
| Ambiguous objective | After attempt 1 (3 min) | Request clarification with specific questions |
| Unclear scope boundaries | After attempt 2 (6 min) | Escalate with disambiguation questions |
| Impossible complexity assessment | No reconnaissance possible | Report gap, request user input |
| Conflicting requirements | Detected during validation | Report conflict, request prioritization |

**Max Attempts**: 3 (total ~6-9 minutes)
**After Max**: Escalate with FAILURE status, detailed clarification questions, suggested resolution paths

---

## Usage Guidelines

**When to Use This Protocol**:
- Any planning agent (researcher-lead, planning, architecture)
- Decision-making under uncertainty
- Handling out-of-scope requests
- Escalation scenarios

**How to Apply**:
1. **Information Hierarchy**: Source decisions in priority order (Primary → Secondary → Tertiary → Fallback)
2. **Decision Protocol**: Follow main path for standard work, iteration path for follow-up
3. **Limitations Protocol**: Acknowledge out-of-scope explicitly, delegate appropriately
4. **Escalation Path**: Attempt resolution systematically (3 attempts max), escalate with specifics

**Agent-Specific Adaptations**:
- **researcher-lead**: Uses CAGEERF methodology within decision protocol
- **/spec command**: Focuses on FR-ID mapping and component breakdown
- **planning**: Emphasizes business context and goal extraction
- **architecture**: Prioritizes NFR analysis and tech stack decisions

---

**Last Updated**: 2025-11-18
**Related Guides**: research-patterns.md, coordination-patterns.md, orchestrator-workflow.md
