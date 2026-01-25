# Anki Artisan

Artisan-crafted Anki flashcard decks with neural TTS. Generate custom language learning decks with high-quality audio pronunciation using ElevenLabs AI.

## Overview

Anki Artisan is a Python-based Anki deck generator that creates professional-quality flashcard decks with neural text-to-speech audio. Built with a language-agnostic architecture, it currently supports Italian and is designed to easily expand to other languages like Spanish, French, and more.

## Key Features

- **Neural TTS Audio**: High-quality pronunciation using ElevenLabs AI voices
- **Automated Deck Generation**: Create `.apkg` files programmatically with genanki
- **Smart Audio Caching**: Prevents redundant API calls and reduces costs
- **Multi-Language Support**: Framework designed for easy language expansion
- **Type-Safe**: Built with Pydantic for data validation and type safety
- **CLI Interface**: Simple command-line interface for deck generation

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.10+ | Primary development language |
| Deck Generation | genanki | Creates .apkg files programmatically |
| Audio Generation | ElevenLabs API | Neural TTS for pronunciation |
| HTTP Client | requests | API calls to ElevenLabs |
| Data Validation | pydantic | Type-safe data models |
| Package Manager | uv | Fast Python package management |

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- ElevenLabs API key ([sign up here](https://elevenlabs.io/))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kemosabe102/anki-artisan.git
cd anki-artisan
```

2. Install dependencies using uv:
```bash
uv pip install -e .
```

3. Configure your ElevenLabs API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. Set up your API key in `.env`:
```
ELEVENLABS_API_KEY=your_actual_api_key_here
```

## Usage

### Generate a Deck

```bash
anki-artisan generate --language italian --output my_italian_deck.apkg
```

### Specify Custom Vocabulary File

```bash
anki-artisan generate --language italian --vocab custom_words.csv --output deck.apkg
```

### List Available Languages

```bash
anki-artisan list-languages
```

## Project Structure

```
anki-artisan/
├── README.md
├── .gitignore
├── LICENSE
├── pyproject.toml          # Project configuration with uv
├── .env.example            # ElevenLabs API key template
├── languages/              # Language-specific data
│   ├── italian/
│   │   ├── vocabulary.csv  # Word pairs and examples
│   │   └── config.json     # Language configuration
│   ├── spanish/
│   └── french/
├── src/
│   └── anki_artisan/
│       ├── __init__.py
│       ├── cli.py          # CLI interface
│       ├── deck_builder.py # Core deck generation
│       ├── audio_gen.py    # ElevenLabs integration
│       ├── models.py       # Pydantic models
│       └── cache.py        # Audio caching logic
├── templates/              # Anki card templates
│   └── language_card.html
├── tests/                  # Unit tests
└── cache/                  # Cached audio files (gitignored)
```

## Adding New Languages

Anki Artisan is designed to make adding new languages straightforward:

1. Create a new directory under `languages/`:
```bash
mkdir -p languages/spanish
```

2. Create `vocabulary.csv`:
```csv
spanish,english,example_sentence
hola,hello,¡Hola! ¿Cómo estás?
gracias,thank you,Gracias por tu ayuda.
```

3. Create `config.json`:
```json
{
  "language_code": "es",
  "language_name": "Spanish",
  "elevenlabs_voice_id": "spanish_voice_id_from_elevenlabs",
  "card_template": "language_card.html"
}
```

4. Generate your deck:
```bash
anki-artisan generate --language spanish --output spanish_deck.apkg
```

## Architecture

### Language-Agnostic Design

- **Core Logic**: Deck generation logic is completely language-independent
- **Configuration-Driven**: Each language is defined by its vocabulary and config files
- **Flexible Templates**: Shared HTML templates with variable substitution
- **Smart Caching**: Audio files are cached using hash keys (word + language + voice_id)

### Audio Caching Strategy

To minimize API costs and improve performance:
- Audio files are hashed using `hashlib` based on content and language
- Cached in the `cache/` directory (gitignored)
- Automatically reused for repeated words
- Significant cost savings for large decks

### Security

- API keys stored in `.env` file (gitignored)
- `.env.example` provides template without exposing secrets
- Never commit sensitive credentials to version control

## Development

### Install Development Dependencies

```bash
uv pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
ruff check src/ tests/
```

## Roadmap

- [ ] Implement core deck generation logic
- [ ] Integrate ElevenLabs API
- [ ] Add unit tests
- [ ] Support for Spanish and French
- [ ] Custom card template system
- [ ] Batch processing for large vocabulary lists
- [ ] Progress indicators for long operations
- [ ] Export statistics and analytics

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [genanki](https://github.com/kerrickstaley/genanki) for Anki deck generation
- [ElevenLabs](https://elevenlabs.io/) for neural TTS technology
- [uv](https://github.com/astral-sh/uv) for fast Python package management
