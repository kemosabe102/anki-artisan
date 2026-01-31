"""Text-to-speech service using ElevenLabs API.

This module handles audio generation with caching to minimize API calls
and manage character quotas efficiently.
"""

import hashlib
import logging
import time
from pathlib import Path
from typing import Optional

from elevenlabs import ElevenLabs
from elevenlabs import save as elevenlabs_save

from .config import CACHE_DIR, get_settings
from .models import GeneratedAudio, LanguageConfig, VoiceSettings

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-speech service with caching and retry logic."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TTS service.

        Args:
            api_key: ElevenLabs API key. If None, reads from settings.
        """
        if api_key is None:
            api_key = get_settings().elevenlabs_api_key

        self._client = ElevenLabs(api_key=api_key)
        self._total_characters = 0

    @property
    def total_characters_used(self) -> int:
        """Total characters sent to API (excludes cached)."""
        return self._total_characters

    def generate_audio(
        self,
        text: str,
        language_config: LanguageConfig,
        voice_id: Optional[str] = None,
    ) -> GeneratedAudio:
        """Generate audio for text, using cache if available.

        Args:
            text: Text to convert to speech
            language_config: Language configuration with voice settings
            voice_id: Override voice ID (uses config default if None)

        Returns:
            GeneratedAudio with file path and metadata
        """
        if voice_id is None:
            voice_id = language_config.elevenlabs.voice_id

        # Generate cache path
        cache_path = self._get_cache_path(
            text=text,
            language=language_config.language_code,
            voice_id=voice_id,
        )

        # Check cache first
        if cache_path.exists():
            logger.debug(f"Cache hit: {cache_path.name}")
            return GeneratedAudio(
                text=text,
                file_path=cache_path,
                cached=True,
                character_count=len(text),
            )

        # Generate new audio
        logger.info(f"Generating audio: '{text[:30]}...' ({len(text)} chars)")
        self._generate_with_retry(
            text=text,
            voice_id=voice_id,
            language_config=language_config,
            output_path=cache_path,
        )

        self._total_characters += len(text)

        return GeneratedAudio(
            text=text,
            file_path=cache_path,
            cached=False,
            character_count=len(text),
        )

    def _generate_with_retry(
        self,
        text: str,
        voice_id: str,
        language_config: LanguageConfig,
        output_path: Path,
        max_retries: int = 3,
    ) -> None:
        """Generate audio with exponential backoff retry.

        Args:
            text: Text to convert
            voice_id: ElevenLabs voice ID
            language_config: Language config with voice settings
            output_path: Where to save the audio file
            max_retries: Maximum retry attempts

        Raises:
            Exception: If all retries fail
        """
        settings = language_config.elevenlabs.voice_settings
        delays = [1, 2, 4]  # Exponential backoff

        for attempt in range(max_retries):
            try:
                # Prepare text with SSML break if configured
                tts_text = self._prepare_text_for_tts(text, settings)

                audio = self._client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=tts_text,
                    model_id=language_config.elevenlabs.model_id,
                    language_code=language_config.language_code,
                    output_format="mp3_44100_128",
                    voice_settings={
                        "stability": settings.stability,
                        "similarity_boost": settings.similarity_boost,
                        "style": settings.style,
                        "use_speaker_boost": settings.use_speaker_boost,
                        "speed": settings.speed,
                    },
                )

                # Ensure cache directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Save audio file
                elevenlabs_save(audio, str(output_path))
                logger.debug(f"Saved audio: {output_path}")
                return

            except Exception as e:
                if attempt < max_retries - 1:
                    delay = delays[attempt]
                    logger.warning(f"API error (attempt {attempt + 1}): {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise

    def _get_cache_path(self, text: str, language: str, voice_id: str) -> Path:
        """Generate cache file path for audio.

        Args:
            text: Source text
            language: Language code
            voice_id: Voice ID

        Returns:
            Path in format: cache/{language}/{voice_id}/{hash}.mp3
        """
        # Create hash from text + language + voice_id
        hash_input = f"{text}|{language}|{voice_id}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        return CACHE_DIR / language / voice_id / f"{hash_value}.mp3"

    def _prepare_text_for_tts(self, text: str, voice_settings: VoiceSettings) -> str:
        """Prepare text for TTS API, adding SSML break if configured.

        Args:
            text: Original text to speak
            voice_settings: Voice settings with leading_pause_seconds

        Returns:
            Text with SSML break tag if pause > 0, otherwise original text
        """
        pause = voice_settings.leading_pause_seconds
        if pause > 0:
            return f'<break time="{pause}s"/>{text}'
        return text

    def list_voices(self) -> list[dict]:
        """List available ElevenLabs voices.

        Returns:
            List of voice dictionaries with id, name, and labels
        """
        response = self._client.voices.get_all()

        voices = []
        for voice in response.voices:
            voices.append({
                "voice_id": voice.voice_id,
                "name": voice.name,
                "labels": voice.labels or {},
            })

        return voices
