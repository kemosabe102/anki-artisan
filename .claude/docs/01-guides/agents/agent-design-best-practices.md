---
title: "Agent Design Best Practices"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Design Best Practices

## Overview

This guide documents comprehensive agent design best practices based on performance research, architecture analysis, and practical implementation experience. Provides actionable patterns for developing high-quality, performant Claude Code agents with optimal initialization times and resource usage.

**📊 Performance-First Design**: This guide prioritizes agent startup performance and resource efficiency as primary design criteria, incorporating empirical findings about tool initialization costs and architectural patterns.

## Core Design Principles

### 1. Single Responsibility Principle

**Pattern**: Each agent should have one clearly defined purpose with narrow scope boundaries.

**Best Practice**:

- Limit agent scope to specific functional areas (e.g., `.claude/**` directory for claude-code-agent)
- Define clear boundaries in the "Role & Boundaries" section
- Use micro-agent architecture for specialized capabilities

**Example**:

```yaml
# Good - Focused scope
name: claude-code-agent
description: Specialized micro-agent for managing Claude Code configuration
scope: .claude/** directory only

# Avoid - Overly broad scope
name: general-helper
description: Does everything related to development
scope: entire codebase
```

### 2. Performance-First Tool Selection

**Pattern**: Grant tools based on initialization cost analysis and operational requirements.

**Tool Performance Categories** (by initialization overhead):

- **🟢 Lightweight (Fast)**: Read, Grep - File system access only, ~20s startup
- **🟡 Medium (Moderate)**: Edit, MultiEdit - File modification with safety checks, ~1-2min startup
- **🔴 Heavy (Slow)**: Write, Bash, WebSearch, WebFetch, MCP Context7 - External dependencies, minutes+ startup

**Performance-Based Selection Rules**:

1. **Read-Only Agents**: Use Read + Grep only (optimal performance pattern)
2. **Enhancement Agents**: Read + Edit (avoid MultiEdit unless essential for bulk operations)
3. **Creator Agents**: Add Write only when file creation is core responsibility
4. **Research Agents**: Add external tools (WebSearch, Context7) sparingly and only for dedicated research roles
5. **Never Mix Heavy Tools**: Avoid combining multiple heavy-initialization tools unless absolutely required

**Tool Usage Guidelines & Performance Impact**:

- **Read Tool (Lightweight)**: For file contents only. NEVER try to read directories
- **Grep Tool (Lightweight)**: Preferred for content search - faster than loading full files
- **Edit Tool (Medium)**: Single file modifications - more efficient than MultiEdit for <3 changes
- **MultiEdit Tool (Medium)**: Bulk operations only - higher computational cost, reserve for >5 changes
- **Write Tool (Heavy)**: File creation with permission framework overhead
- **Bash Tool (Heavy)**: Shell environment initialization - avoid for simple operations
- **External Services (Heavy)**: WebSearch, WebFetch, Context7 require network handshakes

**Performance Anti-Pattern**: Never grant Bash + WebSearch + Context7 to same agent (massive initialization cost)

### 3. Structured Output Compliance

**Pattern**: All agents must return JSON conforming to their specific result schema.

**Best Practice**:

- Define clear operation types in input/result schemas
- Use oneOf patterns for different operation results
- Include status types: SUCCESS, NEEDS_CLARIFICATION, ERROR
- Provide structured error handling with actionable next steps

**Schema Structure**:

```json
{
  "status": "SUCCESS|NEEDS_CLARIFICATION|ERROR",
  "agent": "agent-name",
  "task_id": "unique-identifier",
  "operation_type": "specific-operation",
  "operation_result": {
    /* operation-specific data */
  }
}
```

### 4. Clear Boundary Enforcement

**Pattern**: Agents must validate their operational boundaries before executing any operations.

**Best Practice**:

- Implement path validation for file operations
- Halt execution on boundary violations
- Document what the agent handles vs. avoids vs. escalates to human
- Use explicit boundary checks in tool usage

**Boundary Implementation**:

```markdown
**Handles**:

- Specific file types or directories
- Clearly defined operational scope

**Avoids**:

- Operations outside defined boundaries
- Cross-cutting concerns

**Ask Human**:

- Complex edge cases
- Security-sensitive operations
```

## Agent Configuration Template

### Required Fields

```yaml
---
name: kebab-case-agent-name
description: Specific, focused capability description (max 200 chars)
model: opus|sonnet (based on complexity)
color: unique-identifier-color
tools: minimal-required-tool-set
---
```

### Model Selection Guidelines

- **Sonnet**: Default for most implementation tasks, balanced performance/cost
- **Opus Plan**: Complex reasoning, evaluation, planning tasks requiring deep analysis
- **Haiku**: Simple, fast operations, basic file manipulation (rare use)

### Color Coding Standards

- **Blue**: Configuration and setup agents (Read-only micro-agents)
- **Purple**: Architecture and design agents (Analysis-focused)
- **Green**: Implementation and execution agents (Edit/Write capability)
- **Orange**: Testing and validation agents (Medium complexity)
- **Red**: Error handling and debugging agents (Heavy tools as needed)

### Performance-Based Model Selection

- **Haiku**: Lightweight operations, simple file processing
- **Sonnet**: **Default choice** - balanced performance for most operations
- **Opus**: Complex reasoning, strategic planning, deep analysis only

## Quality Criteria

### Essential Quality Checks

1. **Scope Discipline**: Agent stays within defined boundaries
2. **Tool Use Quality**: Appropriate tool selection and usage patterns
3. **Output Compliance**: Schema-valid JSON responses
4. **Error Handling**: Graceful degradation with clear error messages
5. **Documentation**: Clear purpose, boundaries, and usage examples

### Performance Considerations

- Token optimization in prompts and responses
- Efficient tool usage patterns
- Minimal cross-agent dependencies
- Clear handoff protocols with orchestrator

## Performance Optimization Strategies

### Agent Architecture Patterns

#### 1. 🟢 Read-Only Micro-Agent (Optimal Performance)

**Pattern**: Single-purpose agents with minimal tool overhead
**Tools**: Read + Grep only
**Startup Time**: ~20 seconds
**Best For**: Analysis, validation, content extraction
**Example**: spec-analyzer agent

**Implementation**:

```yaml
name: content-analyzer
model: opus # balanced performance
tools: [Read, Grep]
# Avoid: Edit, MultiEdit, Write, Bash, external services
```

#### 2. 🟡 Enhancement Agent (Balanced Performance)

**Pattern**: File modification with controlled tool set
**Tools**: Read + Edit (avoid MultiEdit unless bulk operations required)
**Startup Time**: 1-2 minutes
**Best For**: Content enhancement, targeted modifications
**Example**: planning agent

**Implementation**:

```yaml
name: content-enhancer
model: opus
tools: [Read, Edit] # Avoid MultiEdit unless >5 simultaneous changes needed
# Avoid: Write (creation), Bash, external services
```

#### 3. 🔴 Full-Capability Agent (Use Sparingly)

**Pattern**: Complex operations requiring multiple heavy tools
**Tools**: Complete tool set with external services
**Startup Time**: 3+ minutes
**Best For**: Research, complex workflows, orchestration
**Optimization**: Minimize usage, delegate to lighter agents when possible

### Model Selection for Performance

**Performance-Capability Matrix**:

- **Haiku**: Fastest initialization, simple operations only
- **Sonnet**: Balanced performance/capability - **recommended default**
- **Opus**: Complex reasoning but slower startup - use for deep analysis only
- **sonnet**: Hybrid approach - Opus for planning, Sonnet for execution

### Architecture Decision Framework

**Before adding any tool, ask**:

1. **Is this tool essential for core responsibility?**
2. **What is the initialization cost impact?**
3. **Can a lighter-weight alternative achieve the same result?**
4. **Will this tool be used >80% of the time the agent runs?**

**Optimization Strategies**:

- **Split Heavy Agents**: Break into focused micro-agents when possible
- **Lazy Loading**: Prefer specialized agents over general-purpose ones
- **Tool Combinations**: Never combine >2 heavy tools unless absolutely required
- **Role Specialization**: Reader vs Editor vs Creator vs Researcher separation

## Anti-Patterns to Avoid

### 1. Performance Anti-Patterns

#### Tool Initialization Bloat

**Problem**: Agent includes multiple heavy-initialization tools (Bash + WebSearch + Context7 + Write)
**Impact**: 5+ minute startup times, resource waste
**Solution**: Split into specialized micro-agents with focused tool sets

**Example - BAD**:

```yaml
name: general-helper
tools: [Read, Write, Edit, MultiEdit, Bash, WebSearch, WebFetch, Context7]
# Result: Massive initialization overhead
```

**Example - GOOD**:

```yaml
# Split into specialized agents
name: content-reader     # Read, Grep only
name: content-enhancer   # Read, Edit only
name: research-agent     # Read, WebSearch, Context7 only
```

#### Complex Multi-Mode Agents

**Problem**: Single agent trying to be creator + editor + reviewer + researcher
**Impact**: Heavy preparation paths, unclear boundaries
**Solution**: Single-responsibility agents with clear role definitions

#### Unnecessary External Dependencies

**Problem**: Including WebSearch/Context7 for agents that rarely research
**Impact**: Network handshake overhead on every startup
**Solution**: Delegate research to dedicated research agents

### 2. Traditional Anti-Patterns

#### Scope Creep

**Problem**: Agent tries to handle responsibilities outside its defined scope.
**Solution**: Strict boundary validation and clear delegation patterns.

#### Tool Bloat

**Problem**: Agent includes unnecessary tools "just in case."
**Solution**: Performance-first tool selection based on initialization cost analysis.

#### Direct Sub-Agent Communication

**Problem**: Agents attempting to communicate directly with other agents.
**Solution**: All coordination through orchestrator with structured handoffs.

#### Inconsistent Output Formats

**Problem**: Agent returns different response structures for similar operations.
**Solution**: Strict schema compliance with operation-specific result types.

## Implementation Guidelines

### Performance-First Agent Creation Workflow

1. **Define Purpose**: Single, clear responsibility statement
2. **Analyze Tool Requirements**: Map operations to tool performance categories
3. **Select Performance Tier**: Read-Only → Enhancement → Full-Capability
4. **Establish Boundaries**: What the agent handles, avoids, and escalates
5. **Optimize Tool Set**: Minimal set required, prefer lightweight alternatives
6. **Design Schema**: Input/output contracts with validation
7. **Performance Test**: Validate startup time meets expectations
8. **Document Patterns**: Clear usage examples and integration notes

### Agent Performance Optimization Checklist

**Pre-Creation Analysis**:

- [ ] Single responsibility clearly defined
- [ ] Tool requirements mapped to performance categories
- [ ] Lighter-weight alternatives evaluated
- [ ] Role specialization (reader vs editor vs creator) determined

**Tool Selection Optimization**:

- [ ] Read + Grep preferred for analysis tasks
- [ ] Edit preferred over MultiEdit for <5 changes
- [ ] External tools (WebSearch, Context7) reserved for dedicated research agents
- [ ] Heavy tools (Write, Bash) only when core to agent responsibility
- [ ] No unnecessary tool combinations

**Performance Validation**:

- [ ] Startup time measured and acceptable for use case
- [ ] Tool usage >80% for included tools
- [ ] No unused heavy-initialization tools
- [ ] Clear performance expectations documented

### Schema Design Best Practices

- Use `oneOf` patterns for different operation types
- Include comprehensive error handling schemas
- Define clear validation criteria for inputs
- Provide structured output for machine processing

### Testing and Validation

- Validate schema compliance for all operations
- Test boundary enforcement with edge cases
- Verify tool permissions match operational requirements
- Ensure graceful error handling and recovery

## Current Agent Performance Analysis & Recommendations

### Existing Agent Optimization Status

#### 🟢 Optimal Performance Agents

- **spec-analyzer**: Read + Grep only (~20s startup) - ✅ Keep as-is
- **architecture**: Focused analysis role - ✅ Performance optimized

#### 🟡 Good Performance Agents

- **planning**: Read + Edit + MultiEdit (moderate startup) - ⚠️ Consider removing MultiEdit if not essential
- **code-quality**: Targeted tool set for quality gates - ✅ Appropriate for complexity

#### 🔴 Performance Improvement Needed

- **planning**: 11 tools including heavy external services - ❌ MAJOR OPTIMIZATION REQUIRED

### CRITICAL: Technical PM Agent Simplification

**Current State Analysis**:

```yaml
name: planning
tools: [Read, Write, Edit, MultiEdit, Bash, WebSearch, WebFetch, Context7]
# Impact: 5+ minute startup time, massive initialization overhead
```

**Architectural Issue**: Technical PM should be a **reviewer-only** role, not creator/editor

**Recommended Optimization** (90% performance improvement expected):

```yaml
name: planning
model: opus # Keep for strategic thinking
tools: [Read, Grep] # Remove 9 tools, keep only review capabilities
# Result: ~20s startup time (from 5+ minutes)
```

**Migration Strategy**:

1. **Remove Creator Tools**: Write, Edit, MultiEdit (file creation/editing not needed for review)
2. **Remove External Services**: WebSearch, WebFetch, Context7 (research not needed for review)
3. **Remove Shell Access**: Bash (no script execution needed for review)
4. **Keep Review Tools**: Read (plan analysis), Grep (content search)

**Impact**: Technical PM becomes pure reviewer with massive performance improvement, aligning with intended architectural role.

### Performance Monitoring Guidelines

**Diagnostic Commands**:

- `/doctor`: Check agent health and configuration
- `/verbose`: Enable detailed logging for performance analysis
- Agent startup time tracking for performance regressions

**Environment Optimization**:

- `CLAUDE_CODE_MAX_OUTPUT_TOKENS`: Control output size
- `BASH_DEFAULT_TIMEOUT_MS`: Optimize bash timeouts
- Regular context cleanup with `/compact`

**Resource Management**:

- Monitor agent response times and success rates
- Track tool initialization overhead patterns
- Restart Claude Code between major workflows
- Implement agent performance baseline metrics

## Integration Patterns

### Performance-Aware Orchestrator Handoffs

- **Fast Agents First**: Delegate to read-only micro-agents for initial analysis
- **Progressive Enhancement**: Move from light to heavy agents only when necessary
- **Parallel Light Operations**: Multiple read-only agents can run simultaneously
- **Sequential Heavy Operations**: Chain heavy agents to minimize resource conflicts

### Orchestrator Handoffs

- Structured JSON inputs with clear operation types
- Schema-validated outputs with confidence scores
- Error states with actionable resolution steps
- Performance metrics and timing expectations

### Human Collaboration Gates

- Explicit pause points for human review
- Clear presentation of recommendations and alternatives
- Performance impact assessment for proposed changes
- Documentation of decision rationale

## Long-Term Performance Strategy

### Immediate Actions (High Impact)

1. **Optimize planning agent** (11 tools → 2 tools, reviewer-only role)
2. **Audit all agents** against performance categories
3. **Split heavy multi-purpose agents** into focused micro-agents
4. **Implement performance monitoring** for startup time tracking

### Strategic Improvements

1. **Develop performance baseline metrics** for all agents
2. **Create agent performance analytics** dashboard
3. **Implement intelligent model selection** based on complexity
4. **Establish automated performance regression detection**

---

**This guide represents comprehensive best practices based on empirical performance research, architectural analysis, and operational experience. Performance optimization is now a primary design criteria for all agent development.**
