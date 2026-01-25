# examples/ Directory

**Purpose**: Concrete usage patterns showing how this agent is called and what it produces

---

## What Goes Here

| File | Purpose | Audience |
|------|---------|----------|
| `delegation-examples.md` | How orchestrator delegates to this agent | Orchestrator, other agents |
| `output-template.md` | Standard output formats with examples | Agent itself, validation |
| `{{workflow}}-examples.md` | Specific workflow demonstrations | Users, developers |

---

## Guidelines

1. **Show complete examples** - Full input/output pairs, not fragments
2. **Cover edge cases** - Include error handling, unusual inputs
3. **Keep current** - Update when agent behavior changes
4. **Use realistic data** - Examples should feel like actual usage

---

## File Purposes

### delegation-examples.md

Shows the orchestrator (and other agents) how to call this agent:
- Task description format
- Required context
- Expected response structure
- Multi-agent coordination patterns

### output-template.md

Defines what the agent produces:
- YAML/JSON structure templates
- Field descriptions
- Complete annotated examples
- Quality checklist

---

## See Also

- **Reference example**: `.claude/agents/ttrpg-campaign-architect/examples/`
- **Orchestrator patterns**: `.claude/docs/03-workflows/orchestrator-workflow.md`
