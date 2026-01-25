# README Templates

Templates for generating README files for different project types.

---

## Python Package

```markdown
# {package_name}

{brief_description}

## Installation

```bash
uv add {package_name}
```

## Quick Start

```python
from {package_name} import {main_class}

# Basic usage example
{usage_example}
```

## Features

- {feature_1}
- {feature_2}
- {feature_3}

## API Reference

### {main_class}

{api_description}

**Methods**:
- `{method_1}({params})`: {description}
- `{method_2}({params})`: {description}

## Testing

```bash
uv run pytest
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and guidelines.

## License

{license_type}
```


---

## CLI Tool

```markdown
# {tool_name}

{brief_description}

## Installation

```bash
uv tool install {tool_name}
```

## Usage

```bash
{tool_name} [OPTIONS] COMMAND [ARGS]
```

### Commands

- `{command_1}`: {description}
- `{command_2}`: {description}
- `{command_3}`: {description}

### Examples

```bash
# {example_1_description}
{tool_name} {command_1} --option value

# {example_2_description}
{tool_name} {command_2} input.txt -o output.txt
```

## Configuration

Configuration file: `~/.config/{tool_name}/config.toml`

```toml
{config_example}
```

## License

{license_type}
```

---

## Library/Framework

```markdown
# {library_name}

{brief_description}

## Installation

```bash
{installation_command}
```

## Core Concepts

### {concept_1}
{explanation_1}

### {concept_2}
{explanation_2}

## Quick Start

```{language}
{quickstart_code}
```

## Documentation

- [Getting Started]({docs_url}/getting-started)
- [API Reference]({docs_url}/api)
- [Examples]({docs_url}/examples)

## Architecture

{architecture_overview_or_diagram}

## Community

- [Discord]({discord_url})
- [Issues]({issues_url})
- [Contributing]({contributing_url})

## License

{license_type}
```

---

## Multi-Package Monorepo

```markdown
# {project_name}

{brief_description}

## Packages

| Package | Description | Version |
|---------|-------------|---------|
| [{package_1}](./packages/{package_1}) | {desc_1} | {version_1} |
| [{package_2}](./packages/{package_2}) | {desc_2} | {version_2} |
| [{package_3}](./packages/{package_3}) | {desc_3} | {version_3} |

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Build all packages
{build_command}
```

## Development

See [DEVELOPMENT.md](./DEVELOPMENT.md) for setup and workflow.

## Documentation

- [Architecture](./docs/architecture/)
- [Contributing](./CONTRIBUTING.md)

## License

{license_type}
```

---

## Agent/Skill Documentation

```markdown
# {agent_or_skill_name}

{brief_description}

## Purpose

{detailed_purpose}

## When to Use

**Invoke when**:
- {trigger_1}
- {trigger_2}
- {trigger_3}

**DO NOT use for**:
- {anti_pattern_1}
- {anti_pattern_2}

## Workflow

### 1. {step_1_name}

{step_1_description}

### 2. {step_2_name}

{step_2_description}

## Examples

### Example 1: {example_name}

**Request**: "{user_request}"

**Approach**:
1. {approach_step_1}
2. {approach_step_2}

**Result**: {outcome}

## References

- {reference_1}
- {reference_2}

## Integration Points

**Works with**:
- `{related_agent_1}` - {relationship}
- `{related_agent_2}` - {relationship}
```

---

## Template Selection Guide

| Project Type | Detect By | Template |
|--------------|-----------|----------|
| Python Package | `pyproject.toml` with `[project]` | Python Package |
| CLI Tool | `pyproject.toml` with `[project.scripts]` | CLI Tool |
| Library/Framework | Multiple modules, public API | Library/Framework |
| Monorepo | `packages/` directory with multiple projects | Multi-Package Monorepo |
| Agent/Skill | Location in `.claude/agents/` or `.claude/skills/` | Agent/Skill Documentation |

---

## Placeholder Replacement

When populating templates, replace:
- `{package_name}`: From `pyproject.toml` name field
- `{version}`: From `pyproject.toml` version field
- `{brief_description}`: From `pyproject.toml` description or infer from code
- `{license_type}`: From `pyproject.toml` license field or LICENSE file
- `{main_class}`: Entry point from `__init__.py`
- `{usage_example}`: From tests or common patterns
- `{features}`: Extract from module structure or docstrings
- `{api_description}`: From class/function docstrings

**Never leave placeholders**: If information unavailable, ask user or use sensible default

---

## Quality Checklist for Generated READMEs

- [ ] All code blocks have language tags
- [ ] Installation commands tested (or standard for ecosystem)
- [ ] Examples are runnable (match actual API)
- [ ] Links point to existing files/URLs
- [ ] No placeholder text (TODO, FIXME, {placeholder})
- [ ] Consistent formatting (heading levels, list style)
- [ ] Version information current
- [ ] License specified clearly
