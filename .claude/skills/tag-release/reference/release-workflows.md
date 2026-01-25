# Release Workflows Reference

**Purpose**: Step-by-step workflows for version bumps, tag creation, and release management

---

## Standard Release Workflow

### 1. Prepare for Release

```bash
# Ensure on main/release branch
git checkout main
git pull origin main

# Verify working directory is clean
git status

# Run tests to ensure everything passes
uv run pytest
```

### 2. Compute Next Version

```bash
# Find current version
git describe --tags --abbrev=0

# Analyze commits since last release
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Determine bump type based on commits:
# - BREAKING CHANGE / feat! / fix! -> MAJOR
# - feat: -> MINOR
# - fix:, perf:, docs:, etc. -> PATCH
```


### 3. Generate Release Notes

```bash
# Get commits for release notes
git log v1.2.0..HEAD --format="%h %s" --reverse

# Group by type (manual or automated)
# - Breaking Changes
# - Features
# - Bug Fixes
# - Other
```

### 4. Create Annotated Tag

```bash
# Create annotated tag with message
git tag -a v1.3.0 -m "Release v1.3.0

## What's Changed

### Features
- feat(auth): add OAuth 2.0 support
- feat(api): add pagination

### Bug Fixes
- fix(auth): correct token handling

Generated with [Claude Code](https://claude.com/claude-code)
"

# Or sign the tag (if GPG configured)
git tag -s v1.3.0 -m "Release v1.3.0..."
```


### 5. Push Tag to Remote

```bash
# Push specific tag
git push origin v1.3.0

# Or push all tags (use with caution)
git push origin --tags
```

### 6. Verify Release

```bash
# Verify tag was created
git tag -l v1.3.0

# Verify tag message
git tag -l v1.3.0 -n10

# Verify remote has tag
git ls-remote --tags origin | grep v1.3.0
```

---

## Pre-Release Workflow

For alpha, beta, or release candidate versions:

```bash
# Alpha release
git tag -a v2.0.0-alpha.1 -m "v2.0.0-alpha.1 - Early testing"

# Beta release
git tag -a v2.0.0-beta.1 -m "v2.0.0-beta.1 - Feature complete"

# Release candidate
git tag -a v2.0.0-rc.1 -m "v2.0.0-rc.1 - Release candidate"

# Increment pre-release
git tag -a v2.0.0-alpha.2 -m "v2.0.0-alpha.2 - Second alpha"
```


---

## Hotfix Release Workflow

For urgent fixes to production:

```bash
# Start from latest release tag
git checkout v1.2.3
git checkout -b hotfix/critical-fix

# Make fix and commit
# ... make changes ...
git commit -m "fix(security): patch critical vulnerability"

# Tag the hotfix
git tag -a v1.2.4 -m "v1.2.4 - Security hotfix"

# Push tag
git push origin v1.2.4

# Merge back to main (don't forget!)
git checkout main
git merge hotfix/critical-fix
```

---

## Tag Signing

### Configure GPG Signing

```bash
# List GPG keys
gpg --list-secret-keys --keyid-format LONG

# Configure git to use GPG key
git config --global user.signingkey YOUR_KEY_ID

# Enable tag signing by default
git config --global tag.gpgsign true
```


### Create Signed Tag

```bash
# Sign tag with -s flag
git tag -s v1.3.0 -m "Release v1.3.0"

# Verify signature
git tag -v v1.3.0
```

---

## Tag Deletion Workflow

### Delete Local Tag

```bash
git tag -d v1.3.0
```

### Delete Remote Tag

```bash
git push origin :refs/tags/v1.3.0

# Or using --delete
git push origin --delete v1.3.0
```

### Replace Existing Tag (DANGEROUS)

```bash
# Delete existing tag
git tag -d v1.3.0
git push origin :refs/tags/v1.3.0

# Create new tag at current HEAD
git tag -a v1.3.0 -m "Release v1.3.0 (re-release)"
git push origin v1.3.0
```

**Warning**: Replacing tags can cause issues for users who already fetched the original tag.


---

## CHANGELOG.md Update Pattern

After creating a release tag, update CHANGELOG.md:

```markdown
# Changelog

## [v1.3.0] - 2025-01-15

### Added
- OAuth 2.0 authentication support (#123)
- Pagination for list endpoints (#124)

### Fixed
- Token expiration calculation (#125)

### Changed
- Improved error messages for API errors

## [v1.2.0] - 2025-01-01

...
```

**Note**: CHANGELOG.md editing is delegated to implementation agents, not performed by this skill directly.

---

## Quick Reference

| Task | Command |
|------|---------|
| Find latest tag | `git describe --tags --abbrev=0` |
| List all tags | `git tag -l "v*" --sort=-version:refname` |
| Create annotated tag | `git tag -a v1.3.0 -m "message"` |
| Create signed tag | `git tag -s v1.3.0 -m "message"` |
| Push single tag | `git push origin v1.3.0` |
| Push all tags | `git push origin --tags` |
| Delete local tag | `git tag -d v1.3.0` |
| Delete remote tag | `git push origin :refs/tags/v1.3.0` |
| View tag details | `git show v1.3.0` |
| Verify signed tag | `git tag -v v1.3.0` |
