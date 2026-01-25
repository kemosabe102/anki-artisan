"""Configuration management for Anki Artisan.

This module handles environment variables, path constants, and language
configuration loading from YAML files.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import (
    DeckConfig,
    ElevenLabsConfig,
    LanguageConfig,
    LanguageFeatures,
    VoiceSettings,
)

# Path constants
BASE_DIR = Path(__file__).parent.parent.parent
LANGUAGES_DIR = BASE_DIR / "languages"
CACHE_DIR = BASE_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "output"


class Settings(BaseSettings):
    """Application settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    elevenlabs_api_key: str = Field(..., description="ElevenLabs API key")
    elevenlabs_voice_id: Optional[str] = Field(None, description="Override voice ID")
    default_language: str = Field("italian", description="Default language")
    audio_cache_dir: Path = Field(CACHE_DIR, description="Audio cache directory")


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()


def load_language_config(language: str) -> LanguageConfig:
    """Load language configuration from YAML file.

    Args:
        language: Language directory name (e.g., 'italian')

    Returns:
        LanguageConfig with all settings for the language

    Raises:
        FileNotFoundError: If language config doesn't exist
        ValueError: If config is invalid
    """
    config_path = LANGUAGES_DIR / language / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Language config not found: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Parse ElevenLabs config
    el_data = data.get("elevenlabs", {})
    voice_settings_data = el_data.get("voice_settings", {})
    voice_settings = VoiceSettings(**voice_settings_data)

    elevenlabs_config = ElevenLabsConfig(
        voice_id=el_data.get("voice_id"),
        voice_name=el_data.get("voice_name"),
        model_id=el_data.get("model_id", "eleven_multilingual_v2"),
        voice_settings=voice_settings,
    )

    # Parse deck config
    deck_data = data.get("deck", {})
    deck_config = DeckConfig(
        name_template=deck_data.get("name_template"),
        deck_id_base=deck_data.get("deck_id_base"),
        model_id_base=deck_data.get("model_id_base"),
    )

    # Parse features
    features_data = data.get("features", {})
    features = LanguageFeatures(
        has_gender=features_data.get("has_gender", False),
        has_articles=features_data.get("has_articles", False),
        gender_types=features_data.get("gender_types", []),
    )

    return LanguageConfig(
        language_code=data.get("language_code"),
        language_name=data.get("language_name"),
        native_name=data.get("native_name"),
        elevenlabs=elevenlabs_config,
        deck=deck_config,
        features=features,
    )


def list_available_languages() -> list[str]:
    """List all available language configurations.

    Returns:
        List of language directory names that have config.yaml
    """
    if not LANGUAGES_DIR.exists():
        return []

    languages = []
    for path in LANGUAGES_DIR.iterdir():
        if path.is_dir() and not path.name.startswith("_"):
            config_file = path / "config.yaml"
            if config_file.exists():
                languages.append(path.name)

    return sorted(languages)


def ensure_directories() -> None:
    """Create cache and output directories if they don't exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
