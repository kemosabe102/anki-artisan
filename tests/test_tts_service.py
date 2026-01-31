"""Tests for TTS service with mocked ElevenLabs API."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anki_artisan.models import LanguageConfig
from anki_artisan.tts_service import TTSService


class TestTTSService:
    """Tests for TTSService."""

    @patch("anki_artisan.tts_service.elevenlabs_save")
    @patch("anki_artisan.tts_service.ElevenLabs")
    def test_generate_audio_cache_miss(
        self,
        mock_elevenlabs_class: MagicMock,
        mock_save: MagicMock,
        sample_language_config: LanguageConfig,
        tmp_path: Path,
    ):
        """API called on cache miss, file saved, character count tracked."""
        # Setup mock client
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client
        mock_client.text_to_speech.convert.return_value = b"fake audio data"

        # Patch CACHE_DIR to use temp directory
        with patch("anki_artisan.tts_service.CACHE_DIR", tmp_path / "cache"):
            service = TTSService(api_key="test_key")

            result = service.generate_audio(
                text="Ciao mondo",
                language_config=sample_language_config,
            )

        # Verify API was called
        mock_client.text_to_speech.convert.assert_called_once()
        mock_save.assert_called_once()

        # Verify result
        assert result.text == "Ciao mondo"
        assert result.cached is False
        assert result.character_count == len("Ciao mondo")
        assert service.total_characters_used == len("Ciao mondo")

    @patch("anki_artisan.tts_service.elevenlabs_save")
    @patch("anki_artisan.tts_service.ElevenLabs")
    def test_generate_audio_cache_hit(
        self,
        mock_elevenlabs_class: MagicMock,
        mock_save: MagicMock,
        sample_language_config: LanguageConfig,
        tmp_path: Path,
    ):
        """Existing file returns cached=True, no API call."""
        # Setup mock client
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client

        cache_dir = tmp_path / "cache"

        with patch("anki_artisan.tts_service.CACHE_DIR", cache_dir):
            service = TTSService(api_key="test_key")

            # Pre-create cache file at expected location
            cache_path = service._get_cache_path(
                text="Ciao",
                language=sample_language_config.language_code,
                voice_id=sample_language_config.elevenlabs.voice_id,
                model_id=sample_language_config.elevenlabs.model_id,
            )
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(b"cached audio")

            result = service.generate_audio(
                text="Ciao",
                language_config=sample_language_config,
            )

        # Verify API was NOT called
        mock_client.text_to_speech.convert.assert_not_called()
        mock_save.assert_not_called()

        # Verify result
        assert result.cached is True
        assert result.file_path == cache_path
        assert service.total_characters_used == 0

    @patch("anki_artisan.tts_service.time.sleep")
    @patch("anki_artisan.tts_service.elevenlabs_save")
    @patch("anki_artisan.tts_service.ElevenLabs")
    def test_generate_audio_retry_on_error(
        self,
        mock_elevenlabs_class: MagicMock,
        mock_save: MagicMock,
        mock_sleep: MagicMock,
        sample_language_config: LanguageConfig,
        tmp_path: Path,
    ):
        """API fails twice, succeeds on 3rd attempt, no exception raised."""
        # Setup mock client that fails twice then succeeds
        mock_client = MagicMock()
        mock_elevenlabs_class.return_value = mock_client
        mock_client.text_to_speech.convert.side_effect = [
            Exception("Rate limit"),
            Exception("Timeout"),
            b"audio data",  # Third attempt succeeds
        ]

        with patch("anki_artisan.tts_service.CACHE_DIR", tmp_path / "cache"):
            service = TTSService(api_key="test_key")

            # Should not raise exception
            result = service.generate_audio(
                text="Test",
                language_config=sample_language_config,
            )

        # Verify retries happened
        assert mock_client.text_to_speech.convert.call_count == 3
        assert mock_sleep.call_count == 2  # Backoff delays
        assert result.cached is False

    @patch("anki_artisan.tts_service.ElevenLabs")
    def test_cache_key_differs_by_model(
        self,
        mock_elevenlabs_class: MagicMock,
        sample_language_config: LanguageConfig,
        tmp_path: Path,
    ):
        """Different model_id produces different cache path."""
        with patch("anki_artisan.tts_service.CACHE_DIR", tmp_path / "cache"):
            service = TTSService(api_key="test_key")

            path1 = service._get_cache_path(
                "ciao", "it", "voice1", "eleven_multilingual_v2"
            )
            path2 = service._get_cache_path(
                "ciao", "it", "voice1", "eleven_turbo_v2_5"
            )

            assert path1 != path2
