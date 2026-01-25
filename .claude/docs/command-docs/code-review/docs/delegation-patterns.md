# Delegation Patterns for /code-review Command

Exact Task() call syntax for each phase of the review workflow.

---

## Phase 0: Tool Availability (HYBRID)

### Direct: Git Check (Orchestrator)

```bash
# Orchestrator executes directly
git --version
```

### Delegated: Semgrep Check

```
Task(
  subagent_type="git-github",
  description="Check semgrep availability",
  prompt="Check if semgrep is installed and available:
    
    Execute: semgrep --version
    
    Return JSON:
    {
      available: boolean,
      version: string | null,
      install_instructions: string (if not available)
    }"
)
```

---

## Phase 1: File Discovery (Delegated)


```
Task(
  subagent_type="git-github",
  description="Discover files for code review",
  prompt="Discover files for review based on source:
    
    Source Flag: {source_flag}
    Source Value: {source_value}
    
    Commands by source:
    - --all: git status --porcelain + git diff --name-only HEAD
    - --branch {name}: git diff --name-only main...{name}
    - --commit {hash}: git show --name-only {hash}
    - --files {paths}: validate existence of each path
    
    Apply exclusions:
    - .claude/**, docs/**, node_modules/**, vendor/**
    - .venv/**, __pycache__/**, dist/**, build/**
    - *.min.js, *.bundle.js, package-lock.json
    
    Detect language by extension (.py -> Python, .ts -> TypeScript, etc.)
    
    Return JSON:
    {
      files: [{path, language, change_type}],
      total_count: number,
      language_breakdown: {language: count}
    }"
)
```

---

## Phase 2: File Batching (Delegated)


```
Task(
  subagent_type="git-github",
  description="Group files into review batches",
  prompt="Group files for parallel review:
    
    Files: {file_list}
    Max batch size: 5 files
    
    Grouping priority:
    1. Language (same language per batch)
    2. Directory proximity (files in same dir together)
    3. Change type (modifications, additions grouped)
    
    Return JSON:
    {
      batches: [
        {
          batch_id: number,
          language: string,
          agent: string,  # python-code-reviewer, etc.
          files: string[],
          file_count: number
        }
      ]
    }"
)
```

---

## Phase 3: Multi-Agent Review

### Core Agent: Python Code Reviewer

```
Task(
  subagent_type="python-code-reviewer",
  description="Review Python files for quality issues",
  prompt="Review Python code for quality issues:
    
    Files: {batch.files}
    Focus: {focus_param}  # security|performance|quality|design|all
    Mode: {mode_param}    # quick|comprehensive
    
    For each finding include:
    - finding_id: string (e.g., 'HIGH-001')
    - location: string (file:line)
    - severity: Critical|High|Medium|Low|Nit
    - confidence: 0.0-1.0
    - message: string
    - recommendation: string
    - verification_command: string
    
    Return JSON:
    {
      findings: [...],
      summary: {total: number, by_severity: {}}
    }"
)
```


### Core Agent: Tech Debt Investigator

```
Task(
  subagent_type="tech-debt-investigator",
  description="Analyze technical debt in review files",
  prompt="Analyze technical debt:
    
    Files: {all_files}
    
    Calculate:
    - debt_score: 0-100
    - TDR: Technical Debt Ratio (float)
    - hotspots: files with most debt
    - category_breakdown: duplication, complexity, coupling
    
    Return JSON:
    {
      debt_score: number,
      tdr: float,
      hotspots: [{file, score, categories}],
      categories: {category: count},
      recommendations: [string]
    }"
)
```

### Core Agent: SAST Scanner

```
Task(
  subagent_type="sast-scanner",
  description="Security scan for vulnerabilities",
  prompt="Security vulnerability scan:
    
    Files: {all_files}
    Depth: {mode_param}  # quick|comprehensive
    
    Check for:
    - OWASP Top 10 (2021)
    - LLM Top 10 (2023) if applicable
    - Hardcoded secrets (API keys, passwords)
    - Injection vulnerabilities (SQL, command, XSS)
    - Authentication/authorization issues
    
    Return JSON:
    {
      vulnerabilities: [{
        finding_id: string,
        owasp_category: string,
        severity: string,
        confidence: float,
        location: string,
        description: string,
        remediation: string
      }],
      severity_counts: {Critical: n, High: n, ...},
      owasp_coverage: {category: boolean}
    }"
)
```


---

## Phase 4: Confidence Investigation (Delegated)

### Researcher-Library (replaces Context7)

```
Task(
  subagent_type="researcher-external",
  description="Validate finding against library documentation",
  prompt="Validate code review finding:
    
    Finding: {finding.message}
    Library: {extracted_library}  # e.g., 'fastapi', 'sqlalchemy'
    Topic: {extracted_topic}      # e.g., 'async dependency injection'
    
    Research:
    1. Find official documentation for the library
    2. Locate documentation on the specific topic
    3. Determine if finding is valid based on official docs
    
    Return JSON:
    {
      validation_result: 'confirmed' | 'contradicted' | 'ambiguous',
      confidence_delta: float,  # e.g., +0.10 or -0.20
      source_citation: string,
      evidence_summary: string
    }"
)
```

### Researcher-Web (replaces Perplexity)


```
Task(
  subagent_type="researcher-external",
  description="Deep research on low-confidence finding",
  prompt="Research code review finding via web sources:
    
    Finding: {finding.message}
    Initial Confidence: {finding.confidence}
    Context: {finding.context}
    
    Research query: '{finding as question}'
    
    Cross-reference with:
    - OWASP standards
    - PEP guidelines (for Python)
    - RFC specifications
    - Community best practices
    
    Return JSON:
    {
      consensus_level: 'strong' | 'moderate' | 'none',
      recommended_confidence: float,
      sources: [{url, title, trust_score}],
      synthesis: string
    }"
)
```

---

## Parallel Launch Pattern

**Launch all Phase 3 agents in single message**:

```
Launching 3 core review agents in parallel...

Task(subagent_type='python-code-reviewer', prompt={...})
Task(subagent_type='tech-debt-investigator', prompt={...})
Task(subagent_type='sast-scanner', prompt={...})  # If semgrep available
```

**Total**: 2-3 agents in parallel (depending on semgrep availability)

---

## Sequential Investigation Pattern

Phase 4 research follows cost-optimized sequence:

```
For each finding with confidence < 0.90:
  
  1. Task(researcher-external, ...)  # Auto-routes Context7 (free) vs Perplexity (paid)
     IF confidence now >= 0.75: STOP
  
  2. # researcher-external handles escalation internally
     IF confidence now >= 0.75: STOP
  
  3. IF confidence still < 0.50: Escalate to Open Questions
```

**Target Ratio**: 4:1 Context7:Perplexity (managed internally by researcher-external)
