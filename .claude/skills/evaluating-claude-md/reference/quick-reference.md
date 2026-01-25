# CloudMD Quick Reference & Evaluation Guide
## Practical Checklist for Orchestrator Implementation

---

## Quick Start: 4-Step Setup

### Step 1: Create Your CloudMD File (30 min)
```markdown
# CloudMD – [Your Project]

## Project Identity
- **Name**: [Project name]
- **Purpose**: [One sentence]
- **Stack**: [Key tech]

## Orchestration Role
You are the read-only coordinator. You delegate to domain specialists.
**You never write code or deep-dive files. You route to experts.**

## Available Specialist Agents
[List your agents here by domain and capability]

## Three-Phase Workflow
1. **Research** → Delegate to domain specialist
2. **Plan** → Delegate to planning specialist  
3. **Implement** → Delegate to implementation specialist

## Core Rules
- ONE strategic read, then delegate
- Stay under 40% context usage
- Compact and restart when threads get long
- Read CODE, not docs (code is truth)
```

### Step 2: List Your Available Agents (10 min)
Create `.claude/agents/` directory and list agent capabilities:
- Research specialists (explorer, platform engineer, etc.)
- Planning specialists (architect, planner, etc.)
- Implementation specialists (implementer, builder, etc.)

### Step 3: Define Phase Checklists (15 min)
Copy phase checklists from Framework document.
Customize for your domain.

### Step 4: Test & Iterate (ongoing)
Run one research task → validate routing → refine.

**Total Setup Time**: ~1 hour

---

## The Three-Phase Pattern (Visual)

```
USER REQUEST
     ↓
┌─────────────────────┐
│  CloudMD Reads:     │
│  • One-read rule    │
│  • Context <40%     │
│  • Then DELEGATES   │
└──────────┬──────────┘
           ↓
    ┌──────────────┐
    │ PHASE 1:     │
    │ RESEARCH     │
    │              │
    │ Delegate to: │
    │ • Explorer   │
    │ • Platform   │
    │ • Domain     │
    │   Specialist │
    └──────┬───────┘
           │ Returns: research_summary.md
           ↓
    ┌──────────────┐
    │ PHASE 2:     │
    │ PLAN         │
    │              │
    │ Delegate to: │
    │ • Architect  │
    │ • Planner    │
    │ • Reviewer   │
    └──────┬───────┘
           │ Returns: implementation_plan.md
           │         (with code snippets!)
           ↓
    ┌──────────────┐
    │ PHASE 3:     │
    │ IMPLEMENT    │
    │              │
    │ Delegate to: │
    │ • Builder    │
    │ • Validator  │
    │ • Implementer│
    └──────┬───────┘
           │ Returns: phase_N_report.md
           ↓
    ┌──────────────┐
    │  DELIVERY ✓  │
    └──────────────┘
```

---

## Critical Success Factors

### 1. The 40% Rule (Stay in Smart Zone)
**Problem**: LLMs degrade after ~40% context usage
**Solution**: 
- Monitor context usage
- Compact when approaching 40%
- Restart threads aggressively

**Signs you're in the "Dumb Zone"**:
- Agent takes >20 turns without progress
- Starts repeating itself
- Hallucinations increase
- Quality drops

**Fix**: Compact now, restart fresh.

---

### 2. Code Truth Over Docs
**Problem**: Documentation is often outdated ("slop")
**Solution**: Research agents must read SOURCE CODE

**Bad Research**:
```
"According to docs/architecture.md, we use polling for notifications."
```

**Good Research**:
```
"Reading src/notification/service.ts:45-67, the NotificationService 
currently uses setInterval polling. WebSocket infrastructure exists 
but is unused (src/websocket/server.ts)."
```

---

### 3. Plans Must Include Code Snippets
**Problem**: Vague plans lead to unreliable implementations
**Solution**: Planning agents must include actual signatures/interfaces

**Bad Plan**:
```
Phase 1: Build notification service
Phase 2: Add WebSocket support
Phase 3: Connect frontend
```

**Good Plan**:
```
Phase 1: Build notification service
Files: src/notification/service.ts

```typescript
interface NotificationService {
  send(userId: string, msg: Message): Promise<void>;
  subscribe(userId: string, handler: Handler): Subscription;
}
```

Tests: Unit tests for send(), integration test for subscribe()
```

**Why**: Code snippets prove the planner understands the implementation before starting.

---

### 4. Frequent Intentional Compaction
**When to Compact**:
- Thread exceeds ~20 turns
- Approaching 40% context
- Agent seems stuck
- Natural phase boundaries

**How to Compact**:
1. Ask agent: "Write a compacted_context.md with only what's needed for the next phase"
2. Review the compaction file
3. Start fresh thread
4. Load only the compaction file

**Result**: Fresh context, stay in Smart Zone.

---

## Orchestrator Evaluation Checklist

### ✅ Structure (Score: /10)
- [ ] File size <200 lines (2 pts)
- [ ] "Read-only coordinator" explicitly stated (2 pts)
- [ ] Project identity clear (name/purpose/stack) (2 pts)
- [ ] Three phases defined (Research/Plan/Implement) (2 pts)
- [ ] Available agents listed (2 pts)

### ✅ Context Management (Score: /10)
- [ ] One-Read Rule stated (4 pts)
- [ ] Token budget strategy documented (3 pts)
- [ ] Anti-patterns listed (3 pts)

### ✅ Agent Configuration (Score: /10)
- [ ] Research specialists listed (2 pts)
- [ ] Planning specialists listed (2 pts)
- [ ] Implementation specialists listed (2 pts)
- [ ] Selection guidance provided (2 pts)
- [ ] Agents described by domain/capability (2 pts)

### ✅ Phase Quality (Score: /10)
- [ ] Research checklist exists (2 pts)
- [ ] Planning checklist exists (2 pts)
- [ ] Implementation checklist exists (2 pts)
- [ ] Exit criteria testable (2 pts)
- [ ] Handoff artifacts defined (2 pts)

### ✅ Quality Standards (Score: /10)
- [ ] "Code Truth" requirement (research must read code) (3 pts)
- [ ] "Code Snippets" requirement (plans must include signatures) (3 pts)
- [ ] Human approval gates identified (2 pts)
- [ ] Blocker escalation path defined (2 pts)

### ✅ Practical Validation (Score: /10)
- [ ] Successfully tested with one research task (3 pts)
- [ ] Team can understand in <2 minutes (2 pts)
- [ ] Agent specs accessible (`.claude/agents/`) (2 pts)
- [ ] Documentation map provided (progressive disclosure) (2 pts)
- [ ] Includes guidance on when to adjust rigor (1 pt)

---

## Scoring Guide

**Total Score**: _____ / 60

| Score | Grade | Assessment |
|-------|-------|------------|
| 55-60 | A+ | Production-ready orchestrator |
| 48-54 | A | Strong orchestrator, minor refinements |
| 42-47 | B | Good foundation, needs iteration |
| 36-41 | C | Functional but missing key concepts |
| <36 | D/F | Requires significant rework |

---

## Common Failure Patterns

### 🚫 Pattern 1: "Swiss Army Knife" CloudMD
**Symptom**: CloudMD is 500+ lines with embedded knowledge
**Problem**: Context pollution before work even starts
**Fix**: Compress to <200 lines; use progressive disclosure

### 🚫 Pattern 2: Rigid Agent Roles
**Symptom**: "Always use researcher for research"
**Problem**: Ignores domain specialization
**Fix**: List agents by capability, route by domain

### 🚫 Pattern 3: No Compaction Protocol
**Symptom**: Threads run 50+ turns, quality degrades
**Problem**: Living in the Dumb Zone
**Fix**: Add explicit compaction triggers (20 turns or 40%)

### 🚫 Pattern 4: Vague Plans
**Symptom**: Plans say "Build the feature" without specifics
**Problem**: Implementers hallucinate details
**Fix**: Require code snippets in all plans

### 🚫 Pattern 5: Documentation Trust
**Symptom**: Research cites docs instead of code
**Problem**: Docs are often outdated ("slop")
**Fix**: Enforce "Code Truth" requirement

---

## Decision Matrix: When to Use Each Phase

| Scenario | Research? | Plan? | Implement? |
|----------|-----------|-------|------------|
| **"Change button color"** | No | No | Direct |
| **"Add form field"** | Quick | Informal | Yes |
| **"New API endpoint"** | Yes | Yes | Yes (phased) |
| **"Refactor auth"** | Deep | Detailed + snippets | Yes (multi-phase) |
| **"Migrate database"** | Multi-domain | Architecture review | Yes (staged) |

**Rule**: Complexity ↑ → Rigor ↑

---

## Agent Selection Quick Guide

### Research Phase
**Question**: "What domain needs investigation?"

| Domain | Suggested Agent |
|--------|----------------|
| Infrastructure/Ops | Platform Engineer |
| API/Backend | Backend Explorer |
| Frontend/UI | Frontend Specialist |
| Data/Analytics | Data Engineer |
| Unknown/Cross-domain | General Explorer |

### Planning Phase
**Question**: "What type of design is needed?"

| Design Type | Suggested Agent |
|-------------|----------------|
| System architecture | System Architect |
| Task sequencing | Planner |
| Trade-off analysis | Design Reviewer |
| Data modeling | Data Architect |
| Multi-domain | Senior Architect |

### Implementation Phase
**Question**: "What needs to be built?"

| Build Type | Suggested Agent |
|------------|----------------|
| Backend code | Backend Implementer |
| Frontend UI | Frontend Builder |
| Tests/QA | Validator |
| Refactoring | Code Refactorer |
| General tasks | General Implementer |

---

## Mental Models

### Context as a Resource
```
Context Budget = Smart Zone (~80k tokens)

Every token spent on:
• Reading files you won't use
• Repeating conversations
• Loading irrelevant docs

Is a token NOT available for:
• High-quality reasoning
• Accurate implementation
• Problem solving
```

**Principle**: Preserve context like you preserve memory in a tight algorithm.

---

### Plans as Team Coordination
```
Traditional Code Review:
Developer writes 1000 lines → Reviewer reads 1000 lines
Time: Hours per PR

Plan-First Review:
Planner writes 50-line plan → Reviewer reads plan → Approves
Time: 10 minutes

Then: Implementer writes 1000 lines (already approved approach)
Review focuses on: Does it match the plan?
```

**Benefit**: Mental alignment at design time, not code review time.

---

### The Compaction Loop
```
Work → Milestone → Compact → Restart → Work → ...

Without compaction:
0 turns: Fresh
20 turns: Effective
40 turns: Degrading
60 turns: Dumb Zone (poor results)

With compaction:
0-20 turns: Fresh → Compact
0-20 turns: Fresh → Compact
0-20 turns: Fresh → Compact
[Always in Smart Zone]
```

---

## Troubleshooting Guide

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| Agent takes 30+ turns | Living in Dumb Zone | Compact and restart now |
| Plans are vague | No code snippet requirement | Add code snippet checklist item |
| Research cites docs | "Code Truth" not enforced | Update research checklist |
| Wrong agent selected | No selection guidance | Add domain-to-agent matrix |
| Phases unclear | No exit checklists | Copy from framework, customize |
| Context pollution early | CloudMD too long | Compress to <200 lines |
| Quality drops mid-project | No compaction protocol | Add 40% restart trigger |

---

## File Structure Reference

```
project-root/
├── CLAUDE.md                    ← Orchestrator (<200 lines)
├── .claude/
│   ├── agents/
│   │   ├── explorer.md          ← Research specialist
│   │   ├── platform-engineer.md ← Research specialist
│   │   ├── architect.md         ← Planning specialist
│   │   ├── planner.md           ← Planning specialist
│   │   ├── implementer.md       ← Implementation specialist
│   │   └── [custom-agents].md   ← Your domain specialists
│   ├── skills/
│   │   └── [reusable procedures]
│   └── WORKFLOW_STATUS.md       ← Phase tracking (optional)
├── docs/
│   ├── adr/                     ← Architecture decisions
│   └── guides/                  ← Implementation guides
└── [rest of codebase]
```

---

## Quick Validation Test

**Test Your CloudMD in 10 Minutes**:

1. **Read Test** (2 min): Can someone unfamiliar understand the three phases?
2. **Agent Test** (3 min): Are available agents clearly listed?
3. **Checklist Test** (2 min): Does each phase have exit criteria?
4. **Size Test** (1 min): Is the file <200 lines?
5. **Delegation Test** (2 min): Run one research query; does it route to the right agent?

**Pass**: 5/5 tests
**Needs Work**: <5/5 tests

---

## Next Steps After Setup

1. **Week 1**: Test with small research tasks
2. **Week 2**: Run full Research → Plan → Implement cycle
3. **Week 3**: Measure context usage; adjust compaction triggers
4. **Week 4**: Get team feedback; refine checklists
5. **Ongoing**: Iterate based on real usage

---

## Key Takeaways (Remember These)

1. **40% Rule**: Compact before you hit the Dumb Zone
2. **Code Truth**: Read source code, not docs
3. **Code Snippets**: Plans must prove understanding
4. **One-Read Rule**: Read once, delegate immediately
5. **Mental Alignment**: Plans coordinate the team
6. **Domain Routing**: Match agent to domain, not role
7. **Frequent Compaction**: Restart threads to stay fresh

---

**Your orchestrator is a living system. Start simple, iterate based on real usage, and refine with each project.**
