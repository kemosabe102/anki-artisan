# Actions Workflows Reference

**Purpose**: GitHub Actions workflow dispatch and trigger management

---

## Overview

This skill provides:
- Manual workflow dispatch via trigger_workflow operation
- Workflow listing and status checking
- Input parameter handling

---

## Listing Workflows

```bash
# List all workflows
AGENT_NAME=github gh workflow list

# List enabled workflows
AGENT_NAME=github gh workflow list --all

# Show workflow details
AGENT_NAME=github gh workflow view ci.yml
```

---

## Triggering Workflows

### Basic Dispatch
```bash
# Trigger workflow on default branch
AGENT_NAME=github gh workflow run ci.yml

# Trigger on specific branch
AGENT_NAME=github gh workflow run ci.yml --ref feature/my-feature

# Trigger on tag
AGENT_NAME=github gh workflow run release.yml --ref v1.3.0
```

### With Inputs

Workflows can accept inputs via `workflow_dispatch`:

```yaml
# .github/workflows/deploy.yml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Deployment environment"
        required: true
        type: choice
        options:
          - staging
          - production
      debug:
        description: "Enable debug logging"
        required: false
        type: boolean
        default: false
```

Trigger with inputs:
```bash
AGENT_NAME=github gh workflow run deploy.yml \
  --ref main \
  -f environment=staging \
  -f debug=true
```

---

## Workflow Run Monitoring

### List Recent Runs
```bash
# All runs
AGENT_NAME=github gh run list

# Runs for specific workflow
AGENT_NAME=github gh run list --workflow ci.yml

# Runs on specific branch
AGENT_NAME=github gh run list --branch main

# Failed runs only
AGENT_NAME=github gh run list --status failure

# Limit results
AGENT_NAME=github gh run list --limit 5
```

### View Run Details
```bash
# View run summary
AGENT_NAME=github gh run view 12345678901

# View with job details
AGENT_NAME=github gh run view 12345678901 --verbose

# View logs
AGENT_NAME=github gh run view 12345678901 --log

# View failed logs only
AGENT_NAME=github gh run view 12345678901 --log-failed
```

### Watch Run Progress
```bash
# Watch until completion
AGENT_NAME=github gh run watch 12345678901

# Watch with exit code
AGENT_NAME=github gh run watch 12345678901 --exit-status
```

---

## Rerunning Workflows

```bash
# Rerun entire workflow
AGENT_NAME=github gh run rerun 12345678901

# Rerun failed jobs only
AGENT_NAME=github gh run rerun 12345678901 --failed

# Rerun with debug logging
AGENT_NAME=github gh run rerun 12345678901 --debug
```

---

## Canceling Workflows

```bash
# Cancel a running workflow
AGENT_NAME=github gh run cancel 12345678901
```

---

## Common Workflow Patterns

### CI Workflow (ci.yml)
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run pytest
```

### Deploy Workflow (deploy.yml)
```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh ${{ inputs.environment }}
```

### Scheduled Workflow
```yaml
name: Nightly Build

on:
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight UTC
  workflow_dispatch:       # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh
```

---

## Workflow Dispatch Requirements

To trigger a workflow manually, it must have:

```yaml
on:
  workflow_dispatch:
```

Workflows without this trigger cannot be dispatched via gh CLI.

---

## Getting Run ID After Dispatch

After triggering, get the run ID:

```bash
# Dispatch workflow
AGENT_NAME=github gh workflow run ci.yml --ref main

# Wait briefly, then get most recent run
AGENT_NAME=github gh run list --workflow ci.yml --limit 1 --json databaseId --jq ".[0].databaseId"
```

---

## Error Scenarios

| Error | Cause | Recovery |
|-------|-------|----------|
| "Workflow not found" | Wrong file name | Check workflow file exists |
| "Workflow disabled" | Workflow is disabled | Enable via gh workflow enable |
| "No workflow_dispatch trigger" | Missing trigger | Add workflow_dispatch to workflow |
| "Invalid input" | Wrong input value | Check input type and options |
| "Ref not found" | Branch/tag missing | Verify ref exists |
