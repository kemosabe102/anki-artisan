---
name: tag-release
description: >
  Semantic versioning and release tagging: version computation, annotated tag creation,
  release note generation, and tag lifecycle management. Use for releases, version bumps,
  changelogs, and tag operations.
---

# Tag Release Skill

**Domain**: Development  
**Responsibility**: Semantic versioning, release tagging, release note generation  
**Triggers**:
  - semantic-versioning metadata
  - release-workflows metadata
  - changelog generation metadata
  - tag operations metadata

---

## Overview

Owns the methodology and operations for:
- Computing next semantic version from commit history
- Creating annotated release tags
- Generating release notes from Conventional Commits
- Listing and managing release tags
- Managing version progression and release lifecycle


**Does NOT own**:
- Commits (see source-control skill)
- Branch management (see branch-strategy skill)
- GitHub releases/publishing (see github skill)
- Push to remote (orchestrator decision)
- CHANGELOG.md file editing (delegates to implementer)

---

## Core Operations

### compute_next_version

Analyzes commits since last release tag and suggests next semantic version.

```
Input: {
  current_version: string,      # Optional: e.g., "v1.2.3" (default: latest tag)
  include_prerelease: boolean   # Optional: consider pre-release versions (default: false)
}
Output: {
  current_version: "v1.2.3",
  next_version: "v1.3.0",
  bump_type: "minor",           # "major" | "minor" | "patch"
  reason: "feat: commits detected",
  commits_analyzed: 15,
  breaking_changes: [],
  features: ["feat(auth): add OAuth support"],
  fixes: ["fix(api): correct timeout handling"]
}
Logic: Parse commits since last tag, apply SemVer rules
```


**SemVer Rules Applied**:
| Commit Pattern | Version Bump | Priority |
|----------------|--------------|----------|
| `BREAKING CHANGE:` in body/footer | MAJOR | Highest |
| `feat!:` or `fix!:` (breaking indicator) | MAJOR | Highest |
| `feat:` or `feat(scope):` | MINOR | Medium |
| `fix:`, `perf:`, `refactor:` | PATCH | Low |
| `docs:`, `style:`, `test:`, `chore:` | PATCH | Lowest |

**Workflow**:
1. Find latest version tag: `git describe --tags --abbrev=0`
2. Get commits since tag: `git log {tag}..HEAD --oneline`
3. Parse each commit for Conventional Commit type
4. Detect breaking changes (body/footer or `!` suffix)
5. Apply highest priority bump rule
6. Return structured result

---

### create_release_tag

Creates an annotated git tag for a release version.

```
Input: {
  version: string,              # Required: e.g., "v1.3.0"
  message: string,              # Optional: tag message (default: auto-generated)
  sign: boolean                 # Optional: GPG sign the tag (default: false)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  tag: "v1.3.0",
  commit_sha: "abc1234567890",
  signed: false,
  message: "Release v1.3.0\n\nFeatures:\n- ..."
}
Logic: Validate version format -> create annotated tag
```


**Pre-Tag Validation** (MANDATORY):
- Version format matches SemVer (`vMAJOR.MINOR.PATCH`)
- Tag does not already exist
- Working directory is clean (no uncommitted changes)
- Not in detached HEAD state (unless intentional)

**Workflow**:
1. Validate version format
2. Check tag doesn't exist: `git tag -l {version}`
3. Generate tag message if not provided
4. Create annotated tag: `git tag -a {version} -m "{message}"`
5. Optionally sign: `git tag -s {version} -m "{message}"`
6. Return tag info

---

### list_tags

Lists all version tags with metadata.

```
Input: {
  pattern: string,              # Optional: glob pattern (default: "v*")
  limit: number,                # Optional: max results (default: 20)
  sort: string                  # Optional: "version" | "date" (default: "version")
}
Output: {
  tags: [
    {
      tag: "v1.3.0",
      commit_sha: "abc1234",
      date: "2025-01-15",
      tagger: "John Doe <john@example.com>",
      message: "Release v1.3.0"
    },
    ...
  ],
  total_count: 15,
  latest: "v1.3.0"
}
Logic: git tag -l with format and sorting
```


**Workflow**:
1. List tags: `git tag -l "{pattern}" --sort=-version:refname`
2. For each tag, get metadata: `git tag -l {tag} --format="..."`
3. Parse and structure results
4. Return sorted list

---

### delete_tag

Removes a tag from local repository.

```
Input: {
  tag: string,                  # Required: tag name to delete
  delete_remote: boolean        # Optional: also delete from remote (default: false)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  deleted_local: true,
  deleted_remote: false,
  warnings: []
}
Logic: Validate tag exists -> delete local -> optionally delete remote
```

**Safety Checks**:
- Confirms tag exists before deletion
- Remote deletion requires explicit `delete_remote: true`
- Warns if tag is the latest release

**Workflow**:
1. Verify tag exists: `git tag -l {tag}`
2. Delete local: `git tag -d {tag}`
3. If delete_remote: `git push origin :refs/tags/{tag}`
4. Return status


---

### get_release_notes

Generates release notes from commit messages between two versions.

```
Input: {
  from_version: string,         # Required: starting version (exclusive)
  to_version: string            # Optional: ending version (default: HEAD)
}
Output: {
  from_version: "v1.2.0",
  to_version: "v1.3.0",
  notes: {
    breaking_changes: [
      { commit: "abc123", message: "BREAKING: remove deprecated API" }
    ],
    features: [
      { commit: "def456", scope: "auth", message: "add OAuth support" }
    ],
    fixes: [
      { commit: "ghi789", scope: "api", message: "correct timeout handling" }
    ],
    performance: [],
    other: [
      { commit: "jkl012", type: "docs", message: "update README" }
    ]
  },
  markdown: "## v1.3.0\n\n### Breaking Changes\n- ..."
}
Logic: Parse commits between versions, group by type
```

**Grouping by Conventional Commit Type**:
| Type | Section Header |
|------|----------------|
| `BREAKING CHANGE` / `!` | Breaking Changes |
| `feat` | Features |
| `fix` | Bug Fixes |
| `perf` | Performance |
| `refactor` | Refactoring |
| `docs`, `style`, `test`, `chore`, `ci`, `build` | Other |


**Workflow**:
1. Get commits: `git log {from}..{to} --format="%H %s"`
2. Parse each commit for Conventional Commit format
3. Group by type
4. Generate markdown output
5. Return structured and formatted notes

---

## Key Methodologies

### Semantic Versioning
[See reference/semantic-versioning.md](reference/semantic-versioning.md)

Format: `MAJOR.MINOR.PATCH` (prefixed with `v`)

| Component | Increment When |
|-----------|----------------|
| MAJOR | Breaking changes (API incompatible) |
| MINOR | New features (backward compatible) |
| PATCH | Bug fixes (backward compatible) |

Pre-release: `v1.2.3-alpha.1`, `v1.2.3-beta.2`, `v1.2.3-rc.1`

### Release Workflows
[See reference/release-workflows.md](reference/release-workflows.md)

- Version bump procedure
- Tag creation and signing
- Release note generation
- CHANGELOG.md update pattern

### Release Notes
[See reference/release-notes.md](reference/release-notes.md)

- Conventional Commit parsing
- Grouping by change type
- Markdown formatting
- GitHub release body format


---

## Error Handling

[See reference/error-handling.md](reference/error-handling.md)

| Error | Category | Recovery |
|-------|----------|----------|
| "Tag already exists" | PERMANENT | Choose different version or delete existing |
| "Invalid version format" | PERMANENT | Correct version to match SemVer pattern |
| "No tags found" | SOFT | Initialize with v0.1.0 or v1.0.0 |
| "Uncommitted changes" | PERMANENT | Commit or stash changes first |
| "GPG signing failed" | PERMANENT | Check GPG key configuration |
| "Remote tag exists" | PERMANENT | Delete remote tag first or choose new version |
| "Cannot parse commits" | SOFT | Fall back to manual release notes |

---

## Delegation Patterns

[See delegation/patterns.md](delegation/patterns.md)

All operations delegate to `source-control` agent. This skill provides:
- Operation definitions and validation rules
- SemVer computation logic
- Release note formatting
- Error recovery guidance

**Example Delegation**:
```
Task(source-control) with:
  operation: create_release_tag
  params: { version: "v1.3.0", message: "Release v1.3.0\n\n..." }
```


---

## Safety Constraints

### SAFE Operations
- `git tag -l` (list tags)
- `git describe --tags` (find latest tag)
- `git log {tag}..HEAD` (commits since tag)
- `git tag -a` (create annotated tag)

### REQUIRES CONFIRMATION
- `git tag -d` (delete local tag)
- `git push origin :refs/tags/{tag}` (delete remote tag)
- `git push --tags` (push all tags to remote)

### FORBIDDEN (This Skill)
- `git tag -f` (force overwrite existing tag)
- Direct commits (see source-control skill)
- Branch operations (see branch-strategy skill)

---

## Bash Command Format

All git commands use AGENT_NAME prefix for logging:

```bash
AGENT_NAME=tag-release git describe --tags --abbrev=0
AGENT_NAME=tag-release git tag -l "v*" --sort=-version:refname
AGENT_NAME=tag-release git tag -a v1.3.0 -m "Release v1.3.0"
AGENT_NAME=tag-release git log v1.2.0..HEAD --oneline
```


---

## Examples

[See examples/usage-examples.md](examples/usage-examples.md)

### Quick Start
```
User: "What should the next version be?"
Skill: compute_next_version() -> "v1.3.0 (minor bump: feat commits detected)"

User: "Create a release tag"
Skill: compute_next_version() -> create_release_tag("v1.3.0")

User: "Generate release notes for this version"
Skill: get_release_notes("v1.2.0", "HEAD") -> markdown changelog
```

---

## Thinking Frameworks

When facing complex release challenges:

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Tag Release**:

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Debugging version conflicts, tracing tag history |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Assessing risks before major version releases |

> **Selection Tip**: version conflicts -> ReACT, major releases -> Pre-Mortem

---

## References

| File | Purpose |
|------|---------|
| reference/semantic-versioning.md | SemVer rules and examples |
| reference/release-workflows.md | Version bump and tag workflows |
| reference/release-notes.md | Changelog generation patterns |
| reference/error-handling.md | Error classification patterns |
| delegation/patterns.md | Task() delegation templates |
| examples/usage-examples.md | End-to-end workflow examples |
