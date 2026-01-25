# Pydantic Validation Schemas

**Purpose**: JSON schema definitions for test dataset validation

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## Schema Definitions

### File Change Schema

```python
from pydantic import BaseModel, Field

class FileChange(BaseModel):
    """Represents a single file change in a commit scenario."""
    file_path: str = Field(..., description="Relative path to the changed file")
    change_type: str = Field(..., description="Conventional Commit type (feat, fix, refactor, etc.)")
    lines_added: int = Field(..., ge=0, description="Number of lines added")
    lines_deleted: int = Field(..., ge=0, description="Number of lines deleted")
```

### Commit Scenario Schema

```python
class CommitScenario(BaseModel):
    """Represents a single test scenario from git history."""
    scenario_id: str = Field(..., pattern=r"^SCENARIO-\d{3}$", description="Unique scenario identifier")
    commit_sha: str = Field(..., min_length=7, max_length=40, description="Git commit SHA")
    commit_message: str = Field(..., min_length=1, description="Full commit message")
    files: list[FileChange] = Field(..., min_length=1, description="List of file changes")
    edge_case_tags: list[str] = Field(default_factory=list, description="Edge case identifiers")

    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "SCENARIO-001",
                "commit_sha": "a1b2c3d4",
                "commit_message": "feat(auth): add OAuth2 login support",
                "files": [
                    {
                        "file_path": "packages/auth/oauth2.py",
                        "change_type": "feat",
                        "lines_added": 150,
                        "lines_deleted": 0
                    }
                ],
                "edge_case_tags": ["mixed_change_types"]
            }
        }
```

### Test Dataset Schema

```python
from datetime import datetime

class TestDataset(BaseModel):
    """Complete test dataset with metadata."""
    version: str = Field(default="1.0", description="Dataset schema version")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO 8601 timestamp")
    scenario_count: int = Field(..., ge=1, description="Total number of scenarios")
    scenarios: list[CommitScenario] = Field(..., min_length=1, description="List of test scenarios")

    def model_post_init(self, __context):
        """Validate scenario count matches list length."""
        if self.scenario_count != len(self.scenarios):
            raise ValueError(f"scenario_count ({self.scenario_count}) must match scenarios length ({len(self.scenarios)})")
```

### Expert Ground Truth Schema

```python
class ExpertGroundTruth(BaseModel):
    """Simulated expert decision for a scenario."""
    scenario_id: str = Field(..., pattern=r"^SCENARIO-\d{3}$", description="Matching scenario identifier")
    expert_decision: dict = Field(..., description="Algorithm-specific expert decision (e.g., file groupings)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in simulated expert decision")
    rationale: str = Field(..., min_length=10, description="Explanation of expert decision reasoning")

    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "SCENARIO-001",
                "expert_decision": {
                    "groups": [
                        {
                            "group_id": "AUTH-001",
                            "files": ["packages/auth/oauth2.py", "packages/auth/models.py"],
                            "rationale": "OAuth2 authentication implementation"
                        }
                    ]
                },
                "confidence": 0.92,
                "rationale": "High confidence - clear functional cohesion around OAuth2 feature"
            }
        }
```

### Ground Truth Dataset Schema

```python
class GroundTruthDataset(BaseModel):
    """Complete ground truth dataset with metadata."""
    version: str = Field(default="1.0", description="Dataset schema version")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO 8601 timestamp")
    ground_truth_count: int = Field(..., ge=1, description="Total number of ground truth entries")
    ground_truths: list[ExpertGroundTruth] = Field(..., min_length=1, description="List of expert decisions")

    def model_post_init(self, __context):
        """Validate ground truth count matches list length."""
        if self.ground_truth_count != len(self.ground_truths):
            raise ValueError(f"ground_truth_count ({self.ground_truth_count}) must match ground_truths length ({len(self.ground_truths)})")
```

## Usage Example

```python
from pathlib import Path
import json

# Create and validate scenario dataset
scenario_dataset = TestDataset(
    scenario_count=20,
    scenarios=[...]  # List of CommitScenario objects
)

# Write validated JSON
output_path = Path("tests/fixtures/scenarios.json")
output_path.write_text(scenario_dataset.model_dump_json(indent=2))

# Create and validate ground truth dataset
ground_truth_dataset = GroundTruthDataset(
    ground_truth_count=20,
    ground_truths=[...]  # List of ExpertGroundTruth objects
)

# Write validated JSON
gt_output_path = Path("tests/fixtures/ground_truth.json")
gt_output_path.write_text(ground_truth_dataset.model_dump_json(indent=2))

# Read-back verification
read_data = TestDataset.model_validate_json(output_path.read_text())
assert read_data.scenario_count == 20
```

## Validation Benefits

- **Type Safety**: Pydantic enforces field types at runtime
- **Constraint Validation**: Field validators ensure data quality (e.g., confidence ∈ [0, 1])
- **Schema Evolution**: Version field enables backward compatibility
- **Self-Documenting**: Field descriptions serve as inline documentation
- **JSON Serialization**: Built-in `model_dump_json()` for clean output

---

**Token Savings**: ~50 lines externalized from agent definition
