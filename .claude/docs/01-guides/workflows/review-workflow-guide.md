---
title: "Code Review Workflow Guide"
date: 2025-11-21
status: ACTIVE
tags: [workflows, code-review, multi-agent]
---

# Code Review Workflow Guide

**Purpose**: Detailed 6-phase workflow for `/review` command with confidence-driven investigation

**Quick Navigation**: [Phase 1](#phase-1-file-discovery--language-detection) | [Phase 2](#phase-2-agent-routing--batching) | [Phase 3](#phase-3-multi-agent-review) | [Phase 4](#phase-4-confidence-driven-investigation) | [Phase 5](#phase-5-finding-consolidation--synthesis) | [Phase 6](#phase-6-report-generation)

---

## Overview

The `/review` command coordinates comprehensive, multi-language code review using specialized reviewer agents with automatic confidence-driven investigation. Reviews prioritize **actionable findings with high confidence** over exhaustive coverage, using industry-standard severity levels and deduplication.

**Key Differentiators**:
1. **NO LOW-CONFIDENCE FINDINGS**: Auto-investigation ensures ≥0.75 confidence before reporting
2. **COST-OPTIMIZED RESEARCH**: 4:1 Context7:Perplexity ratio (80% free research)
3. **EVIDENCE-BASED**: Every finding includes verification commands
4. **MULTI-LANGUAGE**: Extensible routing table (Python now, Java/TypeScript P1)
5. **DESIGN-AWARE**: OOP pattern analysis, SOLID principles, code smells

---

## Phase 1: File Discovery & Language Detection

**Purpose**: Identify code files to review and determine language-specific routing

### Step 1.1: Git-Based File Discovery

**Input Processing** (based on source flag):

```bash
# --all (uncommitted changes)
git status --porcelain
git diff --name-only HEAD

# --branch (branch comparison)
git diff --name-only main...feature-branch

# --commit (specific commit)
git show --name-only <commit-hash>

# --files (explicit paths)
# Validate file existence, no git command needed
```

**Output**: List of file paths with change statistics

**Error Handling**:
- Git command fails → "Git repository not found or corrupted"
- Empty result set → "No changes detected for review"
- Permission errors → "Cannot access git repository"

### Step 1.2: File Filtering

**Exclusion Patterns** (apply to discovered files):

```yaml
excluded_directories:
  - .claude/**          # Agent configuration
  - docs/**             # Documentation (unless --focus=quality)
  - node_modules/**     # Dependencies
  - vendor/**           # Dependencies
  - .venv/**            # Virtual environment
  - __pycache__/**      # Python cache
  - dist/**             # Build artifacts
  - build/**            # Build artifacts

excluded_patterns:
  - "*.min.js"          # Minified code
  - "*.bundle.js"       # Bundled code
  - "*.min.css"         # Minified styles
  - package-lock.json   # Lock files
  - yarn.lock           # Lock files
  - "*.pyc"             # Compiled Python
  - "*.pyo"             # Optimized Python

binary_detection:
  - Use: git ls-files --eol | grep 'i/-text'
  - Filter out binary files completely
```

**Generated Files Detection** (skip review):
- `*.generated.*` pattern
- Auto-generated headers in file comments
- Vendored code markers

**Output**: Filtered list of reviewable files

### Step 1.3: Language Detection

**Primary Method**: GitHub Linguist

```bash
# Install Linguist (if not available)
gem install github-linguist

# Detect language per file
linguist <file-path>
# Output: file-path: 100% Python
```

**Fallback Method**: Pygments (if Linguist unavailable)

```python
from pygments.lexers import get_lexer_for_filename
lexer = get_lexer_for_filename('file.py')
# Returns: PythonLexer → language="Python"
```

**Extension Mapping** (if both fail):

```yaml
language_map:
  .py: Python
  .java: Java
  .ts: TypeScript
  .tsx: TypeScript
  .js: JavaScript
  .jsx: JavaScript
  .go: Go
  .rs: Rust
  .cpp: C++
  .c: C
  .cs: C#
  .kt: Kotlin
  .rb: Ruby
  .php: PHP
  .swift: Swift
```

**Unknown Extension Handling**:
1. Attempt Linguist content analysis (reads file)
2. If still unknown → Escalate to user:
   - "Cannot determine language for [file-path]"
   - "Specify language manually or skip file"
3. Provide skip option to continue review without unknown files

**Output**: List of (file, language) tuples

```json
[
  {"file": "src/auth.py", "language": "Python"},
  {"file": "src/api/routes.java", "language": "Java"},
  {"file": "tests/test_auth.py", "language": "Python"}
]
```

---

## Phase 2: Agent Routing & Batching

**Purpose**: Map languages to reviewer agents and batch files efficiently

### Step 2.1: Language Routing Table

**Language Detection → Agent Routing** (Delegated to Orchestrator):

1. **Detect language** via GitHub Linguist (primary) or Pygments (fallback)
2. **Route to agent** using Agent Selection Framework confidence scoring:
   - Calculate: `(domain_fit × 0.6) + (language_expertise × 0.3) + (availability × 0.1)`
   - Threshold: ≥0.5 → Delegate to reviewer | <0.5 → Report gap to user

3. **Current Available Reviewers**:
   - **Python**: code-quality (confidence: 0.95)
   - **Other languages**: Use Agent Selection Framework to check availability dynamically

4. **Gap Handling** (when no reviewer available):
   - Notify user: "[Language] reviewer not available (recommended: [priority])"
   - Continue review with available languages
   - Report gap in final summary with agent creation recommendation

**Delegation Pattern** (No Hard-Coded Logic):
```yaml
# Instead of maintaining static table, delegate routing decision:
Task(
  subagent_type="<selected-by-orchestrator>",
  prompt=f"Review {file_path} using {language} code review standards"
)
```

**Rationale**: Orchestrator maintains agent registry dynamically. Command specification should not duplicate agent selection logic from `agent-selection-guide.md`.

**Reference**: `.claude/docs/01-guides/agents/agent-selection-guide.md` (Framework 1: Domain-First Thinking)

### Step 2.2: File Grouping

**Delegate to source-control Agent** (File Batching Expert):

**Task**: Group files for optimal review batching
- **Max batch size**: 5 files per agent (token efficiency)
- **Grouping criteria**: Language-first, then directory proximity
- **Output**: List of file batches with assigned reviewer agents

**Delegation Pattern**:
```yaml
Task(
  subagent_type="source-control",
  prompt=f"Group {file_list} into batches (max 5 files each) by language and directory proximity"
)
```

**Rationale**: source-control agent already implements sophisticated file batching logic. Avoid duplicating this logic in command specification.

**Reference**: `.claude/agents/dev-tools/source-control.md` (file grouping and batch optimization patterns)

**Scaling Examples**:

| **File Count** | **Batches** | **Agents** | **Pattern** |
|----------------|-------------|------------|-------------|
| 1-5 files | 1 batch | 1 agent | Single agent |
| 6-10 files | 2 batches | 2 agents | Parallel batch |
| 11-20 files | 3-4 batches | 3-4 agents | Parallel batch |
| 21+ files | 5+ batches | 5+ agents | Parallel batch (max 5 files each) |

**Example Grouping Output**:

```json
[
  {
    "batch_id": 1,
    "language": "Python",
    "agent": "code-quality",
    "files": [
      "src/auth.py",
      "src/validation.py",
      "tests/test_auth.py"
    ],
    "file_count": 3
  },
  {
    "batch_id": 2,
    "language": "Python",
    "agent": "code-quality",
    "files": [
      "packages/core/data.py",
      "packages/core/models.py"
    ],
    "file_count": 2
  },
  {
    "batch_id": 3,
    "language": "Java",
    "agent": "java-code-reviewer",
    "files": [
      "src/api/routes.java",
      "src/api/handlers.java"
    ],
    "file_count": 2,
    "status": "UNAVAILABLE"
  }
]
```

---

## Phase 3: Multi-Agent Review (Parallel Execution)

**Purpose**: Execute code review using 3 core agents + 0-2 dynamic agents

### Step 3.1: Core Agents (ALWAYS Run)

**Multi-Agent Review** (Delegated to Orchestrator):

**Agent Selection** (3 core + 0-2 dynamic):
- Use Agent Selection Framework to choose appropriate reviewers based on:
  - Language detected (Python → code-quality, etc.)
  - Focus parameter (--focus=security → prioritize sast-scanner, etc.)
  - File patterns (debt analysis → tech-debt-investigator, etc.)

**Delegation Pattern**:
```yaml
# Orchestrator selects agents dynamically based on:
# - Detected languages (from Phase 2)
# - User-specified focus (--focus parameter)
# - Agent Selection Confidence ≥0.5 threshold

# Example for Python files with --focus=security:
core_agents = [
  "code-quality",  # Language match
  "sast-scanner",          # Focus match
  "tech-debt-investigator" # Default quality check
]

dynamic_agents = select_dynamic_agents(confidence_threshold=0.5)
```

**Rationale**: Orchestrator has complete agent registry and can apply Agent Selection Framework dynamically. Command should specify criteria, not hard-code agent names.

**Reference**: `.claude/docs/01-guides/agents/agent-selection-guide.md` (Multi-Agent Decision Patterns)

**Parallel Launch Pattern** (single message):

```markdown
Launching 3 core review agents in parallel...

Task(subagent_type='code-quality', prompt={
  "files": ["src/auth.py", "src/validation.py", "tests/test_auth.py"],
  "review_focus": "quality,design,security",
  "investigation_mode": "comprehensive"
})

Task(subagent_type='tech-debt-investigator', prompt={
  "scope": {"files": ["all_files_list"]},
  "debt_metrics": ["debt_score", "TDR", "hotspots"],
  "output_format": "summary"
})

Task(subagent_type='sast-scanner', prompt={
  "scan_paths": ["all_files_list"],
  "scan_depth": "comprehensive",
  "report_format": "findings_list"
})
```

### Step 3.2: Dynamic Agents (0-2, Confidence >0.8)

**Agent Selection Framework**:

```python
def calculate_dynamic_agent_confidence(file_list, change_context):
    """Calculate confidence scores for optional review agents"""

    # Example: Design pattern reviewer
    if any("design" in f or "architecture" in f for f in file_list):
        design_conf = (domain_fit * 0.6) + (unique_value * 0.3) + (cost_efficiency * 0.1)
        # domain_fit: Design/arch files present = 0.9
        # unique_value: OOP pattern analysis = 0.8
        # cost_efficiency: No overlap with core agents = 0.9
        # Total: (0.9*0.6) + (0.8*0.3) + (0.9*0.1) = 0.87 → INCLUDE

    # Example: Performance reviewer
    if any("performance" in changes or "async" in changes for changes in change_context):
        perf_conf = (0.85*0.6) + (0.75*0.3) + (0.8*0.1) = 0.815 → INCLUDE

    return sorted_agents_by_confidence
```

**Dynamic Agent Pool**:

| **Agent** | **Trigger Conditions** | **Unique Value** |
|-----------|------------------------|------------------|
| **design-pattern-reviewer** | `design/`, `architecture/`, SOLID violations | OOP pattern analysis |
| **performance-reviewer** | `async` changes, performance annotations | Profiling insights |
| **api-contract-reviewer** | API changes, OpenAPI files | Contract validation |
| **accessibility-reviewer** | UI/frontend changes | WCAG compliance |

**Confidence Threshold**: ≥0.8 to include (0-2 agents max)

**Launch Pattern** (if confidence met):

```markdown
# If design_conf = 0.87 and perf_conf = 0.815

Task(subagent_type='design-pattern-reviewer', prompt={...})
Task(subagent_type='performance-reviewer', prompt={...})
```

**Total Agents**: 3 core + 0-2 dynamic = **3-5 agents in parallel**

---

## Phase 4: Confidence-Driven Investigation (CRITICAL)

**Purpose**: Automatically increase finding confidence to ≥0.75 through research before reporting

**For EACH finding from all agents**:

### Step 4.1: Confidence Assessment

```yaml
initial_confidence_check:
  - Extract finding confidence score (0.0-1.0)
  - Route based on confidence band:
    - ≥0.90: HIGH → No investigation needed, report as-is
    - 0.75-0.89: MEDIUM → Optional investigation (Context7 only)
    - <0.75: LOW → MANDATORY investigation (Context7 → Perplexity)
```

### Step 4.2: Context7 Research (Confidence 0.75-0.89)

**Trigger**: Finding confidence between 0.75-0.89

**Research Protocol**:

```yaml
context7_validation:
  1_extract_keywords:
    - Parse finding message for library/framework names
    - Example: "FastAPI dependency injection not awaited" → ["fastapi", "async", "dependency injection"]

  2_resolve_library:
    - Use: resolve-library-id(library_name)
    - Example: resolve-library-id("fastapi") → "/fastapi/fastapi"

  3_fetch_docs:
    - Use: get-library-docs(library_id, topic)
    - Example: get-library-docs("/fastapi/fastapi", topic="async dependency injection")
    - Validate finding against official documentation

  4_update_confidence:
    - If docs confirm issue → confidence += 0.1 (cap at 0.95)
    - If docs contradict → downgrade to "Open Question" (confidence <0.5)
    - If docs ambiguous → maintain confidence, note uncertainty

  5_cite_sources:
    - Add to finding:
      - "Source: Context7 - FastAPI Official Docs (trust: 9/10)"
      - "Validated against: Async dependency injection patterns"
```

**Example**:

```markdown
Initial Finding:
- **Confidence**: 0.78 (MEDIUM)
- **Issue**: "requests.get() blocks event loop in async function"

Context7 Research:
- Library: "httpx" (async HTTP client)
- Topic: "async vs sync HTTP calls"
- Result: Docs confirm "requests library is synchronous, use httpx for async"
- Updated Confidence: 0.88 (HIGH)
- Citation: "Context7 - httpx Official Docs (trust: 9/10)"
```

### Step 4.3: Perplexity Research (Confidence <0.75)

**Trigger**: Finding confidence <0.75 (LOW confidence requires deep synthesis)

**Research Protocol**:

```yaml
perplexity_escalation:
  1_formulate_query:
    - Convert finding to research question
    - Example: "Is using requests.get() in async Python functions a blocking issue?"

  2_execute_research:
    - Use: perplexity_search(query, focus="comprehensive")
    - Synthesize from multiple authoritative sources

  3_cross_reference:
    - Validate against industry standards (OWASP, PEP, RFC)
    - Check for consensus across sources

  4_update_confidence:
    - Strong consensus → confidence = 0.80-0.90
    - Moderate consensus → confidence = 0.70-0.79
    - No consensus → confidence remains <0.70 → ESCALATE

  5_document_trail:
    - Add investigation summary to finding
    - Include Perplexity sources with URLs
    - Show confidence progression (initial → final)
```

**Example**:

```markdown
Initial Finding:
- **Confidence**: 0.65 (LOW)
- **Issue**: "Potential SQL injection in query builder"

Perplexity Research:
- Query: "Is string concatenation for SQL queries in SQLAlchemy vulnerable to injection?"
- Sources:
  - OWASP SQL Injection Prevention (A01:2021)
  - SQLAlchemy Security Best Practices
  - NIST Database Security Guidelines
- Synthesis: "Confirmed - parameterized queries required, string concat vulnerable"
- Updated Confidence: 0.88 (HIGH)
- Trail: "Researched with Perplexity: OWASP A01, SQLAlchemy security docs"
```

### Step 4.4: User Escalation (Confidence <0.5 After Research)

**Trigger**: Confidence remains <0.5 after Context7 AND Perplexity research

**Escalation Protocol**:

```yaml
escalate_to_user:
  1_document_gap:
    - Finding description
    - Initial confidence (e.g., 0.45)
    - Research attempts (Context7 result, Perplexity result)
    - Why confidence couldn't be raised

  2_provide_evidence:
    - Sources consulted
    - Conflicting information found
    - Open questions remaining

  3_recommend_action:
    - Manual review required
    - Subject matter expert consultation
    - Additional testing needed

  4_do_not_report_as_fact:
    - Move to "Open Questions" section
    - Flag as "NEEDS VERIFICATION"
    - Include uncertainty explanation
```

**Example**:

```markdown
Open Question (Escalated):
- **Issue**: "Potential race condition in cache invalidation"
- **Initial Confidence**: 0.45
- **Research Trail**:
  - Context7 (Redis docs): Ambiguous on multi-threaded cache access
  - Perplexity (3 sources): Conflicting recommendations (locks vs atomic ops)
- **Gap**: Cannot determine if current implementation is safe without:
  - Understanding thread model (single vs multi-threaded)
  - Reviewing cache access patterns across codebase
  - Testing under concurrent load
- **Recommendation**: Manual code review + load testing
- **DO NOT assume this is a bug** - insufficient evidence
```

**Investigation Summary Per Finding**:

```json
{
  "finding_id": "AUTH-001",
  "severity": "High",
  "message": "Missing null check in login handler",
  "location": "src/auth.py:45",
  "investigation_trail": {
    "initial_confidence": 0.72,
    "context7_research": {
      "library": "pydantic",
      "topic": "Optional field validation",
      "result": "Confirmed - Optional fields can be None without explicit check",
      "confidence_delta": +0.15
    },
    "final_confidence": 0.87,
    "sources": [
      "Context7: Pydantic Field Validation (trust: 9/10)"
    ]
  },
  "recommendation": "Add explicit null check or use Pydantic validation"
}
```

### Step 4.5: Investigation Error Handling

**Resilience Protocol** (Prevents API failures from blocking reviews):

**Retry Logic** (Exponential Backoff):
1. **Context7 failure** → Retry max 3 times (delays: 1s, 2s, 4s)
2. **Perplexity failure** → Retry max 2 times (delays: 2s, 4s)
3. **Both failed** → Degrade gracefully (see error scenarios below)

**Error Scenarios & Recovery**:

| **Error** | **Recovery Strategy** | **Confidence Impact** | **User Notification** |
|-----------|----------------------|----------------------|----------------------|
| Context7 rate limit | Wait + retry → Fallback to Perplexity | -0.05 | "Context7 temporarily unavailable, using Perplexity" |
| Context7 library not found | Skip Context7 → Perplexity only | -0.10 | "No official docs found for [library], using community sources" |
| Perplexity timeout | Mark finding as MEDIUM confidence | -0.15 | "Deep research incomplete, recommendation based on agent analysis" |
| Both APIs offline | Degrade to agent confidence only | -0.25 (cap at 0.50) | "External research unavailable, findings require manual validation" |
| Network connectivity loss | Retry once → Fail gracefully | -0.30 (cap at 0.45) | "Cannot reach research APIs, review incomplete" |

**Confidence Degradation Rules**:
- Single API failure → Reduce confidence by 0.10-0.15
- Multiple failures → Cap confidence at 0.50 (triggers user escalation per Phase 4)
- Document all attempts in `investigation_trail` field
- Example trail: `"Context7: 3 attempts failed (rate limit) | Perplexity: SUCCESS (+0.12 confidence)"`

**Graceful Degradation**:
```yaml
investigation_result:
  status: PARTIAL_SUCCESS
  confidence_boost: 0.08  # Lower than full success (0.15-0.20)
  investigation_trail:
    - "Context7: FAILED after 3 retries (rate limit exceeded)"
    - "Perplexity: SUCCESS - Validated against OWASP A01 documentation"
    - "Final confidence: 0.78 (initial 0.70 + Perplexity boost 0.08)"
  fallback_used: true
  manual_validation_recommended: false  # Still above 0.75 threshold
```

**No Infinite Retries**: Max 5 total API calls (3 Context7 + 2 Perplexity). After limit, mark finding confidence and proceed.

---

## Phase 5: Finding Consolidation & Synthesis

**Purpose**: Deduplicate and prioritize findings from multiple agents

### Step 5.1: Deduplication

**Hash-Based Deduplication** (100% match):

```python
def create_finding_hash(finding):
    """Generate deterministic hash for exact duplicate detection"""
    hash_input = f"{finding.location}|{finding.message}|{finding.rule_id}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
```

**Example**:
- Agent 1: `src/auth.py:45 | Missing null check | RULE-001` → `abc123`
- Agent 2: `src/auth.py:45 | Missing null check | RULE-001` → `abc123` (DUPLICATE)

**Semantic Deduplication** (similarity >0.8):

```python
def calculate_semantic_similarity(finding1, finding2):
    """Calculate similarity between findings using multiple signals"""

    # Step 1: Keyword overlap (0-1)
    keywords1 = set(extract_keywords(finding1.message))
    keywords2 = set(extract_keywords(finding2.message))
    keyword_score = len(keywords1 & keywords2) / len(keywords1 | keywords2)

    # Step 2: Location proximity (0-1)
    if finding1.file == finding2.file:
        line_diff = abs(finding1.line - finding2.line)
        location_score = 1.0 if line_diff <= 5 else 0.5 if line_diff <= 20 else 0.0
    else:
        location_score = 0.0

    # Step 3: Severity match (0-1)
    severity_score = 1.0 if finding1.severity == finding2.severity else 0.5

    # Weighted average
    similarity = (keyword_score * 0.5) + (location_score * 0.3) + (severity_score * 0.2)
    return similarity
```

**LLM Consolidation** (if similarity >0.8):

```markdown
# Send to LLM for semantic merging

Finding 1: "Missing input validation in user registration" (src/auth.py:45)
Finding 2: "User input not sanitized before database insert" (src/auth.py:47)

Similarity: 0.85 (keyword: 0.9, location: 1.0, severity: 0.8)

Prompt: "Are these findings describing the same underlying issue? If yes, merge into single finding with combined details."

Result: MERGE
Merged: "Missing input validation in user registration endpoint - user input not sanitized before database insert (src/auth.py:45-47)"
```

**Consolidation Output**:

```json
{
  "original_findings": 47,
  "exact_duplicates_removed": 8,
  "semantic_merges": 5,
  "final_findings": 34,
  "consolidation_ratio": 0.72
}
```

### Step 5.2: Overlap Detection (Synthesis Trigger)

**Trigger**: 3+ findings with overlap >0.7

**Overlap Formula**:

```python
overlap_score = (
    (keyword_match * 0.4) +    # Shared terminology
    (domain_match * 0.3) +     # Same component/file
    (location_match * 0.2) +   # File proximity
    (agent_type_match * 0.1)   # Similar agent perspective
)
```

**Synthesis Application**:
- If overlap ≥0.7 for 3+ findings → Apply synthesis framework
- Weighted scoring: (Impact × 0.6) / (Effort × Risk_Multiplier × Change_Multiplier)
- Consolidate related findings into recommendations
- Present trade-offs explicitly

**Example**:

```markdown
Overlapping Findings (3 agents flagged similar issues):

1. code-quality: "Missing error handling in async operations" (Severity: High)
2. tech-debt-investigator: "Exception swallowing detected in async handlers" (Debt Impact: Medium)
3. sast-scanner: "Unhandled exceptions may leak sensitive data" (Security: Medium)

Overlap Score: 0.78 (keyword: 0.9, domain: 0.8, location: 0.7, agent: 0.6)

Synthesis:
- **Root Issue**: Async exception handling insufficient
- **Impact**: Security risk (data leaks) + Maintainability debt + Correctness
- **Consolidated Recommendation**: Implement async context managers with explicit error handling
- **Weighted Score**: (9 impact × 0.6) / (5 effort × 1.2 risk × 1.0 change) = 0.90 (HIGH PRIORITY)
```

### Step 5.3: Weighted Scoring (Prioritization)

**Scoring Formula**:

```python
score = (Impact × 0.6) / (Effort × Risk_Multiplier × Change_Multiplier)

# Impact: 1-10 (user harm, security, correctness)
# Effort: 1-10 (time to fix, complexity)
# Risk_Multiplier: 1.0-2.0 (risk of introducing bugs)
# Change_Multiplier: 1.0-1.5 (scope of change)
```

**Impact Calibration**:

| **Impact Level** | **Score** | **Criteria** |
|------------------|-----------|--------------|
| Critical | 9-10 | System failure, security breach, data loss |
| High | 7-8 | Significant breakage, user-facing bugs |
| Medium | 4-6 | Non-core functionality, performance degradation |
| Low | 1-3 | Aesthetic, minimal user impact |

**Effort Calibration**:

| **Effort Level** | **Score** | **Criteria** |
|------------------|-----------|--------------|
| Trivial | 1-2 | Single line change, copy-paste fix |
| Low | 3-4 | Simple refactor, small function change |
| Medium | 5-6 | Multiple files, moderate complexity |
| High | 7-10 | Architectural change, cross-cutting concern |

**Example Scoring**:

```markdown
Finding: "SQL injection vulnerability in query builder"
- Impact: 10 (security breach)
- Effort: 4 (use parameterized queries)
- Risk: 1.2 (low risk with proper testing)
- Change: 1.0 (localized change)
- Score: (10 × 0.6) / (4 × 1.2 × 1.0) = 1.25 → CRITICAL PRIORITY
```

### Step 5.4: Conflict Resolution

**Scenario**: Multiple agents provide contradictory recommendations

**Resolution Protocol**:

```yaml
detect_conflicts:
  - Finding 1: "Use async/await for database calls" (performance-reviewer)
  - Finding 2: "Synchronous ORM queries acceptable for admin endpoints" (code-quality)

resolve_conflict:
  1_severity_hierarchy:
    - If severity differs → Use HIGHEST severity
    - Example: Security > Performance > Style

  2_weighted_scoring:
    - Calculate score for each recommendation
    - Higher score wins

  3_tie_breaking:
    - Lower effort > Lower risk > Simpler solution > Agent expertise

  4_present_trade_offs:
    - If close scores (within 10%) → Present both options to user
    - Include pros/cons for each approach

output:
  - Decision: "Use async/await for high-traffic endpoints, sync acceptable for admin"
  - Rationale: "Performance gains (async) outweigh simplicity (sync) for user-facing code"
  - Trade-off: "Admin endpoints can remain sync (10x lower traffic, simpler error handling)"
```

**Output**: Consolidated findings with conflict resolutions documented

---

## Phase 6: Report Generation

**Purpose**: Generate structured, actionable review report with severity-first ordering

### Step 6.1: Report Structure

```markdown
# Code Review Report
**Generated**: <timestamp>
**Reviewed By**: <agent-list>
**Source**: <--files/--branch/--commit/--all>
**Mode**: <quick/comprehensive>
**Focus**: <security/performance/quality/design/all>

---

## Executive Summary

**Overall Status**: ✅ APPROVED | ⚠️ APPROVED WITH CONDITIONS | ❌ CHANGES REQUIRED

**Review Metrics**:
- Files Reviewed: <X> files (<Y> Python, <Z> Java, etc.)
- Total Findings: <X> (<Critical>, <High>, <Medium>, <Low>, <Nit>)
- Consolidated From: <X> original findings (deduplication: <Y>%)
- Investigation Trail: <X> findings researched with Context7/Perplexity

**Quality Gates**:
- ✅ No Critical Security Issues
- ⚠️ 2 High-Priority Performance Issues (blocking)
- ✅ Design Patterns Acceptable
- ✅ Test Coverage Adequate

**Recommendation**: <Approve / Request Changes / Block Merge>

---

## Findings by Severity

### CRITICAL (0-3 allowed)
*System failure, direct exploitation, data loss*

#### [CRIT-001] SQL Injection Vulnerability
- **Location**: `src/api/routes.py:142`
- **Confidence**: 0.92 (HIGH)
- **Investigation Trail**:
  - Initial Confidence: 0.75
  - Context7 Research: SQLAlchemy security best practices (trust: 9/10)
  - Perplexity Synthesis: OWASP A01:2021 SQL Injection Prevention
  - Final Confidence: 0.92
- **Problem**: Raw SQL query with string concatenation
  ```python
  # WRONG
  query = f"SELECT * FROM users WHERE id = {user_id}"
  ```
- **Why (Principle)**: [Python Security Patterns § SQL Injection Prevention]
  - Allows arbitrary SQL execution through user input
  - Bypasses authentication/authorization
  - Potential data exfiltration
- **Verification**:
  - *Wrong Pattern*: `rg -n "f\"SELECT.*WHERE.*{" src/`
  - *Correct Pattern*: Use parameterized queries
  - *Quick Check*: `pytest tests/security/test_sql_injection.py`
- **Fix**:
  ```python
  # CORRECT
  query = select(User).where(User.id == user_id)
  # Or with raw SQL:
  query = text("SELECT * FROM users WHERE id = :user_id")
  result = session.execute(query, {"user_id": user_id})
  ```
- **Remediation Time**: 10 days (CVSS: 9.1)

---

### HIGH (0-5 allowed)
*Significant breakage, security risks, user-facing bugs*

#### [HIGH-001] Async Function Not Awaited
- **Location**: `src/services/data_loader.py:67`
- **Confidence**: 0.88 (MEDIUM-HIGH)
- **Investigation Trail**:
  - Context7 Research: FastAPI async patterns (trust: 8/10)
  - Confirmed: Async functions must be awaited or event loop blocks
- **Problem**: `fetch_data()` returns coroutine, not result
- **Why**: [Coding Guidelines § Async/Await Patterns]
- **Verification**: `rg -n 'fetch_data\(' | grep -v 'await'`
- **Fix**: `data = await fetch_data()`
- **Remediation Time**: 4 weeks (CVSS: 7.8)

---

### MEDIUM (0-5 allowed)
*Non-core issues, performance degradation, maintainability*

#### [MED-001] N+1 Query Pattern
- **Location**: `src/models/user.py:89-95`
- **Confidence**: 0.82 (MEDIUM)
- **Problem**: Loops over users, queries database per iteration
- **Why**: [Python Performance Patterns § Database Optimization]
- **Fix**: Use `selectinload()` or `joinedload()`
- **Remediation Time**: 12 weeks (CVSS: 5.2)

---

### LOW (0-5 allowed)
*Aesthetic, minimal impact, code clarity*

#### [LOW-001] Magic Number
- **Location**: `src/config.py:23`
- **Confidence**: 0.78 (MEDIUM)
- **Problem**: Hard-coded `3600` without explanation
- **Fix**: `CACHE_TTL_SECONDS = 3600  # 1 hour`
- **Remediation Time**: 25 weeks (CVSS: 2.1)

---

### NITS (0-2 allowed, optional)
*Informational, stylistic preferences*

#### [NIT-001] Variable Naming
- **Location**: `tests/test_auth.py:12`
- **Problem**: `tmp` not descriptive
- **Fix**: Rename to `temp_user_data`
- **Remediation Time**: N/A (informational)

---

## Tests & Coverage

**Missing Tests** (tied to changed behavior):
- `test_user_registration_input_validation` - No test for null email input
- `test_async_error_handling` - Uncovered exception paths in async handlers
- `test_cache_invalidation_concurrency` - Race condition scenarios

**Coverage Gaps**:
- `src/auth.py`: 73% → 85% (add 3 tests above)

**Test Quality Issues**:
- `tests/test_api.py:45` - Assertion too broad (use specific error message)

---

## Security Notes

**OWASP Top 10 (2021)**:
- A01: Injection → [CRIT-001] SQL Injection Vulnerability
- A02: Broken Authentication → No issues found
- A03: Sensitive Data Exposure → [HIGH-002] Logging PII

**LLM Top 10 (2023)**:
- LLM01: Prompt Injection → Not applicable
- LLM02: Insecure Output Handling → No issues found

**Secrets Management**:
- ✅ No hardcoded secrets detected
- ✅ Environment variables used correctly

**Mitigations**:
- Input validation: Use Pydantic models for all API inputs
- Output encoding: Apply HTML escaping in templates
- Logging: Implement PII redaction filter

---

## Performance Notes

**Algorithmic Complexity**:
- `src/utils/sort.py:12` - O(n²) bubble sort → Use `sorted()` (O(n log n))

**Async/Await Issues**:
- [HIGH-001] Blocking async calls (3 instances)

**Caching Opportunities**:
- `get_user_permissions()` called 47 times in single request → Add memoization

---

## Design Patterns & Architecture

**SOLID Principles**:
- ✅ Single Responsibility: Well-separated concerns
- ⚠️ Open/Closed: `UserService` requires modification for new auth types (extend instead)
- ✅ Liskov Substitution: Inheritance used correctly
- ✅ Interface Segregation: Interfaces not bloated
- ✅ Dependency Inversion: DI used appropriately

**Code Smells**:
- Duplicated validation logic across 3 files → Extract to shared validator
- Large class: `UserManager` (347 lines) → Split responsibilities

**Anti-Patterns**:
- God Object: `AuthController` handles too many concerns
- Feature Envy: `Order` class accesses `Customer` internals frequently

---

## Investigation Summary

**Context7 Research** (8 findings validated):
- Libraries: fastapi, pydantic, sqlalchemy, pytest
- Topics: async patterns, validation, ORM queries, testing best practices
- Trust Scores: 8/10 - 10/10 (authoritative sources)

**Perplexity Escalations** (3 findings required synthesis):
- SQL injection prevention (OWASP A01)
- Async exception handling (industry consensus)
- Cache concurrency patterns (conflicting sources → escalated to Open Questions)

**Open Questions** (escalated to user):
- **[OQ-001]** Race condition in cache invalidation (confidence: 0.45 after research)
  - Requires manual review + load testing
  - Conflicting recommendations from sources
  - DO NOT assume this is a bug

**Research Efficiency**:
- Context7: 8 findings (80% of researched findings)
- Perplexity: 2 findings (20% of researched findings)
- Ratio: 4:1 (target achieved)

---

## Recommendations

### Should-Do Changes (Matrix-Justified)

**Critical** (MUST fix before merge):
1. [CRIT-001] Fix SQL injection vulnerability (Impact: 10, Effort: 4, Score: 1.25)

**High** (SHOULD fix before merge):
1. [HIGH-001] Await async functions (Impact: 8, Effort: 3, Score: 1.33)
2. [HIGH-002] Remove PII from logs (Impact: 7, Effort: 5, Score: 0.70)

**Medium** (Consider fixing):
1. [MED-001] Resolve N+1 query (Impact: 5, Effort: 6, Score: 0.42)

### Optional / Later

**Nits** (low priority):
- [NIT-001] Improve variable naming

**Refactoring** (future work):
- Extract duplicated validation logic
- Split `UserManager` class

---

## Language Coverage

**Reviewed**:
- ✅ Python: 12 files (code-quality)
- ✅ Security: All files (sast-scanner)
- ✅ Technical Debt: All files (tech-debt-investigator)

**Gaps** (no reviewer available):
- ⚠️ Java: 3 files (src/api/*.java)
  - Recommendation: Create java-code-reviewer agent (Priority: P1)
- ⚠️ TypeScript: 2 files (src/ui/*.ts)
  - Recommendation: Create typescript-code-reviewer agent (Priority: P1)

---

## Next Steps

**If APPROVED**:
✅ Ready to merge (no blocking issues)

**If APPROVED WITH CONDITIONS**:
⚠️ Address High-priority issues, then merge

**If CHANGES REQUIRED**:
❌ Fix Critical issues before re-review
1. Fix [CRIT-001] SQL injection
2. Re-run `/review --all` to validate fixes
3. Request re-review

**Review Reports**:
- Detailed findings: `review-report-<timestamp>.md`
- Agent reports: `review/[agent]-report.md` (if configured)

---

## Verification Commands

**Run all verifications**:
```bash
# Security checks
pytest tests/security/

# SQL injection pattern detection
rg -n "f\"SELECT.*WHERE.*{" src/

# Async function verification
rg -n 'fetch_data\(' | grep -v 'await'

# Test coverage
pytest --cov=src --cov-report=term-missing
```

**Quick validation**:
```bash
make review-checks  # High-level wrapper for all verification commands
```

---

**Report Generation Time**: <X> seconds
**Review Duration**: <Y> minutes (parallel execution: 3-5 agents simultaneously)
```

### Step 6.2: File:Line Anchors

**Format**: `file.py:line` (clickable in most editors)

**Navigation Support**:

```markdown
[CRIT-001] src/api/routes.py:142
- Click to jump to line 142 in routes.py
- Verification command provided for quick check
```

### Step 6.3: Verification Commands

**Deterministic Checks** (prefer these):

```bash
# Pattern search (wrong signature)
rg -n 'startAsyncOp\(' | grep -v 'await'

# Linter command
ruff check src/ --select S608  # SQL injection rule

# Test execution
pytest tests/security/test_sql_injection.py
```

**Minimal Harnesses** (when deterministic not possible):

```python
# Quick reproduction script
python -c "from src.auth import validate_input; validate_input(None)"
# Expected: Raises ValueError
```

**High-Level Make Targets** (preferred):

```bash
make review-checks          # Aggregate all verification commands
make security-scan          # Run security-specific checks
make test-coverage          # Coverage report
```

---

## Confidence-Severity Matrix

**Purpose**: Define minimum confidence levels per severity to ensure high-signal findings

| **Severity** | **Min Confidence** | **Investigation Required** |
|--------------|-------------------|----------------------------|
| Critical | 0.90 | ALWAYS validate with Context7 + Perplexity |
| High | 0.80 | Validate with Context7 if <0.90 |
| Medium | 0.75 | Validate with Context7 if <0.85 |
| Low | 0.70 | Optional validation |
| Nit | 0.60 | No validation required |

**Escalation Rule**: If confidence < minimum for severity:
1. **Attempt Investigation** (Context7 → Perplexity)
2. **If Still Low** → Downgrade severity OR escalate to "Open Questions"
3. **DO NOT report low-confidence findings as facts**

**Example**:

```markdown
Finding: "Potential memory leak in cache manager"
- Initial Severity: HIGH
- Initial Confidence: 0.65 (BELOW 0.80 threshold)
- Investigation: Context7 research → confidence increases to 0.78 (still below)
- Action: DOWNGRADE severity to MEDIUM (0.75 threshold) OR escalate to Open Questions
```

---

## Finding Schema

**Complete Finding Structure**:

```json
{
  "finding_id": "CRIT-001",
  "severity": "Critical",
  "category": "Security",
  "location": "src/api/routes.py:142",
  "message": "SQL injection vulnerability in query builder",
  "confidence": 0.92,
  "confidence_sources": [
    "Context7: SQLAlchemy Security Best Practices (trust: 9/10)",
    "Perplexity: OWASP A01:2021 SQL Injection Prevention"
  ],
  "problem": "Raw SQL query with string concatenation allows arbitrary SQL execution",
  "principle": "Python Security Patterns § SQL Injection Prevention",
  "verification_commands": [
    "rg -n 'f\\\"SELECT.*WHERE.*{' src/",
    "pytest tests/security/test_sql_injection.py"
  ],
  "recommendation": "Use parameterized queries: query = text('SELECT * FROM users WHERE id = :user_id')",
  "investigation_trail": {
    "initial_confidence": 0.75,
    "context7_research": "Validated against SQLAlchemy docs, increased to 0.85",
    "perplexity_synthesis": "Confirmed with OWASP A01, final confidence 0.92",
    "final_confidence": 0.92
  },
  "impact": 10,
  "effort": 4,
  "risk_multiplier": 1.2,
  "change_multiplier": 1.0,
  "priority_score": 1.25,
  "remediation_time_days": 10,
  "cvss_score": 9.1
}
```

---

## Example Workflows

### Workflow 1: Review Uncommitted Changes

```bash
/review --all

# Discovers: 5 Python files, 3 TypeScript files
# Routes:
#   - code-quality (5 files)
#   - tech-debt-investigator (all 8 files)
#   - sast-scanner (all 8 files)
#   - Escalates TypeScript (no reviewer available)

# Findings:
#   - 2 Critical (confidence 0.92, 0.88)
#   - 3 High (confidence 0.85, 0.82, 0.78)
#   - 1 Medium (confidence 0.68 → researched with Context7 → 0.82)

# Investigation:
#   - 3 findings validated with Context7 (FastAPI, Pydantic, SQLAlchemy)
#   - 1 finding escalated to Perplexity (complex async pattern, confidence 0.72 → 0.85)
#   - 0 findings escalated to user

# Output:
#   - Report: review-report-20251119T143000.md
#   - Status: CHANGES REQUIRED (2 Critical issues)
```

### Workflow 2: Review Specific Commit

```bash
/review --commit abc123 --focus=security

# Discovers: 8 files changed in commit abc123
# Routes:
#   - code-quality (security focus)
#   - sast-scanner (all files)

# Findings:
#   - 1 Critical security issue (confidence 0.65 initially)

# Investigation:
#   - Context7 research: SQLAlchemy security patterns (confidence → 0.78)
#   - Perplexity escalation: OWASP A01 validation (confidence → 0.88)
#   - Final confidence: 0.88 (HIGH)

# Output:
#   - Report shows investigation trail:
#     - Initial: 0.65 (LOW)
#     - Context7: +0.13 (SQLAlchemy docs)
#     - Perplexity: +0.10 (OWASP A01)
#     - Final: 0.88 (APPROVED for reporting)
```

### Workflow 3: Review Feature Branch

```bash
/review --branch feature-auth --mode=comprehensive

# Discovers: 15 files (8 Python, 5 Java, 2 TypeScript)
# Routes:
#   - code-quality (8 Python files, 2 batches)
#   - tech-debt-investigator (all 15 files)
#   - sast-scanner (all 15 files)
#   - design-pattern-reviewer (confidence 0.87, INCLUDED as dynamic agent)
#   - Gaps: Java (5 files), TypeScript (2 files)

# Findings:
#   - 5 design-level issues (SOLID violations)
#   - All confidence ≥0.80 (no investigation needed for 4/5)
#   - 1 finding confidence 0.72 → Context7 research → 0.83

# Output:
#   - Design review report with SOLID principle violations
#   - Gap notice: "Java and TypeScript files not reviewed (no reviewers)"
#   - Recommendation: Create java-code-reviewer (P1), typescript-code-reviewer (P1)
```

---

**Complete Reference**: This guide provides detailed workflows for all 6 phases of the `/review` command. For command usage, see `.claude/commands/review.md`.
