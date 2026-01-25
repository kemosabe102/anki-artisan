"""Tests for CLI integration."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anki_artisan.cli import main


class TestCLI:
    """Tests for CLI commands."""

    @patch("anki_artisan.cli.load_language_config")
    @patch("anki_artisan.cli.list_available_languages")
    @patch("anki_artisan.cli.load_vocabulary")
    def test_generate_dry_run(
        self,
        mock_load_vocab: MagicMock,
        mock_list_langs: MagicMock,
        mock_load_config: MagicMock,
        sample_language_config,
        sample_vocab_item,
        capsys,
    ):
        """Dry run validates without API calls, returns 0."""
        # Setup mocks
        mock_list_langs.return_value = ["italian"]
        mock_load_config.return_value = sample_language_config
        mock_load_vocab.return_value = [sample_vocab_item]

        # Run CLI with dry-run
        result = main(["generate", "--language", "italian", "--dry-run"])

        # Verify success
        assert result == 0

        # Verify output
        captured = capsys.readouterr()
        assert "[Dry run] Validation successful!" in captured.out
        assert "Italian" in captured.out
        assert "Items: 1" in captured.out

    @patch("anki_artisan.cli.list_available_languages")
    def test_generate_invalid_language(
        self,
        mock_list_langs: MagicMock,
        capsys,
    ):
        """Unknown language returns error code + message."""
        # Setup mock
        mock_list_langs.return_value = ["italian", "spanish"]

        # Run CLI with invalid language
        result = main(["generate", "--language", "klingon"])

        # Verify error
        assert result == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "klingon" in captured.out
        assert "italian" in captured.out  # Shows available languages
