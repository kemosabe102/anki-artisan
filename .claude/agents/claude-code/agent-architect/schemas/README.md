# Agent Architect Schemas

## Contents

| File | Purpose |
|------|---------|
| `agent-architect.schema.json` | Input/output contract for all operations |

## Schema Structure

The schema defines:
- **Input**: Operation type, requirements, constraints
- **Output**: SUCCESS or FAILURE with structured data
- **Operations**: create_agent, evaluate_agent, implement_feedback, update_agent, analyze_agent_idea, generate_agent_definition, and more

Extends `base-agent.schema.json` with agent-specific operation results.
