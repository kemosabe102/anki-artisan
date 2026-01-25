# Example: Complex Codebase Research

**Scenario**: "How does authentication work in this application?"

---

## Request Analysis

- **Type**: Open-ended investigation (concept, not specific symbol)
- **Scope**: Multi-file, cross-module understanding
- **Expected Tools**: Glob → Grep → Read (multiple rounds)

---

## Execution

### Phase 1: OBSERVE - Discover Authentication Surface

**Step 1.1: Find auth-related files**

```
Tool: Glob
Pattern: "**/*auth*.py"
```

**Result**:
```
packages/core/auth/
├── __init__.py
├── middleware.py
├── providers/
│   ├── jwt.py
│   ├── oauth.py
│   └── api_key.py
├── decorators.py
└── models.py
tests/unit/auth/
└── test_middleware.py
```

**Step 1.2: Find authentication entry points**

```
Tool: Grep
Pattern: "@authenticate|@require_auth|login|logout"
Type: py
Output Mode: files_with_matches
```

**Result**:
```
packages/core/auth/decorators.py
packages/core/api/routes/users.py
packages/core/api/routes/admin.py
```

### Phase 2: ORIENT - Understand Authentication Flow

**Step 2.1: Read core authentication logic**

```
Tool: Read
File: packages/core/auth/middleware.py
```

**Findings**:
- `AuthMiddleware` class intercepts all requests
- Checks `Authorization` header
- Delegates to appropriate provider (JWT, OAuth, API Key)

**Step 2.2: Read decorator implementation**

```
Tool: Read
File: packages/core/auth/decorators.py
```

**Findings**:
- `@require_auth` - Requires valid token
- `@require_role(role)` - Requires specific role
- `@optional_auth` - Extracts user if present, allows anonymous

**Step 2.3: Understand provider hierarchy**

```
Tool: Grep
Pattern: "class.*Provider"
Path: packages/core/auth/providers/
Output Mode: content
Context: 5
```

**Findings**:
```python
# jwt.py:12
class JWTProvider(AuthProvider):
    def validate(self, token: str) -> User: ...

# oauth.py:18
class OAuthProvider(AuthProvider):
    def validate(self, token: str) -> User: ...

# api_key.py:8
class APIKeyProvider(AuthProvider):
    def validate(self, key: str) -> User: ...
```

### Phase 3: Map Dependencies

**Step 3.1: Find what uses auth**

```
Tool: Grep
Pattern: "from.*auth import|from.*auth\."
Output Mode: content
```

**Result**: 12 files import from auth module

**Step 3.2: Trace configuration**

```
Tool: Grep
Pattern: "AUTH_|JWT_|OAUTH_"
Glob: "*.py"
```

**Result**: Configuration in `packages/core/config/settings.py`

---

## Findings Output

```markdown
## Authentication Architecture Analysis

### Overview
- **Pattern**: Middleware + Decorator + Provider Strategy
- **Entry Point**: `AuthMiddleware` (applied to all routes)
- **Configuration**: `packages/core/config/settings.py`

### Authentication Flow

1. Request → `AuthMiddleware.process_request()`
2. Extract token from `Authorization` header
3. Detect provider type (JWT/OAuth/API Key)
4. Delegate to appropriate `AuthProvider.validate()`
5. Attach `User` object to request context
6. Route decorator (`@require_auth`) checks user presence

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `AuthMiddleware` | `auth/middleware.py:15` | Request interception |
| `JWTProvider` | `auth/providers/jwt.py:12` | JWT token validation |
| `OAuthProvider` | `auth/providers/oauth.py:18` | OAuth token validation |
| `APIKeyProvider` | `auth/providers/api_key.py:8` | API key validation |
| `@require_auth` | `auth/decorators.py:24` | Route protection |

### Configuration Keys

- `JWT_SECRET` - JWT signing key
- `JWT_EXPIRY` - Token expiration (seconds)
- `OAUTH_PROVIDERS` - Enabled OAuth providers
- `API_KEY_HEADER` - Header name for API keys

### Consumers (12 modules)

- `api/routes/users.py` - User endpoints
- `api/routes/admin.py` - Admin endpoints
- `api/routes/data.py` - Data endpoints
- ... (9 more)

### Confidence Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Domain | 0.90 | Found all auth-related files |
| Pattern | 0.85 | Understood middleware + provider pattern |
| Dependency | 0.80 | Mapped 12 consumers, config keys |
| Risk | 0.75 | Identified token validation, needs security review |
| **CQ** | **0.85** | Ready for decision phase |
```

---

## Tool Calls Summary

| Tool | Calls | Purpose |
|------|-------|---------|
| Glob | 1 | Discover auth file structure |
| Grep | 4 | Entry points, providers, imports, config |
| Read | 2 | Middleware, decorators detail |
| **Total** | **7** | |

**Time**: ~20 seconds

---

## Escalation Check

- **Library research needed?** No - all patterns are internal
- **Web research needed?** No - standard authentication pattern
- **CQ ≥ 0.85?** Yes - proceed to decision phase
