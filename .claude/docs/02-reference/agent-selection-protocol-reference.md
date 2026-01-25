# Agent Selection Protocol Reference

**Purpose**: Complete agent selection methodology with decision trees, frameworks, and anti-patterns

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Core Approach

**Principle**: Use framework-based reasoning for common patterns (80%), DCS calculation for novel scenarios (20%)

---

## Quick Decision Tree

```
User Request → Extract file paths → Identify domain(s)
  ↓
Domain Clear? (80% yes)
  ├─ YES → Apply Framework
  │   ├─ Single domain specialist → Immediate selection
  │   └─ Main codebase → Recognize work type → Select specialist
  │
  └─ NO (20%) → Calculate DCS
      ├─ Novel/unprecedented tasks
      ├─ Ambiguous domain boundaries
      ├─ Multiple agents equally qualified
      └─ High-stakes requiring justification
```

---

## Framework-Based Selection (80% of Cases)

### Framework 1: Domain-First Thinking

**Principle**: File path reveals domain → Domain determines specialist

**Domain Mapping**:

| File Path Pattern | Domain | Primary Agents |
|-------------------|--------|----------------|
| `.claude/agents/**` | Agent definitions | claude-code-ecosystem |
| `.claude/commands/**` | Command files | claude-code |
| `.claude/hooks/**` | Hook scripts | claude-code |
| `docs/**/SPEC.md` | Specifications | /spec command, planning |
| `docs/**/*-PLAN.md` | Plans | planning, architecture |
| `docs/**/tasks/**` | Tasks | planning |
| `packages/**/*.py` | Implementation | development, debugger |
| `tests/**/*.py` | Testing | code-quality, code-quality |
| `k8s/**/*.yaml` | Kubernetes | deployment-release |

**Decision Process**:
1. Extract file paths from user request
2. Map paths to domain using table above
3. Select specialist agent for that domain
4. If unclear, proceed to Framework 2

---

### Framework 2: Work Type Recognition

**Principle**: Within domain, what's the verb?

**Work Type Mapping** (for `packages/**` domain):

| Verb/Action | Work Type | Agent | Example |
|-------------|-----------|-------|---------|
| implement, create, build, add | Implementation | development | "Implement OAuth2 authentication" |
| debug, fix, investigate bug | Debugging | debugger | "Fix authentication token expiration bug" |
| test, validate, verify | Testing | code-quality (run), code-quality (generate) | "Run unit tests for auth module" |
| review, check, validate code | Review | code-quality | "Review auth module for security issues" |
| refactor, organize, clean | Refactoring | development | "Refactor auth module structure" |
| research, analyze, find | Research | researcher-codebase | "Find authentication patterns in codebase" |

**Decision Process**:
1. Domain identified (e.g., packages/**)
2. Extract verb from user request
3. Map verb to work type
4. Select specialist for work type within domain

---

### Framework 3: Disambiguation Principles

**When multiple agents seem applicable**, use priority order:

**Priority 1**: Domain Ownership (strongest signal)
- `.claude/agents/**` → claude-code-ecosystem (ALWAYS, regardless of work type)
- `docs/**/SPEC.md` → /spec command or planning (NOT development)

**Priority 2**: Closest Expertise (domain-specific knowledge)
- Test execution → code-quality (NOT debugger, even though both can run tests)
- Test generation → code-quality (NOT development)

**Priority 3**: Least Assumptions (reduce coupling)
- Generic implementation → development (NOT claude-code-ecosystem for main codebase)
- Documentation → documentation (NOT development)

**Example**:
```
Request: "Fix bug in .claude/agents/debugger.md"
Domain: .claude/agents/** → claude-code-ecosystem (Priority 1: Domain Ownership)
NOT debugger (wrong domain despite "debugger" in filename)
```

---

## DCS Calculation (20% of Cases)

### When to Use DCS

**Triggers**:
- Novel/unprecedented tasks without clear pattern
- Ambiguous domain boundaries (affects multiple domains)
- Multiple agents equally qualified
- High-stakes decisions requiring justification

**Formula**:
```
DCS = (Domain Match × 0.60) + (Work Type × 0.30) + (Track Record × 0.10)
```

**Thresholds**:
- High (0.7-1.0): Delegate immediately
- Medium (0.5-0.69): Delegate with monitoring
- Low (<0.5): Report to user + recommend agent creation

---

### DCS Component Scoring

**Domain Match (0.60 weight)**:
- 1.0 = Exact domain match (file path in agent's primary domain)
- 0.7-0.9 = Adjacent domain (related but not primary)
- 0.4-0.6 = Partial overlap (some relevant experience)
- 0.0-0.3 = No domain match

**Work Type (0.30 weight)**:
- 1.0 = Exact work type match (verb aligns with agent capability)
- 0.6-0.9 = Close match (related capability)
- 0.3-0.5 = Partial match (can do it but not primary strength)
- 0.0-0.2 = Work type mismatch

**Track Record (0.10 weight)**:
- 1.0 = Proven success in similar tasks
- 0.6-0.9 = Some success, minor issues
- 0.3-0.5 = Mixed results
- 0.0-0.2 = Frequent failures or untested

---

### DCS Example

**Request**: "Refactor authentication module in packages/auth/"

**Agent Option 1**: development
- Domain Match: 0.9 (packages/** is primary domain)
- Work Type: 0.8 (refactoring is close to implementation)
- Track Record: 0.7 (C+ grade, some issues)
- **DCS = (0.9 × 0.6) + (0.8 × 0.3) + (0.7 × 0.1) = 0.54 + 0.24 + 0.07 = 0.85** ✅

**Agent Option 2**: debugger
- Domain Match: 0.9 (packages/** is shared domain)
- Work Type: 0.4 (refactoring is NOT debugging)
- Track Record: 0.6 (C grade)
- **DCS = (0.9 × 0.6) + (0.4 × 0.3) + (0.6 × 0.1) = 0.54 + 0.12 + 0.06 = 0.72** ❌

**Decision**: development (higher DCS, better work type match)

---

## Anti-Patterns (What NOT to Do)

### ❌ Anti-Pattern 1: Defaulting to development

**Wrong**:
```
Request: "Update .claude/agents/debugger.md"
Selection: development (because it's a file edit)
```

**Why Wrong**: Ignores domain boundaries. `.claude/agents/**` → claude-code-ecosystem (domain ownership)

**Correct**:
```
Request: "Update .claude/agents/debugger.md"
Selection: claude-code-ecosystem (domain expert for agent definitions)
```

---

### ❌ Anti-Pattern 2: Keyword Matching Without Context

**Wrong**:
```
Request: "Create test fixtures for auth module"
Selection: development (because "create" keyword)
```

**Why Wrong**: Ignores work type. "test fixtures" → code-quality (testing domain)

**Correct**:
```
Request: "Create test fixtures for auth module"
Selection: code-quality (domain expert for test generation)
```

---

### ❌ Anti-Pattern 3: Ignoring Domain Boundaries

**Wrong**:
```
Request: "Fix documentation typo in docs/guides/setup.md"
Selection: development (because it's "simple")
```

**Why Wrong**: Ignores domain. `docs/**` → documentation agents

**Correct**:
```
Request: "Fix documentation typo in docs/guides/setup.md"
Selection: documentation (domain expert for documentation)
```

---

### ❌ Anti-Pattern 4: Forcing Single Agent Across Domains

**Wrong**:
```
Request: "Update agent definition and generate tests"
Selection: development (for both tasks)
```

**Why Wrong**: Crosses domain boundaries. Need 2 specialists.

**Correct**:
```
Request: "Update agent definition and generate tests"
Selection: claude-code-ecosystem (.claude/agents/**) + code-quality (tests/**)
Decompose into 2 sequential tasks
```

---

## Correct Patterns (What TO Do)

### ✅ Pattern 1: Respect Domain Ownership

**Principle**: Domain boundaries are strongest signal

```
.claude/agents/** → claude-code-ecosystem (ALWAYS)
docs/**/SPEC.md → /spec command or planning (ALWAYS)
packages/**/*.py → development/debugger/code-quality (depending on work type)
tests/**/*.py → code-quality/code-quality (ALWAYS)
```

---

### ✅ Pattern 2: Consider Work Type Within Domain

**Principle**: Verb determines specialist within domain

```
packages/**:
  ├─ "implement" → development
  ├─ "debug" → debugger
  ├─ "test" → code-quality (run) or code-quality (generate)
  └─ "review" → code-quality
```

---

### ✅ Pattern 3: Apply Disambiguation for Ambiguous Cases

**Principle**: Use priority order (domain ownership > closest expertise > least assumptions)

```
Request: "Analyze test coverage gaps"
Options: code-quality (testing domain) vs researcher-codebase (analysis)
Decision: code-quality (domain ownership + analysis capability)
```

---

### ✅ Pattern 4: Decompose Multi-Domain Tasks

**Principle**: Use multiple specialists for cross-domain work

```
Request: "Implement feature X and document it"
Decompose:
  1. development (packages/** implementation)
  2. documentation (docs/** documentation)
Execute sequentially
```

---

## Decision Framework Summary

**For 80% of Cases** (clear domain):
1. Extract file paths
2. Map to domain using Domain-First Thinking
3. Identify work type within domain
4. Apply disambiguation if needed
5. Select specialist

**For 20% of Cases** (unclear domain):
1. Calculate DCS for top 2-3 candidates
2. Select highest DCS (≥0.5 threshold)
3. If all <0.5, report to user + recommend agent creation

**Always**:
- Respect domain boundaries (strongest signal)
- Consider work type within domains
- Decompose multi-domain tasks
- Avoid anti-patterns (keyword matching, defaulting, boundary violations)

---

**This reference provides complete agent selection methodology for orchestrator delegation decisions.**
