# Changelog

All notable changes to Gauntlet Agents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

**7-Skill Modularization**:

- `research-skill`: Multi-source research coordination (researcher-lead, researcher-codebase, researcher-web, researcher-library)
- `implementation-skill`: Code development workflows (development, development)
- `planning-skill`: SDLC planning (planning, architecture, planning)
- `review-skill`: Quality assurance (code-quality, planning, tech-debt-investigator, sast-scanner)
- `git-automation-skill`: Version control (git-github, CI monitoring)
- `testing-skill`: Test workflows (code-quality, code-quality)
- `infrastructure-skill`: Deployment (deployment-release)

**Marketplace Submission**:

- Plugin manifest validation
- Distribution pipeline
- Version management
- Documentation polish

**Enhanced Observability**:

- OpenTelemetry integration (Feature 006)
- Prometheus metrics
- Jaeger tracing
- Agent performance analytics

**Context7 Integration**:

- Library documentation via MCP server
- Standards synchronization
- Best practices research

## [1.0.0-alpha] - 2025-01-27

### Added

**Plugin Infrastructure**:

- Initial plugin manifest (`.claude-plugin/plugin.json`) for future marketplace distribution
- Hybrid project + plugin structure support (dual mode: git-based project OR installed plugin)
- CI export pipeline (`scripts/ci/export-plugin.sh`) for automated plugin packaging
- Export configuration (`.export-config.json`) defining exportable files
- Plugin hooks configuration (`hooks/hooks.json`) alongside project configuration (`settings.json`)
- Plugin distribution documentation (README.md, CHANGELOG.md)

**Core Components**:

- Specialized agents across OODA loop phases (research, planning, implementation, testing, review)
- Slash commands for SDLC workflows (/spec, /plan, /tasks, /implement, /git, etc.)
- Component-reviewer skill (automated code review)
- Lifecycle hooks (security, validation, cleanup, handoff)
- Comprehensive reference documentation

**Agents by Category**:

- **Research (5 agents)**:
  - `researcher-lead`: Research planning and coordination (spawns workers in parallel, max 3 iterations)
  - `researcher-codebase`: Local code analysis (10:1 compression, pattern discovery)
  - `researcher-web`: External research (SSRF-protected, domain whitelist, OWASP integration)
  - `researcher-library`: Official library docs via Context7 MCP server
  - `context-readiness-assessor`: Context quality gates (0.5 threshold, 4-component scoring)

- **Planning (6 agents)**:
  - `/spec` command: Feature specification creation (SPEC.md, GitHub spec-kit integration)
  - `planning`: Business context enhancement
  - `architecture`: Technical design addition
  - `architecture`: Production readiness validation
  - `planning`: Business alignment reviews
  - `planning`: Task list generation from plans

- **Implementation (4 agents)**:
  - `development`: Feature implementation with pre-flight validation
  - `development`: Hypothesis-driven debugging (root cause analysis)
  - `development`: Behavior-preserving refactoring
  - `claude-code-ecosystem`: Agent lifecycle management (quality evaluation, migrations)

- **Testing (3 agents)**:
  - `test-runner`: Test execution and validation (deprecated - use code-quality)
  - `code-quality`: Test generation specialist (AAA pattern, pytest fixtures, coverage analysis)
  - `code-quality`: Test execution, failure categorization (APPLICATION_BUG/TEST_BUG/ENVIRONMENT/FLAKY), delegation routing

- **Review (4 agents)**:
  - `code-quality`: Python code quality validation (self-correcting review loops, max 3 retries)
  - `planning`: Specification quality assessment
  - `tech-debt-investigator`: Technical debt analysis (duplicate functionality detection, cleanup validation)
  - `sast-scanner`: Security scanning (Semgrep integration, OWASP patterns)

- **Infrastructure (2 agents)**:
  - `deployment-release`: Kubernetes deployment (local dev via scripts: setup-k8s-secrets.sh, deploy-local-k8s.sh)
  - `portfolio-compliance-analyzer`: Portfolio compliance analysis (IPS constraints, rebalancing recommendations, tax optimization)

- **Orchestration (4 agents - OODA)**:
  - `intent-analyzer`: Request decomposition (OBSERVE phase)
  - `hypothesis-former`: Solution hypotheses (DECIDE phase)
  - `contingency-planner`: Failure mode analysis (DECIDE phase)
  - `git-github`: Git/GitHub operations (CI monitoring, PR automation)

- **Documentation (3 agents)**:
  - `documentation`: Documentation health management
  - `/spec` command: Specification creation (SDD mode)
  - `planning` / `architecture`: Plan enrichment

- **Utilities (7 agents)**:
  - `workflow`: `.claude/**` ecosystem manager (config, commands, hooks, schemas)
  - `claude-code-ecosystem`: Agent prompt quality analysis
  - `feature-analyzer`: Feature specification comparison
  - `documentation`: Documentation reference optimization
  - `claude-code-ecosystem`: Agent lifecycle management
  - `claude-code`: Claude Code configuration specialist
  - `intent-analyzer`: Request parsing and decomposition

**Commands**:

- `/spec`: Feature specification creation (GitHub spec-kit integration, file input support)
- `/plan`: Implementation planning (architecture review, business context)
- `/tasks`: Task list generation (3 core + 0-2 dynamic agents validation)
- `/implement`: Task execution with dependency tracking
- `/git`: Git workflow automation (validate, analyze, commit with intelligent grouping)
- `/create-agent`: Agent lifecycle management (interactive mode, manual template)
- `/optimize-claude-md`: Documentation optimization (size reduction, performance improvement)
- `/analyze-portfolio`: Portfolio compliance analysis (financial planning prototype)
- `/spec-review`: Comprehensive specification review

**Skills**:

- `component-reviewer`: Automated codebase component review (quality scoring, improvement recommendations, architecture validation)

**Hooks**:

- **SessionStart**:
  - Documentation context loading (`startup-eval.py`)

- **PreToolUse**:
  - `TodoWrite`: Task sequencing validation (parallel execution opportunities)
  - `WebFetch|WebSearch`: URL validation (SSRF prevention - block internal IPs, localhost, private networks)
  - `Bash`: Command validation (block destructive operations: `rm -rf`, `git reset --hard`, `git clean -fd`, `git checkout <file>`, `git restore <file>`)
  - `Read|Write|Edit|MultiEdit`: Path validation (path traversal prevention, protected file detection)

- **PostToolUse**:
  - Feature plan template validation (required sections)
  - Python code auto-formatting (Ruff)
  - Context7 usage logging (standards sync tracking)
  - Secrets detection (API keys, tokens, passwords in outputs)

- **Stop**:
  - Context window usage monitoring (threshold warnings)
  - Phase completion summary (next steps, blockers)

**Architecture Patterns**:

- **OODA Loop Orchestration**: All agents organized by OODA phase (OBSERVE 13%, ORIENT 44%, DECIDE 13%, ACT 28%)
- **Multi-Agent Analysis**: 3 core + 0-2 dynamic agents pattern (confidence >0.8)
- **Domain-First Thinking**: Agent selection based on file location and work type
- **Context Quality Gates**: 0.5 minimum threshold before implementation
- **Self-Correcting Review Loops**: Pattern violations → fix → re-review (max 3 iterations)
- **Research Coordination**: researcher-lead spawns workers in parallel, synthesizes findings

**Documentation Structure**:

- `.claude/docs/guides/`: Agent selection, file operations, research patterns, tool parallelization
- `.claude/docs/schemas/`: JSON schema definitions extending base-agent.schema.json
- `.claude/docs/templates/`: Report and configuration templates
- `.claude/docs/`: Orchestrator workflow, agent standards, DOC-INDEX

### Changed

**Configuration**:

- Hooks configuration dual format (settings.json for project mode, hooks.json for plugin mode)
- Directory structure plugin-ready (exportable via CI pipeline)
- Documentation organization (132 files indexed in DOC-INDEX.md)

**Agent Architecture**:

- Test execution split: test-runner (deprecated) → code-quality + code-quality
- Research coordination centralized: researcher-lead coordinates all research workers
- Context assessment formalized: context-readiness-assessor with 4-component scoring

**Workflows**:

- Git automation enhanced: `/git` command with validation, analysis, intelligent grouping
- Agent creation standardized: `/create-agent` command with interactive mode
- Specification review formalized: `/spec-review` command with multi-agent analysis

### Migration Notes

**Project Mode (Current)**:

- Continue using as normal (hooks from settings.json)
- All 38 agents, 9 commands, 3 skills available
- No changes required

**Plugin Mode (Future)**:

- Export via CI (`scripts/ci/export-plugin.sh`)
- Install via marketplace OR git repository
- Dual configuration coexists safely

**Breaking Changes**:

- None (backward compatible)

### Technical Details

**OODA Distribution**:

- OBSERVE (13%): 5 agents
- ORIENT (44%): 17 agents (most critical phase)
- DECIDE (13%): 5 agents
- ACT (28%): 11 agents

**Agent Selection**:

- Domain-first thinking (file location → domain → specialist agent)
- Confidence-based delegation (≥0.5 threshold)
- Work type recognition (implementation, debugging, research, review)

**Multi-Agent Pattern**:

- 3 core agents (always): planning, architecture, tech-debt-investigator
- 0-2 dynamic agents (confidence >0.8): feature-analyzer, test-runner, security-reviewer, development
- Confidence formula: `(domain_fit × 0.6) + (unique_value × 0.3) + (cost_efficiency × 0.1)`

**Context Quality Gate**:

- 4-component scoring: Domain Familiarity (0.40), Pattern Clarity (0.30), Dependency Understanding (0.20), Risk Awareness (0.10)
- Minimum 0.5 threshold (0.0-1.0 scale)
- Max 3 research iterations

**Validation**:

- Pre-commit hooks (security, quality gates)
- Security scanning (Semgrep, OWASP patterns)
- Code quality (Ruff auto-formatting, type hints required, >80% coverage)
- Path validation (traversal prevention)
- Command validation (destructive operation blocking)

**Performance**:

- Parallel tool execution (reads, research workers)
- Sequential file operations (Windows file locking)
- Agent scaling limits (5 file modification, 5 research workers, 10 review agents)
- Orchestrator enforcement (count pending agents before spawning)

### Security

**OWASP LLM Top 10 Compliance**:

- LLM01: Prompt Injection ✅ COMPLIANT (input sanitization, agent validation)
- LLM02: Insecure Output Handling ✅ COMPLIANT (schema validation, secrets detection)
- LLM07: Insecure Plugin Design ✅ COMPLIANT (tool permissions, least privilege)
- LLM08: Excessive Agency ✅ COMPLIANT (permission enforcement, path traversal prevention)

**Security Controls**:

- PreToolUse hooks (block dangerous operations)
- Path validation (prevent directory traversal)
- URL validation (SSRF prevention)
- Command whitelisting (approved Bash commands only)
- Secrets detection (API keys, tokens, passwords)
- Audit trail (all operations logged)

## [0.0.1] - 2025-01-01

### Added

**Initial System**:

- 37-agent system (later expanded to 38)
- OODA loop orchestration framework
- Multi-agent analysis patterns
- Comprehensive documentation system (220+ files)
- Slash command infrastructure (9 commands)
- Hooks system with security validation
- Project configuration in `.claude/settings.json`

**Core Workflows**:

- Specification creation (`/spec`)
- Implementation planning (`/plan`)
- Task generation (`/tasks`)
- Git automation (`/git`)
- Agent lifecycle management (`/create-agent`)

**Research System**:

- researcher-lead coordination
- researcher-codebase (local analysis)
- researcher-web (external research)
- researcher-library (Context7 integration)

**Quality Gates**:

- Pre-commit validation
- Self-correcting review loops
- Context quality assessment
- Multi-agent analysis (3 core + 0-2 dynamic)

---

## Version Numbering

- **Major (X.0.0)**: Breaking changes, major architecture shifts
- **Minor (x.Y.0)**: New features, agents, skills (backward compatible)
- **Patch (x.y.Z)**: Bug fixes, documentation updates

## Release Process

1. Update version in `plugin.json` (when plugin format ready)
2. Document changes in CHANGELOG.md (this file)
3. Create git tag: `git tag vX.Y.Z`
4. Push tag: `git push origin vX.Y.Z`
5. GitHub Actions creates plugin archive
6. Test plugin installation locally
7. Submit to marketplace (when ready)

## Comparison to Standards

### [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

**Compliant**:

- ✅ Versions in descending order (newest first)
- ✅ Release dates in ISO 8601 format (YYYY-MM-DD)
- ✅ Grouped changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- ✅ Unreleased section at top
- ✅ Links to version comparisons (TBD when published)

### [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

**Compliant**:

- ✅ MAJOR.MINOR.PATCH format
- ✅ Pre-release identifiers (-alpha, -beta, -rc)
- ✅ Version increment rules documented
- ✅ Public API stability guarantees (agents, commands, skills)

---

**Maintained by**: Gauntlet Agents Team
**Last Updated**: 2025-01-27
**Next Review**: 2025-02-15 (7-skill migration)
