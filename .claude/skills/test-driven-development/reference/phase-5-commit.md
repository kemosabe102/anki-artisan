# Phase 2E: COMMIT

**Goal:** Create atomic, meaningful commit for this chunk.

---

## Activities

### 1. Stage only files for this chunk

```bash
git add <files-for-this-chunk>
git status  # Verify only the right files are staged
```

### 2. Write clear commit message

```
Format: <type>: <short description>

Types:
- feat:     New feature chunk
- fix:      Bug fix for existing feature
- refactor: Restructuring without changing behavior
- test:     Test-only changes
- chore:    Dependencies, configuration, setup

Example:
feat: add password hashing to user authentication

Implements SHA256 hashing with UTF-8 encoding.
Validates against empty passwords.
Adds 3 tests covering valid input, empty input, and hash consistency.

Closes #123
```

### 3. Commit and push

```bash
git commit -m "feat: add password hashing to user authentication"
git push origin feature/your-feature-name
```

---

## Definition of Done (Return to Phase 2A for next chunk when)

- [ ] Commit made with clear, descriptive message
- [ ] Commit is atomic (one logical change only)
- [ ] ALL tests pass after commit
  ```bash
  npm test  # Final verification
  ```
- [ ] Changes pushed to remote (backup + CI/CD runs)
- [ ] Commit message follows conventional commit format
- [ ] If more chunks remain -> Return to Phase 2A (RED) for next chunk
- [ ] If all chunks complete -> Proceed to Phase 3 (Final Self-Review)

---

## Time Investment

3-5 minutes per commit

---

## Related Skills to Invoke

- **commit-message-standards** (conventional commits, team conventions)
