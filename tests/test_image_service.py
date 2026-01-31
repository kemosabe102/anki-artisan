"""Tests for image generation service with mocked OpenAI API."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anki_artisan.image_service import ImageService
from anki_artisan.models import (
    Gender,
    GeneratedImage,
    ImageManifestEntry,
    PartOfSpeech,
    VocabItem,
)


def _make_vocab(word="casa", translation="house", pos=PartOfSpeech.NOUN):
    """Helper to create VocabItem for tests."""
    return VocabItem(
        word=word,
        translation=translation,
        phrase=f"La {word}.",
        phrase_translation=f"The {translation}.",
        part_of_speech=pos,
        gender=Gender.FEMININE,
    )


# Fake base64-encoded PNG (1x1 pixel)
_FAKE_B64_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
    "2mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


class TestImageServiceEligibility:
    """Tests for should_generate_image."""

    def test_noun_is_eligible(self):
        item = _make_vocab(pos=PartOfSpeech.NOUN)
        service = self._make_service()
        assert service.should_generate_image(item) is True

    def test_verb_is_eligible(self):
        item = _make_vocab(word="mangiare", translation="to eat", pos=PartOfSpeech.VERB)
        service = self._make_service()
        assert service.should_generate_image(item) is True

    def test_conjunction_not_eligible(self):
        item = _make_vocab(word="e", translation="and", pos=PartOfSpeech.CONJUNCTION)
        service = self._make_service()
        assert service.should_generate_image(item) is False

    def test_preposition_not_eligible(self):
        item = _make_vocab(word="di", translation="of", pos=PartOfSpeech.PREPOSITION)
        service = self._make_service()
        assert service.should_generate_image(item) is False

    def test_adjective_not_eligible(self):
        item = _make_vocab(word="grande", translation="big", pos=PartOfSpeech.ADJECTIVE)
        service = self._make_service()
        assert service.should_generate_image(item) is False

    def test_ineligible_returns_none(self):
        """Ineligible part of speech returns None from generate_image."""
        item = _make_vocab(word="ma", translation="but", pos=PartOfSpeech.CONJUNCTION)
        service = self._make_service()
        result = service.generate_image(item)
        assert result is None

    @staticmethod
    def _make_service():
        with patch("anki_artisan.image_service.OpenAI"):
            return ImageService(api_key="test_key")


class TestNormalizeTranslation:
    """Tests for _normalize_translation."""

    @patch("anki_artisan.image_service.OpenAI")
    def test_strips_the(self, mock_openai):
        service = ImageService(api_key="test_key")
        assert service._normalize_translation("the house") == "house"

    @patch("anki_artisan.image_service.OpenAI")
    def test_strips_a(self, mock_openai):
        service = ImageService(api_key="test_key")
        assert service._normalize_translation("a car") == "car"

    @patch("anki_artisan.image_service.OpenAI")
    def test_strips_an(self, mock_openai):
        service = ImageService(api_key="test_key")
        assert service._normalize_translation("an apple") == "apple"

    @patch("anki_artisan.image_service.OpenAI")
    def test_lowercases(self, mock_openai):
        service = ImageService(api_key="test_key")
        assert service._normalize_translation("House") == "house"

    @patch("anki_artisan.image_service.OpenAI")
    def test_no_article(self, mock_openai):
        service = ImageService(api_key="test_key")
        assert service._normalize_translation("laboratory") == "laboratory"


class TestGenerateImage:
    """Tests for generate_image with mocked API."""

    @patch("anki_artisan.image_service.IMAGE_CACHE_DIR")
    @patch("anki_artisan.image_service.OpenAI")
    def test_cache_miss_calls_api(self, mock_openai_class, mock_cache_dir, tmp_path):
        """API called on cache miss, manifest updated."""
        mock_cache_dir.__truediv__ = lambda self, other: tmp_path / other
        mock_cache_dir.mkdir = MagicMock()
        # Make Path operations work on tmp_path
        type(mock_cache_dir).exists = lambda self: tmp_path.exists()

        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Mock API response
        mock_image = MagicMock()
        mock_image.b64_json = _FAKE_B64_PNG
        mock_response = MagicMock()
        mock_response.data = [mock_image]
        mock_client.images.generate.return_value = mock_response

        with patch("anki_artisan.image_service.IMAGE_CACHE_DIR", tmp_path):
            service = ImageService(api_key="test_key")
            item = _make_vocab()
            result = service.generate_image(item)

        assert result is not None
        assert result.cached is False
        assert result.translation == "house"
        assert result.file_path.exists()
        mock_client.images.generate.assert_called_once()
        assert service.total_images_generated == 1

    @patch("anki_artisan.image_service.OpenAI")
    def test_cache_hit_no_api_call(self, mock_openai_class, tmp_path):
        """Existing manifest entry + file returns cached=True, no API call."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        with patch("anki_artisan.image_service.IMAGE_CACHE_DIR", tmp_path):
            service = ImageService(api_key="test_key")

            # Pre-populate manifest and file
            filename = service._generate_filename("house")
            (tmp_path / filename).write_bytes(b"fake png")
            service._manifest["house"] = ImageManifestEntry(
                translation="house",
                filename=filename,
                prompt="test prompt",
                generated_at="2026-01-01T00:00:00Z",
            )

            item = _make_vocab()
            result = service.generate_image(item)

        assert result is not None
        assert result.cached is True
        mock_client.images.generate.assert_not_called()
        assert service.total_images_generated == 0

    @patch("anki_artisan.image_service.OpenAI")
    def test_cross_language_sharing(self, mock_openai_class, tmp_path):
        """Same normalized translation returns same filename across languages."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        with patch("anki_artisan.image_service.IMAGE_CACHE_DIR", tmp_path):
            service = ImageService(api_key="test_key")

            # Both Italian "casa" and Spanish "casa" translate to "house"
            italian_item = _make_vocab(word="casa", translation="the house")
            spanish_item = _make_vocab(word="la casa", translation="a house")

            # Normalized keys should be identical
            key1 = service._normalize_translation(italian_item.translation)
            key2 = service._normalize_translation(spanish_item.translation)
            assert key1 == key2 == "house"

            # Filenames should be identical
            assert service._generate_filename(key1) == service._generate_filename(key2)

    @patch("anki_artisan.image_service.time.sleep")
    @patch("anki_artisan.image_service.OpenAI")
    def test_retry_on_api_error(self, mock_openai_class, mock_sleep, tmp_path):
        """API fails twice, succeeds on 3rd attempt."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # First two calls fail, third succeeds
        mock_image = MagicMock()
        mock_image.b64_json = _FAKE_B64_PNG
        mock_response = MagicMock()
        mock_response.data = [mock_image]

        mock_client.images.generate.side_effect = [
            Exception("Rate limit"),
            Exception("Timeout"),
            mock_response,
        ]

        with patch("anki_artisan.image_service.IMAGE_CACHE_DIR", tmp_path):
            service = ImageService(api_key="test_key")
            item = _make_vocab()
            result = service.generate_image(item)

        assert result is not None
        assert result.cached is False
        assert mock_client.images.generate.call_count == 3
        assert mock_sleep.call_count == 2
