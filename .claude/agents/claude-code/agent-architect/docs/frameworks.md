# Agent Architect Frameworks

## Quality Framework

### Evaluation Criteria (Weighted 0-5 Scale)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 0.25 | Task accuracy, external validation |
| **Format Fidelity** | 0.15 | Schema adherence, machine-parseable outputs |
| **Description-Capability Alignment** | 0.10 | Frontmatter accurately reflects capabilities |
| **Scope Discipline** | 0.10 | Avoids role drift, clear boundaries |
| **Tool Use Quality** | 0.10 | Appropriate tool selection/usage |
| **Reliability & Repeatability** | 0.10 | Stable performance across contexts |
| **Safety/Compliance** | 0.10 | No prohibited content, proper refusals |
| **Maintainability** | 0.10 | Prompt clarity, modularity, reasonable length |
| **Efficiency** | 0.025 | Cost/latency budgets, token optimization |
| **Observability** | 0.025 | Structured logging, debugging support |

**AI-Readability Note**: Maintainability criterion includes AI-readability assessment. Agent prompts should follow patterns from `creating-ai-readable-documentation-framework.md`: structured headers, explicit instructions, scannable format, front-loaded key information.

### Grade Calculation

| Grade | Score Range | Description |
|-------|-------------|-------------|
| **A** | 4.5-5.0 | Production ready, excellent performance |
| **B** | 3.5-4.4 | Good performance, minor improvements needed |
| **C** | 2.5-3.4 | Acceptable performance, notable issues |
| **D** | 1.5-2.4 | Poor performance, significant improvements required |
| **F** | 0.0-1.4 | Failing performance, major redesign needed |

### Maturity Stages

- **v0.x (MVP)**: Development only
- **v1.x (Alpha)**: Testing ready
- **v2.x (Beta)**: Production candidate
- **v3.x+ (GA)**: Production ready

---

## Simulation-Driven Development

### Core Principle
Think from the target agent's perspective BEFORE creation.

### Process
1. Simulate what the agent needs to accomplish its goals
2. Consider tool requirements and their descriptions
3. Map out work phases and decision points
4. Identify potential failure modes and edge cases
5. Evaluate frameworks and patterns from agent.template.md

### Tool Description Standards (Anthropic Best Practice)
- Write as if explaining to new team member
- Make implicit context explicit (query formats, terminology)
- Use unambiguous parameter names (`user_id` vs `user`)
- Disclose destructive changes or open-world access
- Include examples where helpful

---

## OODA Loop for Agent Creation/Updates

1. **Observe** - Requirements, existing patterns, agent template, available tools
2. **Orient** - Best approach for agent type, similar patterns, framework selection
3. **Decide** - Tool selection with descriptions, prompt structure, delegation patterns
4. **Act** - Create/update agent, validate against template, evaluate quality

---

## Framework Selection for Agent Design

### Quick Framework Selection Matrix

| Agent Category | Primary Framework | When to Use |
|----------------|------------------|-------------|
| Research agents | ReACT | Iterative investigation loops |
| Implementation agents | CAGEERF | Complex multi-component tasks |
| Analysis/Review agents | 5W1H + DMAIC | Systematic analysis + measurement |
| Planning agents | CAGEERF + OKR | Comprehensive planning + goals |
| Debugging agents | ReACT + 5 Whys | Hypothesis-driven + root cause |
| Optimization agents | SCAMPER + DMAIC | Creative enhancement + process |
| Agent lifecycle | CAGEERF + SCAMPER | Design + enhancement |

### Framework Integration Requirements
- **Reasoning Approach Section**: Reference primary framework methodology
- **Operations Section**: Apply framework steps to agent workflows
- **Quality Matrix**: Include framework alignment in evaluation criteria

---

## Research Tool Selection Protocol

### Context7 First (Free, Authoritative)

**Use for** (confidence < 0.9):
- Agent framework patterns (Pydantic, instructor, guidance)
- Prompt engineering best practices
- MCP server implementation patterns
- Schema design, validation frameworks

**Process**:
1. `resolve_library_id("LibraryName")` → Get library metadata
2. `get_library_docs(library_id, topic, tokens=5000)` → Fetch docs
3. IF trust ≥7 AND snippets ≥100 → STOP, use Context7 solution
4. IF insufficient → Escalate to Perplexity

### Perplexity Escalation (Paid, Use Sparingly)

**Use ONLY when**:
- Confidence < 0.8 (unclear design approach)
- Context7 insufficient (framework not covered)
- Agent creation failed 2+ times
- General prompt engineering research

**Tool Selection**:
- `perplexity_search`: Quick pattern lookups (~$0.003)
- `perplexity_ask`: General questions (~$0.003)
- `perplexity_research`: Comprehensive investigation (~$0.005-0.010)
- `perplexity_reason`: Trade-off analysis (~$0.008-0.015)

---

## Progressive Disclosure for Agent Design

Apply Skills best practices:
- Semantic-rich descriptions (<200 chars)
- Hierarchical structure (When to Use → Capabilities → Guidelines → Examples → Resources)
- Size target (<500 lines)
- Context efficiency (externalize detailed content)
