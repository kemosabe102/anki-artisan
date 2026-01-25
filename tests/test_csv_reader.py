"""Tests for CSV vocabulary file reader."""

import tempfile
from pathlib import Path

import pytest

from anki_artisan.csv_reader import _parse_csv_file, _parse_row
from anki_artisan.models import Gender, PartOfSpeech


class TestLoadVocabulary:
    """Tests for vocabulary loading."""

    def test_load_vocabulary_from_fixture(self, test_vocab_csv: Path):
        """Load test CSV fixture, verify 3 items with correct types."""
        items = _parse_csv_file(test_vocab_csv)

        assert len(items) == 3

        # Verify first item
        item1 = items[0]
        assert item1.word == "test"
        assert item1.translation == "test"
        assert item1.phrase == "Test phrase here."
        assert item1.phrase_translation == "Test phrase translation."
        assert item1.part_of_speech == PartOfSpeech.NOUN
        assert item1.gender == Gender.MASCULINE
        assert item1.tags == ["test"]

        # Verify second item (interjection with n/a gender)
        item2 = items[1]
        assert item2.word == "hello"
        assert item2.part_of_speech == PartOfSpeech.INTERJECTION
        assert item2.gender == Gender.NOT_APPLICABLE

        # Verify third item
        item3 = items[2]
        assert item3.word == "book"
        assert item3.tags == ["objects"]

    def test_load_vocabulary_file_not_found(self):
        """Missing file raises FileNotFoundError."""
        nonexistent_path = Path("/nonexistent/path/vocab.csv")

        with pytest.raises(FileNotFoundError):
            _parse_csv_file(nonexistent_path)

    def test_parse_row_invalid_part_of_speech(self, caplog):
        """Invalid enum logs warning, returns None via ValueError."""
        row = {
            "word": "test",
            "translation": "test",
            "phrase": "Test phrase.",
            "phrase_translation": "Translation.",
            "part_of_speech": "invalid_pos",
            "gender": "m",
            "tags": "",
        }

        with pytest.raises(ValueError) as exc_info:
            _parse_row(row, line_num=2)

        assert "Invalid part_of_speech 'invalid_pos'" in str(exc_info.value)


class TestParseRow:
    """Tests for row parsing edge cases."""

    def test_parse_row_empty_word_returns_none(self):
        """Empty word field returns None (skip row)."""
        row = {
            "word": "",
            "translation": "test",
            "phrase": "Test phrase.",
            "phrase_translation": "Translation.",
            "part_of_speech": "noun",
            "gender": "m",
            "tags": "",
        }

        result = _parse_row(row, line_num=2)
        assert result is None

    def test_parse_row_default_gender(self):
        """Missing gender defaults to n/a."""
        row = {
            "word": "test",
            "translation": "test",
            "phrase": "Test phrase.",
            "phrase_translation": "Translation.",
            "part_of_speech": "noun",
            "gender": "",
            "tags": "",
        }

        result = _parse_row(row, line_num=2)
        assert result.gender == Gender.NOT_APPLICABLE
