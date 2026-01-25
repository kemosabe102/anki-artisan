---
title: "INFUSE Framework - Quick Reference"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
related:
  - ./infuse-framework.md
---
# INFUSE Framework - Quick Reference

**Purpose**: 30-second guide to INFUSE framework for agent prompt engineering

**Audience**: claude-code-ecosystem, orchestrator (during agent creation)

**Progressive Disclosure**: This is Tier 1. For detailed framework, see [infuse-framework.md](./infuse-framework.md)

---

## What is INFUSE?

**INFUSE** is a structured methodology for building AI agent prompts with consistent, predictable behavior. It provides a 6-component framework ensuring agents have clear identity, navigation rules, personality, user guidance, adaptive signals, and boundary enforcement.

**Origin**: Developed for custom GPT engineering, validated by academic research (PromptInfuser 2024), adapted for gauntlet-agents agent prompt design.

---

## The 6 Components (30-Second Overview)

| Component                    | Purpose                                                        | Key Question                                               |
| ---------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------- |
| **I - Identity & Goal**      | Define who the agent is and what it accomplishes               | "What role and mission does this agent have?"              |
| **N - Navigation Rules**     | Govern interaction patterns and boundaries                     | "How should it process information and handle edge cases?" |
| **F - Flow & Personality**   | Establish tone, style, and conversational characteristics      | "What personality fits this agent's domain?"               |
| **U - User Guidance**        | Provide structured approaches for achieving objectives         | "What frameworks guide the user interaction?"              |
| **S - Signals & Adaptation** | Enable dynamic response to user states (confusion, enthusiasm) | "How should it adapt to user emotional/behavioral cues?"   |
| **E - End Instructions**     | Reinforce critical boundaries and immutable constraints        | "What MUST ALWAYS or MUST NEVER happen?"                   |

---

## When to Use INFUSE

**✅ DO Use INFUSE When**:

- Creating new agent prompts from scratch
- Enhancing existing agents with inconsistent behavior
- Designing agents requiring emotional intelligence (user adaptation)
- Building domain-specific agents (technical writer, debugger, researcher)

**⚠️ CONSIDER Using INFUSE When**:

- Refactoring agents with boundary violations
- Adding personality/tone consistency to existing agents
- Improving user guidance frameworks

**❌ SKIP INFUSE When**:

- Simple utility agents with single-function tasks
- Agents where personality/adaptation is irrelevant (e.g., data transformers)
- Time-critical agent creation (use after MVP validation)

---

## Integration with Existing Agent Workflow

**Current Integration Points** (from codebase analysis):

1. **base-agent-pattern.md** (optimal integration point):
   - 23/35 agents inherit from it (~66% coverage)
   - INFUSE components map to: Knowledge Base (N), Reasoning Approach (U), Error Recovery (S), Validation (E)
   - **Action**: Enhance base pattern with INFUSE sections

2. **Agent-Specific Prompts**:
   - Identity & Goal → Role & Boundaries section (lines 10-20)
   - Flow & Personality → Reasoning Approach section (lines 122-150)
   - Signals & Adaptation → Error Recovery Patterns (base pattern inheritance)

3. **Schema-Driven Outputs**:
   - All agents use base-agent.schema.json
   - **Action**: Add `infuse_metadata` field for synthesis tracking

**Quick Integration Checklist**:

- [ ] Review agent's domain and determine INFUSE fit
- [ ] Map INFUSE components to existing agent sections
- [ ] Add Identity & Goal to Role definition
- [ ] Specify Navigation Rules in Permissions/Boundaries
- [ ] Define Flow & Personality in Reasoning Approach
- [ ] Document User Guidance frameworks in workflow
- [ ] Add Signal-Response pairs for adaptation (if needed)
- [ ] Reinforce End Instructions in Validation/Constraints

---

## 30-Second Decision Tree

```
Is this a new agent creation?
├─ YES → Use INFUSE framework (all 6 components)
└─ NO → Is this an enhancement/refactor?
    ├─ YES → Does agent need personality/adaptation?
    │   ├─ YES → Add F (Flow) + S (Signals) components
    │   └─ NO → Check boundaries only (E - End Instructions)
    └─ NO → Skip INFUSE (maintenance/bug fix)
```

---

## Common Pitfalls (Quick Dos/Don'ts)

**DO**:

- ✅ Use specific behavioral anchors ("responds like Chris Voss" not "be helpful")
- ✅ Show examples (models respond better to demonstrations than abstractions)
- ✅ Test edge cases (unusual scenarios reveal boundary gaps)

**DON'T**:

- ❌ Be vague with identity ("helpful assistant" is generic)
- ❌ Skip signal-response pairs (agents lack emotional intelligence without them)
- ❌ Conflict instructions (ensure I/N/F/U/S/E align)

---

## Next Steps

1. **For Complete Framework**: See [infuse-framework.md](./infuse-framework.md) for:
   - Detailed component descriptions with examples
   - Best practices and anti-patterns
   - Academic validation (PromptInfuser research)
   - Integration strategy with base-agent-pattern.md
   - 30+ practical patterns and templates

2. **For Agent Creation**: Use claude-code-ecosystem with INFUSE checklist:
   - Run `/create-agent` and reference INFUSE components during design
   - Validate agent against INFUSE completeness before activation

3. **For Existing Agents**: Run gap analysis:
   - Check agent against 6 components (which are missing?)
   - Prioritize E (End Instructions) and I (Identity) for consistency

---

**Token Budget**: ~600 tokens (vs. ~3,000 for full framework)

**Last Updated**: 2025-10-31
