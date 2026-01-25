---
title: "GitHub Integration Guide for source-control Agent"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# GitHub Integration Guide for source-control Agent

**Purpose**: Standards and patterns for GitHub operations using MCP tools and GitHub CLI

**Audience**: source-control agent (automation)

**Last Updated**: 2025-10-30

---

## Table of Contents

1. [When to Use GitHub CLI vs MCP](#when-to-use-github-cli-vs-mcp)

2. [Issue Formatting Standards](#issue-formatting-standards)

3. [Pull Request Workflow](#pull-request-workflow)

4. [Label Taxonomy](#label-taxonomy)

5. [Claude GitHub Actions Integration](#claude-github-actions-integration)

6. [Security Best Practices](#security-best-practices)

7. [Troubleshooting](#troubleshooting)

---

## When to Use GitHub CLI vs MCP

### Use GitHub MCP Tools (mcp**github**\*)

**Primary method for GitHub operations**:

- Creating/updating issues, PRs, files

- Searching code/issues/repositories

- Repository operations (branches, commits, etc.)

- Managing labels, milestones, releases

- Reading repository metadata

### Getting Local Repository Information

**CRITICAL**: Before using ANY GitHub MCP tools, you MUST get the correct repository owner and name.

**Pattern to use**:

```bash
# Get the repository URL from git
AGENT_NAME=<your-agent> git remote -v

# Example output:
# origin  https://github.com/kemosabe102/gauntlet-agents.git (fetch)
# origin  https://github.com/kemosabe102/gauntlet-agents.git (push)
```

**Extract owner and repo**:
- URL format: `https://github.com/{owner}/{repo}.git`
- Parse the owner and repo name from this URL
- Example: `kemosabe102` (owner), `gauntlet-agents` (repo)

**Alternative - Use get_me first**:

```
# Get authenticated user context
mcp__github__get_me

# This returns your username and other profile information
# However, this gives YOUR username, not the repo owner
# Use git remote for repo owner (which may be different)
```

**Common mistakes to avoid**:
- ❌ Hardcoding repository names (they change between forks/projects)
- ❌ Assuming repo owner = current user
- ❌ Using wrong repository names in MCP tool calls
- ✅ Always use `git remote -v` to get the actual repository

**Why MCP is preferred**:

- Integrated OAuth authentication

- Automatic retry and circuit breakers

- Type-safe operations

- Better error handling

- No shell escaping issues

**How MCP works**:

- Agents dynamically discover available `mcp__github__*` tools

- Tools are self-describing (no need to memorize names)

- Authentication handled via `/mcp` command in Claude Code

- See `.claude/docs/01-guides/integration/integration/mcp.md` for complete setup guide

### Complete GitHub MCP Workflow Example

**Step 1: Get repository information from git**

```bash
# Get the repository URL
AGENT_NAME=source-control git remote -v
# Output: origin  https://github.com/kemosabe102/gauntlet-agents.git (fetch)

# Parse output to extract:
# owner = "kemosabe102"
# repo = "gauntlet-agents"
```

**Step 2: Use MCP tools with correct parameters**

```
# Example: Search for merged PRs
mcp__github__search_pull_requests(
  query: "repo:kemosabe102/gauntlet-agents is:merged",
  sort: "updated",
  order: "desc",
  perPage: 10
)

# Example: List pull requests
mcp__github__list_pull_requests(
  owner: "kemosabe102",
  repo: "gauntlet-agents",
  state: "open",
  perPage: 10
)

# Example: Get PR details
mcp__github__pull_request_read(
  method: "get",
  owner: "kemosabe102",
  repo: "gauntlet-agents",
  pullNumber: 123
)
```

**Key points**:
- ALWAYS get owner/repo from `git remote -v` first
- For search queries, use format: `repo:owner/repo-name`
- For direct tools, use separate `owner` and `repo` parameters
- Never hardcode repository names

### Use GitHub CLI (gh commands)

**Only for GitHub Actions workflow monitoring**:

```bash

# Watch workflow runs

gh run list

gh run view <run-id>

gh run watch <run-id>

```

**Why**: GitHub MCP server doesn't yet provide workflow run tools.

**For all other operations**: Use MCP tools instead of CLI commands.

---

## Issue Formatting Standards

### Core Principle

**GitHub has no "priority" field** - priority information must be encoded in the issue title and labels.

### Issue Title Format

```

[PRIORITY] Brief descriptive title (context/category)

```

**Examples**:

- `[CRITICAL] Remove hardcoded placeholder email in qual/config.py (SEC compliance)`

- `[HIGH] Add production observability framework to tool-design-patterns.md`

- `[MEDIUM] Refactor config.py to use pydantic-settings`

- `[LOW] Update documentation formatting in README`

**Priority Levels**:

- `[CRITICAL]` - Production outages, security vulnerabilities, compliance violations

- `[HIGH]` - GA blockers, major bugs, important features

- `[MEDIUM]` - Performance improvements, refactoring, tech debt

- `[LOW]` - Documentation, minor enhancements, nice-to-haves

### Issue Body Structure

Use clear sections with Markdown formatting:

```markdown
## Component

`path/to/file.py` or component name

## Priority

**CRITICAL/HIGH/MEDIUM/LOW** - Brief justification

## Summary

2-3 sentence overview of the issue

## Evidence

- Line numbers, code snippets, or specific examples

- Links to related files or documentation

- Error messages or logs

## Impact

- **Severity**: Critical/High/Medium/Low

- **Affected areas**: What this impacts

- **Blockers**: What this blocks (if any)

## Recommended Fix

1. Step-by-step remediation plan

2. Alternative approaches (if applicable)

## Estimated Effort

Time estimate or complexity assessment

## Related

- Links to related issues/PRs

- Component review IDs

- Source agents or analysis reports
```

### Creating Issues with MCP

**Conceptual approach** (agents discover exact tool names):

1. Use GitHub MCP tool to create issue

2. Pass title with priority prefix

3. Pass formatted body content

4. Apply labels if they exist (see Label Management below)

**Authentication**: Use `/mcp` command in Claude Code to authenticate with GitHub.

---

## Pull Request Workflow

### PR Title Format

Follow conventional commit format:

```

type: brief description

```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`

### PR Body Structure

```markdown
## Summary

- Bullet point summary of changes

- Key implementation details

## Test Plan

- [x] Unit tests pass

- [x] Integration tests pass

- [x] Manual testing completed

## Related

Fixes #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Creating PRs with MCP

**Conceptual approach**:

1. Use GitHub MCP tool to create pull request

2. Pass conventional commit title

3. Pass formatted body content

4. Link to related issues

**Benefits over CLI**:

- No shell escaping issues

- Better error handling

- Type-safe operations

- OAuth integration

---

## Label Taxonomy

### Standard Labels for This Project

**Priority labels**:

- `priority:critical` - Critical priority issues

- `priority:high` - High priority issues

- `priority:medium` - Medium priority issues

- `priority:low` - Low priority issues

**Type labels**:

- `type:security` - Security-related issues

- `type:bug` - Bug fixes

- `type:feature` - New features

- `type:documentation` - Documentation changes

- `type:refactor` - Code refactoring

- `type:tech-debt` - Technical debt

**Area labels**:

- `area:production` - Production-related changes

- `area:security` - Security area

- `area:testing` - Testing infrastructure

**Special labels**:

- `auto-fix` - Can be automatically fixed by CI

- `ga-blocker` - Blocks GA release

### Label Management

**Creating labels**: Use GitHub MCP tools to create label taxonomy.

**Applying labels**: Apply labels when creating issues or PRs, or add them afterward.

**Checking labels**: Use GitHub MCP tools to list existing labels before applying.

---

## Claude GitHub Actions Integration

### How @claude Triggering Works

**Workflow Trigger Pattern**:

GitHub Actions workflow monitors for:

1. `issue_comment` events (comments on issues)

2. `pull_request_review_comment` events (comments on PR files)

3. `issues` events (new issues opened)

**Conditional execution**:

```yaml
if: |

  (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||

  (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||

  (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
```

### Triggering Claude in Issues

**To activate Claude Code GitHub Actions**:

1. **In issue body** (when creating issue):

   ```markdown
   ## Problem

   We need to implement user authentication.

   @claude Please create a PR implementing OAuth 2.0 authentication following our CLAUDE.md standards.
   ```

2. **In issue comment** (after issue created):

   ```

   @claude implement this feature based on the issue description

   ```

3. **In PR comments**:

   ```

   @claude review this PR for security issues

   @claude fix the TypeError in the user dashboard component

   ```

### Common @claude Commands

```

@claude implement this feature based on the issue description

@claude how should I implement user authentication for this endpoint?

@claude fix the TypeError in the user dashboard component

@claude review this PR for security best practices

@claude refactor this code to follow our patterns

```

### When Claude Will NOT Respond

Claude won't respond if:

- No `@claude` mention in comment/body

- Using `/claude` instead (slash commands are different)

- GitHub Actions workflow not configured

- API key not set in repository secrets

- Claude GitHub app not installed

---

## Security Best Practices

### MCP vs CLI Security Considerations

**MCP advantages**:

- No command injection risk (structured API calls)

- No shell escaping issues

- OAuth token management handled automatically

- Built-in rate limiting and retry logic

**CLI security patterns** (when CLI is necessary):

✅ **SAFE HEREDOC PATTERN** (for multi-line content):

```bash

gh issue create --body "$(cat <<'EOF'

Content here with special characters: $, `, etc.

EOF

)"

```

**Why safe**: Quoted heredoc delimiter (`'EOF'`) prevents variable expansion.

❌ **UNSAFE PATTERNS** (blocked by security hook):

```bash

# Unquoted heredoc (allows variable expansion)

gh issue create --body "$(cat <<EOF

Content with $VARIABLES

EOF

)"



# Command substitution in body

gh issue create --body "Issue: $(malicious_command)"

```

### API Key Management

**NEVER**:

- Hardcode API keys in workflow files

- Commit secrets to repository

- Share API keys in issue comments

**ALWAYS**:

- Use GitHub Secrets (`${{ secrets.ANTHROPIC_API_KEY }}`)

- Use OAuth for MCP authentication

- Rotate keys periodically

- Limit permissions to minimum required

---

## Troubleshooting

### Issue: 422 Validation Failed - Repository not found

**Symptom**:
```
MCP error -32603: failed to search pull requests: GET https://api.github.com/search/issues...:
422 Validation Failed [{Resource:Search Field:q Code:invalid Message:The listed users and
repositories cannot be searched either because the resources do not exist or you do not have
permission to view them.}]
```

**Root Cause**: Using incorrect repository owner/name in GitHub MCP tool calls

**Solution**:

1. **Get the correct repository information**:
   ```bash
   git remote -v
   # Output: origin  https://github.com/kemosabe102/gauntlet-agents.git (fetch)
   ```

2. **Parse owner and repo**:
   - Extract from URL: `https://github.com/{owner}/{repo}.git`
   - Example: owner = "kemosabe102", repo = "gauntlet-agents"

3. **Use correct values in MCP tools**:
   ```
   # For search queries
   mcp__github__search_pull_requests(
     query: "repo:kemosabe102/gauntlet-agents is:merged"
   )

   # For direct tools
   mcp__github__list_pull_requests(
     owner: "kemosabe102",
     repo: "gauntlet-agents"
   )
   ```

**Prevention**: Never hardcode repository names - always get from `git remote -v`

### Issue: GitHub MCP authentication failing

**Symptom**: MCP tools return authentication errors

**Solution**:

1. In Claude Code, run `/mcp` command

2. Select GitHub server

3. Choose "Authenticate" option

4. Complete OAuth flow in browser

5. Verify authentication success

**See**: `.claude/docs/01-guides/integration/integration/mcp.md` for complete authentication guide

### Issue: GitHub CLI commands blocked by security hook

**Symptom**:

```

🚫 COMMAND BLOCKED: Command contains unsafe elements:

unsafe_command_substitution, unsafe_backtick_substitution

```

**Solution**:

Use quoted heredoc delimiter (`'EOF'`) not unquoted (`EOF`):

```bash

# ✅ CORRECT

gh issue create --body "$(cat <<'EOF'

Content here

EOF

)"



# ❌ WRONG

gh issue create --body "$(cat <<EOF

Content here

EOF

)"

```

### Issue: MCP tools not available

**Symptom**: No `mcp__github__*` tools visible to agent

**Possible causes**:

1. **GitHub MCP server not configured**: Run `claude mcp add --transport http github https://api.githubcopilot.com/mcp/`

2. **Session restart needed**: Restart Claude Code session

3. **Authentication not completed**: Use `/mcp` to authenticate

**Verification**:

```bash

# Check configured MCP servers

claude mcp list



# In Claude Code, check server status

/mcp

```

### Issue: Claude not responding to @claude mentions

**Possible causes**:

1. **Workflow not configured**: Check `.github/workflows/` for Claude workflow

2. **App not installed**: Verify Claude GitHub app installation

3. **Wrong syntax**: Use `@claude` not `/claude`

4. **API key missing**: Check repository secrets

**Verification** (using GitHub CLI):

```bash

# Check workflow files exist

ls -la .github/workflows/



# Check recent workflow runs

gh run list



# View specific run logs

gh run view <run-id>

```

---

## Quick Reference

### Decision Tree: Creating Issues

```

START: Need to create GitHub issue

  │

  ├─ Is priority CRITICAL/HIGH?

  │  ├─ Yes → Put [PRIORITY] in title

  │  └─ No → Consider batching into lower priority issue

  │

  ├─ Use MCP or CLI?

  │  ├─ Creating issue → Use GitHub MCP tools

  │  └─ Workflow monitoring only → Use gh CLI

  │

  ├─ Do labels exist in repo?

  │  ├─ Yes → Apply labels via MCP

  │  └─ No → Create issue, note missing labels in comment

  │

  └─ Should Claude auto-fix this?

     ├─ Yes → Add @claude mention in body

     └─ No → Create issue normally

```

### MCP Setup Quick Start

```bash

# 1. Add GitHub MCP server

claude mcp add --transport http github https://api.githubcopilot.com/mcp/



# 2. In Claude Code, authenticate

/mcp

# Select GitHub → Authenticate



# 3. Verify connection

/mcp

# Check GitHub server status

```

### GitHub Actions Workflow Monitoring

```bash

# List recent workflow runs

gh run list



# View specific run details

gh run view <run-id>



# Watch run in real-time

gh run watch <run-id>

```

---

## Integration with source-control Agent

### Agent Responsibilities

The source-control agent should:

1. **Issue Creation**:
   - Always put priority in title: `[PRIORITY] Title`

   - Follow issue body structure template

   - Use GitHub MCP tools for creation

   - Apply labels if they exist

2. **Claude Integration**:
   - Add `@claude` mentions when auto-fix is desired

   - Provide clear instructions for Claude

   - Reference CLAUDE.md standards in requests

3. **Security**:
   - Prefer MCP tools over CLI (no command injection risk)

   - Use quoted heredoc (`'EOF'`) if CLI is necessary

   - Never expose secrets in issue comments

   - Validate operations before execution

4. **Error Handling**:
   - Verify operation success before reporting

   - Provide clear error messages to user

   - Suggest manual alternatives on failure

   - Use fallback to CLI only when MCP unavailable

---

## Related Documentation

- **MCP Setup Guide**: `.claude/docs/01-guides/integration/integration/mcp.md`

- **MCP Authentication**: Use `/mcp` command in Claude Code

- **Security Validation**: `.claude/docs/security/layers/layer-2-injection-detection.md`

- **source-control Agent**: `.claude/agents/source-control.md`

- **GitHub Actions Integration**: [Anthropic Docs](https://docs.anthropic.com/claude/docs/claude-code/github-actions)

---

**Document Status**: Active reference for source-control agent

**Review Cycle**: Update when GitHub MCP tools or Actions workflows change

**Owner**: source-control agent (orchestrator coordinates)
