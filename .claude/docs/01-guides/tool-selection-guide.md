---
title: "Tool Selection Guide: Built-in Tools vs Bash Commands"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Tool Selection Guide: Built-in Tools vs Bash Commands

**Purpose**: Decision framework for choosing Claude Code built-in tools (Glob/Grep/Read) vs bash commands for file operations

**Audience**: All agents, orchestrator

**Quick Reference**: For common operations, prefer built-in tools (Glob/Grep/Read) over bash commands (find/grep/wc)

---

## Core Principle

**Built-in tools are safer, faster, and more token-efficient than bash commands for file discovery and analysis.**

**When to use built-in tools**: 95% of file operations (discovery, search, content analysis)
**When to use bash**: Complex operations requiring pipes, file system operations (mkdir, cp, mv), git commands

---

## Tool Capability Comparison

### Glob vs find

| Operation | Glob Tool | find Command | Recommendation |
|-----------|-----------|--------------|----------------|
| List files by pattern | ✅ `Glob("**/*.py")` | `find . -name "*.py"` | **USE GLOB** |
| Count files | ✅ `len(Glob("**/*.py"))` | `find . -name "*.py" \| wc -l` | **USE GLOB** |
| Sorted by mod time | ✅ Default behavior | ❌ Requires `-printf` + sort | **USE GLOB** |
| Recursive search | ✅ `**/*` pattern | ✅ Default behavior | **USE GLOB** (simpler) |
| Security | ✅ Always allowed | ⚠️ `-exec`/`-delete` blocked | **USE GLOB** |

**Glob Advantages**:
- Structured output (returns list of file paths)
- No subprocess overhead
- Always sorted by modification time
- Pattern-based syntax familiar to developers

**Glob Limitations**:
- No file size information (use Read for individual files)
- No permission filtering (bash find more flexible)
- Pattern-based only (no complex predicates like `-mtime`, `-size`)

**Example**:
```python
# ✅ CORRECT: Use Glob for file discovery
files = Glob("packages/**/*.py")
test_files = Glob("tests/**/test_*.py")
all_md = Glob("docs/**/*.md")

# ❌ WRONG: Using bash find unnecessarily
Bash("find packages/ -name '*.py' -type f")
```

### Grep vs bash grep/rg

| Operation | Grep Tool | bash grep | Recommendation |
|-----------|-----------|-----------|----------------|
| Search pattern | ✅ `Grep(pattern)` | `grep -r pattern` | **USE GREP TOOL** |
| Count matches | ✅ `output_mode="count"` | `grep -r pattern \| wc -l` | **USE GREP TOOL** |
| Type filtering | ✅ `type="py"` | `--include="*.py"` | **USE GREP TOOL** (cleaner) |
| Context lines | ✅ `-A=3, -B=3, -C=3` | `grep -A 3 -B 3` | **EQUIVALENT** |
| Limit results | ✅ `head_limit=20` | `grep ... \| head -20` | **USE GREP TOOL** |
| Case insensitive | ✅ `-i=true` | `grep -i` | **EQUIVALENT** |

**Grep Tool Advantages**:
- Structured output (no parsing needed)
- Better integration with Claude Code
- Safer (no pipe chain validation required)
- Built-in result limiting (head_limit parameter)
- Three output modes: content, files_with_matches, count

**Example**:
```python
# ✅ CORRECT: Use Grep tool for pattern search
Grep("class.*Auth", output_mode="files_with_matches", type="py")
Grep("TODO", output_mode="count")
Grep("def test_", output_mode="content", -A=3, type="py")

# ❌ WRONG: Using bash grep unnecessarily
Bash("grep -r 'class.*Auth' --include='*.py'")
Bash("grep -r 'TODO' | wc -l")
```

### Read vs cat/wc/head/tail

| Operation | Read Tool | bash commands | Recommendation |
|-----------|-----------|---------------|----------------|
| File content | ✅ `Read("file.py")` | `cat file.py` | **USE READ** |
| Line count | ✅ Included in output | `wc -l file.py` | **USE READ** |
| First N lines | ✅ `Read(limit=50)` | `head -n 50` | **USE READ** |
| Middle section | ✅ `Read(offset=100, limit=50)` | `tail -n +100 \| head -n 50` | **USE READ** |
| Images/PDFs | ✅ Multimodal support | ❌ Not supported | **USE READ** |

**Read Tool Advantages**:
- Auto-truncates at 2000 lines (prevents token overflow)
- Returns line numbers (`cat -n` format)
- Multimodal (images, PDFs, Jupyter notebooks)
- No subprocess overhead
- Consistent output format across file types

**Read Tool Limitations**:
- Maximum 2000 lines per call (use offset for larger files)
- Cannot modify files (use Edit or Write)
- No real-time streaming (use bash tail -f for logs)

**Example**:
```python
# ✅ CORRECT: Use Read for file content
content = Read("packages/core/service.py")
first_100 = Read("README.md", limit=100)
lines_100_to_200 = Read("long_file.py", offset=100, limit=100)

# ❌ WRONG: Using bash cat unnecessarily
Bash("cat packages/core/service.py")
Bash("wc -l README.md")
```

---

## Security: Commands NOT Whitelisted

**These commands will FAIL with security block**:

```bash
❌ xargs     # Command injection risk
❌ du        # Not whitelisted
❌ stat      # Not whitelisted
❌ file      # Not whitelisted
❌ cd        # Doesn't persist (cwd resets between bash calls)
❌ sed       # CVE-2021-29873 vulnerability (removed from whitelist)
```

**Source**: `.claude/hooks/security/validate_command.py` - ALLOWED_COMMANDS whitelist (lines 155-229)

**Why these are blocked**:
- **xargs**: Can execute arbitrary commands (command injection vector)
- **du/stat/file**: Not in security whitelist (no business justification)
- **cd**: Technical limitation (cwd resets between bash calls in Claude Code)
- **sed**: Shell escape vulnerability (use Desktop Commander instead)

**Whitelisted bash commands** (safe to use when appropriate):
- **File operations**: `ls`, `cat`, `head`, `tail`, `wc`, `diff`
- **Search**: `grep`, `rg`, `find` (without `-exec`/`-delete`), `ag`, `ack`
- **Filesystem**: `which`, `whereis`, `pwd`, `mkdir`, `cp`, `mv`, `touch`
- **Text processing**: `echo`, `awk`, `sort`, `uniq`, `cut`, `tr`, `column`
- **Development**: `git`, `gh`, `uv`, `python`, `pytest`, `ruff`, `black`, `mypy`

**Complete whitelist**: See `.claude/hooks/security/validate_command.py` lines 155-229

---

## Decision Tree

```
Need to perform file operation?
├─ File discovery (list files by pattern)
│  └─ USE: Glob("**/*.py")
│     - Fast, structured output, sorted by mod time
│     - Example: Glob("tests/**/test_*.py")
│
├─ Search for text pattern
│  ├─ Just need file paths? → Grep(pattern, output_mode="files_with_matches")
│  ├─ Need match count? → Grep(pattern, output_mode="count")
│  └─ Need content + context? → Grep(pattern, output_mode="content", -A=3)
│
├─ Read file content
│  ├─ Full file (<2000 lines)? → Read("file.py")
│  ├─ First N lines? → Read("file.py", limit=N)
│  ├─ Middle section? → Read("file.py", offset=X, limit=N)
│  └─ Image/PDF? → Read("file.png") # Multimodal support
│
└─ Complex operation (pipes, git, filesystem mods)
   ├─ Verify command is whitelisted (see Security section above)
   └─ USE: Bash(...) if no built-in tool available
```

---

## Usage Examples

### File Discovery Examples

**List Python files**:
```python
# ✅ CORRECT: Use Glob for file discovery
files = Glob("**/*.py")
# Returns: List of all .py files, sorted by modification time

# ❌ WRONG: Using bash find
Bash("find . -name '*.py' -type f")
# Problem: Subprocess overhead, unstructured output, security validation required
```

**Count test files**:
```python
# ✅ CORRECT: Use Glob and count in Python
test_files = Glob("tests/**/test_*.py")
count = len(test_files)
# Returns: Integer count, plus list of files for inspection

# ❌ WRONG: Using bash pipe chain
Bash("find tests/ -name 'test_*.py' | wc -l")
# Problem: Two processes, pipe validation, harder to debug
```

**Find recently modified files**:
```python
# ✅ CORRECT: Glob sorts by mod time automatically
recent_files = Glob("packages/**/*.py")[:10]  # First 10 = most recent
# Returns: 10 most recently modified Python files

# ❌ WRONG: Complex bash find command
Bash("find packages/ -name '*.py' -type f -printf '%T@ %p\n' | sort -rn | head -10")
# Problem: -printf not portable, complex syntax, unnecessary
```

### Pattern Search Examples

**Find all class definitions**:
```python
# ✅ CORRECT: Use Grep tool with regex
Grep("^class \\w+", output_mode="files_with_matches", type="py")
# Returns: List of files containing class definitions

# ❌ WRONG: Using bash grep
Bash("grep -r '^class ' --include='*.py'")
# Problem: Unstructured output, requires parsing
```

**Count TODO comments**:
```python
# ✅ CORRECT: Use Grep with count mode
todo_count = Grep("# TODO", output_mode="count")
# Returns: Integer count, plus breakdown by file

# ❌ WRONG: Using bash pipe chain
Bash("grep -r '# TODO' | wc -l")
# Problem: Just a number, no file breakdown, extra subprocess
```

**Find function with context**:
```python
# ✅ CORRECT: Use Grep with context lines
Grep("def authenticate", output_mode="content", -A=5, -B=2, type="py")
# Returns: Function definition + 5 lines after, 2 lines before

# ❌ WRONG: Using bash grep
Bash("grep -A 5 -B 2 'def authenticate' --include='*.py' -r")
# Problem: Unstructured output, harder to parse
```

### File Analysis Examples

**Get file content with line numbers**:
```python
# ✅ CORRECT: Use Read (includes line numbers automatically)
content = Read("packages/core/service.py")
# Returns: Content with line numbers in "cat -n" format

# ❌ WRONG: Using bash cat
Bash("cat -n packages/core/service.py")
# Problem: Subprocess overhead, less structured output
```

**Read first 100 lines**:
```python
# ✅ CORRECT: Use Read with limit
header = Read("large_file.py", limit=100)
# Returns: First 100 lines with line numbers

# ❌ WRONG: Using bash head
Bash("head -n 100 large_file.py")
# Problem: No line numbers, subprocess overhead
```

**Read specific line range**:
```python
# ✅ CORRECT: Use Read with offset and limit
section = Read("file.py", offset=100, limit=50)  # Lines 100-150
# Returns: Lines 100-150 with line numbers

# ❌ WRONG: Using bash tail + head
Bash("tail -n +100 file.py | head -n 50")
# Problem: Two processes, pipe validation, no line numbers from original file
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Using bash when built-in tool exists

```python
# ❌ WRONG: Using bash find with xargs (xargs not whitelisted - will FAIL)
Bash("find packages/ -name '*.py' | xargs grep 'class.*Auth'")
# Problem: xargs blocked by security (command injection risk)

# ✅ CORRECT: Use Glob + Grep separately
files = Glob("packages/**/*.py")
Grep("class.*Auth", output_mode="content", type="py")
# Benefit: Structured output, no security issues, easier to debug
```

### Anti-Pattern 2: Chaining commands unnecessarily

```python
# ❌ WRONG: Using bash pipe chain for simple operation
Bash("cat file.py | wc -l")
# Problem: Two processes, pipe validation overhead

# ✅ CORRECT: Use Read (includes line count)
content = Read("file.py")
# Line count included in output metadata
# Benefit: One operation, structured output, no parsing needed
```

### Anti-Pattern 3: Using find with -exec or -delete

```python
# ❌ WRONG: Using find with -exec (BLOCKED by security)
Bash("find . -name '*.pyc' -exec rm {} \\;")
# Problem: -exec blocked by security validation (line 910)

# ✅ CORRECT: Use Glob + sequential operations
pyc_files = Glob("**/*.pyc")
for file in pyc_files:
    Bash(f"rm {file}")  # rm requires explicit approval
# Benefit: Clear what's being deleted, security validation per file
```

### Anti-Pattern 4: Using non-whitelisted commands

```python
# ❌ WRONG: Using du for file sizes (NOT whitelisted)
Bash("du -sh packages/*")
# Problem: du not in ALLOWED_COMMANDS (will fail security validation)

# ✅ CORRECT: Use built-in tools for analysis
files = Glob("packages/**/*.py")
for file in files[:10]:  # Sample first 10
    content = Read(file)
    # Analyze content directly
# Benefit: Works within security constraints, more precise control
```

### Anti-Pattern 5: Using cd command

```python
# ❌ WRONG: Using cd (doesn't persist AND blocked by security)
Bash("cd tests && pytest")
# Problem: cd blocked + doesn't persist between bash calls

# ✅ CORRECT: Use absolute paths
Bash("pytest /c/Users/kemos/Repos/gauntlet-agents/tests/")
# Benefit: Works reliably, no directory change needed
```

---

## Performance Considerations

**Built-in tools are faster**:
- No subprocess creation overhead
- Direct integration with Claude Code
- Structured output (no parsing needed)
- Sorted results by default (Glob)

**Token efficiency**:
- Bash commands require output parsing → more tokens
- Built-in tools return structured data → fewer tokens
- Example: `Grep(output_mode="count")` returns just number, `grep | wc -l` returns full output

**Parallelization**:
- Built-in tools support parallel execution (see tool-parallelization-patterns.md)
- Multiple Glob/Grep/Read calls can run simultaneously
- Bash commands require sequential execution for safety

**Example benchmark** (conceptual):
```python
# ✅ FAST: Built-in tool (200ms, structured output)
files = Glob("**/*.py")  # ~200ms, returns List[str]

# ❌ SLOW: Bash command (500ms, requires parsing)
Bash("find . -name '*.py'")  # ~500ms, returns raw text needing split()
```

---

## When Bash is Appropriate

**Complex operations requiring pipes**:
```bash
# ✅ APPROPRIATE: Complex git operation with counting
Bash("git log --oneline --since='2 weeks ago' | grep -c 'feat:'")
# Reason: No built-in tool for git log analysis
```

**File system modifications**:
```bash
# ✅ APPROPRIATE: Directory creation
Bash("mkdir -p packages/new_module/tests")
# Reason: No built-in tool for mkdir
```

**Operations not supported by built-in tools**:
```bash
# ✅ APPROPRIATE: File comparison
Bash("diff file1.py file2.py")
# Reason: No built-in diff tool
```

**Git operations**:
```bash
# ✅ APPROPRIATE: Git workflow
Bash("git add packages/core/ && git status")
# Reason: No built-in git integration
```

**Testing and execution**:
```bash
# ✅ APPROPRIATE: Running tests
Bash("uv run pytest tests/unit/ -v")
# Reason: No built-in pytest integration
```

---

## Multi-Agent File Operations

**Pattern**: When multiple agents need file information, use parallel built-in tools

```python
# ✅ EFFICIENT: Parallel Glob calls
agent1_files = Glob("packages/**/*.py")  # Agent 1
agent2_files = Glob("tests/**/*.py")     # Agent 2
agent3_files = Glob("docs/**/*.md")      # Agent 3
# All three execute in parallel

# ❌ INEFFICIENT: Sequential bash calls
Bash("find packages/ -name '*.py'")  # Wait for completion
Bash("find tests/ -name '*.py'")     # Wait for completion
Bash("find docs/ -name '*.md'")      # Wait for completion
# Sequential execution, slower
```

**See**: `.claude/docs/guides/tool-parallelization-patterns.md` for complete parallelization strategies

---

## File Operation Protocol Integration

**Primary workflow**: Try built-in tools first, fallback to bash when necessary

1. **File Discovery**: Always use Glob (never find)
2. **Pattern Search**: Always use Grep (never bash grep/rg)
3. **File Reading**: Always use Read (never cat/head/tail)
4. **File Editing**: Use Desktop Commander (edit_block, write_file)
5. **Bash Commands**: Only when no built-in tool available

**See**: `.claude/docs/guides/file-operation-protocol.md` for complete file editing protocol

---

## Platform-Specific Considerations

**Windows**:
- Built-in tools handle path separators automatically
- Bash commands require Git Bash compatibility
- Prefer built-in tools to avoid path translation issues

**Mac/Linux**:
- Both built-in tools and bash work seamlessly
- Built-in tools still preferred (faster, structured output)

**Cross-platform compatibility**:
```python
# ✅ WORKS EVERYWHERE: Built-in tools
files = Glob("**/*.py")  # Handles Windows/Mac/Linux paths

# ⚠️ PLATFORM-SPECIFIC: Bash commands
Bash("find . -name '*.py'")  # May behave differently on Windows Git Bash
```

---

## Examples

**For real-world tool usage in multi-agent workflows**, see:

- **`.claude/docs/04-examples/code-quality-example.md`** - Shows built-in tools (Read, Grep) used in code review scenarios with overlap detection and synthesis
- **`.claude/docs/04-examples/async-validation-example.md`** - Demonstrates research workflow using Read/Grep for pattern discovery across codebase

**These examples illustrate how built-in tools enable efficient parallel execution and structured output processing.**

---

## References

- **Tool Parallelization**: `.claude/docs/guides/tool-parallelization-patterns.md`
- **Security Hooks**: `.claude/hooks/security/validate_command.py`
- **File Operations**: `.claude/docs/guides/file-operation-protocol.md`
- **Base Agent Pattern**: `.claude/docs/guides/base-agent-pattern.md`
- **Temporary Directory Standards**: `.claude/docs/cleanup/temp-directory-standards.md`

---

**Last Updated**: 2025-11-05
**Confidence**: 0.92 (based on comprehensive tool analysis and security validation)
