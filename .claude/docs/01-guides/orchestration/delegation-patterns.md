# Delegation Patterns

**Purpose**: Best practices for orchestrator agents delegating work to specialist agents
**Last Updated**: 2025-11-21
**Applies To**: Orchestrator agents (researcher-lead, workflow orchestrators)

---

## Four-Component Delegation

Every delegation MUST include:

### 1. Specific Objective
**One core goal**, clearly stated without ambiguity

✅ **Good**:
- "Find all React hooks that use useEffect with empty dependency arrays in src/"
- "Analyze technical debt in packages/auth/ using SQALE methodology"

❌ **Bad**:
- "Look into the codebase" (too vague)
- "Fix everything" (unmeasurable, no scope)

---

### 2. Output Format
**Exactly what format** to return (list, report, answer, structured JSON)

✅ **Good**:
- "Return JSON list: `{file_path: string, line_number: number, hook_name: string}[]`"
- "Return markdown report with Executive Summary + 3-5 findings with file:line citations"

❌ **Bad**:
- "Give me some results" (undefined structure)
- "Whatever format works" (ambiguous, inconsistent)

---

### 3. Tool & Source Guidance
**Which tools to prefer**, what's reliable, research methodology

✅ **Good**:
- "Use Context7 first for official docs, escalate to Perplexity if trust <0.7"
- "Grep for pattern, then Read matching files, compress to top 5 findings"

❌ **Bad**:
- "Use whatever tools you want" (no guidance)
- "Search the internet" (no source quality criteria)

---

### 4. Task Boundaries
**Scope limits**, what to avoid, what's out of scope

✅ **Good**:
- "Analyze packages/auth/** only, exclude tests/ and __pycache__"
- "Report findings but DO NOT modify files or create pull requests"

❌ **Bad**:
- "Do what makes sense" (ambiguous scope)
- No boundaries specified (agent may overcomplicate)

---

## Scaling Rules

### Simple Task (Fact-Finding)
- **Agents**: 1
- **Tool calls**: 3-10
- **Example**: "Find definition of function `process_auth()` in codebase"

### Moderate Task (Comparison/Analysis)
- **Agents**: 2-4
- **Tool calls**: 10-15 per agent
- **Example**: "Compare authentication patterns across packages/auth/ and packages/core/"

### Complex Task (Research/Multi-Perspective)
- **Agents**: 10+ (clearly divided responsibilities)
- **Tool calls**: Variable per agent
- **Example**: "Complete competitive analysis of 5 authentication libraries with security, performance, and DX comparison"

---

## Search Strategy

### Phase 1: Start Wide
- **Broad queries** (<5 words)
- Cast wide net (Grep with loose patterns)
- **Goal**: Identify search space and available sources

**Example**:
```
Grep("authentication", glob="packages/**/*.py", output_mode="files_with_matches")
# Returns: 47 files
```

---

### Phase 2: Evaluate Sources
- **Assess quality** of results from Phase 1
- Identify authoritative sources (official docs, well-maintained files)
- **Prune** low-signal sources

**Example**:
```
# From 47 files, prioritize:
# - packages/auth/core.py (primary implementation)
# - packages/auth/validators.py (validation logic)
# - docs/architecture/auth-flow.md (design doc)
```

---

### Phase 3: Progressively Narrow
- **Focused queries** on high-quality sources
- Extract specific information needed
- **Iterate** if results insufficient

**Example**:
```
Read("packages/auth/core.py")  # Get implementation details
Grep("JWT.*secret", path="packages/auth/")  # Find secret handling
```

---

### Phase 4: Compress Findings
- **Distill insights** from large data
- Return **essential findings only** (not full research)
- **High-signal outputs** for orchestrator consumption

**Example**:
```
# Instead of returning 3,000 lines of code:
Return:
- 3 authentication methods found (JWT, OAuth2, API Key)
- JWT implementation uses HS256 with rotating secrets (file:line citations)
- Vulnerability: API keys stored in plaintext (security-concern.md:45)
```

---

## Example Delegations

### Example 1: Single-Agent Fact-Finding

```markdown
Task(researcher-codebase,
  "Find all uses of deprecated function `old_encrypt()` in packages/.

  **Output**: JSON list with {file_path, line_number, usage_context}.

  **Tools**: Grep for 'old_encrypt', Read matching files for context.

  **Scope**: packages/** only, exclude tests/ and archived/")
```

---

### Example 2: Multi-Agent Parallel Research

```markdown
# Orchestrator delegates to 3 agents in parallel (single message, 3 Task calls):

Task(researcher-external,
  "Research React 19 authentication best practices from official docs.
  Output: 3-5 recommended patterns with citations.")

Task(researcher-external,
  "Find community React authentication patterns from 2024-2025.
  Output: Top 3 libraries with GitHub stars, npm downloads, last updated.")

Task(researcher-codebase,
  "Analyze our existing React auth implementation in src/components/Auth/.
  Output: Current patterns, pain points, technical debt.")

# Orchestrator then synthesizes 3 agent outputs into unified recommendation
```

---

### Example 3: Complex Multi-Perspective Analysis

```markdown
# Orchestrator coordinates 10+ agents for comprehensive library comparison:

# Phase 1: Data gathering (5 agents in parallel)
Task(researcher-external, "Get Passport.js official docs")
Task(researcher-external, "Get Auth0 SDK docs")
Task(researcher-external, "Get NextAuth.js docs")
Task(researcher-external, "Get Supabase Auth docs")
Task(researcher-external, "Get Clerk docs")

# Phase 2: Analysis (5 agents in parallel)
Task(security-analyzer, "Security audit of 5 libraries")
Task(performance-analyzer, "Performance benchmarks")
Task(dx-analyzer, "Developer experience comparison")
Task(cost-analyzer, "Pricing and TCO analysis")
Task(integration-analyzer, "Integration complexity assessment")

# Phase 3: Synthesis
# Orchestrator consolidates findings, applies weighted scoring, generates recommendation
```

---

## Delegation Anti-Patterns

❌ **Vague objectives**:
```
Task(agent, "Look into authentication stuff")  # WRONG
```

❌ **No output format**:
```
Task(agent, "Research React hooks")  # No structure specified
```

❌ **Missing tool guidance**:
```
Task(agent, "Find the answer somehow")  # No methodology
```

❌ **Unbounded scope**:
```
Task(agent, "Fix all the code")  # No limits, will overcomplicate
```

❌ **Over-delegation**:
```
# Delegating 1-line task to agent (overhead > value)
Task(agent, "Count files in src/")  # Just use Glob directly
```

---

## Compression Principle

**Agents as intelligent filters**: Return insights, not raw data

**Before compression**:
- 15 React hook files analyzed
- 3,000 lines of code read
- 50 useEffect instances found

**After compression** (agent output):
- 3 anti-patterns identified: Missing deps (12 instances), empty deps (8), stale closures (5)
- Top 3 high-risk files: Dashboard.tsx:45, UserProfile.tsx:89, Analytics.tsx:123
- Recommendation: Migrate to React 19 `use()` API

**Compression Ratio**: 3,000 lines input → 150 tokens output = 20:1 compression

---

## Best Practices

1. **Clear objectives**: One core goal per delegation
2. **Structured outputs**: Specify exact format (JSON, markdown, etc.)
3. **Tool guidance**: Direct methodology, especially for research
4. **Bounded scope**: Explicit limits prevent overwork
5. **Parallel execution**: Launch independent agents in single message (multiple Task calls)
6. **Compression expectations**: Request high-signal summaries, not raw data dumps
7. **Confidence scoring**: Ask agents to include confidence (0.0-1.0) with findings
8. **Citation requirements**: File:line references for all findings

---

**Reference**: Used by orchestrator agents for multi-agent coordination and delegation decisions
