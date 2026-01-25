# CloudMD Visual Guide & Mental Models
## Diagrams, Flows, and Decision Trees

---

## 1. The Three-Phase OODA Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      USER REQUEST                             │
│         "Build real-time notification system"                 │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────────────┐
         │      CLOUDMD ORCHESTRATOR               │
         │   (Read-Only Coordinator, <200 lines)  │
         │                                         │
         │  • Routes to domain specialists        │
         │  • Preserves context via delegation    │
         │  • Stays in Smart Zone (<40% usage)    │
         │  • Compacts and restarts as needed     │
         └────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ PHASE 1  │   │ PHASE 2  │   │ PHASE 3  │
   │ RESEARCH │   │   PLAN   │   │IMPLEMENT │
   │          │   │          │   │          │
   │ (Observe)│   │ (Orient/ │   │  (Act)   │
   │          │   │  Decide) │   │          │
   └──────────┘   └──────────┘   └──────────┘
```

---

## 2. Phase 1: Research (OODA: Observe)

```
┌─────────────────────────────────────────────────────────┐
│              PHASE 1: RESEARCH (OBSERVE)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CloudMD selects domain-appropriate specialist:        │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Explorer      │  │   Platform      │            │
│  │   Agent         │  │   Engineer      │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Backend       │  │   Frontend      │            │
│  │   Specialist    │  │   Specialist    │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  Agent investigates (fresh context):                   │
│    • Reads SOURCE CODE (not docs)                     │
│    • Maps dependencies                                 │
│    • Identifies gaps                                   │
│    • Lists constraints                                 │
│                                                         │
│  Returns to CloudMD:                                   │
│    ✓ research_summary.md                              │
│    ✓ Key facts with file:line references             │
│    ✓ Gaps identified                                   │
│    ✓ Recommended next steps                           │
│                                                         │
│  Exit Checklist:                                       │
│  ☑ Scope clarity     ☑ Code truth (not docs)         │
│  ☑ Current state     ☑ Dependencies mapped            │
│  ☑ Gaps listed       ☑ Context compacted              │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Phase 2: Planning (OODA: Orient + Decide)

```
┌─────────────────────────────────────────────────────────┐
│          PHASE 2: PLAN (ORIENT + DECIDE)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CloudMD selects planning specialist:                  │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Architect     │  │    Planner      │            │
│  │   Agent         │  │    Agent        │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Design        │  │   Data          │            │
│  │   Reviewer      │  │   Architect     │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  Agent designs (fresh context + research summary):     │
│    • Evaluates options                                 │
│    • Documents trade-offs                              │
│    • Creates phased roadmap                            │
│    • Includes CODE SNIPPETS (signatures/interfaces)   │
│    • Assesses risks                                    │
│                                                         │
│  Returns to CloudMD:                                   │
│    ✓ implementation_plan.md                           │
│    ✓ Approach justification                           │
│    ✓ Trade-off analysis                               │
│    ✓ CODE SNIPPETS proving understanding              │
│    ✓ Phased roadmap with verification                 │
│                                                         │
│  Exit Checklist:                                       │
│  ☑ Approach justified    ☑ Code snippets included    │
│  ☑ Trade-offs clear      ☑ Phases sequenced           │
│  ☑ Risks assessed        ☑ Human approval obtained    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   APPROVAL GATE       │
              │   (Human Review)      │
              └───────────────────────┘
```

---

## 4. Phase 3: Implementation (OODA: Act)

```
┌─────────────────────────────────────────────────────────┐
│           PHASE 3: IMPLEMENT (ACT)                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CloudMD selects implementation specialist:            │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │  Implementer    │  │    Builder      │            │
│  │     Agent       │  │     Agent       │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Validator     │  │   Refactorer    │            │
│  │     Agent       │  │     Agent       │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  For EACH phase in roadmap:                            │
│                                                         │
│  Agent implements (fresh context + plan):              │
│    • Builds according to code snippets                 │
│    • Writes tests                                      │
│    • Validates against success criteria               │
│    • Reports blockers immediately                      │
│                                                         │
│  Returns to CloudMD (per phase):                       │
│    ✓ phase_N_report.md                                │
│    ✓ Changes made (with files)                        │
│    ✓ Tests passed (with evidence)                     │
│    ✓ Blockers (if any)                                │
│    ✓ Ready for next phase? (Y/N)                      │
│                                                         │
│  Exit Checklist (per phase):                           │
│  ☑ Code quality      ☑ Snippets match plan           │
│  ☑ Tests passing     ☑ Blockers resolved              │
│  ☑ Docs updated      ☑ Stakeholders notified          │
└─────────────────────────────────────────────────────────┘
```

---

## 5. The Smart Zone vs. Dumb Zone

```
Context Window: 200,000 tokens (Claude 3.5 Sonnet)

┌─────────────────────────────────────────────────────────┐
│  0%                                                      │
│  ├──────────────────────────────────────────────────    │
│  │                                                       │
│  │          SMART ZONE                                  │
│  │       (High-quality reasoning)                       │
│  │                                                       │
│  │   • Agent makes smart decisions                      │
│  │   • Tool selection accurate                          │
│  │   • Context used efficiently                         │
│  │   • Minimal hallucination                            │
│  │                                                       │
│ 40%  ← ← ← ← ← DANGER LINE ← ← ← ← ←                   │
│  ├──────────────────────────────────────────────────    │
│  │                                                       │
│  │          DUMB ZONE                                   │
│  │      (Degraded performance)                          │
│  │                                                       │
│  │   • Agent makes poor choices                         │
│  │   • Starts repeating itself                          │
│  │   • Hallucinations increase                          │
│  │   • Quality drops significantly                      │
│  │                                                       │
│100%                                                      │
└─────────────────────────────────────────────────────────┘

STRATEGY: Stay in Smart Zone via:
  1. One-Read Rule (minimal upfront reading)
  2. Aggressive delegation (offload to specialists)
  3. Frequent compaction (restart at phase boundaries)
  4. Context monitoring (track usage actively)
```

---

## 6. The Compaction Loop (Staying Fresh)

```
WITHOUT COMPACTION (Degrading):
───────────────────────────────────────────────────────
Turn 0:  ████░░░░░░░░░░░░░░░░  (Fresh, 10% context)
Turn 10: ████████████░░░░░░░░  (Good, 30% context)
Turn 20: ████████████████████  (Danger, 50% context)
Turn 30: ████████████████████  (Dumb Zone, 60%)
Turn 40: ████████████████████  (Poor results, 70%)


WITH COMPACTION (Always Fresh):
───────────────────────────────────────────────────────
Phase 1 (Research):
Turn 0:  ████░░░░░░░░░░░░░░░░  (Fresh)
Turn 15: ████████████░░░░░░░░  (30%)
         ↓ COMPACT → research_summary.md
         ↓ RESTART thread

Phase 2 (Planning):
Turn 0:  ████░░░░░░░░░░░░░░░░  (Fresh + summary)
Turn 12: ██████████░░░░░░░░░░  (25%)
         ↓ COMPACT → implementation_plan.md
         ↓ RESTART thread

Phase 3 (Implement):
Turn 0:  ████░░░░░░░░░░░░░░░░  (Fresh + plan)
Turn 18: ██████████████░░░░░░  (35%)
         ↓ COMPACT → phase_checkpoint.md
         ↓ RESTART thread

[Always operating in Smart Zone!]
```

---

## 7. Agent Selection Decision Tree

```
                    ┌─────────────────────┐
                    │   USER REQUEST      │
                    └──────────┬──────────┘
                               │
                               ▼
                ┌──────────────────────────┐
                │ CloudMD: ONE strategic   │
                │ read to understand       │
                │ (max 5 files)            │
                └────────┬─────────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │ Which PHASE is needed? │
                └─┬──────────┬───────────┬┘
                  │          │           │
            RESEARCH     PLAN      IMPLEMENT
                  │          │           │
                  ▼          ▼           ▼
        ┌─────────────┐ ┌─────────┐ ┌─────────────┐
        │Which DOMAIN?│ │ Design  │ │What needs   │
        │             │ │ type?   │ │ building?   │
        └──┬──────────┘ └────┬────┘ └──────┬──────┘
           │                 │              │
    ┌──────┼──────┐         ▼              ▼
    ▼      ▼      ▼         
┌───────┐ ┌────┐ ┌────┐  System    Backend  Frontend
│Infra  │ │API │ │UI  │  Arch      Builder  Builder
│(Platf)│ │(BE)│ │(FE)│  ↓          ↓        ↓
└───────┘ └────┘ └────┘  Architect  Implement Implement
    ↓       ↓      ↓      Agent     Agent     Agent
Platform  Backend Frontend
Engineer  Explorer Specialist
Agent     Agent    Agent
```

---

## 8. Code Truth vs. Documentation Slop

```
TRADITIONAL APPROACH (Unreliable):
──────────────────────────────────────
CloudMD → reads docs/architecture.md
       → "System uses polling"
       → Plans based on docs
       → Implements based on docs
       → SURPRISE: Docs are 2 years old!
       → Actual code uses WebSocket
       → Wasted time, wrong solution


CODE TRUTH APPROACH (Reliable):
──────────────────────────────────────
CloudMD → delegates to Explorer
Explorer → reads src/notification/service.ts
        → finds actual implementation
        → "Currently: setInterval polling"
        → "Available: WebSocket infrastructure"
CloudMD → receives TRUTH from source code
       → Plans based on reality
       → Implements correctly
       → SUCCESS: Solution matches reality
```

**Rule**: Documentation is "slop" (often outdated). Code is truth.

---

## 9. Plans as Mental Alignment Tool

```
TRADITIONAL CODE REVIEW:
────────────────────────────────────────────────
Developer codes 1000 lines
    ↓
Reviewer reads 1000 lines (2-4 hours)
    ↓
Finds architectural issues
    ↓
Request changes (expensive rework)
    ↓
Repeat


PLAN-FIRST REVIEW:
────────────────────────────────────────────────
Planner creates 50-line plan with code snippets
    ↓
Reviewer reads plan (10 minutes)
    ↓
Finds architectural issues IN DESIGN
    ↓
Plan revised (cheap iteration)
    ↓
Approved plan → Implementer codes 1000 lines
    ↓
Reviewer checks: Does it match the plan?
    ↓
Merge (fast, high confidence)


BENEFIT: Catch issues at design time (cheap)
         Not at code review time (expensive)
```

---

## 10. The Plan Detail Trade-Off Curve

```
                    Reliability
                         ↑
                         │
                         │        ╱╲
                         │       ╱  ╲
                         │      ╱    ╲  ← Sweet Spot
                         │     ╱      ╲    (Readable +
                         │    ╱        ╲     Executable)
                         │   ╱          ╲
                         │  ╱            ╲
                         │ ╱              ╲
    Too Vague →          │╱                ╲  ← Too Detailed
    (unreliable)         ┼──────────────────╲ (unreadable)
                         └────────────────────→
                              Plan Detail


FINDING YOUR SWEET SPOT:

Too Vague:
  "Phase 1: Build notification service"
  Problem: Implementer has to guess everything

Good (Sweet Spot):
  "Phase 1: Build notification service
   Files: src/notification/service.ts
   
   interface NotificationService {
     send(userId: string, msg: Message): Promise<void>;
     subscribe(userId: string, cb: Handler): Subscription;
   }
   
   Tests: Unit test send(), integration test subscribe()"

Too Detailed:
  [30 pages of pseudocode with every function implementation]
  Problem: Nobody will read it; loses benefit
```

---

## 11. Context Budget Visualization

```
Total Context: 200,000 tokens (Claude 3.5 Sonnet)

RECOMMENDED ALLOCATION:
┌────────────────────────────────────────────────────┐
│ CloudMD Permanent (~1,200 tokens)                  │
│  ├─ Role definition (500)                          │
│  ├─ Agent list (300)                               │
│  └─ Phase structure (400)                          │
├────────────────────────────────────────────────────┤
│ Working Memory (~2,300 tokens)                     │
│  ├─ Current phase context (2,000)                  │
│  └─ File references (300)                          │
├────────────────────────────────────────────────────┤
│ SMART ZONE (~80,000 tokens = 40% of total)        │
│  └─ Available for high-quality work               │
├────────────────────────────────────────────────────┤
│ Conversation History (remaining)                   │
│  └─ Task-specific interaction                      │
└────────────────────────────────────────────────────┘

DANGER: If you exceed ~80k tokens used:
  → Entering Dumb Zone
  → Quality degrades
  → Compact and restart NOW
```

---

## 12. Blocker Escalation Flow

```
Phase 3: Implementation
        │
        ▼
Implementer working on Phase 2
        │
        ▼
    ┌─────────────────────────┐
    │   BLOCKER DETECTED      │
    │ "WebSocket drops at 10k"│
    └─────────┬───────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │ Report to CloudMD       │
    │ "Blocker in Phase 2"    │
    └─────────┬───────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │ CloudMD: "Consult        │
    │ architect on options"   │
    └─────────┬───────────────┘
              │
              ▼
    Delegate to Architect:
    "WebSocket drops at 10k load.
     Options:
       A) Async I/O refactor (20h, correct)
       B) Connection pooling (4h, temporary)"
              │
              ▼
    Architect returns trade-offs
              │
              ▼
    ┌─────────────────────────┐
    │ CloudMD escalates to    │
    │ HUMAN for decision      │
    └─────────┬───────────────┘
              │
              ▼
    Human: "Go with B for now"
              │
              ▼
    CloudMD delegates revised task:
    "Implement connection pooling (4h)"
              │
              ▼
    Implementer completes revised Phase 2
              │
              ▼
    Continue to Phase 3
```

---

## 13. When to Use Each Rigor Level

```
COMPLEXITY SCALE:
─────────────────────────────────────────────────────

Trivial     Simple      Medium      Complex    Critical
  │           │           │            │          │
  ▼           ▼           ▼            ▼          ▼
                                                   
No phases   Quick       R+P+I      Deep R+P+I   Multi-domain
  │         context     Standard   Detailed     R+P+I with
  │           │         flow       snippets     reviews
  ▼           ▼           ▼            ▼          ▼

"Change    "Add form   "New API   "Refactor   "Migrate
 button     field"      endpoint"  auth"       database"
 color"

Examples:
─────────────────────────────────────────────────────

Trivial:
  • Research: None
  • Plan: None
  • Implement: Direct instruction
  
Simple:
  • Research: 5-min context check
  • Plan: Informal (verbal)
  • Implement: Standard

Medium:
  • Research: Focused (one domain)
  • Plan: Structured with phases
  • Implement: Phase-gated

Complex:
  • Research: Deep (multiple domains)
  • Plan: Detailed + code snippets
  • Implement: Multi-phase validation

Critical:
  • Research: Multi-specialist
  • Plan: Architecture review
  • Implement: Staged rollout + monitoring
```

---

## 14. Session Pattern Example (All 3 Phases)

```
TIME     CLOUDMD                        SPECIALIST
──────────────────────────────────────────────────────
0:00   User: "Build notification system"
       │
       ▼
0:01   ONE-READ: glob src/notification/*
       Found: polling-based system
       │
       ▼ DELEGATE TO EXPLORER
       "Research notification architecture"
       │                                  ┌─────────────
       │                                  │ Reads code
       │                                  │ Maps deps
0:05   │                                  │ Identifies
       │                                  │ gaps
       │                                  └─────────────
       ▼ RECEIVES                         Returns:
       research_summary.md               • Polling today
       • WebSocket exists                • Can upgrade
       • 15k users affected              
       │
       ▼ COMPACT & RESTART (fresh thread)
       │
0:06   Load: research_summary.md only
       │
       ▼ DELEGATE TO ARCHITECT
       "Design real-time system"
       │                                  ┌─────────────
       │                                  │ Evaluates
       │                                  │ options
0:12   │                                  │ Creates
       │                                  │ roadmap +
       │                                  │ snippets
       │                                  └─────────────
       ▼ RECEIVES                         Returns:
       implementation_plan.md            • 3 phases
       • Code snippets                   • 40h estimate
       • Trade-offs                      • Risks
       │
       ▼ HUMAN APPROVAL GATE
       User: "Approved"
       │
       ▼ COMPACT & RESTART (fresh thread)
       │
0:15   Load: implementation_plan.md only
       │
       ▼ DELEGATE TO IMPLEMENTER
       "Build Phase 1: Event system"
       │                                  ┌─────────────
       │                                  │ Codes
       │                                  │ Tests
0:25   │                                  │ Validates
       │                                  └─────────────
       ▼ RECEIVES                         Returns:
       phase_1_report.md                 • PASS
       Tests passing ✓                   
       │
       ▼ DELEGATE: Phase 2
       │
0:35   ▼ RECEIVES: Phase 2 PASS ✓
       │
       ▼ DELEGATE: Phase 3
       │
0:45   ▼ RECEIVES: Phase 3 PASS ✓
       │
       ▼ PROJECT COMPLETE
       All phases verified ✓
```

**Key**: Context stayed fresh via compaction at phase boundaries.

---

**End of Visual Guide**

These diagrams provide visual mental models for understanding and explaining the CloudMD orchestration pattern. Use them for onboarding, debugging, and team alignment.
