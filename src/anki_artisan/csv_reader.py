"""CSV vocabulary file reader and validator.

This module handles loading and validating vocabulary CSV files,
converting rows into validated VocabItem models.
"""

import csv
import logging
from pathlib import Path

from pydantic import ValidationError

from .config import LANGUAGES_DIR
from .models import Gender, PartOfSpeech, VocabItem

logger = logging.getLogger(__name__)


def load_vocabulary(language: str, level: str) -> list[VocabItem]:
    """Load vocabulary from a CSV file.

    Args:
        language: Language directory name (e.g., 'italian')
        level: CEFR level (e.g., 'a1', 'a2', 'b1')

    Returns:
        List of validated VocabItem instances

    Raises:
        FileNotFoundError: If vocabulary file doesn't exist
    """
    csv_path = LANGUAGES_DIR / language / f"{level}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {csv_path}")

    return _parse_csv_file(csv_path)


class CSVValidationError(Exception):
    """Raised when CSV validation fails."""

    def __init__(self, errors: list[str], csv_path: Path):
        self.errors = errors
        self.csv_path = csv_path
        error_list = "\n  ".join(errors)
        super().__init__(f"Validation failed for {csv_path.name}:\n  {error_list}")


def _parse_csv_file(csv_path: Path) -> list[VocabItem]:
    """Parse and validate a CSV vocabulary file.

    Args:
        csv_path: Path to the CSV file

    Returns:
        List of validated VocabItem instances

    Raises:
        CSVValidationError: If any rows fail validation
    """
    items: list[VocabItem] = []
    errors: list[str] = []

    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for line_num, row in enumerate(reader, start=2):  # Line 1 is header
            try:
                item = _parse_row(row, line_num)
                if item:
                    items.append(item)
            except ValidationError as e:
                errors.append(f"Line {line_num}: {e}")
            except ValueError as e:
                errors.append(f"Line {line_num}: {e}")

    if errors:
        raise CSVValidationError(errors, csv_path)

    logger.info(f"Loaded {len(items)} vocabulary items from {csv_path.name}")
    return items


def _parse_row(row: dict[str, str], line_num: int) -> VocabItem | None:
    """Parse a single CSV row into a VocabItem.

    Args:
        row: Dictionary from csv.DictReader
        line_num: Line number for error reporting

    Returns:
        VocabItem if valid, None if row should be skipped
    """
    # Skip empty rows
    if not row.get("word", "").strip():
        return None

    # Parse part of speech
    pos_str = row.get("part_of_speech", "").strip().lower()
    try:
        part_of_speech = PartOfSpeech(pos_str)
    except ValueError:
        raise ValueError(f"Invalid part_of_speech '{pos_str}'")

    # Parse gender with default
    gender_str = row.get("gender", "n/a").strip().lower()
    if not gender_str or gender_str == "":
        gender_str = "n/a"
    try:
        gender = Gender(gender_str)
    except ValueError:
        raise ValueError(f"Invalid gender '{gender_str}'")

    # Parse tags
    tags_str = row.get("tags", "").strip()
    tags = tags_str.split() if tags_str else []

    return VocabItem(
        word=row["word"].strip(),
        translation=row["translation"].strip(),
        phrase=row["phrase"].strip(),
        phrase_translation=row["phrase_translation"].strip(),
        part_of_speech=part_of_speech,
        gender=gender,
        tags=tags,
    )
