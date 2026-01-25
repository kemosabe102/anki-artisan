"""Anki Artisan - Generate Anki flashcard decks with neural TTS audio.

This package provides tools for creating vocabulary flashcard decks
with ElevenLabs text-to-speech audio for language learning.
"""

from .cli import main
from .config import (
    BASE_DIR,
    CACHE_DIR,
    LANGUAGES_DIR,
    OUTPUT_DIR,
    Settings,
    ensure_directories,
    get_settings,
    list_available_languages,
    load_language_config,
)
from .csv_reader import load_vocabulary
from .deck_builder import DeckBuilder
from .models import (
    DeckConfig,
    ElevenLabsConfig,
    Gender,
    GeneratedAudio,
    LanguageConfig,
    LanguageFeatures,
    PartOfSpeech,
    VocabItem,
    VoiceSettings,
)
from .tts_service import TTSService

__version__ = "0.1.0"

__all__ = [
    # CLI
    "main",
    # Config
    "BASE_DIR",
    "CACHE_DIR",
    "LANGUAGES_DIR",
    "OUTPUT_DIR",
    "Settings",
    "ensure_directories",
    "get_settings",
    "list_available_languages",
    "load_language_config",
    # CSV
    "load_vocabulary",
    # Deck Builder
    "DeckBuilder",
    # Models
    "DeckConfig",
    "ElevenLabsConfig",
    "Gender",
    "GeneratedAudio",
    "LanguageConfig",
    "LanguageFeatures",
    "PartOfSpeech",
    "VocabItem",
    "VoiceSettings",
    # TTS
    "TTSService",
]
