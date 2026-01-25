---
title: "Rollback Strategy Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Rollback Strategy Guide

**Purpose**: Standardize backup and rollback procedures for safe development
**Pain Points Addressed**: Preventing data loss, enabling quick recovery
**Time Savings**: Prevents hours of rework from lost changes

## Core Principle

**Always create backups before significant changes. Recovery is faster than recreation.**

## Backup Directory Structure

```
.backups/                    # Git-ignored backup directory
├── 2025-10-03/             # Date-organized
│   ├── CLAUDE.md.143022    # Timestamp format HHMMSS
│   ├── agent-backup/       # Directory backups
│   └── archive/            # Important long-term backups
└── README.md               # Backup inventory
```

## When to Create Backups

### Always Backup Before

- Modifying files >100 lines
- Renaming or moving files
- Updating agents or hooks
- Bulk changes (multiple files)
- System configuration changes
- Refactoring operations
- Destructive operations

### Backup Triggers by File Size

| File Size    | Action             | Backup Required |
| ------------ | ------------------ | --------------- |
| <50 lines    | Minor edit         | Optional        |
| 50-100 lines | Moderate change    | Recommended     |
| >100 lines   | Significant change | **Required**    |
| Any size     | Rename/move        | **Required**    |

## Backup Procedures

### Manual Backup Command

```bash
# Single file backup
cp original.md .backups/original.md.$(date +%Y%m%d_%H%M%S)

# Directory backup
cp -r original-dir/ .backups/original-dir.$(date +%Y%m%d_%H%M%S)/

# With description
cp file.md .backups/file.md.$(date +%Y%m%d_%H%M%S).before-refactor
```

### Automated Backup Script

```bash
#!/bin/bash
# save as scripts/backup.sh

backup_file() {
    local file=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir=".backups/$(date +%Y-%m-%d)"

    mkdir -p "$backup_dir"
    cp "$file" "$backup_dir/$(basename $file).$timestamp"
    echo "Backed up: $file → $backup_dir/$(basename $file).$timestamp"
}

# Usage
backup_file "CLAUDE.md"
```

### Python Backup Helper

```python
# save as scripts/backup_helper.py
import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path: str, description: str = "") -> Path:
    """Create timestamped backup of file."""
    file = Path(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_dir = Path(f".backups/{datetime.now().strftime('%Y-%m-%d')}")
    date_dir.mkdir(parents=True, exist_ok=True)

    suffix = f".{description}" if description else ""
    backup_path = date_dir / f"{file.name}.{timestamp}{suffix}"

    shutil.copy2(file, backup_path)
    print(f"✅ Backed up: {file} → {backup_path}")
    return backup_path

# Usage
backup_file("CLAUDE.md", "before-anthropic-update")
```

## Rollback Procedures

### Quick Rollback

```bash
# List available backups
ls -la .backups/

# Find specific file backups
find .backups -name "CLAUDE.md.*" -type f | sort

# Rollback to specific backup
cp .backups/2025-10-03/CLAUDE.md.143022 CLAUDE.md

# Verify rollback
diff .backups/2025-10-03/CLAUDE.md.143022 CLAUDE.md
```

### Selective Rollback

```bash
# Compare current with backup
diff CLAUDE.md .backups/2025-10-03/CLAUDE.md.143022

# Cherry-pick specific sections
# Use your editor to manually merge

# Or use git-style merge
diff3 -m \
    .backups/CLAUDE.md.original \
    CLAUDE.md \
    .backups/CLAUDE.md.backup \
    > CLAUDE.md.merged
```

### Emergency Recovery

```bash
# If everything is broken
cd .backups/
ls -la  # Find latest good state

# Restore entire directory
cp -r 2025-10-03/project-backup/* ../

# Or restore specific files
for file in *.backup; do
    cp "$file" "../${file%.backup}"
done
```

## Cleanup Schedule

### Retention Policy

| Backup Age | Action                 | Reason              |
| ---------- | ---------------------- | ------------------- |
| <7 days    | Keep all               | Recent work         |
| 7-30 days  | Keep daily snapshots   | Medium-term history |
| >30 days   | Archive important only | Space management    |
| >90 days   | Delete                 | Obsolete            |

### Cleanup Commands

```bash
# Remove backups older than 7 days
find .backups -type f -mtime +7 -delete

# Archive important backups
mkdir -p .backups/archive
mv .backups/*important* .backups/archive/

# Clean empty directories
find .backups -type d -empty -delete
```

### Automated Cleanup Script

```bash
#!/bin/bash
# save as scripts/cleanup-backups.sh

# Remove old backups (>7 days)
find .backups -type f -mtime +7 -not -path "*/archive/*" -delete

# Remove empty date directories
find .backups -type d -empty -delete

# Report
echo "Backup cleanup complete"
echo "Remaining backups:"
du -sh .backups/
```

## Integration with Workflow

### Pre-Change Checklist

- [ ] Identify files to modify
- [ ] Check file sizes
- [ ] Create backups if needed
- [ ] Document backup location
- [ ] Proceed with changes

### Post-Change Verification

- [ ] Changes working as expected?
- [ ] If yes, note success in log
- [ ] If no, rollback procedure ready
- [ ] Clean up old backups after confirmation

## Best Practices

### DO ✅

- Backup before destructive operations
- Use descriptive backup names
- Test rollback procedures regularly
- Document what each backup contains
- Clean up old backups weekly

### DON'T ❌

- Skip backups to save time
- Delete backups immediately
- Backup generated files
- Commit backups to git
- Keep backups forever

## Quick Reference Card

```bash
# Backup single file
cp file.md .backups/file.md.$(date +%Y%m%d_%H%M%S)

# Rollback file
cp .backups/file.md.timestamp file.md

# List backups
ls -la .backups/

# Find specific backup
find .backups -name "file.md.*"

# Clean old backups
find .backups -mtime +7 -delete
```

## Backup Log Template

Create `.backups/README.md`:

```markdown
# Backup Log

## 2025-10-03

- CLAUDE.md.143022 - Before Anthropic update
- agents/ - Before renaming refactor
- \*.py.150000 - Before Python upgrade

## Important Backups (Archive)

- 2025-09-01/system-working.tar.gz - Last known good state
```

## Git Integration

While backups are git-ignored, you can track backup metadata:

```bash
# Create backup
cp CLAUDE.md .backups/CLAUDE.md.$(date +%Y%m%d_%H%M%S)

# Note in commit
git commit -m "refactor: update CLAUDE.md structure

Backup created at .backups/CLAUDE.md.20251003_143022
Can rollback if issues found"
```

## Validation

### Test Your Rollback

```bash
# 1. Create test file
echo "test content" > test.txt

# 2. Backup
cp test.txt .backups/test.txt.backup

# 3. Modify
echo "modified" > test.txt

# 4. Rollback
cp .backups/test.txt.backup test.txt

# 5. Verify
cat test.txt  # Should show "test content"
```

---

**Remember**: Backups are insurance. Better to have and not need than need and not have!
