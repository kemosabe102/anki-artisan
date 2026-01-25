# Gauntlet Plugin

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue) ![License](https://img.shields.io/badge/license-MIT-green)

**Multi-agent financial research system with specialized agents for SDLC workflows**

## Overview

Gauntlet Agents is a comprehensive multi-agent orchestration system built for Claude Code, featuring:

- **Agents**: Specialized for research, planning, implementation, testing, and review across OODA loop phases

- **Commands**: Slash commands for SDLC workflows (`/spec`, `/plan`, `/tasks`, `/implement`, `/git`)

- **Skills**: Automated code review system with modular skill-based architecture

- **Hooks**: Security validation, artifact cleanup, session handoffs, and development automation

- **OODA Loop**: Observe-Orient-Decide-Act orchestration framework with 44% focus on ORIENT phase

## Installation

### As Project Configuration (Current)

```bash































# Clone repository































git clone https://github.com/kemogsport/gauntlet-agents.git































cd gauntlet-agents































































# Install dependencies































uv python install 3.13































uv venv --python 3.13































uv sync































































# Start Claude Code - agents/commands auto-discovered































claude































```

### As Plugin (Future)

#### Via Marketplace

```bash































claude plugin install gauntlet@marketplace































```

#### Via Git Repository

code-quality

```bash































claude plugin install gauntlet@git+https://github.com/kemogsport/gauntlet-agents.git































```

#### Via Local Archive

```bash































# Download release archive































claude plugin install ./gauntlet-1.0.0-alpha.tar.gz































```

## Components

### Agents

**Research (5 agents)**:

- `researcher-lead`: Research planning and coordination (spawns researcher workers in parallel)

- `researcher-codebase`: Local code analysis (10:1 compression, pattern discovery)

- `researcher-web`: External research (SSRF-protected, OWASP integration)

- `researcher-library`: Official library docs via Context7 MCP server

- `context-readiness-assessor`: Context quality gates (0.5 threshold, max 3 iterations)

**Planning (5 agents)**:

- `planning`: Business context enhancement

- `architecture`: Technical design addition

- `architecture`: Production readiness validation

- `planning`: Business alignment reviews

- `planning`: Task list generation from plans

**Implementation (4 agents)**:

- `development`: Feature implementation with pre-flight validation

- `development`: Hypothesis-driven debugging (root cause analysis)

- `development`: Behavior-preserving refactoring

- `claude-code-ecosystem`: Agent lifecycle management (quality evaluation, migrations)

**Testing (3 agents)**:

- `test-runner`: Test execution and validation (deprecated - use code-quality)

- `code-quality`: Test generation specialist (AAA pattern, pytest fixtures)

- `code-quality`: Test execution, failure categorization (APPLICATION_BUG/TEST_BUG/ENVIRONMENT/FLAKY), delegation routing

**Review (4 agents)**:

- `code-reviewer`: Code quality validation (self-correcting review loops)

- `planning`: Specification quality assessment

- `tech-debt-investigator`: Technical debt analysis (duplicate functionality detection)

- `sast-scanner`: Security scanning (Semgrep integration)

**Infrastructure (2 agents)**:

- `deployment-release`: Kubernetes deployment (local dev via scripts)

- `portfolio-compliance-analyzer`: Portfolio compliance analysis (IPS constraints, rebalancing)

**Orchestration (4 agents - OODA)**:

- `intent-analyzer`: Request decomposition (OBSERVE phase)

- `hypothesis-former`: Solution hypotheses (DECIDE phase)

- `contingency-planner`: Failure mode analysis (DECIDE phase)

- `source-control`: Git/GitHub operations (CI monitoring, PR automation)

**Documentation (2 agents)**:

- `documentation`: Documentation health management

- `planning` / `architecture`: Plan enrichment

**Utilities (7 agents)**:

- `workflow`: `.claude/**` ecosystem manager (config, commands, hooks, schemas)

- `claude-code-ecosystem`: Agent prompt quality analysis

- `feature-analyzer`: Feature specification comparison

- `documentation`: Documentation reference optimization

- `claude-code-ecosystem`: Agent lifecycle management

- `claude-code`: Claude Code configuration specialist

- `intent-analyzer`: Request parsing and decomposition

**See**: `.claude/agents/` directory for complete agent definitions

### Commands

- **`/spec`**: Create feature specifications with GitHub spec-kit integration
  - Example: `/spec "Add OAuth2 authentication support"`

  - Supports file input: `/spec file:path/to/requirements.txt`

- **`/plan`**: Generate implementation plans with architecture review
  - Example: `/plan docs/01-planning/specifications/013-plugin-distribution-system/`

- **`/tasks`**: Break down plans into executable task lists
  - Example: `/tasks docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/`

  - Multi-agent validation: 3 core + 0-2 dynamic agents

- **`/implement`**: Execute tasks with dependency tracking
  - Example: `/implement docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/`

- **`/git`**: Git workflow automation (validate, analyze, commit)
  - Example: `/git prepare` (validation without commit)

  - Example: `/git commit --groups=1,2,3` (validate and commit)

- **`/create-agent`**: Agent lifecycle management
  - Interactive mode: `/create-agent`

  - Manual template: `/create-agent --create-definition my-agent.md`

- **`/optimize-claude-md`**: Optimize CLAUDE.md size and performance

- **`/analyze-portfolio`**: Portfolio compliance analysis (financial planning prototype)

- **`/spec-review`**: Comprehensive specification review

**See**: `.claude/commands/` directory for command definitions

### Skills

**Current (1)**:

- `component-reviewer`: Automated codebase component review (quality scoring, improvement recommendations)

**Planned (7 skills - Feature 013)**:

- `research-skill`: Multi-source research coordination

- `implementation-skill`: Code development workflows

- `planning-skill`: SDLC planning (spec → plan → tasks)

- `review-skill`: Quality assurance and validation

- `git-automation-skill`: Version control automation

- `testing-skill`: Test execution and validation

- `infrastructure-skill`: Kubernetes deployment

**See**: `.claude/skills/` directory for skill definitions

### Hooks (25)

**SessionStart**:

- Load critical documentation context (`startup-eval.py`)

**PreToolUse**:

- `TodoWrite`: Task sequencing validation

- `WebFetch|WebSearch`: URL validation (SSRF prevention - block internal IPs, localhost, private networks)

- `Bash`: Command validation (block destructive operations: `rm -rf`, `git reset --hard`, `git clean -fd`)

- `Read|Write|Edit|MultiEdit`: Path validation (path traversal prevention)

**PostToolUse**:

- Feature plan template validation

- Python code auto-formatting (Ruff)

- Context7 usage logging

- Secrets detection (API keys, tokens, passwords)

**Stop**:

- Context window usage monitoring

- Phase completion summary with next steps

**See**: `.claude/hooks/` directory for hook scripts

## Usage

### Agent Invocation

Agents are automatically invoked by the orchestrator based on task requirements using domain-first thinking:

```































User: "Find all authentication patterns in packages/core/"































→ Orchestrator delegates to researcher-codebase agent































































User: "Create a spec for OAuth2 support"































→ Orchestrator uses /spec command































































User: "Fix bug in login flow"































→ Orchestrator delegates to development agent (unknown root cause = investigation work)































```

### Command Usage

```bash































# Create feature specification































/spec "Add OAuth2 authentication support"































































# Generate implementation plan































/plan docs/01-planning/specifications/013-plugin-distribution-system/































































# Generate task list































/tasks docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/































































# Execute tasks with validation































/implement docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/































































# Git workflow automation































/git commit --groups=1,2,3































































# Create new agent































/create-agent --create-definition my-agent.md































```

### Skills Usage

Skills are autonomously invoked by Claude based on context:

```































User: "Review the researcher-web agent for quality"































→ Claude activates component-reviewer skill































→ Performs automated quality analysis































→ Returns improvement recommendations































```

## Architecture

### OODA Loop Orchestration

All agents are organized by OODA phase:

- **OBSERVE (13%)**: `intent-analyzer` (request decomposition)

- **ORIENT (44% - MOST CRITICAL)**: `researcher-*` agents, `context-readiness-assessor`, analysis agents

- **DECIDE (13%)**: `hypothesis-former`, `contingency-planner`

- **ACT (28%)**: `development`, `code-quality`, `development`, `development`, review agents, `source-control`

**Key Insight**: 44% of agents in ORIENT phase - most failures stem from insufficient context gathering, not execution.

### Multi-Agent Patterns

**3 core + 0-2 dynamic agents** for comprehensive analysis:

- **Core Agents** (always included):
  - `planning`: Business alignment validation

  - `architecture`: Technical design validation

  - `tech-debt-investigator`: Duplicate functionality detection, cleanup validation

- **Dynamic Agents** (confidence >0.8):
  - `feature-analyzer`: Multi-component features, dependency graphs

  - `test-runner`: Test-heavy features, validation complexity

  - `security-reviewer`: External-facing APIs, auth/authz

  - `development`: Code quality improvements, structural changes

**Confidence Formula**: `(domain_fit × 0.6) + (unique_value × 0.3) + (cost_efficiency × 0.1)`

### Directory Structure

```































.claude/































├── .claude-plugin/           # Plugin metadata (future)































│   └── plugin.json































├── agents/                   # Agent definitions































├── commands/                 # Slash commands































├── skills/                   # Skill definitions































├── hooks/                    # Lifecycle hooks































│   ├── hooks.json           # Hook configuration (plugin format)































│   └── *.py                 # Hook scripts































├── docs/                    # Reference documentation































│   ├── guides/              # Agent selection, file operations, research patterns































│   ├── schemas/             # JSON schema definitions































│   └── templates/           # Report and configuration templates































├── templates/               # Development templates































└── settings.json            # Project configuration































```

## Configuration

### OpenTelemetry Monitoring Setup

The file includes OpenTelemetry (OTEL) environment variables for distributed tracing, metrics, and logging.

**Quick Start**:

1. **Copy example template**: `cp .claude/settings.json.example .claude/settings.json`

2. **Choose scenario**:
   - **Local dev with monitoring**: Keep default values (OTEL collector at localhost:4317)

   - **Local dev without monitoring**: Set `OTEL_SDK_DISABLED=true`

   - **Production/staging**: Update endpoint and resource attributes

3. **Customize values**:
   - `OTEL_SERVICE_NAME`: Add environment suffix (`-dev`, `-staging`, `-prod`)

   - `OTEL_RESOURCE_ATTRIBUTES`: Update `developer` name and environment tags

4. **Restart Claude Code session**

**Example Scenarios**:

```json

// Local development with monitoring (default)

"OTEL_SDK_DISABLED": "false",

"OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",

"OTEL_SERVICE_NAME": "claude-code-orchestrator",

"OTEL_RESOURCE_ATTRIBUTES": "environment=local,developer=YOUR_NAME"



// Local development without monitoring

"OTEL_SDK_DISABLED": "true"



// Kubernetes staging

"OTEL_EXPORTER_OTLP_ENDPOINT": "http://otel-collector.observability.svc.cluster.local:4317",

"OTEL_SERVICE_NAME": "claude-code-orchestrator-staging",

"OTEL_RESOURCE_ATTRIBUTES": "environment=staging,cluster=staging-cluster,version=1.2.3"

```

**Documentation**: See `.claude/settings.json.example` for complete variable explanations, troubleshooting guides, and vendor-specific examples (Datadog, Honeycomb, SignOz).

**Start Observability Stack** (local development):

```bash

docker-compose -f k8s/local/docker-compose.yml up -d

# Verify: http://localhost:16686 (Jaeger), http://localhost:9090 (Prometheus), http://localhost:3000 (Grafana)

```

## Documentation

**Quick Start**:

- Agent Selection: `.claude/docs/01-guides/agents/agent-selection-guide.md`

- File Operations: `.claude/docs/01-guides/file-ops/file-operation-protocol.md`

- Orchestration: `.claude/docs/03-workflows/orchestrator-workflow.md`

- Research Patterns: `.claude/docs/00-core/research-patterns.md`

**Complete Index**: `.claude/docs/02-reference/DOC-INDEX.md`

**Top 10 Reference Docs**:

1. `.claude/docs/03-workflows/orchestrator-workflow.md` - Agent coordination, delegation patterns

2. `.claude/docs/01-guides/agents/agent-selection-guide.md` - Domain-first thinking framework

3. `.claude/docs/01-guides/file-ops/file-operation-protocol.md` - File editing protocol, rate limiting

4. `.claude/docs/00-core/research-patterns.md` - Research delegation strategies

5. `.claude/docs/01-guides/performance/tool-parallelization-patterns.md` - Read/Grep/Write efficiency

6. `.claude/docs/01-guides/agents/base-agent-pattern.md` - Agent design standards

7. `.claude/docs/01-guides/agents/agent-standards-extended.md` - Comprehensive agent patterns

8. `docs/04-guides/development/spec-driven-development.md` - SDD methodology

9. `docs/01-planning/custom/confidence-based-delegation-framework.md` - Agent selection confidence

10. `.claude/docs/00-core/ooda-loop-framework.md` - ORIENT phase gating

## Development

### Requirements

- Python 3.13+

- [uv](https://github.com/astral-sh/uv) package manager

- Git + [GitHub CLI](https://cli.github.com/)

### Setup

```bash































# Install Python 3.13 and create environment































uv python install 3.13































uv venv --python 3.13































uv sync































































# Verify installation































uv run python -c "import pydantic_ai; print('✅ Ready!')"































```

### Testing

```bash































# Run all tests































uv run pytest































































# Unit tests only































uv run pytest tests/unit/































































# With coverage































uv run pytest -v --cov=packages































































# Specific test































uv run pytest -k "test_name"































```

### Code Style

- **Formatting**: Ruff (auto-formats on save via PostToolUse hook)

- **Type Hints**: Required (Python 3.13+)

- **Imports**: Standard → Third-party → Local (absolute imports)

- **Async**: Required for I/O operations

- **Coverage**: >80% required

## Roadmap

### Current Phase: Plugin Distribution System (Feature 013)

- [x] Phase 1: Hybrid project+plugin structure (this release)

- [ ] Phase 2: 7-skill migration (research, implementation, planning, review, git-automation, testing, infrastructure)

- [ ] Phase 3: Marketplace submission

### Future Enhancements

- Enhanced observability (OpenTelemetry integration)

- Context7 MCP server integration

- Marketplace distribution

- Cross-project agent sharing

- Agent performance analytics

- Skill-based modularization

## Security

### OWASP LLM Top 10 Compliance

**Addressed Risks**:

- **LLM01: Prompt Injection** ✅ COMPLIANT
  - Input sanitization (path validation, command filtering)

  - Agent definition validation (dangerous pattern detection)

  - No external content processing (WebFetch domain-whitelisted)

- **LLM02: Insecure Output Handling** ✅ COMPLIANT
  - Schema validation (base-agent.schema.json compliance)

  - Secrets detection in outputs (API keys, tokens, passwords)

  - Path validation for all file operations

- **LLM07: Insecure Plugin Design** ✅ COMPLIANT
  - Tool permission validation (domain boundaries)

  - Least privilege enforcement (agent-specific tool access)

  - Input validation for all tool calls

- **LLM08: Excessive Agency** ✅ COMPLIANT
  - Permission enforcement (PreToolUse hooks)

  - Path traversal prevention

  - Destructive command blocking (`rm -rf`, `git reset --hard`)

  - Approval requirements (git push, dependency changes)

### Security Features

- **PreToolUse Hooks**: Block dangerous operations before execution

- **Path Validation**: Prevent directory traversal attacks

- **URL Validation**: SSRF prevention (block internal IPs, private networks)

- **Command Whitelisting**: Only approved Bash commands allowed

- **Secrets Detection**: Scan outputs for API keys, tokens, passwords

- **Audit Trail**: All operations logged for review

## Contributing

Contributions welcome! Please see CONTRIBUTING.md (TBD).

### Development Guidelines

1. **Branch First**: Always create feature branches (`feature/NNN-description`)

2. **Test First**: Write tests before implementation

3. **Validate**: Use `/git prepare` or `scripts/prepare-code-review.py --fast`

4. **Document**: Update relevant documentation

5. **PR Process**: Create PR → Address feedback → Squash & merge

## License

MIT License - See LICENSE file for details.

## Support

- **Issues**: https://github.com/kemogsport/gauntlet-agents/issues

- **Documentation**: `.claude/docs/02-reference/DOC-INDEX.md`

- **Project Repository**: https://github.com/kemogsport/gauntlet-agents

## Version

**Current**: 1.0.0-alpha (2025-01-27)

**Next**: 1.1.0 (7-skill migration, marketplace submission)

---

**Built with Claude Code** | **Powered by Multi-Agent Orchestration** | **OODA Loop Architecture**

## Additional Guides

For comprehensive guides on agent development, workflows, and best practices, see:

- [Agent Development Guide Index](.claude/docs/01-guides/readme.md)
- [File Operations Protocol](.claude/docs/01-guides/file-ops/file-operation-protocol.md)
- [Workflow Patterns](.claude/docs/03-workflows/WORKFLOW.md)
- [Agent Selection Guide](.claude/docs/01-guides/agents/agent-selection-guide.md)

