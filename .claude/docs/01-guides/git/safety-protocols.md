# Git Safety Protocols

**Purpose**: Critical git commands that destroy uncommitted work + safe alternatives

**Audience**: Orchestrator, all agents with git operations

**Protection**: Security hooks BLOCK these commands automatically

---

## 🚫 BANNED OPERATIONS

**NEVER run these commands - they destroy uncommitted work:**

### Category 1: File-Level Destruction

```bash
# ❌ BANNED - Discards all changes in specific file
git checkout <file>     # Reverts file to HEAD state, loses uncommitted edits
git restore <file>      # Same as checkout, discards working directory changes
```

**Why Banned**: Permanent loss of uncommitted changes in targeted file. No recovery possible.

**Affected Workflow**: User spent 2 hours editing file → git checkout file.py → ALL WORK GONE

---

### Category 2: Repository-Wide Destruction

```bash
# ❌ BANNED - Wipes out ALL uncommitted work
git reset --hard        # Reverts entire working directory to HEAD, loses ALL changes
git clean -fd          # Deletes ALL untracked files permanently
```

**Why Banned**:
- **git reset --hard**: Nuclear option - destroys every uncommitted change across entire repository
- **git clean -fd**: Deletes untracked files (new files user created but hasn't staged yet)

**Affected Workflow**: User working on 5 files → git reset --hard → ALL 5 FILES REVERTED → Hours of work lost

---

### Category 3: Any Data-Discarding Command

```bash
# ❌ BANNED - Catch-all for destructive operations
git checkout -f         # Force checkout (ignores uncommitted changes)
git reset --hard HEAD~1 # Hard reset to previous commit
git clean -fdx          # Clean including ignored files
```

**Common Thread**: Any command that discards user work without explicit permission

---

## ✅ SAFE ALTERNATIVES

**These commands are SAFE - they only affect staging area, not working directory:**

```bash
# ✅ SAFE - Unstages files (preserves working directory changes)
git reset HEAD          # Unstages all files (used in /git commit workflow)
git reset HEAD <file>   # Unstages specific file without discarding changes
git reset --soft HEAD~1 # Moves HEAD to previous commit, keeps staging area + working directory

# Key Distinction:
# - git reset HEAD (no flags) = SAFE - only manipulates staging area
# - git reset --hard = BANNED - destroys uncommitted work
```

### Safe Workflow Examples

**Unstage Everything** (no data loss):
```bash
git reset HEAD          # All files remain in working directory with changes intact
```

**Undo Last Commit** (keep changes):
```bash
git reset --soft HEAD~1 # Commit undone, changes remain staged
```

**Discard Changes** (ONLY after user confirmation):
```bash
# User: "Are you sure you want to discard changes to auth.py?"
# User: "Yes, discard auth.py"
git restore auth.py     # NOW safe to run (explicit permission given)
```

---

## User Permission Protocol

**If user explicitly requests discarding work:**

1. **Show impact** (run git status first):
   ```bash
   git status
   # Output: Modified: auth.py (150 lines changed), config.yaml (5 lines changed)
   ```

2. **Explicit confirmation request**:
   ```
   "Are you sure you want to discard changes to:
   - auth.py (150 lines of uncommitted work)
   - config.yaml (5 lines of uncommitted work)

   This action is IRREVERSIBLE. Type 'Yes, discard [filename]' to confirm."
   ```

3. **Wait for exact confirmation**:
   - ✅ Accept: "Yes, discard auth.py" or "Yes, discard all changes"
   - ❌ Reject: "yes", "ok", "sure" (not explicit enough)

4. **Execute ONLY after explicit confirmation**:
   ```bash
   git restore auth.py config.yaml
   ```

---

## Why These Protections Exist

### Permanent Data Loss
- Git **only tracks committed changes**
- Uncommitted work exists **only in working directory** (not in git history)
- Once discarded → **No recovery mechanism** (no git reflog, no backup)

### User Trust Violation
- Users expect AI assistance to be **non-destructive by default**
- Losing hours of work damages trust irreparably
- Permission-based approach maintains user agency

### No Undo
Unlike most file operations (which can be undone with Ctrl+Z or file recovery):
- git reset --hard → No undo
- git clean -fd → No undo
- git checkout <file> → No undo

---

## Security Hook Implementation

**Protection Layer**: `.claude/hooks/validate-deps.py` (runs on tool calls)

**Detection Pattern**:
```python
BANNED_PATTERNS = [
    r'git\s+checkout\s+\S+',      # git checkout <file>
    r'git\s+restore\s+\S+',       # git restore <file>
    r'git\s+reset\s+--hard',      # git reset --hard
    r'git\s+clean\s+-[fFdDxX]+',  # git clean -fd/-fdx
]
```

**Hook Behavior**:
- Detects banned pattern in Bash tool call
- **BLOCKS execution** (returns error before running)
- Provides safe alternative suggestion
- Logs security event

**Override**: User can explicitly request (after confirmation protocol above)

---

## Common Scenarios & Safe Alternatives

### Scenario 1: "I want to undo my changes to this file"

**❌ WRONG**: `git checkout file.py` (data loss)
**✅ CORRECT**:
1. Show user what will be lost: `git diff file.py`
2. Get explicit confirmation
3. If confirmed: `git restore file.py`

---

### Scenario 2: "I want to unstage everything"

**❌ WRONG**: `git reset --hard` (data loss)
**✅ CORRECT**: `git reset HEAD` (unstages, preserves changes)

---

### Scenario 3: "I want to clean up untracked files"

**❌ WRONG**: `git clean -fd` (permanent deletion)
**✅ CORRECT**:
1. Preview: `git clean -fd --dry-run` (show what would be deleted)
2. Get explicit confirmation per file
3. If confirmed: `rm <specific-file>` (more controlled than git clean)

---

### Scenario 4: "Start fresh from last commit"

**❌ WRONG**: `git reset --hard HEAD` (data loss)
**✅ CORRECT**:
1. Verify: `git status` (show user what will be lost)
2. Offer alternatives:
   - Stage everything: `git add .` (preserve work)
   - Create backup commit: `git commit -m "WIP backup"` (preserve in history)
   - If user REALLY wants to discard → Follow permission protocol

---

## Integration with Git Workflow Commands

**Safe Commands** (used in /git prepare, /git commit):
```bash
git status              # ✅ Read-only
git diff                # ✅ Read-only
git add <files>         # ✅ Stages changes (reversible with git reset HEAD)
git commit              # ✅ Creates commit (reversible with git reset --soft)
git reset HEAD          # ✅ Unstages (preserves working directory)
git push                # ✅ Pushes commits (user permission required for force push)
```

**Integration Point**: /git prepare validates changes → /git commit stages + commits → All operations reversible until push

---

## Emergency Recovery (If Banned Command Runs)

**If git reset --hard accidentally executed**:

1. **Check reflog** (might recover commits):
   ```bash
   git reflog
   git reset --hard HEAD@{1}  # Restore to previous state (if committed)
   ```

2. **Check IDE backups**:
   - VS Code: `.vscode/.history/`
   - IntelliJ: Local History feature
   - Sublime: Session restore

3. **File system recovery** (last resort):
   - Windows: Shadow Copy / File History
   - Mac: Time Machine
   - Linux: ext4 undelete tools (low success rate)

**Reality**: Recovery success rate <20% for uncommitted work. **Prevention is critical.**

---

## References

- **Git Documentation**: https://git-scm.com/docs/git-reset
- **Workflow Integration**: `.claude/commands/git.md` (safe command patterns)
- **Hook Implementation**: `.claude/hooks/validate-deps.py` (security layer)

---

**Last Updated**: 2025-11-21
**Used By**: Orchestrator, source-control agent, all agents with git operations
**Auto-loaded**: Via startup-eval.py hook
**Protection Level**: CRITICAL (data loss prevention)
