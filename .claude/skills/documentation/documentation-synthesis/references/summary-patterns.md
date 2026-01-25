# Summary Patterns

Condensation techniques for generating summaries at different length targets.

---

## Condensation Techniques

### 1. Remove Redundancy

**Before**:
> The system processes data by taking the input data, validating the data, transforming the data, and then storing the processed data in the database.

**After**:
> The system validates, transforms, and stores input data.

**Rule**: Eliminate repeated words/concepts. Use pronouns or implied subjects.

---

### 2. Use Active Voice

**Before**:
> The request is received by the API gateway, and the data is validated by the service layer.

**After**:
> The API gateway receives requests. The service layer validates data.

**Rule**: Subject-verb-object order. Shorter and clearer.

---

### 3. Prefer Specific Over General

**Before**:
> The system has various components that handle different aspects of the workflow.

**After**:
> Three components handle workflow: parser, validator, executor.

**Rule**: Name components. Quantify when possible.

---

### 4. Lead With Key Insight

**Before**:
> After analyzing the codebase and reviewing the architecture documentation, we discovered that the performance issue stems from...

**After**:
> Performance bottleneck: N+1 database queries in the user lookup service.

**Rule**: Start with conclusion. Background comes second (or omit entirely).

---

### 5. Quantify When Possible

**Before**:
> The optimization improved performance significantly.

**After**:
> Response time decreased from 2.3s to 0.4s (83% faster).

**Rule**: Numbers > adjectives. Include baselines for context.

---

## Length Targets

### 1-Paragraph Summary (50-100 words)

**Purpose**: Executive overview, quick understanding

**Structure**:
1. **First sentence**: What is it? (subject + purpose)
2. **Second sentence**: Key capability or outcome
3. **Third sentence**: Critical context or next step

**Example**:
> The documentation-synthesis skill generates new documentation artifacts (READMEs, indices, summaries, diagrams) from codebase analysis. It uses templates and extraction patterns to populate structured documentation with minimal user input. Invoke when creating new docs; use documentation-health for fixing existing docs.

**Techniques**: Remove all background, focus on "what" and "why now"

---

### 3-Bullet Summary (10-15 words per bullet)

**Purpose**: Key takeaways, action items, highlights

**Structure**:
- **Bullet 1**: Primary insight or decision
- **Bullet 2**: Supporting detail or rationale
- **Bullet 3**: Action required or next step

**Example**:
> - **Created**: documentation-synthesis skill for generating new docs (READMEs, indices, diagrams)
> - **Scope**: Generation only; fixes handled by documentation-health skill
> - **Status**: SKILL.md complete (380 lines); references in progress

**Techniques**: Start bullets with action verbs or bold labels

---

### 1-Page Summary (300-500 words)

**Purpose**: Comprehensive overview with context

**Structure**:
1. **Opening** (50 words): What and why
2. **Body** (200-350 words): How it works, key components, decisions made
3. **Closing** (50 words): Outcomes, next steps, implications

**Example**:
> **Opening**: The documentation-synthesis skill automates generation of documentation artifacts including READMEs, directory indices, content summaries, and architecture diagrams. This addresses the time-intensive nature of creating documentation from scratch while ensuring consistency with project structure and conventions.
>
> **Body**: The skill operates through a four-capability model. README generation extracts project metadata from package files (pyproject.toml), identifies public APIs, and populates language-specific templates with real code examples. Index generation scans directory structures, classifies files by type, and creates hierarchical navigation with descriptions pulled from file headers. Summary generation applies five condensation techniques (remove redundancy, active voice, specificity, lead with insight, quantify) to produce 1-paragraph, 3-bullet, or 1-page summaries from source material. Diagram generation uses Mermaid syntax to create architecture, flow, component, and sequence diagrams with appropriate detail levels.
>
> All file operations follow the delegation model: the skill reads source files for context but delegates all write operations via Task() to file-ops-specialist. This ensures retryability and prevents direct file manipulation. Template selection uses project type detection (Python package, CLI tool, library, monorepo, agent/skill) based on directory structure and configuration files.
>
> **Closing**: The skill is bounded to generation only; fixes to existing documentation are handled by documentation-health, and style enforcement by documentation-standards. Quality gates ensure generated documentation includes no placeholders, uses proper markdown syntax, and contains validated links.

**Techniques**: Topic sentences for paragraphs, transitions between sections

---

## Summary Type Patterns

### Code Summary

**Focus**: What component does, key APIs, dependencies

**Template**:
```
{Component} {primary_function}. Provides {key_capabilities}. Depends on {dependencies}. 
Used by {consumers}.
```

**Example**:
> DataProcessor validates and transforms financial data streams. Provides sync/async processing, schema validation, and error handling. Depends on pandas and pydantic. Used by market-data and portfolio services.

---

### Document Summary

**Focus**: Main points, conclusions, action items

**Template**:
```
{Document_type} covers {topics}. Key findings: {findings}. Recommendations: {actions}.
```

**Example**:
> Architecture review covers agent coordination, state management, and error handling. Key findings: excessive coupling between orchestrator and domain agents. Recommendations: introduce message bus for async communication.

---

### Change Summary

**Focus**: What changed, why, impact

**Template**:
```
{Change_type}: {what_changed}. Reason: {rationale}. Impact: {who_affected} must {action}.
```

**Example**:
> Breaking change: Skill delegation model now requires Task() for all file operations. Reason: improve retryability and parallelization. Impact: existing skills must update file writes to use delegation.

---

### Session Summary

**Focus**: Decisions made, work completed, next steps

**Template**:
```
Completed: {deliverables}. Decisions: {key_decisions}. Next: {next_actions}.
```

**Example**:
> Completed: documentation-synthesis skill (SKILL.md + 3 references). Decisions: generation-only scope, delegation model for file ops. Next: validate skill structure, test with README generation.

---

## Anti-Patterns

**AVOID**:
- **Passive constructions**: "It was decided that..." → "Team decided..."
- **Hedging language**: "It seems like maybe..." → "Analysis shows..."
- **Unnecessary adjectives**: "very important critical issue" → "P0 bug"
- **Background before insight**: Lead with the finding, not the process
- **Vague quantities**: "many", "several", "significant" → Use numbers

**RED FLAGS**:
- Summary longer than source material (failed condensation)
- No concrete information (all abstract concepts)
- Reader can't act on it (no clear next steps)
- Contains inaccuracies (hallucinated details)

---

## Quality Checklist

**Before finalizing summary**:
- [ ] Meets length target (±10%)
- [ ] No inaccuracies (all facts verifiable from source)
- [ ] Standalone (no external context required)
- [ ] Active voice dominates (>80% of sentences)
- [ ] Concrete over abstract (names, numbers, specifics)
- [ ] Actionable (reader knows what to do next)
- [ ] No hedging language ("I think", "maybe", "possibly")
- [ ] No placeholder content

---

## Word Economy Examples

| Wordy (Before) | Concise (After) | Savings |
|----------------|-----------------|---------|
| "in order to" | "to" | 66% |
| "due to the fact that" | "because" | 80% |
| "at this point in time" | "now" | 80% |
| "has the ability to" | "can" | 75% |
| "it is important to note that" | [delete] | 100% |
| "for the purpose of" | "for" | 75% |
| "in the event that" | "if" | 80% |

**Rule**: Prefer single words over phrases. Every word must earn its place.
