"""Image generation service using OpenAI gpt-image-1.

This module handles AI image generation with manifest-based caching.
Images are keyed by normalized English translation, enabling cross-language
sharing (e.g., Italian "casa" and Spanish "casa" share the same "house" image).
"""

import base64
import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from openai import OpenAI

from .config import IMAGE_CACHE_DIR, get_settings
from .models import GeneratedImage, ImageManifestEntry, PartOfSpeech, VocabItem

logger = logging.getLogger(__name__)

# Parts of speech eligible for image generation
_IMAGE_ELIGIBLE = {PartOfSpeech.NOUN, PartOfSpeech.VERB}

_BASE_PROMPT = (
    "A simple, clean illustration on a plain white background. "
    "Flat design style with bold outlines and vibrant colors. "
    "No text, no labels, no watermarks. "
    "Suitable for a language learning flashcard. "
)

_MANIFEST_FILE = "manifest.json"


class ImageService:
    """Image generation service with manifest-based caching."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the image service.

        Args:
            api_key: OpenAI API key. If None, reads from settings.
        """
        if api_key is None:
            api_key = get_settings().openai_api_key

        if not api_key:
            raise ValueError("OpenAI API key is required for image generation")

        self._client = OpenAI(api_key=api_key)
        self._total_generated = 0
        self._manifest = self._load_manifest()

    @property
    def total_images_generated(self) -> int:
        """Total images generated via API (excludes cached)."""
        return self._total_generated

    @property
    def estimated_cost(self) -> float:
        """Estimated cost at $0.02 per image (quality='low')."""
        return self._total_generated * 0.02

    def should_generate_image(self, vocab_item: VocabItem) -> bool:
        """Check if a vocabulary item is eligible for image generation.

        Args:
            vocab_item: Vocabulary item to check

        Returns:
            True for nouns and verbs, False otherwise
        """
        return vocab_item.part_of_speech in _IMAGE_ELIGIBLE

    def generate_image(self, vocab_item: VocabItem) -> Optional[GeneratedImage]:
        """Generate an image for a vocabulary item, using cache if available.

        Args:
            vocab_item: Vocabulary item to generate image for

        Returns:
            GeneratedImage with file path and metadata, or None if ineligible
        """
        if not self.should_generate_image(vocab_item):
            return None

        normalized = self._normalize_translation(vocab_item.translation)
        prompt = self._build_prompt(normalized, vocab_item.part_of_speech)

        # Check manifest cache
        if normalized in self._manifest:
            entry = self._manifest[normalized]
            file_path = IMAGE_CACHE_DIR / entry.filename
            if file_path.exists():
                logger.debug(f"Image cache hit: {normalized}")
                return GeneratedImage(
                    translation=normalized,
                    file_path=file_path,
                    cached=True,
                    prompt=entry.prompt,
                )
            # File missing from disk, regenerate
            logger.warning(f"Manifest entry exists but file missing: {entry.filename}")

        # Generate new image
        filename = self._generate_filename(normalized)
        output_path = IMAGE_CACHE_DIR / filename

        logger.info(f"Generating image for: '{normalized}'")
        self._generate_with_retry(prompt, output_path)
        self._total_generated += 1

        # Update manifest
        entry = ImageManifestEntry(
            translation=normalized,
            filename=filename,
            prompt=prompt,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._manifest[normalized] = entry
        self._save_manifest()

        return GeneratedImage(
            translation=normalized,
            file_path=output_path,
            cached=False,
            prompt=prompt,
        )

    def _normalize_translation(self, translation: str) -> str:
        """Normalize English translation for use as cache key.

        Strips leading articles and lowercases.

        Args:
            translation: Raw English translation

        Returns:
            Normalized string (e.g., "the house" -> "house")
        """
        normalized = translation.strip().lower()
        for prefix in ("the ", "a ", "an "):
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
                break
        return normalized.strip()

    def _load_manifest(self) -> dict[str, ImageManifestEntry]:
        """Load image manifest from disk.

        Returns:
            Dictionary mapping normalized translations to manifest entries
        """
        manifest_path = IMAGE_CACHE_DIR / _MANIFEST_FILE
        if not manifest_path.exists():
            return {}

        try:
            with open(manifest_path, encoding="utf-8") as f:
                data = json.load(f)
            return {
                key: ImageManifestEntry(**value) for key, value in data.items()
            }
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to load manifest: {e}")
            return {}

    def _save_manifest(self) -> None:
        """Write manifest to disk."""
        manifest_path = IMAGE_CACHE_DIR / _MANIFEST_FILE
        IMAGE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

        data = {key: entry.model_dump() for key, entry in self._manifest.items()}
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _build_prompt(self, translation: str, pos: PartOfSpeech) -> str:
        """Build image generation prompt.

        Args:
            translation: Normalized English translation
            pos: Part of speech

        Returns:
            Full prompt string for the API
        """
        if pos == PartOfSpeech.VERB:
            return f"{_BASE_PROMPT}Show a person performing the action: {translation}."
        return f"{_BASE_PROMPT}Subject: {translation}."

    def _generate_with_retry(
        self, prompt: str, output_path: Path, max_retries: int = 3
    ) -> None:
        """Call OpenAI API to generate image with exponential backoff.

        Args:
            prompt: Image generation prompt
            output_path: Where to save the PNG file
            max_retries: Maximum retry attempts

        Raises:
            Exception: If all retries fail
        """
        delays = [1, 2, 4]

        for attempt in range(max_retries):
            try:
                response = self._client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    quality="low",
                )

                # Decode base64 image data and write PNG
                image_data = base64.b64decode(response.data[0].b64_json)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_data)
                logger.debug(f"Saved image: {output_path}")
                return

            except Exception as e:
                if attempt < max_retries - 1:
                    delay = delays[attempt]
                    logger.warning(
                        f"Image API error (attempt {attempt + 1}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"Image generation failed after {max_retries} attempts: {e}")
                    raise

    def _generate_filename(self, normalized_key: str) -> str:
        """Generate deterministic filename from cache key.

        Args:
            normalized_key: Normalized English translation

        Returns:
            Filename like "a1b2c3d4e5f67890.png"
        """
        hash_value = hashlib.sha256(normalized_key.encode()).hexdigest()[:16]
        return f"{hash_value}.png"
