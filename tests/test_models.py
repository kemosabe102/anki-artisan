"""Tests for Pydantic data models."""

import pytest
from pydantic import ValidationError

from anki_artisan.models import Gender, PartOfSpeech, VocabItem


class TestVocabItem:
    """Tests for VocabItem model."""

    def test_vocab_item_valid(self):
        """Create VocabItem with all fields, verify types."""
        item = VocabItem(
            word="gatto",
            translation="cat",
            phrase="Il gatto nero.",
            phrase_translation="The black cat.",
            part_of_speech=PartOfSpeech.NOUN,
            gender=Gender.MASCULINE,
            tags=["animals", "basics"],
        )

        assert item.word == "gatto"
        assert item.translation == "cat"
        assert item.phrase == "Il gatto nero."
        assert item.phrase_translation == "The black cat."
        assert item.part_of_speech == PartOfSpeech.NOUN
        assert item.gender == Gender.MASCULINE
        assert item.tags == ["animals", "basics"]

    def test_vocab_item_phrase_too_long(self):
        """Phrase >6 words raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            VocabItem(
                word="test",
                translation="test",
                phrase="This phrase has way too many words here.",
                phrase_translation="Translation here.",
                part_of_speech=PartOfSpeech.NOUN,
                gender=Gender.NOT_APPLICABLE,
            )

        assert "Phrase must have ≤6 words" in str(exc_info.value)

    def test_vocab_item_tags_parsing(self):
        """Tags from string/list/None all work correctly."""
        # From string (space-separated)
        item1 = VocabItem(
            word="test",
            translation="test",
            phrase="Test phrase.",
            phrase_translation="Translation.",
            part_of_speech=PartOfSpeech.NOUN,
            tags="tag1 tag2 tag3",
        )
        assert item1.tags == ["tag1", "tag2", "tag3"]

        # From list
        item2 = VocabItem(
            word="test",
            translation="test",
            phrase="Test phrase.",
            phrase_translation="Translation.",
            part_of_speech=PartOfSpeech.NOUN,
            tags=["a", "b"],
        )
        assert item2.tags == ["a", "b"]

        # From None (default)
        item3 = VocabItem(
            word="test",
            translation="test",
            phrase="Test phrase.",
            phrase_translation="Translation.",
            part_of_speech=PartOfSpeech.NOUN,
            tags=None,
        )
        assert item3.tags == []

        # From empty string
        item4 = VocabItem(
            word="test",
            translation="test",
            phrase="Test phrase.",
            phrase_translation="Translation.",
            part_of_speech=PartOfSpeech.NOUN,
            tags="",
        )
        assert item4.tags == []


class TestGenderEnum:
    """Tests for Gender enum."""

    def test_gender_enum_values(self):
        """All gender values (m/f/n/mf/c/n/a) parse correctly."""
        assert Gender("m") == Gender.MASCULINE
        assert Gender("f") == Gender.FEMININE
        assert Gender("n") == Gender.NEUTER
        assert Gender("mf") == Gender.DUAL
        assert Gender("c") == Gender.COMMON
        assert Gender("n/a") == Gender.NOT_APPLICABLE

        # Verify all expected values exist
        expected_values = {"m", "f", "n", "mf", "c", "n/a"}
        actual_values = {g.value for g in Gender}
        assert actual_values == expected_values
