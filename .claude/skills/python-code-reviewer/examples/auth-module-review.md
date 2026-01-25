# Example Review: Authentication Module

This example demonstrates a complete code review following the code-quality skill format.

---

## Review Report: auth.py

**Status:** ⚠️ WARNING

**Scope:** `packages/core/auth.py`

---

### Summary

This module implements JWT-based authentication with user validation. The core logic is sound, but there are security concerns around token handling and missing type hints that should be addressed before merging.

---

### Critical Issues ❌

1. **Hardcoded JWT Secret**
   - **File:** `packages/core/auth.py` (line 15)
   - **Category:** Security
   - **Problem:** JWT secret is hardcoded in source code
   
   **Current code:**
   ```python
   JWT_SECRET = "super-secret-key-12345"
   ```
   
   **Required fix:**
   ```python
   import os
   JWT_SECRET = os.environ["JWT_SECRET"]
   ```
   
   **Explanation:** Hardcoded secrets in source code can be exposed through version control. Secrets must be loaded from environment variables or a secrets manager.

2. **SQL Injection in User Lookup**
   - **File:** `packages/core/auth.py` (line 42)
   - **Category:** Security
   - **Problem:** String formatting used in SQL query
   
   **Current code:**
   ```python
   def get_user(username: str) -> User | None:
       query = f"SELECT * FROM users WHERE username = '{username}'"
       return db.execute(query).first()
   ```
   
   **Required fix:**
   ```python
   def get_user(username: str) -> User | None:
       query = "SELECT * FROM users WHERE username = :username"
       return db.execute(query, {"username": username}).first()
   ```
   
   **Explanation:** String formatting in SQL queries allows SQL injection attacks. An attacker could pass `' OR '1'='1` as username to bypass authentication.

---

### Warnings ⚠️

1. **Missing Type Hints**
   - **File:** `packages/core/auth.py` (lines 25-30)
   - **Category:** Type Safety
   - **Problem:** `validate_user` function lacks type annotations
   
   **Current code:**
   ```python
   def validate_user(username, password):
       user = get_user(username)
       return verify_password(password, user.hashed_password)
   ```
   
   **Suggested fix:**
   ```python
   def validate_user(username: str, password: str) -> bool:
       user = get_user(username)
       if user is None:
           return False
       return verify_password(password, user.hashed_password)
   ```
   
   **Explanation:** Type hints improve code documentation and enable static analysis with mypy. Also added null check for user.

2. **Broad Exception Handling**
   - **File:** `packages/core/auth.py` (lines 45-48)
   - **Category:** Error Handling
   - **Problem:** Catching generic Exception masks specific errors
   
   **Current code:**
   ```python
   try:
       token_data = decode_token(token)
   except Exception:
       return None
   ```
   
   **Suggested fix:**
   ```python
   try:
       token_data = decode_token(token)
   except jwt.ExpiredSignatureError:
       logger.info("Token expired")
       return None
   except jwt.InvalidTokenError as e:
       logger.warning(f"Invalid token: {e}")
       return None
   ```
   
   **Explanation:** Specific exception handling enables better logging and debugging. Different error types may require different responses.

3. **Mutable Default Argument**
   - **File:** `packages/core/auth.py` (line 60)
   - **Category:** Bug Risk
   - **Problem:** Default list argument will persist across calls
   
   **Current code:**
   ```python
   def create_token(user_id: int, scopes: list[str] = []) -> str:
       payload = {"sub": user_id, "scopes": scopes}
       return jwt.encode(payload, JWT_SECRET)
   ```
   
   **Suggested fix:**
   ```python
   def create_token(user_id: int, scopes: list[str] | None = None) -> str:
       if scopes is None:
           scopes = []
       payload = {"sub": user_id, "scopes": scopes}
       return jwt.encode(payload, JWT_SECRET)
   ```
   
   **Explanation:** Mutable default arguments retain modifications across calls, leading to unexpected behavior.

---

### Suggestions 💡

1. **Use Pydantic for Token Data**
   - **File:** `packages/core/auth.py` (line 35)
   - **Current approach:** Token payload handled as plain dict
   
   **Suggested improvement:**
   ```python
   from pydantic import BaseModel
   from datetime import datetime
   
   class TokenPayload(BaseModel):
       sub: int
       exp: datetime
       scopes: list[str] = []
   ```
   
   **Rationale:** Pydantic models provide automatic validation and clear documentation of the expected token structure.

2. **Add Password Strength Validation**
   - **File:** `packages/core/auth.py` (line 70)
   - **Current approach:** No validation on password strength during registration
   
   **Suggested improvement:**
   ```python
   import re
   
   def validate_password_strength(password: str) -> bool:
       """Require 8+ chars, uppercase, lowercase, digit."""
       if len(password) < 8:
           return False
       if not re.search(r"[A-Z]", password):
           return False
       if not re.search(r"[a-z]", password):
           return False
       if not re.search(r"\d", password):
           return False
       return True
   ```
   
   **Rationale:** Enforcing password complexity helps protect user accounts.

---

### Overall Assessment

The authentication module implements standard JWT patterns correctly, but has two critical security issues (hardcoded secret and SQL injection) that must be fixed immediately. The warning-level issues around type safety, exception handling, and mutable defaults should be addressed to meet project standards.

**Key Strengths:**
- Clean separation of concerns between token and user validation
- Uses secure password hashing library (bcrypt)
- Token expiration properly implemented

**Key Weaknesses:**
- Hardcoded secret (critical security issue)
- SQL injection vulnerability (critical security issue)
- Missing type hints throughout
- Generic exception handling obscures errors

**Recommendation:** ❌ REQUEST CHANGES

---

## Review Checklist Used

- [x] Step 1: Identify Review Scope
- [x] Step 2: Review Code Structure and Design
- [x] Step 3: Review Type Safety
- [x] Step 4: Review Security - **Found 2 critical issues**
- [x] Step 5: Review Exception Handling - **Found 1 warning**
- [x] Step 6: Review Performance
- [x] Step 7: Review Testability
- [x] Step 8: Review Python Version Compatibility
- [x] Step 9: Review Common Pitfalls - **Found mutable default**
