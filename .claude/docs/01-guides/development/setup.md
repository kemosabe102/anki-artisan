# Gauntlet Agents: Environment Setup & Tooling

---

This document contains all environment setup, development tooling, and troubleshooting guidance for the Gauntlet Agents project.

## Critical Platform Requirements

### ⚠️ Windows Unicode/Charmap Compatibility

**SOLUTION:** Enable UTF-8 support in Windows Settings → Time & Language → Administrative language settings → Check "Beta: Use Unicode UTF-8 for worldwide language support" → Restart.

**If UTF-8 setting unavailable:** Use ASCII alternatives in console output only:

- `[OK]` `[ERROR]` `[WARN]` instead of ✅❌⚠️
- `>>>` `*` `->` instead of 🚀•▶️

**Rule:** Avoid Unicode characters in print statements, logging, and CLI output on Windows cp1252 systems.

## Development Environment Setup

### Language & Tools

- **Python:** 3.13+ (see `pyproject.toml` for current version and dependencies)
- **Package Manager:** UV (ONLY dependency manager - faster than pip, replaces pip/venv entirely)
- **Linter/Formatter:** Ruff (configuration in `pyproject.toml`)
- **Testing:** pytest with asyncio support and custom markers
- **Type Checking:** mypy (gradual strictness progression)
- **LLM Providers:** OpenAI and Google Gemini via Pydantic AI
  - **Model Routing:** Opus for deep reasoning (planner, debugger), Sonnet for execution (development, test-runner, reviewer)

### **CRITICAL:** UV-Only Dependency Management

**This project uses UV exclusively. No pip, requirements.txt, or manual venv commands.**

```bash
# Initial project setup (run ONCE when starting)
uv python install 3.13                    # Install Python 3.13 for UV
uv venv --python 3.13                     # Create virtual environment
uv sync                                    # Install all dependencies from pyproject.toml

# Adding new dependencies (see Context7 validation in Tier 4)
uv add package-name                        # Add to pyproject.toml and install
uv add --dev package-name                  # Add development dependency
uv add --optional ollama package-name     # Add to optional dependency group

# Daily usage - ALWAYS use uv run
uv run python script.py                   # Run Python with project environment
uv run pytest                             # Run tests with proper dependencies
uv run python scripts/prepare-code-review.py  # Run development scripts
```

### 🚨 CRITICAL: Always Use UV Run Commands

- **NEVER use bare `python`, `pytest`, `mypy` commands** - These use system Python
- **ALWAYS use `uv run python`** - Ensures project virtual environment
- **ALWAYS use `uv run pytest`** - Ensures proper package resolution
- **ALWAYS use `uv run mypy`** - Ensures correct dependency versions
- **Exception:** Only use bare commands if explicitly documented in troubleshooting

## CLI Efficiency Principle

**[CRITICAL] Script-First Development Philosophy**

**Core Rule:** Use existing scripts instead of manual command chains. If you run 2+ commands repeatedly, find or create a script.

**Script Discovery:**

- **Code Review:** `scripts/prepare-code-review.py` - **MAIN WORKFLOW** - Complete code review preparation pipeline
- **Development:** `scripts/development/` - CI validation, development utilities
- **Deployment:** `scripts/deployment/` - Local K8s deployment, self-contained validation with auto port-forwarding
- **Monitoring:** `scripts/monitoring/` - SLO validation, metrics collection
- **Validation:** `scripts/validation/` - Data validation, intake testing
- **Troubleshooting:** `scripts/troubleshooting/` - CI debugging, container auth
- **Testing:** `scripts/testing/run_tests.py` - Targeted test execution

**Implementation Priority:**

1. **IDENTIFY WORKFLOW** - Recognize when you're executing a process (preparing for code review, deploying, validating changes)
2. **CHECK** - Look for existing script in `scripts/` directory that handles this workflow
3. **USE** - Execute the script for the entire process rather than individual commands
4. **ASK TO CREATE** - If no script exists for a workflow you just executed, ask human: "I noticed you ran [workflow description]. Should we create a script for this process?" Human decides whether to create the script.

**Example:** Instead of running manual multi-step processes, use the consolidated script which handles the complete workflow in one command.

**Efficiency Metrics:** 1 command > 3 commands. Consistent > variable. Predictable > custom.

**This principle governs ALL development workflows below - always seek script-based solutions first.**

## Troubleshooting

### UV Dependency Issues [MOST COMMON]

**When you see ModuleNotFoundError or dependency issues:**

#### 1. First-Time Setup Issues

```bash
# Problem: Fresh checkout or corrupted environment
# Solution: Clean setup
uv python install 3.13          # Ensure Python 3.13 available
uv venv --clear --python 3.13   # Create clean virtual environment
uv sync --reinstall              # Fresh install of all dependencies
```

#### 2. Windows-Specific UV Issues

```bash
# Problem: "The file cannot be accessed by the system" or permission errors
# Root Cause: Windows Store Python vs UV Python conflict

# Solution A: Use proper Python version
uv python install 3.13
uv venv --clear --python 3.13
uv sync

# Solution B: If Solution A fails, check Python paths
uv python list                   # Check available Python versions
# Look for non-WindowsApps paths, use those versions
```

#### 3. Missing Dependencies (pydantic_ai, etc.)

```bash
# Problem: Import errors for packages that should be installed
# Root Cause: Using system Python instead of UV environment

# WRONG (causes import errors):
python script.py                 # Uses system Python
pytest                          # Uses system pytest

# CORRECT (uses UV environment):
uv run python script.py         # Uses project virtual environment
uv run pytest                   # Uses project dependencies
```

#### 4. Dependency Version Conflicts

```bash
# Problem: Package version conflicts or incompatible versions
# Solution: Clean reinstall
uv sync --reinstall             # Reinstall all packages
uv pip check                    # Verify no conflicts remain
```

### Import Error Resolution [STOP-THINK-FIX]

**When you see ModuleNotFoundError:**

1. **STOP** - Do not install the package immediately
2. **CHECK UV FIRST** - 90% of import errors are UV usage issues:
   - Are you using `uv run` commands? (See Development Environment Setup)
   - Is the dependency installed? Use `uv pip list | grep package-name`
   - Is your virtual environment working? Check with environment validation commands below
3. **ANALYZE** - Check the import chain to understand why it's needed
   - Is this module actually used in our simplified architecture?
   - Is this a leftover from the complex multi-agent system?
4. **VERIFY** - Check if the dependency is in `pyproject.toml`
   - If not listed, it's likely unnecessary legacy code
5. **FIX** - Choose the right solution:
   - **Use uv run** if dependency exists but not found (most common)
   - **Remove the import** if it's legacy code
   - **Add to pyproject.toml** only if truly needed (validate with Context7 first)

**Red flag:** If fixing one import reveals another missing package, you're in legacy code. Delete it instead of fixing it.

### Environment Validation

Use UV run commands (see Development Environment Setup) to test:

- `python -c "import pydantic_ai; print('Environment OK')"`
- `python -c "import pydantic_ai, openai, pydantic; print('All core dependencies working')"`
- `python -c "import sys; print('Python path:', sys.executable)"` (should show project .venv path)

### **IMPORTANT:** Dependency Management Migration Complete
