"""Command-line interface for Anki Artisan.

This module provides the main entry point and CLI commands for
generating Anki flashcard decks with TTS audio.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

from .config import (
    OUTPUT_DIR,
    ensure_directories,
    get_settings,
    list_available_languages,
    load_language_config,
)
from .csv_reader import load_vocabulary
from .deck_builder import DeckBuilder
from .image_service import ImageService
from .tts_service import TTSService


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def cmd_list_languages(args: argparse.Namespace) -> int:
    """List available languages."""
    languages = list_available_languages()

    if not languages:
        print("No languages configured.")
        return 1

    print("Available languages:")
    for lang in languages:
        config = load_language_config(lang)
        print(f"  - {lang}: {config.language_name} ({config.native_name or config.language_code})")

    return 0


def cmd_list_voices(args: argparse.Namespace) -> int:
    """List available ElevenLabs voices."""
    try:
        tts = TTSService()
        voices = tts.list_voices()

        print(f"Available voices ({len(voices)}):")
        for voice in voices:
            labels = voice.get("labels", {})
            accent = labels.get("accent", "")
            gender = labels.get("gender", "")
            info = f"{accent} {gender}".strip()
            print(f"  - {voice['name']}")
            print(f"    ID: {voice['voice_id']}")
            if info:
                print(f"    Info: {info}")

        return 0

    except Exception as e:
        print(f"Error listing voices: {e}")
        return 1


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate an Anki deck."""
    language = args.language
    level = args.level.lower()
    output_path = args.output
    voice_id_override = args.voice_id
    dry_run = args.dry_run
    cache_only = args.cache_only
    skip_images = args.skip_images
    images_only = args.images_only

    # Validate mutually exclusive flags
    if skip_images and images_only:
        print("Error: --skip-images and --images-only are mutually exclusive")
        return 1

    # Validate language
    available = list_available_languages()
    if language not in available:
        print(f"Error: Language '{language}' not found. Available: {', '.join(available)}")
        return 1

    # Load configuration
    try:
        config = load_language_config(language)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    # Load vocabulary
    try:
        vocab_items = load_vocabulary(language, level)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    if not vocab_items:
        print(f"Error: No vocabulary items found for {language}/{level}")
        return 1

    print(f"Loaded {len(vocab_items)} vocabulary items for {config.language_name} {level.upper()}")

    # Dry run - just validate
    if dry_run:
        print("\n[Dry run] Validation successful!")
        print(f"  Language: {config.language_name}")
        print(f"  Level: {level.upper()}")
        print(f"  Items: {len(vocab_items)}")
        print(f"  Voice: {config.elevenlabs.voice_name or config.elevenlabs.voice_id}")
        return 0

    # Ensure directories exist
    ensure_directories()

    # Initialize TTS service (skip if images_only)
    tts = None
    if not images_only:
        try:
            tts = TTSService()
        except Exception as e:
            print(f"Error initializing TTS service: {e}")
            return 1

    # Initialize image service (skip if skip_images)
    image_service = None
    if not skip_images:
        settings = get_settings()
        if settings.openai_api_key:
            try:
                image_service = ImageService()
            except Exception as e:
                print(f"Error initializing image service: {e}")
                return 1
        else:
            logger.warning("OPENAI_API_KEY not set, skipping images")

    # Use override voice ID if provided
    voice_id = voice_id_override or config.elevenlabs.voice_id

    # Generate audio and images for all items
    if tts:
        print(f"\nGenerating audio using voice: {voice_id}")
    if image_service:
        print("Generating images...")

    audio_map: dict[str, tuple] = {}
    image_map: dict[str, object] = {}

    for i, item in enumerate(vocab_items, 1):
        print(f"  [{i}/{len(vocab_items)}] {item.word}...")

        # Audio generation (skip if images_only)
        if tts:
            try:
                word_audio = tts.generate_audio(item.word, config, voice_id)
                phrase_audio = tts.generate_audio(item.phrase, config, voice_id)
                audio_map[item.word] = (word_audio, phrase_audio)

                status = "cached" if word_audio.cached and phrase_audio.cached else "generated"
                print(f"    audio: {status}")

            except Exception as e:
                print(f"    Audio error: {e}")
                return 1

        # Image generation
        if image_service:
            try:
                image = image_service.generate_image(item)
                if image:
                    image_map[item.word] = image
                    img_status = "cached" if image.cached else "generated"
                    print(f"    image: {img_status}")
            except Exception as e:
                print(f"    Image error: {e}")
                return 1

    # Summaries
    if tts:
        print(f"\nAudio: {tts.total_characters_used} characters used")
    if image_service:
        n = image_service.total_images_generated
        print(f"Images: {n} generated, ~${image_service.estimated_cost:.2f}")

    # Cache only modes - skip deck building
    if cache_only or images_only:
        print("\n[Cache mode] Complete!")
        return 0

    # Build deck
    print("\nBuilding Anki deck...")
    builder = DeckBuilder(config, level)

    for item in vocab_items:
        word_audio, phrase_audio = audio_map[item.word]
        image = image_map.get(item.word)
        builder.add_vocab_item(item, word_audio, phrase_audio, image=image)

    # Determine output path
    if output_path is None:
        output_path = OUTPUT_DIR / f"{language}_{level}.apkg"
    else:
        output_path = Path(output_path)

    # Write package
    final_path = builder.build_package(output_path)

    print(f"\n✓ Deck created: {final_path}")
    print(f"  Notes: {builder.note_count}")
    print(f"  Cards: {builder.note_count * 3} (3 card types per note)")

    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="anki-artisan",
        description="Generate Anki flashcard decks with neural TTS audio",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list-languages command
    subparsers.add_parser(
        "list-languages",
        help="List available languages",
    )

    # list-voices command
    subparsers.add_parser(
        "list-voices",
        help="List available ElevenLabs voices",
    )

    # generate command
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate an Anki deck",
    )
    gen_parser.add_argument(
        "--language", "-l",
        required=True,
        help="Language to generate (e.g., italian)",
    )
    gen_parser.add_argument(
        "--level",
        default="a1",
        help="CEFR level (default: a1)",
    )
    gen_parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for .apkg file",
    )
    gen_parser.add_argument(
        "--voice-id",
        help="Override default voice ID",
    )
    gen_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate only, don't generate audio or deck",
    )
    gen_parser.add_argument(
        "--cache-only",
        action="store_true",
        help="Generate audio cache only, skip deck building",
    )
    gen_parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip image generation (audio only)",
    )
    gen_parser.add_argument(
        "--images-only",
        action="store_true",
        help="Generate image cache only, skip audio and deck building",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    setup_logging(args.verbose)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "list-languages":
        return cmd_list_languages(args)
    elif args.command == "list-voices":
        return cmd_list_voices(args)
    elif args.command == "generate":
        return cmd_generate(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
