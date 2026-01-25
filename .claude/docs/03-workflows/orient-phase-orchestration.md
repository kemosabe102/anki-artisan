# ORIENT Phase Orchestration Workflow

**Purpose**: Complete guide for parallel agent spawning during ORIENT phase when Context_Quality is uncertain or agent selection is ambiguous.

**Last Updated**: 2025-11-24

**Applies To**: Claude Code orchestrator (primary), context-readiness-assessor (coordination)

---

## Quick Reference

**Trigger**: PATH 1 fails (ASC <0.5) | PATH 2 ambiguous (3+ ties) | Self-assess CQ <0.7 | Security keywords

**Pattern**: Spawn 2-4 agents in parallel → Consolidate CQ scores → Gate decision (≥0.85 proceed | <0.85 iterate)

**Duration**: 60-120s per iteration (2-4 agents parallel)

**Exit**: Success (CQ ≥0.85) | Iterate (Δ_CQ ≥0.05) | Escalate (3 rounds or Δ_CQ <0.05)

---

## When to Use Discovery Pattern

### Trigger Conditions (Use ANY)

1. **PATH 1 Failure**: All agent ASC scores <0.5
   - Example: "Implement blockchain smart contract validation" → No agent domain match
   - Why: Need exploration to understand requirements before selecting agent

2. **PATH 2 Ambiguity**: 3+ agents tie with ASC 0.5-0.7
   - Example: "Add caching layer" → Could be development, architecture, OR tech-debt-investigator
   - Why: Multiple valid approaches, need context to disambiguate

3. **Self-Assessment Low**: Orchestrator's own CQ estimate <0.7
   - Example: "Optimize database queries" → Unfamiliar with current DB architecture
   - Why: High uncertainty in own understanding, need validation

4. **Security-Critical**: Keywords detected
   - Keywords: "auth", "authentication", "authorization", "payment", "crypto", "security", "credentials", "token", "session"
   - Example: "Add JWT token refresh flow"
   - Why: Security tasks require thorough context gathering (failure modes, attack vectors)

### Anti-Triggers (Do NOT Use)

- ❌ PATH 1 success (clear agent ASC ≥0.8) → Use that agent directly
- ❌ Simple file edits (typos, formatting, comments) → Direct execution
- ❌ CLAUDE.md modifications → Direct execution (special case)
- ❌ Research-only tasks → Delegate to researcher-lead (not Discovery Pattern)

---

## Discovery Pattern Workflow

### Phase 1: Spawn Exploration Agents (Parallel)

**Minimum Configuration** (2 agents):
```
1. context-readiness-assessor (ALWAYS) - Primary CQ calculator
2. researcher-codebase - Find existing patterns in local code
```

**Standard Configuration** (3-4 agents):
```
1. context-readiness-assessor (ALWAYS)
2. 2-3 domain specialists with ASC 0.4-0.7 (highest-confidence agents even if below threshold)
3. researcher-codebase (if local patterns needed)
```

**Maximum Configuration** (5 agents, reserve for complex/security-critical):
```
1. context-readiness-assessor (ALWAYS)
2. 2-3 domain specialists (ASC 0.4-0.7)
3. researcher-codebase (local patterns)
4. contingency-planner (risk assessment for novel approaches)
5. researcher-external (external best practices) [auto-routes Context7 vs Perplexity]
```

**Launch Pattern** (single message, parallel execution):
```python
# Pseudocode for orchestrator
Task(context-readiness-assessor,
     "Assess context readiness for [task]. Return 4-component CQ score.")
Task(code-quality,
     "From Python domain perspective, assess understanding for [task].")
Task(researcher-codebase,
     "Find existing patterns for [task] in packages/ and tests/.")
```

### Phase 2: Consolidate CQ Scores

**Agents Return Results**:
```
context-readiness-assessor: CQ=0.82, breakdown=[D:0.78, P:0.85, Dep:0.80, R:0.85]
code-quality: CQ=0.88 (Python patterns familiar)
researcher-codebase: CQ=0.79 (found 3 similar implementations)
```

**Apply Weighted Average** (primary method):
```
CQ_consolidated = (0.50 × 0.82) + (0.35 × [(0.88+0.79)/2]) + (0.15 × N/A)
                = 0.410 + 0.292 + 0.0
                = 0.702 (no researcher-lead present, redistribute weight)

Adjusted formula when researcher-lead absent:
CQ_consolidated = (0.55 × 0.82) + (0.45 × 0.835)
                = 0.451 + 0.376
                = 0.827 (<0.85 → ITERATE)
```

**Consensus Check**:
- Range: 0.88 - 0.79 = 0.09 (Strong consensus, scores within 0.10)
- Decision: Iterate (CQ close to threshold, consensus suggests targeted research will succeed)

### Phase 3: Gate Decision

**Decision Matrix**:

| CQ Score | Consensus | Action | Rationale |
|----------|-----------|--------|-----------|
| ≥0.85 | Strong (±0.10) | **PROCEED to DECIDE** | High confidence, all agents agree |
| ≥0.85 | Weak (>0.20) | **ITERATE** (1 agent) | Scores diverge, resolve conflict first |
| 0.70-0.84 | Any | **ITERATE** (1-2 agents) | Near threshold, targeted research likely to cross |
| <0.70 | Any | **ESCALATE** if Round 1, else **ITERATE** | Significant gaps, may need multiple rounds |

**Exit Conditions**:
- ✅ **Success**: CQ ≥0.85 with strong consensus → Proceed to DECIDE phase
- 🔄 **Iterate**: CQ 0.70-0.84 OR weak consensus → Spawn targeted follow-up agents (max 3 iterations)
- ⚠️ **Escalate**: 3 iterations reached OR Δ_CQ <0.05 (diminishing returns) → Inform user of gaps, request clarification

### Phase 4: Iterative Refinement (If Needed)

**Iteration Strategy**:

**Round 1** (Broad Exploration):
- 3-4 agents, diverse perspectives
- Goal: Understand problem space, identify major gaps
- Output: CQ breakdown by dimension (D, P, Dep, R)

**Round 2** (Targeted Research):
- 1-2 agents addressing lowest-scoring dimension from Round 1
- Example: If Domain=0.65 (lowest), spawn researcher-external for specific library docs
- Goal: Address specific knowledge gaps
- Output: Updated CQ with improvements in target dimension

**Round 3** (Final Validation):
- 1 agent: context-readiness-assessor only
- Goal: Verify all improvements, recalculate holistic CQ
- Output: Final gate decision (proceed or escalate)

**Diminishing Returns Detection**:
```
Δ_CQ = CQ_round_n - CQ_round_(n-1)

If Δ_CQ < 0.05:
  → Marginal improvement, unlikely to reach 0.85
  → ESCALATE to user (explain gaps, request clarification)
```

**Example Iteration Flow**:
```
Round 1: CQ=0.72 [D:0.65, P:0.75, Dep:0.78, R:0.70] → Domain lowest
→ Spawn researcher-external: "Research Python asyncio patterns for task queue"

Round 2: CQ=0.83 [D:0.80, P:0.75, Dep:0.78, R:0.82] → Pattern still low
→ Spawn researcher-codebase: "Find existing task queue implementations in packages/"

Round 3: CQ=0.88 [D:0.82, P:0.90, Dep:0.85, R:0.85] → SUCCESS
→ Proceed to DECIDE phase with domain specialist agents
```

---

## Cost Optimization Strategies

### Minimize Agent Count

**Prefer 2-3 agents over 4-5** unless:
- Security-critical (auth, payment, crypto)
- Novel domain (no existing patterns)
- User explicitly requests thorough analysis

**Cost Breakdown**:
- 2 agents: ~60s latency, ~4K tokens
- 3 agents: ~75s latency, ~6K tokens
- 4 agents: ~90s latency, ~8K tokens
- 5 agents: ~120s latency, ~10K tokens

### Research Tool Selection

**Context7 FIRST** (free, authoritative):
- researcher-external (Context7 + Perplexity, auto-routes)
- researcher-codebase (local files)

**Perplexity SECOND** (paid, use when Context7 insufficient):
- researcher-external (unified external research)
- Only spawn if Context7 confidence <0.8 OR 2+ failures

**Target Ratio**: 4:1 (Context7:Perplexity)

### Iteration Thresholds

**Aggressive** (minimize iterations):
- Threshold: CQ ≥0.80 (instead of 0.85)
- When: Non-security-critical, familiar domains
- Risk: May miss edge cases

**Conservative** (standard):
- Threshold: CQ ≥0.85
- When: Default for most tasks
- Balance: Quality vs. speed

**Paranoid** (maximize context):
- Threshold: CQ ≥0.90 + strong consensus
- When: Security-critical, high-risk changes
- Cost: +1-2 iterations typically

---

## Example Scenarios

### Scenario 1: Security Keyword Trigger

**User Request**: "Add OAuth2 authentication to API endpoints"

**OBSERVE**: Security keyword "OAuth2" detected

**ORIENT Discovery** (spawn 4 agents parallel):
```
1. context-readiness-assessor: Assess CQ for OAuth2 implementation
2. code-quality: Evaluate from Python security perspective
3. researcher-codebase: Find existing auth patterns in packages/
4. researcher-external: Research "Python OAuth2 best practices"
```

**Results**:
- context-readiness-assessor: CQ=0.81 [D:0.85, P:0.75, Dep:0.82, R:0.78]
- code-quality: CQ=0.86
- researcher-codebase: CQ=0.78 (found 1 basic auth example)
- researcher-external: CQ=0.84

**Consolidate**: CQ = 0.823 (<0.85)

**Iterate** (Round 2, address Pattern + Risk gaps):
```
1. researcher-external: "OAuth2 attack vectors and security pitfalls"
2. researcher-external: "Python security libraries for OAuth2 (authlib, oauthlib)"
```

**Round 2 Results**: CQ = 0.89 → PROCEED to DECIDE

**Decision Time**: ~150s (2 rounds), 6 agents total

---

### Scenario 2: PATH 1 Failure (No Clear Agent)

**User Request**: "Optimize GraphQL query performance"

**OBSERVE**: Task type = optimization, domain = GraphQL

**PATH 1 Attempt**: Evaluate all agents
- development: ASC=0.42 (knows Python, unfamiliar with GraphQL)
- debugger: ASC=0.38 (performance expertise, no GraphQL)
- tech-debt-investigator: ASC=0.35 (code quality, not GraphQL-specific)

**All ASC <0.5 → ORIENT Discovery**

**Spawn 3 agents**:
```
1. context-readiness-assessor: Assess CQ for GraphQL optimization
2. researcher-codebase: Find existing GraphQL implementations
3. researcher-external: "GraphQL query optimization best practices"
```

**Results**: CQ = 0.88 → PROCEED to DECIDE

**DECIDE** (with context):
- Now understand GraphQL usage in codebase (found `packages/api/graphql/`)
- Select development (ASC now 0.72 with context) + architecture (0.68)
- Delegate optimization task with research findings

---

### Scenario 3: PATH 2 Ambiguity (Multiple Agents Tie)

**User Request**: "Add Redis caching layer"

**OBSERVE**: Task = new feature, domain = caching/infrastructure

**PATH 2 Attempt**: 3 agents tie
- development: ASC=0.65 (Python implementation)
- architecture: ASC=0.68 (infrastructure decision)
- tech-debt-investigator: ASC=0.62 (performance optimization context)

**3+ agents within 0.5-0.7 → ORIENT Discovery**

**Spawn 2 agents**:
```
1. context-readiness-assessor: Assess readiness for Redis integration
2. researcher-codebase: Find existing caching patterns
```

**Results**:
- context-readiness-assessor: CQ=0.91, recommends architecture FIRST (validate approach)
- researcher-codebase: Found in-memory caching in `packages/core/cache.py`

**DECIDE** (sequential delegation):
1. architecture: Validate Redis vs alternatives (returns: Redis approved)
2. development: Implement Redis client + integration

---

## Anti-Patterns

### ❌ Over-Using Discovery Pattern

**Problem**: Spawning agents for simple tasks that PATH 1 resolves

**Example**:
```
User: "Fix typo in claude-code-ecosystem.md"
❌ BAD: Spawn 4 agents to assess context
✅ GOOD: PATH 1 → claude-code-ecosystem (ASC=0.92) → Delegate immediately
```

**Cost**: 90s wasted, 8K unnecessary tokens

---

### ❌ Under-Consolidating (Using First Agent's Score)

**Problem**: Only using context-readiness-assessor's score, ignoring domain specialists

**Example**:
```
context-readiness-assessor: CQ=0.78
code-quality: CQ=0.90 (Python patterns very familiar)

❌ BAD: Use 0.78 → Iterate unnecessarily
✅ GOOD: Consolidate to 0.84 → Consider iteration (close to 0.85)
```

---

### ❌ Infinite Iteration Loop

**Problem**: Continuing to iterate even when Δ_CQ <0.05

**Example**:
```
Round 1: CQ=0.78
Round 2: CQ=0.81 (Δ=0.03)
Round 3: CQ=0.82 (Δ=0.01) ← Diminishing returns

❌ BAD: Round 4 (unlikely to improve)
✅ GOOD: ESCALATE after Round 3 (explain gaps to user)
```

---

### ❌ Skipping Consensus Check

**Problem**: Proceeding with CQ=0.86 when scores range [0.68, 0.95]

**Example**:
```
Weighted avg: CQ=0.86 (meets threshold)
But: context-readiness-assessor=0.68, researcher-external=0.95

❌ BAD: Proceed (fundamental disagreement masked by averaging)
✅ GOOD: Iterate to resolve conflict (why does CRA see major gaps?)
```

---

## Integration with OODA Loop

**Full OODA Flow with Discovery**:

```
OBSERVE:
├─ Parse user request
├─ Identify domain/task type
├─ Extract constraints
└─ Check security keywords → [Trigger if found]

ORIENT:
├─ Self-assess CQ (rough estimate)
├─ IF CQ <0.7 OR security keyword:
│   ├─ Spawn Discovery agents (2-4 parallel)
│   ├─ Consolidate CQ scores
│   ├─ Gate decision (≥0.85 proceed | <0.85 iterate)
│   └─ Iterate up to 3 rounds if needed
└─ ELSE: Continue with PATH 1/2/3

DECIDE:
├─ Evaluate ALL agent descriptions
├─ Calculate ASC for each
├─ IF all ASC <0.5: Return to ORIENT Discovery
├─ ELSE: Select agents (ASC ≥0.8 use all, 0.5-0.79 use highest)
└─ Prepare delegation strategy

ACT:
├─ Delegate to selected agent(s)
├─ Track with TodoWrite
├─ Verify results
└─ Iterate if confidence <0.85
```

---

## See Also

- **CQ Consolidation**: `.claude/docs/01-guides/orchestration/orient-research-coordination.md` (complete consolidation algorithm)
- **Agent Selection**: `.claude/docs/01-guides/agents/agent-selection-guide.md` (PATH 1/2/3 frameworks)
- **Research Coordination**: `.claude/docs/01-guides/research/research-trigger-patterns.md` (when to trigger research)
- **OODA Framework**: `orchestrator-workflow.md` (complete OODA loop methodology)

---

**Status**: ACTIVE | **Version**: 1.0.0 | **Last Updated**: 2025-11-24
