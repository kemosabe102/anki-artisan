# Industry Standards Reference for AI Agent Prompt Evaluation

**Version**: 1.0
**Purpose**: SRE and production AI agent best practices for evaluating prompt quality

---

## Claude Code-Specific Constraints

**Valid Agent Frontmatter Fields** (ONLY these are supported):
- `name` (required), `description` (required)
- `tools`, `model`, `permissionMode`, `skills` (optional)

**NOT Supported in Claude Code**:
- version, maturity, temperature, disallowedTools, color, status, tags

---

## Quick Reference: Industry Practice to Claude Code

| Industry Practice | Claude Code Implementation |
|-------------------|---------------------------|
| Version field | Use git tags/commits |
| Maturity field | External docs or description |
| Temperature | Global config only |
| DisallowedTools | Use `tools` allow-list |
| Model selection | `model` field (opus recommended, sonnet, haiku, inherit) |
| Permission control | `permissionMode` field |

---

## 10 Key Standards

### 1. System Prompt Design
- Establish instruction hierarchy (Schema → Agent → Orchestrator → User)
- Define role, task, goal, constraints clearly
- Use explicit instructions over inference

### 2. Structured Outputs & Tool Reliability
- Enforce JSON Schema with `additionalProperties: false`
- Tool descriptions at 80%+ detail coverage
- Defensive error handling (natural language errors)

### 3. Failure Handling & Recovery
- Map potential error states before they occur (reduces critical failures by ~47%)
- Graceful degradation for non-critical failures
- Intelligent retry with exponential backoff (1s, 2s, 4s, max 3-5 attempts)

### 4. Context & Memory Management
- Target <15K tokens for agent definitions
- Hierarchical information structure (Essential → Progressive → External → Escalation)

### 5. Prompting Techniques
- ReAct pattern: Think → Act → Observe cycles
- Few-shot examples: 1-5 well-crafted demonstrations
- Constraint-based prompting with schema enforcement

### 6. Guardrails & Security
- Deterministic guardrails (schema + permissions)
- Start locked down, gradually loosen based on evidence
- Input/output validation rigorously

### 7. Production Observability
- Track prompts, responses, token usage, latency, error patterns
- Behavioral anomaly detection (baselines + triggers)
- Confidence scoring for tiered decision-making

### 8. Model Parameters & Consistency
- Low temperature (0.0-0.3) for production reliability
- Built-in recovery logic over external retry mechanisms

### 9. Documentation & Versioning
- Treat prompts as living artifacts with test-driven iteration
- Systematic versioning with A/B testing capability
- Project-specific guidance files (CLAUDE.md pattern)

### 10. Testing & Evaluation
- 30+ test cases per agent (success, edge, failure scenarios)
- Progressive validation: Tier 1 (basic) → Tier 2 (edge) → Tier 3 (chaos)
- Systematic tracking for audit trails

---

## Compliance Checklist (Quick Reference)

### System Design
- [ ] Instruction hierarchy documented
- [ ] Role, task, goal, constraints defined
- [ ] Explicit instructions (not inference-reliant)

### Reliability
- [ ] JSON Schema with additionalProperties: false
- [ ] Tool definitions with 80%+ detail
- [ ] Transient vs permanent error differentiation
- [ ] Graceful degradation implemented

### Context & Prompting
- [ ] Token count <15K
- [ ] Hierarchical structure (4 levels)
- [ ] ReAct pattern with examples
- [ ] 1-5 few-shot examples

### Security
- [ ] Schema + permission guardrails
- [ ] Input/output validation
- [ ] Path sanitization

### Observability
- [ ] Multi-dimensional confidence scoring
- [ ] Behavioral baselines defined
- [ ] Tiered decision-making (high/medium/low)

### Documentation
- [ ] Git-based versioning
- [ ] 30+ test cases
- [ ] Progressive validation (3 tiers)

---

## References

- [Anthropic Prompt Engineering Guide](https://www.anthropic.com/engineering)
- [ReAct: Reasoning + Acting](https://arxiv.org/abs/2210.03629)
- [SRE for AI Agents](https://www.getmonetizely.com/articles/how-to-master-error-handling-in-agentic-ai-systems)
