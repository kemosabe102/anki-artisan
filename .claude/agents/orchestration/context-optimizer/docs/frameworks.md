# Context Optimization Frameworks

**Purpose**: Complete 5-phase workflow and progressive disclosure optimization strategies.

---

## 5-Phase Analysis Workflow

### Input Requirements

- **analysis_scope**: agents | orchestrator | mcp | full
- **target_agents**: `"all"` | `["agent1", "agent2"]` | `"pattern-*"`
- **depth_level**: quick | standard | comprehensive
- **focus_areas**: redundancy | structure | compression | all

---

### Phase 1: Discovery (Baseline Collection)

**Duration**: 10-15 min (ecosystem) | 2-3 min (targeted)

#### Targeting Logic

**IF target == "all"**:
- Glob: `.claude/agents/**/*.md`
- Sample: Select largest 5-10 for deep analysis

**IF target is list**:
- Read: Each specified agent directly
- NO sampling (analyze ALL specified)

**IF target is pattern**:
- Glob: `.claude/agents/**/{pattern}`
- IF >10 agents: Sample largest 5-10
- IF ≤10 agents: Analyze ALL

#### Discovery Steps

1. **Inventory**: Glob all agent files, count lines, estimate tokens
2. **Token Estimation**: `line_count × 4.5 = approx_tokens`
3. **Structure Review**: Read 3-5 representative agents, extract common patterns
4. **Orchestrator Analysis**: Read CLAUDE.md, estimate tokens, identify embedded vs referenced
5. **MCP Audit**: Read `.claude/settings.json`, count tools, estimate overhead

---

### Phase 2: Deep Analysis (Redundancy Detection)

**Duration**: 15-20 min

1. **Section Extraction**: Extract Knowledge Base, Pre-Flight, Workflow, Error Recovery sections
2. **Similarity Analysis**: Compare pairwise, identify >80% similar sections
3. **Pattern Consolidation**: Group similar sections, select canonical version
4. **Example Bloat Detection**: Count examples per agent, measure token cost

---

### Phase 3: Best Practice Validation

**Duration**: 10-15 min

1. **External Research**: WebFetch Anthropic context guide, MCP patterns
2. **Compliance Check**: Compare current vs best practices
3. **Compression Audit**: Check for compression checkpoints, verify ratios
4. **Token Density Analysis**: Scan filler words (<5%), active voice (>80%), example count (≤3)

---

### Phase 4: Optimization Planning

**Duration**: 15-20 min

1. **Finding Categorization**: Group by category, prioritize by severity
2. **Recommendation Generation**: Create actionable items, calculate ROI, assess risk
3. **Implementation Planning**: Phase 1 (quick wins) → Phase 2 (strategic) → Phase 3 (advanced)
4. **Metrics Definition**: Set baselines, targets, measurement framework

---

### Phase 5: Report Generation

**Duration**: 10-15 min

1. **Executive Summary**: Total tokens, optimization potential, top 5 findings
2. **Detailed Analysis**: Per-agent breakdown, redundancy patterns, MCP analysis
3. **Recommendations Roadmap**: Priority matrix, phased plan, risk assessment
4. **Output Delivery**: Write to `docs/04-guides/domain-specific/`

---

## Progressive Disclosure Optimization

### 1. Three-Tier Loading Pattern

**Detection Criteria**:
- Documents >200 lines → Candidate for externalization
- Agent definitions with detailed references → Candidate for Level 3
- Specifications with comprehensive API docs → Separate reference files

**Token Savings Formula**:
```
Token_Savings = (Current_Size - Metadata_Size) × (1 - Usage_Frequency)

Where:
- Current_Size: Full document token count
- Metadata_Size: Summary/description (~100 tokens)
- Usage_Frequency: 0.0 (never) to 1.0 (always)
```

**Example**:
```
Document: api-integration-guide.md
Current Size: 2500 tokens
Usage Frequency: 0.3 (30% of invocations)

Optimization:
- Metadata-only: ~100 tokens
- Savings = (2500 - 100) × (1 - 0.3) = 1680 tokens

Recommendation:
- Tier 1 (Metadata): API overview, auth types, base URLs
- Tier 2 (On-demand): Common patterns, error handling
- Tier 3 (External): Complete endpoint reference
```

---

### 2. Executable Script Pattern

**Key Insight**: Scripts consume **zero tokens** during execution; only output enters context.

**Detection Criteria**:
- Code blocks >50 lines
- Repeated validation logic
- Complex data transformations
- API integration samples

**Pattern**:
```
BEFORE (500 tokens in context):
[500 lines of Python inline]

AFTER (0 tokens in context):
Run: `scripts/validate_schema.py --input schema.json`
Output: ~50 tokens enters context

Savings: 450 tokens per invocation
```

---

### 3. Reference Consolidation

**Detection Criteria**:
- Same explanation in 3+ documents
- Technical specs duplicated from official sources
- Common patterns repeated across agents

**Pattern**:
```
BEFORE (400 tokens × 5 agents = 2000 tokens):
[Long Pydantic explanation in 5 agents]

AFTER (50 tokens × 5 agents = 250 tokens):
**Validation**: See `pydantic-validation-patterns.md` lines 45-78.

Savings: 1750 tokens across ecosystem
```

---

## Optimization Strategy Selection

| Strategy | Confidence | Risk | When to Use |
|----------|-----------|------|-------------|
| **Reference** | High | Low | Content duplicates existing guide |
| **Extend** | Medium | Low | Partial overlap, add reference |
| **Create** | Medium | Medium | No suitable reference exists |
| **Keep** | High | Low | Essential context, <50 lines, unique |

---

## Workflow Timing Summary

| Mode | Agents | Duration | Use Case |
|------|--------|----------|----------|
| **"all"** | Sample 5-10 | 60-85 min | Ecosystem comprehensive review |
| **["a1", "a2"]** | Exact list | 2-10 min | Quick feedback, comparison |
| **"pattern-*"** | Glob match | 8-20 min | Agent family consistency |

---

## Common Workflow Patterns

**Quick Scan** (15-20 min):
Glob → Read largest 3-5 → Identify redundancies → Estimate savings → Executive summary

**Standard Analysis** (60-85 min):
Full 5-phase workflow

**Focused Analysis** (30-40 min):
Scope to specific component → Deep dive → Best practices → Targeted recommendations

---

**Usage**: Consult this guide for detailed workflow steps and progressive disclosure optimization techniques.
