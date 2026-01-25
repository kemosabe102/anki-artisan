# Usage Examples

Real-world examples of branch-strategy skill operations.

---

## Example 1: Starting a New Feature

**User Request**: "Create a branch for the login feature"

### Skill Processing

1. **Parse Request**: Create branch, feature type, description "login"
2. **Generate Name**: `feature/login` (apply naming conventions)
3. **Validate**: Matches `feature/*` pattern -> PASS
4. **Delegate**: Task(source-control) with create_branch

### Conversation Flow

```
User: Create a branch for the login feature

Claude: I'll create a feature branch for the login feature.

[Validates name: feature/login -> PASS]
[Task(source-control): create_branch("feature/login", base="main")]

Created branch `feature/login` from `main`.

Current status:
- Branch: feature/login
- Base: main
- Tracking: Not set (use `git push -u origin feature/login` to set)
```

---

## Example 2: Checking Remote Status

**User Request**: "Am I up to date with the remote?"

### Skill Processing

1. **Parse Request**: Status check, remote sync
2. **Operations**: fetch_remote -> get_remote_status
3. **Interpret**: Provide actionable recommendation

### Conversation Flow

```
User: Am I up to date with the remote?

Claude: Let me check your sync status with the remote.

[Task(source-control): fetch_remote(origin, prune=true)]
[Task(source-control): get_remote_status()]

Branch sync status for `feature/user-auth`:

| Metric | Value |
|--------|-------|
| Tracking | origin/feature/user-auth |
| Ahead | 2 commits |
| Behind | 0 commits |
| Status | Ready to push |

Recommendation: Your local branch has 2 commits not on the remote. 
Run `git push` to sync.
```

---

## Example 3: Safe Branch Switch with Dirty Working Directory

**User Request**: "Switch to main"

### Skill Processing

1. **Parse Request**: Switch branch, target "main"
2. **Pre-check**: Detect dirty working directory
3. **Auto-stash**: Preserve work before switch
4. **Switch**: Change to target branch
5. **Report**: Include stash info

### Conversation Flow

```
User: Switch to main

Claude: Switching to main branch.

[Detected uncommitted changes]
[Task(source-control): switch_branch("main", stash_if_dirty=true)]

Switched to `main` branch.

Note: Your uncommitted changes were stashed automatically.
- Stash ref: stash@{0}
- Message: "WIP on feature/user-auth: abc1234 last commit message"

To restore your changes later:
  git stash pop
```

---

## Example 4: Branch Deletion with Safety Check

**User Request**: "Delete the feature/old-auth branch"

### Skill Processing

1. **Parse Request**: Delete branch, target "feature/old-auth"
2. **Safety Checks**: 
   - Not current branch? YES
   - Fully merged? NO -> Requires confirmation
3. **Prompt User**: Warn about unmerged commits
4. **Execute**: Only after confirmation

### Conversation Flow

```
User: Delete the feature/old-auth branch

Claude: Checking branch status before deletion...

[Task(source-control): delete_branch("feature/old-auth", force=false)]
[Result: FAILURE - branch not fully merged]

Warning: Branch `feature/old-auth` has 3 unmerged commits.

These commits will be lost if you delete this branch:
- abc1234: feat(auth): add OAuth support
- def5678: feat(auth): add token refresh
- ghi9012: test(auth): add OAuth tests

Options:
1. Force delete anyway: I'll delete with `git branch -D`
2. Keep branch: Cancel deletion
3. Merge first: Merge to main before deleting

What would you like to do?

User: Force delete it

Claude: Deleting branch with force...

[Task(source-control): delete_branch("feature/old-auth", force=true)]

Deleted branch `feature/old-auth`.

Note: The 3 unmerged commits are still accessible via reflog for ~30 days.
Recovery command (if needed): `git checkout -b feature/old-auth abc1234`
```

---

## Example 5: List All Branches

**User Request**: "Show me all branches"

### Conversation Flow

```
User: Show me all branches

Claude: Fetching branch information...

[Task(source-control): fetch_remote(prune=true)]
[Task(source-control): list_branches(include_remote=true)]

Branches:

**Local Branches:**
| Branch | Tracking | Status |
|--------|----------|--------|
| * main | origin/main | Up to date |
| feature/user-auth | origin/feature/user-auth | Ahead 2 |
| fix/login-bug | (none) | No tracking |

**Remote Branches (origin):**
- origin/main
- origin/develop
- origin/feature/user-auth
- origin/feature/api-v2

Current branch: main
```

---

## Example 6: Invalid Branch Name

**User Request**: "Create branch UserAuth"

### Skill Processing

1. **Parse Request**: Create branch, name "UserAuth"
2. **Validate**: Does NOT match conventions -> FAIL
3. **Suggest Fix**: Provide corrected name

### Conversation Flow

```
User: Create branch UserAuth

Claude: I'll validate the branch name first.

[Validation: "UserAuth" against naming conventions]
[Result: FAIL]

Invalid branch name: `UserAuth`

Issues:
- Missing prefix (feature/, fix/, etc.)
- Contains uppercase letters (should be lowercase)

Suggested corrections:
- `feature/user-auth` (if this is a new feature)
- `fix/user-auth` (if this is a bug fix)

Would you like me to create `feature/user-auth`?
```

---

## Example 7: Pre-PR Branch Sync

**User Request**: "Sync my branch before creating a PR"

### Skill Processing

1. **Fetch**: Get latest from remote
2. **Check Status**: Ahead/behind main
3. **Rebase**: If behind main
4. **Push**: Update remote branch

### Conversation Flow

```
User: Sync my branch before creating a PR

Claude: I'll sync your branch with main to prepare for a PR.

[Task(source-control): fetch_remote(origin)]
[Task(source-control): get_remote_status()]

Current status:
- Branch: feature/user-auth
- Behind main: 5 commits
- Ahead of main: 3 commits

Rebasing onto latest main...

[Task(source-control): rebase onto origin/main]

Rebase successful. Pushing updated branch...

[Task(source-control): push --force-with-lease]

Branch `feature/user-auth` is now in sync with main and ready for PR.

Summary:
- Integrated 5 new commits from main
- Your 3 commits rebased on top
- Remote branch updated
```


---

## Quick Reference: User Requests to Operations

| User Says | Skill Operation(s) |
|-----------|-------------------|
| "create branch for X" | validate name -> create_branch |
| "switch to X" | switch_branch (with auto-stash) |
| "delete branch X" | delete_branch (with safety check) |
| "show branches" | fetch_remote -> list_branches |
| "am I up to date?" | fetch_remote -> get_remote_status |
| "sync my branch" | fetch -> get_status -> rebase -> push |
| "what branches exist?" | list_branches |
| "clean up old branches" | list_branches -> delete_branch (multiple) |
