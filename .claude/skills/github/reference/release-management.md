# Release Management Reference

**Purpose**: GitHub Release publishing (platform releases, NOT git tags)

---

## Overview

This skill manages GitHub Releases, which are:
- Published releases on github.com (visible on Releases page)
- Associated with git tags
- Include release notes, assets, and metadata

**Note**: For git tag creation, use the tag-release skill.

---

## Creating Releases

### Prerequisites
1. Git tag must exist (create via tag-release skill)
2. Tag must be pushed to remote
3. Authenticated via gh CLI

### Via gh CLI
```bash
# Basic release
AGENT_NAME=github gh release create v1.3.0

# With title and notes
AGENT_NAME=github gh release create v1.3.0 \
  --title "v1.3.0" \
  --notes "## Changes\n\n- Feature 1\n- Bug fix 2"

# Draft release
AGENT_NAME=github gh release create v1.3.0 --draft

# Prerelease
AGENT_NAME=github gh release create v1.3.0-beta.1 --prerelease

# Auto-generate notes
AGENT_NAME=github gh release create v1.3.0 --generate-notes

# From specific tag
AGENT_NAME=github gh release create v1.3.0 --target main
```

---

## Release Notes Template

```markdown
## v1.3.0

### Breaking Changes

- Changed API endpoint from /v1 to /v2

### Features

- Added OAuth2 support (#123)
- New dashboard widgets (#145)

### Bug Fixes

- Fixed login timeout issue (#134)
- Resolved memory leak in worker (#156)

### Performance

- Improved query performance by 40%

### Documentation

- Updated API reference
- Added migration guide

---

**Full Changelog**: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
```

---

## Listing Releases

```bash
# List all releases
AGENT_NAME=github gh release list

# List with limit
AGENT_NAME=github gh release list --limit 10

# View specific release
AGENT_NAME=github gh release view v1.3.0

# View latest release
AGENT_NAME=github gh release view --latest
```

---

## Editing Releases

```bash
# Update title
AGENT_NAME=github gh release edit v1.3.0 --title "Version 1.3.0"

# Update notes
AGENT_NAME=github gh release edit v1.3.0 --notes "Updated notes..."

# Publish draft
AGENT_NAME=github gh release edit v1.3.0 --draft=false

# Mark as prerelease
AGENT_NAME=github gh release edit v1.3.0 --prerelease

# Mark as latest
AGENT_NAME=github gh release edit v1.3.0 --latest
```

---

## Release Assets

### Upload Assets
```bash
# Upload single file
AGENT_NAME=github gh release upload v1.3.0 ./dist/app-v1.3.0.zip

# Upload multiple files
AGENT_NAME=github gh release upload v1.3.0 ./dist/*.tar.gz

# Upload with custom name
AGENT_NAME=github gh release upload v1.3.0 ./build/app.exe#app-windows-v1.3.0.exe
```

### Download Assets
```bash
# Download all assets
AGENT_NAME=github gh release download v1.3.0

# Download specific asset
AGENT_NAME=github gh release download v1.3.0 --pattern "*.tar.gz"
```

---

## Deleting Releases

```bash
# Delete release (keeps tag)
AGENT_NAME=github gh release delete v1.3.0

# Delete with confirmation skip
AGENT_NAME=github gh release delete v1.3.0 --yes

# Delete release and tag
AGENT_NAME=github gh release delete v1.3.0 --cleanup-tag
```

**Warning**: Deleting releases is permanent. Use with caution.

---

## Auto-Generate Notes

GitHub can auto-generate release notes from PRs:

```bash
AGENT_NAME=github gh release create v1.3.0 --generate-notes
```

Configuration via `.github/release.yml`:
```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
  categories:
    - title: Breaking Changes
      labels:
        - breaking
    - title: Features
      labels:
        - feature
        - enhancement
    - title: Bug Fixes
      labels:
        - bug
        - fix
    - title: Other Changes
      labels:
        - "*"
```

---

## Workflow Integration

### Release on Tag Push

Automate releases via GitHub Actions:

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create ${{ github.ref_name }} \
            --generate-notes
```

---

## Skill Boundary

| Operation | This Skill (github) | tag-release Skill |
|-----------|---------------------|-------------------|
| Create git tag | No | Yes |
| List git tags | No | Yes |
| Create GitHub Release | Yes | No |
| Upload release assets | Yes | No |
| Generate release notes | Yes | No |

---

## Error Scenarios

| Error | Cause | Recovery |
|-------|-------|----------|
| "Tag not found" | Tag does not exist | Create tag via tag-release skill |
| "Release already exists" | Release for tag exists | Edit existing or use different tag |
| "Asset upload failed" | File not found | Verify file path |
| "Permission denied" | Insufficient access | Check repository permissions |
