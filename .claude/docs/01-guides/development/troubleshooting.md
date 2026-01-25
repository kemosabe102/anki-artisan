# Troubleshooting Guide

Common issues and solutions for Claude Code and Gauntlet Agents.

**Quick Links**:

- [Python Environment Issues](#python-environment-issues)
- [Claude Code Issues](#claude-code-issues)
- [Testing Issues](#testing-issues)
- [Windows-Specific Issues](#windows-specific-issues)
- [Git & File Operations](#git--file-operations)

---

## Python Environment Issues

### ModuleNotFoundError

**Problem**: Python can't find installed packages when running scripts

**Symptoms**:

```bash
$ python script.py
ModuleNotFoundError: No module named 'pydantic_ai'
```

**Root Cause**: Running bare `python` command uses system Python, not the UV-managed virtual environment

**Solution**:

```bash
# ✅ CORRECT: Always use 'uv run python'
uv run python script.py

# ✅ CORRECT: Running pytest
uv run pytest tests/unit/

# ❌ WRONG: Bare python command
python script.py  # Uses system Python, not venv
```

**Why**: UV manages a project-specific virtual environment. The `uv run` prefix activates this environment automatically.

---

### Permission Errors

**Problem**: Can't install or modify packages, getting permission denied errors

**Symptoms**:

```bash
PermissionError: [Errno 13] Permission denied: '...'
Error: Failed to install package
```

**Root Cause**: Corrupted virtual environment or conflicting Python installations

**Solution**:

```bash
# Clear and rebuild virtual environment
uv venv --clear --python 3.13 && uv sync

# If issues persist, check UV installation
uv --version

# Reinstall UV if needed (Windows)
pip install --upgrade uv
```

**Prevention**: Always use `uv add package-name` instead of `pip install`

---

### Dependency Sync Issues

**Problem**: Project dependencies out of sync after pulling changes

**Symptoms**:

```bash
ImportError: cannot import name 'X' from 'package'
# Or missing packages after git pull
```

**Solution**:

```bash
# Sync dependencies with pyproject.toml
uv sync

# If adding new dependency
uv add package-name  # Updates pyproject.toml + lockfile

# Verify environment
uv run python -c "import pydantic_ai; print('✅ Ready!')"
```

---

## Claude Code Issues

### Changes Not Appearing

**Problem**: Modified files don't show updated content in Claude Code session

**Symptoms**:

- Agent definitions not recognized after editing
- Hooks not executing after modification
- Commands not available after creation

**Root Cause**: Claude Code caches certain file types at session start

**Solution**:

**Files Requiring Restart** (NEW files only):

```
✅ Restart Required:
- New agents: `.claude/agents/*.md`
- New hooks: `.claude/hooks/*.py`
- New commands: `.claude/commands/*.md`

❌ No Restart Needed:
- Modifying existing agents/hooks/commands
- Any changes to `.claude/docs/**`
- Main codebase changes (packages/**, tests/**)
```

**How to Restart**: Exit and restart Claude Code CLI session

---

### Agent Not Found Error

**Problem**: Claude Code can't find a sub-agent when delegating

**Symptoms**:

```
Error: Agent 'agent-name' not found
```

**Root Cause**: Agent name mismatch or missing agent file

**Solution**:

```bash
# 1. Check agent file exists
ls .claude/agents/agent-name.md

# 2. Verify frontmatter 'name' field matches filename
# File: .claude/agents/development.md
# Frontmatter: name: development  ✅ MATCH

# 3. Check for typos in delegation
Task(agent="development", ...)  # Must match exactly
```

---

### Session Handoff Issues

**Problem**: Context lost between Claude Code sessions

**Symptoms**:

- Agent doesn't remember previous work
- Need to re-explain project context

**Solution**:

```bash
# 1. Check handoff file was generated
ls .claude/handoffs/*.md

# 2. Use startup-eval.py hook to load handoff
# (Automatically runs on session start)

# 3. Manual handoff review
Read .claude/handoffs/YYYY-MM-DD-HH-MM.md
```

---

## Testing Issues

### Tests Not Found

**Problem**: pytest can't locate test files

**Symptoms**:

```bash
$ uv run pytest test_file.py
ERROR: file or directory not found: test_file.py
```

**Root Cause**: Incorrect working directory or relative path

**Solution**:

```bash
# ✅ CORRECT: Use full path from project root
uv run pytest tests/unit/test_file.py

# ✅ CORRECT: Run all tests in directory
uv run pytest tests/unit/

# ✅ CORRECT: Run specific test function
uv run pytest tests/unit/test_file.py::test_function_name

# ❌ WRONG: Relative path without directory
uv run pytest test_file.py
```

**Working Directory**: Always run pytest from `C:/Users/kemos/Repos/gauntlet-agents/`

---

### Tests Pass Locally But Fail in CI

**Problem**: Tests pass with `uv run pytest` but fail in GitHub Actions

**Root Cause**: Environment differences, missing dependencies, or platform-specific issues

**Solution**:

```bash
# 1. Run FULL validation matching CI exactly
scripts/prepare-code-review.py --full

# 2. Check for platform-specific tests (Windows vs Linux)
# Mark platform-specific tests with pytest.mark.skipif

# 3. Review CI logs for specific failure
gh run view --log-failed
```

---

### Import Errors in Tests

**Problem**: Tests can't import modules from packages/

**Symptoms**:

```python
ModuleNotFoundError: No module named 'packages'
```

**Root Cause**: Incorrect import path or missing package installation

**Solution**:

```python
# ✅ CORRECT: Use absolute imports
from packages.core.service import Service

# ❌ WRONG: Relative imports
from ..packages.core.service import Service

# Ensure packages installed in editable mode
uv sync  # Installs local packages
```

---

## Windows-Specific Issues

### "File Modified Since Read" Bug

**Problem**: Edit/Write operations fail with "file has been modified since it was read"

**Symptoms**:

```
Error: The file has been modified since it was read
# Even though no external modifications occurred
```

**Root Cause**: Claude Code v1.0.111+ has overly sensitive file modification detection triggered by Windows path format mixing

**Solution**:

**MANDATORY Path Rules**:

```bash
# ✅ CORRECT: Relative paths with forward slashes
docs/guides/file.md
.claude/agents/agent.md

# ❌ WRONG: Absolute paths
C:/Users/kemos/Repos/gauntlet-agents/docs/guides/file.md

# ❌ WRONG: Backslashes
docs\guides\file.md

# ❌ WRONG: Mixed separators
C:\path/to\file
```

**Sequential Edits on .claude/ Files**:

```markdown
# ✅ CORRECT: Sequential with re-read

1. Read file.md
2. Edit file.md (change 1)
3. Wait for completion
4. Read file.md AGAIN (IMPORTANT!)
5. Edit file.md (change 2)
6. Wait for completion

# ❌ WRONG: Parallel edits on same file

1. Read file.md
2. Edit file.md (change 1)
3. Edit file.md (change 2) ← FAILS
```

**Emergency Fallback**:

```bash
# Downgrade to version before regression bug
npm install -g @anthropic-ai/claude-code@1.0.100
```

**See**: CLAUDE.md (Windows + Git Bash Path Handling section) for complete path handling rules

---

### Git Bash Path Translation Issues

**Problem**: Paths work in PowerShell but fail in Git Bash

**Root Cause**: MSYS2 translates paths between Windows and POSIX formats

**Solution**:

```bash
# ✅ CORRECT: Use POSIX-style paths in Git Bash
/c/Users/kemos/Repos/gauntlet-agents/  # Git Bash
C:/Users/kemos/Repos/gauntlet-agents/  # PowerShell

# Best practice: Use relative paths (work everywhere)
docs/guides/file.md
```

---

### File Locking on .claude/ Directory

**Problem**: Concurrent edits on .claude/ files fail

**Root Cause**: Windows has stricter file locking than Unix systems

**Solution**:

```markdown
# ✅ CORRECT: Sequential edits only

Edit .claude/agents/agent1.md
Wait for completion
Edit .claude/agents/agent2.md

# ❌ WRONG: Parallel edits (file locking conflict)

Edit .claude/agents/agent1.md
Edit .claude/agents/agent2.md ← May fail
```

**See**: `.claude/docs/guides/file-operation-protocol.md` for complete guidelines

---

## Git & File Operations

### "Working Tree Dirty" Error

**Problem**: Can't switch branches or pull changes

**Symptoms**:

```bash
$ git checkout feature/branch
error: Your local changes would be overwritten by checkout
```

**Solution**:

```bash
# Option 1: Stash changes
git stash
git checkout feature/branch
git stash pop

# Option 2: Commit changes
git add file1.py file2.py
git commit -m "WIP: description"
git checkout feature/branch

# Option 3: Discard changes (⚠️ DESTRUCTIVE)
git restore file1.py  # Discard specific file
git restore .         # Discard all changes
```

---

### Large Files in Git

**Problem**: Git operations slow or failing due to large files

**Symptoms**:

```bash
warning: large files detected
remote: error: File too large
```

**Solution**:

```bash
# 1. Check file sizes
git ls-files --others --exclude-standard | xargs du -sh

# 2. Add to .gitignore
echo "large-file.bin" >> .gitignore
git rm --cached large-file.bin

# 3. Review .gitignore patterns
.venv/
*.pyc
__pycache__/
.pytest_cache/
*.log
```

---

### Merge Conflicts

**Problem**: Git can't automatically merge changes

**Symptoms**:

```bash
$ git merge feature/branch
CONFLICT (content): Merge conflict in file.py
```

**Solution**:

```bash
# 1. Check conflict status
git status

# 2. Resolve conflicts manually
# Open file.py, find conflict markers:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> feature/branch

# 3. After resolving
git add file.py
git commit -m "merge: resolve conflicts in file.py"
```

**Prevention**: Pull main before creating feature branches

```bash
git checkout main
git pull
git checkout -b feature/new-feature
```

---

## Performance Issues

### Slow Tool Execution

**Problem**: Read/Grep operations taking too long

**Root Cause**: Large files or inefficient search patterns

**Solution**:

```bash
# 1. Use specific file paths instead of globbing
Read specific/file.py  # Fast
Read **/*.py           # Slow (searches all files)

# 2. Use type filters in Grep
Grep(pattern="...", type="py")  # Faster
Grep(pattern="...", glob="**/*") # Slower

# 3. Limit search scope
Grep(pattern="...", path="specific/directory/")
```

**See**: `.claude/docs/guides/tool-parallelization-patterns.md`

---

### High Token Usage

**Problem**: Hitting token limits or slow responses

**Root Cause**: Large file operations or inefficient context

**Solution**:

```bash
# 1. Use versioning strategy for large files (>22.5K tokens)
# Write new version instead of editing existing
Write path/to/file_v2.py

# 2. Delegate to sub-agents for analysis
# researcher-codebase provides compressed synthesis
Task(agent="researcher-codebase", prompt="analyze X")

# 3. Monitor context usage
# See .claude/docs/01-guides/context-monitoring-guide.md
```

---

## Agent-Specific Issues

### claude-code-ecosystem Can't Find Agent

**Problem**: claude-code-ecosystem reports agent doesn't exist

**Solution**:

```bash
# 1. Verify file exists
ls .claude/agents/agent-name.md

# 2. Check frontmatter format
---
name: agent-name  # Must match filename
description: ...
model: opus
tools: Read, Write  # Comma-separated, not YAML list
---

# 3. Validate with Glob
Glob(pattern="**/*.md", path=".claude/agents/")
```

---

### researcher-lead Executing Instead of Planning

**Problem**: researcher-lead performs research instead of creating plans

**Root Cause**: Incorrect invocation phrasing

**Solution**:

```markdown
# ✅ CORRECT: Triggers planning mode

Task(agent="researcher-lead", prompt="CREATE A RESEARCH PLAN for [objective]")

# ❌ WRONG: Triggers execution mode

Task(agent="researcher-lead", prompt="Investigate [objective]")
```

**See**: CLAUDE.md (Orchestrator-to-researcher-lead Invocation Protocol section)

---

### development Used on docs/\*\*

**Problem**: development creating documentation instead of code

**Root Cause**: Wrong agent for domain

**Solution**:

```markdown
# ✅ CORRECT: Documentation agents for docs/\*\*

docs/01-planning/specifications/** → /spec command
docs/** plans → planning, architecture
docs/\*\* tasks → planning

# ✅ CORRECT: development for packages/\*\*

packages/**, tests/**, scripts/\*\* → development

# ❌ WRONG: development for docs/\*\*

Task(agent="development", prompt="update docs/...") # NO!
```

**See**: CLAUDE.md (Agent Domain Boundaries section)

---

## Additional Resources

### Core Documentation

- **Setup Guide**: `.claude/docs/SETUP.md` - Initial setup and configuration
- **File Operation Protocol**: `.claude/docs/guides/file-operation-protocol.md` - File editing best practices
- **CLAUDE.md**: Core orchestration patterns and warnings

### Workflow Guides

- **Orchestrator Workflow**: `.claude/docs/orchestrator-workflow.md` - Agent coordination patterns
- **Research Patterns**: `.claude/docs/guides/research-patterns.md` - Research delegation strategies
- **Tool Parallelization**: `.claude/docs/guides/tool-parallelization-patterns.md` - Performance optimization

### Agent-Specific Guides

- **Agent Standards (Extended)**: `.claude/docs/agent-standards-extended.md` - Agent design standards
- **Base Agent Pattern**: `.claude/docs/guides/base-agent-pattern.md` - Standard agent structure
- **Agent Optimization Lessons**: `.claude/docs/guides/agent-optimization-lessons-learned.md` - Practical lessons

### Security & Compliance

- **Security README**: `.claude/docs/security/README.md` - Security policies
- **Allowed Domains**: `.claude/docs/security/allowed-domains.md` - WebFetch/WebSearch whitelist

---

## Still Having Issues?

If your issue isn't covered here:

1. **Check recent changes**: `git log --oneline -10`
2. **Review agent logs**: Look for error details in tool output
3. **Consult CLAUDE.md**: Search for keywords related to your issue
4. **Ask the orchestrator**: Describe the problem with symptoms and context

**Common Debugging Questions**:

- What command are you running?
- What's the exact error message?
- What file/directory are you working in?
- What did you try already?

---

**Living Document** - Add new issues and solutions as they're discovered.
