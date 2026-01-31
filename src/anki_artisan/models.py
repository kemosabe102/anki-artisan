"""Pydantic data models for Anki Artisan.

This module defines all data models used throughout the application,
including vocabulary items, language configurations, and audio metadata.
"""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PartOfSpeech(str, Enum):
    """Grammatical categories for vocabulary items."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    PRONOUN = "pronoun"
    INTERJECTION = "interjection"
    PHRASE = "phrase"
    IDIOM = "idiom"
    PROVERB = "proverb"


class Gender(str, Enum):
    """Grammatical gender for European languages.

    Extended to support various European language systems:
    - m/f: Italian, Spanish, French, Portuguese
    - m/f/n: German
    - c: Swedish, Danish (common gender)
    - mf: Dual gender words (e.g., Italian "il/la nipote")
    - na: Not applicable (English, verbs, adverbs)
    """

    MASCULINE = "m"
    FEMININE = "f"
    NEUTER = "n"
    DUAL = "mf"
    COMMON = "c"
    NOT_APPLICABLE = "n/a"


class VocabItem(BaseModel):
    """A single vocabulary item with word, translation, and example phrase."""

    word: str = Field(..., min_length=1, description="Target language word")
    translation: str = Field(..., min_length=1, description="English translation")
    phrase: str = Field(..., min_length=1, description="Example phrase (≤6 words)")
    phrase_translation: str = Field(..., min_length=1, description="English phrase translation")
    part_of_speech: PartOfSpeech
    gender: Gender = Gender.NOT_APPLICABLE
    tags: list[str] = Field(default_factory=list)

    @field_validator("phrase")
    @classmethod
    def validate_phrase_length(cls, v: str) -> str:
        """Ensure phrase has at most 6 words."""
        word_count = len(v.split())
        if word_count > 6:
            raise ValueError(f"Phrase must have ≤6 words, got {word_count}: '{v}'")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: str | list[str] | None) -> list[str]:
        """Parse tags from space-separated string or list."""
        if v is None or v == "":
            return []
        if isinstance(v, str):
            return v.split()
        return v


class VoiceSettings(BaseModel):
    """ElevenLabs voice settings for audio generation."""

    stability: float = Field(0.7, ge=0.0, le=1.0, description="Voice consistency")
    similarity_boost: float = Field(0.8, ge=0.0, le=1.0, description="Voice adherence")
    style: float = Field(0.0, ge=0.0, le=1.0, description="Expressive variation")
    use_speaker_boost: bool = Field(True, description="Speaker boost enhancement")
    speed: float = Field(0.9, ge=0.5, le=2.0, description="Speech speed")
    leading_pause_seconds: float = Field(
        0.0, ge=0.0, le=3.0, description="Leading pause to prevent audio truncation"
    )


class ElevenLabsConfig(BaseModel):
    """ElevenLabs API configuration for a language."""

    voice_id: str = Field(..., min_length=1, description="Primary voice ID")
    voice_name: Optional[str] = Field(None, description="Voice display name")
    model_id: str = Field("eleven_multilingual_v2", description="TTS model ID")
    voice_settings: VoiceSettings = Field(default_factory=VoiceSettings)


class DeckConfig(BaseModel):
    """Anki deck configuration."""

    name_template: str = Field(..., description="Deck name template with {level} placeholder")
    deck_id_base: int = Field(..., description="Base deck ID for uniqueness")
    model_id_base: int = Field(..., description="Base model ID for uniqueness")


class LanguageFeatures(BaseModel):
    """Language-specific grammatical features."""

    has_gender: bool = False
    has_articles: bool = False
    gender_types: list[str] = Field(default_factory=list)


class LanguageConfig(BaseModel):
    """Complete configuration for a language."""

    language_code: str = Field(..., min_length=2, max_length=5, description="ISO language code")
    language_name: str = Field(..., min_length=1, description="English language name")
    native_name: Optional[str] = Field(None, description="Native language name")
    elevenlabs: ElevenLabsConfig
    deck: DeckConfig
    features: LanguageFeatures = Field(default_factory=LanguageFeatures)


class GeneratedAudio(BaseModel):
    """Metadata for a generated audio file."""

    text: str = Field(..., description="Source text that was converted to speech")
    file_path: Path = Field(..., description="Path to the audio file")
    cached: bool = Field(False, description="Whether the audio was loaded from cache")
    character_count: int = Field(..., ge=0, description="Character count for quota tracking")

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True
