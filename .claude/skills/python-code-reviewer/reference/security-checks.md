# Security Checks Reference

Detailed security review patterns for Python code. This reference covers OWASP Top 10 vulnerabilities and Python-specific security concerns.

## Table of Contents

1. [Input Validation (OWASP A03)](#input-validation-owasp-a03)
2. [Dangerous Functions](#dangerous-functions)
3. [Authentication and Secrets](#authentication-and-secrets)
4. [Error Handling Security](#error-handling-security)
5. [Code Examples](#code-examples)

---

## Input Validation (OWASP A03)

All external input must be validated through Pydantic or explicit checks.

### SQL Injection Prevention

**Check:** SQL queries use parameterized statements (no string formatting)

```python
# ❌ BAD - SQL injection vulnerable
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
query = "SELECT * FROM users WHERE name = '%s'" % name

# ✅ GOOD - Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### Path Traversal Prevention

**Check:** File paths validated against directory escape attacks

```python
# ❌ BAD - Path traversal vulnerable
file_path = os.path.join(upload_dir, user_filename)
# User could pass "../../../etc/passwd"

# ✅ GOOD - Validate path stays within allowed directory
from pathlib import Path

safe_path = Path(base_dir) / Path(user_filename).name
if not safe_path.resolve().is_relative_to(Path(base_dir).resolve()):
    raise ValueError("Invalid path")
```

### Command Injection Prevention

**Check:** Command execution uses safe patterns

```python
# ❌ BAD - Command injection vulnerable
subprocess.run(f"grep {pattern} {file}", shell=True)
os.system(f"rm {filename}")

# ✅ GOOD - List form without shell=True
subprocess.run(["grep", pattern, file], check=True)
subprocess.run(["rm", filename], check=True)
```

---

## Dangerous Functions

Functions that are inherently risky and require special scrutiny.

### eval() and exec()

**Rule:** Never use on untrusted input

```python
# ❌ BAD - Arbitrary code execution
result = eval(user_input)
exec(user_code)

# ✅ GOOD - Use safe alternatives
import ast
result = ast.literal_eval(user_input)  # Only for literals

# Or use structured parsing
import json
data = json.loads(user_input)
```

### Unsafe Deserialization

**Rule:** Never pickle/yaml.load untrusted data

```python
# ❌ BAD - Arbitrary code execution via pickle
data = pickle.loads(user_input)
data = yaml.load(user_input)  # Unsafe loader

# ✅ GOOD - Use safe alternatives
data = json.loads(user_input)
data = yaml.safe_load(user_input)
```

### Dynamic Import

**Rule:** Never import modules based on user input

```python
# ❌ BAD - Arbitrary module execution
module = __import__(user_module_name)

# ✅ GOOD - Whitelist allowed modules
ALLOWED_MODULES = {"json", "csv", "math"}
if user_module_name in ALLOWED_MODULES:
    module = __import__(user_module_name)
else:
    raise ValueError("Module not allowed")
```

---

## Authentication and Secrets

### Hardcoded Secrets

**Check:** No hardcoded passwords, API keys, or secrets in source code

```python
# ❌ BAD - Secrets in code
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password123@localhost/db"

# ✅ GOOD - Load from environment
import os
API_KEY = os.environ["API_KEY"]

# ✅ BETTER - Use pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    database_url: str
    
    class Config:
        env_file = ".env"
```

### Password Handling

**Check:** Passwords use strong hashing

```python
# ❌ BAD - Weak or no hashing
hashed = hashlib.md5(password.encode()).hexdigest()
stored_password = password  # Plain text!

# ✅ GOOD - Use bcrypt or similar
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

---

## Error Handling Security

### Information Leakage

**Check:** Error messages don't expose internal details

```python
# ❌ BAD - Exposes internal paths and structure
except Exception as e:
    return {"error": str(e), "traceback": traceback.format_exc()}

# ✅ GOOD - Generic error to user, detailed log internally
except Exception as e:
    logger.exception("Internal error processing request")
    return {"error": "An internal error occurred"}
```

### Logging Sensitive Data

**Check:** Logs don't contain secrets or PII

```python
# ❌ BAD - Logging sensitive data
logger.info(f"User login: {username}, password: {password}")
logger.debug(f"API response: {response.json()}")  # May contain tokens

# ✅ GOOD - Mask sensitive fields
logger.info(f"User login: {username}")
logger.debug(f"API response status: {response.status_code}")
```

---

## Code Examples

### Secure File Upload Handler

```python
from pathlib import Path
from pydantic import BaseModel, validator
import magic  # python-magic for file type detection

class FileUpload(BaseModel):
    filename: str
    content: bytes
    
    @validator("filename")
    def validate_filename(cls, v):
        # Only allow safe characters
        safe_name = Path(v).name
        if not safe_name or safe_name.startswith("."):
            raise ValueError("Invalid filename")
        return safe_name

def save_upload(upload: FileUpload, base_dir: Path) -> Path:
    # Validate file type by content, not extension
    mime_type = magic.from_buffer(upload.content, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type {mime_type} not allowed")
    
    # Safe path construction
    dest = base_dir / upload.filename
    if not dest.resolve().is_relative_to(base_dir.resolve()):
        raise ValueError("Invalid path")
    
    dest.write_bytes(upload.content)
    return dest
```

### Secure Database Query

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_user_orders(
    session: Session,
    user_id: int,
    status: str | None = None
) -> list[Order]:
    """Fetch orders with parameterized filtering."""
    query = select(Order).where(Order.user_id == user_id)
    
    if status:
        # Whitelist valid statuses
        if status not in ("pending", "completed", "cancelled"):
            raise ValueError("Invalid status")
        query = query.where(Order.status == status)
    
    return session.scalars(query).all()
```
