# Workflow Phases for /review Command

Detailed documentation for each of the 7 workflow phases (Phase 0-6).

---

## Phase 0: Pre-Flight Validation

**Purpose**: Verify required tools are available before starting review.

### Step 0.1: Tool Availability Check

```bash
# Required tools
git --version    # REQUIRED - abort if missing
semgrep --version # OPTIONAL - warn if missing, skip sast-scanner
```

### Step 0.2: Handle Missing Tools

**Git Missing** (BLOCKING):
```
ERROR: Git not found in PATH.
Cannot discover files for review.
Please install git: https://git-scm.com/downloads
ABORTING REVIEW.
```

**Semgrep Missing** (WARNING):
```
WARNING: Semgrep not installed.
Security scanning (sast-scanner) will be SKIPPED.
Your review will NOT include:
- OWASP Top 10 vulnerability detection
- Hardcoded secrets scanning
- Security best practice checks

To enable security scanning:
  pip install semgrep
  OR
  brew install semgrep (macOS)

Continuing with reduced coverage...
```

### Step 0.3: Adjust Agent Set

If Semgrep missing, remove sast-scanner from Phase 3:
- Core agents: code-quality, tech-debt-investigator (2 instead of 3)
- Add note to report: "Security scan skipped - Semgrep not available"

---

## Phase 1: File Discovery & Language Detection

**Purpose**: Identify code files to review and determine language-specific routing.

### Step 1.1: Git-Based File Discovery

**Input Processing** (based on source flag):

```bash
# --all (uncommitted changes)
git status --porcelain
git diff --name-only HEAD

# --branch (branch comparison)
git diff --name-only main...<branch-name>

# --commit (specific commit)
git show --name-only <commit-hash>

# --files (explicit paths)
# Validate file existence, no git command needed
```

### Step 1.2: File Filtering

**Exclusion Patterns**:
- `.claude/**`, `docs/**`, `node_modules/**`, `vendor/**`
- `.venv/**`, `__pycache__/**`, `dist/**`, `build/**`
- `*.min.js`, `*.bundle.js`, `*.min.css`
- `package-lock.json`, `yarn.lock`, `*.pyc`

**Binary Detection**: `git ls-files --eol | grep 'i/-text'`

### Step 1.3: Language Detection (Simplified)

**Primary Method**: File extension mapping (fast, reliable):
```python
EXTENSION_MAP = {
    ".py": "Python",
    ".ts": "TypeScript", 
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
}
```

**Unknown Extensions**: Files not in map are flagged:
- Add to report: "Language Gap Detected: {filename} (unknown extension)"
- These files are NOT skipped - they appear in report for manual review
- Do NOT silently ignore unknown file types

**Note**: Linguist/Pygments removed as dependencies - extension mapping is sufficient and has no external tool requirements.

**Output**: List of `(file, language)` tuples

---

## Phase 2: Agent Routing & Batching

**Purpose**: Map languages to reviewer agents and batch files efficiently.

### Step 2.1: Language Routing

Delegate to orchestrator's Agent Selection Framework:
- Calculate: `(domain_fit * 0.6) + (language_expertise * 0.3) + (availability * 0.1)`
- Threshold: >= 0.5 -> Delegate | < 0.5 -> Report gap

**Current Language Support**: Python only (code-quality: 0.95 confidence)

**Future Languages**: Architecture supports TypeScript, Go, Rust as reviewers are developed. Currently, non-Python files are flagged as "Language Gap Detected" in the report.

### Step 2.2: File Grouping

**Delegate to source-control agent** for file grouping and batch organization:
- Uses source-control's change analysis capabilities to intelligently group related files
- Max batch size: 5 files per agent
- Grouping criteria: Language-first, then directory proximity, then change type

**Scaling**:
| File Count | Batches | Pattern |
|------------|---------|---------|
| 1-5 | 1 | Single agent |
| 6-10 | 2 | Parallel batch |
| 11-20 | 3-4 | Parallel batch |
| 21+ | 5+ | Max 5 files each |

---

## Phase 3: Multi-Agent Review (Parallel Execution)

**Purpose**: Execute code review using 3 core agents + 0-2 dynamic agents.

### Core Agents (ALWAYS Run)

1. **code-quality** (or language-specific): Code quality, patterns, bugs
2. **tech-debt-investigator**: Debt metrics, hotspots, maintainability
3. **sast-scanner**: Security vulnerabilities, secrets, OWASP compliance

### Dynamic Agents (0-2, Confidence > 0.8)

**Current Status**: No dynamic review agents implemented yet. Architecture supports future additions.

**Planned Agents** (not yet available):
| Agent | Trigger Conditions | Unique Value |
|-------|-------------------|--------------|
| design-pattern-reviewer | `design/`, `architecture/`, SOLID violations | OOP pattern analysis |
| performance-reviewer | `async` changes, performance annotations | Profiling insights |
| api-contract-reviewer | API changes, OpenAPI files | Contract validation |

**For Now**: 3 core agents only. Dynamic agents will be added as reviewers are developed.

**Total**: 3 agents (core only until dynamic agents are implemented)

---

## Phase 4: Confidence-Driven Investigation

**Purpose**: Automatically increase finding confidence to >= 0.75 through research.

See `confidence-investigation.md` for complete protocol.

**Quick Reference**:
- >= 0.90: No investigation needed
- 0.75-0.89: Context7 validation (optional)
- < 0.75: MANDATORY investigation (Context7 -> Perplexity)
- < 0.50 after research: Escalate to "Open Questions"

---

## Phase 5: Finding Consolidation & Synthesis

**Purpose**: Deduplicate and prioritize findings from multiple agents.

### Hash-Based Deduplication (100% match)
```python
hash_input = f"{location}|{message}|{rule_id}"
finding_hash = sha256(hash_input)[:16]
```

### Semantic Deduplication (similarity > 0.8)
```python
similarity = (keyword_overlap * 0.5) + (location_proximity * 0.3) + (severity_match * 0.2)
```

### Synthesis Trigger
If 3+ findings with overlap > 0.7:
- Apply synthesis-and-recommendation-framework.md
- Weighted scoring: `(Impact * 0.6) / (Effort * Risk * Change)`
- Consolidate into recommendations with trade-offs

---

## Phase 6: Report Generation

**Purpose**: Generate structured, actionable review report.

### Report Structure
1. **Executive Summary**: Status, metrics, quality gates, recommendation
2. **Findings by Severity**: Critical -> High -> Medium -> Low -> Nit
3. **Tests & Coverage**: Missing tests, coverage gaps
4. **Security Notes**: OWASP Top 10, LLM Top 10, secrets
5. **Performance Notes**: Complexity, async issues, caching
6. **Investigation Summary**: Context7/Perplexity research, Open Questions
7. **Recommendations**: Should-Do (matrix-justified), Optional/Later
8. **Verification Commands**: Deterministic checks per finding

### File:Line Anchors
Format: `file.py:line` (clickable in most editors)

### Verification Commands
Prefer deterministic checks:
```bash
rg -n 'pattern' src/           # Pattern search
ruff check src/ --select S608  # Linter rule
pytest tests/security/         # Test execution
```
