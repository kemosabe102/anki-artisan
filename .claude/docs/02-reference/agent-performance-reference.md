# Agent Performance Reference

**Purpose**: Performance optimization strategies, tier definitions, and delegation rules

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Performance Tier Definitions

### 🟢 Fast Agents (<30s startup)

**Characteristics**:
- Read-only operations (Read, Grep, Research tools)
- No file mutations (no Edit/Write/Bash)
- Rapid context assessment
- Quick feedback loops

**Agents**:
- **planning** (B+): Quality assessment, ambiguity detection
- **planning** (A): Business alignment review, NFR assessment, structured reporting

**Use Cases**:
- Initial analysis before enhancements
- Rapid quality checks
- Business alignment validation
- First-pass review

**Optimization Strategy**: Prefer fast agents for initial assessment, then delegate to medium-tier agents for modifications.

---

### 🟡 Medium Agents (1-2min startup)

**Characteristics**:
- File modification capabilities (Edit/Write tools)
- Research + enhancement workflows
- Context7 research integration
- Targeted file operations

**Agents**:
- **planning** (B+): Business context enhancement
- **architecture** (B+): Technical design addition
- **architecture** (B+): Technical validation with Edit Plans

**Use Cases**:
- Content enhancement
- Placeholder replacement
- Technical design population
- Quality-driven file modifications

**Optimization Strategy**: Use for targeted modifications after fast agent assessment confirms need.

---

### 🔴 Slow Agents (3+min startup)

**Status**: None remaining after performance optimizations

**Historical Context**:
- planning: 5min → <30s (70% reduction via Read+Grep+Research only)
- architecture: 3min → 1-2min (70% reduction via review-only pattern)

---

## Performance Optimization Strategies

### Strategy 1: Review-Only Pattern

**Principle**: Separate review from enhancement for faster feedback

**Implementation**:
1. **Review agents** (planning, planning, architecture): Read+Grep+Research only
2. **Enhancement agents** (planning, architecture): Add Edit/Write tools
3. **Handoff**: Review agents generate Edit Plans for enhancement agents

**Benefits**:
- 70% startup time reduction
- Faster feedback loops
- Clear separation of concerns
- Parallel review + sequential enhancement

**Example**:
```
# Before optimization (sequential, 7min total):
planning (5min) → edits files

# After optimization (parallel + sequential, 2.5min total):
planning review (30s) + planning (30s) [parallel]
→ Handoff Edit Plan
→ planning (1.5min) edits files
```

---

### Strategy 2: Parallel Independent Work

**Principle**: Launch multiple agents for independent files simultaneously

**Scaling**:
- **File Modifications**: MAX 5 agents (approval management, file system constraints)
- **Research Workers**: MAX 5 agents (read-only, parallel safe)
- **Review Agents**: 3-5 optimal, MAX 10 allowed
- **Practical Limit**: 15-20 agents total

**Performance**: Linear scaling (5 components = 5x faster)

**Example**:
```python
# Single message with 3 parallel tasks (2min instead of 6min):
Task(agent="planning", prompt="Enhance core-PLAN.md")
Task(agent="planning", prompt="Enhance analysis-PLAN.md")
Task(agent="planning", prompt="Enhance integration-PLAN.md")
```

**Critical Constraint**: Sequential execution MANDATORY for `.claude/**` directory (file locking)

---

### Strategy 3: Fast Agents First

**Principle**: Rapid feedback before expensive operations

**Workflow**:
1. **Fast review** (planning, planning): 30s assessment
2. **Validate need**: Check review findings
3. **If needed, enhance**: planning, architecture (1-2min)

**Benefits**:
- Avoid unnecessary enhancement work
- Early detection of quality issues
- User feedback before expensive operations
- Progress visibility (fast agents report first)

---

### Strategy 4: Targeted Research

**Principle**: Focus research on specific gaps, not broad exploration

**Implementation**:
- **Context_Quality assessment**: Identify specific dimension gaps (Domain/Pattern/Dependency/Risk)
- **Targeted delegation**: researcher-codebase for patterns, researcher-external for best practices
- **Compression**: 10:1 (codebase) to 15:1 (library) compression ratios

**Example**:
```
# Instead of:
"Research authentication patterns" (broad, 3-5min)

# Use:
"Find OAuth2 implementation in packages/auth/** matching our BaseService pattern" (targeted, <1min)
```

---

## Performance Wins Case Studies

### Case Study 1: planning (70% reduction)

**Before** (5min startup):
- Tools: Read, Grep, Write, Edit, Bash, Research
- Heavy tool loading overhead
- File mutation capabilities (unused)

**After** (<30s startup):
- Tools: Read, Grep, Research only
- 7 tools (removed Write, Edit, Bash)
- Zero file mutations
- Generates Business Review Reports + Edit Plans

**Impact**:
- 70% startup time reduction
- Faster business alignment feedback
- Parallel review capability
- No functionality loss (handoff to planning for edits)

---

### Case Study 2: architecture (70% reduction)

**Before** (3min startup):
- Tools: Read, Grep, Write, Edit, Research
- File modification capabilities
- Heavy tool loading

**After** (1-2min startup):
- Tools: Read, Grep, Research only
- 6 tools (removed Write, Edit)
- Review-only pattern
- Generates Technical Review Reports + Edit Plans

**Impact**:
- 70% startup time reduction
- Parallel technical validation
- Handoff to architecture for file modifications
- Clear review/enhancement separation

---

## Orchestrator Delegation Rules

### Rule 1: Fast Agents First for Analysis

**Pattern**: Prefer fast agents for initial assessment

```
User requests plan enhancement:
  ├─ FAST: planning review (30s) → Business Review Report
  ├─ FAST: planning (30s) → Quality assessment
  └─ MEDIUM: planning (1.5min) → Apply enhancements
```

**Rationale**: Rapid feedback, validate need before expensive operations

---

### Rule 2: Parallel for Independent Files

**Pattern**: Launch multiple enhancement agents simultaneously

```
Multiple component plans to enhance:
  ├─ Task(planning, "core-PLAN.md")
  ├─ Task(planning, "analysis-PLAN.md")
  └─ Task(planning, "integration-PLAN.md")
# Single message, 3x faster
```

**Exception**: Sequential MANDATORY for `.claude/**` modifications

---

### Rule 3: Sequential for `.claude/**`

**Pattern**: Never parallelize `.claude/**` directory modifications

**Rationale**: Windows file locking (99% Edit failure rate on parallel)

```
Modifying .claude/agents/*.md:
  ├─ claude-code-ecosystem: debugger.md → WAIT for completion
  └─ claude-code-ecosystem: code-quality.md → Start after previous completes
```

---

### Rule 4: Progress Feedback for >1min Agents

**Pattern**: Inform user during agent initialization

```
"Launching architecture for technical design (typically 1-2min)..."
```

**Rationale**: User awareness, manage expectations, reduce perceived latency

---

## Performance Monitoring

### Key Metrics

**Startup Time**:
- Fast: <30s
- Medium: 1-2min
- Slow: 3+min (target: eliminate)

**Throughput**:
- Sequential: N × time_per_agent
- Parallel: max(time_per_agent) for independent work
- Scaling factor: Linear up to MAX limits

**Tool Loading Overhead**:
- Each tool adds ~5-10s to startup
- Review-only: 6-7 tools optimal
- Enhancement: 8-10 tools acceptable

### Optimization Targets

**Primary**: Startup time <30s for 50% of agents
**Secondary**: Parallel capability for 80% of workflows
**Tertiary**: Zero 3+min agents

---

**This reference provides complete performance optimization guidance for orchestrator delegation decisions.**
