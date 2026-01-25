# Tag Release Usage Examples

**Purpose**: End-to-end workflow examples for tag and release operations

---

## Example 1: Standard Release Workflow

### Scenario
User wants to create a new release after completing several features and fixes.

### Conversation Flow

**User**: "What should the next version be?"

**Orchestrator**:
1. Invokes tag-release skill for guidance
2. Delegates: Task(source-control, operation="compute_next_version")

**Agent executes**:
```bash
git describe --tags --abbrev=0  # -> v1.2.3
git log v1.2.3..HEAD --oneline  # -> 12 commits
```

**Agent returns**:
```json
{
  "current_version": "v1.2.3",
  "next_version": "v1.3.0",
  "bump_type": "minor",
  "reason": "feat: commits detected (3 features, no breaking changes)",
  "commits_analyzed": 12,
  "features": [
    "feat(auth): add OAuth support",
    "feat(api): add pagination",
    "feat(ui): add dark mode"
  ],
  "fixes": [
    "fix(auth): correct token handling",
    "fix(api): timeout issue"
  ]
}
```

**Orchestrator presents**:
> Suggested version: v1.3.0 (minor bump)
> 12 commits analyzed: 3 features, 2 fixes, 7 other
> Proceed with v1.3.0? [y/n]

**User**: "Yes, create the release"

**Orchestrator**:
1. Delegates: Task(source-control, operation="get_release_notes", from="v1.2.3")
2. Delegates: Task(source-control, operation="create_release_tag", version="v1.3.0")

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "tag": "v1.3.0",
  "commit_sha": "abc1234567890",
  "message": "Release v1.3.0..."
}
```

**Orchestrator reports**:
> Created release tag v1.3.0 at commit abc1234
> Push to remote with: git push origin v1.3.0

---

## Example 2: Pre-Release Workflow

### Scenario
User wants to create a beta release for testing new features.

### Conversation Flow

**User**: "Create a beta release for the new auth system"

**Orchestrator**:
1. Computes next version (currently at v1.2.3)
2. Suggests pre-release: v1.3.0-beta.1

**Agent executes**:
```bash
git tag -l "v1.3.0-beta*"  # Check for existing betas
# No existing betas found
```

**Orchestrator presents**:
> Suggested pre-release: v1.3.0-beta.1
> This indicates feature-complete but not production-ready
> Proceed? [y/n]

**User**: "Yes"

**Agent creates**:
```bash
git tag -a v1.3.0-beta.1 -m "v1.3.0-beta.1 - Auth system beta"
```

**Orchestrator reports**:
> Created pre-release tag v1.3.0-beta.1
> Note: Pre-release versions are not considered latest

---

## Example 3: Hotfix Release

### Scenario
Critical bug discovered in production, need immediate patch release.

### Conversation Flow

**User**: "We need a hotfix release, there is a critical auth bug"

**Orchestrator**:
1. Gets current version: v1.3.0
2. Suggests patch: v1.3.1

**Agent executes**:
```bash
git describe --tags --abbrev=0  # -> v1.3.0
git log v1.3.0..HEAD --oneline  # -> 1 commit (the fix)
```

**Orchestrator presents**:
> Hotfix release: v1.3.1
> Changes since v1.3.0:
> - fix(auth): critical security patch (#456)
> Proceed? [y/n]

**User**: "Yes, and push it immediately"

**Agent creates tag and pushes**:
```bash
git tag -a v1.3.1 -m "v1.3.1 - Security hotfix"
git push origin v1.3.1
```

**Orchestrator reports**:
> Created and pushed hotfix v1.3.1
> Tag: v1.3.1 at commit def789

---

## Example 4: Generating Release Notes Only

### Scenario
User wants to see what would be in the next release without creating it.

### Conversation Flow

**User**: "Show me what would be in the release notes"

**Orchestrator**:
1. Delegates: Task(source-control, operation="get_release_notes", from="v1.2.3")

**Agent executes**:
```bash
git log v1.2.3..HEAD --format="%H|%s|%b"
```

**Agent returns**:
```json
{
  "from_version": "v1.2.3",
  "to_version": "HEAD",
  "notes": {
    "breaking_changes": [],
    "features": [
      { "commit": "abc123", "scope": "auth", "message": "add OAuth support" },
      { "commit": "def456", "scope": "api", "message": "add pagination" }
    ],
    "fixes": [
      { "commit": "ghi789", "scope": "auth", "message": "correct token handling" }
    ],
    "other": [
      { "commit": "jkl012", "type": "docs", "message": "update README" },
      { "commit": "mno345", "type": "test", "message": "add auth tests" }
    ]
  },
  "markdown": "..."
}
```

**Orchestrator presents**:
> ## Upcoming v1.3.0
> 
> ### Features
> - **auth**: add OAuth support (abc123)
> - **api**: add pagination (def456)
> 
> ### Bug Fixes
> - **auth**: correct token handling (ghi789)
> 
> ### Other
> - docs: update README
> - test: add auth tests
> 
> No breaking changes detected.
> Ready to create release? [y/n]

---

## Example 5: Breaking Change Detection

### Scenario
User has made breaking changes and needs a major version bump.

### Conversation Flow

**User**: "Prepare the release"

**Orchestrator**:
1. Delegates version computation

**Agent analyzes commits**:
- "feat\!: remove deprecated v1 API"
- "feat(auth): change response format"
- "BREAKING CHANGE: authentication response now includes..."

**Agent returns**:
```json
{
  "current_version": "v1.3.0",
  "next_version": "v2.0.0",
  "bump_type": "major",
  "reason": "BREAKING CHANGE detected",
  "breaking_changes": [
    "feat\!: remove deprecated v1 API",
    "feat(auth): change response format [BREAKING]"
  ]
}
```

**Orchestrator presents**:
> WARNING: Breaking changes detected\!
> 
> Recommended: v2.0.0 (MAJOR bump)
> 
> Breaking Changes:
> - Remove deprecated v1 API
> - Authentication response format changed
> 
> This indicates incompatible API changes.
> Consumers will need to update their code.
> 
> Proceed with v2.0.0? [y/n]

---

## Example 6: List Existing Tags

### Scenario
User wants to see release history.

### Conversation Flow

**User**: "Show me all releases"

**Orchestrator**:
1. Delegates: Task(source-control, operation="list_tags")

**Agent executes**:
```bash
git tag -l "v*" --sort=-version:refname --format="%(refname:short)|%(creatordate:short)|%(subject)"
```

**Agent returns**:
```json
{
  "tags": [
    { "tag": "v1.3.0", "date": "2025-01-15", "message": "Release v1.3.0" },
    { "tag": "v1.2.3", "date": "2025-01-10", "message": "Release v1.2.3" },
    { "tag": "v1.2.2", "date": "2025-01-05", "message": "Hotfix release" },
    { "tag": "v1.2.1", "date": "2025-01-03", "message": "Release v1.2.1" },
    { "tag": "v1.2.0", "date": "2025-01-01", "message": "Release v1.2.0" }
  ],
  "total_count": 5,
  "latest": "v1.3.0"
}
```

**Orchestrator presents**:
> Release History (5 releases):
> 
> v1.3.0  2025-01-15  Release v1.3.0 (latest)
> v1.2.3  2025-01-10  Release v1.2.3
> v1.2.2  2025-01-05  Hotfix release
> v1.2.1  2025-01-03  Release v1.2.1
> v1.2.0  2025-01-01  Release v1.2.0

---

## Example 7: Delete a Tag

### Scenario
User needs to remove an incorrectly created tag.

### Conversation Flow

**User**: "Delete the v1.3.1 tag, it was created by mistake"

**Orchestrator**:
1. Confirms tag exists
2. Asks about remote deletion

**Orchestrator presents**:
> Found tag v1.3.1 (local)
> 
> Options:
> 1. Delete local only
> 2. Delete local and remote
> 
> Which option? [1/2]

**User**: "Delete local and remote"

**Agent executes**:
```bash
git tag -d v1.3.1
git push origin :refs/tags/v1.3.1
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "deleted_local": true,
  "deleted_remote": true,
  "warnings": []
}
```

**Orchestrator reports**:
> Deleted tag v1.3.1 from local and remote

---

## Example 8: Error Recovery - Tag Exists

### Scenario
User tries to create a tag that already exists.

### Conversation Flow

**User**: "Create release v1.3.0"

**Agent attempts**:
```bash
git tag -a v1.3.0 -m "..."
```

**Agent returns**:
```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "tag_exists",
    "error_classification": "PERMANENT",
    "error_message": "fatal: tag v1.3.0 already exists",
    "recovery_suggestions": [
      "Delete existing tag: git tag -d v1.3.0",
      "Choose different version: v1.3.1",
      "View existing tag: git show v1.3.0"
    ]
  }
}
```

**Orchestrator presents**:
> Cannot create v1.3.0 - tag already exists
> 
> Options:
> 1. View existing v1.3.0 tag details
> 2. Delete v1.3.0 and recreate
> 3. Create v1.3.1 instead
> 
> What would you like to do?

---

## Quick Reference: Common Operations

| User Request | Skill Operation | Key Commands |
|--------------|-----------------|--------------|
| "What version next?" | compute_next_version | git describe, git log |
| "Create release" | create_release_tag | git tag -a |
| "Show releases" | list_tags | git tag -l |
| "Generate changelog" | get_release_notes | git log --format |
| "Delete tag" | delete_tag | git tag -d, git push origin :refs/tags/ |
| "Create beta" | create_release_tag (pre-release) | git tag -a v1.0.0-beta.1 |

