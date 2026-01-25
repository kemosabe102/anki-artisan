# Strategic Planning Document Relationships

## Document Hierarchy & Flow

Strategic Plan → Roadmap Items → Feature Specs → Technical Plans → Executable Tasks

## Document Definitions

### 1. Strategic Plan (Business Level)

- **Purpose**: Overall business objectives and quarterly goals
- **Audience**: Leadership, product strategy
- **Content**: Market positioning, competitive advantage, revenue goals
- **Timeframe**: 6-12 months
- **Location**: `docs/00-project/SPEC.md` (system level)

### 2. Roadmap Items (Capability Level)

- **Purpose**: Capability descriptions that advance strategic objectives
- **Audience**: Product managers, engineering leads
- **Content**: Feature capabilities, business value, success metrics
- **Timeframe**: 1-3 months per item
- **Location**: `docs/00-project/ROADMAP-*.md`

### 3. Feature Specs (Requirement Level)

- **Purpose**: Detailed specifications that implement roadmap capabilities
- **Audience**: Engineering teams, QA, design
- **Content**: Functional requirements, acceptance criteria, constraints
- **Timeframe**: 2-6 weeks per spec
- **Location**: `docs/01-planning/specifications/XXX-[feature-name]/SPEC.md`

### 4. Technical Plans (Implementation Level)

- **Purpose**: Implementation approach and architecture for specs
- **Audience**: Developers, architects, DevOps
- **Content**: Technology choices, architecture patterns, dependencies
- **Timeframe**: 1-3 weeks per plan
- **Location**: `docs/01-planning/specifications/XXX-[feature-name]/plans/`

### 5. Executable Tasks (Action Level)

- **Purpose**: Step-by-step actions to complete technical plans
- **Audience**: Individual developers, sub-agents
- **Content**: Specific implementation steps, acceptance criteria, assignments
- **Timeframe**: Hours to days per task
- **Location**: `docs/01-planning/specifications/XXX-[feature-name]/tasks/`

## Traceability Requirements

- Each document must reference its parent document
- Changes upstream require validation of downstream impacts
- Agent creation tasks must map to specific technical plan requirements
- All artifacts maintain golden thread back to strategic objectives

## Maturity Progression

- Documents mature together through the SDLC
- Higher-level documents stabilize before lower-level implementation
- Changes require validation against maturity constraints

## Commands Trigger Workflows

- Each command represents a workflow that operates on these documents
- Commands should be designed with the complete document flow in mind
- Workflow agent will coordinate command design with document relationships

## Agent Naming Guidelines (Future Agents Only)

**Naming Principles:**

1. **Simple Words**: Use common English vocabulary (avoid jargon)
2. **Clear Function**: Name describes what the agent does
3. **Granularity-Aware**: Name reflects current scope (can split later)
4. **Accessible**: Easy for non-native English speakers
5. **Descriptive**: Based on capabilities, not metaphors

**Examples for Future Agents:**

- Agent that handles data validation → **Validator**
- Agent that manages deployments → **Deployer**
- Agent that monitors systems → **Monitor**
- Agent that creates documentation → **Documenter**
- Agent that builds workflows → **Workflow** (or WorkflowBuilder)

**Note**: Existing agents will be refactored in Q4 2025 as technical debt item.
