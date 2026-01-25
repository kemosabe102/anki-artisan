# Semantic Versioning Reference

**Purpose**: SemVer rules for version computation and validation

---

## Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
- v1.0.0          (stable release)
- v1.2.3          (stable release)
- v2.0.0-alpha.1  (pre-release)
- v2.0.0-beta.2   (pre-release)
- v2.0.0-rc.1     (release candidate)
- v1.2.3+build.42 (with build metadata)
```

---

## Version Components

| Component | Description | When to Increment |
|-----------|-------------|-------------------|
| MAJOR | Breaking changes | API incompatible changes |
| MINOR | New features | Backward compatible additions |
| PATCH | Bug fixes | Backward compatible fixes |

---

## Increment Rules


### MAJOR Version (X.0.0)

Increment when making incompatible API changes:

- Removing public API endpoints
- Changing function signatures
- Removing or renaming exported classes/functions
- Changing return types
- Breaking database schema changes

**Detection from Commits**:
```
BREAKING CHANGE: in commit body or footer
feat!: or fix!: (exclamation mark suffix)
```

**Examples**:
```
feat!: remove deprecated user API
fix!: change authentication response format

BREAKING CHANGE: The /api/v1/users endpoint has been removed.
Use /api/v2/users instead.
```

---

### MINOR Version (0.X.0)

Increment when adding functionality in a backward compatible manner:

- New API endpoints
- New optional parameters
- New exported functions/classes
- New features that don't break existing code


**Detection from Commits**:
```
feat: or feat(scope):
```

**Examples**:
```
feat(auth): add OAuth 2.0 support
feat(api): add pagination to list endpoints
feat: introduce dark mode theme
```

---

### PATCH Version (0.0.X)

Increment when making backward compatible bug fixes:

- Bug fixes
- Performance improvements
- Documentation updates
- Internal refactoring (no API changes)

**Detection from Commits**:
```
fix:, perf:, refactor:, docs:, style:, test:, chore:, ci:, build:
```

**Examples**:
```
fix(auth): correct token expiration calculation
perf(db): optimize query performance
docs: update API documentation
refactor: simplify error handling logic
```

---

## Pre-Release Versions


Pre-release versions indicate unstable releases:

| Stage | Format | Purpose |
|-------|--------|---------|
| Alpha | v1.0.0-alpha.1 | Internal testing, incomplete features |
| Beta | v1.0.0-beta.1 | External testing, feature complete |
| RC | v1.0.0-rc.1 | Release candidate, ready for release |

**Precedence** (lowest to highest):
```
v1.0.0-alpha.1 < v1.0.0-alpha.2 < v1.0.0-beta.1 < v1.0.0-rc.1 < v1.0.0
```

---

## Version Validation

### Valid Versions
```
v1.0.0
v0.1.0
v10.20.30
v1.0.0-alpha
v1.0.0-alpha.1
v1.0.0-0.3.7
v1.0.0-x.7.z.92
v1.0.0+20130313144700
v1.0.0-beta+exp.sha.5114f85
```

### Invalid Versions
```
1.0.0          (missing v prefix - project convention)
v1.0           (missing patch version)
v1.0.0.0       (too many components)
v01.0.0        (leading zeros)
v1.0.0-        (empty pre-release)
```


---

## Version Comparison

Versions are compared component by component:

```
v1.0.0 < v2.0.0    (MAJOR comparison)
v1.1.0 < v1.2.0    (MINOR comparison)
v1.1.1 < v1.1.2    (PATCH comparison)
v1.0.0-alpha < v1.0.0-beta < v1.0.0-rc < v1.0.0
```

---

## Initial Development (0.x.x)

During initial development (MAJOR = 0):
- Anything may change at any time
- Public API should not be considered stable
- v0.1.0 is typically the first development release
- v1.0.0 indicates first stable public API

---

## Git Commands for Version Operations

```bash
# Find latest version tag
git describe --tags --abbrev=0 --match "v*"

# List all version tags sorted
git tag -l "v*" --sort=-version:refname

# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Validate tag format (regex)
echo "v1.2.3" | grep -E "^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$"
```
