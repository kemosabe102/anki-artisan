# Error Handling for Tag Release Operations

**Purpose**: Error classification and recovery patterns for tag/release operations

**MANDATORY**: Classify errors BEFORE taking recovery actions.

---

## Error Classification Overview

| Category | Retry? | Max Attempts | Action |
|----------|--------|--------------|--------|
| PERMANENT | No | 0 | Return FAILURE with recovery suggestions |
| TRANSIENT | Yes | 3 | Exponential backoff, then FAILURE |
| SOFT | No | 0 | Warn user, proceed with caution |

---

## Tag Operation Errors

### PERMANENT (No Retry)

| Error Pattern | Example Message | Recovery Suggestion |
|---------------|-----------------|---------------------|
| Tag already exists | "fatal: tag 'v1.3.0' already exists" | Delete existing tag or choose different version |
| Invalid version format | "v1.3 is not valid SemVer" | Correct to MAJOR.MINOR.PATCH format |
| Uncommitted changes | "Please commit or stash changes" | Commit or stash before tagging |
| GPG signing failed | "gpg failed to sign the data" | Check GPG key configuration |
| Remote tag exists | "error: tag 'v1.3.0' already exists on remote" | Delete remote tag first |
| No tags found | "fatal: No names found" | Initialize with v0.1.0 or v1.0.0 |
| Detached HEAD | "HEAD detached" | Checkout branch before tagging |


### TRANSIENT (Retry with Backoff)

| Error Pattern | Example Message | Backoff |
|---------------|-----------------|---------|
| Network timeout | "Connection timed out" | 2s, 4s, 8s |
| Remote unavailable | "Could not resolve host" | 2s, 4s, 8s |
| Lock file busy | ".git/index.lock already exists" | 1s, 2s, 4s |

### SOFT (Warn and Proceed)

| Error Pattern | Example Message | Action |
|---------------|-----------------|--------|
| No conventional commits | "Could not parse commit types" | Warn, fall back to manual notes |
| Mixed commit formats | "Some commits not conventional" | Warn, include unparsed in "Other" |
| Pre-release detected | "Current version is pre-release" | Warn user, confirm increment |

---

## Failure Output Schema

When returning FAILURE, include classification context:

```json
{
  "status": "FAILURE",
  "operation": "create_release_tag",
  "failure_details": {
    "failure_type": "tag_exists",
    "error_classification": "PERMANENT",
    "retry_attempts": 0,
    "error_message": "fatal: tag 'v1.3.0' already exists",
    "recovery_suggestions": [
      "Delete existing tag: git tag -d v1.3.0",
      "Choose different version: v1.3.1 or v1.4.0",
      "Use force (DANGEROUS): git tag -f v1.3.0"
    ]
  }
}
```


---

## Common Recovery Paths

### Tag Already Exists (Local)

```bash
# Option 1: Delete and recreate
git tag -d v1.3.0
git tag -a v1.3.0 -m "Release v1.3.0"

# Option 2: Choose next patch version
git tag -a v1.3.1 -m "Release v1.3.1"
```

### Tag Already Exists (Remote)

```bash
# Delete remote tag first
git push origin :refs/tags/v1.3.0

# Then push new tag
git push origin v1.3.0
```

### GPG Signing Failed

```bash
# Check GPG key
gpg --list-secret-keys

# Test signing
echo "test" | gpg --clearsign

# If key expired, generate new or extend
gpg --edit-key YOUR_KEY_ID
> expire
> save

# Or disable signing for this tag
git tag -a v1.3.0 -m "Release v1.3.0"  # without -s
```


### No Tags Found (First Release)

```bash
# Initialize with v0.1.0 (development)
git tag -a v0.1.0 -m "Initial development release"

# Or v1.0.0 (stable)
git tag -a v1.0.0 -m "Initial stable release"
```

### Cannot Parse Commits

```bash
# Fall back to manual release notes
# List all commits since beginning or last known good state
git log --oneline

# Create tag with manual message
git tag -a v1.3.0 -m "Release v1.3.0

- Feature A
- Bug fix B
- Improvement C
"
```

---

## Anti-Patterns

- Force-overwriting tags without user confirmation
- Retrying PERMANENT errors
- Pushing tags before verifying they're correct
- Creating tags on dirty working directory
- Skipping version validation

---

## Retry Configuration

### Tag Creation

```
max_retries: 0 (most errors are PERMANENT)
```

### Remote Operations (push)

```
max_retries: 3
backoff: exponential (2s, 4s, 8s)
retry_on: network timeout, temporary unavailability
no_retry: authentication failure, permission denied
```

