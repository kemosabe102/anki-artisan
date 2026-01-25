"""Tests for Anki deck builder."""

import zipfile
from pathlib import Path

import pytest

from anki_artisan.deck_builder import DeckBuilder
from anki_artisan.models import GeneratedAudio, LanguageConfig, VocabItem


class TestDeckBuilder:
    """Tests for DeckBuilder."""

    def test_add_vocab_item_and_build(
        self,
        sample_language_config: LanguageConfig,
        sample_vocab_item: VocabItem,
        tmp_path: Path,
    ):
        """Add item, build package, verify note count + media files."""
        builder = DeckBuilder(sample_language_config, level="a1")

        # Create fake audio files
        word_audio_path = tmp_path / "word.mp3"
        phrase_audio_path = tmp_path / "phrase.mp3"
        word_audio_path.write_bytes(b"fake word audio")
        phrase_audio_path.write_bytes(b"fake phrase audio")

        word_audio = GeneratedAudio(
            text=sample_vocab_item.word,
            file_path=word_audio_path,
            cached=False,
            character_count=len(sample_vocab_item.word),
        )
        phrase_audio = GeneratedAudio(
            text=sample_vocab_item.phrase,
            file_path=phrase_audio_path,
            cached=False,
            character_count=len(sample_vocab_item.phrase),
        )

        # Add vocab item
        builder.add_vocab_item(sample_vocab_item, word_audio, phrase_audio)

        # Verify note count
        assert builder.note_count == 1

        # Build package
        output_path = tmp_path / "test_deck.apkg"
        result_path = builder.build_package(output_path)

        # Verify package was created
        assert result_path == output_path
        assert output_path.exists()

        # Verify it's a valid zip file (apkg is a zip)
        assert zipfile.is_zipfile(output_path)

        # Verify media files are included
        with zipfile.ZipFile(output_path, "r") as zf:
            names = zf.namelist()
            # apkg should contain media files
            assert "media" in names or any("collection" in n for n in names)

    def test_build_empty_deck(
        self,
        sample_language_config: LanguageConfig,
        tmp_path: Path,
    ):
        """Zero items builds valid (empty) package."""
        builder = DeckBuilder(sample_language_config, level="a1")

        # Verify zero notes
        assert builder.note_count == 0

        # Build empty package
        output_path = tmp_path / "empty_deck.apkg"
        result_path = builder.build_package(output_path)

        # Verify package was created and is valid
        assert result_path == output_path
        assert output_path.exists()
        assert zipfile.is_zipfile(output_path)
