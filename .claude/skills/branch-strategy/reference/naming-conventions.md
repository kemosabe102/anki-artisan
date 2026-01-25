# Branch Naming Conventions

Standard naming patterns for branch organization and clarity.

---

## Prefix Categories

| Prefix | Purpose | When to Use |
|--------|---------|-------------|
| `feature/*` | New functionality | Adding new capabilities, features, or modules |
| `fix/*` | Bug fixes | Correcting defects, errors, or unexpected behavior |
| `refactor/*` | Code restructuring | Improving code without changing behavior |
| `docs/*` | Documentation | README updates, API docs, guides |
| `test/*` | Test changes | Adding/fixing tests without prod code changes |
| `chore/*` | Maintenance | Dependency updates, config changes, tooling |
| `hotfix/*` | Urgent fixes | Production issues requiring immediate attention |
| `release/*` | Release prep | Version bumps, changelog, release notes |
| `experiment/*` | Exploratory work | Spikes, POCs, investigations |

---

## Naming Rules

### Format
```
<prefix>/<kebab-case-description>
```

### Rules

1. **Use kebab-case**: Words separated by hyphens
   - Good: `feature/user-authentication`
   - Bad: `feature/userAuthentication`, `feature/user_authentication`

2. **Be descriptive but concise**: 2-4 words typically
   - Good: `fix/login-timeout`
   - Bad: `fix/bug`, `fix/fix-the-issue-with-login-timing-out-after-30-seconds`

3. **Include ticket ID when applicable**: After prefix or at end
   - Format: `feature/ABC-123-user-auth` or `feature/user-auth-ABC-123`
   - Consistent within project

4. **Lowercase only**: No uppercase letters
   - Good: `feature/api-client`
   - Bad: `feature/API-Client`

5. **No special characters**: Only alphanumeric and hyphens
   - Good: `fix/null-pointer`
   - Bad: `fix/null_pointer`, `fix/null.pointer`

---

## Validation Regex

```regex
^(feature|fix|refactor|docs|test|chore|hotfix|release|experiment)/[a-z0-9]+(-[a-z0-9]+)*$
```

### Validation Logic

```python
import re

VALID_PREFIXES = [
    "feature", "fix", "refactor", "docs", 
    "test", "chore", "hotfix", "release", "experiment"
]

def validate_branch_name(name: str) -> dict:
    """Validate branch name against conventions."""
    pattern = r"^(" + "|".join(VALID_PREFIXES) + r")/[a-z0-9]+(-[a-z0-9]+)*$"
    
    if re.match(pattern, name):
        prefix = name.split("/")[0]
        return {
            "valid": True,
            "convention": f"{prefix}/*",
            "name": name
        }
    
    # Provide helpful error
    errors = []
    if "/" not in name:
        errors.append("Missing prefix (e.g., feature/, fix/)")
    else:
        prefix = name.split("/")[0]
        if prefix not in VALID_PREFIXES:
            errors.append(f"Invalid prefix '{prefix}'. Use: {', '.join(VALID_PREFIXES)}")
        
        suffix = name.split("/", 1)[1] if "/" in name else ""
        if not suffix:
            errors.append("Missing description after prefix")
        elif not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", suffix):
            errors.append("Description must be kebab-case (lowercase, hyphens)")
    
    return {
        "valid": False,
        "errors": errors,
        "suggestion": suggest_fix(name)
    }

def suggest_fix(name: str) -> str:
    """Suggest corrected branch name."""
    # Convert to kebab-case
    import re
    fixed = re.sub(r'[_\s]+', '-', name.lower())
    fixed = re.sub(r'[^a-z0-9/-]', '', fixed)
    
    # Add prefix if missing
    if "/" not in fixed:
        fixed = f"feature/{fixed}"
    
    return fixed
```

---

## Examples

### Good Branch Names

| Name | Why It's Good |
|------|---------------|
| `feature/user-authentication` | Clear prefix, descriptive, kebab-case |
| `fix/login-timeout-ABC-123` | Includes ticket ID |
| `refactor/api-client-v2` | Version indicator acceptable |
| `docs/readme-quickstart` | Specific documentation area |
| `hotfix/prod-null-pointer` | Urgency indicated by prefix |

### Bad Branch Names (With Fixes)

| Bad Name | Problem | Fixed Name |
|----------|---------|------------|
| `userAuth` | No prefix, camelCase | `feature/user-auth` |
| `feature/UserAuth` | Uppercase | `feature/user-auth` |
| `fix_login_bug` | Underscores | `fix/login-bug` |
| `my-branch` | No prefix | `feature/my-branch` |
| `feature/` | Empty description | `feature/description-here` |
| `FEATURE/CAPS` | Uppercase | `feature/caps` |

---

## Protected Branch Patterns

These branches have special meaning and restrictions:

| Pattern | Purpose | Restrictions |
|---------|---------|--------------|
| `main` | Primary branch | No direct commits, PR required |
| `master` | Legacy primary | No direct commits, PR required |
| `develop` | Integration branch | Feature branches merge here |
| `release/*` | Release candidates | Limited commits, version bumps only |
| `hotfix/*` | Production fixes | Merge to main AND develop |

---

## Quick Reference Card

```
PREFIX OPTIONS:
  feature/   fix/   refactor/   docs/   test/   chore/   hotfix/   release/

FORMAT:
  <prefix>/<kebab-case-description>

EXAMPLES:
  feature/user-login
  fix/null-pointer-exception
  refactor/database-connection
  docs/api-reference
```
