"""Shared pytest fixtures for Anki Artisan tests."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from anki_artisan.models import (
    DeckConfig,
    ElevenLabsConfig,
    Gender,
    LanguageConfig,
    LanguageFeatures,
    PartOfSpeech,
    VocabItem,
    VoiceSettings,
)


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def test_vocab_csv(fixtures_dir: Path) -> Path:
    """Path to test vocabulary CSV file."""
    return fixtures_dir / "test_vocab.csv"


@pytest.fixture
def sample_vocab_item() -> VocabItem:
    """Sample VocabItem for unit tests."""
    return VocabItem(
        word="casa",
        translation="house",
        phrase="La casa rossa.",
        phrase_translation="The red house.",
        part_of_speech=PartOfSpeech.NOUN,
        gender=Gender.FEMININE,
        tags=["basics", "home"],
    )


@pytest.fixture
def sample_language_config() -> LanguageConfig:
    """Sample LanguageConfig for unit tests."""
    return LanguageConfig(
        language_code="it",
        language_name="Italian",
        native_name="Italiano",
        elevenlabs=ElevenLabsConfig(
            voice_id="test_voice_id",
            voice_name="Test Voice",
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(),
        ),
        deck=DeckConfig(
            name_template="Italian {level}",
            deck_id_base=1000000000,
            model_id_base=2000000000,
        ),
        features=LanguageFeatures(
            has_gender=True,
            has_articles=True,
            gender_types=["m", "f"],
        ),
    )


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Temporary directory for cache/output (auto-cleanup)."""
    return tmp_path


@pytest.fixture
def mock_tts_service(tmp_path: Path, sample_language_config: LanguageConfig):
    """Mock TTS service that creates fake audio files without API calls."""
    from anki_artisan.models import GeneratedAudio
    from anki_artisan.tts_service import TTSService

    mock_service = MagicMock(spec=TTSService)
    mock_service._total_characters = 0
    mock_service.total_characters_used = 0

    def generate_audio(text, language_config, voice_id=None):
        # Create a fake audio file
        cache_dir = tmp_path / "cache"
        cache_dir.mkdir(exist_ok=True)
        audio_path = cache_dir / f"{hash(text)}.mp3"
        audio_path.write_bytes(b"fake mp3 data")

        mock_service._total_characters += len(text)
        mock_service.total_characters_used = mock_service._total_characters

        return GeneratedAudio(
            text=text,
            file_path=audio_path,
            cached=False,
            character_count=len(text),
        )

    mock_service.generate_audio.side_effect = generate_audio
    return mock_service
