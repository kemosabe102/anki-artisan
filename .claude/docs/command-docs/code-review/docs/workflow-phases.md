# Workflow Phases for /code-review Command

Detailed documentation for each of the 7 workflow phases (Phase 0-6) with checkpoint persistence.

---

## Checkpoint System

After each phase, write a checkpoint to enable resume on failure:

```json
{
  "command": "code-review",
  "session_id": "<uuid>",
  "last_completed_phase": 2,
  "timestamp": "2025-01-15T10:30:00Z",
  "state": { /* phase-specific state */ }
}
```

**Checkpoint Location**: `temp/code-review/{session_id}/checkpoint.json`

**Stale Threshold**: Checkpoints older than 24 hours are considered stale.

---

## Phase 0: Pre-Flight Validation (HYBRID)

**Purpose**: Verify required tools are available before starting review.

**HYBRID Approach**:
- **Direct**: Check git availability (blocking, required)
- **Delegate**: Check semgrep availability via Task(git-github)


### Step 0.1: Direct Git Check

```bash
# DIRECT - orchestrator executes
git --version    # REQUIRED - abort if missing
```

### Step 0.2: Delegate Semgrep Check

```
Task(
  subagent_type="git-github",
  description="Check semgrep tool availability",
  prompt="Check if semgrep is installed and available:
    
    Execute: semgrep --version
    
    Return:
    - available: boolean
    - version: string (if available)
    - install_instructions: string (if not available)"
)
```

### Step 0.3: Handle Missing Tools

**Git Missing** (BLOCKING):
```
ERROR: Git not found in PATH.
Cannot discover files for review.
Please install git: https://git-scm.com/downloads
ABORTING REVIEW.
```


**Semgrep Missing** (WARNING - from delegated check):
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

### Step 0.4: Checkpoint Write

```json
{
  "phase": 0,
  "tools_available": {
    "git": true,
    "semgrep": false
  },
  "warnings": ["Semgrep not installed - security scan skipped"],
  "agent_set": ["python-code-reviewer", "tech-debt-investigator"]
}
```

---

## Phase 1: File Discovery (DELEGATED)

**Purpose**: Identify code files to review via git-github agent.


### Step 1.1: Delegate to git-github

```
Task(
  subagent_type="git-github",
  description="Discover files for code review",
  prompt="Discover files based on source flag:
    
    Source: {source_flag}  # --all, --branch, --commit, --files
    
    For --all: git status --porcelain + git diff --name-only HEAD
    For --branch: git diff --name-only main...{branch}
    For --commit: git show --name-only {commit}
    For --files: Validate paths exist
    
    Exclusions:
    - .claude/**, docs/**, node_modules/**, vendor/**
    - .venv/**, __pycache__/**, dist/**, build/**
    - *.min.js, *.bundle.js, *.min.css
    - package-lock.json, yarn.lock, *.pyc
    
    Return:
    - files: [{path, language, change_type}]
    - total_count: number
    - language_breakdown: {language: count}"
)
```

### Step 1.2: Language Detection

**Extension Mapping** (handled by git-github agent):
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


### Step 1.3: Checkpoint Write

```json
{
  "phase": 1,
  "files": [
    {"path": "src/auth.py", "language": "Python", "change_type": "modified"},
    {"path": "src/api.py", "language": "Python", "change_type": "added"}
  ],
  "total_count": 2,
  "language_breakdown": {"Python": 2}
}
```

---

## Phase 2: Agent Routing & Batching

**Purpose**: Map languages to reviewer agents and batch files efficiently.

### Step 2.1: Delegate Batching to git-github

```
Task(
  subagent_type="git-github",
  description="Group files into review batches",
  prompt="Group files for review:
    
    Files: {file_list_from_phase_1}
    Max batch size: 5 files
    
    Grouping priority:
    1. Language (same language per batch)
    2. Directory proximity
    3. Change type
    
    Return:
    - batches: [{batch_id, language, files, agent}]"
)
```


### Step 2.2: Agent Assignment

| Language | Primary Agent | Confidence |
|----------|--------------|------------|
| Python | python-code-reviewer | 0.95 |
| TypeScript | (gap - report in output) | N/A |
| JavaScript | (gap - report in output) | N/A |

### Step 2.3: Checkpoint Write

```json
{
  "phase": 2,
  "batches": [
    {
      "batch_id": 1,
      "language": "Python",
      "agent": "python-code-reviewer",
      "files": ["src/auth.py", "src/api.py"],
      "file_count": 2
    }
  ]
}
```

---

## Phase 3: Multi-Agent Review (Parallel)

**Purpose**: Execute review using 3 core agents + 0-2 dynamic agents.

### Core Agents

1. **python-code-reviewer**: Language-specific quality review
2. **tech-debt-investigator**: Debt metrics, TDR, hotspots
3. **sast-scanner**: Security vulnerabilities, OWASP compliance

### Step 3.1: Parallel Launch

See `delegation-patterns.md` for exact Task() syntax.

Launch all core agents simultaneously:
- Task(python-code-reviewer, ...)
- Task(tech-debt-investigator, ...)
- Task(sast-scanner, ...) # If semgrep available from Phase 0


### Step 3.2: Dynamic Agent Selection (Future)

When implemented, select 0-2 additional agents if confidence > 0.8:
- design-pattern-reviewer
- performance-reviewer
- api-contract-reviewer

### Step 3.3: Checkpoint Write

```json
{
  "phase": 3,
  "raw_findings": [
    {
      "finding_id": "HIGH-001",
      "source_agent": "python-code-reviewer",
      "severity": "High",
      "confidence": 0.78,
      "location": "src/auth.py:42"
    }
  ],
  "agent_results": {
    "python-code-reviewer": {"status": "success", "finding_count": 3},
    "tech-debt-investigator": {"status": "success", "debt_score": 34},
    "sast-scanner": {"status": "skipped", "reason": "semgrep_unavailable"}
  }
}
```

---

## Phase 4: Confidence Investigation (DELEGATED)

**Purpose**: Boost finding confidence through research delegation.

### Key Change from /review

**Instead of direct MCP calls, delegate to researcher agents:**
- `researcher-external` (replaces direct Context7 and Perplexity calls, auto-routes based on query)

See `confidence-investigation.md` for complete protocol.


### Step 4.1: Route by Confidence Band

| Confidence | Action |
|------------|--------|
| >= 0.90 | No investigation |
| 0.75-0.89 | Optional Task(researcher-external) |
| < 0.75 | MANDATORY Task(researcher-external) |
| < 0.50 after research | Escalate to Open Questions |

### Step 4.2: Checkpoint Write

```json
{
  "phase": 4,
  "validated_findings": [],
  "investigation_summary": {
    "total_investigated": 5,
    "researcher_library_calls": 4,
    "researcher_web_calls": 1,
    "confidence_boosts": 3,
    "escalated_to_open_questions": 1
  }
}
```

---

## Phase 5: Consolidation & Conflict Resolution

**Purpose**: Deduplicate findings and resolve severity conflicts.

### Step 5.1: Hash Deduplication

```python
hash_input = f"{location}|{message}|{rule_id}"
finding_hash = sha256(hash_input)[:16]
```

### Step 5.2: Semantic Deduplication

```python
similarity = (keyword_overlap * 0.5) + (location_proximity * 0.3) + (severity_match * 0.2)
# Merge if similarity > 0.8
```


### Step 5.3: Severity Conflict Resolution

When multiple agents report the same issue with different severities:

```json
{
  "conflict_resolution": {
    "conflicting_agents": ["python-code-reviewer", "sast-scanner"],
    "severities_reported": ["Medium", "High"],
    "resolution_strategy": "highest_severity",
    "final_severity": "High",
    "rationale": "Security agent (sast-scanner) rated higher; security takes precedence"
  }
}
```

**Resolution Rules**:
1. **Security vs Quality**: Security agent severity wins
2. **Same Domain**: Higher confidence agent wins
3. **Tie**: Use highest severity (conservative)

### Step 5.4: Checkpoint Write

```json
{
  "phase": 5,
  "consolidated_findings": [],
  "dedup_stats": {
    "hash_duplicates_removed": 2,
    "semantic_duplicates_merged": 1
  },
  "conflicts_resolved": 1
}
```

---

## Phase 6: Report Generation

**Purpose**: Generate structured, actionable review report.

### Report Sections

1. **Executive Summary**: Status, metrics, quality gates
2. **Findings by Severity**: Critical -> High -> Medium -> Low -> Nit
3. **Investigation Summary**: Research stats, Open Questions
4. **Verification Commands**: Per-finding checks


### Checkpoint Write (Final)

```json
{
  "phase": 6,
  "status": "COMPLETE",
  "report_path": "temp/code-review/{session_id}/report.md",
  "summary": {
    "status": "APPROVED_WITH_CONDITIONS",
    "total_findings": 8,
    "critical": 0,
    "high": 2,
    "medium": 4,
    "low": 2
  }
}
```

### Checkpoint Cleanup

On successful completion, delete checkpoint file.
On failure, preserve for resume capability.
