"""Anki deck builder using genanki.

This module creates Anki flashcard decks with vocabulary items,
audio files, and three card types for comprehensive learning.
"""

import logging
from pathlib import Path
from typing import Optional

import genanki

from .models import GeneratedAudio, GeneratedImage, LanguageConfig, VocabItem

logger = logging.getLogger(__name__)

# Card template CSS
CARD_CSS = """
.card {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 24px;
    text-align: center;
    color: #333;
    background-color: #fafafa;
    padding: 20px;
}

.word {
    font-size: 32px;
    font-weight: bold;
    color: #2e7d32;
    margin-bottom: 10px;
}

.translation {
    font-size: 28px;
    color: #1565c0;
    margin-bottom: 15px;
}

.phrase {
    font-size: 20px;
    font-style: italic;
    color: #555;
    margin: 10px 0;
}

.phrase-translation {
    font-size: 18px;
    color: #666;
    margin: 5px 0;
}

.meta {
    font-size: 16px;
    color: #888;
    margin-top: 15px;
}

.pos {
    background-color: #e8f5e9;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 5px;
}

.gender {
    background-color: #e3f2fd;
    padding: 2px 8px;
    border-radius: 4px;
}

.listening-prompt {
    font-size: 20px;
    color: #ff9800;
    margin-bottom: 20px;
}

.image {
    margin: 10px auto;
    max-width: 256px;
}
.image img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}
"""


class DeckBuilder:
    """Builder for Anki vocabulary decks with audio."""

    def __init__(self, language_config: LanguageConfig, level: str):
        """Initialize deck builder.

        Args:
            language_config: Language configuration
            level: CEFR level (a1, a2, b1, etc.)
        """
        self._config = language_config
        self._level = level.upper()

        # Create unique IDs based on config
        deck_id = language_config.deck.deck_id_base + hash(level) % 1000
        model_id = language_config.deck.model_id_base + hash(level) % 1000

        # Create note model with 9 fields
        self._model = genanki.Model(
            model_id,
            f"{language_config.language_name} Vocabulary",
            fields=[
                {"name": "Word"},
                {"name": "Translation"},
                {"name": "Phrase"},
                {"name": "PhraseTranslation"},
                {"name": "WordAudio"},
                {"name": "PhraseAudio"},
                {"name": "PartOfSpeech"},
                {"name": "Gender"},
                {"name": "Image"},
            ],
            templates=[
                self._recognition_template(),
                self._production_template(),
                self._listening_template(),
            ],
            css=CARD_CSS,
        )

        # Create deck
        deck_name = language_config.deck.name_template.format(level=self._level)
        self._deck = genanki.Deck(deck_id, deck_name)

        # Track media files
        self._media_files: list[str] = []

    def _recognition_template(self) -> dict:
        """Recognition card: Target → English."""
        return {
            "name": "Recognition",
            "qfmt": """
                <div class="word">{{Word}}</div>
                {{WordAudio}}
            """,
            "afmt": """
                {{FrontSide}}
                <hr>
                <div class="translation">{{Translation}}</div>
                {{#Image}}<div class="image">{{Image}}</div>{{/Image}}
                <div class="phrase">{{Phrase}}</div>
                {{PhraseAudio}}
                <div class="phrase-translation">{{PhraseTranslation}}</div>
                <div class="meta">
                    <span class="pos">{{PartOfSpeech}}</span>
                    <span class="gender">{{Gender}}</span>
                </div>
            """,
        }

    def _production_template(self) -> dict:
        """Production card: English → Target."""
        return {
            "name": "Production",
            "qfmt": """
                <div class="translation">{{Translation}}</div>
            """,
            "afmt": """
                {{FrontSide}}
                <hr>
                <div class="word">{{Word}}</div>
                {{WordAudio}}
                {{#Image}}<div class="image">{{Image}}</div>{{/Image}}
                <div class="phrase">{{Phrase}}</div>
                {{PhraseAudio}}
                <div class="phrase-translation">{{PhraseTranslation}}</div>
                <div class="meta">
                    <span class="pos">{{PartOfSpeech}}</span>
                    <span class="gender">{{Gender}}</span>
                </div>
            """,
        }

    def _listening_template(self) -> dict:
        """Listening card: Audio Only → All."""
        return {
            "name": "Listening",
            "qfmt": """
                <div class="listening-prompt">🎧 Listen and identify:</div>
                {{WordAudio}}
            """,
            "afmt": """
                {{FrontSide}}
                <hr>
                <div class="word">{{Word}}</div>
                <div class="translation">{{Translation}}</div>
                <div class="phrase">{{Phrase}}</div>
                {{PhraseAudio}}
                <div class="phrase-translation">{{PhraseTranslation}}</div>
                <div class="meta">
                    <span class="pos">{{PartOfSpeech}}</span>
                    <span class="gender">{{Gender}}</span>
                </div>
            """,
        }

    def add_vocab_item(
        self,
        vocab: VocabItem,
        word_audio: GeneratedAudio,
        phrase_audio: GeneratedAudio,
        image: Optional[GeneratedImage] = None,
    ) -> None:
        """Add a vocabulary item to the deck.

        Args:
            vocab: Vocabulary item data
            word_audio: Generated audio for the word
            phrase_audio: Generated audio for the phrase
            image: Optional generated image for the vocabulary item
        """
        # Get audio filenames
        word_audio_file = word_audio.file_path.name
        phrase_audio_file = phrase_audio.file_path.name

        # Build image field
        image_field = f'<img src="{image.file_path.name}">' if image else ""

        # Create note with all 9 fields
        note = genanki.Note(
            model=self._model,
            fields=[
                vocab.word,
                vocab.translation,
                vocab.phrase,
                vocab.phrase_translation,
                f"[sound:{word_audio_file}]",
                f"[sound:{phrase_audio_file}]",
                vocab.part_of_speech.value,
                vocab.gender.value,
                image_field,
            ],
        )

        self._deck.add_note(note)

        # Track media files
        self._media_files.append(str(word_audio.file_path))
        self._media_files.append(str(phrase_audio.file_path))
        if image:
            self._media_files.append(str(image.file_path))

        logger.debug(f"Added note: {vocab.word}")

    def build_package(self, output_path: Path) -> Path:
        """Build and save the Anki package.

        Args:
            output_path: Path for the .apkg file

        Returns:
            Path to the created package
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create package with media
        package = genanki.Package(self._deck)
        package.media_files = self._media_files

        package.write_to_file(str(output_path))

        logger.info(f"Created deck: {output_path} ({self.note_count} items, {len(self._media_files)} media files)")
        return output_path

    @property
    def note_count(self) -> int:
        """Number of notes in the deck."""
        return len(self._deck.notes)
