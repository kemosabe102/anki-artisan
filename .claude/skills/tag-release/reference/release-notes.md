# Release Notes Reference

**Purpose**: Changelog generation from Conventional Commits

---

## Commit Parsing

### Conventional Commit Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Type to Section Mapping

| Commit Type | Release Notes Section | Priority |
|-------------|----------------------|----------|
| `BREAKING CHANGE` | Breaking Changes | 1 (highest) |
| `feat!`, `fix!` | Breaking Changes | 1 |
| `feat` | Features | 2 |
| `fix` | Bug Fixes | 3 |
| `perf` | Performance | 4 |
| `refactor` | Refactoring | 5 |
| `docs` | Documentation | 6 |
| `test` | Testing | 7 |
| `build`, `ci` | Build & CI | 8 |
| `style`, `chore` | Other | 9 (lowest) |

---

## Release Notes Structure


### Standard Format

```markdown
## v1.3.0 (2025-01-15)

### Breaking Changes
- **api**: remove deprecated `/v1/users` endpoint (#123)

### Features
- **auth**: add OAuth 2.0 support (#124)
- **api**: add pagination to list endpoints (#125)

### Bug Fixes
- **auth**: correct token expiration calculation (#126)
- **db**: fix connection pool leak (#127)

### Performance
- **query**: optimize database queries for large datasets (#128)

### Documentation
- update API reference for v2 endpoints (#129)

### Other
- update dependencies to latest versions (#130)
```

---

## Parsing Commits for Release Notes

### Git Command to Extract Commits

```bash
# Get commits since last tag with full message
git log v1.2.0..HEAD --format="%H|%s|%b" --reverse
```


### Parsing Logic

1. **Extract type**: Match `^(\w+)(\(.+\))?!?:` pattern
2. **Extract scope**: Parse content within parentheses
3. **Detect breaking**: Check for `!` suffix or `BREAKING CHANGE:` in body/footer
4. **Extract subject**: Text after `:` on first line
5. **Extract PR/issue**: Match `(#\d+)` pattern

### Example Parsing

```
Input:  "feat(auth): add OAuth support (#123)"
Output: {
  type: "feat",
  scope: "auth",
  subject: "add OAuth support",
  breaking: false,
  pr: "#123"
}

Input:  "fix!: critical security patch"
Output: {
  type: "fix",
  scope: null,
  subject: "critical security patch",
  breaking: true,
  pr: null
}
```

---

## Grouping Algorithm

```python
def group_commits(commits):
    groups = {
        "breaking": [],
        "features": [],
        "fixes": [],
        "performance": [],
        "other": []
    }
    
    for commit in commits:
        if commit.breaking:
            groups["breaking"].append(commit)
        elif commit.type == "feat":
            groups["features"].append(commit)
        elif commit.type == "fix":
            groups["fixes"].append(commit)
        elif commit.type == "perf":
            groups["performance"].append(commit)
        else:
            groups["other"].append(commit)
    
    return groups
```


---

## Markdown Formatting

### Section Headers

```markdown
### Breaking Changes
### Features  
### Bug Fixes
### Performance
### Documentation
### Other
```

### Entry Format

```markdown
- **<scope>**: <subject> (<pr>)
- <subject> (<pr>)  # when no scope
```

### Examples

```markdown
- **auth**: add OAuth 2.0 support (#124)
- **api**: add pagination to list endpoints (#125)
- update README with new examples (#130)
```

---

## GitHub Release Body Format

For GitHub releases (via `gh` CLI or API):

```markdown
## What's Changed

### Breaking Changes
- **api**: remove deprecated endpoint (#123)

### New Features
- **auth**: add OAuth 2.0 support (#124)

### Bug Fixes
- **auth**: fix token refresh (#126)

**Full Changelog**: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
```


---

## Edge Cases

### Commits Without Conventional Format

If commit doesn't match Conventional Commits pattern:
1. Classify as "Other"
2. Use full commit message as subject
3. Flag as `needs_review: true`

### Multiple Types in One Commit

If commit has multiple types (rare, non-standard):
1. Use the first type detected
2. Log warning for manual review

### Empty Sections

Omit sections with no entries:
```markdown
# v1.3.0

### Bug Fixes
- fix(api): correct error handling

# Note: No Features, Breaking Changes, etc. sections
```

---

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| Get commits | `git log v1.2.0..HEAD --format="%H\|%s\|%b"` |
| Parse type | `/^(\w+)(\(.+\))?!?:/` |
| Parse scope | `/\(([^)]+)\)/` |
| Detect breaking | `!:` suffix OR `BREAKING CHANGE:` in body |
| Parse PR | `/(#\d+)/` |
