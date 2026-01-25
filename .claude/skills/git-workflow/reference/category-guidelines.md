# Category Guidelines Reference

**Purpose**: Explains WHY files are classified into 9 semantic categories.

---

## The 9 Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| database | Data layer changes | migrations/, models/, *.sql |
| api | Endpoint changes | routes/, handlers/, controllers/ |
| ui | Frontend changes | components/, pages/, *.tsx, *.jsx |
| config | Configuration | .env*, settings/, *.yaml |
| tests | Test files | tests/, test_*.py |
| docs | Documentation | docs/, *.md |
| infrastructure | DevOps | k8s/, .github/, Dockerfile |
| claude_code | Claude Code ecosystem | .claude/agents/, .claude/skills/ |
| code | General code (fallback) | Everything else |

---

## Why Separate Categories?

### 1. Domain-Specific Review
Each category needs different expertise:
- Database: DBA knowledge, migration safety
- API: Security, authentication, input validation
- UI: Accessibility, XSS prevention, UX

### 2. Targeted Quality Gates
Different agents for different categories:
- API → sast-scanner for security
- claude_code → claude-code-ecosystem for agent quality

### 3. Clean Git History
Separating categories creates:
- Atomic, focused commits
- Easier code review
- Simple reverts when needed

### 4. Parallel Review
Independent categories can be reviewed in parallel.

---

## Detection Priority

Categories are detected in priority order (highest first):

| Priority | Category | Why This Priority? |
|----------|----------|-------------------|
| 100 | database | Schema changes are highest risk |
| 95 | claude_code | Agent changes affect automation |
| 90 | api | Endpoint changes are user-facing |
| 85 | ui | UI changes are visible |
| 80 | config | Config changes affect runtime |
| 75 | tests | Tests validate other code |
| 70 | docs | Docs explain other code |
| 65 | infrastructure | Infra enables deployment |
| 0 | code | Fallback for everything else |

---

## Category Display Names

| Internal | Display (for users) |
|----------|---------------------|
| database | Database & Models |
| api | API Endpoints |
| ui | UI Components |
| config | Configuration |
| tests | Test Files |
| docs | Documentation |
| infrastructure | Infrastructure |
| claude_code | Claude Code Agents |
| code | General Code |

---

## Cross-Category Rule

**CRITICAL**: Files are NEVER grouped across categories.

Why?
- Different reviewers for different domains
- Easier to revert specific changes
- Cleaner git blame history

---

## See Also

- FileGrouper heuristics: `.claude/skills/source-control/reference/fileGrouper-heuristics.md`
- Execution logic: `.claude/commands/git.md`
