# Development Guide

## Environment Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- ElevenLabs API key ([sign up](https://elevenlabs.io/))

### Installation

```bash
# Clone repository
git clone https://github.com/kemosabe102/anki-artisan.git
cd anki-artisan

# Install with uv
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"
```

### Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
ELEVENLABS_API_KEY=your_actual_api_key_here
```

---

## CLI Usage

### Generate a Deck

```bash
# Basic generation
anki-artisan generate --language italian --output my_deck.apkg

# With custom vocabulary file
anki-artisan generate --language italian --vocab custom_words.csv --output deck.apkg

# Verbose mode
anki-artisan generate --language italian --output deck.apkg --verbose
```

### Validation & Testing

```bash
# Dry run - validate CSV without calling API
anki-artisan generate --language italian --dry-run

# Use only cached audio (no API calls)
anki-artisan generate --language italian --cache-only
```

### Voice Management

```bash
# List available ElevenLabs voices
anki-artisan --list-voices
```

---

## Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/anki_artisan

# Specific test file
pytest tests/test_models.py

# Verbose output
pytest -v
```

### Test Structure

```
tests/
├── test_models.py       # Pydantic model tests
├── test_csv_reader.py   # CSV parsing tests
├── test_tts_service.py  # TTS service tests (mocked)
├── test_deck_builder.py # Deck generation tests
└── conftest.py          # Shared fixtures
```

---

## Code Quality

### Formatting

```bash
# Format with black
black src/ tests/

# Check only (no changes)
black src/ tests/ --check
```

### Linting

```bash
# Run ruff
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix
```

### Type Checking (optional)

```bash
mypy src/anki_artisan
```

---

## Adding New Languages

### 1. Create Language Directory

```bash
mkdir -p languages/spanish
```

### 2. Create vocabulary.csv

```csv
spanish,english,example_sentence,part_of_speech,gender,tags
hola,hello,¡Hola! ¿Cómo estás?,interjection,n/a,a1 greetings
gracias,thank you,Gracias por tu ayuda.,noun,f,a1 common
```

### 3. Create config.json

```json
{
  "language_code": "es",
  "language_name": "Spanish",
  "elevenlabs_voice_id": "spanish_voice_id_here",
  "card_template": "language_card.html"
}
```

### 4. Generate Deck

```bash
anki-artisan generate --language spanish --output spanish_deck.apkg
```

---

## Project Architecture

### Data Flow

```
CSV File → csv_reader.py → VocabItem models
                              ↓
                         tts_service.py → ElevenLabs API
                              ↓
                         Audio files (cached)
                              ↓
                         deck_builder.py → .apkg file
```

### Key Modules

| Module | Responsibility |
|--------|---------------|
| `cli.py` | Command-line interface, argument parsing |
| `models.py` | Pydantic data models, validation |
| `csv_reader.py` | CSV parsing, row validation |
| `tts_service.py` | ElevenLabs API, audio caching |
| `deck_builder.py` | genanki deck/note creation |

---

## Debugging

### Common Issues

| Issue | Solution |
|-------|----------|
| Missing API key | Set `ELEVENLABS_API_KEY` in `.env` |
| Invalid voice ID | Run `--list-voices` to get valid IDs |
| CSV validation error | Check column names match spec |
| Phrase too long | Keep phrases ≤6 words |

### Verbose Mode

```bash
anki-artisan generate --language italian --verbose
```

Shows:
- CSV parsing progress
- API calls being made
- Cache hits/misses
- Character usage

---

## Git Workflow

### Before Committing

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Run tests
pytest
```

### Commit Message Format

```
type: brief description

- Detail 1
- Detail 2
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
