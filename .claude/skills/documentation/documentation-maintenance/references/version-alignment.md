# Version Alignment Reference

**Purpose**: Keep documentation synchronized with code versions across all documentation types.

---

## Synchronization Strategies

### Strategy 1: Single Source of Truth

Maintain version in ONE location, reference everywhere:

```python
# pyproject.toml
[project]
version = "2.3.0"
```

```yaml
# docs/_config.yml
version: "{{ read_version('pyproject.toml') }}"
```

```markdown
# README.md
Current version: {{ version }}
```

**Benefits:**
- No manual updates across files
- Eliminates version drift
- Single point of change

### Strategy 2: Version Metadata File

Centralize all version-related data:

```yaml
# .version-metadata.yml
current:
  version: "2.3.0"
  release_date: "2025-01-15"
  codename: "Falcon"
  
supported:
  - version: "2.3.0"
    eol_date: "2026-01-15"
  - version: "2.2.0"
    eol_date: "2025-07-15"
    
deprecated:
  - version: "2.1.0"
    sunset_date: "2025-03-01"
  - version: "2.0.0"
    sunset_date: "2025-01-01"
    
compatibility:
  python: ">=3.9,<4.0"
  dependencies:
    - package: "requests"
      min_version: "2.28.0"
```

### Strategy 3: Automated Version Injection

Use build-time or runtime injection:

```python
# Generate version-stamped docs at build time
import subprocess
from datetime import datetime

def inject_version():
    version = subprocess.check_output(['git', 'describe', '--tags']).decode().strip()
    build_date = datetime.now().isoformat()
    
    return {
        'version': version,
        'build_date': build_date
    }
```

---

## Changelog Synchronization

### Automated Changelog Generation

**From Git Commits:**

```bash
# Generate changelog from conventional commits
git log --pretty=format:"%s" v2.2.0..v2.3.0 | \
  grep -E "^(feat|fix|docs|refactor):" | \
  sort -t: -k1,1
```

**From PR Labels:**

```yaml
# .github/release.yml
changelog:
  categories:
    - title: "New Features"
      labels: ["enhancement", "feature"]
    - title: "Bug Fixes"
      labels: ["bug", "fix"]
    - title: "Documentation"
      labels: ["documentation"]
    - title: "Breaking Changes"
      labels: ["breaking-change"]
```

### Changelog Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-01-15

### Added
- New authentication module (#123) - [Docs](docs/auth.md)
- Support for async operations (#124) - [Guide](docs/async-guide.md)

### Changed
- Updated API endpoint structure (#125) - [Migration](docs/migrations/api-v2.3.md)
- Improved error handling (#126)

### Deprecated
- Old auth method - removal in v3.0.0 (#127) - [Alternative](docs/auth.md#new-method)

### Removed
- Legacy config format (deprecated in v2.0.0) (#128)

### Fixed
- Memory leak in worker pool (#129)
- Race condition in cache (#130)

### Security
- Updated dependency X to patch CVE-2025-1234 (#131)

[2.3.0]: https://github.com/org/repo/compare/v2.2.0...v2.3.0
```

### Documentation Links in Changelog

**Always include:**
- Link to feature documentation for "Added" items
- Link to migration guide for "Changed/Deprecated" items
- Link to security advisory for "Security" items

---

## API Documentation Version Matching

### Version-Specific API Docs

**Directory Structure:**

```
docs/api/
├── current/           # Always points to latest
│   ├── endpoints.md
│   └── schemas.md
├── v2.3/             # Version-specific
│   ├── endpoints.md
│   └── schemas.md
├── v2.2/
│   ├── endpoints.md
│   └── schemas.md
└── versions.json     # Version index
```

**versions.json:**

```json
{
  "current": "2.3.0",
  "supported": ["2.3.0", "2.2.0"],
  "deprecated": ["2.1.0"],
  "versions": {
    "2.3.0": {
      "release_date": "2025-01-15",
      "eol_date": "2026-01-15",
      "docs_path": "/docs/api/v2.3/",
      "changelog": "/changelog#2.3.0"
    }
  }
}
```

### API Doc Frontmatter

```yaml
---
api_version: "2.3.0"
last_updated: "2025-01-15"
code_reference: "src/api/v2/endpoints.py"
generated_from: "openapi-spec-v2.3.0.yml"
verified: true
---
```

### Schema Validation

Ensure API docs match implementation:

```python
# Conceptual validation - NOT executable
def validate_api_docs():
    # Extract schema from code
    code_schema = extract_schema_from_code("src/api/")
    
    # Extract schema from docs
    docs_schema = parse_openapi_spec("docs/api/openapi.yml")
    
    # Compare
    mismatches = compare_schemas(code_schema, docs_schema)
    
    if mismatches:
        raise ValueError(f"API docs out of sync: {mismatches}")
```

---

## Breaking Change Documentation

### Pre-Merge Requirements

**Before merging breaking change:**

1. Document the change in migration guide
2. Update API documentation
3. Add changelog entry
4. Update version compatibility matrix
5. Add deprecation notice (if applicable)

### Breaking Change Template

```markdown
# Breaking Change: [Feature Name]

## Version
- Introduced: v2.3.0
- Affects: v2.x users upgrading to v2.3.0+

## What Changed
Clear description of the breaking change.

## Why This Change
Rationale for the breaking change.

## Migration Path

### Before (v2.2.0)
```python
# Old usage
old_api.method(param1, param2)
```

### After (v2.3.0)
```python
# New usage
new_api.method(param1, param2, new_param="default")
```

## Step-by-Step Migration

1. Update dependencies to v2.3.0+
2. Replace old API calls with new signature
3. Add new required parameters
4. Test thoroughly

## Compatibility Notes
- Backward compatible: No
- Forward compatible: No
- Workaround available: Yes (see below)

## Temporary Workaround
If immediate migration is not possible, use compatibility layer:
```python
from compatibility import legacy_adapter
legacy_adapter.old_api.method(param1, param2)
```
```

---

## Version Badge Management

### Automated Badge Updates

```markdown
<!-- Auto-updated via CI -->
![Version](https://img.shields.io/badge/version-2.3.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
```

### Badge Update Script

```yaml
# .github/workflows/update-badges.yml
name: Update Version Badges
on:
  release:
    types: [published]

jobs:
  update-badges:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update version in README
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          sed -i "s/version-[0-9.]*-blue/version-${VERSION}-blue/" README.md
      - name: Commit changes
        run: |
          git config user.name "github-actions"
          git commit -am "Update version badges to ${VERSION}"
          git push
```

---

## Version Compatibility Matrix

### Matrix Template

```markdown
## Version Compatibility

| Component | v2.3.0 | v2.2.0 | v2.1.0 (deprecated) |
|-----------|--------|--------|---------------------|
| Python    | 3.9+   | 3.8+   | 3.7+                |
| Database  | 14+    | 12+    | 11+                 |
| API       | v2     | v2     | v1 (removed)        |
| SDK       | 2.3.x  | 2.2.x  | 2.1.x (EOL)         |

### Support Status
- ✅ **Supported**: Active development and security updates
- ⚠️ **Deprecated**: Security updates only, upgrade recommended
- ❌ **End of Life**: No updates, upgrade required
```

### Dependency Version Tracking

```yaml
# .dependency-versions.yml
documentation_version: "2.3.0"

dependencies:
  - name: python
    minimum: "3.9"
    recommended: "3.11"
    tested: ["3.9", "3.10", "3.11"]
    
  - name: database
    minimum: "14.0"
    recommended: "15.0"
    breaking_change_at: "16.0"

code_references:
  - file: "pyproject.toml"
    line: 12
  - file: "README.md"
    section: "Installation"
```

---

## Release Synchronization Workflow

### Pre-Release Checklist

**Documentation tasks before release:**

- [ ] Update version in all documentation files
- [ ] Generate/update changelog from commits/PRs
- [ ] Verify API docs match code (run schema validation)
- [ ] Update version badges in README
- [ ] Update compatibility matrix
- [ ] Review and finalize migration guides
- [ ] Verify all examples use correct version
- [ ] Check cross-references for version-specific links
- [ ] Update installation instructions

### Release-Day Actions

1. **Tag release in code repository**
2. **Publish updated documentation** (sync with code tag)
3. **Update version index** (versions.json)
4. **Archive previous version docs** (if major/minor release)
5. **Announce release** with changelog and docs links

### Post-Release Verification

**Within 24 hours of release:**

- [ ] Verify documentation site shows new version
- [ ] Test installation instructions with new version
- [ ] Check all version badges updated
- [ ] Verify changelog entry displays correctly
- [ ] Test navigation to new version-specific docs
- [ ] Monitor for user reports of doc/code mismatches

---

## Best Practices

1. **Single Source of Truth**: Version defined once, referenced everywhere
2. **Automate Updates**: Use CI/CD to update version badges and metadata
3. **Version Before Release**: Align docs before tagging release
4. **Link Changelog Entries**: Every change links to its documentation
5. **Validate Schemas**: Automated checks for API doc/code alignment
6. **Archive Old Versions**: Keep historical docs accessible
7. **Test Examples**: Verify code examples work with documented version
